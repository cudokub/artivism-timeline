# -*- coding: utf-8 -*-
from __future__ import annotations
import json, html

data = json.load(open('/Users/cudo/Desktop/Artivism/research-data.json'))
periods = data['result']['results']  # 0:2563 1:2564 2:2565 3:2566 4:2567 5:2568-69
events_txt = open('/Users/cudo/Desktop/Artivism/freearts-events.txt').read().strip().split('\n')
culture = json.load(open('/Users/cudo/Desktop/Artivism/culture-curated.json'))['items']
CULT_TAG = {1:'1-2563', 2:'2-2564', 3:'3-2565', 4:'4-2566', 5:'5-2567-กลาง68', 6:'6-มิย68-กพ69'}
def cult_in(tag): return [c for c in culture if c['period_tag'] == tag]

fa_events = []
for line in events_txt:
    parts = [p.strip() for p in line.split('|')]
    fa_events.append({'date': parts[0], 'id': parts[1], 'name': parts[2], 'tier': parts[4].replace('tier:','')})

PHASES = [
    dict(num=1, name='ระเบิด', window='ก.ค. – ธ.ค. 2563', pidx=[0],
         talk='Act สิ Art · Mob Fest (คลุมอนุสาวรีย์ + ขบวนเสด็จ)',
         fa_range=('2020-01-01','2020-12-31'),
         punch='Free Arts เกิดในเดือนที่ขบวนกำลังพีค — งานอัดแน่นแบบสัปดาห์ต่อสัปดาห์ตลอด 4 เดือน หนาแน่นที่สุดใน 5 ปีของกลุ่ม'),
    dict(num=2, name='ราคาที่ต้องจ่าย', window='2564', pidx=[1],
         talk='Save Penguin · ที่นี่มีคนตาย',
         fa_range=('2021-01-01','2021-12-31'),
         punch='งานเปลี่ยนโทนจากเทศกาลเป็นงานดูแลกันและงานความทรงจำ (กราฟิกรายวันให้คนอดอาหาร, ภาพให้คนที่ตาย) · โบนัสจากทีมรีเสิช: กิจกรรมศิลปะ-เต้นของศิลปะปลดแอกใน #ม็อบ20มีนา ถูกบันทึกอยู่ในประมวลข่าวการชุมนุม — เราอยู่ในบันทึกประวัติศาสตร์ของขบวน'),
    dict(num=3, name='แผ่ว แต่ไม่ดับ', window='2565', pidx=[2],
         talk='ฉลองวันชาติ คณะราษฎรยังไม่ตาย (โต๊ะยาว)',
         fa_range=('2022-01-01','2022-12-31'),
         punch='ม็อบมวลชนหายไป แต่ Free Arts กลับทำงานที่ใหญ่ที่สุด — 6 ตุลา หวังว่าเสียงลมจะพาล่องไป (8,000+ คน) และฉลองวันชาติโต๊ะยาว คือคำตอบว่า "เมื่อลงถนนไม่ได้ ศิลปะทำอะไร"'),
    dict(num=4, name='ความหวังในคูหา → ถูกหัก', window='2566', pidx=[3],
         talk='พร้อม (Street Art กับพี่หนูหริ่ง)',
         fa_range=('2023-01-01','2023-12-31'),
         punch='ปีที่อารมณ์สวิงแรงสุด และงาน "พร้อม" เกิดตรงจุดที่ความหวังกำลังถูกหักพอดี (ก.ค. 66 — สัปดาห์เดียวกับที่ สว. โหวตสกัดพิธา) street art นั้นคือเสียงของคนที่เพิ่งชนะเลือกตั้งแต่ถูกปล้นชัยชนะ'),
    dict(num=5, name='ความสูญเสีย และความเงียบ', window='2567 – กลาง 2568', pidx=[4],
         talk='นิรโทษกรรมประชาชน',
         fa_range=('2024-01-01','2025-06-14'),
         extra_events=[('2568-2569', lambda d: d < '2025-06' or d == '2025-07-16')],
         punch='นิรโทษกรรมประชาชนอยู่ช่วงนี้ — และช่วงเงียบที่ยาวที่สุดของ Free Arts (ธ.ค. 67 – มิ.ย. 68) อยู่ตรงนี้ เล่าตรงๆ ได้เลยว่าทำไมหยุด'),
    dict(num=6, name='กลับมา เพื่ออนาคต', window='มิ.ย. 2568 – ก.พ. 2569', pidx=[5],
         talk='Voter Concert → Present & Future',
         fa_range=('2025-06-15','2026-12-31'),
         punch='Free Arts กลับมาพร้อมสนามใหม่ (ประชามติ) — Voter Concert ขมวดทุกอย่าง: connection ศิลปิน 5 ปี + จังหวะการเมืองที่ถูกต้อง → ประชามติผ่าน 19.88 ล้านเสียง → เส้น timeline ยังวิ่งต่อ: สสร. / รัฐธรรมนูญใหม่ / อนาคตที่ยังไม่ถูกเขียน → Present & Future ชวนคนจินตนาการ'),
]

