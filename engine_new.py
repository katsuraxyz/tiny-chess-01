import os,json,urllib.request

# Original implementation; ISC license in the submission directory.
N=(31,33,14,18,-31,-33,-14,-18)
D=(15,17,-15,-17)
R=(1,-1,16,-16)
V=(0,100,320,335,500,950,0)
MASK={0:13,4:12,7:14,112:7,116:3,119:11}
LIMIT=48000

def fen(s):
    f=s.split(); b=[0]*128
    for y,row in enumerate(f[0].split('/')):
        x=0
        for p in row:
            if p.isdigit(): x+=int(p)
            else:
                b[(7-y)*16+x]=(' PNBRQK'.index(p.upper()))*(1 if p.isupper() else -1); x+=1
    return tuple(b),1 if f[1]=='w' else -1,sum(1<<i for i,p in enumerate('KQkq') if p in f[2]),square(f[3]) if f[3]!='-' else -1,int(f[4])

def square(s): return ord(s[0])-97+16*(int(s[1])-1)
def uci(m):
    a,b,p=m
    return ''.join(chr(97+(s&7))+str(1+(s>>4)) for s in (a,b))+(' nbrq'[p-1] if p else '')
def key(s): return s[:4]

def attacked(b,s,c):
    for d in (15,17):
        t=s-c*d
        if not t&136 and b[t]==c: return True
    for d in N:
        t=s+d
        if not t&136 and b[t]==2*c: return True
    for d in D+R:
        t=s+d; first=True
        while not t&136:
            p=b[t]
            if p:
                if p*c>0 and (abs(p)==5 or abs(p)==(3 if d in D else 4) or first and abs(p)==6): return True
                break
            first=False; t+=d
    return False

def play(s,m):
    b,c,r,e,h=s; b=list(b); a,t,p=m; man=b[a]; victim=b[t]
    b[a]=0; b[t]=c*p if p else man
    if abs(man)==1 and t==e and not victim: b[t-16*c]=0
    if abs(man)==6 and abs(t-a)==2:
        ra=a+3 if t>a else a-4; rt=a+1 if t>a else a-1
        b[rt]=b[ra]; b[ra]=0
    return tuple(b),-c,r&MASK.get(a,15)&MASK.get(t,15),(a+t)//2 if abs(man)==1 and abs(t-a)==32 and any(not (t+d)&136 and b[t+d]==-c for d in (-1,1)) else -1,0 if abs(man)==1 or victim else h+1

def moves(s):
    b,c,r,e,h=s; k=b.index(c*6)
    for a in range(128):
        if a&136 or b[a]*c<=0: continue
        p=abs(b[a]); targets=[]
        if p==1:
            t=a+16*c
            if not t&136 and not b[t]:
                targets.append(t)
                if a>>4==(1 if c==1 else 6) and not b[t+16*c]: targets.append(t+16*c)
            for d in (15,17):
                t=a+c*d
                if not t&136 and (b[t]*c<0 or t==e): targets.append(t)
        else:
            for d in N if p==2 else D if p==3 else R if p==4 else D+R:
                t=a+d
                while not t&136:
                    if b[t]*c>0: break
                    targets.append(t)
                    if b[t] or p in (2,6): break
                    t+=d
            if p==6 and a==(4 if c==1 else 116) and not attacked(b,a,-c):
                shift=0 if c==1 else 2
                for bit,step,rook in ((1,1,3),(2,-1,-4)):
                    if r&(bit<<shift) and b[a+rook]==4*c and not b[a+step] and not b[a+2*step] and (step==1 or not b[a-3]):
                        q=list(b); q[a]=0; q[a+step]=6*c
                        if not attacked(q,a+step,-c): targets.append(a+2*step)
        for t in targets:
            if abs(b[t])==6: continue
            for pr in (5,4,3,2) if p==1 and t>>4 in (0,7) else (0,):
                m=a,t,pr; ns=play(s,m)
                if not attacked(ns[0],t if p==6 else k,-c):
                    capture=abs(b[t]) or (1 if p==1 and t==e else 0)
                    yield m,ns,capture

def evaluate(s):
    b,c,r_,e,h=s
    mg=eg=ph=0
    wp=[[],[]]
    for a,p in enumerate(b):
        if not p: continue
        side=1 if p>0 else -1; k=abs(p); x=a&7; y=(a>>4) if side>0 else 7-(a>>4)
        ctr=7-abs(2*x-7)-abs(2*y-7)
        m1=e1=V[k]
        if k==1:
            m1+=y*7+ctr*3; e1+=y*y*4+ctr*2; wp[side<0].append((x,y))
        elif k==2: m1+=ctr*9; e1+=ctr*6; ph+=1
        elif k==3: m1+=ctr*5+y*2; e1+=ctr*5; ph+=1
        elif k==4: m1+=y*2+(15 if y==6 else 0); e1+=ctr*2; ph+=2
        elif k==5: m1+=ctr*2; e1+=ctr*4; ph+=4
        else: m1+=-ctr*7-y*12+(25 if y==0 and x in (1,2,6) else 0); e1+=ctr*9
        mg+=side*m1; eg+=side*e1
    ph=24 if ph>24 else ph
    for sd in (0,1):
        mine=wp[sd]; theirs=wp[1-sd]; sg=1-2*sd
        for x,y in mine:
            if sum(qx==x for qx,qy in mine)>1: mg-=sg*12; eg-=sg*18
            if not any(abs(qx-x)==1 for qx,qy in mine): mg-=sg*10; eg-=sg*8
            if not any(abs(qx-x)<=1 and 7-qy>y for qx,qy in theirs): eg+=sg*y*y*6
    pair=0
    if sum(1 for q in b if q==3)>=2: pair+=22
    if sum(1 for q in b if q==-3)>=2: pair-=22
    return c*(mg*ph+eg*(24-ph))//24+12+pair

