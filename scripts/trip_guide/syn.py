# -*- coding: utf-8 -*-
"""Hidden search-synonym layer for the trip guide.

Why this exists: searching "빠에야" returned 1 hit while 9 venues served it.
Two stacked causes — the dish field wasn't in the search index at all, and the
data itself said "파에야" in some rows and "쌀 요리" in others. Indexing the
field fixed half; this table fixes the other half by expanding each card's
searchable text with Korean spelling variants, the original-language term
(es/pt) and English. The expansion is invisible on the card — index only.

Extend by putting the term as it appears in card text on the left, and every
other way someone might type it on the right.
"""
SYN = {
 '파에야': '빠에야 paella arroz 아로스 쌀요리 밥',
 '쌀 요리': '파에야 빠에야 paella arroz 아로스 밥',
 '타파스': '따파스 tapas 안주',
 '문어': '뿔뽀 pulpo polvo octopus 낙지',
 '대구': '바칼라우 bacalhau bacalao cod 코드',
 '새우': '감바 gamba gambas camarao 프론 prawn shrimp 쉬림프',
 '붉은새우': '감바로하 gamba roja carabinero 홍새우',
 '스테이크': 'steak chuleton 소고기 비프 beef 고기',
 '소고기': 'beef 쇠고기 비프 스테이크',
 '돼지': '포크 pork 돼지고기 이베리코 iberico',
 '이베리코': 'iberico 하몽 jamon 돼지',
 '크로케타': 'croqueta croquete 크로켓 고로케 croquette',
 '에그타르트': '파스텔 드 나타 pastel de nata natas 타르트',
 '참치': 'tuna atun atum 다랑어 참다랑어 마구로',
 '참다랑어': '참치 tuna atun 블루핀 bluefin',
 '굴': 'oyster ostra 오이스터',
 '해산물': 'seafood marisco 마리스코 씨푸드 조개',
 '스시': 'sushi 초밥 오마카세 omakase 사시미',
 '오마카세': 'omakase 스시 sushi 초밥',
 '타르타르': 'tartare tartar 육회',
 '젤라토': 'gelato 아이스크림 ice cream 젤라또',
 '츄러스': 'churros 추로스 churro',
 '피자': 'pizza 피짜',
 '파스타': 'pasta 면',
 '리소토': 'risotto 리조또 쌀',
 '테이스팅': 'tasting 코스 menu degustacion 오마카세 시식',
 '코스': 'tasting 테이스팅 degustacion 세트',
 '와인': 'wine vino vinho 와인바',
 '포트와인': 'port wine porto 포르투와인',
 '치즈케이크': 'cheesecake 치즈 케이크',
 '오믈렛': 'tortilla 토르티야 또르띠야 omelette 감자오믈렛',
 '한식': 'korean 한국 코리안 김치',
 '채식': 'vegan vegetarian 비건 베지테리언',
 '브런치': 'brunch 아침 조식 breakfast',
 '베이커리': 'bakery 빵 padaria panaderia 제과',
 '카페': 'cafe coffee 커피 카페테리아',
}


def expand(text):
    t = (text or '')
    out = []
    for k, v in SYN.items():
        if k in t:
            out.append(v)
    return ' '.join(out)
