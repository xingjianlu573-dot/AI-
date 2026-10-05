# 测试报告

测试日期：2026-10-05
测试环境：开发机（Windows），可访问海外网络；**未在中国大陆真实网络环境下回归**。

---

## 1. 已通过的测试（静态 / 本地）

| # | 测试项 | 方法 | 结果 |
|---|---|---|---|
| 1 | 工作流 JSON 合法性 | `json.load()` 解析 `workflows/customer-inbox-ai-automation.json` | ✅ 通过 |
| 2 | 模拟数据 JSON 合法性 | `json.load()` 解析 `simulation/sample-tickets.json`，计数 | ✅ 通过，25 条工单 |
| 3 | docker-compose YAML 合法性 | `yaml.safe_load()` | ✅ 通过 |
| 4 | AI Provider 测试脚本语法 | `ast.parse()` | ✅ 通过 |
| 5 | AI Provider 配置切换逻辑 | 分别设 `MODEL_PROVIDER=deepseek/qwen/zhipu` 跑脚本 | ✅ 三家 base_url / model 正确输出 |
| 6 | 表单 HTML 无外链依赖 | 审查 `form/index.html` | ✅ 零 CDN、零第三方 JS、零外部图片 |
| 7 | 图片资源全部本地化 | 检查 README 里的图片引用 | ✅ 全部相对路径 |
| 8 | 环境变量模板完整性 | 对照代码里用到的所有配置项 | ✅ `.env.example` 覆盖 n8n / 5 家模型 / 飞书 |

---

## 2. 未在本机执行的测试（诚实声明）

以下项目受限于当前环境**没有 Docker、没有各家国产模型 API Key、开发机不在中国大陆**，未做实跑：

| # | 测试项 | 原因 | 用户如何自测 |
|---|---|---|---|
| A | `docker compose up -d` 实际起容器 | 本机未安装 Docker | 按 README_CN 第 1 节配好镜像加速器后执行 |
| B | 真实调用 DeepSeek / 通义 / 智谱 / Kimi API | 没有 API Key | 在 `.env` 填好 Key 后跑 `python scripts/test_ai_provider.py`，看到 `[OK]` 即可 |
| C | n8n 导入工作流后节点串联 | 本机无 n8n | `docker compose up -d` 后浏览器打开 5678，看工作流是否自动出现 |
| D | 飞书多维表格写入 / 卡片通知 | 没有飞书应用凭据 | 按 README_CN 第 5 节配好，用 simulation 里一条数据 POST webhook |
| E | 中国大陆真实访问速度 | 开发机在海外 | 在国内云服务器上 `curl -I https://api.deepseek.com/v1` 等确认延迟 |

**声明**：以上 5 项不是"已经测过没问题"，而是"代码和配置已准备好，等用户填入真实凭据后可一键验证"。

---

## 3. 国内访问风险复检（对照初始审查）

| 初始风险 | 本次优化 | 状态 |
|---|---|---|
| OpenAI API 国内不可直连 | `.env.example` 提供 4 家国产 OpenAI 兼容接口，README_CN 给出切换步骤 | ✅ 已缓解 |
| Docker Hub 拉镜像慢 | README_CN 给出 3 个国内 registry mirror，docker-compose 支持换成阿里云私有镜像 | ✅ 已缓解 |
| n8n 装 npm 包慢 | README_CN 第 3 节给出 `npm config set registry https://registry.npmmirror.com` | ✅ 已缓解 |
| GitHub clone 慢 | README_CN FAQ 给出 ghproxy 镜像 | ✅ 已缓解 |
| 飞书服务国内可达 | 本来就是国内服务 | ✅ 无变化 |
| 前端 CDN / 第三方 JS | 项目本就零外链 | ✅ 无风险 |

---

## 4. 核心功能冒烟测试步骤（用户在国内跑）

```bash
# 1. 配 .env
cp .env.example .env
# 填入 DEEPSEEK_API_KEY=sk-xxx + 飞书五项

# 2. 起 n8n
docker compose up -d

# 3. 测 AI 连通性（PowerShell）
Get-Content .env | ForEach-Object {
  if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
    [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim(), 'Process')
  }
}
python scripts/test_ai_provider.py
# 预期输出：[OK] 调用成功，模型回复：'你好' 之类

# 4. 在 n8n 里激活工作流，POST 一条测试
curl -X POST http://localhost:5678/webhook/customer-inbox `
  -H "Content-Type: application/json" `
  -d '{"name":"测试","contact":"t@t.com","source":"官网表单","message":"我要退款，今天必须处理"}'

# 5. 预期结果
# - 飞书多维表格多一行
# - 你自己飞书收到一张红色/橙色卡片
# - curl 返回 {"code":0,"ticket_id":"TK-..."}
```

---

## 5. 结论

- **静态资产**：全部通过合法性校验；
- **国内可达性**：通过国产模型 + 国内镜像 + 飞书原生集成，已消除海外网络依赖；
- **待用户实跑**：填入真实 API Key 和飞书凭据后，按第 4 节冒烟测试走一遍即可端到端验收。
