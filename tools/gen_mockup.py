# -*- coding: utf-8 -*-
from __future__ import annotations
import json, html

# ---- data: slice ก.ค.–ธ.ค. 2563 ----
research = json.load(open('/Users/cudo/Desktop/Artivism/research-data.json'))
politics = [e for e in research['result']['results'][0]['key_events']]

culture_raw = json.load(open('/Users/cudo/Desktop/Artivism/culture-curated.json'))['items']
CULT_DATES = {
    'วิ่งกันนะแฮมทาโร่': '2020-07-26',
    'ปฏิรูป — Rap Against Dictatorship': '2020-11-13',
    'School Town King': '2020-12-17',
    'ปรากฏการณ์สะท้านฟ้า': '2020-09-15',
    'เป็ดยางเหลือง': '2020-11-17',
    'นิทรรศการ "แขวน"': '2020-10-01',
    'PrachathipaType': '2020-09-19',
    'คืนกราฟฟิตี้ราชประสงค์': '2020-11-18',
}
culture = []
for it in culture_raw:
    if it['period_tag'] != '1-2563': continue
    d = it.get('date_exact') if it.get('date_exact') and it.get('date_exact') != 'unknown' else None
    if not d:
        for kw, dd in CULT_DATES.items():
            if kw in it['title']: d = dd; break
    if d and d >= '2020-07-01':
        culture.append({'date': d, 'name': it['title'], 'desc': it['story'], 'cat': it['cat']})

fa = []
for line in open('/Users/cudo/Desktop/Artivism/freearts-events.txt'):
    p = [x.strip() for x in line.split('|')]
    if '2020-07-01' <= p[0] <= '2020-12-31':
        fa.append({'date': p[0], 'name': p[2], 'hero': p[4] == 'tier:hero'})

def esc(s): return html.escape(s or '')

def js_items(items, kind):
    out = []
    for it in items:
        crack = kind == 'pol' and any(k in it['name'] for k in ['สลาย', 'จับกุม', 'ฉุกเฉิน'])
        out.append({
            'd': it['date'], 'n': it['name'],
            'desc': (it.get('desc') or it.get('description') or '')[:260],
            'crowd': it.get('crowd_estimate', ''),
            'hero': it.get('hero', False), 'crack': crack,
        })
    return out

data = {
    'pol': js_items(politics, 'pol'),
    'cul': js_items(culture, 'cul'),
    'fa': js_items(fa, 'fa'),
}

