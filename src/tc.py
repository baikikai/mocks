import re
MINOR={'a','an','the','and','but','or','nor','for','of','to','in','on','at','by','as','vs','via','per','with','from','into','over'}
def _cap(w):
    # capitalise first letter of each hyphen/slash part, keep the rest
    def one(p):
        for i,ch in enumerate(p):
            if ch.isalpha(): return p[:i]+ch.upper()+p[i+1:]
        return p
    return re.sub(r"[^-/]+",lambda m:one(m.group(0)),w)
def tc(t):
    if not re.search(r'[a-z]',t): return t
    ws=re.split(r'(\s+)',t); idx=[i for i,w in enumerate(ws) if w.strip()]
    out=[]
    for n,w in enumerate(ws):
        if not w.strip(): out.append(w); continue
        first=n==idx[0]; last=n==idx[-1]
        bare=re.sub(r'^\W+|\W+$','',w).lower()
        if re.search(r'\d',w) or w[:1] in '([' and not w[1:2].isalpha() : out.append(w); continue
        if bare in MINOR and not first and not last: out.append(w)
        else: out.append(_cap(w))
    return ''.join(out)
if __name__=='__main__':
    for s in ['Becoming a member','Uchideshi program','Dues and costs','Joining the dojo',"Kids' Aikido",'Anti-racism/DEI','Our Commitment to Anti-Racism','Gi (uniform)','Policies','Origins and History of Tendokan Dojo','In General','Pay-it-forward level 1','Tendokan Dojo, Part II','Donate by check']: print(s,'->',tc(s))
