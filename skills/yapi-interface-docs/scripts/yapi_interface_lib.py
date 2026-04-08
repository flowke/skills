#!/usr/bin/env python3
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from resolve_yapi_config import resolve as resolve_config_internal  # noqa: E402


class YapiInterfaceError(RuntimeError):
    pass


LOGIN_URL = "https://yapi.xesv5.com/"


def mask(value: str) -> str:
    value = str(value or "")
    if not value:
        return ""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}***{value[-4:]}"


def resolve_config(start_dir: Optional[str] = None):
    path, data, _ = resolve_config_internal(Path(start_dir or os.getcwd()).expanduser().resolve())
    return path, data


def extract_interface_id(value: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise YapiInterfaceError("interface id or URL is required")
    if text.isdigit():
        return text

    parsed = urlparse(text)
    if parsed.query:
        query = parse_qs(parsed.query)
        ids = query.get("id") or query.get("interface_id")
        if ids and ids[0].strip().isdigit():
            return ids[0].strip()

    match = re.search(r"/interface/(?:api|mock/\d+/api)/(\d+)(?:[/?#]|$)", text)
    if match:
        return match.group(1)

    raise YapiInterfaceError(f"could not extract interface id from input: {text}. Try --id <number> instead.")


def build_interface_url(base_url: str, interface_id: str) -> str:
    return f"{str(base_url).rstrip('/')}/api/interface/get?{urlencode({'id': interface_id})}"


def _default_headers(base_url: str) -> Dict[str, str]:
    return {
        "accept": "application/json, text/plain, */*",
        "referer": f"{str(base_url).rstrip('/')}/",
        "user-agent": "yapi-interface-docs-skill/1.0",
    }


def _merge_headers(config: Dict[str, Any]) -> Dict[str, str]:
    headers = _default_headers(config["base_url"])
    for key, value in (config.get("headers") or {}).items():
        if value is None:
            continue
        headers[str(key)] = str(value)
    headers["cookie"] = config["cookie"]
    return headers


def _decode_error_body(exc: HTTPError) -> str:
    try:
        return exc.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def http_get_json(url: str, headers: Dict[str, str], timeout_sec: int) -> Dict[str, Any]:
    req = Request(url, headers=headers, method="GET")
    try:
        with urlopen(req, timeout=timeout_sec) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
    except HTTPError as e:
        raw = _decode_error_body(e)
        body = raw.strip()
        diagnosis = diagnose_permission_issue(body) if body else None
        if e.code in (401, 403) and not diagnosis:
            diagnosis = "possible permission or cookie issue"
        suffix = f" ({diagnosis})" if diagnosis else ""
        recovery = f". {auth_recovery_hint()}" if diagnosis else ""
        if body:
            raise YapiInterfaceError(f"HTTP {e.code} while requesting {url}: {body}{suffix}{recovery}") from e
        raise YapiInterfaceError(f"HTTP {e.code} while requesting {url}{suffix}{recovery}") from e
    except URLError as e:
        raise YapiInterfaceError(f"network error while requesting {url}: {e}") from e

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        raise YapiInterfaceError(f"response is not valid JSON: {raw[:500]}") from e

    if not isinstance(payload, dict):
        raise YapiInterfaceError(f"unexpected response type: {type(payload).__name__}")
    return payload


def diagnose_permission_issue(message: str) -> Optional[str]:
    text = str(message or "").lower()
    keywords = ["login", "token", "cookie", "permission", "auth", "unauthorized", "forbidden", "登录", "权限"]
    if any(keyword in text for keyword in keywords):
        return "possible permission or cookie issue"
    return None


def auth_recovery_hint() -> str:
    return f"Open {LOGIN_URL} in a browser, log in again, then provide a fresh cookie to update .yapi-config.json."


def unwrap_yapi_response(payload: Dict[str, Any]) -> Dict[str, Any]:
    errcode = payload.get("errcode")
    errmsg = payload.get("errmsg") or payload.get("errMsg") or payload.get("message") or payload.get("msg") or ""
    if errcode not in (None, 0):
        diagnosis = diagnose_permission_issue(errmsg)
        suffix = f" ({diagnosis})" if diagnosis else ""
        recovery = f". {auth_recovery_hint()}" if diagnosis else ""
        raise YapiInterfaceError(f"YAPI error {errcode}: {errmsg or json.dumps(payload, ensure_ascii=False)}{suffix}{recovery}")

    data = payload.get("data")
    if isinstance(data, dict):
        return data
    if isinstance(payload.get("obj"), dict):
        return payload["obj"]
    raise YapiInterfaceError(f"YAPI response did not contain interface data: {json.dumps(payload, ensure_ascii=False)}")


def fetch_interface_doc(config: Dict[str, Any], interface_id: str) -> Dict[str, Any]:
    headers = _merge_headers(config)
    url = build_interface_url(config["base_url"], interface_id)
    payload = http_get_json(url, headers=headers, timeout_sec=int(config.get("timeout_sec", 20)))
    data = unwrap_yapi_response(payload)
    return {
        "request_url": url,
        "payload": payload,
        "data": data,
    }


def _clean_items(value: Any):
    if isinstance(value, list):
        return [item for item in value if item not in (None, "", [], {})]
    return value


def summarize_interface_doc(data: Dict[str, Any]) -> Dict[str, Any]:
    query_path = data.get("query_path") if isinstance(data.get("query_path"), dict) else {}
    path_params = data.get("req_params") or query_path.get("params") or []
    query_params = data.get("req_query") or []
    headers = data.get("req_headers") or []
    body_type = data.get("req_body_type") or data.get("req_body_other_type") or ""
    body = {
        "type": body_type,
        "form": _clean_items(data.get("req_body_form") or []),
        "raw": data.get("req_body_other") or "",
        "is_json_schema": bool(data.get("req_body_is_json_schema")),
    }
    response = {
        "type": data.get("res_body_type") or "",
        "body": data.get("res_body") or "",
        "is_json_schema": bool(data.get("res_body_is_json_schema")),
    }

    summary = {
        "id": data.get("_id") or data.get("id"),
        "title": data.get("title") or "",
        "path": data.get("path") or query_path.get("path") or "",
        "method": data.get("method") or "",
        "status": data.get("status"),
        "project": data.get("project_name") or data.get("project_title") or data.get("project_id"),
        "category": data.get("cat_name") or data.get("cat_title") or data.get("catid"),
        "path_params": _clean_items(path_params),
        "query_params": _clean_items(query_params),
        "headers": _clean_items(headers),
        "request_body": body,
        "response": response,
        "markdown": data.get("markdown") or "",
        "description": data.get("desc") or "",
    }

    return {key: value for key, value in summary.items() if value not in (None, "", [], {})}


def pretty_text_summary(summary: Dict[str, Any]) -> str:
    lines = []

    def add(label: str, value: Any):
        if value in (None, "", [], {}):
            return
        if isinstance(value, (dict, list)):
            rendered = json.dumps(value, ensure_ascii=False, indent=2)
            lines.append(f"{label}:\n{rendered}")
        else:
            lines.append(f"{label}: {value}")

    add("Interface ID", summary.get("id"))
    add("Title", summary.get("title"))
    add("Method", summary.get("method"))
    add("Path", summary.get("path"))
    add("Project", summary.get("project"))
    add("Category", summary.get("category"))
    add("Status", summary.get("status"))
    add("Path Params", summary.get("path_params"))
    add("Query Params", summary.get("query_params"))
    add("Headers", summary.get("headers"))
    add("Request Body", summary.get("request_body"))
    add("Response", summary.get("response"))
    add("Markdown", summary.get("markdown"))
    add("Description", summary.get("description"))
    return "\n\n".join(lines)


def build_config_diagnostic(config_path: Path, config: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "config_path": str(config_path),
        "base_url": config.get("base_url", ""),
        "cookie": mask(config.get("cookie", "")),
        "timeout_sec": config.get("timeout_sec"),
    }
