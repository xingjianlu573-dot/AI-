# -*- coding: utf-8 -*-
"""绘制 AI Workflow Automation Platform 工作流示意图（n8n 风格，9 阶段 / 13 节点）。无 emoji 版。"""
from PIL import Image, ImageDraw, ImageFont

W, H = 2800, 1500
img = Image.new("RGB", (W, H), "#F7F8FA")
d = ImageDraw.Draw(img)

F = "C:/Windows/Fonts/msyh.ttc"
def font(sz): return ImageFont.truetype(F, sz)

TITLE = font(54)
SUB = font(26)
NODE_T = font(26)
NODE_S = font(19)
SMALL = font(20)
VAL = font(22)
HEAD = font(28)

C = {
    "trigger":  ("#E5E7EB", "#4B5563"),
    "ai":       ("#EDE9FE", "#6D28D9"),
    "rag":      ("#E0E7FF", "#4338CA"),
    "data":     ("#DBEAFE", "#1D4ED8"),
    "sla":      ("#FEF3C7", "#B45309"),
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

NW, NH = 250, 128
y = 560
# 9 个阶段横排（2800 宽，留足箭头空间）
xs = [155, 474, 793, 1112, 1431, 1750, 2069, 2388, 2707]

nodes = [
    (xs[0], y, "trigger", "①", "Webhook 接收", "客户进线统一入口"),
    (xs[1], y, "ai",      "②", "LLM 需求分析", "意图·情绪·紧急度 · 0.1"),
    (xs[2], y, "ai",      "③", "AI 智能分类", "7 类业务自动归口 · 0.1"),
    (xs[3], y, "rag",     "④", "知识库检索 RAG", "检索政策片段 top-k"),
    (xs[4], y, "ai",      "⑤", "自动生成摘要", "≤60 字 · 引用知识库 · 0.4"),
    (xs[5], y, "data",    "⑥", "生成工单记录", "结构化落库字段"),
    (xs[6], y, "sla",     "⑦", "SLA 矩阵 28 组合", "分类×紧急度→P1~P4+团队"),
    (xs[7], y, "sync",    "⑧", "同步飞书/数据库", "多维表格自动写入"),
    (xs[8], y, "notify",  "⑨", "通知负责人", "飞书卡片带 SLA 徽章"),
]

boxes = []
for cx, cy, key, num, t, s in nodes:
    fill, line = C[key]
    x1, y1, x2, y2 = cx-NW/2, cy-NH/2, cx+NW/2, cy+NH/2
    rr(x1, y1, x2, y2, 18, fill, line, 3)
    d.ellipse([x1+10, cy-20, x1+50, cy+20], fill=line)
    ctext(x1+30, cy, num, font(22), "#FFFFFF")
    ctext(cx+30, cy-26, t, NODE_T, "#111827")
    ctext(cx+30, cy+24, s, NODE_S, line)
    boxes.append((x1, y1, x2, y2, cx, cy))

# 主箭头
for i in range(len(boxes)-1):
    ax, bx, ay, by = boxes[i][2], boxes[i+1][0], y, y
    d.line([(ax+4, ay), (bx-14, by)], fill="#9CA3AF", width=5)
    d.polygon([(bx-14, by-11), (bx-14, by+11), (bx, by)], fill="#9CA3AF")

# 模型节点（分温度双模型）
mx, my = 1431, 250
rr(mx-230, my-70, mx+230, my+70, 14, C["model"][0], C["model"][1], 3)
ctext(mx, my-42, "LLM 双模型策略", NODE_T, "#111827")
ctext(mx, my+2, "分析/分类 · temp 0.1（一致性）", SMALL, C["model"][1])
ctext(mx, my+36, "摘要 · temp 0.4（自然）", SMALL, C["model"][1])
for idx in [1, 2, 4]:
    tx = boxes[idx][4]
    d.line([(mx, my+70), (tx, y-NH/2-6)], fill="#F9A8D4", width=3)
    d.ellipse([tx-6, y-NH/2-12, tx+6, y-NH/2], fill=C["model"][1])

# RAG 知识库来源标注（放在 ④ 上方、副标题下方，避免重叠）
ragx = boxes[3][4]
ragy = 208
d.line([(ragx, y-NH/2-6), (ragx, ragy+24)], fill="#A5B4FC", width=3)
rr(ragx-190, ragy-24, ragx+190, ragy+24, 12, "#EEF2FF", C["rag"][1], 2)
ctext(ragx, ragy, "知识库（Qdrant/pgvector/飞书）", NODE_S, C["rag"][1])

# 节点下方业务注解
values = [
    "替代人工分诊\n进线 0 等待",
    "听懂客户\n不再靠关键词",
    "自动派单\n减少错派漏派",
    "答案有依据\n不编造口径",
    "扫一眼就知道\n要不要紧",
    "记录标准化\n可统计可复盘",
    "响应时限\n不再是拍脑袋",
    "数据不落地\n不靠人工抄录",
    "高危工单秒级触达\n投诉不隔夜",
]
for i, b in enumerate(boxes):
    cx = b[4]
    for j, line in enumerate(values[i].split("\n")):
        ctext(cx, y+NH/2+42+j*30, line, VAL, "#374151")

# 底部：前后对比
by0 = 1130
d.rounded_rectangle([100, by0, W-100, by0+320], radius=20, fill="#FFFFFF", outline="#E5E7EB", width=2)
ctext(W/2, by0+45, "流程优化：从「人工分拣 + 手动录入 + 挨个通知」到「AI 自动受理 + RAG 检索 + SLA 路由，分钟级闭环」", HEAD, "#111827")

cols = [
    (450,  "改造前", "#FEE2E2", "#B91C1C",
        ["人工逐个看邮件 / 表单", "凭经验分类、经常错派", "答案靠个人记忆、口径不一", "下班后工单无人跟进", "投诉靠打电话挨个催"]),
    (1300, "改造后", "#DCFCE7", "#15803D",
        ["全渠道进线统一接入", "LLM 识别意图/情绪/紧急度", "RAG 检索政策、摘要引用依据", "SLA 矩阵自动定级定责", "飞书卡片 @ 负责人 + 出错告警"]),
    (2150, "业务收益", "#DBEAFE", "#1D4ED8",
        ["响应时长 小时级 → 分钟级", "人工分拣工作量 下降约 80%", "分类准确率 稳定 90% 以上", "P1 工单 30 分钟内触达", "工单数据可沉淀、可分析"]),
]
for cx, title, bg, fg, lines in cols:
    d.rounded_rectangle([cx-280, by0+85, cx+280, by0+300], radius=14, fill=bg)
    ctext(cx, by0+115, title, NODE_T, fg)
    for j, line in enumerate(lines):
        ctext(cx, by0+155+j*28, line, SMALL, "#1F2937")

img.save("assets/workflow-overview.png", "PNG")
print("ok", img.size)
