from __future__ import annotations

import argparse
import importlib.util
import json
import os
import random
import re
import shutil
import socket
import string
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Tuple


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Hackathon-24h-Bench CISPA adapter")
    parser.add_argument("--repo-dir", required=True)
    parser.add_argument("--host", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--selected-rules-json", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--mitmdump-log", required=True)
    parser.add_argument("--probe-sleep", type=float, default=0.0)
    parser.add_argument("--direct-sleep", type=float, default=0.0)
    return parser.parse_args()


def _write_payload(output_path: Path, payload: Dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")


def _random_path() -> str:
    return "".join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))


def _wait_for_port(host: str, port: int, timeout_sec: float) -> None:
    deadline = time.time() + timeout_sec
    while time.time() < deadline:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                return
        time.sleep(0.1)
    raise RuntimeError(f"mitmdump did not start listening on {host}:{port}")


def _patch_direct_util() -> None:
    import dpkt
    from helpers import direct_util

    def _patched_parse_response(response: bytes, head_response: bool = False):
        responses = re.split(rb"(?<=\r\n\r\n)(?=HTTP/)", response)
        parsed = []
        for chunk in responses:
            try:
                if head_response:
                    head, sep, tail = chunk.partition(b"\r\n\r\n")
                    if not sep:
                        raise dpkt.UnpackError("missing response header terminator")
                    resp = dpkt.http.Response(head + sep)
                    resp.body = b""
                    resp.data = tail
                else:
                    resp = dpkt.http.Response(chunk)
                parsed.append((resp, chunk))
            except Exception as exc:  # pragma: no cover - adapter integration path
                parsed.append((exc, chunk))
        return parsed

    direct_util.parse_response = _patched_parse_response


def _patch_testcases() -> None:
    import dpkt
    import testcases
    from helpers.db_util import DirectTest, Violation
    from helpers.direct_util import build_request, one_req

    content_head_cls = getattr(testcases, "content_head_request", None)
    if content_head_cls is None or getattr(content_head_cls, "_longagent_patched", False):
        return

    def _patched_content_head_request_test(self, url):
        dt = DirectTest.create(url=url, name=self.name, type=self.type)
        extra = ""
        violation = Violation.VALID
        req = build_request(url.host, url.port, method=b"HEAD", request_target=url.path)
        resp = one_req(url, dt, req, head_response=True)[0][0]
        if isinstance(resp, dpkt.UnpackError):
            violation = Violation.UNCLEAR
            extra = f"{resp}"
        elif getattr(resp, "data", b"") != b"":
            violation = Violation.INVALID
            extra = f"Additional data to head response: {resp.data}"
        dt.violation = violation
        dt.extra = extra
        dt.save()
        return dt

    content_head_cls.test = _patched_content_head_request_test
    content_head_cls._longagent_patched = True


def _bootstrap_repo(repo_dir: Path) -> None:
    repo_text = str(repo_dir.resolve())
    if repo_text not in sys.path:
        sys.path.insert(0, repo_text)


def _build_selected_tests(
    selected_rule_ids: List[str],
) -> Tuple[Dict[str, str], List[Any], List[Any], List[Any], List[str]]:
    import inspect
    import testcases
    from helpers.db_util import Activity

    activity_by_rule: Dict[str, str] = {}
    direct_tests: List[Any] = []
    direct_base_tests: List[Any] = []
    retro_tests: List[Any] = []
    missing_rule_ids: List[str] = []

    available: Dict[str, Any] = {}
    for name, obj in inspect.getmembers(testcases):
        if inspect.isclass(obj):
            available[name] = obj

    for rule_id in selected_rule_ids:
        obj = available.get(rule_id)
        if obj is None:
            missing_rule_ids.append(rule_id)
            continue
        test_obj = obj()
        activity_name = getattr(test_obj.activity, "name", str(test_obj.activity))
        activity_by_rule[rule_id] = activity_name
        if test_obj.activity == Activity.DIRECT:
            direct_tests.append(test_obj)
        elif test_obj.activity == Activity.DIRECT_BASE:
            direct_base_tests.append(test_obj)
        elif test_obj.activity == Activity.RETRO:
            retro_tests.append(test_obj)

    return activity_by_rule, direct_tests, direct_base_tests, retro_tests, missing_rule_ids


def _create_targets(host: str, port: int):
    from helpers.db_util import Site, Url

    site = Site.create(
        site_type="local",
        description=f"longagent-http://{host}:{port}",
        rank=-1,
        bucket=-1,
        origin=f"http://{host}:{port}",
        site=host,
        reachable=True,
        status="Testing",
        org_scheme="http",
    )
    base_url = Url.create(
        site=site,
        full_url=f"http://{host}:{port}/",
        scheme="http",
        host=host,
        port=port,
        path="/",
        description="Base URL",
        is_base=True,
    )
    random_path = f"/{_random_path()}"
    non_existing_url = Url.create(
        site=site,
        full_url=f"http://{host}:{port}{random_path}",
        scheme="http",
        host=host,
        port=port,
        path=random_path,
        description="non-existing",
        is_base=False,
    )
    return [base_url, non_existing_url]


