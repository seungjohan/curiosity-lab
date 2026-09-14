# -*- coding: utf-8 -*-
import csv, html, json
from urllib.parse import quote

CITY_EN = {'바르셀로나':'Barcelona Spain','리스본':'Lisbon Portugal','포르투':'Porto Portugal'}

def gurl(name, pid, cityname):
    return ('https://www.google.com/maps/search/?api=1&query='
            + quote(name + ' ' + CITY_EN[cityname]) + '&query_place_id=' + pid)

# name, pid, cat, rating, reviews, price, addr, note
BCN = [
("Disfrutar","ChIJTSzGu4WipBIRkznre9Zwis0","파인다이닝",4.8,3794,"€€€€","Carrer de Villarroel 163, Eixample","미슐랭 3스타. 세계 50 베스트 1위(2024). 예약 12개월 전 오픈. 토·일 휴무"),
("Hisop","ChIJx2nrT5yipBIRcT4_prXJJck","파인다이닝",4.5,1386,"€€€€","Passatge de Marimon 9, Sant Gervasi","미슐랭 1스타. 코스 약 €100으로 스타 중 가장 저렴한 편. 일요일 휴무"),
("Bar Pimentel","ChIJ8XLoZiyjpBIRSFg13se5ncQ","타파스",4.5,1803,"€€","Carrer dels Carders 11, El Born","크로케타가 유명. 예약 안 하면 대기"),
("Bar Colom","ChIJb2HVzleipBIRsd7SIU8GRmE","타파스·파에야",4.7,36631,"€€","Carrer dels Escudellers 33, 고딕지구","예약 안 받음. 저녁엔 30분씩 줄. 해산물 파에야"),
("Ciutat Comtal","ChIJmSmV-_KipBIR1rXbKL9Yhp4","타파스",4.4,23323,"€€","Rambla de Catalunya 18","푸아그라 올린 소고기 타파스. 새벽 1시까지"),
("La Flauta","ChIJbUeDbIyipBIRhf2n9OIXpig","타파스",4.5,13245,"€€","Carrer d'Aribau 23","현지인 비중 높음. 감자 오믈렛. 일요일 휴무"),
("Tapa Tapa","ChIJC2uTpZeipBIR89h7dQLu61k","타파스",4.3,16166,"€€","Pg. de Gràcia 44","카사 바트요 바로 앞. 먹물 파에야. 아침 8시부터"),
("3 Focs","ChIJqbtM4o2ipBIRrMyfwmj0UA4","그릴",4.6,9267,"€€","Carrer de València 207","숯불 스테이크와 구운 야채. 4인 €85 정도"),
("Lomo Alto","ChIJ5YTN_OyipBIRevrlp03RoAY","스테이크",4.3,3181,"€€€","Carrer d'Aragó 285","숙성 소고기 전문. 60~180일 숙성 중 선택"),
("Barceloneta","ChIJ6_dLhqujpBIRMs68zrFMqSc","해산물",4.4,9255,"€€€€","Carrer de l'Escar 22, Port Vell","항구 뷰. 농어구이와 굴. 옷차림 신경쓸 것"),
("Luigi Ristorante","ChIJefmo1-2ipBIRBr5cUyZ1Qt0","이탈리안",4.4,7274,"€€","Carrer de Roger de Llúria 50","피자와 파스타. 테라스 있음"),
("Honest Greens","ChIJnx1hjdyjpBIR4nH2Pz1ry10","샐러드",4.5,12483,"€€","Rambla de Catalunya 3","채식 옵션 많음. 앱으로 주문하면 줄 안 서도 됨"),
("LA PAPA","ChIJnSeRvgWjpBIRRcG2xbaFLJ4","브런치",4.6,3290,"€€","Carrer d'Aribau 92","시나몬롤. 오후 6시까지만"),
("Jon Cake","ChIJEUD1q-ijpBIRUoUk9GGIAAs","디저트",4.5,4734,"€","Carrer de Sant Pere Més Baix 36","바스크 치즈케이크. 고르곤졸라 맛 추천. 대기 김"),
("99 cheesecake","ChIJr9gtDACjpBIR--1V1IfFwoM","디저트",4.6,1992,"€","Carrer d'Aribau 42","치즈케이크 €0.99, 토핑 €0.80. 테이크아웃만"),
("Xurreria Laietana","ChIJw-m_F_qipBIRMyqWzvfxE-c","츄러스",4.7,5462,"€","Via Laietana 46","츄러스 6개 + 핫초코 €5. 앉을 자리 거의 없음"),
("DelaCrem","ChIJ3TMuUYyipBIRr5QWiKg3WQA","젤라토",4.6,8335,"€","Carrer d'Enric Granados 15","두 가지 맛 €3.90부터. 밤 12시 반까지"),
("Lucciano's","ChIJp0KWj5ajpBIR2fQkRm3QBmk","젤라토",4.5,5087,"€","Gran Via 601","새벽 1시까지. 피스타치오"),
]
LIS = [
("Pastéis de Belém","ChIJW3H9LkXLHg0RZZZttMb27_8","에그타르트",4.6,99984,"€","R. de Belém 84-92","1837년 원조. 왼쪽 테이크아웃 줄이 빠름. 매일 8-22시"),
("Time Out Market","ChIJdWBeWYc0GQ0RktxySU7hjxM","푸드코트",4.4,75597,"€€€","Mercado da Ribeira, Av. 24 de Julho","유명 셰프 스톨 모음. 자리 잡기가 관건. 매일 10-24시"),
("Uma Marisqueira","ChIJU0ckwHg0GQ0RGFRTQgsiyxU","해산물",4.6,26994,"€€€","R. dos Sapateiros 177","해산물밥(arroz de marisco). 조리 20분. 예약 권장"),
("Pinóquio","ChIJQUcK2oAzGQ0R5g3QY_kRlTc","해산물",4.3,6018,"€€€","Praça dos Restauradores 79","마늘새우와 조개. 서비스 빠름"),
("O Coradinho","ChIJgWKYjoIzGQ0R7LGjS4xyhdQ","가정식",4.4,952,"€€","R. de Santa Marta 4","현지인 타스카. 메뉴 매일 바뀜. 문어구이 €12. 일요일 휴무"),
("O Cartaxinho","ChIJT5KXkIIzGQ0Rs7pfHP_FKno","가정식",4.4,1204,"€€","R. de Santa Marta 20B","점심엔 직장인으로 꽉 참. 조개 돼지고기. 토요일 휴무"),
("Palácio Chiado","ChIJNbReWH40GQ0RcUjkcqCogWI","레스토랑",4.4,4058,"€€€€","R. do Alecrim 70","19세기 궁전 건물. 문어 요리. 예약 필수"),
("Mano a Mano","ChIJF8m_1j01GQ0RXhkirJLcKco","이탈리안",4.5,2431,"€€€","R. do Alecrim 22","프로슈토 루꼴라 피자"),
("Han Table Barbecue","ChIJVRlRmgYxGQ0RQjFzIYv_ekU","한식",4.9,20698,"€€€","R. da Pimenta 5, Expo","리스본 평점 최상위. 이베리코 8종 양념구이. 예약 권장"),
("K-BOB","ChIJdyHHRpkzGQ0RXiTLjLchJps","한식",4.5,1529,"€€€","Avenida Ressano Garcia 41A","김치찌개, 김밥, 치킨. 월요일 휴무"),
("Nicolau","ChIJj7fHtnk0GQ0RmaMk-MWsx_I","브런치",4.5,11121,"€€","R. de São Nicolau 17","잉글리시 브렉퍼스트. 바이샤 한복판"),
("Amélia","ChIJz7Mew2YzGQ0RqC8D468aEjk","브런치",4.6,9078,"€€","R. Ferreira Borges 101","온실 같은 인테리어. 프렌치토스트. 뒷마당 자리"),
("A Brasileira","ChIJ6QQiHX80GQ0RU5XEIRyTjvQ","카페",4.2,10421,"€","R. Garrett 120","1905년 시아두 명물. 페소아 동상 앞 테라스. 매일 8-24시"),
("Café da Garagem","ChIJOSikPogzGQ0RjbLAaULrSZ0","카페·전망",4.2,1369,"€","Costa do Castelo 75","극장 안 숨은 카페. 그라사 전망. 월·화 휴무"),
("Quiosque Ribeira das Naus","ChIJN-XUX3w0GQ0Rf5T09qdrY54","강변 키오스크",4.2,4767,"€","Av. Ribeira das Naus 5","테주강변 야외석. 포르투 토닉. 매일 11-23시"),
("Park Rooftop","ChIJTRo64mU1GQ0RfEYk1nPW13c","루프탑 바",4.0,3277,"€€","Calçada do Combro 58","주차장 건물 5층. 엘리베이터 타고 올라감. 일요일 휴무"),
("A Padaria Portuguesa","ChIJcwL3DAozGQ0RfDyynR4w0F8","베이커리",4.0,2916,"€€","Av. da República 39B","커피+생오렌지주스 포함 조식 €3-5. 아침 7시부터"),
("Choupana Caffe","ChIJ0-54YrAzGQ0RD7v_jVeuV9Q","카페",3.4,53,"€€","Rua Prof. Fernando da Fonseca","크루아상으로 유명했던 곳. 경기장 안으로 이전"),
("Jeronymo","ChIJ_WP7RMcxGQ0Rza8w2lrdHRs","카페",3.6,793,"€€","Estação do Oriente, Loja G212","오리엔트역 안. 아침 6시 반부터. 기차 전 간단히"),
("Geladaria Surf","ChIJC8H_fKMzGQ0RCRLPaBvPc4Q","젤라토",4.2,792,"€","Av. Manuel da Maia 56","자정까지"),
("Woori 한국마트","ChIJj25b8SIzGQ0RffMx8O1jq1Q","마트",4.7,245,"","R. Artilharia 1 20a","리스본 최고 한국 식료품점. 수제 김치. 일요일 휴무"),
("KoPo Mart","ChIJcRzc6rQ1GQ0Re1qtla-Bl4g","마트",4.6,214,"","Av. Infante Santo 58D","한국 식료품. 일요일 휴무"),
("Galveias 궁전 도서관","ChIJsZGRp6czGQ0RpQfsX8qX-cg","도서관",4.7,469,"","Campo Pequeno","궁전 건물. 뒷마당 카페가 좋음. 주말 휴관"),
("Biblioteca do INA","ChIJR2BNayI1GQ0RCwBhnVfm_sg","도서관",5.0,2,"","Rua da Alfândega 5","오전·오후 개관 시간이 다름. 주말 휴관"),
("Spacio Shopping","ChIJh4tkhDEyGQ0RuhCPYtdrnyg","쇼핑몰",4.2,14059,"","R. Cidade de Bolama 4","주차 2시간 무료. 매일 10-23시"),
]
POR = [
("Tapabento S.Bento","ChIJwbK6ceRkJA0R_zPMrOhZmgk","타파스",4.6,6472,"€€€","R. da Madeira 221","상 벤투역 옆. 대구 크로켓, 돼지목살 타코. 예약 필수. 월·화 휴무"),
("Espaço Porto Cruz","ChIJG0x3Sd5kJA0Rw3KjhuOoSMg","포트와인 바",4.4,4105,"€€€","Largo Miguel Bombarda 23, Gaia","강 건너 가이아. 루프탑 노을 뷰. 월요일 휴무"),
]