def esc(s): return html.escape(s or '')

def phase_events(ph):
    """political events for phase, handling the 2568-69 split"""
    evs = []
    for i in ph['pidx']:
        for e in periods[i]['key_events']:
            d = e['date']
            if ph['num'] == 5 and i == 4:
                evs.append(e)
            elif ph['num'] == 5:
                pass
            else:
                evs.append(e)
    # P5 borrows early 2568-69 events; P6 excludes them
    p56 = periods[5]['key_events']
    if ph['num'] == 5:
        evs += [e for e in p56 if e['date'] < '2025-06' or e['date'] == '2025-07-16']
    if ph['num'] == 6:
        evs = [e for e in p56 if not (e['date'] < '2025-06' or e['date'] == '2025-07-16')]
    evs.sort(key=lambda e: e['date'])
    return evs

def fa_in(ph):
    lo, hi = ph['fa_range']
    return [e for e in fa_events if lo <= e['date'] <= hi]

THMONTH = {1:'ม.ค.',2:'ก.พ.',3:'มี.ค.',4:'เม.ย.',5:'พ.ค.',6:'มิ.ย.',7:'ก.ค.',8:'ส.ค.',9:'ก.ย.',10:'ต.ค.',11:'พ.ย.',12:'ธ.ค.'}
def thdate(d):
    p = d.split('-')
    y = int(p[0]) + 543
    if len(p) == 1: return str(y)
    if len(p) == 2: return f"{THMONTH[int(p[1])]} {str(y)[2:]}"
    return f"{int(p[2])} {THMONTH[int(p[1])]} {str(y)[2:]}"


def cult_html(lst, title):
    if not lst: return ''
    h = [f'<div class="cult-block"><h4>{title} — {len(lst)} ชิ้น</h4>']
    for c in lst:
        dead = '<span class="dead">⚠ ลิงก์ตาย</span>' if c['link_status'] == 'dead' else ''
        h.append(f'<div class="cult-item"><span class="cat">{esc(c["cat"])}</span>'
                 f'<a href="{esc(c["link"])}" target="_blank">{esc(c["title"])}</a>'
                 f'<span class="meta">{esc(c["creator"])} · {esc(c["year"])}</span>{dead}'
                 f'<div class="story">{esc(c["story"])}</div>'
                 f'<div class="show">ขึ้นจอ: {esc(c["show_asset"])}</div></div>')
    h.append('</div>')
    return ''.join(h)

