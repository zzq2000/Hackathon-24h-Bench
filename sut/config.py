"""
Configuration Module for System Under Test

Provides configuration loading and validation for SUTs and benchmarks.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

import yaml

logger = logging.getLogger(__name__)


class SUTConfig:
    """
    Configuration manager for System Under Test.

    Handles loading and accessing configuration from YAML files.
    """

    # Default paths
    _ROOT_DIR = Path(__file__).parent.parent
    # New config layout (preferred):
    #   config/
    #     global.yaml
    #     system.database.yaml
    #     system.message_queue.yaml
    SYSTEMS_DIR = _ROOT_DIR / "config"
    LEGACY_SYSTEMS_DIR = _ROOT_DIR / "systems"
    DEFAULT_CONFIG_FILE = _ROOT_DIR / "config" / "global.yaml"
    LEGACY_CONFIG_FILE = _ROOT_DIR / "config.yaml"
    # Compatibility-only: optional external benchmark override file.
    DEFAULT_BENCH_FILE = _ROOT_DIR / "bench.yaml"
    LEGACY_BENCH_FILE = _ROOT_DIR / "bench.yaml"

    # Tier name aliases for normalization
    # Canonical names are L0/L1/L2/... across all system types.
    TIER_ALIASES: Dict[str, str] = {
        # Short aliases
        "t0": "L0",
        "t1": "L1",
        "t2": "L2",
        "t3": "L3",
        "t4": "L4",
        "t5": "L5",
        "t6": "L6",
        # Long aliases used by some CLI callers
        "tier0": "L0",
        "tier1": "L1",
        "tier2": "L2",
        "tier3": "L3",
        "tier4": "L4",
        "tier5": "L5",
        "tier6": "L6",
    }

    def __init__(
        self,
        system_type: str,
        config_file: Optional[Path] = None,
        bench_file: Optional[Path] = None,
    ):
        """
        Initialize configuration.

        Args:
            system_type: Type of system (database, message_queue, etc.)
            config_file: Path to main config file (optional)
            bench_file: Path to benchmark config file (optional)
        """
        self.system_type = system_type
        self._config: Dict[str, Any] = {}
        self._bench_config: Dict[str, Any] = {}

        # Load system-specific config
        for system_config_path in self._get_system_config_candidates(system_type):
            if system_config_path.exists():
                self._load_system_config(system_config_path)
                break

        # Load main config (overrides system config)
        if config_file and config_file.exists():
            self._load_main_config(config_file)
        else:
            for candidate in self._get_default_main_config_candidates():
                if candidate.exists():
                    self._load_main_config(candidate)
                    break

        # Load benchmark config (overrides both)
        if bench_file and bench_file.exists():
            self._load_bench_config(bench_file)
        else:
            for candidate in self._get_default_bench_config_candidates(system_type):
                if candidate.exists():
                    self._load_bench_config(candidate)
                    break

    @classmethod
    def _get_system_config_candidates(cls, system_type: str) -> List[Path]:
        """Return candidate paths for system configuration in priority order."""
        return [
            cls.SYSTEMS_DIR / f"system.{system_type}.yaml",
            cls.SYSTEMS_DIR / f"{system_type}.yaml",
            cls.LEGACY_SYSTEMS_DIR / f"{system_type}.yaml",
        ]

    @classmethod
    def _get_default_main_config_candidates(cls) -> List[Path]:
        """Return candidate paths for global configuration in priority order."""
        return [cls.DEFAULT_CONFIG_FILE, cls.LEGACY_CONFIG_FILE]

    @classmethod
    def _get_default_bench_config_candidates(cls, system_type: str) -> List[Path]:
        """Return candidate benchmark override config paths for compatibility."""
        candidates: List[Path] = [cls.DEFAULT_BENCH_FILE]
        if cls.LEGACY_BENCH_FILE != cls.DEFAULT_BENCH_FILE:
            candidates.append(cls.LEGACY_BENCH_FILE)
        return candidates

    def _load_system_config(self, path: Path) -> None:
        """Load system-specific configuration."""
        try:
            content = yaml.safe_load(path.read_text(encoding="utf-8"))
            self._config = content or {}
            logger.debug(f"Loaded system config from {path}")
        except (yaml.YAMLError, IOError, OSError) as e:
            logger.warning(f"Failed to load system config: {e}")

    def _load_main_config(self, path: Path) -> None:
        """Load main configuration file."""
        try:
            content = yaml.safe_load(path.read_text(encoding="utf-8"))
            if content:
                self._deep_merge(self._config, content)
            logger.debug(f"Loaded main config from {path}")
        except (yaml.YAMLError, IOError, OSError) as e:
            logger.warning(f"Failed to load main config: {e}")

    def _load_bench_config(self, path: Path) -> None:
        """Load benchmark configuration file."""
        try:
            content = yaml.safe_load(path.read_text(encoding="utf-8"))
            self._bench_config = content or {}
            logger.debug(f"Loaded bench config from {path}")
        except (yaml.YAMLError, IOError, OSError) as e:
            logger.warning(f"Failed to load bench config: {e}")

    def _deep_merge(self, base: Dict, override: Dict) -> None:
        """Deep merge override into base dictionary."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot-separated key."""
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def get_system_config(self) -> Dict[str, Any]:
        """Get system configuration section."""
        return self._config.get("system", {})

    def get_target_dir(self) -> Path:
        """Get target directory for the SUT."""
        system = self.get_system_config()
        target = system.get("target_dir", f"./workspace/{self.system_type}")
        return Path(target)

    def get_default_port(self) -> int:
        """Get default port for the SUT."""
        system = self.get_system_config()
        return system.get("default_port", 0)

    def get_benchmarks(self) -> List[str]:
        """Get list of enabled benchmarks."""
        benchmarks = self._config.get("benchmarks", [])
        return [b["name"] for b in benchmarks if b.get("enabled", True)]

    def get_tiers(self) -> List[str]:
        """Get list of tier names."""
        tiers = self._config.get("tiers", {})
        return list(tiers.keys())

    def normalize_tier_name(self, tier: str) -> str:
        """
        Normalize a tier name to the canonical name used in config.

        Tries the tier as-is first, then checks aliases.

        Args:
            tier: Tier name (may be an alias)

        Returns:
            Canonical tier name
        """
        tiers = self._config.get("tiers", {})
        tier_lower = tier.lower().strip()

        # Try direct match first
        if tier_lower in tiers:
            return tier_lower

        # Try case-insensitive match
        for t in tiers:
            if t.lower() == tier_lower:
                return t

        # Try alias lookup
        if tier_lower in self.TIER_ALIASES:
            alias = self.TIER_ALIASES[tier_lower]
            if alias in tiers:
                return alias
            # Try case-insensitive alias match
            for t in tiers:
                if t.lower() == alias.lower():
                    return t

        # Return original if no match found
        return tier

    def get_tier_config(self, tier: str) -> Dict[str, Any]:
        """
        Get configuration for a specific tier.

        Supports tier name aliases (e.g., 't0' -> 'L0').

        Args:
            tier: Tier name (may be an alias)

        Returns:
            Tier configuration dictionary
        """
        tiers = self._config.get("tiers", {})
        normalized = self.normalize_tier_name(tier)
        return tiers.get(normalized, {})

    def get_benchmark_config(self, benchmark: str, tier: str = None) -> Dict[str, Any]:
        """
        Get benchmark configuration.

        Args:
            benchmark: Benchmark name
            tier: Optional tier name for tier-specific config (supports aliases)

        Returns:
            Benchmark configuration dictionary
        """
        config = {}

        # Global benchmark config
        if benchmark in self._config:
            config.update(self._config[benchmark])

        # Normalize tier name if provided
        normalized_tier = self.normalize_tier_name(tier) if tier else None

        # Tier-specific config
        if normalized_tier:
            tier_config = self.get_tier_config(normalized_tier)
            if benchmark in tier_config:
                self._deep_merge(config, tier_config[benchmark])

        # Bench file config
        if benchmark in self._bench_config:
            self._deep_merge(config, self._bench_config[benchmark])

        # Bench file tier-specific overrides (legacy bench.yaml shape)
        # Expected format:
        #   tiers:
        #     <benchmark>:
        #       <tier_name>:
        #         ...
        if tier:
            bench_tiers = self._bench_config.get("tiers")
            if isinstance(bench_tiers, dict):
                per_bench = bench_tiers.get(benchmark)
                if isinstance(per_bench, dict):
                    # Try both original and normalized tier names
                    for try_tier in (tier, normalized_tier):
                        if try_tier:
                            override = per_bench.get(try_tier)
                            if isinstance(override, dict):
                                self._deep_merge(config, override)
                                break

        return config

    def get_docker_config(self) -> Dict[str, Any]:
        """Get Docker configuration."""
        return self._config.get("docker", {})

    def get_feedback_config(self) -> Dict[str, Any]:
        """Get feedback configuration."""
        return self._config.get("feedback", {})

    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary."""
        return {
            "system_type": self.system_type,
            "config": self._config,
            "bench_config": self._bench_config,
        }

    @classmethod
    def get_available_system_types(cls) -> List[str]:
        """Get list of available system types."""
        types: List[str] = []
        seen = set()
        if cls.SYSTEMS_DIR.exists():
            for f in cls.SYSTEMS_DIR.glob("system.*.yaml"):
                system_type = f.name[len("system."):-len(".yaml")]
                if system_type and system_type not in seen:
                    seen.add(system_type)
                    types.append(system_type)
            # Backward compatibility if old-style files are accidentally placed in config/.
            for f in cls.SYSTEMS_DIR.glob("*.yaml"):
                if f.name.startswith("system."):
                    continue
                # Skip non-system config files in the new layout.
                if f.stem in {"global"} or f.name.startswith("benchmark."):
                    continue
                if "." in f.stem:
                    continue
                system_type = f.stem
                if system_type and system_type not in seen:
                    seen.add(system_type)
                    types.append(system_type)
        if cls.LEGACY_SYSTEMS_DIR.exists():
            for f in cls.LEGACY_SYSTEMS_DIR.glob("*.yaml"):
                system_type = f.stem
                if system_type and system_type not in seen:
                    seen.add(system_type)
                    types.append(system_type)
        return types


def load_config(
    system_type: str,
    config_file: Optional[Path] = None,
    bench_file: Optional[Path] = None,
) -> SUTConfig:
    """
    Load configuration for a system type.

    Args:
        system_type: Type of system
        config_file: Optional config file path
        bench_file: Optional bench file path

    Returns:
        SUTConfig instance
    """
    return SUTConfig(system_type, config_file, bench_file)