CITIES = [("바르셀로나","bcn","#B4472C",BCN),("리스본","lis","#1E6A8D",LIS),("포르투","por","#7A2E45",POR)]
E = html.escape

rows=[]
for cname,slug,color,items in CITIES:
    for n,pid,cat,r,rc,pr,ad,note in items:
        rows.append(dict(city=cname,slug=slug,color=color,name=n,pid=pid,cat=cat,
                         rating=r,rc=rc,price=pr,addr=ad,note=note))

def sec(cname,slug,color,items):
    o=['<section class="city" data-city="%s">'%slug]
    o.append('<h2><span class="dot" style="background:%s"></span>%s <span class="ct">%d</span></h2>'%(color,E(cname),len(items)))
    for n,pid,cat,r,rc,pr,ad,note in items:
        meta=' · '.join(x for x in [E(cat), ('★ %.1f'%r), pr] if x)
        o.append('<article class="p" data-q="%s">'
                 '<a class="nm" href="%s" target="_blank" rel="noopener">%s</a>'
                 '<p class="mt">%s</p><p class="ad">%s</p><p class="nt">%s</p></article>'
                 %(E((n+' '+cat+' '+ad+' '+note).lower()),E(gurl(n,pid,cname)),E(n),meta,E(ad),E(note)))
    o.append('</section>')
    return '\n'.join(o)