parts = []
parts.append("""<!DOCTYPE html>
<html lang="th"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Timeline การเมืองไทย × ศิลปะปลดแอก 2563–2569</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
:root { --bg:#0c0c0c; --fg:rgba(242,240,235,.85); --dim:rgba(242,240,235,.5); --faint:rgba(242,240,235,.32);
  --accent:#e8452c; --gold:#e8b34c; --card:rgba(242,240,235,.045); --line:rgba(242,240,235,.12); }
html { scroll-behavior:smooth; }
body { background:var(--bg); color:var(--fg); font-family:'Sukhumvit Set','Noto Sans Thai','Helvetica Neue',sans-serif;
  font-weight:300; line-height:1.85; padding:0 20px 120px; }
.wrap { max-width:880px; margin:0 auto; }
header { padding:80px 0 30px; }
h1 { font-size:clamp(26px,4vw,44px); font-weight:600; line-height:1.3; letter-spacing:.01em; }
.sub { color:var(--dim); margin-top:12px; font-size:15px; }
.status { display:inline-block; margin-top:18px; font-size:13px; color:var(--gold);
  border:1px solid rgba(232,179,76,.4); border-radius:999px; padding:5px 16px; }
nav { position:sticky; top:0; background:rgba(12,12,12,.92); backdrop-filter:blur(12px);
  padding:14px 0; margin:30px 0 10px; border-bottom:1px solid var(--line); z-index:10;
  display:flex; gap:8px; flex-wrap:wrap; }
nav a { color:var(--dim); text-decoration:none; font-size:13px; border:1px solid var(--line);
  border-radius:999px; padding:4px 13px; white-space:nowrap; transition:.15s; }
nav a:hover { color:var(--fg); border-color:var(--dim); }
h2 { font-size:clamp(20px,2.6vw,30px); font-weight:600; margin:0 0 6px; }
h3 { font-size:16px; font-weight:600; color:var(--dim); letter-spacing:.12em; text-transform:uppercase; margin:34px 0 14px; }
table.overview { width:100%; border-collapse:collapse; margin:26px 0 10px; font-size:15px; }
table.overview th { text-align:left; color:var(--faint); font-weight:400; font-size:12.5px; letter-spacing:.1em;
  padding:8px 12px; border-bottom:1px solid var(--line); }
table.overview td { padding:11px 12px; border-bottom:1px solid rgba(242,240,235,.06); vertical-align:top; }
table.overview td.n { color:var(--accent); font-weight:600; }
table.overview a { color:var(--fg); text-decoration:none; font-weight:400; border-bottom:1px dotted var(--faint); }
section.phase { padding:70px 0 30px; border-top:1px solid var(--line); margin-top:50px; position:relative; }
.ghost { position:absolute; top:26px; right:0; font-size:clamp(80px,14vw,150px); font-weight:700;
  color:rgba(242,240,235,.05); line-height:1; user-select:none; }
.window { color:var(--accent); font-size:14px; letter-spacing:.15em; margin-bottom:8px; }
.mood { color:var(--dim); font-size:15.5px; max-width:70ch; margin-top:14px; padding-left:16px;
  border-left:2px solid rgba(232,69,44,.5); }
.talkline { margin-top:16px; font-size:14px; color:var(--gold); }
.talkline b { font-weight:600; }
ul.timeline { list-style:none; margin-top:6px; }
ul.timeline li { padding:13px 0 13px 110px; position:relative; border-bottom:1px solid rgba(242,240,235,.05); font-size:15px; }
ul.timeline li .d { position:absolute; left:0; top:14px; width:95px; color:var(--faint);
  font-size:12.5px; letter-spacing:.03em; }
ul.timeline li b { font-weight:600; color:rgba(242,240,235,.95); }
ul.timeline li .desc { color:var(--dim); font-size:14px; margin-top:3px; }
ul.timeline li .crowd { color:var(--gold); font-size:12.5px; margin-top:3px; opacity:.85; }
.chips { display:flex; gap:8px; flex-wrap:wrap; margin-top:4px; }
.chips span { border:1px solid var(--line); border-radius:12px; padding:6px 14px; font-size:13px; color:var(--dim); line-height:1.6; max-width:100%; }
.pause { background:var(--card); border-radius:10px; padding:18px 22px; margin-top:26px; font-size:14.5px; color:var(--dim); }
.pause b { color:var(--gold); font-weight:600; }
.fa-block { background:rgba(232,69,44,.06); border:1px solid rgba(232,69,44,.22); border-radius:12px;
  padding:22px 26px; margin-top:30px; }
.fa-block h4 { font-size:14px; font-weight:600; letter-spacing:.12em; color:var(--accent); margin-bottom:12px; }
.fa-block .ev { display:flex; gap:14px; font-size:14px; padding:3.5px 0; }
.fa-block .ev .d { color:var(--faint); font-size:12px; min-width:72px; padding-top:2px; }
.fa-block .ev.hero b { color:#fff; }
.fa-block .ev .tier { font-size:10.5px; color:var(--gold); margin-left:6px; letter-spacing:.08em; }
.punch { margin-top:16px; font-size:14.5px; line-height:1.8; color:rgba(242,240,235,.75); border-top:1px dashed rgba(232,69,44,.3); padding-top:14px; }
.punch::before { content:"จุดเล่าที่แรง — "; color:var(--accent); font-weight:600; }
details.sources { margin-top:24px; }
details.sources summary { cursor:pointer; color:var(--faint); font-size:13px; letter-spacing:.06em; }
details.sources ul { list-style:none; margin-top:12px; }
details.sources li { font-size:13px; padding:4px 0; color:var(--dim); }
details.sources a { color:var(--dim); text-decoration:none; border-bottom:1px dotted var(--faint); }
details.sources a:hover { color:var(--fg); }
.cult-block { background:rgba(232,179,76,.05); border:1px solid rgba(232,179,76,.22); border-radius:12px; padding:22px 26px; margin-top:18px; }
.cult-block h4 { font-size:14px; font-weight:600; letter-spacing:.12em; color:var(--gold); margin-bottom:14px; }
.cult-item { padding:10px 0; border-bottom:1px solid rgba(242,240,235,.05); font-size:14px; }
.cult-item:last-child { border-bottom:none; }
.cult-item .cat { display:inline-block; font-size:10.5px; letter-spacing:.08em; color:var(--gold); border:1px solid rgba(232,179,76,.35); border-radius:999px; padding:1px 9px; margin-right:8px; vertical-align:2px; }
.cult-item a { color:rgba(242,240,235,.95); font-weight:600; text-decoration:none; border-bottom:1px dotted var(--faint); }
.cult-item .meta { color:var(--faint); font-size:12.5px; margin-left:8px; }
.cult-item .story { color:var(--dim); margin-top:4px; font-size:13.5px; }
.cult-item .show { color:rgba(232,179,76,.75); margin-top:3px; font-size:12.5px; }
.dead { color:#e8452c; font-size:11px; margin-left:6px; }
.qbox { background:var(--card); border-radius:12px; padding:26px 30px; margin-top:20px; }
.qbox p { margin-bottom:12px; font-size:15px; }
.qbox .q { color:var(--gold); font-weight:600; }
ul.check { list-style:none; margin-top:10px; }
ul.check li { padding:6px 0 6px 30px; position:relative; font-size:14.5px; color:var(--dim); }
ul.check li::before { content:"☐"; position:absolute; left:2px; color:var(--faint); }
footer { margin-top:80px; color:var(--faint); font-size:12.5px; border-top:1px solid var(--line); padding-top:20px; }
</style></head><body><div class="wrap">
<header>
<h1>Timeline การเมืองไทย × ศิลปะปลดแอก<br>2563 – 2569</h1>
<div class="sub">รายงานทีมรีเสิชสำหรับทอล์ค ARTIVISM 2026 ห้องเรียน 4 · จัดทำ 3 ก.ค. 2026<br>
แหล่งอ้างอิงหลัก: TLHR · iLaw · ประชาไท · Mob Data Thailand · Thai PBS · The Standard ฯลฯ</div>
<div class="status">ครบ 6 ช่วง ตรวจเว็บแล้วทุกช่วง — รอทีมมนุษย์ตรวจอีกชั้น</div>
</header>
<nav>""")

