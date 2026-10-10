# 测试报告

测试日期：2026-10-10（第二轮回归：以用户角度实测 + 静态校验修复）
测试环境：开发机（Windows），可访问海外网络；**未在中国大陆真实网络环境下回归**。

---

## 1. 已通过的测试（静态 / 本地 / 浏览器实测）

| # | 测试项 | 方法 | 结果 |
|---|---|---|---|
| 1 | 工作流 JSON 合法性 + 节点引用完整性 | `json.load()` + 遍历 `connections` 引用核对（`validate_workflows.py`） | ✅ 通过，主工作流 13 节点、error-handler 2 节点，全部 NONE issues |
| 2 | 双模型温度 | 读取两个 `lmChatOpenAi` 节点 | ✅ 分析/分类 0.1、摘要 0.4 |
| 3 | 演示页 JS 语法 | esprima 解析 `index.html` / `demo/index.html` 内嵌脚本 | ✅ 通过（两份一致，10.2k chars） |
| 4 | SLA 矩阵 Code 节点 JS | esprima 按 n8n 函数体方式校验 | ✅ 通过 |
| 5 | 环境变量一致性 | 提取 workflow 全部 `$env.*` 引用 vs `.env.example` | ✅ 引用 5 项全部已定义（修复后） |
| 6 | 跨节点引用完整性 | 检查 `$('节点名')` 引用 | ✅ 无悬空引用 |
| 7 | docker-compose YAML | `yaml.safe_load()` | ✅ 通过，services: n8n + n8n-import |
| 8 | 模拟数据 JSON 合法性 | `json.load()` 解析 `simulation/sample-tickets.json` | ✅ 通过，25 条工单 |
| 9 | AI Provider 测试脚本语法与切换逻辑 | `ast.parse()` + 分别设 provider 跑脚本 | ✅ 通过，deepseek/qwen/zhipu 三家路径解析 OK |
| 10 | 表单 / 演示 HTML 无外链依赖 | 审查 `form/index.html`、`index.html` | ✅ 零 CDN、零第三方 JS、零外部图片 |
| 11 | 图片资源全部本地化 | 检查 README 里的图片引用 | ✅ 全部相对路径 |
| 12 | **浏览器实测演示页**（用户角度） | computer_use 打开 `index.html` → 点击"提交并生成工单" | ✅ 9 节点流水线全部跑通：RAG 命中 2 条、SLA P1/30min、飞书卡片 [P1] 渲染正常 |
| 13 | 演示页文案 bug 回归 | 提交后检查摘要/卡片文本 | ✅ 修复后无"紧急紧急"重复 |

### 本轮修复记录（从 2026-10-05 版本发现问题并修复）

| # | 问题 | 修复 |
|---|---|---|
| A | `LLM_MODEL` 被 workflow 引用但 `.env.example` 未定义 → 模型节点会 fallback 到海外 `gpt-4o-mini`（国内不可直连） | `.env.example` 新增直通段：`LLM_MODEL` / `OPENAI_BASE_URL` / `OPENAI_API_KEY`，README_CN 模型章节改为"改 .env 三行即可" |
| B | README_CN 引导用户手填 Model，与 workflow 内嵌 `$env.LLM_MODEL` 表达式不一致 | 模型配置章节 + Q6/Q7 同步改为表达式指引 |
| C | 仓库已重命名 `AI-`→`AI`，README / README_CN 仍写旧名链接（clone、Pages、仓库地址共 6 处） | 全部更新为 `AI` |
| D | docker-compose 注释声称"挂载 `/workflows` 自动导入"，但 n8n 官方机制是显式 `n8n import:workflow`，照做会导入失败 | 新增 `n8n-import` 一次性容器（list:workflow 判空防重复导入），README_CN 同步说明 |
| E | 演示页摘要/工单卡出现"紧急紧急"（`urgLabel` 已含"紧急"又拼"紧急"） | 紧急度标签统一为完整语义（低紧急/中紧急/高紧急/紧急），展示处不再拼字；卡片颜色判断同步修正 |
| F | 工作流总览图仍是旧 7 节点版，缺 RAG / SLA / 双模型 | 重绘为 9 阶段版（含知识库标注、双模型策略、SLA 矩阵），并修复首版"⑨ 节点出画布截断"问题 |
| G | `docs/nodes.md` 还是旧 7 节点结构 | 重写为 13 节点 + error-handler + 分温度策略 + 新配置表 |
| H | `docs/business-value.md` 仍只提"紧急度路由" | 补充 RAG / SLA / 错误处理亮点 |

---

## 2. 未在本机执行的测试（诚实声明）

以下项目受限于当前环境**没有 Docker、没有各家国产模型 API Key、开发机不在中国大陆**，未做实跑：

| # | 测试项 | 原因 | 用户如何自测 |
|---|---|---|---|
| A | `docker compose up -d` 实际起容器 | 本机未安装 Docker | 按 README_CN 第 1 节配好镜像加速器后执行 |
| B | 真实调用 DeepSeek / 通义 / 智谱 / Kimi API | 没有 API Key | 在 `.env` 填好 Key 后跑 `python scripts/test_ai_provider.py`，看到 `[OK]` 即可 |
| C | n8n 导入工作流后节点串联 | 本机无 n8n | `docker compose up -d` 后，n8n-import 容器会自动导入；浏览器打开 5678 确认 |
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
# 填 OPENAI_API_KEY=sk-xxx（国产模型 Key）+ 飞书五项；LLM_MODEL 默认 deepseek-chat
# 可选：OPENAI_BASE_URL 换成通义/智谱/Kimi 地址

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
