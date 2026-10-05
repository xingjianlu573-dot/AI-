# -*- coding: utf-8 -*-
"""绘制 AI Workflow Automation Platform 工作流示意图（n8n 风格）。无 emoji 版。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 2600, 1500
img = Image.new("RGB", (W, H), "#F7F8FA")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"
def font(sz): return ImageFont.truetype(F, sz)

TITLE = font(54)
SUB = font(26)
NODE_T = font(29)
NODE_S = font(20)
SMALL = font(20)
VAL = font(22)
HEAD = font(28)

C = {
    "trigger":  ("#E5E7EB", "#4B5563"),
    "ai":       ("#EDE9FE", "#6D28D9"),
    "data":     ("#DBEAFE", "#1D4ED8"),
    "sync":     ("#D1FAE5", "#047857"),
    "notify":   ("#FFEDD5", "#C2410C"),
    "model":    ("#FCE7F3", "#BE185D"),
}

def rr(x1, y1, x2, y2, r, fill, outline, ow=3):
    d.rounded_rectangle([x1, y1, x2, y2], radius=r, fill=fill, outline=outline, width=ow)

def ctext(cx, cy, text, f, fill="#111827"):
    bb = d.textbbox((0, 0), text, font=f)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    d.text((cx-tw/2, cy-th/2-bb[1]), text, font=f, fill=fill)

# 标题
ctext(W/2, 75, "AI Workflow Automation Platform", TITLE, "#111827")
ctext(W/2, 135, "企业客户进线智能受理流程 · 表单 / 邮件 / 咨询 / 文档 自动处理", SUB, "#6B7280")

NW, NH = 310, 130
y = 580
xs = [195, 575, 955, 1335, 1715, 2095, 2475]

nodes = [
    (xs[0], y, "trigger", "①", "表单 / Webhook 接收", "客户进线统一入口"),
    (xs[1], y, "ai",      "②", "LLM 需求分析", "意图·情绪·紧急度"),
    (xs[2], y, "ai",      "③", "AI 智能分类", "7 类业务自动归口"),
    (xs[3], y, "ai",      "④", "自动生成摘要", "60 字工单摘要"),
    (xs[4], y, "data",    "⑤", "生成工单记录", "结构化落库字段"),
    (xs[5], y, "sync",    "⑥", "同步飞书 / 数据库", "多维表格自动写入"),
    (xs[6], y, "notify",  "⑦", "自动通知负责人", "飞书卡片按紧急度"),
]

boxes = []
for cx, cy, key, num, t, s in nodes:
    fill, line = C[key]
    x1, y1, x2, y2 = cx-NW/2, cy-NH/2, cx+NW/2, cy+NH/2
    rr(x1, y1, x2, y2, 18, fill, line, 3)
    # 编号圆
    d.ellipse([x1+14, cy-22, x1+58, cy+22], fill=line)
    ctext(x1+36, cy, num, font(24), "#FFFFFF")
    ctext(cx+20, cy-28, t, NODE_T, "#111827")
    ctext(cx+20, cy+24, s, NODE_S, line)
    boxes.append((x1, y1, x2, y2, cx, cy))

# 主箭头
for i in range(len(boxes)-1):
    ax, bx, ay, by = boxes[i][2], boxes[i+1][0], y, y
    d.line([(ax+6, ay), (bx-18, by)], fill="#9CA3AF", width=5)
    d.polygon([(bx-18, by-11), (bx-18, by+11), (bx-4, by)], fill="#9CA3AF")

# 模型节点
mx, my = 955, 310
rr(mx-200, my-55, mx+200, my+55, 14, C["model"][0], C["model"][1], 3)
ctext(mx, my-16, "LLM 大模型", NODE_T, "#111827")
ctext(mx, my+22, "GPT-4o-mini · temperature 0.1", SMALL, C["model"][1])
for idx in [1, 2, 3]:
    tx = boxes[idx][4]
    d.line([(mx, my+55), (tx, y-NH/2-6)], fill="#F9A8D4", width=3)
    d.ellipse([tx-6, y-NH/2-12, tx+6, y-NH/2], fill=C["model"][1])

# 节点下方业务注解
values = [
    "替代人工分诊\n进线 0 等待",
    "听懂客户\n不再靠关键词",
    "自动派单\n减少错派漏派",
    "扫一眼就知道\n要不要紧",
    "记录标准化\n可统计可复盘",
    "数据不落地\n不靠人工抄录",
    "高危工单秒级触达\n投诉不隔夜",
]
for i, b in enumerate(boxes):
    cx = b[4]
    for j, line in enumerate(values[i].split("\n")):
        ctext(cx, y+NH/2+45+j*30, line, VAL, "#374151")

# 底部：前后对比
by0 = 1130
d.rounded_rectangle([100, by0, W-100, by0+320], radius=20, fill="#FFFFFF", outline="#E5E7EB", width=2)
ctext(W/2, by0+45, "流程优化：从「人工分拣 + 手动录入 + 挨个通知」到「AI 自动受理，分钟级闭环」", HEAD, "#111827")

cols = [
    (450,  "改造前", "#FEE2E2", "#B91C1C",
        ["人工逐个看邮件 / 表单", "凭经验分类、经常错派", "手动复制进 Excel", "下班后工单无人跟进", "投诉靠打电话挨个催"]),
    (1300, "改造后", "#DCFCE7", "#15803D",
        ["全渠道进线统一接入", "LLM 识别意图/情绪/紧急度", "结构化字段写入飞书表格", "卡片自动 @ 对应负责人", "高危工单实时推送告警"]),
    (2150, "业务收益", "#DBEAFE", "#1D4ED8",
        ["响应时长 小时级 → 分钟级", "人工分拣工作量 下降约 80%", "分类准确率 稳定 90% 以上", "投诉处理不隔夜", "工单数据可沉淀、可分析"]),
]
for cx, title, bg, fg, lines in cols:
    d.rounded_rectangle([cx-280, by0+85, cx+280, by0+300], radius=14, fill=bg)
    ctext(cx, by0+115, title, NODE_T, fg)
    for j, line in enumerate(lines):
        ctext(cx, by0+155+j*28, line, SMALL, "#1F2937")

img.save("assets/workflow-overview.png", "PNG")
print("ok", img.size)