body='\n'.join(sec(c,s,col,i) for c,s,col,i in CITIES)

doc = """<!DOCTYPE html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>바르셀로나 · 리스본 · 포르투 저장 목록</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{--paper:#FCFBF7;--ink:#16191D;--dim:#6B6F76;--line:#E2DED3;--blue:#1E4E8C}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.6 Inter,-apple-system,BlinkMacSystemFont,sans-serif;-webkit-font-smoothing:antialiased}
.wrap{max-width:640px;margin:0 auto;padding:0 20px 64px}
header{padding:44px 0 22px}
h1{font:600 34px/1.15 Fraunces,Georgia,serif;margin:0 0 10px;letter-spacing:-.01em}
.sub{margin:0;color:var(--dim);font-size:15px}
.sub a{color:var(--blue)}
.bar{position:sticky;top:0;background:var(--paper);padding:12px 0;border-bottom:1px solid var(--line);z-index:5}
input[type=search]{width:100%;padding:11px 14px;font:400 16px Inter,sans-serif;color:var(--ink);background:#fff;border:1px solid var(--line);border-radius:8px;-webkit-appearance:none}
input[type=search]:focus{outline:2px solid var(--blue);outline-offset:1px;border-color:transparent}
.chips{display:flex;gap:8px;margin-top:10px;flex-wrap:wrap}
.chip{font:400 14px Inter,sans-serif;padding:6px 14px;border:1px solid var(--line);background:#fff;border-radius:999px;color:var(--dim);cursor:pointer}
.chip[aria-pressed=true]{background:var(--ink);border-color:var(--ink);color:var(--paper)}
.chip:focus-visible{outline:2px solid var(--blue);outline-offset:2px}
h2{font:600 15px/1 Inter,sans-serif;margin:34px 0 0;padding-bottom:12px;border-bottom:1px solid var(--line);display:flex;align-items:center;gap:9px}
.dot{width:9px;height:9px;border-radius:50%;flex:none}
.ct{color:var(--dim);font-weight:400}
.p{padding:16px 0;border-bottom:1px solid var(--line)}
.nm{font:600 20px/1.3 Fraunces,Georgia,serif;color:var(--ink);text-decoration:none;border-bottom:1px solid var(--blue);padding-bottom:1px}
.nm:hover,.nm:focus-visible{color:var(--blue)}
.mt{margin:7px 0 0;font-size:14px;color:var(--dim)}
.ad{margin:2px 0 0;font-size:14px;color:var(--dim)}
.nt{margin:8px 0 0;font-size:15px}
.city[hidden],.p[hidden]{display:none}
.none{color:var(--dim);padding:28px 0;font-size:15px}
footer{margin-top:40px;font-size:14px;color:var(--dim);line-height:1.7}
@media(max-width:420px){h1{font-size:28px}.nm{font-size:18px}}
</style></head><body><div class="wrap">
<header>
<h1>바르셀로나 · 리스본 · 포르투</h1>
<p class="sub">저장해둔 45곳. 가게 이름을 누르면 구글 지도가 열립니다.</p>
</header>
<div class="bar">
<input type="search" id="q" placeholder="가게 이름, 음식, 동네로 찾기" aria-label="검색">
<div class="chips" role="group" aria-label="도시 필터">
<button class="chip" data-f="all" aria-pressed="true">전체 45</button>
<button class="chip" data-f="bcn" aria-pressed="false">바르셀로나 18</button>
<button class="chip" data-f="lis" aria-pressed="false">리스본 25</button>
<button class="chip" data-f="por" aria-pressed="false">포르투 2</button>
</div></div>
__BODY__
<p class="none" id="none" hidden>결과가 없습니다.</p>
<footer>평점과 영업시간은 저장 시점 기준이라 바뀔 수 있어요. 정확한 정보는 링크를 눌러 구글 지도에서 확인하세요.</footer>
</div>
<script>
var q=document.getElementById('q'),chips=[].slice.call(document.querySelectorAll('.chip')),
    secs=[].slice.call(document.querySelectorAll('.city')),none=document.getElementById('none'),f='all';
function run(){var t=q.value.trim().toLowerCase(),n=0;
 secs.forEach(function(s){var vis=0;
  [].slice.call(s.querySelectorAll('.p')).forEach(function(p){
   var ok=(f==='all'||s.dataset.city===f)&&(!t||p.dataset.q.indexOf(t)>-1);
   p.hidden=!ok; if(ok){vis++;n++;}});
  s.hidden=vis===0;});
 none.hidden=n>0;}
chips.forEach(function(c){c.addEventListener('click',function(){
 chips.forEach(function(x){x.setAttribute('aria-pressed',x===c);});f=c.dataset.f;run();});});
q.addEventListener('input',run);
</script></body></html>"""

open('/mnt/user-data/outputs/여행_맛집_지도.html','w',encoding='utf-8').write(doc.replace('__BODY__',body))

with open('/mnt/user-data/outputs/여행_맛집_바르셀로나_리스본_포르투.csv','w',newline='',encoding='utf-8-sig') as f:
    w=csv.writer(f); w.writerow(["도시","이름","분류","구글평점","리뷰수","가격대","주소","메모","구글지도"])
    for r in rows:
        w.writerow([r['city'],r['name'],r['cat'],r['rating'],r['rc'],r['price'],r['addr'],r['note'],
                    gurl(r['name'], r['pid'], r['city'])])
print(len(rows))