parts.append('<a href="#prologue">ราก</a>')
for ph in PHASES:
    parts.append(f'<a href="#p{ph["num"]}">{ph["num"]}. {esc(ph["name"])}</a>')
parts.append('<a href="#quiet">ช่วงเงียบ</a><a href="#check">เช็คลิสต์</a></nav>')

# overview table
parts.append('<h3>ข้อเสนอการแบ่งช่วง</h3><table class="overview"><tr><th>ช่วง</th><th>ชื่อ (เสนอ)</th><th>เวลา</th><th>งานที่เล่าในทอล์ค</th></tr>')
parts.append('<tr><td class="n">ราก</td><td><a href="#prologue">หม้ออัดแรงดัน</a></td><td>รัฐประหาร 57 – มิ.ย. 63</td><td>บริบทเปิด — เชื้อไฟ 6 ปี</td></tr>')
for ph in PHASES:
    parts.append(f'<tr><td class="n">{ph["num"]}</td><td><a href="#p{ph["num"]}">{esc(ph["name"])}</a></td>'
                 f'<td>{esc(ph["window"])}</td><td>{esc(ph["talk"])}</td></tr>')
parts.append('</table>')

pro = periods[6] if len(periods) > 6 else None
parts.append('<section class="phase" id="prologue"><div class="ghost">0</div>'
             '<div class="window">ราก · รัฐประหาร 2557 – มิ.ย. 2563</div>'
             '<h2>หม้ออัดแรงดัน — เชื้อไฟ 6 ปี ก่อนการระเบิด</h2>')
