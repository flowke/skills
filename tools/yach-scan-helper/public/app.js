const bootstrapEl = document.getElementById('bootstrap');
const eventsEl = document.getElementById('events');
const renderBtn = document.getElementById('renderBtn');
let bootstrap = null;
let stateValue = `state-${Date.now()}`;

function log(message, extra) {
  const line = `[${new Date().toLocaleTimeString()}] ${message}` + (extra ? `\n${JSON.stringify(extra, null, 2)}` : '');
  eventsEl.textContent = `${line}\n\n${eventsEl.textContent}`.slice(0, 12000);
}

async function fetchBootstrap() {
  const resp = await fetch('/api/bootstrap');
  bootstrap = await resp.json();
  bootstrapEl.textContent = JSON.stringify(bootstrap, null, 2);
  return bootstrap;
}

function renderQr() {
  if (!bootstrap) return;
  if (!bootstrap.appId) {
    log('缺少 appId，请先在 .env 中配置 YACH_OAUTH_APP_ID / YACH_OAUTH_APP_SECRET');
    return;
  }
  const template = bootstrap.authorizeTemplate;
  if (!template) {
    log('没有可用的 authorizeTemplate，可能是配置不完整。');
    return;
  }
  const goto = encodeURIComponent(template.replace('STATE_PLACEHOLDER', stateValue));
  log('开始渲染二维码', { goto });
  if (typeof window.yyLogin !== 'function') {
    log('yyLogin 未加载成功，请检查 /yyLogin.browser.js');
    return;
  }
  window.yyLogin({
    id: 'login_container',
    goto,
    style: 'border:none;background-color:#FFFFFF;',
    width: '365px',
    height: '400px'
  });
}

window.addEventListener('message', async (event) => {
  const origin = event.origin;
  if (origin !== 'https://yach-work.zhiyinlou.com') {
    return;
  }
  const data = event.data;
  log('收到来自 yach-work.zhiyinlou.com 的 postMessage', { data });
  if (!data || typeof data !== 'string') return;

  // 文档提到 event.data 有时可能是 refreshUrl；这里仅做日志。
  if (data.startsWith('http')) {
    log('检测到 refreshUrl，可按需刷新二维码', { refreshUrl: data });
    return;
  }

  // 其余字符串大概率是 loginTmpCode
  try {
    const resp = await fetch('/api/authorize-url', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ loginTmpCode: data, state: stateValue })
    });
    const json = await resp.json();
    log('收到后端生成的授权结果', json);
    if (json.directUserInfo) {
      const userid = (((json.directUserInfo || {}).obj || {}).user_info || {}).userid || '';
      log('已直接解析出 userid', { userid, directUserInfo: json.directUserInfo });
      alert(userid ? `扫码成功，userid = ${userid}` : '扫码成功，但返回里没有 userid，请看页面日志');
      return;
    }
    if (json.authorizeUrl) {
      log('未能直接解析 userid，回退为浏览器跳转授权', { authorizeUrl: json.authorizeUrl });
      window.location.href = json.authorizeUrl;
    }
  } catch (err) {
    log('根据 loginTmpCode 构造授权跳转失败', { error: String(err) });
  }
});

renderBtn.addEventListener('click', () => {
  stateValue = `state-${Date.now()}`;
  renderQr();
});

fetchBootstrap().then(() => {
  log('bootstrap 完成');
}).catch((err) => {
  bootstrapEl.textContent = String(err);
  log('bootstrap 失败', { error: String(err) });
});
