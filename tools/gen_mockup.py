# -*- coding: utf-8 -*-
from __future__ import annotations
import json, html, os

research = json.load(open('/Users/cudo/Desktop/Artivism/research-data.json'))
_res = research['result']['results']
politics = (_res[0]['key_events'] + _res[1]['key_events'] + _res[2]['key_events'] + _res[3]['key_events']
            + _res[4]['key_events'] + _res[5]['key_events'])

culture_raw = json.load(open('/Users/cudo/Desktop/Artivism/culture-curated.json'))['items']
CULT_DATES = {
    'วิ่งกันนะแฮมทาโร่': '2020-07-26', 'ปฏิรูป — Rap Against Dictatorship': '2020-11-13',
    'School Town King': '2020-12-17', 'ปรากฏการณ์สะท้านฟ้า': '2020-09-15',
    'เป็ดยางเหลือง': '2020-11-17', 'นิทรรศการ "แขวน"': '2020-10-01',
    'PrachathipaType': '2020-09-19', 'คืนกราฟฟิตี้ราชประสงค์': '2020-11-18',
}
culture = []
for it in culture_raw:
    if it['period_tag'] not in ('1-2563', '2-2564', '3-2565', '4-2566', '5-2567', '5-2567-กลาง68', '6-มิย68-กพ69'): continue
    d = it.get('date_exact') if it.get('date_exact') and it.get('date_exact') != 'unknown' else None
    if not d:
        for kw, dd in CULT_DATES.items():
            if kw in it['title']: d = dd; break
    if d and d >= '2020-07-01':
        culture.append({'date': d, 'name': it['title'], 'short': it.get('short'), 'hero': it.get('hero', False), 'desc': it['story']})

IMG_DIR = '/Users/cudo/Desktop/Artivism/site/tl-img'
import subprocess
def img_ar(path):
    r = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path], capture_output=True, text=True)
    vals = [int(l.split(': ')[1]) for l in r.stdout.strip().split('\n')[1:]]
    return round(vals[0] / vals[1], 3)
fa = []
for line in open('/Users/cudo/Desktop/Artivism/freearts-events.txt'):
    p = [x.strip() for x in line.split('|')]
    if '2020-07-01' <= p[0] <= '2026-02-28':
        eid = p[1]
        fp = f'{IMG_DIR}/{eid}.jpg'
        img = f'tl-img/{eid}.jpg' if os.path.exists(fp) else None
        hero = p[4] == 'tier:hero'
        fa.append({'date': p[0], 'name': p[2], 'hero': hero, 'img': img,
                   'ar': img_ar(fp) if img else 1.0})  # ไม่มีรูป → placeholder จัตุรัส 1:1

def items(lst, kind):
    out = []
    for it in lst:
        out.append({'d': it['date'], 'n': it.get('short') or it['name'], 'm': it.get('mid'), 'full': it['name'],
                    'desc': (it.get('desc') or it.get('description') or '')[:260],
                    'crowd': it.get('crowd_estimate', ''),
                    'hero': it.get('hero', False), 'img': it.get('img'), 'ar': it.get('ar', 1.6)})
    return out

data = {'pol': items(politics, 'pol'), 'cul': items(culture, 'cul'), 'fa': items(fa, 'fa')}