class Stop(Exception): pass

def choose(s,allowed=None,prior=()):
    global nodes,table,killers,history,path
    nodes=0; table={}; killers={}; history={}; path=list(prior)
    roots=[v for v in moves(s) if allowed is None or uci(v[0]) in allowed]
    if not roots: return None
    best=roots[0][0]
    for depth in range(1,30):
        roots.sort(key=lambda v: v[0]!=best)
        alpha=-32000; candidate=best
        try:
            path.append(key(s))
            for m,ns,cap in roots:
                score=-search(ns,depth-1,-32000,-alpha,1)
                if score>alpha: alpha=score; candidate=m
        except Stop: break
        finally: path.pop()
        best=candidate
        if abs(alpha)>29000: break
    return best

def search(s,depth,alpha,beta,ply):
    global nodes
    nodes+=1
    if nodes>LIMIT: raise Stop
    b,c,r_,e,h=s; k=key(s); a0=alpha
    chk=attacked(b,b.index(6*c),-c)
    if h>=100 or path.count(k)>=2:
        if chk and not next(moves(s),None): return -30000+ply
        return 0
    if ply>=64: return evaluate(s)
    hit=table.get(s)
    tmove=hit[3] if hit else None
    if hit and depth>0 and hit[0]>=depth:
        sc=hit[1]
        if sc>29000: sc-=ply
        elif sc<-29000: sc+=ply
        if hit[2]==0 or (hit[2]==1 and sc>=beta) or (hit[2]==-1 and sc<=alpha): return sc
    opts=list(moves(s))
    if not opts: return -30000+ply if chk else 0
    if depth<=0 and not chk:
        stand=evaluate(s)
        if stand>=beta: return stand
        if stand>alpha: alpha=stand
        opts=[v for v in opts if v[2] or v[0][2]]
        if not opts: return alpha
    def order(v):
        m,ns,cap=v
        if m==tmove: return 3
        if cap or m[2]: return 2
        if m==killers.get(ply): return 1
        return 0
    opts.sort(key=order,reverse=True)
    best=-32000; move=None; path.append(k)
    try:
        for i,(m,ns,cap) in enumerate(opts):
            drop=1 if depth>=4 and i>=5 and not chk and not cap and not m[2] and (-c*6 not in ns[0] or not attacked(ns[0],ns[0].index(-c*6),c)) else 0
            if i==0: sc=-search(ns,depth-1,-beta,-alpha,ply+1)
            else:
                sc=-search(ns,depth-1-drop,-alpha-1,-alpha,ply+1)
                if alpha<sc<beta and drop: sc=-search(ns,depth-1,-alpha-1,-alpha,ply+1)
                if alpha<sc<beta: sc=-search(ns,depth-1,-beta,-alpha,ply+1)
            if sc>best: best=sc; move=m
            if sc>alpha:
                alpha=sc
                if alpha>=beta:
                    if not cap and not m[2] and depth>0:
                        killers[ply]=m; history[c,m]=min(8000,history.get((c,m),0)+depth*depth)
                    break
    finally: path.pop()
    if depth>0:
        table[s]=(depth,best+ply if best>29000 else best-ply if best<-29000 else best,1 if best>=beta else -1 if best<=a0 else 0,move)
    return best

def run():
    base=os.environ['MAKEFUN_ENV_URL'].rstrip('/')
    def post(route,data):
        request=urllib.request.Request(base+route,json.dumps(data).encode(),{'Content-Type':'application/json'})
        with urllib.request.urlopen(request) as response: return json.load(response)
    g=post('/game',{})
    while g['status']!='done':
        if g['status']!='your_move':
            g=post('/game',{}); continue
        seen=[]; previous=fen(g['start_fen'])
        for u in g['moves']:
            seen.append(key(previous))
            previous=play(previous,(square(u[:2]),square(u[2:4]),' pnbrqk'.index(u[4]) if len(u)>4 else 0))
        s=fen(g['fen']); m=choose(s,set(g['legal_moves']),seen)
        if m is None: raise ValueError('No legal root move')
        g=post('/move',{'game':g['game'],'move':uci(m)})

if __name__=='__main__': run()