def _start_mitmdump(repo_dir: Path, db_name: str, selected_rules_file: Path, mitmdump_log: Path) -> Tuple[subprocess.Popen[str], int]:
    proxy_port = _find_free_port()
    addon_path = Path(__file__).with_name("http_bench_cispa_addon.py").resolve()
    mitmdump_log.parent.mkdir(parents=True, exist_ok=True)
    log_handle = mitmdump_log.open("a", encoding="utf-8")
    env = os.environ.copy()
    env["LONGAGENT_CISPA_REPO_DIR"] = str(repo_dir.resolve())
    env["LONGAGENT_CISPA_SELECTED_RULES_JSON"] = str(selected_rules_file.resolve())
    mitmdump_cmd = _mitmdump_command()
    proc = subprocess.Popen(
        mitmdump_cmd + [
            "-s",
            str(addon_path),
            "-p",
            str(proxy_port),
            "--set",
            "validate_inbound_headers=false",
            "--set",
            "ssl_insecure=true",
            "--set",
            f"db_name={db_name}",
        ],
        cwd=str(repo_dir),
        stdout=log_handle,
        stderr=log_handle,
        text=True,
        env=env,
    )
    try:
        _wait_for_port("127.0.0.1", proxy_port, timeout_sec=10)
    except Exception:
        proc.terminate()
        proc.wait(timeout=10)
        log_handle.close()
        raise
    proc._longagent_log_handle = log_handle  # type: ignore[attr-defined]
    return proc, proxy_port


def _stop_mitmdump(proc: subprocess.Popen[str] | None) -> None:
    if proc is None:
        return
    try:
        if proc.poll() is None:
            proc.terminate()
            proc.wait(timeout=10)
    except Exception:
        try:
            proc.kill()
            proc.wait(timeout=5)
        except Exception:
            pass
    log_handle = getattr(proc, "_longagent_log_handle", None)
    if log_handle is not None:
        try:
            log_handle.close()
        except Exception:
            pass


def _find_free_port(host: str = "127.0.0.1") -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, 0))
        return int(sock.getsockname()[1])


def _mitmdump_command() -> List[str]:
    sibling = Path(sys.executable).resolve().with_name("mitmdump")
    if sibling.exists():
        return [str(sibling)]

    if importlib.util.find_spec("mitmproxy.tools.main") is not None:
        return [
            sys.executable,
            "-c",
            "from mitmproxy.tools.main import mitmdump; raise SystemExit(mitmdump())",
        ]

    mitmdump = shutil.which("mitmdump")
    if not mitmdump:
        raise RuntimeError("mitmdump not found in PATH and mitmproxy is unavailable in current Python")
    return [mitmdump]


def _aggregate_rule_results(
    *,
    selected_rule_ids: List[str],
    activity_by_rule: Dict[str, str],
) -> Tuple[Dict[str, Dict[str, Any]], Dict[str, int], str | None]:
    from helpers.db_util import DirectTest, ProbeTest, ReqResp, RetroTest, Violation

    rows_by_rule: Dict[str, List[Dict[str, Any]]] = {rule_id: [] for rule_id in selected_rule_ids}
    table_counts = {
        "reqresp": ReqResp.select().count(),
        "proxy_reqresp": ReqResp.select().where(ReqResp.req_type.startswith("proxy-probe")).count(),
        "directtest": DirectTest.select().count(),
        "probetest": ProbeTest.select().count(),
        "retrotest": RetroTest.select().count(),
    }

    for table_name, model in (
        ("direct", DirectTest),
        ("probe", ProbeTest),
        ("retro", RetroTest),
    ):
        query = model.select().where(model.name << selected_rule_ids)
        for row in query:
            rows_by_rule.setdefault(row.name, []).append(
                {
                    "table": table_name,
                    "violation": str(row.violation or ""),
                    "test_error": str(row.test_error or ""),
                    "extra": str(row.extra or ""),
                }
            )

    runtime_error: str | None = None
    needs_proxy = any(activity_by_rule.get(rule_id) in {"PROXY", "RETRO"} for rule_id in selected_rule_ids)
    needs_direct = any(activity_by_rule.get(rule_id) in {"DIRECT", "DIRECT_BASE"} for rule_id in selected_rule_ids)
    if needs_proxy and table_counts["proxy_reqresp"] == 0:
        runtime_error = "cispa adapter captured no proxy probe traffic"
    elif needs_direct and table_counts["directtest"] == 0:
        runtime_error = "cispa adapter materialized no direct test rows"

    rule_results: Dict[str, Dict[str, Any]] = {}
    for rule_id in selected_rule_ids:
        activity = activity_by_rule.get(rule_id, "UNKNOWN")
        rows = rows_by_rule.get(rule_id, [])
        violations = [row["violation"] for row in rows if row["violation"]]
        has_runtime = any(row["test_error"] or row["violation"] == Violation.FAILED for row in rows)
        has_invalid = any(row["violation"] == Violation.INVALID for row in rows)
        has_valid = any(row["violation"] == Violation.VALID for row in rows)
        has_inapplicable = any(row["violation"] == Violation.INAPPLICABLE for row in rows)
        has_unclear = any(row["violation"] == Violation.UNCLEAR for row in rows)

        if rows:
            if has_runtime:
                status = "RUNTIME_ERROR"
                source = "db_rows"
                reason = "test_error"
            elif has_invalid:
                status = "FAIL"
                source = "db_rows"
                reason = "breaks_specification"
            elif has_valid:
                status = "PASS"
                source = "db_rows"
                reason = "follows_specification"
            elif has_inapplicable:
                status = "PASS"
                source = "db_rows"
                reason = "inapplicable_only"
            elif has_unclear:
                status = "FAIL"
                source = "db_rows"
                reason = "unclear"
            else:
                status = "RUNTIME_ERROR"
                source = "db_rows"
                reason = "unrecognized_row_state"
        else:
            if activity == "PROXY" and table_counts["proxy_reqresp"] > 0:
                status = "PASS"
                source = "no_materialized_row"
                reason = "assumed_inapplicable"
            else:
                status = "RUNTIME_ERROR"
                source = "missing_rule_result"
                reason = "no_rows"

        rule_results[rule_id] = {
            "status": status,
            "activity": activity,
            "source": source,
            "reason": reason,
            "row_count": len(rows),
            "violations": violations,
        }

    return rule_results, table_counts, runtime_error


