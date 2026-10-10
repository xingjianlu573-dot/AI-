<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>AI Business Workflow Automation · 在线演示</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, "Segoe UI", "Microsoft YaHei", sans-serif;
    background: #0f172a; color: #e2e8f0; min-height: 100vh; padding: 20px;
  }
  .header { text-align: center; margin-bottom: 20px; }
  .header h1 { font-size: 26px; color: #fff; }
  .header p { color: #94a3b8; font-size: 13px; margin-top: 6px; }
  .badge {
    display: inline-block; background: #7c3aed; color: #fff;
    padding: 2px 10px; border-radius: 10px; font-size: 11px; margin-left: 6px;
  }
  .grid { display: grid; grid-template-columns: 380px 1fr; gap: 20px; max-width: 1500px; margin: 0 auto; }
  .card {
    background: #1e293b; border: 1px solid #334155; border-radius: 14px; padding: 20px;
  }
  .card h2 { font-size: 15px; color: #fff; margin-bottom: 14px; }
  label { display: block; font-size: 12px; color: #94a3b8; margin: 10px 0 4px; }
  input, select, textarea {
    width: 100%; padding: 9px 11px; background: #0f172a; border: 1px solid #334155;
    border-radius: 8px; color: #e2e8f0; font-size: 13px; font-family: inherit; outline: none;
  }
  input:focus, textarea:focus { border-color: #7c3aed; }
  textarea { min-height: 90px; resize: vertical; }
  button {
    width: 100%; padding: 11px; margin-top: 14px; border: 0; border-radius: 8px;
    background: linear-gradient(135deg, #7c3aed, #4f46e5); color: #fff;
    font-size: 14px; font-weight: 600; cursor: pointer;
  }
  button:hover { opacity: .92; }
  button.ghost {
    background: #334155; color: #e2e8f0; font-weight: 400; margin-top: 8px;
  }
  .pipeline { display: flex; flex-direction: column; gap: 10px; }
  .node {
    display: grid; grid-template-columns: 44px 1fr; gap: 12px; align-items: start;
    padding: 12px; border-radius: 10px; background: #0f172a; border: 1px solid #334155;
    opacity: .45; transition: all .3s;
  }
  .node.active { opacity: 1; border-color: #7c3aed; box-shadow: 0 0 0 1px #7c3aed inset; }
  .node.done { opacity: 1; border-color: #059669; }
  .node .icon {
    width: 36px; height: 36px; border-radius: 8px; background: #334155;
    display: flex; align-items: center; justify-content: center; font-size: 16px; color: #fff;
  }
  .node.active .icon { background: #7c3aed; }
  .node.done .icon { background: #059669; }
  .node .title { font-size: 13px; color: #fff; font-weight: 600; }
  .node .meta { font-size: 12px; color: #94a3b8; margin-top: 3px; min-height: 16px; }
  .node.done .meta { color: #86efac; }
  .result { margin-top: 16px; display: none; }
  .ticket {
    background: #fff; color: #0f172a; border-radius: 12px; padding: 18px; margin-bottom: 12px;
  }
  .ticket .row { display: flex; justify-content: space-between; font-size: 12px; color: #64748b; margin-bottom: 8px; }
  .ticket h3 { font-size: 16px; margin-bottom: 8px; }
  .ticket p { font-size: 13px; line-height: 1.6; color: #334155; }
  .chip {
    display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-right: 4px;
  }
  .chip-cat { background: #ede9fe; color: #6d28d9; }
  .chip-low { background: #dbeafe; color: #1d4ed8; }
  .chip-medium { background: #fef3c7; color: #b45309; }
  .chip-high { background: #ffedd5; color: #c2410c; }
  .chip-critical { background: #fee2e2; color: #b91c1c; }
  .chip-p1 { background: #fee2e2; color: #b91c1c; }
  .chip-p2 { background: #ffedd5; color: #c2410c; }
  .chip-p3 { background: #fef3c7; color: #b45309; }
  .chip-p4 { background: #dbeafe; color: #1d4ed8; }
  .kb { background: #fff; border-radius: 10px; overflow: hidden; color: #0f172a; margin-bottom: 12px; }
  .kb .kh { padding: 10px 14px; background: #ede9fe; color: #6d28d9; font-weight: 600; font-size: 13px; }
  .kb .kb2 { padding: 12px 14px; font-size: 12.5px; line-height: 1.7; color: #334155; }
  .feishu { background: #fff; border-radius: 10px; overflow: hidden; color: #0f172a; }
  .feishu .fh { padding: 10px 14px; color: #fff; font-weight: 600; font-size: 13px; }
  .feishu .fb { padding: 12px 14px; font-size: 13px; line-height: 1.7; }
  .fh-red { background: #dc2626; } .fh-orange { background: #ea580c; } .fh-blue { background: #2563eb; }
  .divider { border: 0; border-top: 1px solid #e2e8f0; margin: 8px 0; }
  .spinner {
    display: inline-block; width: 12px; height: 12px; border: 2px solid #7c3aed;
    border-top-color: transparent; border-radius: 50%; animation: spin .8s linear infinite;
    vertical-align: middle; margin-right: 4px;
  }
  @keyframes spin { to { transform: rotate(360deg); } }
  h2.sec { color: #fff; margin: 18px 0 10px; font-size: 14px; }
</style>
</head>
<body>
<div class="header">
  <h1>AI Business Workflow Automation <span class="badge">在线演示</span></h1>
  <p>Webhook → LLM 分析 → 分类 → RAG 知识库检索 → 摘要 → 工单 → SLA 矩阵 → 飞书通知 · 全流程本地模拟</p>
</div>

<div class="grid">
  <div class="card">
    <h2>① 客户进线表单</h2>
    <label>客户姓名</label>
    <input id="f-name" value="王磊">
    <label>公司</label>
    <input id="f-company" value="杭州明远贸易有限公司">
    <label>联系方式</label>
    <input id="f-contact" value="wangl@mingyuan.com">
    <label>来源渠道</label>
    <select id="f-source">
      <option>官网表单</option><option>邮件</option><option>企业微信</option>
      <option>客服电话</option><option>小程序</option>
    </select>
    <label>问题描述</label>
    <textarea id="f-msg">我们生产线今早九点开始系统直接登不进去了，MES 数据同步全断了！车间 80 多个人在等，这是重大事故！！！</textarea>
    <button onclick="run()">提交并生成工单</button>
    <button class="ghost" onclick="loadSample()">🎲 载入一条示例客户</button>
  </div>

  <div class="card">
    <h2>② 自动化流水线（实时）</h2>
    <div class="pipeline" id="pipe">
      <div class="node" data-i="0"><div class="icon">📥</div><div><div class="title">Webhook 接收</div><div class="meta">等待进线…</div></div></div>
      <div class="node" data-i="1"><div class="icon">🧠</div><div><div class="title">LLM 需求分析</div><div class="meta">意图 / 情绪 / 紧急度 · 温度 0.1</div></div></div>
      <div class="node" data-i="2"><div class="icon">🏷️</div><div><div class="title">AI 智能分类</div><div class="meta">7 类业务自动归口 · 温度 0.1</div></div></div>
      <div class="node" data-i="3"><div class="icon">📚</div><div><div class="title">知识库检索（RAG）</div><div class="meta">检索相关政策片段</div></div></div>
      <div class="node" data-i="4"><div class="icon">✍️</div><div><div class="title">自动生成摘要</div><div class="meta">≤60 字 · 引用知识库 · 温度 0.4</div></div></div>
      <div class="node" data-i="5"><div class="icon">🗂️</div><div><div class="title">生成工单记录</div><div class="meta">结构化字段</div></div></div>
      <div class="node" data-i="6"><div class="icon">⏱️</div><div><div class="title">SLA 矩阵（28 组合）</div><div class="meta">分类 × 紧急度 → 时限与责任团队</div></div></div>
      <div class="node" data-i="7"><div class="icon">🗄️</div><div><div class="title">同步飞书 / 数据库</div><div class="meta">写入多维表格（含 SLA 字段）</div></div></div>
      <div class="node" data-i="8"><div class="icon">🔔</div><div><div class="title">通知负责人</div><div class="meta">飞书卡片按紧急度</div></div></div>
    </div>

    <div class="result" id="result">
      <h2 class="sec">知识库检索（RAG）命中</h2>
      <div class="kb" id="kb"></div>
      <h2 class="sec">生成的工单</h2>
      <div class="ticket" id="ticket"></div>
      <h2 class="sec">飞书通知卡片</h2>
      <div class="feishu" id="feishu"></div>
    </div>
  </div>
</div>

<script>
// ====== 内嵌示例客户 ======
const SAMPLES = [
  {name:"王磊",company:"杭州明远贸易",contact:"wangl@mingyuan.com",source:"官网表单",msg:"我们公司有 120 人，想咨询一下你们企业版怎么收费？能不能先开 30 天试用？"},
  {name:"李思颖",company:"上海澄光设计",contact:"13800001111",source:"邮件",msg:"上周四下单的年度会员，发票至今没收到，财务已经催我第三次了，请今天务必处理。"},
  {name:"张建国",company:"广州恒锐制造",contact:"zhangjg@hengrui.cn",source:"客服电话",msg:"我们生产线今早九点开始系统直接登不进去了，MES 数据同步全断了！车间 80 多个人在等，这是重大事故！！！"},
  {name:"刘洋",company:"深圳前海创智",contact:"liuyang@qianhai.ai",source:"官网表单",msg:"我们是做 AI 创业的，看到你们开放平台，想谈一下战略合作和渠道代理，方便约个下周的会吗？"},
  {name:"赵敏",company:"成都悦居民宿",contact:"13900002222",source:"小程序",msg:"App 昨晚更新之后，订单列表一直转圈加载不出来，客人的预订我都看不到，今天就要退房了，很急！"},
  {name:"吴强",company:"武汉长江教育",contact:"wuqiang@cjedu.com",source:"客服电话",msg:"我要投诉！你们销售答应给我一周上门培训，结果合同签完就人间蒸发，这已经是第三个人接我电话了！"},
  {name:"徐军",company:"青岛港口物流",contact:"xujun@qingdao-port.com",source:"邮件",msg:"发票抬头开错了，税号少了一位，已经退回，麻烦重新开一份，财务这周就要归档。"},
  {name:"高宇",company:"沈阳北方重工",contact:"gaoyu@bfzg.com",source:"客服电话",msg:"我们买的私有化部署版，今早后台报 502，运维已经重启过容器还是不行，远程协助请马上安排。"},
  {name:"邓超",company:"石家庄燕赵医药",contact:"13600004444",source:"客服电话",msg:"合同写的是 7×24 支持，昨晚出问题打了三小时电话没人接！这种服务态度我要发函投诉到你们总部。"},
  {name:"宋雨",company:"宁波舟山港供应链",contact:"songyu@zs-port.com",source:"邮件",msg:"你好，我们集团 IT 部想集中采购，年预算大概 80 万，能否给个大客户折扣方案？"},
];

// ====== 模拟知识库（对应 simulation/knowledge-base.md）======
const KB = [
  {tags:["收费","企业版","价格","费用","多少钱"], content:"企业版按席位年付，50 人起订，基础版 ¥199/席/年，专业版 ¥399/席/年，企业版需商务报价。"},
  {tags:["试用","30 天"], content:"专业版支持 30 天免费试用，企业版可申请 14 天 POC 环境。"},
  {tags:["发票","开票"], content:"对公转账到账后 3 个工作日内开具电子发票，可在控制台自助申请。"},
  {tags:["发票","抬头","税号","重开"], content:"发票抬头/税号错误可发起红冲重开，或联系财务部（billing@yunqi.com），1 个工作日内处理。"},
  {tags:["登录","登不","打不开"], content:"登录失败请先检查浏览器缓存与网络；连续失败请联系技术支持，紧急故障 30 分钟内响应。"},
  {tags:["502","500","故障","宕机"], content:"平台故障会在状态页公告，SLA 赔付按合同执行；私有化部署版优先远程协助。"},
  {tags:["退款","退订","取消"], content:"未使用满 30 天的年付订单支持按剩余时长退款；已开发票需先红冲。"},
  {tags:["数据","存储","region","节点"], content:"中国大陆节点默认华东（上海）；跨境业务可配置海外节点，满足数据出境合规要求。"},
  {tags:["等保","合规","安全"], content:"产品通过等保三级测评，支持签署 DPA（数据处理协议）。"},
  {tags:["合作","代理","渠道"], content:"联系商务团队（bd@yunqi.com）提交合作资料，审核通过后按阶梯返佣。"},
  {tags:["折扣","采购","预算"], content:"集团集中采购可申请大客户折扣方案，具体联系商务团队报价。"},
  {tags:["投诉","SLA","响应"], content:"P1（30 分钟响应）：投诉+高/紧急、技术支持+紧急、任何 critical 工单；P2 1~2h；P3 4~8h；P4 24h。"},
];

function searchKB(msg, topK = 3) {
  const hits = KB.map(item => {
    const score = item.tags.filter(t => msg.includes(t)).length;
    return { item, score };
  }).filter(h => h.score > 0).sort((a, b) => b.score - a.score).slice(0, topK);
  return hits.map(h => h.item.content);
}

// ====== 本地规则模拟 AI ======
function analyze(msg) {
  const m = msg;
  let category = "other", catLabel = "其他";
  if (/投诉|曝光|差评|说法|发函|人间蒸发|服务态度/.test(m)) { category="complaint"; catLabel="投诉"; }
  else if (/合作|代理|渠道|战略合作|联合案例/.test(m)) { category="partnership"; catLabel="商务合作"; }
  else if (/发票|账单|扣款|报销|付款|多扣|退款|退钱|退订|取消.*会员/.test(m)) { category="billing"; catLabel="账单/付款"; }
  else if (/登不进|登录不|打不开|报错|崩溃|502|500|宕机|故障|转圈|加载不出来|重启|推送|bug/.test(m)) { category="tech_support"; catLabel="技术支持"; }
  else if (/退款|退货|退换|取消订单|改套餐/.test(m)) { category="after_sales"; catLabel="售后/退换"; }
  else if (/价格|收费|多少钱|试用|采购|报价|预算|席位|企业版|个人版|团队版|对比|迁移|折扣/.test(m)) { category="sales_inquiry"; catLabel="售前咨询"; }
  let urgency = "low", urgLabel = "低";
  if (/重大事故|马上|立刻|紧急|宕机|全断|全停|车间|生产线|三小时|80 多人|今天必须|今天就要/.test(m)) { urgency="critical"; urgLabel="紧急"; }
  else if (/今天|今天就要|今天务必|这周|财务.*催|很急|催我/.test(m)) { urgency="high"; urgLabel="高"; }
  else if (/下周|方便约|想了解|咨询一下/.test(m)) { urgency="low"; urgLabel="低"; }
  else { urgency="medium"; urgLabel="中"; }
  let sentiment = "neutral", sentLabel = "中性";
  const exclaim = (m.match(/!/g)||[]).length;
  if (/投诉|曝光|发函|人间蒸发|服务态度|重大/.test(m) || exclaim>=3) { sentiment="angry"; sentLabel="愤怒"; }
  else if (/急|催|今天务必|今天必须|今天就要/.test(m)) { sentiment="negative"; sentLabel="负面"; }
  else if (/用得很好|顺手|谢谢|不错/.test(m)) { sentiment="positive"; sentLabel="正面"; }
  const intent = m.length > 40 ? m.slice(0,40)+"…" : m;
  const summary = `客户${intent}（${catLabel}·${urgLabel}紧急·${sentLabel}情绪）`;
  return { category, catLabel, urgency, urgLabel, sentiment, sentLabel, intent, summary };
}

// ====== SLA 矩阵（与 n8n workflow 的 JS 一致）======
function sla(category, urgency) {
  const SLAs = {
    sales_inquiry:{level:'P4',time:'24h', team:'销售部'},
    after_sales:  {level:'P3',time:'8h',  team:'售后部'},
    tech_support: {level:'P3',time:'4h',  team:'技术支持'},
    billing:      {level:'P3',time:'4h',  team:'财务部'},
    partnership:  {level:'P4',time:'24h', team:'商务部'},
    complaint:    {level:'P2',time:'2h',  team:'客户成功'},
    other:        {level:'P4',time:'24h', team:'客服中心'},
  };
  const U = { low:0, medium:1, high:2, critical:3 };
  const urgent = { high:{level:'P2',time:'1h'}, critical:{level:'P1',time:'30min'} };
  const base = SLAs[category] || SLAs.other;
  let s = Object.assign({}, base);
  if (U[urgency] >= 2) s = Object.assign({}, base, urgent[urgency]);
  if (category === 'complaint' && U[urgency] >= 2) s = {level:'P1', time:'30min', team:'客户成功+主管'};
  if (category === 'tech_support' && urgency === 'critical') s = {level:'P1', time:'30min', team:'技术支持+主管'};
  return s;
}

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function run() {
  const name = document.getElementById('f-name').value.trim();
  const company = document.getElementById('f-company').value.trim();
  const contact = document.getElementById('f-contact').value.trim();
  const source = document.getElementById('f-source').value;
  const msg = document.getElementById('f-msg').value.trim();
  if (!name || !msg) { alert('请填写客户姓名和问题描述'); return; }

  document.querySelectorAll('.node').forEach(n => n.className='node');
  document.getElementById('result').style.display = 'none';

  const nodes = document.querySelectorAll('.node');
  const a = analyze(msg);
  const kbHits = searchKB(msg);
  const s = sla(a.category, a.urgency);
  const ticketId = 'TK-' + new Date().toISOString().slice(0,10).replace(/-/g,'') + '-' + Math.floor(Math.random()*9000+1000);

  setNode(0, 'active', '<span class="spinner"></span>接收中…');
  await sleep(450);
  setNode(0, 'done', `✓ 已收到来自 ${source} 的进线`);

  setNode(1, 'active', '<span class="spinner"></span>理解客户意图…');
  await sleep(850);
  setNode(1, 'done', `意图：${a.intent} · 情绪：${a.sentLabel} · 紧急度：${a.urgLabel}`);

  setNode(2, 'active', '<span class="spinner"></span>归类业务线…');
  await sleep(650);
  setNode(2, 'done', `✓ 归入「${a.catLabel}」（${a.category}）`);

  setNode(3, 'active', '<span class="spinner"></span>检索知识库…');
  await sleep(700);
  setNode(3, 'done', kbHits.length ? `✓ 命中 ${kbHits.length} 条相关政策片段` : '✓ 无精确命中（摘要将不引用知识库）');

  setNode(4, 'active', '<span class="spinner"></span>生成摘要…');
  await sleep(600);
  setNode(4, 'done', `✓ ${a.summary}`);

  setNode(5, 'active', '<span class="spinner"></span>生成工单…');
  await sleep(450);
  setNode(5, 'done', `✓ 工单号 ${ticketId}，字段已结构化`);

  setNode(6, 'active', '<span class="spinner"></span>计算 SLA…');
  await sleep(500);
  setNode(6, 'done', `✓ ${s.level} · ${s.time} 内响应 · 责任团队：${s.team}`);

  setNode(7, 'active', '<span class="spinner"></span>写入飞书多维表格…');
  await sleep(550);
  setNode(7, 'done', '✓ 多维表格新增一行（含 SLA 字段）');

  setNode(8, 'active', '<span class="spinner"></span>推送飞书卡片…');
  await sleep(450);
  setNode(8, 'done', `✓ 已 @ 责任团队（${a.urgLabel==='紧急'?'红色卡片':a.urgLabel==='高'?'橙色卡片':'蓝色卡片'}）`);

  renderResult({ticketId, name, company, contact, source, msg, ...a, kbHits, sla:s});
}

function setNode(i, state, meta) {
  const n = document.querySelectorAll('.node')[i];
  n.className = 'node ' + state;
  n.querySelector('.meta').innerHTML = meta;
}

function renderResult(d) {
  const urgClass = {low:'chip-low', medium:'chip-medium', high:'chip-high', critical:'chip-critical'}[d.urgency];
  const pClass = {P1:'chip-p1', P2:'chip-p2', P3:'chip-p3', P4:'chip-p4'}[d.sla.level];

  document.getElementById('kb').innerHTML = d.kbHits.length ? `
    <div class="kh">📚 RAG 检索 · 命中 ${d.kbHits.length} 条</div>
    <div class="kb2">${d.kbHits.map(h => '• ' + h).join('<br>')}</div>
  ` : `
    <div class="kh">📚 RAG 检索 · 未命中</div>
    <div class="kb2">未检索到相关政策片段，摘要未引用知识库（不影响主流程）。</div>
  `;

  document.getElementById('ticket').innerHTML = `
    <div class="row"><span>工单 ${d.ticketId}</span><span>${new Date().toLocaleString('zh-CN')}</span></div>
    <h3>${d.company || d.name}</h3>
    <div>
      <span class="chip chip-cat">${d.catLabel}</span>
      <span class="chip ${urgClass}">${d.urgLabel}紧急</span>
      <span class="chip chip-low">${d.sentLabel}情绪</span>
      <span class="chip ${pClass}">SLA ${d.sla.level}</span>
      <span class="chip chip-p4">${d.sla.time} 响应</span>
    </div>
    <hr class="divider">
    <p><b>联系方式：</b>${d.contact}<br>
       <b>来源：</b>${d.source}<br>
       <b>客户原话：</b>${d.msg}<br>
       <b>AI 摘要：</b>${d.summary}<br>
       <b>SLA：</b>${d.sla.level} · ${d.sla.time} 内响应 · 责任团队 ${d.sla.team}</p>
  `;
  const headerCls = d.urgency==='critical' ? 'fh-red' : d.urgency==='high' ? 'fh-orange' : 'fh-blue';
  const icon = d.urgency==='critical' ? '🚨' : d.urgency==='high' ? '⚠️' : '📬';
  document.getElementById('feishu').innerHTML = `
    <div class="fh ${headerCls}">${icon} 新客户工单 ${d.ticketId} [${d.sla.level}]</div>
    <div class="fb">
      <b>分类：</b>${d.catLabel}　<b>紧急度：</b>${d.urgLabel}　<b>情绪：</b>${d.sentLabel}<br>
      <b>客户：</b>${d.name}（${d.contact}）<br>
      <b>公司：</b>${d.company}<br>
      <hr class="divider">
      <b>AI 摘要：</b>${d.summary}<br>
      <hr class="divider">
      <b>SLA：</b>${d.sla.level} · ${d.sla.time} 内响应 · 责任团队：${d.sla.team}<br>
      <hr class="divider">
      <span style="color:#94a3b8;font-size:12px">来源：${d.source} · 已同步至飞书多维表格（含 SLA 字段）</span>
    </div>
  `;
  document.getElementById('result').style.display = 'block';
}

function loadSample() {
  const s = SAMPLES[Math.floor(Math.random()*SAMPLES.length)];
  document.getElementById('f-name').value = s.name;
  document.getElementById('f-company').value = s.company;
  document.getElementById('f-contact').value = s.contact;
  document.getElementById('f-source').value = s.source;
  document.getElementById('f-msg').value = s.msg;
}
</script>
</body>
</html>
