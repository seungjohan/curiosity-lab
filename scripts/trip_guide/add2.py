import json,sys
d=json.load(open('enrich.json',encoding='utf-8'))
n=0
for k,v in json.load(sys.stdin).items():
    if k not in d: print('MISS',k); continue
    if v.get('dish'): d[k]['dish']=v['dish']
    if v.get('note'): d[k]['note']=v['note']
    n+=1
json.dump(d,open('enrich.json','w'),ensure_ascii=False)
print('갱신',n,'| 메뉴',sum(1 for x in d.values() if x.get('dish')),
      '| 특징',sum(1 for x in d.values() if x.get('note')))
