# 中国大陆部署指南（README_CN）

本文件面向中国大陆用户：**无需代理、无需特殊网络环境**，从零跑通这个企业 AI 自动化案例。

---

## 0. 前置说明

本项目是一个 **n8n 工作流案例**，不是独立的前后端应用。运行时依赖三样东西：

1. **n8n**（开源工作流引擎）—— 用 Docker 一键起；
2. **一个大模型接口** —— 推荐用国产模型，国内直连；
3. **飞书开放平台** —— 国内原生服务，无需任何额外网络配置。

下面给三种部署方式，按你手头资源选。

---

## 1. 方式 A：本地 Docker 运行（推荐先在本机跑通）

### 1.1 配置 Docker 国内镜像加速

国内直连 Docker Hub 拉 `n8nio/n8n` 会很慢甚至超时。先给 Docker 加加速器：

**Windows / macOS（Docker Desktop）**：
Settings → Docker Engine → 在 JSON 里加：

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com",
    "https://docker.mirrors.ustc.edu.cn"
  ]
}
```

**Linux（/etc/docker/daemon.json）**：

```json
{
  "registry-mirrors": [
    "https://docker.m.daocloud.io",
    "https://dockerproxy.com"
  ]
}
```

改完 `sudo systemctl restart docker`。

### 1.2 启动

```bash
git clone https://github.com/xingjianlu573-dot/AI.git
cd AI
cp .env.example .env
# 编辑 .env，至少填一个国产模型的 API Key + 飞书凭据
docker compose up -d
```

打开 http://localhost:5678 ，用 `.env` 里的账号密码登录。

工作流由 compose 里的 `n8n-import` 一次性容器自动导入（首次 `docker compose up -d` 时执行 `n8n import:workflow`，已导入过会自动跳过，不会重复），直接在 n8n 里激活即可。

---

## 2. 方式 B：国内云服务器部署

随便选一家：**阿里云 ECS / 腾讯云 CVM / 华为云 / 火山引擎**，配置 2 核 4G 起步，系统 Ubuntu 22.04。

```bash
# 1) 装 Docker
curl -fsSL https://get.docker.com | bash
# 2) 配上面的镜像加速器
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<'EOF'
{
  "registry-mirrors": ["https://docker.m.daocloud.io"]
}
EOF
sudo systemctl restart docker

# 3) 拉代码、起服务
git clone https://github.com/xingjianlu573-dot/AI.git
cd AI
cp .env.example .env
# 改 .env：
#   N8N_HOST=你的服务器公网IP或域名
#   WEBHOOK_URL=http://你的域名或IP:5678/
docker compose up -d
```

**注意事项**：
- 云厂商安全组要放通 `5678` 端口；
- 正式使用建议套一层 Nginx + HTTPS（Let's Encrypt 或阿里云免费证书）；
- 不要把 n8n 直接裸奔在公网，务必改 `.env` 里的默认密码。

---

## 3. 方式 C：本地 Node 直接跑（不用 Docker）

如果你不想装 Docker，可以直接用 npm 全局跑 n8n：

```bash
# 先把 npm 切到国内源
npm config set registry https://registry.npmmirror.com

