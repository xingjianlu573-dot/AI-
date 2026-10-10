# -*- coding: utf-8 -*-
"""修复自检发现的 bug：SLA 顺序 / RAG 兜底 / LLM_MODEL 统一。"""
import json

f = "workflows/customer-inbox-ai-automation.json"
wf = json.load(open(f, encoding="utf-8"))

# ---- Fix A: ⑤ → SLA矩阵 → [⑥, ⑦]（让 ⑥ 拿到 sla_level）----
wf["connections"]["⑤ 生成结构化工单记录"]["main"] = [[
    {"node": "SLA 矩阵（28 组合）", "type": "main", "index": 0}
]]
wf["connections"]["SLA 矩阵（28 组合）"]["main"] = [[
    {"node": "⑥ 同步飞书多维表格", "type": "main", "index": 0},
    {"node": "⑦ 自动通知负责人", "type": "main", "index": 0}
]]

# ---- Fix B: 知识库检索节点失败不阻断主流程 ----
for n in wf["nodes"]:
    if n["id"] == "node-kb-search":
        n["onError"] = "continueRegularOutput"

    # ---- Fix D: 模型节点统一用 LLM_MODEL ----
    if n["type"] == "@n8n/n8n-nodes-langchain.lmChatOpenAi":
        n["parameters"]["model"] = "={{ $env.LLM_MODEL || 'gpt-4o-mini' }}"

    # ---- 摘要 prompt：可选链兜底，检索失败/为空时不报错 ----
    if n["id"] == "node-llm-summary":
        n["parameters"]["text"] = (
            "=请用不超过 60 个汉字，为这条客户工单生成一段摘要，便于负责人在飞书通知里快速扫读。\n\n"
            "客户：{{ $('① 表单/Webhook 接收').first().json.body.name || '未知' }}\n"
            "分类：{{ $json.category }}\n情绪：{{ $json.sentiment }}\n紧急度：{{ $json.urgency }}\n"
            "诉求：{{ $json.intent }}\n期望动作：{{ $json.expectedAction }}\n\n"
            "知识库检索到的相关政策片段（仅作背景参考，不要照抄）：\n"
            "{{ ($('知识库检索（RAG）').first()?.json?.top_k || []).map(x => x.content).join('；').slice(0, 300) || '无' }}\n\n"
            "输出就是摘要正文，不要加前缀。"
        )

json.dump(wf, open(f, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("workflow fixed")
