# -*- coding: utf-8 -*-
import csv, html, re, unicodedata, json
exec(open('page.py',encoding='utf-8').read().split("CITIES =")[0])
from spots import SPOTS
from ko import ko
from mine_dish import MINE_DISH
from notes_guide import G as GNOTE
from syn import expand
import os
PL_EUR = {1:'~€12', 2:'~€20', 3:'~€35', 4:'~€60'}
ENR = json.load(open('enrich.json',encoding='utf-8')) if os.path.exists('enrich.json') else {}
MC  = json.load(open('mine_coords.json',encoding='utf-8'))

E = html.escape
def norm(s):
    s = unicodedata.normalize('NFKD', s or '').encode('ascii','ignore').decode().lower()
    return re.sub(r'[^a-z0-9]','',s)

CITY = {'Barcelona':'바르셀로나','Lisbon':'리스본','Lisboa':'리스본','Porto':'포르투'}
recs = []

# --- source 1: 내가 가본 곳
for cname, items in [('바르셀로나',BCN),('리스본',LIS),('포르투',POR)]:
    for n,pid,cat,r,rc,pr,ad,note in items:
        mc = MC.get(n+'|'+cname, {})
        pnum = {'€':'~€12','€€':'~€22','€€€':'~€40','€€€€':'~€70'}.get(pr,'')
        recs.append(dict(src='mine', city=cname, name=n, cat=cat,
                         meta=[cat, '★%.1f'%r] + ([pnum] if pnum else []),
                         addr=ad, note=note, badges=[], dish=MINE_DISH.get(n,''), url=gurl(n,pid,cname),
                         lat=mc.get('lat'), lng=mc.get('lng')))

seen = {(norm(x['name']), x['city']) for x in recs}

def award_badges(mich, repsol):
    b = []
    if mich == 'Bib Gourmand': b.append('빕구르망')
    elif mich == 'Selected': b.append('미슐랭 셀렉티드')
    if repsol: b.append('레스폴 ' + repsol)
    return b

# --- source 2: 미슐랭 · 레스폴
for _gi, row in enumerate(csv.DictReader(open('all-cities-full.csv',encoding='utf-8'))):
    c = CITY[row['City']]
    k = (norm(row['Name']), c)
    if k in seen: continue
    seen.add(k)
    price = row['Avg_Price_EUR'].strip()
    addr = re.sub(r',\s*(Spain|Portugal)\s*$', '', row['Address'].strip())
    addr = re.sub(r',\s*\d{4,5}(-\d{3})?\s*$', '', addr)
    e = ENR.get(row['Name']+'|'+c, {})
    gn = GNOTE.get(_gi, ('',''))
    _e0 = ENR.get(row['Name']+'|'+CITY[row['City']], {})
    _dish = _e0.get('dish') or gn[0]
    meta = [x for x in [ko(row['Cuisine']), ('★%.1f'%e['rating'] if e.get('rating') else ''),
                        ('€'+price if price else ''), e.get('closed','')] if x]
    recs.append(dict(src='guide', city=c, name=row['Name'], cat=ko(row['Cuisine']),
                     meta=meta, addr=e.get('addr') or addr, note=_e0.get('note') or gn[1], dish=_dish,
                     badges=award_badges(row['Michelin_Award'].strip(), row['Repsol_Award'].strip()),
                     url=row['Maps_Url'].strip(), lat=e.get('lat'), lng=e.get('lng')))

# --- source 3: 현지 가이드 (BCBM)
for row in csv.DictReader(open('bcbm-lisboa-porto.csv',encoding='utf-8')):
    c = CITY[row['City']]
    k = (norm(row['Name']), c)
    if k in seen: continue
    seen.add(k)
    price = row['Avg_Price_EUR'].strip()
    cat = ko(row['Main_Menu']) or ko(row['Google_Category'])
    e = ENR.get(row['Name']+'|'+c, {})
    pstr = ('€'+price) if price else PL_EUR.get(e.get('pl') or 0,'')
    meta = [x for x in [cat, ('★%.1f'%e['rating'] if e.get('rating') else ''),
                        pstr, e.get('closed','')] if x]
    recs.append(dict(src='local', city=c, name=row['Name'], cat=cat, meta=meta,
                     addr=e.get('addr',''), note=e.get('note',''), dish=e.get('dish',''),
                     badges=award_badges(row['Michelin_Award'].strip(), ''),
                     url=row['Maps_Url'].strip(), lat=e.get('lat'), lng=e.get('lng')))

