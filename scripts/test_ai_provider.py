# -*- coding: utf-8 -*-
r"""
AI Provider 连通性测试脚本
根据环境变量 MODEL_PROVIDER 选择对应国产/海外 OpenAI 兼容接口，发一条最简 chat completion。

用法：
    # 1) 先加载 .env（PowerShell）：
    Get-Content .env | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            [Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim(), 'Process')
        }
    }
    # 2) 跑：
    python scripts/test_ai_provider.py
"""
import json
import os
import sys
import urllib.request
import urllib.error

# 各家 provider 的默认配置（全部 OpenAI 兼容协议）
PROVIDERS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "model": "deepseek-chat",
        "key_env": "DEEPSEEK_API_KEY",
    },
    "qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-plus",
        "key_env": "DASHSCOPE_API_KEY",
    },
    "zhipu": {
        "base_url": "https://open.bigmodel.cn/api/paas/v4",
        "model": "glm-4-flash",
        "key_env": "ZHIPU_API_KEY",
    },
    "moonshot": {
        "base_url": "https://api.moonshot.cn/v1",
        "model": "moonshot-v1-8k",
        "key_env": "MOONSHOT_API_KEY",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
        "key_env": "OPENAI_API_KEY",
    },
}


def main():
    provider = os.environ.get("MODEL_PROVIDER", "deepseek").lower()
    if provider not in PROVIDERS:
        print(f"[X] 未知 MODEL_PROVIDER={provider}，可选：{list(PROVIDERS)}")
        sys.exit(1)

    cfg = PROVIDERS[provider]
    api_key = os.environ.get(cfg["key_env"], "").strip()
    model = os.environ.get(f"{provider.upper()}_MODEL", cfg["model"])
    base_url = os.environ.get(f"{provider.upper()}_BASE_URL", cfg["base_url"]).rstrip("/")

    print(f"==> Provider: {provider}")
    print(f"    Base URL : {base_url}")
    print(f"    Model    : {model}")
    if not api_key or api_key.startswith("sk-xxxx"):
        print("[!] 未配置 API Key，跳过实际调用（仅打印配置）")
        return

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "用一个字回答：你好"}],
        "temperature": 0,
        "max_tokens": 10,
    }
    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            answer = body["choices"][0]["message"]["content"].strip()
            print(f"[OK] 调用成功，模型回复：{answer!r}")
    except urllib.error.HTTPError as e:
        print(f"[X] HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:300]}")
        sys.exit(2)
    except Exception as e:
        print(f"[X] 网络错误：{e}")
        print("    国内用户请确认用的是国产 provider，且本机能直连该 base_url。")
        sys.exit(3)


if __name__ == "__main__":
    main()