if pro:
    parts.append(f'<div class="mood">{esc(pro["mood"])}</div>')
    parts.append('<h3>เชื้อไฟที่สะสม</h3><ul class="timeline">')
    for e in pro['key_events']:
        crowd = f'<div class="crowd">👥 {esc(e["crowd_estimate"])}</div>' if e.get('crowd_estimate') and e['crowd_estimate'] not in ('—','') else ''
        parts.append(f'<li><span class="d">{thdate(e["date"])}</span><b>{esc(e["name"])}</b>'
                     f'<div class="desc">{esc(e["description"])}</div>{crowd}</li>')
    parts.append('</ul>')
    if pro.get('pauses_or_lulls'):
        parts.append(f'<div class="pause"><b>จังหวะเงียบใต้การกดปราบ:</b> {esc(pro["pauses_or_lulls"])}</div>')
parts.append(cult_html([c for c in culture if c['period_tag'] == 'prologue'], 'งานวัฒนธรรมยุคตั้งเชื้อไฟ (คนอื่นทำ — คัดมาให้เลือกขึ้นจอ)'))
if pro:
    srcs = pro['sources']
    parts.append(f'<details class="sources"><summary>แหล่งอ้างอิง ({len(srcs)})</summary><ul>')
    for s in srcs:
        pub = esc(s.get('publication','')) + ' — ' if s.get('publication') else ''
        parts.append(f'<li>{pub}<a href="{esc(s["url"])}" target="_blank">{esc(s["title"])}</a></li>')
    parts.append('</ul></details>')
parts.append('</section>')

for ph in PHASES:
    pr = periods[ph['pidx'][0]]
    evs = phase_events(ph)
    fas = fa_in(ph)
    parts.append(f'<section class="phase" id="p{ph["num"]}"><div class="ghost">{ph["num"]}</div>')
    parts.append(f'<div class="window">ช่วงที่ {ph["num"]} · {esc(ph["window"])}</div>')
    parts.append(f'<h2>{esc(ph["name"])}</h2>')
    parts.append(f'<div class="mood">{esc(pr["mood"])}</div>')
    parts.append(f'<div class="talkline">งานที่เล่าในทอล์ค: <b>{esc(ph["talk"])}</b></div>')

    parts.append('<h3>การเมืองในช่วงนี้</h3><ul class="timeline">')
    for e in evs:
        crowd = f'<div class="crowd">👥 {esc(e["crowd_estimate"])}</div>' if e.get('crowd_estimate') and e['crowd_estimate'] not in ('—','') else ''
        parts.append(f'<li><span class="d">{thdate(e["date"])}</span><b>{esc(e["name"])}</b>'
                     f'<div class="desc">{esc(e["description"])}</div>{crowd}</li>')
    parts.append('</ul>')

    parts.append('<h3>ประเด็นที่เรียกร้อง</h3><div class="chips">')
    for d in pr['demands']: parts.append(f'<span>{esc(d)}</span>')
    parts.append('</div>')

    parts.append('<h3>รูปแบบการเคลื่อนไหว</h3><div class="chips">')
    for f in pr['forms']: parts.append(f'<span>{esc(f)}</span>')
    parts.append('</div>')

    if pr.get('pauses_or_lulls'):
        parts.append(f'<div class="pause"><b>จังหวะแผ่ว/หยุดของขบวน:</b> {esc(pr["pauses_or_lulls"])}</div>')

    parts.append(f'<div class="fa-block"><h4>ศิลปะปลดแอก ในช่วงนี้ — {len(fas)} events</h4>')
    for e in fas:
        hero = ' hero' if e['tier'] == 'hero' else ''
        tier = f'<span class="tier">{e["tier"].upper()}</span>' if e['tier'] == 'hero' else ''
        parts.append(f'<div class="ev{hero}"><span class="d">{thdate(e["date"])}</span><span><b>{esc(e["name"])}</b>{tier}</span></div>')
    parts.append(f'<div class="punch">{esc(ph["punch"])}</div></div>')
    parts.append(cult_html(cult_in(CULT_TAG[ph['num']]), 'งานวัฒนธรรมร่วมยุค (คนอื่นทำ — คัดมาให้เลือกขึ้นจอ)'))

    srcs = pr['sources']
    parts.append(f'<details class="sources"><summary>แหล่งอ้างอิง ({len(srcs)})</summary><ul>')
    for s in srcs:
        pub = esc(s.get('publication','')) + ' — ' if s.get('publication') else ''
        parts.append(f'<li>{pub}<a href="{esc(s["url"])}" target="_blank">{esc(s["title"])}</a></li>')
    parts.append('</ul></details></section>')

