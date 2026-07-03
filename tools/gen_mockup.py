# -*- coding: utf-8 -*-
from __future__ import annotations
import json, html, os

research = json.load(open('/Users/cudo/Desktop/Artivism/research-data.json'))
politics = research['result']['results'][0]['key_events']

culture_raw = json.load(open('/Users/cudo/Desktop/Artivism/culture-curated.json'))['items']
CULT_DATES = {
    'วิ่งกันนะแฮมทาโร่': '2020-07-26', 'ปฏิรูป — Rap Against Dictatorship': '2020-11-13',
    'School Town King': '2020-12-17', 'ปรากฏการณ์สะท้านฟ้า': '2020-09-15',
    'เป็ดยางเหลือง': '2020-11-17', 'นิทรรศการ "แขวน"': '2020-10-01',
    'PrachathipaType': '2020-09-19', 'คืนกราฟฟิตี้ราชประสงค์': '2020-11-18',
}
culture = []
for it in culture_raw:
    if it['period_tag'] != '1-2563': continue
    d = it.get('date_exact') if it.get('date_exact') and it.get('date_exact') != 'unknown' else None
    if not d:
        for kw, dd in CULT_DATES.items():
            if kw in it['title']: d = dd; break
    if d and d >= '2020-07-01':
        culture.append({'date': d, 'name': it['title'], 'short': it.get('short'), 'hero': it.get('hero', False), 'desc': it['story']})

IMG_DIR = '/Users/cudo/Desktop/Artivism/site/tl-img'
import subprocess
def img_w(path, hero):
    r = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path], capture_output=True, text=True)
    vals = [int(l.split(': ')[1]) for l in r.stdout.strip().split('\n')[1:]]
    if hero: return max(90, min(380, round(235 * vals[0] / vals[1])))
    return max(30, min(100, round(50 * vals[0] / vals[1])))
fa = []
for line in open('/Users/cudo/Desktop/Artivism/freearts-events.txt'):
    p = [x.strip() for x in line.split('|')]
    if '2020-07-01' <= p[0] <= '2020-12-31':
        eid = p[1]
        fp = f'{IMG_DIR}/{eid}.jpg'
        img = f'tl-img/{eid}.jpg' if os.path.exists(fp) else None
        hero = p[4] == 'tier:hero'
        fa.append({'date': p[0], 'name': p[2], 'hero': hero, 'img': img,
                   'iw': img_w(fp, hero) if img else 80})

def items(lst, kind):
    out = []
    for it in lst:
        out.append({'d': it['date'], 'n': it.get('short') or it['name'], 'full': it['name'],
                    'desc': (it.get('desc') or it.get('description') or '')[:260],
                    'crowd': it.get('crowd_estimate', ''),
                    'hero': it.get('hero', False), 'img': it.get('img'), 'iw': it.get('iw', 96)})
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
.ev .lbl { position:absolute; white-space:nowrap; font-size:11px; color:var(--dim); left:6px; top:-7px;
  max-width:200px; overflow:hidden; text-overflow:ellipsis; }
.ev .tick { position:absolute; width:1px; background:rgba(242,240,235,.13); left:0; }
.ev:hover .lbl { color:var(--fg); z-index:40; }
.ev.big .dot { width:11px; height:11px; left:-5.5px; top:-5.5px; }
.ev.big .lbl { font-size:13.5px; font-weight:600; color:rgba(242,240,235,.92); top:-9px; max-width:240px; }

