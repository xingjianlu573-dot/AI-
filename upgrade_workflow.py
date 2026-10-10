# -*- coding: utf-8 -*-
"""升级 workflow JSON：RAG 检索 + SLA 矩阵 + 分温度双模型 + 重试。"""
import json, io, copy

P = "workflows/customer-inbox-ai-automation.json"
wf = json.load(open(P, encoding="utf-8"))

# ---------- 1. 原模型改名（分析/分类用，低温 0.1） ----------
for n in wf["nodes"]:
    if n["id"] == "node-chat-model":
        n["name"] = "OpenAI Chat Model（分析/分类）"
        n["parameters"]["options"]["temperature"] = 0.1
        n["position"] = [120, -40]

# ---------- 2. 新增：摘要专用模型（中温 0.4，更自然的摘要） ----------
wf["nodes"].append({
    "parameters": {"model": "={{ $env.OPENAI_MODEL || 'gpt-4o-mini' }}",
                   "options": {"temperature": 0.4}},
    "id": "node-chat-model-summary",
    "name": "OpenAI Chat Model（摘要）",
    "type": "@n8n/n8n-nodes-langchain.lmChatOpenAi",
    "typeVersion": 1.2,
    "position": [520, -40]
})

# ---------- 3. 新增：知识库检索（RAG）节点 ----------
kb_node = {
    "parameters": {
        "url": "={{ $env.KB_SEARCH_URL }}?q={{ encodeURIComponent($('③ AI 智能分类').item.json.intent || $('① 表单/Webhook 接收').item.json.body.message) }}&top_k=3",
        "method": "GET",
        "authentication": "none",
        "sendHeaders": False,
        "sendBody": False,
        "options": {
            "response": {"response": {"responseFormat": "json"}},
            "retryOnFail": True
        }
    },
    "id": "node-kb-search",
    "name": "知识库检索（RAG）",
    "type": "n8n-nodes-base.httpRequest",
    "typeVersion": 4.2,
    "position": [520, 300]
}
wf["nodes"].append(kb_node)

# ---------- 4. 摘要节点：prompt 注入 RAG 上下文 ----------
for n in wf["nodes"]:
    if n["id"] == "node-llm-summary":
        n["parameters"]["text"] = (
            "=请用不超过 60 个汉字，为这条客户工单生成一段摘要，便于负责人在飞书通知里快速扫读。\n\n"
            "客户：{{ $('① 表单/Webhook 接收').item.json.body.name || '未知' }}\n"
            "分类：{{ $json.category }}\n情绪：{{ $json.sentiment }}\n紧急度：{{ $json.urgency }}\n"
            "诉求：{{ $json.intent }}\n期望动作：{{ $json.expectedAction }}\n\n"
            "知识库检索到的相关政策片段（可用于澄清或补充背景，不要照抄）：\n"
            "{{ $('知识库检索（RAG）').item.json.top_k ? $('知识库检索（RAG）').item.json.top_k.map(x => x.content).join('；').slice(0, 300) : '无' }}\n\n"
            "输出就是摘要正文，不要加前缀。"
        )
        n["parameters"]["options"]["systemMessage"] = "你是工单摘要撰写人。输出就是摘要正文，不要加前缀、不要加引号、不要换行。"

# ---------- 5. SLA 矩阵：替换 紧急度路由 节点 ----------
sla_node = {
    "parameters": {
        "jsCode": """// SLA 矩阵：分类 × 紧急度 → 响应时限 / 负责人团队
const SLAs = {
  //            low                 medium              high                critical
  sales_inquiry:{level:'P4',time:'24h', team:'销售部'},
  after_sales:  {level:'P3',time:'8h',  team:'售后部'},
  tech_support: {level:'P3',time:'4h',  team:'技术支持'},
  billing:      {level:'P3',time:'4h',  team:'财务部'},
  partnership:  {level:'P4',time:'24h', team:'商务部'},
  complaint:    {level:'P2',time:'2h',  team:'客户成功'},
  other:        {level:'P4',time:'24h', team:'客服中心'},
};
const U = { low:0, medium:1, high:2, critical:3 };
const urgent = { 'high': {level:'P2',time:'1h'}, 'critical': {level:'P1',time:'30min'} };
const cat = $json.category || 'other';
const urg = $json.urgency || 'low';
const base = SLAs[cat] || SLAs.other;
let sla = base;
if (U[urg] >= 2) sla = Object.assign({}, base, urgent[urg]);
// 特殊：投诉 + 高/紧急 一律 P1
if (cat === 'complaint' && U[urg] >= 2) sla = {level:'P1', time:'30min', team:'客户成功+主管'};
if (cat === 'tech_support' && urg === 'critical') sla = {level:'P1', time:'30min', team:'技术支持+主管'};
$json.sla_level = sla.level;
$json.sla_time = sla.time;
$json.sla_owner = sla.team;
return $json;"""
    },
    "id": "node-sla-matrix",
    "name": "SLA 矩阵（28 组合）",
    "type": "n8n-nodes-base.function",
    "typeVersion": 1,
    "position": [1240, 440]
}
wf["nodes"] = [n for n in wf["nodes"] if n["id"] != "node-urgency-switch"]
wf["nodes"].append(sla_node)

