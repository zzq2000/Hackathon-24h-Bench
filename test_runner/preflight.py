"""
Runtime dependency preflight checks for test_runner.

The preflight step runs before benchmark cycles and attempts to:
1) Detect required runtime dependencies from selected system/bench/tier configs.
2) Auto-install missing Python dependencies.
3) Ensure Docker daemon is usable and required images are pulled.

When a non-auto-fixable dependency is missing (for example `git`), the
preflight raises RuntimeError with actionable details.
"""

from __future__ import annotations

import hashlib
import importlib.util
import logging
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

try:
    import tomllib
except Exception:  # pragma: no cover - fallback for older Python runtimes
    try:
        import tomli as tomllib  # type: ignore[no-redef]
    except Exception:
        tomllib = None

logger = logging.getLogger(__name__)


@dataclass
class PreflightPlan:
    """Concrete dependency operations inferred from current run configuration."""

    python_packages: Set[Tuple[str, Optional[str]]] = field(default_factory=set)
    required_commands: Set[str] = field(default_factory=set)
    require_docker: bool = False
    docker_images: Set[str] = field(default_factory=set)
    docker_builds: List["DockerBuildSpec"] = field(default_factory=list)
    need_cispa_setup: bool = False
    cispa_repo: str = "https://github.com/cispa/http-conformance.git"
    need_cispa_postgres: bool = False
    cispa_postgres_image: str = "postgres:15-alpine"


@dataclass(frozen=True)
class DockerBuildSpec:
    """Definition for a local Docker image that must be built before running."""

    image: str
    context: str
    dockerfile: str
    build_args: Tuple[Tuple[str, str], ...] = ()


