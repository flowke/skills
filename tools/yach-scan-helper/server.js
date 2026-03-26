const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { URL, URLSearchParams } = require('url');

loadDotEnv(path.join(__dirname, '.env'));

const PORT = Number(process.env.PORT || 8787);
const APP_ID = process.env.YACH_OAUTH_APP_ID || '';
const APP_SECRET = process.env.YACH_OAUTH_APP_SECRET || '';
const REDIRECT_URI = process.env.YACH_OAUTH_REDIRECT_URI || `http://127.0.0.1:${PORT}/oauth/callback`;
const STATIC_DIR = path.join(__dirname, 'public');
const YYLOGIN_JS = path.join(__dirname, 'node_modules', 'yach.open.yylogin', 'lib', 'yyLogin.browser.js');

let cachedApiToken = process.env.YACH_OAUTH_API_TOKEN || '';
let cachedQuickSign = null;

function loadDotEnv(file) {
  if (!fs.existsSync(file)) return;
  const lines = fs.readFileSync(file, 'utf8').split(/\r?\n/);
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx < 0) continue;
    const key = trimmed.slice(0, idx).trim();
    let value = trimmed.slice(idx + 1).trim();
    if ((value.startsWith('"') && value.endsWith('"')) || (value.startsWith("'") && value.endsWith("'"))) {
      value = value.slice(1, -1);
    }
    if (!(key in process.env)) process.env[key] = value;
  }
}

function sendJson(res, status, obj) {
  const body = JSON.stringify(obj, null, 2);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  res.end(body);
}

function sendHtml(res, status, html) {
  res.writeHead(status, {
    'Content-Type': 'text/html; charset=utf-8',
    'Cache-Control': 'no-store'
  });
  res.end(html);
}

function sendText(res, status, text, type='text/plain; charset=utf-8') {
  res.writeHead(status, { 'Content-Type': type, 'Cache-Control': 'no-store' });
  res.end(text);
}

function notFound(res) {
  sendText(res, 404, 'Not Found');
}

function mask(value) {
  if (!value) return '';
  if (value.length <= 6) return '***';
  return `${value.slice(0, 3)}***${value.slice(-3)}`;
}

function signTimestamp(timestamp, secret) {
  return crypto.createHmac('sha256', secret).update(String(timestamp)).digest('base64');
}

async function httpJson(method, url, body = null, headers = {}) {
  const init = { method, headers: { 'User-Agent': 'yach-scan-helper/0.1', ...headers } };
  if (body != null) init.body = body;
  const resp = await fetch(url, init);
  const text = await resp.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch (e) {
    throw new Error(`Non-JSON response (${resp.status}): ${text}`);
  }
  if (!resp.ok) {
    throw new Error(`HTTP ${resp.status}: ${JSON.stringify(data)}`);
  }
  return data;
}

async function getApiToken() {
  if (cachedApiToken) return cachedApiToken;
  if (!APP_ID || !APP_SECRET) throw new Error('Missing YACH_OAUTH_APP_ID / YACH_OAUTH_APP_SECRET');

  // Fallback inference: some tenants may support using appId/appSecret on the generic /gettoken endpoint.
  // This is not explicitly guaranteed by the扫码登录文档, so treat failures as expected and configure YACH_OAUTH_API_TOKEN if needed.
  const url = `https://yach-oapi.zhiyinlou.com/gettoken?appkey=${encodeURIComponent(APP_ID)}&appsecret=${encodeURIComponent(APP_SECRET)}`;
  const data = await httpJson('GET', url);
  const token = data.access_token || (data.obj && data.obj.access_token) || '';
  if (!token) {
    throw new Error(`Failed to infer OAuth API token via /gettoken: ${JSON.stringify(data)}`);
  }
  cachedApiToken = token;
  return token;
}

async function getQuickSign() {
  if (cachedQuickSign) return cachedQuickSign;
  const token = await getApiToken();
  const url = `https://yach-oapi.zhiyinlou.com/connect/oauth2/quick_login_sign?access_token=${encodeURIComponent(token)}`;
  const data = await httpJson('GET', url);
  const quickSign = data.obj && data.obj.quick_sign;
  if (!quickSign) {
    throw new Error(`Failed to get quick_sign: ${JSON.stringify(data)}`);
  }
  cachedQuickSign = quickSign;
  return quickSign;
}