# ---------- 6. 通知节点：卡片带上 SLA ----------
for n in wf["nodes"]:
    if n["id"] == "node-notify-owner":
        n["parameters"]["jsonBody"] = (
            "={\n  \"receive_id\": \"{{ $env.FEISHU_OWNER_USER_ID }}\",\n"
            "  \"msg_type\": \"interactive\",\n"
            "  \"content\": JSON.stringify({\n"
            "    config: { wide_screen_mode: true },\n"
            "    header: {\n"
            "      template: $json.urgency === 'critical' ? 'red' : ($json.urgency === 'high' ? 'orange' : 'blue'),\n"
            "      title: { tag: 'plain_text', content: '新客户工单 ' + $json.ticket_id + ' [' + $json.sla_level + ']' }\n"
            "    },\n"
            "    elements: [\n"
            "      { tag: 'div', text: { tag: 'lark_md', content: '**分类：**' + $json.category + '\\n**紧急度：**' + $json.urgency + '\\n**情绪：**' + $json.sentiment + '\\n**客户：**' + $json.customer_name + '（' + $json.contact + '）' } },\n"
            "      { tag: 'hr' },\n"
            "      { tag: 'div', text: { tag: 'lark_md', content: '**AI 摘要：**\\n' + $json.summary } },\n"
            "      { tag: 'div', text: { tag: 'lark_md', content: '**SLA：**' + $json.sla_level + ' · ' + $json.sla_time + ' 内响应 · 责任团队：' + $json.sla_owner } },\n"
            "      { tag: 'note', elements: [{ tag: 'plain_text', content: '来源：' + $json.source + ' · 已同步至飞书多维表格' }] }\n"
            "    ]\n"
            "  })\n}"
        )
        n["parameters"]["options"] = {"retryOnFail": True}

# ---------- 7. 同步飞书：写入 SLA 字段 + 重试 ----------
for n in wf["nodes"]:
    if n["id"] == "node-sync-feishu":
        n["parameters"]["jsonBody"] = (
            "={\n  \"fields\": {\n"
            "    \"工单号\": $json.ticket_id,\n    \"客户\": $json.customer_name,\n"
            "    \"联系方式\": $json.contact,\n    \"来源\": $json.source,\n"
            "    \"分类\": $json.category,\n    \"情绪\": $json.sentiment,\n"
            "    \"紧急度\": $json.urgency,\n    \"SLA等级\": $json.sla_level,\n"
            "    \"SLA时限\": $json.sla_time,\n    \"摘要\": $json.summary,\n"
            "    \"原始内容\": $json.raw_message,\n    \"状态\": $json.status,\n"
            "    \"创建时间\": {{ $now.format('x') }}\n  }\n}"
        )
        n["parameters"]["options"] = {"response": {"response": {"responseFormat": "json"}}, "retryOnFail": True}

# ---------- 8. 重连 connections ----------
conn = wf["connections"]

# ③ 之后接 知识库检索（RAG）
conn["③ AI 智能分类"]["main"] = [[{"node": "知识库检索（RAG）", "type": "main", "index": 0}]]

# 知识库检索 → ④
conn["知识库检索（RAG）"] = {"main": [[{"node": "④ 自动生成摘要", "type": "main", "index": 0}]]}

# ④ 用摘要模型
conn["④ 自动生成摘要"]["ai_languageModel"] = [[{"node": "OpenAI Chat Model（摘要）", "type": "ai_languageModel", "index": 0}]]

# ⑤ → ⑥ + SLA 矩阵（替换原 紧急度路由）
conn["⑤ 生成结构化工单记录"]["main"] = [[
    {"node": "⑥ 同步飞书多维表格", "type": "main", "index": 0},
    {"node": "SLA 矩阵（28 组合）", "type": "main", "index": 0}
]]

# SLA 矩阵 → ⑦
conn["SLA 矩阵（28 组合）"] = {"main": [[{"node": "⑦ 自动通知负责人", "type": "main", "index": 0}]]}

# 删除旧 紧急度路由 连接
conn.pop("紧急度路由", None)

json.dump(wf, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("nodes:", len(wf["nodes"]))
print("connections:", list(conn.keys()))