parts.append("""
<section class="phase" id="quiet"><div class="window">คำถามสำคัญ</div>
<h2>ช่วงเงียบของ Free Arts — ข้อมูลตอบไม่ได้ พวกเราต้องตอบเอง</h2>
<div class="qbox">
<p><span class="q">1. พ.ค. – ต.ค. 2567 (หลังบุ้งเสียชีวิต):</span> เงียบ 5 เดือน — เหนื่อย? เศร้า? ไม่รู้จะทำอะไร? หรือชีวิตส่วนตัวเรียกร้อง?</p>
<p><span class="q">2. ธ.ค. 2567 – มิ.ย. 2568:</span> เงียบ 6 เดือน ยาวที่สุดใน 5 ปี — ขณะที่การเมืองระดับบนกำลังระส่ำ อะไรทำให้กลับมาตอน 24 มิถุนา 2568?</p>
<p style="color:var(--dim); font-size:14px;">สองช่วงนี้คือเนื้อทอล์คที่มีค่าที่สุดถ้าเล่าตรงๆ — คนฟังไม่เคยได้ยินกลุ่มศิลปะเล่าเรื่อง "การหยุด" ของตัวเอง</p>
</div></section>

<section class="phase" id="check"><div class="window">ก่อนใช้จริง</div>
<h2>รายการตรวจสอบสำหรับทีมมนุษย์</h2>
<ul class="check">
<li>ตัวเลขผู้ชม Voter Concert — สื่อไม่ระบุ ถ้ามีตัวเลขภายในให้ใช้ของเรา</li>
<li>ชื่อช่วงทั้ง 6 เป็นแค่ข้อเสนอ — ตั้งใหม่ได้เลย ควรเป็นภาษาของพวกเราเอง</li>
<li>เช็คว่างานไหนของ Free Arts อยู่ผิดช่วง (จัดตามวันที่ใน events.json)</li>
<li>เหตุผลช่วงเงียบ 2 ช่วง (หัวข้อด้านบน)</li>
</ul></section>

<footer>ไฟล์ประกอบ: research-data.json (ข้อมูลดิบ + แหล่งอ้างอิงทั้งหมด) · freearts-events.txt (timeline 70 events) · research-timeline.md (ฉบับ markdown)<br>
จัดทำโดยทีมรีเสิช AI 6 คน (การเมือง) + 7 คน (วัฒนธรรม) + เรียบเรียงโดย Claude — สถานะ: draft รอทีมมนุษย์ตรวจ</footer>
</div></body></html>""")

out = '\n'.join(parts)
open('/Users/cudo/Desktop/Artivism/site/index.html','w').write(out)
print('written', len(out), 'chars')