SRC = [('mine','내가 가본 곳'),('guide','미슐랭 · 레스폴'),('local','현지 가이드'),('near','내 주변')]
CITIES = [('바르셀로나','bcn','#B4472C'),('리스본','lis','#1E6A8D'),('포르투','por','#7A2E45')]
CSLUG = {c:s for c,s,_ in CITIES}
for r in recs: r['cslug'] = CSLUG[r['city']]

n_src = {s:sum(1 for r in recs if r['src']==s) for s,_ in SRC}
n_src['near'] = sum(1 for r in recs if r.get('lat'))
n_city = {s:sum(1 for r in recs if r['cslug']==s) for _,s,_ in CITIES}

def card(r):
    meta = ' · '.join(r['meta'])
    bd = ''.join('<span class="bg">%s</span>'%E(b) for b in r['badges'])
    _base = (r['name']+' '+r['cat']+' '+r['addr']+' '+r['note']+' '+r.get('dish','')+' '
             +' '.join(r['badges']))
    q = E((_base+' '+expand(_base)).lower())
    ll = ' data-lat="%s" data-lng="%s"'%(r['lat'],r['lng']) if r.get('lat') else ''
    o = ['<article class="p" data-src="%s" data-city="%s" data-q="%s"%s><span class="ds"></span>'%(r['src'],r['cslug'],q,ll)]
    o.append('<a class="nm" href="%s" target="_blank" rel="noopener">%s</a>%s'%(E(r['url']),E(r['name']),bd))
    if meta: o.append('<p class="mt">%s</p>'%E(meta))
    if r['addr']: o.append('<p class="ad">%s</p>'%E(r['addr']))
    if r.get('dish'): o.append('<p class="dh">%s</p>'%E(r['dish']))
    if r['note']: o.append('<p class="nt">%s</p>'%E(r['note']))
    o.append('</article>')
    return ''.join(o)

body = []
for cname, cslug, col in CITIES:
    body.append('<section class="city" data-city="%s"><h2><span class="dot" style="background:%s"></span>%s <span class="ct"></span></h2>'%(cslug,col,E(cname)))
    body += [card(r) for r in recs if r['cslug']==cslug]
    body.append('</section>')
body = '\n'.join(body)

chips_src = ''.join('<button class="chip" data-s="%s" aria-pressed="%s">%s <b>%d</b></button>'
                    %(s,'true' if i==0 else 'false',E(l),n_src[s]) for i,(s,l) in enumerate(SRC))
GAZ = [{'n':l,'a':al,'c':c,'lat':la,'lng':ln} for c,l,al,la,ln in SPOTS] + \
      [{'n':r['name'],'a':(r['addr'] or '').lower(),'c':r['cslug'],'lat':r['lat'],'lng':r['lng']}
       for r in recs if r.get('lat')]
# 주소에서 거리 이름을 뽑아 좌표 평균으로 추가
_st = {}
for r in recs:
    if not r.get('lat') or not r.get('addr'): continue
    street = re.split(r'\s+\d', r['addr'].split(',')[0].strip(), 1)[0].strip(' .,')
    if len(street) < 5: continue
    _st.setdefault((street, r['cslug']), []).append((float(r['lat']), float(r['lng'])))
for (street, cs), pts in _st.items():
    GAZ.append({'n': street, 'a': street.lower(), 'c': cs,
                'lat': sum(p[0] for p in pts)/len(pts), 'lng': sum(p[1] for p in pts)/len(pts)})