.card { position:absolute; z-index:6; }
.card .tick { position:absolute; width:1px; background:rgba(232,69,44,.3); left:0; }
.card .dotb { position:absolute; width:9px; height:9px; border-radius:50%; background:var(--fa); left:-4.5px; }
.card.hero .dotb { width:14px; height:14px; left:-7px; box-shadow:0 0 12px rgba(232,69,44,.5); }
.card .box { position:absolute; left:-2px; }
.card img, .card .ph { display:block; border-radius:6px; object-fit:cover; border:1px solid rgba(232,69,44,.35);
  background:#1a1210; }
.card img { height:50px; object-fit:cover; }
.card.hero img { width:auto; height:235px; max-width:380px; object-fit:contain; border-width:2px; box-shadow:0 4px 22px rgba(232,69,44,.25); }
.card .ph { width:80px; height:50px; display:flex; align-items:center; justify-content:center;
  color:rgba(232,69,44,.5); font-size:10px; }
.card .cap { font-size:10.5px; color:var(--dim); line-height:1.35; width:100px; margin-top:4px;
  display:-webkit-box; -webkit-line-clamp:2; -webkit-box-orient:vertical; overflow:hidden; }
.card.hero .cap { font-size:15px; font-weight:700; color:#fff; width:auto; max-width:240px; }
.card:hover img { border-color:var(--fa); }
.card:hover .cap { color:var(--fg); }

#tip { position:fixed; display:none; z-index:100; max-width:340px; background:#1a1a18; border:1px solid rgba(242,240,235,.2);
  border-radius:10px; padding:12px 15px; font-size:12.5px; line-height:1.6; color:var(--dim); pointer-events:none; }
#tip b { color:var(--fg); display:block; margin-bottom:3px; font-size:13px; }
#tip .dt { color:var(--faint); font-size:11px; }
#tip .crowd { color:var(--cul); font-size:11.5px; margin-top:4px; }
#guide { position:absolute; top:0; bottom:0; width:1px; background:rgba(232,179,76,.35); display:none; z-index:2; }
</style></head><body>
<header>
  <h1>Timeline Mockup v3 — 3 เส้นเรื่อง</h1>
  <span class="sub">การเมือง 15% · FREE ARTS 75% (hero 50 : งานอื่น 50) · วัฒนธรรม 10%</span>
  <div class="legend">
    <span><span class="k" style="background:var(--pol)"></span>การเมือง</span>
    <span><span class="k" style="background:var(--fa)"></span>Free Arts</span>
    <span><span class="k" style="background:var(--cul)"></span>วัฒนธรรม</span>
  </div>
</header>
<div class="zoom">ซูม:
  <button data-z="8">แน่น</button><button data-z="12" class="on">กลาง</button><button data-z="18">ขยาย</button>
  <span style="align-self:center; margin-left:8px">ลากเพื่อเลื่อน · ชี้เพื่อดูรายละเอียด</span>
</div>
<div id="viewport"><div id="world"><div id="guide"></div></div></div>
<div id="tip"></div>
<script>
const DATA = __DATA__;
const T0 = new Date('2020-06-26').getTime(), T1 = new Date('2021-01-06').getTime();
const DAY = 86400000;
// lanes: pol 25% / fa 60% / cul 15% of 760 usable (top 40 for month labels)
const POL = { top:40,  h:122 };            // 15% — เกาะเส้นแบ่งบน ชี้ขึ้น
const FA  = { top:162, h:607 };            // 75% — เส้นแดง = เส้น Hero
const CUL = { top:769, h:81 };             // 10% — เกาะเส้นแบ่งล่าง ชี้ลง
const HERO_LINE = FA.top + 303;            // hero 50% / งานอื่น 50% ของโซน Free Arts
const MONTHS = [['2020-07-01','ก.ค. 63'],['2020-08-01','ส.ค.'],['2020-09-01','ก.ย.'],['2020-10-01','ต.ค.'],['2020-11-01','พ.ย.'],['2020-12-01','ธ.ค.'],['2021-01-01','']];
let pxday = 12;
const world = document.getElementById('world');
const vp = document.getElementById('viewport');
const tip = document.getElementById('tip');
const guide = document.getElementById('guide');
function x(d) { return (new Date(d).getTime() - T0) / DAY * pxday + 40; }
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

function dotLane(anchorY, key, color, dir) {
  // dir 'up': จุดเรียงเหนือเส้น anchor เท่านั้น / 'down': ใต้เส้นเท่านั้น — ไม่ล้ำเขตเลนอื่น
  const arr = [...DATA[key]].sort((a, b) => a.d.localeCompare(b.d));
  const rows = [];
  arr.forEach(it => {
    const px = x(it.d), w = Math.min(it.n.length * (it.hero ? 7.6 : 6), 240) + 14;
    let r = 0; while (rows[r] !== undefined && rows[r] > px) r++;
    rows[r] = px + w; it._row = r;
  });
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
    const lbl = document.createElement('div'); lbl.className = 'lbl'; lbl.textContent = it.n;
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
  const ROW_OVERRIDE = { 'บ๊ายบายไดโนเสาร์ x นักเรียนเลว': 'B1', 'ม็อบ 22 พฤศจิกา ถนนอักษะ': 'B3' };  // จัดตามที่เอเลียร์เคาะ 3 ก.ค. 69
  const tracks = { A1: -1e9, B1: -1e9, B2: -1e9, B3: -1e9 };
  arr.forEach(it => {
    const px = x(it.d);
    const w = (it.hero ? Math.max(it.iw || 190, 140) : Math.max(it.iw || 80, 80) + 10) + 14;
    let tk;
    if (it.hero) tk = 'A1';
    else if (ROW_OVERRIDE[it.n]) tk = ROW_OVERRIDE[it.n];
    else {
      tk = ['B1', 'B2', 'B3'].find(k => tracks[k] < px);
      if (!tk) tk = ['B1', 'B2', 'B3'].reduce((a, b) => tracks[a] <= tracks[b] ? a : b); // ตกทุกแถว → เลือกแถวที่ว่างเร็วสุด (กันซ้อนตำแหน่งเดียวกัน)
    }
    tracks[tk] = Math.max(tracks[tk], px + w); it._tk = tk;
  });
  arr.forEach(it => {
    const card = document.createElement('div');
    card.className = 'card' + (it.hero ? ' hero' : '');
    card.style.left = x(it.d) + 'px'; card.style.top = mid + 'px';
    const gap = { A1: 14, B1: 14, B2: 14 + 82 + 12, B3: 14 + (82 + 12) * 2 };
    const above = it._tk.startsWith('A');
    const off = gap[it._tk];
    const tick = document.createElement('div'); tick.className = 'tick';
    if (above) { tick.style.top = -off + 'px'; tick.style.height = off + 'px'; }
    else { tick.style.top = '0'; tick.style.height = off + 'px'; }
    const dotb = document.createElement('div'); dotb.className = 'dotb';
    dotb.style.top = it.hero ? '-7px' : '-4.5px';
    const box = document.createElement('div'); box.className = 'box';
    if (above) box.style.bottom = off + 'px';  // ยึดขอบล่างการ์ดกับเส้นเชื่อม — สูงเท่าไหร่ก็ไม่หลุด/ไม่ชนเส้นบน
    else box.style.top = off + 'px';
    if (it.img) { const im = document.createElement('img'); im.src = it.img; im.loading = 'lazy';
      if (!it.hero) im.style.width = (it.iw || 80) + 'px';
      box.appendChild(im); }
    else { const ph = document.createElement('div'); ph.className = 'ph'; ph.textContent = 'ไม่มีรูป'; box.appendChild(ph); }
    const cap = document.createElement('div'); cap.className = 'cap'; cap.textContent = it.n;
    cap.style.width = it.hero ? Math.max(it.iw || 190, 140) + 'px' : Math.max(it.iw || 80, 80) + 'px';
    box.appendChild(cap);
    card.appendChild(tick); card.appendChild(dotb); card.appendChild(box);
    hover(card, it); world.appendChild(card);
  });
}

function render() {
  world.querySelectorAll('.mgrid,.mlabel,.ev,.card,.base,.lane-sep').forEach(e => e.remove());
  world.style.width = ((T1 - T0) / DAY * pxday + 120) + 'px';
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

[[POL, 'การเมือง', 'var(--pol)'], [FA, 'FREE ARTS', 'var(--fa)'], [CUL, 'วัฒนธรรม', 'var(--cul)']].forEach(([L, label, color]) => {
  const t = document.createElement('div'); t.className = 'lanetag'; t.textContent = label; t.style.color = color;
  document.body.appendChild(t);
  const place = () => { const r = vp.getBoundingClientRect(); t.style.top = (r.top + L.top + 4) + 'px'; };
  place(); addEventListener('resize', place); addEventListener('scroll', place);
});
document.querySelectorAll('.zoom button').forEach(b => b.addEventListener('click', () => {
  document.querySelectorAll('.zoom button').forEach(x => x.classList.remove('on'));
  b.classList.add('on'); pxday = +b.dataset.z; render();
}));
let drag = null;
vp.addEventListener('mousedown', e => { drag = { x: e.clientX, s: vp.scrollLeft }; vp.classList.add('drag'); });
addEventListener('mousemove', e => { if (drag) vp.scrollLeft = drag.s - (e.clientX - drag.x); });
addEventListener('mouseup', () => { drag = null; vp.classList.remove('drag'); });
vp.addEventListener('wheel', e => { if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) { vp.scrollLeft += e.deltaY; e.preventDefault(); } }, { passive: false });
</script></body></html>"""
page = page.replace('__DATA__', json.dumps(data, ensure_ascii=False))
open('/Users/cudo/Desktop/Artivism/site/mockup.html', 'w').write(page)
print(f"v2: pol {len(data['pol'])} | cul {len(data['cul'])} | fa {len(data['fa'])} (with img: {sum(1 for f in data['fa'] if f['img'])})")
