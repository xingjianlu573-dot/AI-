# -*- coding: utf-8 -*-
"""绘制 AI Business Workflow Automation System 技术架构图（分层）。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 2600, 1700
img = Image.new("RGB", (W, H), "#F8FAFC")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"
def font(sz): return ImageFont.truetype(F, sz)

TITLE = font(52)
SUB = font(24)
LAYER_T = font(26)
MOD_T = font(22)
MOD_S = font(17)
SIDE_T = font(20)

def rr(x1, y1, x2, y2, r, fill, outline, ow=2):
    d.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=fill, outline=outline, width=ow)

def ctext(cx, cy, text, f, fill="#0f172a"):
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    d.text((cx-tw/2, cy-th/2-bb[1]), text, font=f, fill=fill)

# 标题
ctext(W/2, 70, "AI Business Workflow Automation System", TITLE, "#0f172a")
ctext(W/2, 120, "企业客户需求自动处理 · 技术架构", SUB, "#64748b")

# 颜色方案：每层一个色系
LAYERS = [
    ("接入层 Inbound Layer",   "#FEF3C6", "#D97706", "客户从 5 个入口进入，统一汇聚"),
    ("编排层 Orchestration",   "#DBEAFE", "#2563EB", "n8n 工作流引擎：Webhook → 节点串联 → 路由"),
    ("AI 能力层 AI Layer",     "#EDE9FE", "#7C3AED", "LLM 需求分析 · 智能分类 · 自动摘要 · 结构化输出"),
    ("数据层 Data Layer",      "#D1FAE5", "#059669", "飞书多维表格 · 业务数据库 · 数据仓库"),
    ("触达层 Outbound Layer",  "#FFEDD5", "#EA580C", "飞书卡片 · 邮件 · 企微消息 · 短信"),
]

# 主区域：左 200~2100 是分层，右 2150~2500 是横切关注点
LX1, LX2 = 180, 2080
SX1, SX2 = 2140, 2520

# 横切侧栏
rr(SX1, 200, SX2, 1560, 16, "#F1F5F9", "#94A3B8", 2)
ctext((SX1+SX2)/2, 240, "横切能力", LAYER_T, "#334155")
cross = [
    ("凭据管理", "OpenAI / 飞书 App"),
    ("执行日志", "每步入参出参可追溯"),
    ("失败重试", "指数退避 + 告警"),
    ("权限隔离", "按角色看对应工单"),
    ("成本监控", "Token 用量周报"),
]
for i, (t, s) in enumerate(cross):
    y = 310 + i*180
    rr(SX1+20, y, SX2-20, y+140, 12, "#FFFFFF", "#CBD5E1", 2)
    ctext((SX1+SX2)/2, y+45, t, SIDE_T, "#0f172a")
    ctext((SX1+SX2)/2, y+90, s, MOD_S, "#64748b")

# 5 层
top = 200
layer_h = 250
gap = 30
modules_per_layer = [
    ["官网表单", "客户邮件", "企业微信", "客服电话", "小程序/H5"],
    ["Webhook 入口", "条件路由", "紧急度分支", "错误处理", "执行回执"],
    ["LLM 需求分析", "AI 智能分类", "结构化输出", "自动摘要", "Prompt 模板"],
    ["飞书多维表格", "MySQL 业务库", "数据仓库/BI", "工单状态机", "审计日志"],
    ["飞书卡片通知", "邮件通知", "企微群消息", "高危短信", "SLA 升级"],
]

for i, (lname, bg, line, desc) in enumerate(LAYERS):
    y1 = top + i*(layer_h+gap)
    y2 = y1 + layer_h
    rr(LX1, y1, LX2, y2, 16, bg, line, 3)
    ctext(LX1+180, y1+35, lname, LAYER_T, line)
    ctext(LX1+180, y1+72, desc, MOD_S, "#475569")
    # 5 个模块
    mods = modules_per_layer[i]
    mw = (LX2 - LX1 - 40) / 5
    for j, m in enumerate(mods):
        mx1 = LX1+20 + j*mw + 8
        mx2 = LX1+20 + (j+1)*mw - 8
        my1 = y1 + 100
        my2 = y2 - 20
        rr(mx1, my1, mx2, my2, 10, "#FFFFFF", line, 2)
        ctext((mx1+mx2)/2, (my1+my2)/2 - 12, m, MOD_T, "#0f172a")
        ctext((mx1+mx2)/2, (my1+my2)/2 + 22, "●●●", MOD_S, line)

# 层间箭头（中间）
for i in range(4):
    y_a = top + (i+1)*(layer_h+gap) - gap
    y_b = top + (i+1)*(layer_h+gap)
    cx = (LX1+LX2)/2
    d.line([(cx, y_a), (cx, y_b-8)], fill="#94A3B8", width=4)
    d.polygon([(cx-10, y_b-8), (cx+10, y_b-8), (cx, y_b+4)], fill="#94A3B8")

# 底部：数据流标注
by = 1580
ctext(W/2, by+20,
      "数据流：客户进线（HTTPS） → n8n 编排（内存） → LLM API（HTTPS） → 飞书 OpenAPI / MySQL（HTTPS） → 飞书消息推送",
      MOD_S, "#475569")

img.save("docs/architecture.png", "PNG")
print("ok", img.size)