function buildAuthorizeUrl({ loginTmpCode = '', state = '' , quickSign = ''}) {
  if (!APP_ID) throw new Error('Missing YACH_OAUTH_APP_ID');
  if (!APP_SECRET) throw new Error('Missing YACH_OAUTH_APP_SECRET');
  const timestamp = Date.now();
  const signature = signTimestamp(timestamp, APP_SECRET);
  const url = new URL('https://yach-oapi.zhiyinlou.com/connect/oauth2/sns_authorize');
  url.searchParams.set('appid', APP_ID);
  url.searchParams.set('response_type', 'code');
  url.searchParams.set('scope', 'snsapi_login');
  url.searchParams.set('state', state || `state-${timestamp}`);
  url.searchParams.set('redirect_uri', REDIRECT_URI);
  if (quickSign) url.searchParams.set('quick_sign', quickSign);
  if (loginTmpCode) url.searchParams.set('loginTmpCode', loginTmpCode);
  url.searchParams.set('timestamp', String(timestamp));
  url.searchParams.set('signature', signature);
  return url.toString();
}


async function authorizeWithLoginTmpCode(loginTmpCode, state = '', quickSign = '') {
  const authorizeUrl = buildAuthorizeUrl({ loginTmpCode, state, quickSign });
  const resp = await fetch(authorizeUrl, {
    method: 'GET',
    redirect: 'manual',
    headers: { 'User-Agent': 'yach-scan-helper/0.1' }
  });

  const location = resp.headers.get('location') || '';
  let code = '';
  if (location) {
    try {
      const u = new URL(location);
      code = u.searchParams.get('code') || '';
    } catch (_) {}
  }

  return {
    status: resp.status,
    location,
    code,
    authorizeUrl
  };
}

async function exchangeCodeForUser(code) {
  if (!APP_ID || !APP_SECRET) throw new Error('Missing YACH_OAUTH_APP_ID / YACH_OAUTH_APP_SECRET');
  const timestamp = Date.now();
  const signature = signTimestamp(timestamp, APP_SECRET);
  const url = new URL('https://yach-oapi.zhiyinlou.com/sns/getuserinfo_bycode');
  url.searchParams.set('accessKey', APP_ID);
  url.searchParams.set('timestamp', String(timestamp));
  url.searchParams.set('signature', signature);

  const body = new URLSearchParams({ tmp_auth_code: code }).toString();
  const data = await httpJson('POST', url.toString(), body, {
    'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8'
  });
  return data;
}

