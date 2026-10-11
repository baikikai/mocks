import re,html,json,sys
from html.parser import HTMLParser
SKIP=('script','style','noscript','svg','nav','header','footer')
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.items=[]; s.skip=0; s.cur=None; s.hrefs=[]
    def flush(s):
        if s.cur is not None:
            t=s.cur[1]; s.items.append((s.cur[0],t)); s.cur=None
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in SKIP: s.skip+=1
        if s.skip: return
        if t in('h1','h2','h3','h4','p'):
            s.flush(); s.cur=[t,'']
        elif t=='br' and s.cur: s.cur[1]+='\n'
        elif t=='img':
            src=a.get('src','')
            if 'wixstatic' in src and '/media/' in src:
                s.flush(); s.items.append(('img',(src.split('/v1/')[0],a.get('alt',''))))
        elif t=='a' and s.cur is not None and a.get('href','').startswith('http'):
            s.cur[1]+='['; s.hrefs.append(a['href'])
        elif t=='a': s.hrefs.append(None)
    def handle_endtag(s,t):
        if t in SKIP and s.skip: s.skip-=1; return
        if s.skip: return
        if t in('h1','h2','h3','h4','p'): s.flush()
        if t=='a' and s.hrefs:
            h=s.hrefs.pop()
            if h and s.cur is not None: s.cur[1]+=f']({h})'
    def handle_data(s,d):
        if not s.skip and s.cur is not None: s.cur[1]+=d
def parse(name):
    p=P(); p.feed(open(name+'.html').read()); p.flush()
    out=[]
    for k,v in p.items:
        if k=='img': out.append({'type':'img','src':v[0],'file':v[1]}); continue
        v=html.unescape(v).replace('​','')
        for part in v.split('\n'):
            part=re.sub(r'\s+',' ',part).strip()
            if part: out.append({'type':k,'text':part})
    return out
def paras(items,mapping):
    res=[]
    for it in items:
        if it['type']=='img': res.append(it); continue
        t=mapping.get(it['type'],it['type'])
        text=it['text']
        m=re.match(r'^\(\d\)\s+(.*)$',text)
        if t=='p' and m: res.append({'type':'li','text':m.group(1)}); continue
        res.append({'type':t,'text':text})
    return res
def trim(items,first_text=None):
    return [i for i in items if not (i['type']=='p' and i['text'] in ('top of page','bottom of page'))]
def clean_tail(items):
    for i in items:
        if 'text' in i: i['text']=re.sub(r'bottom of page$','',i['text']).replace('top of page','',1) if i['text'].endswith('bottom of page') else i['text']
    return items
out={}
m=clean_tail(paras(parse('mission-vision'),{'h3':'h2'}))
out['mission-vision']=m
out['classes']=clean_tail(paras(parse('classes'),{'h3':'h2'}))
h=clean_tail(paras(parse('history'),{'h1':'h2'}))
for i in h:
    if i['type']=='h2' and i['text'].startswith('- by'):
        i['type']='p'; i['text']=i['text'][2:].strip()
out['history']=h
ins=clean_tail(parse('instructors'))
out['instructors']=ins
# drop the document title bleed (first element "X | Brooklyn Aikikai top of page" is title, not in items)
json.dump(out,open('web-raw.json','w'),ensure_ascii=False,indent=1)
for k,v in out.items(): print(k,len(v),[i['type'] for i in v][:14])