page = """<!DOCTYPE html>
<html lang="th"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Timeline Mockup — 3 เส้นเรื่อง (ช่วงที่ 1: ก.ค.–ธ.ค. 2563)</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
:root { --bg:#0c0c0c; --fg:rgba(242,240,235,.88); --dim:rgba(242,240,235,.5); --faint:rgba(242,240,235,.25);
  --pol:#cfcbc2; --cul:#e8b34c; --fa:#e8452c; --line:rgba(242,240,235,.1); }
body { background:var(--bg); color:var(--fg); font-family:'Sukhumvit Set','Noto Sans Thai',sans-serif;
  font-weight:300; overflow-x:hidden; }
header { padding:26px 4vw 14px; display:flex; align-items:baseline; gap:1rem; flex-wrap:wrap; }
h1 { font-size:clamp(17px,2vw,24px); font-weight:600; }
.sub { color:var(--dim); font-size:13px; }
.legend { display:flex; gap:1.2rem; margin-left:auto; font-size:12.5px; color:var(--dim); align-items:center; }
.legend .k { display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:6px; vertical-align:-1px; }
.zoom { padding:0 4vw 10px; display:flex; gap:8px; }
.zoom button { background:none; border:1px solid var(--line); color:var(--dim); border-radius:8px;
  padding:4px 14px; font-family:inherit; font-size:13px; cursor:pointer; }
.zoom button.on { color:var(--fg); border-color:var(--dim); }

#viewport { overflow-x:auto; overflow-y:hidden; cursor:grab; border-top:1px solid var(--line); }
#viewport.drag { cursor:grabbing; }
#world { position:relative; height:660px; }

.mgrid { position:absolute; top:0; bottom:0; border-left:1px solid rgba(242,240,235,.07); }
.mlabel { position:absolute; top:8px; font-size:12px; color:var(--dim); padding-left:8px; letter-spacing:.08em; }

.lane { position:absolute; left:0; right:0; }
.lane .base { position:absolute; left:0; right:0; height:1px; background:var(--line); }
.lane-label { position:sticky; }
.lanetag { position:fixed; left:14px; z-index:30; font-size:11.5px; letter-spacing:.14em; color:var(--dim);
  background:rgba(12,12,12,.85); padding:3px 10px; border-radius:999px; border:1px solid var(--line); }

.ev { position:absolute; z-index:5; }
.ev .dot { width:8px; height:8px; border-radius:50%; position:absolute; left:-4px; }
.ev.crack .dot { width:0; height:0; border-radius:0; border-left:6px solid transparent; border-right:6px solid transparent;
  border-top:9px solid #b3543f; left:-6px; }
.ev .lbl { position:absolute; white-space:nowrap; font-size:11.5px; color:var(--dim); left:6px; top:-6px;
  max-width:220px; overflow:hidden; text-overflow:ellipsis; }
.ev .tick { position:absolute; width:1px; background:rgba(242,240,235,.14); left:0; }
.ev:hover .lbl { color:var(--fg); z-index:40; }
.ev.hero .dot { width:15px; height:15px; left:-7.5px; box-shadow:0 0 14px rgba(232,69,44,.55); }
.ev.hero .lbl { font-size:13px; font-weight:600; color:var(--fg); }

#tip { position:fixed; display:none; z-index:100; max-width:340px; background:#1a1a18; border:1px solid rgba(242,240,235,.2);
  border-radius:10px; padding:12px 15px; font-size:12.5px; line-height:1.6; color:var(--dim); pointer-events:none; }
#tip b { color:var(--fg); display:block; margin-bottom:3px; font-size:13px; }
#tip .dt { color:var(--faint); font-size:11px; }
#tip .crowd { color:var(--cul); font-size:11.5px; margin-top:4px; }
#guide { position:absolute; top:0; bottom:0; width:1px; background:rgba(232,179,76,.35); display:none; z-index:2; }
.note { padding:14px 4vw 40px; color:var(--faint); font-size:12.5px; line-height:1.8; }
</style></head><body>
<header>
  <h1>Timeline Mockup — 3 เส้นเรื่อง</h1>
  <span class="sub">ช่วงที่ 1 · ก.ค.–ธ.ค. 2563 · scale เวลาจริง (ช่องว่าง = ความเงียบจริง)</span>
  <div class="legend">
    <span><span class="k" style="background:var(--pol)"></span>การเมือง</span>
    <span><span class="k" style="background:var(--cul)"></span>วัฒนธรรม</span>
    <span><span class="k" style="background:var(--fa)"></span>Free Arts</span>
    <span>▼ = สลายชุมนุม/จับกุม</span>
  </div>
</header>
<div class="zoom">ซูม:
  <button data-z="6">แน่น</button><button data-z="11" class="on">กลาง</button><button data-z="18">ขยาย</button>
  <span class="sub" style="align-self:center; margin-left:8px">ลากเพื่อเลื่อน · ชี้จุดเพื่อดูรายละเอียด+เส้นเทียบเวลา</span>
</div>
<div id="viewport"><div id="world"><div id="guide"></div></div></div>
<div id="tip"></div>
<div class="note">
หมายเหตุ mockup: ① ใช้เวลาจริง — ความถี่/ช่องว่างคือข้อมูล ② งานวัฒนธรรม 3 ชิ้นของช่วงนี้ยังวางไม่ได้เพราะไม่มีวันที่ (ขุนศึกฯ, Royalist Marketplace, เลเซอร์ตามหาความจริง — ต้องตัดสินใจตอนทำเต็ม) ③ ถ้ารูปแบบนี้เวิร์ค เวอร์ชันเต็มจะเพิ่ม: แถบ 6 ช่วงพื้นหลัง + ครอบคลุม 2557–2569 + ลิงก์คลิกได้
</div>
<script>
const DATA = __DATA__;
const T0 = new Date('2020-06-28').getTime(), T1 = new Date('2021-01-04').getTime();
const DAY = 86400000;
const LANES = [
  { key:'pol', label:'การเมือง', color:'var(--pol)', top:60,  height:200 },
  { key:'cul', label:'วัฒนธรรม', color:'var(--cul)', top:280, height:170 },
  { key:'fa',  label:'FREE ARTS', color:'var(--fa)',  top:470, height:180 },
];
const MONTHS = [['2020-07-01','ก.ค. 63'],['2020-08-01','ส.ค.'],['2020-09-01','ก.ย.'],['2020-10-01','ต.ค.'],['2020-11-01','พ.ย.'],['2020-12-01','ธ.ค.'],['2021-01-01','']];
let pxday = 11;
const world = document.getElementById('world');
const vp = document.getElementById('viewport');
const tip = document.getElementById('tip');
const guide = document.getElementById('guide');

function x(dstr) { return (new Date(dstr).getTime() - T0) / DAY * pxday + 40; }
function thd(dstr) { const d = new Date(dstr);
  const m = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
  return d.getDate() + ' ' + m[d.getMonth()] + ' ' + (d.getFullYear() + 543 - 2500); }

function render() {
  world.querySelectorAll('.mgrid,.mlabel,.lane,.ev').forEach(e => e.remove());
  world.style.width = ((T1 - T0) / DAY * pxday + 120) + 'px';
  MONTHS.forEach(([d, l]) => {
    const g = document.createElement('div'); g.className = 'mgrid'; g.style.left = x(d) + 'px'; world.appendChild(g);
    if (l) { const t = document.createElement('div'); t.className = 'mlabel'; t.style.left = x(d) + 'px'; t.textContent = l; world.appendChild(t); }
  });
  LANES.forEach(L => {
    const lane = document.createElement('div'); lane.className = 'lane';
    lane.style.top = L.top + 'px'; lane.style.height = L.height + 'px';
    const base = document.createElement('div'); base.className = 'base'; base.style.top = (L.height / 2) + 'px';
    lane.appendChild(base); world.appendChild(lane);

    // stagger rows: sort by date, assign row avoiding label overlap
    const items = [...DATA[L.key]].sort((a, b) => a.d.localeCompare(b.d));
    const rows = []; // last label end px per row
    items.forEach(it => {
      const px = x(it.d);
      const w = Math.min(it.n.length * 6.2, 225) + 14;
      let r = 0;
      while (rows[r] !== undefined && rows[r] > px) r++;
      rows[r] = px + w;
      it._row = r;
    });
    const mid = L.height / 2;
    items.forEach(it => {
      const ev = document.createElement('div');
      ev.className = 'ev' + (it.hero ? ' hero' : '') + (it.crack ? ' crack' : '');
      const up = it._row % 2 === 0;
      const off = Math.floor(it._row / 2 + (up ? 0 : 1)) * 26 + (it.hero ? 10 : 14);
      const yy = up ? mid - off : mid + off;
      ev.style.left = x(it.d) + 'px'; ev.style.top = (L.top + yy) + 'px';
      const dot = document.createElement('div'); dot.className = 'dot';
      if (!it.crack) dot.style.background = L.color;
      dot.style.top = it.hero ? '-7.5px' : '-4px';
      const tick = document.createElement('div'); tick.className = 'tick';
      tick.style.top = up ? '0px' : (mid - yy) + 'px';
      tick.style.height = Math.abs(mid - yy) + 'px';
      if (up) { tick.style.top = '0'; tick.style.height = (mid - yy) + 'px'; }
      else { tick.style.top = (mid - yy) + 'px'; tick.style.height = (yy - mid) + 'px'; }
      const lbl = document.createElement('div'); lbl.className = 'lbl'; lbl.textContent = it.n;
      ev.appendChild(tick); ev.appendChild(dot); ev.appendChild(lbl);
      ev.addEventListener('mousemove', e => {
        tip.style.display = 'block';
        tip.innerHTML = '<b>' + it.n + '</b><span class="dt">' + thd(it.d) + '</span>' +
          (it.desc ? '<div>' + it.desc + '…</div>' : '') +
          (it.crowd ? '<div class="crowd">👥 ' + it.crowd + '</div>' : '');
        tip.style.left = Math.min(e.clientX + 16, innerWidth - 360) + 'px';
        tip.style.top = Math.min(e.clientY + 14, innerHeight - 180) + 'px';
        guide.style.display = 'block'; guide.style.left = x(it.d) + 'px';
      });
      ev.addEventListener('mouseleave', () => { tip.style.display = 'none'; guide.style.display = 'none'; });
      world.appendChild(ev);
    });
  });
}
render();

// lane tags fixed at left
LANES.forEach(L => {
  const t = document.createElement('div'); t.className = 'lanetag';
  t.textContent = L.label; t.style.color = L.color;
  document.body.appendChild(t);
  const place = () => { const r = vp.getBoundingClientRect(); t.style.top = (r.top + L.top + 6) + 'px'; };
  place(); addEventListener('resize', place); addEventListener('scroll', place);
});

// zoom
document.querySelectorAll('.zoom button').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.zoom button').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); pxday = +b.dataset.z; render();
}));
// drag scroll
let drag = null;
vp.addEventListener('mousedown', e => { drag = { x: e.clientX, s: vp.scrollLeft }; vp.classList.add('drag'); });
addEventListener('mousemove', e => { if (drag) vp.scrollLeft = drag.s - (e.clientX - drag.x); });
addEventListener('mouseup', () => { drag = null; vp.classList.remove('drag'); });
vp.addEventListener('wheel', e => { if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) { vp.scrollLeft += e.deltaY; e.preventDefault(); } }, { passive: false });
</script></body></html>"""

page = page.replace('__DATA__', json.dumps(data, ensure_ascii=False))
open('/Users/cudo/Desktop/Artivism/timeline-mockup.html', 'w').write(page)
print(f"pol:{len(data['pol'])} cul:{len(data['cul'])} fa:{len(data['fa'])}")
