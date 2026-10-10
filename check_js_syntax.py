# -*- coding: utf-8 -*-
"""用 esprima 检查项目中所有内嵌 JS 的语法（用户角度自检）。"""
import esprima
import json
import re
import sys

issues = []

# 1. 演示页 index.html 与 demo/index.html 的内嵌 <script>
for path in ["index.html", "demo/index.html"]:
    html = open(path, encoding="utf-8").read()
    scripts = re.findall(r"<script>(.*?)</script>", html, re.S)
    for i, code in enumerate(scripts):
        try:
            esprima.parseScript(code)
            print(f"[OK] {path} script#{i} 语法通过 ({len(code)} chars)")
        except Exception as e:
            issues.append(f"{path} script#{i}: {e}")
            print(f"[X]  {path} script#{i}: {e}")

# 2. workflow 内 Code 节点的 jsCode
wf = json.load(open("workflows/customer-inbox-ai-automation.json", encoding="utf-8"))
for n in wf["nodes"]:
    if n["type"] == "n8n-nodes-base.function":
        code = n["parameters"].get("jsCode", "")
        # n8n Function 节点把代码包在函数体内执行，顶层 return 合法；模拟该运行方式
        wrapped = "function __n8n_run() {\n" + code + "\n}"
        try:
            esprima.parseScript(wrapped)
            print(f"[OK] 节点 {n['name']} jsCode 语法通过（按 n8n 函数体方式校验）")
        except Exception as e:
            issues.append(f"节点 {n['name']}: {e}")
            print(f"[X]  节点 {n['name']}: {e}")

print("\n=== 结论 ===")
if issues:
    print("发现问题:", len(issues))
    for i in issues:
        print(" -", i)
    sys.exit(1)
else:
    print("全部 JS 语法通过")
