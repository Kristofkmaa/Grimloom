import sys,re,io,base64,json
sys.path.insert(0,'/home/claude/grimloom/build')
from build_evo import proc,D
from defringe import defringe
from PIL import Image
import numpy as np
from scipy import ndimage
s=open('/home/claude/grimloom/src.html').read()
m=re.search(r"ASSETS\.k_m_sorcier = \{ src: 'data:image/png;base64,([^']+)'",s)
REF=np.array(Image.open(io.BytesIO(base64.b64decode(m.group(1)))).convert('RGBA'))[...,3]>40
FR=[(0,4),(1,4),(2,4),(3,2),(4,4)]
def cell(a,r,f): return a[r*320:(r+1)*320,f*300:(f+1)*300]
def scale(im,r,f,s):
  box=(f*300,r*320,f*300+300,r*320+320); c=im.crop(box); b=c.resize((round(300*s),round(320*s)),Image.NEAREST)
  ox,oy=round(150*s-150),round(300*s-300); b=b.crop((ox,oy,ox+300,oy+320)); im.paste((0,0,0,0),box); im.paste(b,box[:2])
def run(n):
  proc(n,slash=False); im=Image.open(D+'out_'+n+'.png').convert('RGBA'); a=np.array(im)
  for r,fs in FR:
    for f in range(fs):
      c=cell(a,r,f); lab,k=ndimage.label(c[...,3]>0)
      for i in range(1,k+1):
        if np.where((lab==i).any(1))[0].max()<45: c[lab==i,3]=0
  im=Image.fromarray(a)
  scale(im,2,1,1.08); scale(im,2,2,1.08); scale(im,3,0,1.1); scale(im,3,1,1.1)
  a=np.array(im); out=np.zeros_like(a); shifts=[]
  for r,fs in FR:
    for f in range(fs):
      c=cell(a,r,f); M=c[...,3]>40; R=cell(REF,r,f)
      band=slice(170,300); best=(-1,0)
      for dx in range(-50,51):
        sh=np.roll(M[band],dx,axis=1); sc=(sh&R[band]).sum()/max(1,(sh|R[band]).sum())
        if sc>best[0]: best=(sc,dx)
      shifts.append((r,f,best[1],round(best[0],2)))
  for r,fs in FR:
    ds=[x[2] for x in shifts if x[0]==r]; med=int(np.median(ds))
    for f in range(fs):
      dx=med if r in (0,1,4) else ds[f]
      cell(out,r,f)[:]=np.roll(cell(a,r,f),dx,axis=1)
  o,_=defringe(Image.fromarray(out))
  o.quantize(colors=200,method=Image.FASTOCTREE,dither=Image.Dither.NONE).save(D+'out_'+n+'.png',optimize=True)
  print(n,[x for x in shifts if abs(x[2])>8 or x[3]<0.6])
  return base64.b64encode(open(D+'out_'+n+'.png','rb').read()).decode()
res={}
for n in ['m_apprenti','m_pyro','m_necro','m_foudre','m_brasier','m_liche','m_tempete']: res[n]=run(n)
json.dump(res,open(D+'mevo.json','w'))
