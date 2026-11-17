import json,os,sys,urllib.request,urllib.error
U=os.environ.get('MAKEFUN_ENV_URL') or sys.exit('MAKEFUN_ENV_URL is not set')
V={'p':100,'n':320,'b':330,'r':500,'q':900,'k':20000}
C='abcdefgh'
def post(p,b):
 r=urllib.request.Request(U+p,data=json.dumps(b).encode(),headers={'content-type':'application/json'})
 try:
  with urllib.request.urlopen(r) as x:return json.load(x)
 except urllib.error.HTTPError as e:sys.exit('%s: HTTP %s'%(p,e.code))
def bd(f):
 z={}
 for y,row in enumerate(f.split()[0].split('/')):
  x=0
  for c in row:
   if c.isdigit():x+=int(c)
   else:z[C[x]+str(8-y)]=c;x+=1
 return z
def val(b,s):
 p=b.get(s);return V.get(p.lower(),0) if p else 0
def choose(f,ms):
 b=bd(f); side=f.split()[1]; own='PNBRQK' if side=='w' else 'pnbrqk'
 def score(m):
  a,d=m[:2],m[2:4]; p=b.get(a,'p'); q=b.get(d); n=p.lower(); cap=val(b,d)
  if n=='p' and a[0]!=d[0] and not q:cap=100
  pr=V.get(m[4].lower(),0) if len(m)>4 else 0
  # Prefer forcing material gains, centralization, promotion, and castling.
  cx=abs(3.5-(C.index(d[0]))); cy=abs(4.5-int(d[1])); center=35-(8*(cx+cy))
  advance=(int(d[1])-int(a[1]))*(1 if side=='w' else -1)
  castle=45 if n=='k' and abs(C.index(d[0])-C.index(a[0]))==2 else 0
  # Penalize hanging a queen/rook when a quiet move is available.
  risk=-val(b,a)//18 if cap==0 and n in 'qr' else 0
  return (cap*14+pr*12+center+advance*4+castle+risk, -val(b,a), -ord(m[0]),-ord(m[1]),m)
 return max(ms,key=score)
while 1:
 g=post('/game',{})
 if g['status']=='done':break
 while g['status']=='your_move':
  g=post('/move',{'game':g['game'],'move':choose(g['fen'],g['legal_moves'])})
 print('game',g['game'],g['outcome'],g['reason'],file=sys.stderr)
print('done',g.get('wins'),g.get('draws'),g.get('losses'),file=sys.stderr)
