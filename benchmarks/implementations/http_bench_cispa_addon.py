from __future__ import annotations

import inspect
import json
import os
import sys
from pathlib import Path
from typing import Any, List

from mitmproxy import ctx, http, log


def _bootstrap_repo() -> None:
    repo_dir = Path(os.environ["LONGAGENT_CISPA_REPO_DIR"]).resolve()
    repo_text = str(repo_dir)
    if repo_text not in sys.path:
        sys.path.insert(0, repo_text)


_bootstrap_repo()

import testcases  # noqa: E402
from helpers.db_util import Activity, DirectTest, ProbeTest, ReqResp, Violation, db  # noqa: E402


def _load_selected_rule_ids() -> set[str]:
    rules_path = Path(os.environ["LONGAGENT_CISPA_SELECTED_RULES_JSON"]).resolve()
    data = json.loads(rules_path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        return set()
    return {str(item).strip() for item in data if str(item).strip()}


def _selected_proxy_tests() -> List[Any]:
    selected = _load_selected_rule_ids()
    out: List[Any] = []
    ignored = {
        "StrEnum",
        "Activity",
        "Violation",
        "Level",
        "datetime",
        "DirectTest",
        "ProbeTest",
        "RetroTest",
        "ReqResp",
        "Url",
    }
    for name, obj in inspect.getmembers(testcases):
        if name not in selected or name in ignored or not inspect.isclass(obj):
            continue
        test_obj = obj()
        if test_obj.activity == Activity.PROXY:
            out.append(test_obj)
    return out


class FilteredConformanceChecker:
    def load(self, loader) -> None:
        loader.add_option(
            name="db_name",
            typespec=str,
            default="",
            help="Specify DB Name",
        )

    def running(self) -> None:
        self.db = db
        self.db.init(ctx.options.db_name)
        self.db.connect()
        self.db.create_tables([ReqResp, ProbeTest, DirectTest])
        self.msg = ""
        self.tests = _selected_proxy_tests()

    def done(self) -> None:
        self.db.close()

    def request(self, flow: http.HTTPFlow) -> None:
        flow.url_id = None
        flow.probe_id = None
        try:
            flow.url_id = flow.request.query["url_id"]
            del flow.request.query["url_id"]
            flow.probe_id = flow.request.query["probe_id"]
            del flow.request.query["probe_id"]
        except KeyError:
            pass

    def response(self, flow: http.HTTPFlow) -> None:
        if flow.request.method == "CONNECT":
            return

        req_resp = ReqResp.create(
            url=flow.url_id,
            real_url=flow.request.url,
            probe_id=flow.probe_id,
            msg=self.msg,
            req_type="proxy-probe",
            req_method=flow.request.method,
            req_version=flow.request.http_version,
            req_headers=flow.request.headers.fields,
            req_body=flow.request.get_text(strict=False),
            resp_code=str(flow.response.status_code),
            resp_version=flow.response.http_version,
            resp_headers=flow.response.headers.fields,
            resp_body=flow.response.get_text(strict=False),
        )
        self.msg = ""

        for test_obj in self.tests:
            try:
                result = test_obj.test(flow)
                if result is None:
                    result = ProbeTest()
            except Exception as exc:
                result = ProbeTest(
                    name=test_obj.name,
                    test_error=str(exc),
                    type=test_obj.type,
                    violation=Violation.FAILED,
                )
            result.req = req_resp
            result.url = flow.url_id
            if result.type != "" or result.test_error != "":
                if result.violation != Violation.INAPPLICABLE:
                    result.save()

    def error(self, flow: http.HTTPFlow) -> None:
        try:
            url_id = flow.url_id
        except AttributeError:
            url_id = None
        try:
            probe_id = flow.probe_id
        except AttributeError:
            probe_id = None

        ReqResp.create(
            url=url_id,
            real_url=flow.request.url,
            probe_id=probe_id,
            error=flow.error,
            msg=self.msg,
            req_type="proxy-probe-error",
            req_method=flow.request.method,
            req_version=flow.request.http_version,
            req_headers=flow.request.headers.fields,
            req_body=flow.request.get_text(strict=False),
        )
        self.msg = ""

    def add_log(self, entry: log.LogEntry) -> None:
        if "Unexpected" in entry.msg or "Swallowing" in entry.msg:
            self.msg = entry.msg


addons = [FilteredConformanceChecker()]