function renderCallbackPage({ code, state, result, error }) {
  const title = error ? 'Yach 扫码登录失败' : 'Yach 扫码登录成功';
  const payload = error ? { error } : result;
  const pretty = escapeHtml(JSON.stringify(payload, null, 2));
  const userid = !error ? (((result || {}).obj || {}).user_info || {}).userid || '' : '';
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${escapeHtml(title)}</title>
  <style>
    body{font-family:ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#0b1020;color:#eef2ff;margin:0;padding:24px}
    .card{max-width:920px;margin:0 auto;background:#131a2f;border:1px solid #2a3358;border-radius:16px;padding:24px}
    .ok{color:#8ef0a7}.err{color:#ff9c9c}.muted{color:#aeb8d6}
    code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}
    pre{background:#0a0f1f;border:1px solid #263055;border-radius:12px;padding:16px;overflow:auto}
    .pill{display:inline-block;padding:4px 10px;border-radius:999px;background:#1a2340;border:1px solid #31406f;margin-right:8px}
    a{color:#9ec1ff}
  </style>
</head>
<body>
  <div class="card">
    <h1 class="${error ? 'err' : 'ok'}">${escapeHtml(title)}</h1>
    <p class="muted">这个页面用于把扫码登录拿到的身份信息展示出来，方便确认 <code>userid</code> 是否可作为 <code>from_user_id</code>。</p>
    <p><span class="pill">code: ${escapeHtml(code || '')}</span><span class="pill">state: ${escapeHtml(state || '')}</span></p>
    ${userid ? `<p>识别到 userid：<strong>${escapeHtml(userid)}</strong></p>` : ''}
    <pre>${pretty}</pre>
    <p><a href="/">返回扫码页</a></p>
  </div>
</body>
</html>`;
}

function escapeHtml(s) {
  return String(s)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#39;');
}

async function readJsonBody(req) {
  const chunks = [];
  for await (const chunk of req) chunks.push(chunk);
  const raw = Buffer.concat(chunks).toString('utf8');
  return raw ? JSON.parse(raw) : {};
}

const server = http.createServer(async (req, res) => {
  try {
    const url = new URL(req.url, `http://127.0.0.1:${PORT}`);
    if (req.method === 'GET' && url.pathname === '/') {
      return sendHtml(res, 200, fs.readFileSync(path.join(STATIC_DIR, 'index.html'), 'utf8'));
    }
    if (req.method === 'GET' && url.pathname === '/app.js') {
      return sendText(res, 200, fs.readFileSync(path.join(STATIC_DIR, 'app.js'), 'utf8'), 'application/javascript; charset=utf-8');
    }
    if (req.method === 'GET' && url.pathname === '/styles.css') {
      return sendText(res, 200, fs.readFileSync(path.join(STATIC_DIR, 'styles.css'), 'utf8'), 'text/css; charset=utf-8');
    }
    if (req.method === 'GET' && url.pathname === '/yyLogin.browser.js') {
      return sendText(res, 200, fs.readFileSync(YYLOGIN_JS, 'utf8'), 'application/javascript; charset=utf-8');
    }
    if (req.method === 'GET' && url.pathname === '/api/bootstrap') {
      let quickSign = '';
      let quickSignError = '';
      try {
        quickSign = await getQuickSign();
      } catch (e) {
        quickSignError = String(e.message || e);
      }
      const authorizeTemplate = APP_ID && APP_SECRET ? buildAuthorizeUrl({ state: 'STATE_PLACEHOLDER', quickSign }) : '';
      return sendJson(res, 200, {
        appId: APP_ID,
        redirectUri: REDIRECT_URI,
        authorizeTemplate,
        quickSignAvailable: Boolean(quickSign),
        quickSignError,
        maskedApiToken: mask(cachedApiToken),
        notes: [
          '如果 quickSign 获取失败，页面仍可用于辅助调试，但扫码二维码可能无法正常渲染或缺少快捷登录能力。',
          '本 helper 默认把扫码结果换到 userid，并显示原始返回。'
        ]
      });
    }
    if (req.method === 'POST' && url.pathname === '/api/authorize-url') {
      const body = await readJsonBody(req);
      const quickSign = (body.quickSign || '') || await getQuickSign().catch(() => '');
      const state = body.state || '';
      const loginTmpCode = body.loginTmpCode || '';
      const authorizeUrl = buildAuthorizeUrl({
        loginTmpCode,
        state,
        quickSign,
      });

      let direct = null;
      let directUserInfo = null;
      let directError = '';
      if (loginTmpCode) {
        try {
          direct = await authorizeWithLoginTmpCode(loginTmpCode, state, quickSign);
          if (direct.code) {
            directUserInfo = await exchangeCodeForUser(direct.code);
          }
        } catch (e) {
          directError = String(e.message || e);
        }
      }

      return sendJson(res, 200, { authorizeUrl, direct, directUserInfo, directError });
    }
    if (req.method === 'GET' && url.pathname === '/oauth/callback') {
      const code = url.searchParams.get('code') || '';
      const state = url.searchParams.get('state') || '';
      if (!code) {
        return sendHtml(res, 400, renderCallbackPage({ code, state, error: '缺少 code 参数，回调未完成或回调域名不正确。' }));
      }
      try {
        const result = await exchangeCodeForUser(code);
        return sendHtml(res, 200, renderCallbackPage({ code, state, result }));
      } catch (e) {
        return sendHtml(res, 500, renderCallbackPage({ code, state, error: String(e.message || e) }));
      }
    }
    return notFound(res);
  } catch (e) {
    return sendJson(res, 500, { error: String(e.message || e) });
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`yach-scan-helper listening on http://127.0.0.1:${PORT}`);
  console.log(`redirect_uri = ${REDIRECT_URI}`);
  if (!APP_ID || !APP_SECRET) {
    console.log('WARNING: missing YACH_OAUTH_APP_ID / YACH_OAUTH_APP_SECRET; copy .env.example to .env and fill them before using the QR flow.');
  }
});
