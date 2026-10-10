# -*- coding: utf-8 -*-
"""检查 workflow 引用的环境变量是否都在 .env.example 中有定义。"""
import json
import re

wf = json.load(open("workflows/customer-inbox-ai-automation.json", encoding="utf-8"))
env_refs = set()
for n in wf["nodes"]:
    for fld in ["parameters", "json", "webhook"]:
        s = json.dumps(n.get(fld, {}), ensure_ascii=False)
        env_refs |= set(re.findall(r"\$env\.([A-Z_0-9]+)", s))
        env_refs |= set(re.findall(r"env\.([A-Z_0-9]+)", s))

env_file = open(".env.example", encoding="utf-8").read()
defined = set(re.findall(r"^([A-Z_0-9]+)=", env_file, re.M))

print("workflow 引用的环境变量:", sorted(env_refs))
print(".env.example 已定义:", len(defined))
missing = env_refs - defined
print("引用但未定义:", sorted(missing) if missing else "无")

# 引用到的节点依赖（$('...') 跨节点引用）
node_names = {n["name"] for n in wf["nodes"]}
deps = set()
for n in wf["nodes"]:
    s = json.dumps(n.get("parameters", {}), ensure_ascii=False)
    deps |= set(re.findall(r"\$\(\s*['\"]([^'\"]+)['\"]", s))
broken_deps = deps - node_names
print("跨节点引用:", sorted(deps))
print("引用了不存在的节点:", sorted(broken_deps) if broken_deps else "无")
