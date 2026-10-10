# -*- coding: utf-8 -*-
"""修复 1) 文档中旧仓库名 AI- 链接；2) .env.example 缺失的直通变量。"""
import re

# ---- 1) README.md 与 README_CN.md 旧链接修复 ----
fixes = [
    ("README.md", "https://xingjianlu573-dot.github.io/AI-/", "https://xingjianlu573-dot.github.io/AI/"),
    ("README.md", "https://github.com/xingjianlu573-dot/AI-", "https://github.com/xingjianlu573-dot/AI"),
    ("README_CN.md", "https://github.com/xingjianlu573-dot/AI-.git", "https://github.com/xingjianlu573-dot/AI.git"),
    ("README_CN.md", "cd AI-", "cd AI"),
    ("README_CN.md", "https://ghproxy.com/https://github.com/xingjianlu573-dot/AI-.git", "https://ghproxy.com/https://github.com/xingjianlu573-dot/AI.git"),
]
for f, old, new in fixes:
    s = open(f, encoding="utf-8").read()
    n = s.count(old)
    if n:
        open(f, "w", encoding="utf-8").write(s.replace(old, new))
        print(f"[FIX] {f}: {n} 处 '{old}' -> '{new}'")
    else:
        print(f"[--] {f}: 未找到 '{old}'")

# ---- 2) .env.example 增加工作流直通变量（LLM_MODEL / OPENAI_BASE_URL / OPENAI_API_KEY）----
env = open(".env.example", encoding="utf-8").read()
if "LLM_MODEL=" not in env:
    block = """
# ============================================================
# n8n 工作流实际读取的三个变量（OpenAI 兼容直通）
# 模型节点参数已内嵌表达式 $env.LLM_MODEL，默认 DeepSeek。
# 切换模型只改这三行 + MODEL_PROVIDER，无需改 n8n 节点。
# n8n 凭据配置：Base URL 填  {{ $env.OPENAI_BASE_URL }}
#              API Key 填  {{ $env.OPENAI_API_KEY }}
# ============================================================
# 国内用户默认用 DeepSeek（可直连）；改其他家就换成对应地址与模型名
LLM_MODEL=deepseek-chat
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxx

"""
    # 插到 MODEL_PROVIDER 段之前
    anchor = "# 可选项：openai | deepseek | qwen | zhipu | moonshot\n"
    assert anchor in env, "anchor not found"
    env = env.replace(anchor, anchor + block)
    open(".env.example", "w", encoding="utf-8").write(env)
    print("[FIX] .env.example: 增加 LLM_MODEL / OPENAI_BASE_URL / OPENAI_API_KEY 直通段")
else:
    print("[--] .env.example: LLM_MODEL 已存在")
