import numpy as np, base64, json, colorsys
from PIL import Image
D='/home/claude/grimloom/fxart/'
def bands(prof, n, minlen=5):
  on=prof>0; segs=[]; s=None
  for i,v in enumerate(list(on)+[False]):
    if v and s is None: s=i
    if not v and s is not None:
      if i-s>=minlen: segs.append((s,i))
      s=None
  return segs
def to_alpha(a):
  a=a.astype(float); m=a.max(-1); al=np.clip((m-14)/150,0,1)
  rgb=np.where(al[...,None]>0, a/np.maximum(al[...,None],1e-3)*0.0+a/np.maximum(m[...,None]/255,1e-3)*np.minimum(1,m[...,None]/255+0.0), 0)
  rgb=np.clip(a/np.maximum(al[...,None],0.05),0,255)
  return np.dstack([rgb,al*255]).astype(np.uint8)
STRICT=[False]
GUIDE={'imp':[135,265,395,530,648,772,925]}
def slice_sheet(name, cols, rows, cw, ch):
  global GN
  im=np.array(Image.open(D+name+'_src.png').convert('RGB')); H,W=im.shape[:2]
  lum=im.max(-1)>40
  rs=bands(lum.sum(1)>2, rows, 8)
  # fusionne les petites bandes proches pour obtenir 'rows' lignes
  while len(rs)>rows:
    g=[rs[i+1][0]-rs[i][1] for i in range(len(rs)-1)]; k=int(np.argmin(g)); rs[k]=(rs[k][0],rs[k+1][1]); del rs[k+1]
  if len(rs)!=rows:
    prof=(im.max(-1)>30).sum(1).astype(float); prof=np.convolve(prof,np.ones(5)/5,'same'); cuts=[0]
    for k in range(1,rows):
      c=GUIDE[name][k-1] if name in GUIDE else int(k*H/rows); lo,hi=c-25,c+25; cuts.append(lo+int(np.argmin(prof[lo:hi])))
    cuts.append(H); rs=[(cuts[i],cuts[i+1]) for i in range(rows)]; STRICT[0]=True
  else: STRICT[0]=False
  out=np.zeros((rows*ch, cols*cw, 4),np.uint8); CWs=W/cols
  for r,(y0,y1) in enumerate(rs):
    cy=(y0+y1)/2; hh=max(y1-y0, 1)
    for c in range(cols):
      x0,x1=int(c*CWs),int((c+1)*CWs); cell=im[:, x0:x1]
      # boîte englobante horizontale commune à la ligne : on garde la cellule entière, centrée verticalement sur la bande
      if STRICT[0]: ya,yb=y0,y1
      else: sh=max(hh+16, int(CWs*ch/cw)); ya=int(max(0,cy-sh/2)); yb=int(min(H,cy+sh/2))
      piece=cell[ya:yb]
      rgba=to_alpha(piece); p=Image.fromarray(rgba,'RGBA')
      p.thumbnail((cw,ch),Image.LANCZOS)
      cvs=Image.new('RGBA',(cw,ch)); cvs.paste(p,((cw-p.width)//2,(ch-p.height)//2),p)
      out[r*ch:(r+1)*ch, c*cw:(c+1)*cw]=np.array(cvs)
  return out
def recolor(block, hue_to):
  a=block.astype(float)/255; out=block.copy()
  r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
  import numpy as _n
  mx=_n.maximum(_n.maximum(r,g),b); mn=_n.minimum(_n.minimum(r,g),b)
  # bleu -> jaune électrique : on permute les canaux (b -> r,g) pour garder les nuances
  out[...,0]=_n.clip((b*0.95+r*0.3)*255,0,255); out[...,1]=_n.clip((b*0.85+g*0.4)*255,0,255); out[...,2]=_n.clip((r*0.5+g*0.2)*255,0,255)
  return out
res={}
for name,cols,rows,cw,ch in [('prj',4,8,128,64),('imp',6,8,112,96),('spl',6,8,128,104)]:
  o=slice_sheet(name,cols,rows,cw,ch)
  if name in ('prj','imp'):
    y=recolor(o[5*ch:6*ch],None); o=np.vstack([o,y])
  Image.fromarray(o,'RGBA').save(D+name+'.png',optimize=True)
  res[name]={'cw':cw,'ch':ch,'n':cols,'b64':base64.b64encode(open(D+name+'.png','rb').read()).decode()}
  print(name,o.shape,len(res[name]['b64'])//1024,'KB')
json.dump(res,open(D+'fx.json','w'))
