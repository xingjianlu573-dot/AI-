# AI Business Workflow Automation System

🔗 **[在线演示](https://xingjianlu573-dot.github.io/AI-/)** ｜ **[GitHub 仓库](https://github.com/xingjianlu573-dot/AI-)** ｜ [🇨🇳 国内部署指南](./README_CN.md)

> 一个面向企业场景的 
>
> **AI 工作流自动化**
>
>  案例：基于开源工作流引擎 
>
> [n8n](https://github.com/n8n-io/n8n)
>
> ，把每天涌入的客户咨询、表单、邮件、文档
>
> **自动接住 → 听懂 → 分类 → 落库 → 通知到人**
>
> 。
> 开箱支持 
>
> **国产大模型切换**
>
> （DeepSeek / 通义千问 / 智谱 GLM / 月之暗面 Kimi），
>
> **国内一键 Docker 部署**
>
> ，无需海外网络环境。

[🇨🇳 国内部署指南 README\_CN.md](./README_CN.md) · [业务价值说明](./docs/business-value.md) · [节点说明](./docs/nodes.md)



***

## ✨ 作品集亮点



| 能力               | 本项目落地                                         |
| ---------------- | --------------------------------------------- |
| **Workflow 自动化** | n8n 串联 Webhook → LLM → 分类 → 落库 → 通知，全链路无人工介入  |
| **Agent 式决策**    | LLM 节点输出意图 / 情绪 / 紧急度，由 "紧急度路由" 决定是否升级告警      |
| **结构化输出**        | 用 Structured Output 强约束模型，不让自由发挥污染工单数据        |
| **RAG / 知识沉淀**   | 所有工单自动写入飞书多维表格，天然形成可检索的客户知识库                  |
| **国产模型适配**       | 一套 OpenAI 兼容协议，通过环境变量切换 4 家国产模型               |
| **国内部署能力**       | docker-compose 一键起、Docker 镜像加速、npm 国内源、飞书原生集成 |
| **可观测**          | 每步入参出参留痕、失败重试、健康检查                            |



***

## 🏢 企业痛点

200 人 SaaS 公司每天从 5 个入口（官网表单 / 邮件 / 企微 / 客服电话 / 小程序）收到上百条客户进线。改造前：



* 客服早上开 5 个后台翻消息，漏看是常态；

* 凭经验分类，新员工常错派，客户被 "踢皮球"；

* 手动复制粘贴进 Excel，字段格式混乱，无法统计；

* 微信 @ 同事派单，人在开会就漏单；

* 夜间、周末、节假日无人响应，投诉发酵到社交平台。

**本项目把上面整条链路自动化成分钟级闭环。**



***

## 🔄 自动化流程



```
客户进线（表单/邮件/企微/电话/小程序）
            ↓
   ① Webhook 统一接收
            ↓
   ② LLM 需求分析（意图 / 情绪 / 紧急度）
            ↓
   ③ AI 智能分类（售前/售后/技术/账单/合作/投诉/其他）
            ↓
   ④ 自动生成 60 字摘要
            ↓
   ⑤ 生成结构化工单
            ↓
   ⑥ 同步飞书多维表格 / MySQL
            ↓
   ⑦ 按紧急度飞书卡片通知负责人（红/橙/蓝）
```



![工作流总览](assets/workflow-overview.png)



***

## 🏗️ 技术架构



![技术架构](docs/architecture.png)

五层结构：接入层 → n8n 编排层 → AI 能力层 → 数据层 → 触达层，外加凭据 / 日志 / 重试 / 权限 / 成本五条横切能力。

**技术栈**：



* **工作流引擎**：n8n（自托管，AGPL）

* **大模型**：OpenAI 兼容协议，默认 DeepSeek，可切通义 / 智谱 / Kimi/OpenAI

* **数据存储**：飞书多维表格（业务看板）+ MySQL（系统记录）

* **通知通道**：飞书开放平台 IM 卡片

* **前端表单**：零依赖单文件 HTML



***

## 📁 仓库结构



```
.
├── README.md                  # 本文件（作品集主页）
├── README_CN.md               # 国内部署完整指南
├── .env.example               # 所有环境变量（含国产模型切换）
├── docker-compose.yml         # 一键起 n8n
├── workflows/
│   └── customer-inbox-ai-automation.json   # 导入 n8n 即跑
├── form/
│   └── index.html             # 客户进线表单
├── simulation/
│   └── sample-tickets.json    # 25 条标注好的模拟工单
├── scripts/
│   └── test_ai_provider.py    # AI 接口连通性测试
├── assets/
│   └── workflow-overview.png
└── docs/
    ├── architecture.png
    ├── nodes.md
    ├── business-value.md
    └── test-report.md         # 测试报告
```



***

## 🚀 快速开始（国内用户看这里 → [README\_CN.md](./README_CN.md)）



```
cp .env.example .env          # 填一个国产模型 Key + 飞书凭据
docker compose up -d          # 一键起 n8n（建议先配国内镜像加速）
# 打开 http://localhost:5678，工作流已自动导入，激活即可
```



***

## 💰 业务收益



| 指标        | 改造前            | 改造后      |
| --------- | -------------- | -------- |
| 客户首次响应    | 数小时～1 工作日      | < 1 分钟   |
| 工单错派率     | 15%\~25%       | < 5%     |
| 高危工单隔夜未处理 | 每周 3\~5 起      | ≈ 0      |
| 人工分拣 / 录入 | 每人每天 1.5\~2 小时 | ≈ 0      |
| 数据完整率     | 字段缺失、格式混乱      | 100% 结构化 |



***

## 📜 License

MIT