page = """<!DOCTYPE html>
<html lang="th"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Timeline Mockup v3 — 3 เส้นเรื่อง</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
:root { --bg:#0c0c0c; --fg:rgba(242,240,235,.88); --dim:rgba(242,240,235,.5); --faint:rgba(242,240,235,.25);
  --pol:#cfcbc2; --cul:#e8b34c; --fa:#e8452c; --line:rgba(242,240,235,.1); }
body { background:var(--bg); color:var(--fg); font-family:'Sukhumvit Set','Noto Sans Thai',sans-serif;
  font-weight:300; overflow-x:hidden; }
header { padding:22px 4vw 10px; display:flex; align-items:baseline; gap:1rem; flex-wrap:wrap; }
h1 { font-size:clamp(16px,1.9vw,22px); font-weight:600; }
.sub { color:var(--dim); font-size:13px; }
.legend { display:flex; gap:1.1rem; margin-left:auto; font-size:12.5px; color:var(--dim); align-items:center; }
.legend .k { display:inline-block; width:9px; height:9px; border-radius:50%; margin-right:6px; vertical-align:-1px; }
.zoom { padding:0 4vw 8px; display:flex; gap:8px; font-size:13px; color:var(--dim); }
.zoom button { background:none; border:1px solid var(--line); color:var(--dim); border-radius:8px;
  padding:3px 13px; font-family:inherit; font-size:13px; cursor:pointer; }
.zoom button.on { color:var(--fg); border-color:var(--dim); }
#viewport { overflow-x:auto; overflow-y:hidden; cursor:grab; border-top:1px solid var(--line); }
#viewport.drag { cursor:grabbing; }
#world { position:relative; height:850px; }
.mgrid { position:absolute; top:0; bottom:0; border-left:1px solid rgba(242,240,235,.07); }
.mlabel { position:absolute; top:6px; font-size:12px; color:var(--dim); padding-left:8px; letter-spacing:.08em; }
.lane-sep { position:absolute; left:0; right:0; height:1px; background:rgba(242,240,235,.06); }
.base { position:absolute; left:0; right:0; height:1px; background:var(--line); }
.lanetag { position:fixed; left:14px; z-index:30; font-size:11px; letter-spacing:.14em; color:var(--dim);
  background:rgba(12,12,12,.85); padding:3px 10px; border-radius:999px; border:1px solid var(--line); }

.ev { position:absolute; z-index:5; }
.ev .dot { width:7px; height:7px; border-radius:50%; position:absolute; left:-3.5px; top:-3.5px; }
.ev .lbl { position:absolute; white-space:nowrap; font-size:11px; color:var(--dim); left:6px; top:-7px; }
.ev .tick { position:absolute; width:1px; background:rgba(242,240,235,.13); left:0; }
.ev:hover .lbl { color:var(--fg); z-index:40; }
.ev.big .dot { width:11px; height:11px; left:-5.5px; top:-5.5px; }
.ev.big .lbl { font-size:13.5px; font-weight:600; color:rgba(242,240,235,.92); top:-9px; }

.card { position:absolute; z-index:6; }
.card .tick { position:absolute; width:1px; background:rgba(232,69,44,.3); left:0; }
.card .dotb { position:absolute; width:9px; height:9px; border-radius:50%; background:var(--fa); left:-4.5px; }
.card.hero .dotb { width:14px; height:14px; left:-7px; box-shadow:0 0 12px rgba(232,69,44,.5); }
.card .box { position:absolute; left:-2px; }
.card img, .card .ph { display:block; border-radius:6px; object-fit:cover; border:1px solid rgba(232,69,44,.35);
  background:#1a1210; }
.card img { object-fit:cover; }
.card.hero img { object-fit:contain; border-width:2px; box-shadow:0 4px 22px rgba(232,69,44,.25); }
.card .ph { width:100px; height:70px; display:flex; align-items:center; justify-content:center;
  color:rgba(232,69,44,.5); font-size:10px; }
.card .cap { font-size:10.5px; color:var(--dim); line-height:1.35; width:100px; margin-top:4px;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.card.hero .cap { font-size:15px; font-weight:700; color:#fff; width:auto; max-width:280px; margin-top:8px; }
.card:hover img { border-color:var(--fa); }
.card:hover .cap { color:var(--fg); }

#tip { position:fixed; display:none; z-index:100; max-width:340px; background:#1a1a18; border:1px solid rgba(242,240,235,.2);
  border-radius:10px; padding:12px 15px; font-size:12.5px; line-height:1.6; color:var(--dim); pointer-events:none; }
#tip b { color:var(--fg); display:block; margin-bottom:3px; font-size:13px; }
#tip .dt { color:var(--faint); font-size:11px; }
#tip .crowd { color:var(--cul); font-size:11.5px; margin-top:4px; }
#guide { position:absolute; top:0; bottom:0; width:1px; background:rgba(232,179,76,.35); display:none; z-index:2; }
.pband { position:absolute; top:0; bottom:0; z-index:0; pointer-events:none; }
.pband .pname { position:absolute; top:26px; left:14px; font-size:11px; letter-spacing:.16em; white-space:nowrap; font-weight:600; }
.pband .pbar { position:absolute; top:0; left:0; right:0; height:2px; opacity:.4; }
</style></head><body>
<header>
  <h1>Timeline Mockup v3 — 3 เส้นเรื่อง</h1>
</header>
<div class="zoom"><span style="align-self:center">ลากเพื่อเลื่อน · ชี้เพื่อดูรายละเอียด</span></div>
<div id="viewport"><div id="world"><div id="guide"></div></div></div>
<div id="tip"></div>
<script>
const DATA = __DATA__;
const T0 = new Date('2020-06-26').getTime(), T1 = new Date('2027-03-08').getTime();  // ต่ออนาคตโล่งๆ 1 ปีหลัง Voter Concert
const DAY = 86400000;
// lanes: pol 25% / fa 60% / cul 15% of 760 usable (top 40 for month labels)
const POL = { top:40,  h:122 };            // 15%
const FA  = { top:162, h:607 };            // 75% — สเกลการ์ดคงเดิม (ล็อกแล้ว)
const CUL = { top:769, h:81 };             // 10%
const HERO_LINE = FA.top + 296;            // กึ่งกลาง: อากาศบน-ล่าง ~52px เท่ากัน
const GAP = 12;                            // ช่องว่างมาตรฐานทุกจุด
const MONTHS = [['2020-07-01','ก.ค. 63'],['2020-08-01','ส.ค.'],['2020-09-01','ก.ย.'],['2020-10-01','ต.ค.'],['2020-11-01','พ.ย.'],['2020-12-01','ธ.ค.'],
  ['2021-01-01','ม.ค. 64'],['2021-02-01','ก.พ.'],['2021-03-01','มี.ค.'],['2021-04-01','เม.ย.'],['2021-05-01','พ.ค.'],['2021-06-01','มิ.ย.'],
  ['2021-07-01','ก.ค.'],['2021-08-01','ส.ค.'],['2021-09-01','ก.ย.'],['2021-10-01','ต.ค.'],['2021-11-01','พ.ย.'],['2021-12-01','ธ.ค.'],
  ['2022-01-01','ม.ค. 65'],['2022-02-01','ก.พ.'],['2022-03-01','มี.ค.'],['2022-04-01','เม.ย.'],['2022-05-01','พ.ค.'],['2022-06-01','มิ.ย.'],
  ['2022-07-01','ก.ค.'],['2022-08-01','ส.ค.'],['2022-09-01','ก.ย.'],['2022-10-01','ต.ค.'],['2022-11-01','พ.ย.'],['2022-12-01','ธ.ค.'],
  ['2023-01-01','ม.ค. 66'],['2023-02-01','ก.พ.'],['2023-03-01','มี.ค.'],['2023-04-01','เม.ย.'],['2023-05-01','พ.ค.'],['2023-06-01','มิ.ย.'],
  ['2023-07-01','ก.ค.'],['2023-08-01','ส.ค.'],['2023-09-01','ก.ย.'],['2023-10-01','ต.ค.'],['2023-11-01','พ.ย.'],['2023-12-01','ธ.ค.'],
  ['2024-01-01','ม.ค. 67'],['2024-02-01','ก.พ.'],['2024-03-01','มี.ค.'],
  ['2024-04-01','เม.ย. 67'],['2024-07-01','ก.ค.'],['2024-10-01','ต.ค.'],['2025-01-01','ม.ค. 68'],['2025-04-01','เม.ย.'],  // โซนพับเวลา — รายไตรมาส
  ['2025-06-01','มิ.ย. 68'],
  ['2025-07-01','ก.ค.'],['2025-08-01','ส.ค.'],['2025-09-01','ก.ย.'],['2025-10-01','ต.ค.'],['2025-11-01','พ.ย.'],['2025-12-01','ธ.ค.'],
  ['2026-01-01','ม.ค. 69'],['2026-02-01','ก.พ.'],['2026-03-01','มี.ค.'],['2026-04-01','เม.ย.'],['2026-05-01','พ.ค.'],['2026-06-01','มิ.ย.'],
  ['2026-07-01','ก.ค.'],['2026-08-01','ส.ค.'],['2026-09-01','ก.ย.'],['2026-10-01','ต.ค.'],['2026-11-01','พ.ย.'],['2026-12-01','ธ.ค.'],
  ['2027-01-01','ม.ค. 70'],['2027-02-01','ก.พ.'],['2027-03-01','']];

// ═══ ช่วงของเรื่อง — bg สีจางแบ่งยุค ═══
const PBANDS = [
  { a:'2020-07-01', b:'2021-01-01', name:'ช่วง 1 · การระเบิด', tint:'rgba(232,69,44,.055)', ink:'rgba(235,120,98,.85)' },
  { a:'2021-01-01', b:'2022-01-01', name:'ช่วง 2 · ราคาที่ต้องจ่าย', tint:'rgba(96,136,216,.06)', ink:'rgba(140,168,228,.85)' },
  { a:'2022-01-01', b:'2023-01-01', name:'ช่วง 3 · แผ่วแต่ไม่ดับ', tint:'rgba(168,120,220,.055)', ink:'rgba(185,155,230,.85)' },
  { a:'2023-01-01', b:'2024-01-01', name:'ช่วง 4 · ความหวังในคูหา → ถูกหัก', tint:'rgba(88,190,120,.05)', ink:'rgba(130,205,155,.85)' },
  { a:'2024-01-01', b:'2025-01-01', name:'ช่วง 5 · ความสูญเสียและความเงียบ', tint:'rgba(165,165,175,.05)', ink:'rgba(185,185,198,.85)' },
  { a:'2025-01-01', b:'2027-03-08', name:'ช่วง 6 · การเติบโต', tint:'rgba(232,179,76,.06)', ink:'rgba(238,196,110,.9)' },
];
// ═══ สเกล curated 3 ท่อน — single experience ไม่มีปุ่มซูม (แก้ px/วัน ตรงนี้ / เพิ่มท่อนได้เรื่อยๆ) ═══
const SEGS = [
  { from: '2020-06-26', px: 12 },  // การระเบิด — งานถี่ ต้องการอากาศ
  { from: '2021-07-01', px: 8 },   // ดินแดง → ทะลุวัง
  { from: '2022-04-01', px: 5 },   // งานห่าง — เดินเรื่องเร็วขึ้น (รวมปี 66 ทั้งปี)
  { from: '2024-04-01', px: 3 },   // พับเวลา: ความเงียบยาว
  { from: '2025-06-01', px: 5 },   // การเติบโต — กลับจังหวะปกติ
];
SEGS.forEach(s => s.t = new Date(s.from).getTime());
const world = document.getElementById('world');
const vp = document.getElementById('viewport');
const tip = document.getElementById('tip');
const guide = document.getElementById('guide');
function x(d) {
  const t = new Date(d).getTime();
  let px = 40;
  for (let i = 0; i < SEGS.length; i++) {
    const a = SEGS[i].t, b = i + 1 < SEGS.length ? SEGS[i + 1].t : Infinity;
    if (t > a) px += (Math.min(t, b) - a) / DAY * SEGS[i].px;
  }
  return px;
}
function thd(dstr) { const d = new Date(dstr);
  const m = ['ม.ค.','ก.พ.','มี.ค.','เม.ย.','พ.ค.','มิ.ย.','ก.ค.','ส.ค.','ก.ย.','ต.ค.','พ.ย.','ธ.ค.'];
  return d.getDate() + ' ' + m[d.getMonth()] + ' ' + (d.getFullYear() + 543 - 2500); }
function hover(el, it) {
  el.addEventListener('mousemove', e => {
    tip.style.display = 'block';
    tip.innerHTML = '<b>' + (it.full || it.n) + '</b><span class="dt">' + thd(it.d) + '</span>' +
      (it.desc ? '<div>' + it.desc + '…</div>' : '') +
      (it.crowd ? '<div class="crowd">👥 ' + it.crowd + '</div>' : '');
    tip.style.left = Math.min(e.clientX + 16, innerWidth - 360) + 'px';
    tip.style.top = Math.min(e.clientY + 14, innerHeight - 190) + 'px';
    guide.style.display = 'block'; guide.style.left = x(it.d) + 'px';
  });
  el.addEventListener('mouseleave', () => { tip.style.display = 'none'; guide.style.display = 'none'; });
}

const lblCtx = document.createElement('canvas').getContext('2d');
function lblW(t, hero) {
  lblCtx.font = (hero ? '600 13.5px ' : '11px ') + "'Sukhumvit Set','Noto Sans Thai',sans-serif";
  return lblCtx.measureText(t).width;
}

function dotLane(anchorY, key, color, dir) {
  // dir 'up': จุดเรียงเหนือเส้น anchor เท่านั้น / 'down': ใต้เส้นเท่านั้น — ไม่ล้ำเขตเลนอื่น
  const arr = [...DATA[key]].sort((a, b) => a.d.localeCompare(b.d));
  const MAXROW = dir === 'up' ? 4 : 2;   // ความจุเลน: off = 15 + row*23 ต้องไม่ทะลุเขต
  // ชื่อสองระดับ: ลองชื่อกลาง (m) ก่อนทุกอัน — ถ้ากองลึกเกินเลน ถอยชื่อกลางแถวคลัสเตอร์นั้นเป็นชื่อสั้น (n) ทีละอัน
  const useMid = new Map(arr.map(it => [it, !!it.m]));
  const pack = () => {
    const rows = []; let deepest = 0;
    arr.forEach(it => {
      const t = useMid.get(it) ? it.m : it.n;
      const px = x(it.d), w = lblW(t, it.hero) + 18;
      let r = 0; while (rows[r] !== undefined && rows[r] > px) r++;
      rows[r] = px + w; it._row = r; it._lbl = t;
      deepest = Math.max(deepest, r);
    });
    return deepest;
  };
  for (let guard = 0; guard < arr.length && pack() > MAXROW; guard++) {
    const overX = arr.filter(it => it._row > MAXROW).map(it => x(it.d));
    const cand = arr.filter(it => useMid.get(it) && overX.some(ox => Math.abs(x(it.d) - ox) < 400))
      .sort((a, b) => (lblW(b.m, b.hero) - lblW(b.n, b.hero)) - (lblW(a.m, a.hero) - lblW(a.n, a.hero)))[0]
      || arr.find(it => useMid.get(it));
    if (!cand) break;
    useMid.set(cand, false);
  }
  arr.forEach(it => {
    const ev = document.createElement('div');
    ev.className = 'ev' + (it.hero ? ' big' : '');
    const off = 15 + it._row * 23;
    const yy = dir === 'up' ? anchorY - off : anchorY + off;
    ev.style.left = x(it.d) + 'px'; ev.style.top = yy + 'px';
    const tick = document.createElement('div'); tick.className = 'tick';
    if (dir === 'up') { tick.style.top = '0'; tick.style.height = off + 'px'; }
    else { tick.style.top = -off + 'px'; tick.style.height = off + 'px'; }
    const dot = document.createElement('div'); dot.className = 'dot';
    dot.style.background = color;
    const lbl = document.createElement('div'); lbl.className = 'lbl'; lbl.textContent = it._lbl || it.n;
    ev.appendChild(tick); ev.appendChild(dot); ev.appendChild(lbl);
    hover(ev, it); world.appendChild(ev);
  });
}

function faLane() {
  const mid = HERO_LINE;
  const base = document.createElement('div'); base.className = 'base';
  base.style.top = mid + 'px'; base.style.background = 'rgba(232,69,44,.25)'; world.appendChild(base);
  const arr = [...DATA.fa].sort((a, b) => a.d.localeCompare(b.d));
  // Hero = เหนือเส้นแถวเดียว / งานอื่น = ใต้เส้น 3 แถว
  // ═══ ภาษากลางของทีม: ขนาด = ใหญ่(hero)/กลาง/เล็ก/จิ๋ว · แถว = บน(A1)/ล่างหนึ่ง(B1)/ล่างสอง(B2) ═══
  const ROW_OVERRIDE = { 'Graffiti #FREEART': 'B1', 'ป้ายแจก ม็อบสถานทูตเยอรมัน': 'A1',
    '#พร้อม — ค': 'B1',
    'Respect My Vote — เคารพผลเลือกตั้ง': 'A1',
    'ตลาดนัดราษฎร': 'A1' };  // บังคับแถวรายการ์ด: 'A1'|'B1'|'B2' — hero + B1 = hero ใต้เส้น (ครั้งแรก: #พร้อม — ค)
  const AR_OVERRIDE = { 'Graffiti #FREEART': 1.6, 'ตลาดนัดราษฎร': 1.0 };              // สัดส่วนแสดงผลรายการ์ด — รูปจริง 1.79 crop ขอบข้างเล็กน้อยกันดันเพื่อนบ้าน ก.ย. 63
  const TEXT_ONLY = [];                                          // เลนข้อความล่างสุด — ไม่มีรูป กินที่น้อย (ตอนนี้ว่าง)
  const SIZE_OVERRIDE = {                                         // ขนาดที่เอเลียร์เคาะ 4 ก.ค. 69
    'Graffiti #FREEART': 'จิ๋ว',
    'โยนไฟล์หมุดคณะราษฎรออนไลน์': 'จิ๋ว',
    'เวทีศิลปะ ม็อบ 19 กันยา': 'กลาง',
    'ฝันถึง 6 ตุลา ใครฆ่าประชาชน': 'จิ๋ว',
    'เวทีศิลปะ ม็อบ 14 ตุลา': 'กลาง',
    'ปริญญาประชาชน': 'จิ๋ว',
    'ป้ายแจก ม็อบสถานทูตเยอรมัน': 'จิ๋ว',
    'ภาพ Set ปล่อยเพื่อนเรา': 'กลาง',
    'ผ้ายันต์ราษฎร': 'จิ๋ว',
    'บ๊ายบายไดโนเสาร์ x นักเรียนเลว': 'เล็ก',
    'รูปคณะรัฐมนตรี': 'เล็ก',
    'อดอาหารประท้วง — กราฟิกรายวัน': 'จิ๋ว',
    'ทลายแม็พ 112': 'เล็ก',
    'ประติมานุสรณ์ 6 ตุลา – ทุกใบหน้ามีชีวิต': 'ใหญ่',
    'เมียนมาร์ X BIPAM': 'เล็ก',
    'วันเด็ก × พรบ.การศึกษา x นักเรียนเลว': 'กลาง',
    'ม็อบเปิดท้ายวันศุกร์ ลุกไล่เผด็จการ': 'เล็ก',
    'ม็อบ18กรกฎา — เผาหุ่นประยุทธ์': 'เล็ก',
    'ราษฎรยืนยันดันเพดาน': 'กลาง',
    'Respect My Vote — เคารพผลเลือกตั้ง': 'เล็ก',
    'นิรโทษกรรมประชาชน – แคมเปญล่ารายชื่อ': 'กลาง',
    '24 มิถุนา วันประชาชน by Tune & Co.': 'กลาง',
    '10 สิงหา ความฝันประชาชน by Tune & Co.': 'กลาง',
    'Run2Free — วิ่งเพื่อเสรีภาพ by Tune & Co.': 'กลาง',
    'ตุลาที่คิดถึง — Dear October by Tune & Co.': 'กลาง',
    'รณรงค์ประชามติ 8 กุมภา by Tune & Co': 'กลาง',
    'สกรีนเสื้อ #NO112': 'จิ๋ว',
    'กูไม่ไว้วางใจมึง ออกไป๊! x Mob Fest': 'เล็ก',
    'สกรีนเสื้อ ม็อบ 20 กุมภา': 'จิ๋ว',
    'สกรีนเสื้อ x เดินทะลุฟ้า': 'จิ๋ว',
    'ตั๋วช้าง': 'จิ๋ว',
    'ม็อบสกายวอล์ค – คืนสิทธิ์ประกันตัว': 'เล็ก',
    'ยื่นหยุดขัง!': 'เล็ก',
    'ห้องเรียนรัฐมนตรี x นักเรียนเลว': 'เล็ก',
    'สหภาพคนทำงาน': 'เล็ก',
    'ราษฎรฟ้องกลับ': 'เล็ก',
    'สถาบันปรีดีฯ – คำถาม': 'เล็ก',
    'ตลาดนัดราษฎร': 'เล็ก',
    '#NoNpoBill': 'เล็ก',
    'ไพร์ดพาเหรด – โมเมนต์ระหว่างขบวน': 'เล็ก',
    'โหวตอภิปรายไม่ไว้วางใจรัฐบาลประยุทธ์ โดยประชาชนจ้าาาา': 'กลาง',
    'แคมป์ฟังสภา จับตาอภิปรายไม่ไว้วางใจประยุทธ์': 'กลาง',
    'สำนักข่าวไหน': 'เล็ก',
    '#SavePenguin': 'กลาง',
    'ต้นไม้หน้าศาล': 'เล็ก',
    'วาดพื้น แก้ได้ถ้าแก้รัฐธรรมนูญ': 'เล็ก',
    'วาดพื้น รัฐประหารมึงเจอกู': 'กลาง',
    '#Saveจะนะ x Alex Face': 'กลาง',
  };
  const TH_SIZE = { 'ใหญ่': 'hero', 'กลาง': 'medium', 'เล็ก': 'small', 'จิ๋ว': 'tiny' };
  const SIZE = { hero: 200, medium: 140, small: 96, tiny: 74, ph: 56 };  // ph = placeholder จัตุรัสรอรูป
  const PAD = { hero: 24, medium: 24, small: 24, tiny: 10, ph: 10 };
  const wOf = (it, h) => (!it.img && h === SIZE.ph) ? SIZE.ph
    : Math.max(Math.min(Math.round(h * (it.ar || 1.6)), Math.round(h * 1.9)), 60);

  // ความหนาแน่น: ใครมีเพื่อนบ้านใกล้กว่า 100px → โซนแน่น → ย่อลงหนึ่งขั้น
  const DENSE_GAP = 100;
  arr.forEach((it, i) => {
    const px = x(it.d);
    const dPrev = i > 0 ? px - x(arr[i-1].d) : 1e9;
    const dNext = i < arr.length - 1 ? x(arr[i+1].d) - px : 1e9;
    it._dense = Math.min(dPrev, dNext) < DENSE_GAP;
  });

  const tracks = { A1: -1e9, A1snug: -1e9, B1: -1e9, B2: -1e9 };
  const heroSpans = [];
  const placedAbove = [];  // skyline เหนือเส้น — ให้ ph ที่ล้นด้านล่างลอยขึ้นชั้นสองได้
  const placedBelow = [];  // skyline: กล่องที่วางแล้ว {x0,x1,y0,y1}
  arr.filter(it => it.hero).forEach(it => {
    const px = x(it.d), w = Math.max(wOf(it, SIZE.hero), 84) + PAD.hero;
    if (ROW_OVERRIDE[it.n] === 'B1') {
      // HERO ใต้เส้น — เกาะเส้นแบบเดียวกับ hero บน แต่ห้อยลงล่าง จองพื้นที่ใน skyline ล่าง
      placedBelow.push({ x0: px, x1: px + w, xr: px + wOf(it, SIZE.hero), y0: GAP, y1: GAP + 244 });
      it._tk = 'B'; it._size = 'hero'; it._y = GAP;
      return;
    }
    heroSpans.push([px - 24, px + w]);
    placedAbove.push({ x0: px - 24, x1: px + w, xr: px + w, y0: GAP, y1: GAP + 244 });
    it._tk = 'A1'; it._size = 'hero';
  });
  const hitsHero = (px, w) => heroSpans.some(([a, b]) => px < b && px + w > a);
  const spanOf = (it, size) => Math.max(wOf(it, SIZE[size]), size === 'ph' ? 56 : size === 'tiny' ? 66 : 84) + PAD[size];

  // เลนข้อความ: เฉพาะการ์ดใน TEXT_ONLY — งานไม่มีรูปเข้าระบบการ์ดปกติเป็น placeholder 1:1
  const isText = it => !it.hero && TEXT_ONLY.includes(it.n);
  const trows = [];
  arr.filter(isText).forEach(it => {
    it._tk = 'T'; it._size = 'text';
    const px = x(it.d), w = lblW(it.n, false) + 18;
    let r = 0; while (trows[r] !== undefined && trows[r] > px) r++;
    trows[r] = px + w; it._trow = r;
  });
  const boxH = s => SIZE[s] + (s === 'ph' ? 20 : 32);  // ph caption บรรทัดเดียว
  arr.filter(it => !it.hero && !isText(it)).forEach(it => {
    const px = x(it.d);
    const up = it._dense ? 'small' : 'medium';
    const low = it._dense ? 'tiny' : 'small';
    if (AR_OVERRIDE[it.n]) it.ar = AR_OVERRIDE[it.n];
    const forced = SIZE_OVERRIDE[it.n] ? (TH_SIZE[SIZE_OVERRIDE[it.n]] || SIZE_OVERRIDE[it.n]) : !it.img ? 'ph' : null;
    const legacy = it.d < '2021-01-01';  // ช่วง 1 ล็อกแล้ว — กติกาขอบเผื่อระยะแบบเดิมเป๊ะ
    const snugOf = s => Math.max(wOf(it, SIZE[s]), s === 'ph' ? 56 : s === 'tiny' ? 66 : 84);
    // ปี 64+: แถวบนว่างเมื่อพ้นขอบจริงของการ์ดก่อนหน้า (+4px หายใจ) ไม่ใช่ขอบเผื่อระยะ
    const a1free = () => legacy ? tracks.A1 < px : (tracks.A1 < px || tracks.A1snug + 4 < px);
    let size, below = true;
    if (ROW_OVERRIDE[it.n] === 'A1') {
      // บังคับขึ้นบน: วางบน skyline เหนือเส้น — แถวบนว่างก็เกาะเส้น ไม่ว่างก็ซ้อนชั้นสอง
      // คำสั่งคนมาก่อน: เช็คชนด้วยขอบจริงของการ์ด (xr) ไม่ใช่ขอบเผื่อระยะหายใจ
      const sz = forced || up, h = boxH(sz);
      const w = Math.max(wOf(it, SIZE[sz]), sz === 'ph' ? 56 : sz === 'tiny' ? 66 : 84) + 2;
      let y = GAP, moved = true;
      while (moved) { moved = false;
        for (const r of placedAbove) {
          if (px < (r.xr !== undefined ? r.xr : r.x1) - 6 && px + w - 6 > r.x0 && y < r.y1 && y + h > r.y0) { y = r.y1 + GAP; moved = true; }
        } }
      if (y + h <= 284) {
        placedAbove.push({ x0: px, x1: px + spanOf(it, sz), xr: px + w, y0: y, y1: y + h });
        it._size = sz; it._y2 = y;
        if (y === GAP) { it._tk = 'A1'; tracks.A1 = Math.max(tracks.A1, px + spanOf(it, sz));
          tracks.A1snug = Math.max(tracks.A1snug, px + w); }
        else it._tk = 'A2';
        return;
      }
    }
    if (!ROW_OVERRIDE[it.n] && forced && a1free() && !hitsHero(px, spanOf(it, forced))) {
      size = forced; below = false;
    } else if (!ROW_OVERRIDE[it.n] && !forced && a1free() && !hitsHero(px, spanOf(it, up))) {
      size = up; below = false;
    } else {
      size = forced || low;
    }
    if (!below) { it._tk = 'A1'; it._size = size; tracks.A1 = Math.max(tracks.A1, px + spanOf(it, size));
      tracks.A1snug = Math.max(tracks.A1snug, px + snugOf(size));
      placedAbove.push({ x0: px, x1: px + spanOf(it, size), y0: GAP, y1: GAP + boxH(size),
        xr: px + snugOf(size) }); return; }
    // skyline ล่างเส้น: ชิดเส้นที่สุด ชนแล้วหลบลง — ลึกเกินเพดาน (ก่อนเลนข้อความ) ให้ย่อไซส์แล้วลองใหม่
    const LIMIT = it.d < '2021-01-01' ? 260 : 306;  // ปี 64 ไม่มีเลนข้อความ ใช้พื้นที่ลึกได้ถึงขอบเขต
    const LADDER = ['medium', 'small', 'tiny'];
    const place = s => {
      const w = spanOf(it, s), h = boxH(s), ws = snugOf(s);
      let y = GAP, moved = true;
      while (moved) {
        moved = false;
        for (const r of placedBelow) {
          // ปี 64+ เช็คชนด้วยขอบจริง (xr) + tolerance 4px — แพ็คแน่นขึ้น ไม่โดนย่อโดยไม่จำเป็น
          const hit = legacy ? (px < r.x1 && px + w > r.x0)
            : (px < (r.xr !== undefined ? r.xr : r.x1) - 4 && px + ws - 4 > r.x0);
          if (hit && y < r.y1 && y + h > r.y0) { y = r.y1 + GAP; moved = true; }
        }
      }
      return { y, w, h, ws };
    };
    let s = size, spot = place(s);
    while (spot.y + spot.h > LIMIT && LADDER.indexOf(s) !== -1 && LADDER.indexOf(s) < LADDER.length - 1) {
      s = LADDER[LADDER.indexOf(s) + 1];
      spot = place(s);
    }
    if ((!legacy || s === 'ph') && spot.y + spot.h > LIMIT) {
      // ล่างเต็มจริง → ลองลอยขึ้นชั้นสองเหนือแถวบน (A2) — เช็คชนด้วยขอบจริง
      const w = spanOf(it, s), ws = snugOf(s), h = boxH(s);
      let y = GAP, moved = true;
      while (moved) { moved = false;
        for (const r of placedAbove) {
          if (px < (r.xr !== undefined ? r.xr : r.x1) - 4 && px + ws - 4 > r.x0 && y < r.y1 && y + h > r.y0) { y = r.y1 + GAP; moved = true; }
        } }
      if (y + h <= 284) {
        placedAbove.push({ x0: px, x1: px + w, xr: px + ws, y0: y, y1: y + h });
        it._tk = 'A2'; it._size = s; it._y2 = y; return;
      }
    }
    if (spot.y + spot.h > LIMIT) spot.y = Math.max(GAP, LIMIT - spot.h);  // ทางหนีสุดท้าย → หนีบไว้ไม่ให้ทะลุเขต
    placedBelow.push({ x0: px, x1: px + spot.w, xr: px + spot.ws, y0: spot.y, y1: spot.y + spot.h });
    it._tk = 'B'; it._size = s; it._y = spot.y;
  });
  arr.forEach(it => {
    const card = document.createElement('div');
    card.className = 'card' + (it.hero ? ' hero' : '');
    card.style.left = x(it.d) + 'px'; card.style.top = mid + 'px';
    const above = it._tk === 'A1' || it._tk === 'A2';
    const off = it._tk === 'T' ? 264 + it._trow * 15 : it._tk === 'A2' ? it._y2 : (it._tk === 'B' ? it._y : GAP);
    if (it._tk === 'T') {  // เลนข้อความ: จุด + ชื่อ เท่านั้น
      const tick = document.createElement('div'); tick.className = 'tick';
      tick.style.top = '0'; tick.style.height = off + 'px'; tick.style.opacity = '.35';
      const dotb = document.createElement('div'); dotb.className = 'dotb'; dotb.style.top = '-4.5px';
      const txt = document.createElement('div');
      txt.style.cssText = 'position:absolute; left:8px; top:' + (off - 7) + 'px; font-size:11px; color:rgba(242,240,235,.5); white-space:nowrap;';
      txt.textContent = it.n;
      card.appendChild(tick); card.appendChild(dotb); card.appendChild(txt);
      hover(card, it); world.appendChild(card);
      return;
    }
    const tick = document.createElement('div'); tick.className = 'tick';
    if (above) { tick.style.top = -off + 'px'; tick.style.height = off + 'px'; }
    else { tick.style.top = '0'; tick.style.height = off + 'px'; }
    const dotb = document.createElement('div'); dotb.className = 'dotb';
    dotb.style.top = it.hero ? '-7px' : '-4.5px';
    const box = document.createElement('div'); box.className = 'box';
    if (above) box.style.bottom = off + 'px';  // ยึดขอบล่างการ์ดกับเส้นเชื่อม — สูงเท่าไหร่ก็ไม่หลุด/ไม่ชนเส้นบน
    else box.style.top = off + 'px';
    if (it.img) { const im = document.createElement('img'); im.src = it.img; im.loading = 'lazy';
      im.style.height = SIZE[it._size] + 'px';
      if (!it.hero) im.style.width = wOf(it, SIZE[it._size]) + 'px'; else im.style.width = 'auto';
      box.appendChild(im); }
    else { const ph = document.createElement('div'); ph.className = 'ph'; ph.textContent = 'รอรูป';
      ph.style.cssText = 'width:' + wOf(it, SIZE[it._size]) + 'px; height:' + SIZE[it._size] + 'px;' +
        'border-style:dashed; border-color:rgba(232,69,44,.4);'; box.appendChild(ph); }
    const cap = document.createElement('div'); cap.className = 'cap'; cap.textContent = it.n;
    cap.style.width = Math.max(wOf(it, SIZE[it._size]), it._size === 'tiny' ? 66 : 84) + 'px';
    if (it._size === 'tiny') cap.style.fontSize = '9.5px';
    if (it._size === 'ph') { cap.style.cssText = 'width:60px; font-size:8.5px; -webkit-line-clamp:1; margin-top:3px;'; }
    if (it.n.includes('Tune & Co')) {  // งานตระกูล Tune & Co — ชื่อเต็มสำคัญ ให้ 3 บรรทัดไม่ตัด
      cap.style.webkitLineClamp = '3';
      cap.style.width = Math.max(wOf(it, SIZE[it._size]), 120) + 'px';
    }
    box.appendChild(cap);
    card.appendChild(tick); card.appendChild(dotb); card.appendChild(box);
    hover(card, it); world.appendChild(card);
  });
}

function render() {
  world.querySelectorAll('.mgrid,.mlabel,.ev,.card,.base,.lane-sep,.pband').forEach(e => e.remove());
  world.style.width = (x(new Date(T1)) + 80) + 'px';
  PBANDS.forEach(p => {
    const b = document.createElement('div'); b.className = 'pband';
    const x0 = x(p.a), x1 = x(p.b);
    b.style.left = x0 + 'px'; b.style.width = (x1 - x0) + 'px';
    b.style.background = 'linear-gradient(180deg, ' + p.tint + ', transparent 60%, ' + p.tint + ')';
    const bar = document.createElement('div'); bar.className = 'pbar'; bar.style.background = p.ink;
    b.appendChild(bar); world.appendChild(b);  // ป้ายชื่อช่วง (.pname) ถอดออก 6 ก.ค. 69 — เหลือแถบสี+เส้นบนไว้แยกยุค
  });
  MONTHS.forEach(([d, l]) => {
    const g = document.createElement('div'); g.className = 'mgrid'; g.style.left = x(d) + 'px'; world.appendChild(g);
    if (l) { const t = document.createElement('div'); t.className = 'mlabel'; t.style.left = x(d) + 'px'; t.textContent = l; world.appendChild(t); }
  });
  [FA.top, FA.top + FA.h].forEach(y => {
    const s = document.createElement('div'); s.className = 'lane-sep'; s.style.top = y + 'px';
    s.style.background = 'rgba(242,240,235,.14)'; world.appendChild(s);
  });
  dotLane(FA.top, 'pol', 'var(--pol)', 'up');
  faLane();
  dotLane(FA.top + FA.h, 'cul', 'var(--cul)', 'down');
}
render();

// ป้ายเลน (lanetag) การเมือง/FREE ARTS/วัฒนธรรม ถอดออก 6 ก.ค. 69 — ไม่จำเป็นแล้ว
let drag = null;
vp.addEventListener('mousedown', e => { drag = { x: e.clientX, s: vp.scrollLeft }; vp.classList.add('drag'); });
addEventListener('mousemove', e => { if (drag) vp.scrollLeft = drag.s - (e.clientX - drag.x); });
addEventListener('mouseup', () => { drag = null; vp.classList.remove('drag'); });
vp.addEventListener('wheel', e => { if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) { vp.scrollLeft += e.deltaY; e.preventDefault(); } }, { passive: false });
</script></body></html>"""
page = page.replace('__DATA__', json.dumps(data, ensure_ascii=False))
open('/Users/cudo/Desktop/Artivism/site/mockup.html', 'w').write(page)
print(f"v2: pol {len(data['pol'])} | cul {len(data['cul'])} | fa {len(data['fa'])} (with img: {sum(1 for f in data['fa'] if f['img'])})")