class DependencyPreflight:
    """Performs dependency checks + auto-setup for selected benchmarks."""

    _DOCKER_BUILD_FINGERPRINT_LABEL = "hackathon-24h-bench.build-fingerprint"

    _IMPORT_OVERRIDES: Dict[str, str] = {
        "python-dotenv": "dotenv",
        "pyyaml": "yaml",
        "jinja2": "jinja2",
        "flask": "flask",
        "werkzeug": "werkzeug",
        "scikit-learn": "sklearn",
        "strenum": "strenum",
        "psycopg2": "psycopg2",
        "psycopg2-binary": "psycopg2",
    }

    def __init__(self, *, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._pip_installed_specs: Set[str] = set()
        self._docker_ok: Optional[Tuple[bool, str]] = None

    def run(
        self,
        *,
        system_type: str,
        tiers: Sequence[str],
        benchmarks: Sequence[str],
        tier_configs: Dict[str, Dict[str, Any]],
        docker_cfg: Dict[str, Any],
    ) -> None:
        plan = self._build_plan(
            system_type=system_type,
            tiers=tiers,
            benchmarks=benchmarks,
            tier_configs=tier_configs,
            docker_cfg=docker_cfg,
        )

        logger.info("Running dependency preflight...")

        # Commands first
        for cmd in sorted(plan.required_commands):
            self._ensure_command(cmd)

        # Python packages
        for spec, import_name in sorted(plan.python_packages):
            self._ensure_python_package(spec, import_name=import_name)

        # cispa setup may install additional deps inferred from pyproject.toml
        if plan.need_cispa_setup:
            self._prepare_cispa_dependencies(plan.cispa_repo)

        # Docker checks + image pulls
        if plan.require_docker:
            self._ensure_docker_usable()
            for build in plan.docker_builds:
                self._ensure_docker_build(build)
            for image in sorted(plan.docker_images):
                self._ensure_docker_image(image)

        if plan.need_cispa_postgres:
            self._check_cispa_postgres_available(plan.cispa_postgres_image)

        logger.info("Dependency preflight completed.")

    def _build_plan(
        self,
        *,
        system_type: str,
        tiers: Sequence[str],
        benchmarks: Sequence[str],
        tier_configs: Dict[str, Dict[str, Any]],
        docker_cfg: Dict[str, Any],
    ) -> PreflightPlan:
        plan = PreflightPlan()

        # Core Python deps used by built-in benchmark runners.
        if system_type == "database":
            plan.python_packages.add(("pymysql", "pymysql"))
        if system_type == "message_queue":
            plan.python_packages.add(("pytest", "pytest"))
            plan.python_packages.add(("pika", "pika"))
            plan.required_commands.add("git")
        if system_type == "http_server":
            # Frequently imported by generated HTTP server variants.
            plan.python_packages.add(("asyncpg", "asyncpg"))

        for tier in tiers:
            per_tier = tier_configs.get(tier, {}) if isinstance(tier_configs, dict) else {}
            for bench in benchmarks:
                bench_cfg = per_tier.get(bench, {})
                if not isinstance(bench_cfg, dict):
                    bench_cfg = {}
                self._extend_plan_for_benchmark(
                    plan=plan,
                    tier=tier,
                    bench=bench,
                    bench_cfg=bench_cfg,
                    docker_cfg=docker_cfg if isinstance(docker_cfg, dict) else {},
                )

        return plan

    def _extend_plan_for_benchmark(
        self,
        *,
        plan: PreflightPlan,
        tier: str,
        bench: str,
        bench_cfg: Dict[str, Any],
        docker_cfg: Dict[str, Any],
    ) -> None:
        bench_name = str(bench).strip().lower()

        if bench_name == "http_bench":
            suites = self._select_http_suites(bench_cfg, tier=tier)
            if "cispa" in suites:
                plan.required_commands.add("git")
                plan.need_cispa_setup = True
                plan.cispa_repo = str(
                    bench_cfg.get("cispa_repo")
                    or plan.cispa_repo
                )
                plan.need_cispa_postgres = True
                plan.require_docker = True
                pg_image = str(bench_cfg.get("cispa_postgres_image") or "postgres:15-alpine")
                plan.cispa_postgres_image = pg_image
                plan.docker_images.add(pg_image)
            if "h1spec" in suites:
                if shutil.which("h1spec") is None:
                    plan.require_docker = True
                    image = str(bench_cfg.get("h1spec_deno_image") or "denoland/deno:alpine-2.1.4")
                    plan.docker_images.add(image)
            return

        if bench_name == "mq_bench":
            suites = self._select_mq_suites(bench_cfg, tier=tier)
            if "pika" in suites:
                plan.required_commands.add("git")
                plan.python_packages.add(("pytest", "pytest"))
                plan.python_packages.add(("pika", "pika"))
            if "omq" in suites:
                plan.require_docker = True
                image = str(bench_cfg.get("omq_docker_image") or "pivotalrabbitmq/omq")
                plan.docker_images.add(image)
            if "perftest" in suites:
                plan.require_docker = True
                image = str(bench_cfg.get("perftest_docker_image") or "pivotalrabbitmq/perf-test")
                plan.docker_images.add(image)
            return

        if bench_name == "redis_bench":
            suites = self._select_redis_suites(bench_cfg, tier=tier)
            if "redis_benchmark" in suites:
                plan.require_docker = True
                image = str(bench_cfg.get("redis_benchmark_image") or "redis:7.2.4-alpine")
                plan.docker_images.add(image)
            if "ycsb" in suites:
                plan.require_docker = True
                build_spec = DockerBuildSpec(
                    image=str(
                        bench_cfg.get("ycsb_runner_image")
                        or "hackathon-24h-bench/ycsb-runner:0.17.0-temurin11"
                    ),
                    context=str(
                        bench_cfg.get("ycsb_runner_context")
                        or "./benchmarks/implementations/docker/ycsb_runner"
                    ),
                    dockerfile=str(
                        bench_cfg.get("ycsb_runner_dockerfile")
                        or "./benchmarks/implementations/docker/ycsb_runner/Dockerfile"
                    ),
                    build_args=(
                        ("YCSB_BASE_IMAGE", str(
                            bench_cfg.get("ycsb_base_image")
                            or "eclipse-temurin:11-jre-jammy"
                        )),
                        ("YCSB_RELEASE_URL", str(
                            bench_cfg.get("ycsb_release_url")
                            or (
                                "https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/"
                                "ycsb-redis-binding-0.17.0.tar.gz"
                            )
                        )),
                        ("YCSB_RELEASE_FALLBACK_URL", str(
                            bench_cfg.get("ycsb_release_fallback_url")
                            or (
                                "https://github.com/brianfrankcooper/YCSB/releases/download/0.17.0/"
                                "ycsb-0.17.0.tar.gz"
                            )
                        )),
                    ),
                )
                if build_spec not in plan.docker_builds:
                    plan.docker_builds.append(build_spec)
            if "memtier" in suites:
                plan.require_docker = True
                image = str(bench_cfg.get("memtier_docker_image") or "redislabs/memtier_benchmark:2.1.0")
                plan.docker_images.add(image)
            return

        if bench_name == "sysbench":
            plan.require_docker = True
            image = str(
                bench_cfg.get("docker_image")
                or docker_cfg.get("sysbench_image")
                or "severalnines/sysbench:latest"
            )
            plan.docker_images.add(image)
            plan.python_packages.add(("pymysql", "pymysql"))
            return

        if bench_name in {"tpcc", "tpch"}:
            plan.require_docker = True
            image = str(
                bench_cfg.get("docker_image")
                or docker_cfg.get("hammerdb_image")
                or "tpcorg/hammerdb:v4.9"
            )
            plan.docker_images.add(image)
            plan.python_packages.add(("pymysql", "pymysql"))
            return

    @staticmethod
    def _select_http_suites(cfg: Dict[str, Any], *, tier: str) -> List[str]:
        suites = cfg.get("suites")
        if isinstance(suites, list) and suites:
            return [str(s).strip().lower() for s in suites if str(s).strip()]

        tier_key = str(tier).strip().upper()
        if tier_key == "L0":
            return ["h1spec"]
        if tier_key == "L1":
            return ["cispa"]
        if tier_key in {"L2", "L3", "L4"}:
            return ["tfb"]
        return ["h1spec"]

    @staticmethod
    def _select_mq_suites(cfg: Dict[str, Any], *, tier: str) -> List[str]:
        suites = cfg.get("suites")
        if isinstance(suites, list) and suites:
            return [str(s).strip().lower() for s in suites if str(s).strip()]

        tier_key = str(tier).strip().lower()
        if tier_key in {"l0", "t0", "tier0"}:
            return ["pika"]
        if tier_key in {"l1", "t1", "tier1"}:
            return ["pika", "omq"]
        if tier_key in {"l2", "l3", "t2", "t3", "tier2", "tier3"}:
            return ["pika", "omq", "perftest"]
        return ["pika"]

    @staticmethod
    def _select_redis_suites(cfg: Dict[str, Any], *, tier: str) -> List[str]:
        suites = cfg.get("suites")
        if isinstance(suites, list) and suites:
            return [str(s).strip().lower() for s in suites if str(s).strip()]

        tier_key = str(tier).strip().lower()
        if tier_key in {"l0", "t0", "tier0"}:
            return ["tcl"]
        if tier_key in {"l1", "t1", "tier1"}:
            return ["tcl", "redis_benchmark"]
        if tier_key in {"l2", "t2", "tier2"}:
            return ["tcl", "redis_benchmark"]
        if tier_key in {"l3", "t3", "tier3"}:
            return ["tcl"]
        if tier_key in {"l4", "t4", "tier4"}:
            return ["tcl", "redis_benchmark"]
        if tier_key in {"l5", "t5", "tier5"}:
            return ["ycsb"]
        if tier_key in {"l6", "t6", "tier6"}:
            return ["tcl", "ycsb", "memtier"]
        return ["tcl"]

    def _run_cmd(
        self,
        cmd: Sequence[str],
        *,
        cwd: Optional[Path] = None,
        timeout: int = 600,
        check: bool = False,
    ) -> subprocess.CompletedProcess:
        proc = subprocess.run(
            list(cmd),
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        if check and proc.returncode != 0:
            stderr = (proc.stderr or "").strip()
            stdout = (proc.stdout or "").strip()
            detail = stderr or stdout or f"return code {proc.returncode}"
            raise RuntimeError(f"Command failed: {' '.join(cmd)}: {detail}")
        return proc

    def _ensure_command(self, name: str) -> None:
        if shutil.which(name):
            return
        raise RuntimeError(
            f"Missing required command: {name}. Please install it and rerun test_runner."
        )

    def _ensure_python_package(self, spec: str, *, import_name: Optional[str]) -> None:
        if spec in self._pip_installed_specs:
            return

        module_name = import_name or self._infer_import_name(spec)
        if module_name and importlib.util.find_spec(module_name) is not None:
            self._pip_installed_specs.add(spec)
            return

        install_spec = self._resolve_runtime_compatible_spec(spec)
        if install_spec != spec:
            logger.info(
                "Adjusting dependency for current Python runtime: %s -> %s",
                spec,
                install_spec,
            )

        logger.info("Installing missing Python dependency: %s", install_spec)
        self._run_cmd(
            [sys.executable, "-m", "pip", "install", install_spec],
            timeout=1200,
            check=True,
        )
        self._pip_installed_specs.add(spec)
        self._pip_installed_specs.add(install_spec)

    def _ensure_docker_usable(self) -> None:
        if self._docker_ok is not None:
            ok, err = self._docker_ok
            if not ok:
                raise RuntimeError(err)
            return

        if shutil.which("docker") is None:
            msg = "Docker CLI not found in PATH. Please install Docker."
            self._docker_ok = (False, msg)
            raise RuntimeError(msg)

        probe = self._run_cmd(["docker", "info"], timeout=20, check=False)
        if probe.returncode != 0:
            detail = (probe.stderr or probe.stdout or "").strip() or "docker info failed"
            msg = f"Docker daemon is not usable: {detail}"
            self._docker_ok = (False, msg)
            raise RuntimeError(msg)

        self._docker_ok = (True, "")

    def _ensure_docker_image(self, image: str) -> None:
        inspect = self._run_cmd(
            ["docker", "image", "inspect", image],
            timeout=30,
            check=False,
        )
        if inspect.returncode == 0:
            return

        logger.info("Pulling missing Docker image: %s", image)
        self._run_cmd(["docker", "pull", image], timeout=1800, check=True)

    def _ensure_docker_build(self, spec: DockerBuildSpec) -> None:
        context_path = Path(spec.context).resolve()
        dockerfile_path = Path(spec.dockerfile).resolve()
        if not context_path.exists():
            raise RuntimeError(f"Docker build context not found: {context_path}")
        if not dockerfile_path.exists():
            raise RuntimeError(f"Docker build file not found: {dockerfile_path}")

        expected_fingerprint = self._docker_build_fingerprint(spec)
        existing_fingerprint = self._docker_image_build_fingerprint(spec.image)
        if existing_fingerprint == expected_fingerprint:
            return

        logger.info("Building local Docker image: %s", spec.image)
        cmd = [
            "docker", "build", "--pull",
            "-t", spec.image,
            "-f", str(dockerfile_path),
            "--label", f"{self._DOCKER_BUILD_FINGERPRINT_LABEL}={expected_fingerprint}",
        ]
        for key, value in spec.build_args:
            cmd.extend(["--build-arg", f"{key}={value}"])
        cmd.append(str(context_path))
        self._run_cmd(cmd, timeout=1800, check=True)

    def _docker_image_build_fingerprint(self, image: str) -> Optional[str]:
        inspect = self._run_cmd(
            [
                "docker",
                "image",
                "inspect",
                "--format",
                f"{{{{ index .Config.Labels \"{self._DOCKER_BUILD_FINGERPRINT_LABEL}\" }}}}",
                image,
            ],
            timeout=30,
            check=False,
        )
        if inspect.returncode != 0:
            return None
        value = (inspect.stdout or "").strip()
        return value or None

    def _docker_build_fingerprint(self, spec: DockerBuildSpec) -> str:
        context_path = Path(spec.context).resolve()
        dockerfile_path = Path(spec.dockerfile).resolve()

        digest = hashlib.sha256()
        digest.update(f"image={spec.image}\n".encode("utf-8"))
        for key, value in spec.build_args:
            digest.update(f"arg:{key}={value}\n".encode("utf-8"))

        included_files: Set[Path] = set()
        for path in sorted(context_path.rglob("*")):
            if not path.is_file():
                continue
            rel = path.relative_to(context_path).as_posix()
            if self._should_skip_docker_context_path(rel):
                continue
            self._update_digest_with_file(digest, path, rel)
            included_files.add(path.resolve())

        dockerfile_resolved = dockerfile_path.resolve()
        if dockerfile_resolved not in included_files:
            rel = dockerfile_resolved.name
            self._update_digest_with_file(digest, dockerfile_resolved, rel)

        return digest.hexdigest()

    @staticmethod
    def _should_skip_docker_context_path(rel_path: str) -> bool:
        parts = [part for part in rel_path.split("/") if part]
        skip_names = {".git", "__pycache__", ".pytest_cache", ".mypy_cache"}
        return any(part in skip_names for part in parts)

    @staticmethod
    def _update_digest_with_file(digest: "hashlib._Hash", path: Path, rel_path: str) -> None:
        digest.update(f"file:{rel_path}\n".encode("utf-8"))
        digest.update(path.read_bytes())

    def _prepare_cispa_dependencies(self, repo_url: str) -> None:
        repo_dir = self.cache_dir / "http_conformance_repo"
        if (repo_dir / ".git").is_dir():
            self._run_cmd(["git", "pull", "--ff-only"], cwd=repo_dir, timeout=120, check=False)
        elif repo_dir.exists():
            shutil.rmtree(repo_dir)
            self._run_cmd(
                ["git", "clone", "--depth", "1", repo_url, str(repo_dir)],
                timeout=300,
                check=True,
            )
        else:
            self._run_cmd(
                ["git", "clone", "--depth", "1", repo_url, str(repo_dir)],
                timeout=300,
                check=True,
            )

        req_file = repo_dir / "requirements.txt"
        if req_file.exists():
            logger.info("Installing cispa dependencies from %s", req_file)
            self._run_cmd(
                [sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                timeout=1800,
                check=True,
            )
            return

        pyproject_file = repo_dir / "pyproject.toml"
        if not pyproject_file.exists():
            raise RuntimeError(
                f"cispa repo has neither requirements.txt nor pyproject.toml: {repo_dir}"
            )

        for spec, import_name in self._extract_poetry_dependencies(pyproject_file):
            self._ensure_python_package(spec, import_name=import_name)

    def _check_cispa_postgres_available(self, image: str) -> None:
        container_name = f"lab-cispa-pg-preflight-{os.getpid()}-{int(time.time() * 1000)}"
        run_cmd = [
            "docker", "run", "-d", "--rm",
            "--name", container_name,
            "-e", "POSTGRES_USER=postgres",
            "-e", "POSTGRES_PASSWORD=postgres",
            "-e", "POSTGRES_DB=postgres",
            image,
        ]
        started = self._run_cmd(run_cmd, timeout=60, check=False)
        if started.returncode != 0:
            detail = (started.stderr or started.stdout or "").strip() or "docker run failed"
            raise RuntimeError(
                f"cispa PostgreSQL preflight failed to start container: {detail}"
            )

        try:
            deadline = time.time() + 30
            last_detail = ""
            while time.time() < deadline:
                probe = self._run_cmd(
                    ["docker", "exec", container_name, "pg_isready", "-U", "postgres"],
                    timeout=10,
                    check=False,
                )
                if probe.returncode == 0:
                    return
                last_detail = (probe.stderr or probe.stdout or "").strip()
                time.sleep(1)

            suffix = f": {last_detail}" if last_detail else ""
            raise RuntimeError(
                "cispa PostgreSQL preflight container is not ready within 30s" + suffix
            )
        finally:
            self._run_cmd(["docker", "rm", "-f", container_name], timeout=20, check=False)

    def _extract_poetry_dependencies(self, pyproject_file: Path) -> List[Tuple[str, Optional[str]]]:
        global tomllib
        toml_loader = tomllib
        if toml_loader is None:
            self._ensure_python_package("tomli", import_name="tomli")
            try:
                import tomli as toml_loader  # type: ignore[import-not-found]
            except Exception as e:
                raise RuntimeError(
                    "Python tomllib/tomli is unavailable; cannot parse cispa pyproject.toml."
                ) from e
            tomllib = toml_loader  # cache parser for this process

        raw = toml_loader.loads(pyproject_file.read_text(encoding="utf-8"))
        tool = raw.get("tool") or {}
        poetry = tool.get("poetry") or {}
        deps = poetry.get("dependencies") or {}
        if not isinstance(deps, dict):
            return []

        specs: List[Tuple[str, Optional[str]]] = []
        for pkg_name, requirement in deps.items():
            if str(pkg_name).strip().lower() == "python":
                continue
            pip_name = self._normalize_pip_name(str(pkg_name).strip())
            spec = self._to_pip_spec(pip_name, requirement)
            import_name = self._infer_import_name(pip_name)
            specs.append((spec, import_name))
        return specs

    @staticmethod
    def _python_version() -> Tuple[int, int]:
        return (sys.version_info.major, sys.version_info.minor)

    @classmethod
    def _resolve_runtime_compatible_spec(cls, spec: str) -> str:
        """
        Rewrite known-incompatible pins for the current Python runtime.
        """
        match = re.match(
            r"^\s*([A-Za-z0-9_.-]+)(\[[^\]]+\])?\s*(==|>=|<=|!=|~=|>|<)?\s*(.*?)\s*$",
            spec,
        )
        if not match:
            return spec

        pkg, extras, op, version_text = match.group(1), match.group(2), match.group(3), match.group(4)
        if pkg.lower() != "pandas":
            return spec
        if cls._python_version() < (3, 13):
            return spec
        if op != "==":
            return spec

        ver = cls._parse_major_minor(version_text)
        if ver is None or ver >= (2, 2):
            return spec

        extras_text = extras or ""
        return f"{pkg}{extras_text}>=2.2.0"

    @staticmethod
    def _parse_major_minor(version_text: str) -> Optional[Tuple[int, int]]:
        m = re.match(r"^\s*(\d+)(?:\.(\d+))?", version_text or "")
        if not m:
            return None
        major = int(m.group(1))
        minor = int(m.group(2) or "0")
        return (major, minor)

    @staticmethod
    def _normalize_pip_name(name: str) -> str:
        if name.lower() == "psycopg2":
            # More portable in CI/host environments without libpq headers.
            return "psycopg2-binary"
        return name

    @classmethod
    def _infer_import_name(cls, spec: str) -> str:
        # Strip extras and version operators.
        pkg = spec
        for token in ("==", ">=", "<=", "!=", "~=", ">", "<"):
            if token in pkg:
                pkg = pkg.split(token, 1)[0]
        pkg = pkg.split("[", 1)[0].strip().lower()
        if pkg in cls._IMPORT_OVERRIDES:
            return cls._IMPORT_OVERRIDES[pkg]
        return pkg.replace("-", "_")

    @staticmethod
    def _to_pip_spec(pkg_name: str, requirement: Any) -> str:
        def _apply_version(base: str, version_text: str) -> str:
            v = version_text.strip()
            if not v or v == "*":
                return base
            if v.startswith("^") or v.startswith("~"):
                return f"{base}>={v[1:]}"
            if v.startswith((">", "<", "=", "!")):
                return f"{base}{v}"
            return f"{base}=={v}"

        if isinstance(requirement, str):
            return _apply_version(pkg_name, requirement)

        if isinstance(requirement, dict):
            extras = requirement.get("extras")
            base = pkg_name
            if isinstance(extras, list) and extras:
                extras_text = ",".join(str(x).strip() for x in extras if str(x).strip())
                if extras_text:
                    base = f"{base}[{extras_text}]"

            version = requirement.get("version")
            if isinstance(version, str):
                return _apply_version(base, version)
            return base

        return pkg_name


def run_dependency_preflight(
    *,
    system_type: str,
    tiers: Sequence[str],
    benchmarks: Sequence[str],
    tier_configs: Dict[str, Dict[str, Any]],
    docker_cfg: Dict[str, Any],
    work_dir: Path,
) -> None:
    """Run preflight checks and auto-setup runtime dependencies."""
    cache_dir = work_dir / ".bench_cache"
    preflight = DependencyPreflight(cache_dir=cache_dir)
    preflight.run(
        system_type=system_type,
        tiers=tiers,
        benchmarks=benchmarks,
        tier_configs=tier_configs,
        docker_cfg=docker_cfg,
    )
