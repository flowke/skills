#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from yapi_interface_lib import YapiInterfaceError, auth_recovery_hint, diagnose_permission_issue, extract_interface_id, summarize_interface_doc, unwrap_yapi_response


class ExtractInterfaceIdTests(unittest.TestCase):
    def test_extract_from_plain_id(self):
        self.assertEqual(extract_interface_id("184595"), "184595")

    def test_extract_from_page_url(self):
        url = "https://yapi.xesv5.com/project/3932/interface/api/184595"
        self.assertEqual(extract_interface_id(url), "184595")

    def test_extract_from_api_url_query(self):
        url = "https://yapi.xesv5.com/api/interface/get?id=184595"
        self.assertEqual(extract_interface_id(url), "184595")

    def test_extract_failure(self):
        with self.assertRaises(YapiInterfaceError):
            extract_interface_id("https://yapi.xesv5.com/project/3932/interface/api/not-a-number")


class ResolveConfigTests(unittest.TestCase):
    def test_missing_config_reports_search_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            env = dict(os.environ)
            env["HOME"] = tmp
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "resolve_yapi_config.py"), "--start-dir", tmp, "--validate"],
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("no .yapi-config.json found", proc.stderr)
            self.assertIn("Minimal example", proc.stderr)

    def test_missing_cookie_reports_clear_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            config_path = Path(tmp) / ".yapi-config.json"
            config_path.write_text(json.dumps({"base_url": "https://yapi.xesv5.com"}), encoding="utf-8")
            env = dict(os.environ)
            env["HOME"] = tmp
            proc = subprocess.run(
                [sys.executable, str(SCRIPTS / "resolve_yapi_config.py"), "--start-dir", tmp, "--validate"],
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("missing required keys", proc.stderr)
            self.assertIn("cookie", proc.stderr)


class SummaryTests(unittest.TestCase):
    def test_summary_contains_core_fields(self):
        data = {
            "_id": 184595,
            "title": "获取班级列表",
            "path": "/api/classes",
            "method": "GET",
            "project_name": "教务服务",
            "cat_name": "班级管理",
            "req_params": [{"name": "schoolId", "desc": "学校 ID"}],
            "req_query": [{"name": "page", "desc": "页码"}],
            "req_headers": [{"name": "Authorization", "required": "1"}],
            "req_body_type": "json",
            "req_body_other": '{"grade": "3"}',
            "req_body_is_json_schema": True,
            "res_body_type": "json",
            "res_body": '{"list": []}',
            "res_body_is_json_schema": True,
            "markdown": "# 接口说明",
            "desc": "用于获取班级列表",
        }
        summary = summarize_interface_doc(data)
        self.assertEqual(summary["id"], 184595)
        self.assertEqual(summary["title"], "获取班级列表")
        self.assertEqual(summary["path"], "/api/classes")
        self.assertEqual(summary["method"], "GET")
        self.assertIn("request_body", summary)
        self.assertIn("response", summary)

    def test_permission_diagnosis(self):
        self.assertEqual(diagnose_permission_issue("permission denied"), "possible permission or cookie issue")
        self.assertEqual(diagnose_permission_issue("请先登录"), "possible permission or cookie issue")
        self.assertIsNone(diagnose_permission_issue("interface not found"))

    def test_auth_recovery_hint_contains_login_url(self):
        self.assertIn("https://yapi.xesv5.com/", auth_recovery_hint())

    def test_yapi_error_includes_auth_recovery_hint(self):
        with self.assertRaises(YapiInterfaceError) as ctx:
            unwrap_yapi_response({"errcode": 401, "errmsg": "请先登录"})
        self.assertIn("https://yapi.xesv5.com/", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