gaz_json = json.dumps(GAZ, ensure_ascii=False)
spot_opts = ''.join('<option value="%s">'%html.escape(g['n']) for g in GAZ)
chips_city = '<button class="chip" data-f="all" aria-pressed="true">전체</button>' + ''.join(
    '<button class="chip" data-f="%s" aria-pressed="false">%s <b>%d</b></button>'%(s,E(c),n_city[s]) for c,s,_ in CITIES)

doc = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>바르셀로나 · 리스본 · 포르투</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{--paper:#FCFBF7;--ink:#16191D;--dim:#6B6F76;--line:#E2DED3;--blue:#1E4E8C}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.6 Inter,-apple-system,BlinkMacSystemFont,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:640px;margin:0 auto;padding:0 20px 64px}
header{padding:44px 0 20px}
h1{font:600 34px/1.15 Fraunces,Georgia,serif;margin:0 0 10px;letter-spacing:-.01em}
.sub{margin:0;color:var(--dim);font-size:15px}
.bar{position:sticky;top:0;background:var(--paper);padding:12px 0 14px;border-bottom:1px solid var(--line);z-index:5}
input[type=search]{width:100%;padding:11px 14px;font:400 16px Inter,sans-serif;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:8px;-webkit-appearance:none}
input[type=search]:focus{outline:2px solid var(--blue);outline-offset:1px;border-color:transparent}
.chips{display:flex;gap:7px;margin-top:10px;flex-wrap:wrap}
.chip{font:400 14px Inter,sans-serif;padding:6px 13px;border:1px solid var(--line);background:#fff;border-radius:999px;color:var(--dim);cursor:pointer}
.chip b{font-weight:400;opacity:.6;margin-left:2px}
.chip[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.chip:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
.chips.sub-row .chip{font-size:13px;padding:5px 11px}
h2{font:600 15px/1 Inter,sans-serif;margin:34px 0 0;padding-bottom:12px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:9px}
.dot{width:9px;height:9px;border-radius:50%;flex:none}
.ct{color:var(--dim);font-weight:400}
.p{padding:16px 0;border-bottom:1px solid var(--line)}
.nm{font:600 20px/1.35 Fraunces,Georgia,serif;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--blue);padding-bottom:1px}
.nm:hover,.nm:focus-visible{color:var(--blue)}
.bg{display:inline-block;margin-left:8px;font:500 11px/1 Inter,sans-serif;letter-spacing:.02em;padding:4px 7px;border:1px solid var(--line);border-radius:4px;color:var(--dim);vertical-align:3px;white-space:nowrap}
.mt,.ad{margin:7px 0 0;font-size:14px;color:var(--dim)}
.ad{margin-top:2px}
.dh{margin:8px 0 0;font-size:14px;color:var(--blue)}
.nt{margin:5px 0 0;font-size:15px}
.city[hidden],.p[hidden]{display:none}
.ds{float:right;font:500 13px Inter,sans-serif;color:var(--blue);margin-top:5px}
#spot{width:100%;margin-top:10px;padding:11px 14px;font:400 16px Inter,sans-serif;background:#fff;border:1px solid var(--line);border-radius:8px;color:var(--ink);-webkit-appearance:none}
#spot:focus{outline:2px solid var(--blue);outline-offset:1px;border-color:transparent}
#hit{margin:8px 0 0;font-size:13px;color:var(--dim);min-height:18px}
.none{color:var(--dim);padding:28px 0;font-size:15px}
footer{margin-top:40px;font-size:14px;color:var(--dim);line-height:1.7}
@media(max-width:420px){h1{font-size:28px}.nm{font-size:18px}}
</style></head><body><div class="wrap">
<header><h1>바르셀로나 · 리스본 · 포르투</h1>
<p class="sub">가게 이름을 누르면 구글 지도가 열립니다.</p></header>
<div class="bar">
<input type="search" id="q" placeholder="가게 이름, 음식, 동네로 찾기" aria-label="검색">
<div class="chips" role="group" aria-label="출처">__SRC__</div>
<div class="chips sub-row" role="group" aria-label="도시">__CITY__</div>
<div id="near" hidden>
<input id="spot" list="gaz" autocomplete="off" placeholder="현재 위치 — 건물, 관광지, 지하철역, 거리 이름, 좌표">
<datalist id="gaz">__SPOTS__</datalist>
<p id="hit"></p>
<div class="chips sub-row" role="group" aria-label="반경">
<button class="chip r" data-r="500" aria-pressed="false">500m</button>
<button class="chip r" data-r="1000" aria-pressed="true">1km</button>
<button class="chip r" data-r="2000" aria-pressed="false">2km</button>
<button class="chip r" data-r="0" aria-pressed="false">전체</button>
</div></div>
</div>
__BODY__
<p class="none" id="none" hidden>결과가 없습니다.</p>
<footer>평점·가격·영업시간은 저장 시점 기준이라 바뀔 수 있어요. 정확한 정보는 이름을 눌러 구글 지도에서 확인하세요. 가격은 1인 기준이며, ~ 표시는 추정치입니다.</footer>
</div>
<script>
var q=document.getElementById('q'),secs=[].slice.call(document.querySelectorAll('.city')),
 none=document.getElementById('none'),src='mine',city='all',
 nearBox=document.getElementById('near'),spot=document.getElementById('spot'),
 hit=document.getElementById('hit'),GAZ=__GAZ__,rad=1000,o=null,
 sc=[].slice.call(document.querySelectorAll('[data-s]')),cc=[].slice.call(document.querySelectorAll('[data-f]')),
 rc=[].slice.call(document.querySelectorAll('.r')),all=[].slice.call(document.querySelectorAll('.p'));
function dist(a,b,c,d){var R=6371000,p=Math.PI/180,x=(c-a)*p,y=(d-b)*p,
 h=Math.sin(x/2)*Math.sin(x/2)+Math.cos(a*p)*Math.cos(c*p)*Math.sin(y/2)*Math.sin(y/2);
 return 2*R*Math.asin(Math.sqrt(h));}
function fmt(m){return m<1000?Math.round(m/10)*10+'m':(m/1000).toFixed(1)+'km';}
function norm(x){return (x||'').toLowerCase().replace(/[^a-z0-9가-힣]/g,'');}
function resolve(txt){
 var t=(txt||'').trim(); if(!t)return {o:null,msg:''};
 var m=t.match(/^\s*(-?\d+\.\d+)\s*,\s*(-?\d+\.\d+)\s*$/);
 if(m)return {o:[parseFloat(m[1]),parseFloat(m[2])],msg:'좌표 기준'};
 var k=norm(t),exact=null,part=null;
 for(var i=0;i<GAZ.length;i++){var g=GAZ[i];
  if(norm(g.n)===k){exact=g;break;}
  if(!part&&(norm(g.n).indexOf(k)>-1||norm(g.a).indexOf(k)>-1))part=g;}
 var g=exact||part;
 if(!g)return {o:null,msg:'\u2018'+t+'\u2019 을(를) 못 찾았어요. 동네 이름이나 가게 이름을 입력하거나, 구글 지도에서 좌표를 복사해 붙여넣으세요.'};
 return {o:[g.lat,g.lng],msg:g.n+' 기준'};}
var CACHE={},pending=null,lastQ='';
function lookup(t){
 if(CACHE[t]!==undefined){if(CACHE[t]){o=CACHE[t];run();}return;}
 if(lastQ===t)return; lastQ=t;
 clearTimeout(pending);
 pending=setTimeout(function(){
  hit.textContent='지도에서 찾는 중\u2026';
  var url='https://nominatim.openstreetmap.org/search?format=json&limit=1&accept-language=ko'
   +'&viewbox=-9.28,38.82,-8.55,41.25&q='+encodeURIComponent(t+', Portugal Espanha');
  fetch(url).then(function(r){return r.json();}).then(function(j){
   if(!j||!j.length){CACHE[t]=null;
    hit.textContent='\u2018'+t+'\u2019 을(를) 못 찾았어요. 다른 이름으로 해보거나 구글 지도 좌표를 붙여넣으세요.';return;}
   var g=[parseFloat(j[0].lat),parseFloat(j[0].lon)];CACHE[t]=g;
   var nm=(j[0].display_name||t).split(',').slice(0,2).join(', ');
   hit.textContent=nm+' 기준 (온라인 검색)';o=g;
   var sv=spot.value.trim(); if(sv===t)draw();
  }).catch(function(){CACHE[t]=null;
   hit.textContent='온라인 검색에 실패했어요. 인터넷 연결을 확인하거나 좌표를 붙여넣으세요.';});
 },600);}
function run(){var near=src==='near';
 nearBox.hidden=!near; o=null;
 if(near){var res=resolve(spot.value);o=res.o;
  if(res.msg)hit.textContent=res.msg;
  if(!o&&spot.value.trim().length>1)lookup(spot.value.trim());}
 draw();}
function draw(){var t=q.value.trim().toLowerCase(),tot=0,near=src==='near';
 all.forEach(function(p){p.__d=null;
  if(near&&o&&p.dataset.lat){p.__d=dist(o[0],o[1],+p.dataset.lat,+p.dataset.lng);}});
 secs.forEach(function(s){var v=0;
  [].slice.call(s.querySelectorAll('.p')).forEach(function(p){
   var ok;
   if(near){ok=o!==null&&p.__d!==null&&(rad===0||p.__d<=rad);}
   else{ok=p.dataset.src===src&&(city==='all'||p.dataset.city===city);}
   if(ok&&t&&p.dataset.q.indexOf(t)<0)ok=false;
   p.hidden=!ok;
   p.querySelector('.ds').textContent=(near&&ok&&p.__d!==null)?fmt(p.__d):'';
   if(ok){v++;tot++;}});
  if(near&&v){var box=s,ps=[].slice.call(s.querySelectorAll('.p')).filter(function(p){return !p.hidden;});
   ps.sort(function(a,b){return a.__d-b.__d;}).forEach(function(p){box.appendChild(p);});}
  s.querySelector('.ct').textContent=v||''; s.hidden=v===0;});
 none.hidden=tot>0;
 none.textContent=(near&&!o)?'현재 위치를 입력해 주세요. 동네, 지하철역, 관광지, 건물 이름 다 됩니다.':'결과가 없습니다.';
 if(near&&!o)none.hidden=false;}
sc.forEach(function(b){b.onclick=function(){sc.forEach(function(x){x.setAttribute('aria-pressed',x===b);});src=b.dataset.s;run();};});
cc.forEach(function(b){b.onclick=function(){cc.forEach(function(x){x.setAttribute('aria-pressed',x===b);});city=b.dataset.f;run();};});
rc.forEach(function(b){b.onclick=function(){rc.forEach(function(x){x.setAttribute('aria-pressed',x===b);});rad=+b.dataset.r;run();};});
spot.addEventListener('input',run); spot.addEventListener('change',run); q.addEventListener('input',run); run();
</script></body></html>"""

out = doc.replace('__GAZ__',gaz_json).replace('__SPOTS__',spot_opts).replace('__SRC__',chips_src).replace('__CITY__',chips_city).replace('__BODY__',body)
open('/mnt/user-data/outputs/여행_맛집_지도.html','w',encoding='utf-8').write(out)

with open('/mnt/user-data/outputs/여행_맛집_전체.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(['출처','도시','이름','분류','인증','가격','주소','메모','구글지도'])
    lab={'mine':'내가 가본 곳','guide':'미슐랭·레스폴','local':'현지 가이드'}
    for r in recs:
        w.writerow([lab[r['src']],r['city'],r['name'],r['cat'],' / '.join(r['badges']),
                    ' · '.join(r['meta']),r['addr'],r['note'],r['url']])
print(len(recs), n_src, n_city)