def main() -> int:
    args = _parse_args()
    repo_dir = Path(args.repo_dir).resolve()
    output_json = Path(args.output_json).resolve()
    selected_rules_file = Path(args.selected_rules_json).resolve()
    mitmdump_log = Path(args.mitmdump_log).resolve()
    selected_rule_ids = [
        str(item).strip()
        for item in json.loads(selected_rules_file.read_text(encoding="utf-8"))
        if str(item).strip()
    ]

    payload: Dict[str, Any] = {
        "db_name": "",
        "selected_rule_count": len(selected_rule_ids),
        "materialized_rule_count": 0,
        "reqresp_count": 0,
        "table_counts": {},
        "rule_results": {},
        "runtime_error": None,
    }

    mitmdump_proc: subprocess.Popen[str] | None = None
    db = None
    try:
        if not repo_dir.is_dir():
            raise RuntimeError(f"CISPA repo directory not found: {repo_dir}")
        _bootstrap_repo(repo_dir)
        os.chdir(repo_dir)

        import run_checks
        from helpers.db_util import AddResp, DirectTest, Monitoring, ProbeTest, ReqResp, RetroTest, Site, Url, db, setup_db
        from helpers.requestors import HttpxRequestor

        _patch_direct_util()
        _patch_testcases()

        activity_by_rule, direct_tests, direct_base_tests, retro_tests, missing_rule_ids = _build_selected_tests(selected_rule_ids)
        db_name = f"results_longagent_{os.getpid()}_{int(time.time() * 1000)}"
        payload["db_name"] = db_name

        setup_db(db_name)
        db.init(db_name)
        db.connect()
        db.create_tables([Site, Url, DirectTest, ProbeTest, RetroTest, AddResp, ReqResp, Monitoring])

        urls = _create_targets(args.host, args.port)

        mitmdump_proc, proxy_port = _start_mitmdump(repo_dir, db_name, selected_rules_file, mitmdump_log)
        requestor = HttpxRequestor(proxy={"all://": f"http://127.0.0.1:{proxy_port}"}, error_set=set())

        class _NoopRedbot:
            def run(self, url):  # noqa: ANN001
                return None

            def close(self):
                return None

        redbot = _NoopRedbot()

        for url in urls:
            run_checks.run_tests(
                url,
                "local",
                redbot,
                requestor,
                direct_tests,
                direct_base_tests,
                retro_tests,
                set(),
                probe_sleep=args.probe_sleep,
                direct_sleep=args.direct_sleep,
            )

        rule_results, table_counts, runtime_error = _aggregate_rule_results(
            selected_rule_ids=selected_rule_ids,
            activity_by_rule=activity_by_rule,
        )
        for rule_id in missing_rule_ids:
            rule_results[rule_id] = {
                "status": "RUNTIME_ERROR",
                "activity": "UNKNOWN",
                "source": "unknown_rule",
                "reason": "selected rule not found in repo",
                "row_count": 0,
                "violations": [],
            }

        payload["table_counts"] = table_counts
        payload["reqresp_count"] = table_counts.get("reqresp", 0)
        payload["rule_results"] = rule_results
        payload["materialized_rule_count"] = sum(
            1 for info in rule_results.values() if int(info.get("row_count") or 0) > 0
        )
        payload["runtime_error"] = runtime_error

        _write_payload(output_json, payload)
        return 0 if runtime_error is None else 1
    except Exception as exc:
        payload["runtime_error"] = str(exc)
        _write_payload(output_json, payload)
        print(f"CISPA adapter failed: {exc}")
        return 1
    finally:
        _stop_mitmdump(mitmdump_proc)
        try:
            if db is not None and not db.is_closed():
                db.close()
        except Exception:
            pass


if __name__ == "__main__":
    raise SystemExit(main())
