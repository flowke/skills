#!/usr/bin/env python3
import json
import os
import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Iterable, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from resolve_yach_config import resolve as resolve_config_internal  # noqa: E402


class YachMessageError(RuntimeError):
    pass


def resolve_config(start_dir: Optional[str] = None):
    path, data, _ = resolve_config_internal(Path(start_dir or os.getcwd()).expanduser().resolve())
    return path, data


def _http_json(method: str, url: str, body: Optional[Dict[str, Any]] = None, form: bool = False) -> Dict[str, Any]:
    data = None
    headers = {"User-Agent": "yach-message-skill/1.0"}
    if body is not None:
        if form:
            data = urlencode(body).encode("utf-8")
            headers["Content-Type"] = "application/x-www-form-urlencoded; charset=utf-8"
        else:
            data = json.dumps(body, ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json; charset=utf-8"
    req = Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8", errors="ignore")
    except HTTPError as e:
        raw = e.read().decode("utf-8", errors="ignore")
        raise YachMessageError(f"HTTP {e.code}: {raw}") from e
    except URLError as e:
        raise YachMessageError(f"network error: {e}") from e

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise YachMessageError(f"response is not valid JSON: {raw}") from e


def get_access_token(config: Dict[str, Any]) -> str:
    query = urlencode({"appkey": config["appkey"], "appsecret": config["appsecret"]})
    url = f"{config['base_url'].rstrip('/')}/gettoken?{query}"
    data = _http_json("GET", url)
    token = data.get("access_token") or data.get("obj", {}).get("access_token")
    if not token:
        raise YachMessageError(f"failed to get access_token: {json.dumps(data, ensure_ascii=False)}")
    return token


def make_message_id(prefix: str = "ymsg") -> str:
    return f"{prefix}-{uuid.uuid4().hex}"


def split_csv_like(value: Optional[str]) -> list[str]:
    if not value:
        return []
    parts = []
    for item in value.replace(",", "|").split("|"):
        item = item.strip()
        if item:
            parts.append(item)
    return parts


def join_pipe(values: Optional[Iterable[str]]) -> Optional[str]:
    if not values:
        return None
    cleaned = [str(v).strip() for v in values if str(v).strip()]
    return "|".join(cleaned) if cleaned else None


def build_at(at_work_codes=None, at_mobiles=None, at_all: bool = False):
    payload = {}
    work_codes = split_csv_like(at_work_codes) if isinstance(at_work_codes, str) else list(at_work_codes or [])
    mobiles = split_csv_like(at_mobiles) if isinstance(at_mobiles, str) else list(at_mobiles or [])
    if mobiles:
        payload["atMobiles"] = mobiles
    if work_codes:
        payload["atWorkCodes"] = work_codes
    if at_all:
        payload["isAtAll"] = True
    return payload or None


def build_text_message(content: str, at_work_codes=None, at_mobiles=None, at_all: bool = False) -> Dict[str, Any]:
    if not content or not content.strip():
        raise YachMessageError("text message content cannot be empty")
    message = {
        "msgtype": "text",
        "text": {"content": content},
    }
    at = build_at(at_work_codes=at_work_codes, at_mobiles=at_mobiles, at_all=at_all)
    if at:
        message["at"] = at
    return message


def infer_markdown_title(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip().lstrip("#").strip()
        if stripped:
            return stripped[:60]
    return "知音楼消息"


def build_markdown_message(
    text: str,
    title: Optional[str] = None,
    image: Optional[str] = None,
    at_work_codes=None,
    at_mobiles=None,
    at_all: bool = False,
) -> Dict[str, Any]:
    if not text or not text.strip():
        raise YachMessageError("markdown text cannot be empty")
    payload = {
        "msgtype": "markdown",
        "markdown": {
            "title": title.strip() if title else infer_markdown_title(text),
            "text": text,
        },
    }
    if image:
        payload["markdown"]["image"] = image
    at = build_at(at_work_codes=at_work_codes, at_mobiles=at_mobiles, at_all=at_all)
    if at:
        payload["at"] = at
    return payload


def load_message_from_args(message_json: Optional[str], message_file: Optional[str]) -> Optional[Dict[str, Any]]:
    if message_json and message_file:
        raise YachMessageError("use only one of --message-json or --message-file")
    if message_json:
        try:
            return json.loads(message_json)
        except json.JSONDecodeError as e:
            raise YachMessageError(f"invalid --message-json: {e}") from e
    if message_file:
        path = Path(message_file).expanduser().resolve()
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except FileNotFoundError as e:
            raise YachMessageError(f"message file not found: {path}") from e
        except json.JSONDecodeError as e:
            raise YachMessageError(f"invalid JSON in message file {path}: {e}") from e
    return None


def read_text_content(content: Optional[str], content_file: Optional[str]) -> Optional[str]:
    if content is not None and content_file:
        raise YachMessageError("use only one of --content or --content-file")
    if content is not None:
        return content
    if content_file:
        path = Path(content_file).expanduser().resolve()
        try:
            return path.read_text(encoding="utf-8")
        except FileNotFoundError as e:
            raise YachMessageError(f"content file not found: {path}") from e
    if not sys.stdin.isatty():
        data = sys.stdin.read()
        return data if data else None
    return None


def _mask_access_token_in_url(url: str) -> str:
    marker = "access_token="
    if marker not in url:
        return url
    prefix, suffix = url.split(marker, 1)
    if "&" in suffix:
        token, rest = suffix.split("&", 1)
        return f"{prefix}{marker}***&{rest}"
    return f"{prefix}{marker}***"


def preview(url: str, body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "url": _mask_access_token_in_url(url),
        "body": body,
    }


def send_single_message(
    config: Dict[str, Any],
    token: str,
    message: Dict[str, Any],
    to_user_id: Optional[str] = None,
    to_work_code: Optional[str] = None,
    message_id: Optional[str] = None,
    dry_run: bool = False,
):
    if not to_user_id and not to_work_code:
        raise YachMessageError("at least one of to_user_id / to_work_code is required")
    url = f"{config['base_url'].rstrip('/')}/v1/single/message/send?access_token={token}"
    body = {
        "message": json.dumps(message, ensure_ascii=False),
        "message_id": message_id or make_message_id("single"),
    }
    if to_user_id:
        body["to_user_id"] = to_user_id
    if to_work_code:
        body["to_work_code"] = to_work_code
    if dry_run:
        return preview(url, body)
    return _http_json("POST", url, body, form=True)


def send_group_message(
    config: Dict[str, Any],
    token: str,
    message: Dict[str, Any],
    group_id: str,
    message_id: Optional[str] = None,
    dry_run: bool = False,
):
    if not group_id or not str(group_id).strip():
        raise YachMessageError("group_id is required")
    url = f"{config['base_url'].rstrip('/')}/group/robot/message/send?access_token={token}"
    body = {
        "group_id": str(group_id).strip(),
        "message": json.dumps(message, ensure_ascii=False),
        "message_id": message_id or make_message_id("group"),
    }
    if dry_run:
        return preview(url, body)
    return _http_json("POST", url, body, form=True)


def send_user_single_message(
    config: Dict[str, Any],
    token: str,
    message: Dict[str, Any],
    from_user_id: str,
    to_user_id: str,
    message_id: Optional[str] = None,
    dry_run: bool = False,
):
    if not from_user_id or not str(from_user_id).strip():
        raise YachMessageError("from_user_id is required")
    if not to_user_id or not str(to_user_id).strip():
        raise YachMessageError("to_user_id is required")
    url = f"{config['base_url'].rstrip('/')}/single/message/send?access_token={token}"
    body = {
        "from_user_id": str(from_user_id).strip(),
        "to_user_id": str(to_user_id).strip(),
        "message": json.dumps(message, ensure_ascii=False),
        "message_id": message_id or make_message_id("user-single"),
    }
    if dry_run:
        return preview(url, body)
    return _http_json("POST", url, body, form=True)



def send_user_group_message(
    config: Dict[str, Any],
    token: str,
    message: Dict[str, Any],
    from_user_id: str,
    group_id: str,
    message_id: Optional[str] = None,
    dry_run: bool = False,
):
    if not from_user_id or not str(from_user_id).strip():
        raise YachMessageError("from_user_id is required")
    if not group_id or not str(group_id).strip():
        raise YachMessageError("group_id is required")
    url = f"{config['base_url'].rstrip('/')}/group/message/send?access_token={token}"
    body = {
        "from_user_id": str(from_user_id).strip(),
        "group_id": str(group_id).strip(),
        "message": json.dumps(message, ensure_ascii=False),
        "message_id": message_id or make_message_id("user-group"),
    }
    if dry_run:
        return preview(url, body)
    return _http_json("POST", url, body, form=True)