# 安装并启动
npm install -g n8n
n8n start
```

打开 http://localhost:5678 ，然后 Workflows → Import from File 选 `workflows/customer-inbox-ai-automation.json`。

---

## 4. 国产大模型配置（关键）

项目默认不再指向 `api.openai.com`（国内不可直连）。在 `.env` 里选一个 provider：

| 提供商 | 环境变量 | 注册地址 | 备注 |
|---|---|---|---|
| **DeepSeek** | `MODEL_PROVIDER=deepseek` | https://platform.deepseek.com/ | 便宜、中文好，推荐 |
| **通义千问** | `MODEL_PROVIDER=qwen` | https://bailian.console.aliyun.com/ | 阿里云百炼，企业稳定 |
| **智谱 GLM** | `MODEL_PROVIDER=zhipu` | https://open.bigmodel.cn/ | 有免费额度 |
| **月之暗面 Kimi** | `MODEL_PROVIDER=moonshot` | https://platform.moonshot.cn/ | 长文本强 |

四家都是 **OpenAI 兼容协议**，所以 n8n 里的 OpenAI 节点只需要改一个地方：
- **Credential → Base URL**：填 `.env` 里对应 `*_BASE_URL`（或填表达式 `{{ $env.OPENAI_BASE_URL }}`）
- **Model**：工作流已内嵌 `$env.LLM_MODEL` 表达式，**不用在节点里改**，直接在 `.env` 设 `LLM_MODEL` 即可（默认 `deepseek-chat`）
- **API Key**：填表达式 `{{ $env.OPENAI_API_KEY }}` 或直接粘 key

切模型 = 改 `.env` 三行：`MODEL_PROVIDER`、`LLM_MODEL`、`OPENAI_BASE_URL`（+ 对应 API Key），全程不用碰工作流。

### 一键验证连通性

```bash
# PowerShell：先加载 .env
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
    [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim(), 'Process')
  }
}
python scripts/test_ai_provider.py
```

看到 `[OK] 调用成功` 就说明模型通了。

---

## 5. 飞书侧配置（国内必做）

1. 打开 https://open.feishu.cn/ → 创建自建应用；
2. 开通权限：
   - `bitable:app`（多维表格读写）
   - `im:message`（发消息）
3. 创建一个多维表格，拿到：
   - `app_token`（URL 里 `/base/` 后面那段）
   - `table_id`（URL 里 `?table=` 后面那段）
4. 把机器人拉到目标群，或者在"成员"里加自己拿到 `user_id`；
5. 填进 `.env`：
   ```
   FEISHU_APP_ID=...
   FEISHU_APP_SECRET=...
   FEISHU_BITABLE_APP_TOKEN=...
   FEISHU_BITABLE_TABLE_ID=...
   FEISHU_OWNER_USER_ID=...
   ```

---

## 6. 常见问题（FAQ）

**Q1：`docker compose up` 拉镜像卡半天？**
A：镜像加速器没配对。检查 `/etc/docker/daemon.json` 或 Docker Desktop 设置里的 `registry-mirrors`，改完重启 Docker。还不行就把 `docker-compose.yml` 里的 `image:` 改成你自己在阿里云镜像服务里同步好的 `registry.cn-hangzhou.aliyuncs.com/.../n8n:latest`。

**Q2：n8n 里测试 OpenAI 节点报 ETIMEDOUT / 连接被拒？**
A：你还在用默认的 `https://api.openai.com/v1`。把 Credential 的 Base URL 改成国产模型地址（见上表）。

**Q3：飞书多维表格写入 401 / 403？**
A：① 应用没开通 `bitable:app` 权限；② 多维表格没把应用加为协作者（打开表格 → 右上角"…"→ 添加文档应用）。

**Q4：飞书卡片发不出来？**
A：检查 `im:message` 权限和 `receive_id_type=user_id` 是否对应。

**Q5：GitHub clone 慢怎么办？**
A：用 `https://ghproxy.com/https://github.com/xingjianlu573-dot/AI.git` 这种加速镜像，或者直接在 GitHub 网页上 Download ZIP。

**Q6：n8n 工作流里为什么还要手动填一次 Base URL？**
A：n8n 的 OpenAI Credential 是存数据库的，不会自动读 `.env`。第一次配置时把 Credential 的 Base URL 填 `{{ $env.OPENAI_BASE_URL }}`、API Key 填 `{{ $env.OPENAI_API_KEY }}` 即可，之后换 provider 只改 `.env`。

**Q7：想换成本地开源模型（Ollama）？**
A：把 `MODEL_PROVIDER=openai`，`OPENAI_BASE_URL=http://host.docker.internal:11434/v1`，`LLM_MODEL=qwen2.5`，n8n 的 OpenAI 节点就能直连本机 Ollama。

---

## 7. 验证清单

跑通后逐项打勾：

- [ ] `docker compose ps` 看到 n8n 容器 healthy
- [ ] 浏览器打开 n8n 不报错
- [ ] `python scripts/test_ai_provider.py` 输出 `[OK]`
- [ ] Workflows 里能看到 `customer-inbox-ai-automation`
- [ ] 点 Test Workflow，用 `simulation/sample-tickets.json` 里一条数据 POST 到 webhook
- [ ] 飞书多维表格多了一行
- [ ] 飞书收到通知卡片
