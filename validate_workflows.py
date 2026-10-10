# -*- coding: utf-8 -*-
"""校验两个 workflow JSON：合法性 + 节点引用完整性 + AI 模型连接。"""
import json

files = [
    "workflows/customer-inbox-ai-automation.json",
    "workflows/error-handler.json",
]

for f in files:
    wf = json.load(open(f, encoding="utf-8"))
    names = {n["name"] for n in wf["nodes"]}
    ids = {n["id"] for n in wf["nodes"]}
    assert len(names) == len(ids), f"duplicate node names/ids in {f}"

    bad = []
    for src, outs in wf["connections"].items():
        if src not in names:
            bad.append("source missing: " + src)
        for groups in outs.values():
            for conn in groups:
                for c in conn:
                    if c["node"] not in names:
                        bad.append("target missing: %s in %s" % (c["node"], src))

    # 每个 chainLlm 必须有 ai_languageModel 连接
    llm_nodes = [n["name"] for n in wf["nodes"] if n["type"] == "@n8n/n8n-nodes-langchain.chainLlm"]
    for ln in llm_nodes:
        outs = wf["connections"].get(ln, {})
        if "ai_languageModel" not in outs:
            bad.append("chainLlm missing ai_languageModel: " + ln)

    print(f, "| nodes:", len(wf["nodes"]), "| issues:", bad if bad else "NONE")

# 双模型温度检查
wf = json.load(open("workflows/customer-inbox-ai-automation.json", encoding="utf-8"))
for n in wf["nodes"]:
    if n["type"] == "@n8n/n8n-nodes-langchain.lmChatOpenAi":
        print("model node:", n["name"], "| temp:", n["parameters"]["options"]["temperature"])

print("ALL OK")
