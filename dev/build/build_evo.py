import sys, json, base64, os
from PIL import Image
import numpy as np
from scipy import ndimage
D='/home/claude/grimloom/evo/'
CELLW,CELLH,FOOT=300,320,300; counts=[4,4,4,2,4]
def torso_cx(cm,feet):
  band=cm[max(0,feet-150):feet-80]; c=band.sum(0); best=(0,0,0); s=None
  for x in range(len(c)+1):
    v=c[x] if x<len(c) else 0
    if v>0 and s is None: s=x;acc=0
    if s is not None:
      if v>0: acc+=v
      else:
        if acc>best[0]: best=(acc,s,x)
        s=None
  return (best[1]+best[2])/2
def proc(name,slash=True):
  a=np.array(Image.open(D+name+'.png').convert('RGB')).astype(float); H,W=a.shape[:2]
  r,g,b=a[...,0],a[...,1],a[...,2]
  d=np.sqrt((255-r)**2+g**2+(255-b)**2); alpha=np.clip((d-45)/55,0,1)
  sp=(1-alpha); o=a.copy(); o[...,0]-=sp*120; o[...,2]-=sp*80; o=np.clip(o,0,255)
  rgba=np.dstack([o.astype(np.uint8),(alpha*255).astype(np.uint8)]); m=alpha>0.5
  rows=m.sum(1); rs=[];on=False
  for y in range(H):
    if rows[y]>0 and not on: s0=y;on=True
    if rows[y]==0 and on: rs.append((s0,y));on=False
  if on: rs.append((s0,H))
  rs=[x for x in rs if x[1]-x[0]>60]
  if len(rs)!=5:
    # lignes fusionnées : coupe au creux le plus bas autour des cinquièmes
    rs=[];prev=0
    for k in range(1,5):
      c=int(H*k/5); lo,hi=c-40,c+40; cut=lo+int(np.argmin(rows[lo:hi])); rs.append((prev,cut)); prev=cut
    rs.append((prev,H))
    rs=[(y0+int(np.argmax(rows[y0:y1]>0)), y1-int(np.argmax(rows[y0:y1][::-1]>0))) for y0,y1 in rs]
  assert len(rs)==5,(name,rs)
  CW=W/4; sheet=np.zeros((CELLH*5,CELLW*4,4),np.uint8); anc=[]
  for ri,(y0,y1) in enumerate(rs):
    row=[]
    for fi in range(counts[ri]):
      x0,x1=int(fi*CW),int((fi+1)*CW); yy0=max(0,y0-14); cm=m[yy0:y1+4,x0:x1]
      lb,nb=ndimage.label(cm); sz0=ndimage.sum(cm,lb,range(1,nb+1)); big=lb==(np.argmax(sz0)+1)
      ys,xs=np.where(big); feet=ys.max(); cx=torso_cx(cm,feet)
      piece=Image.fromarray(rgba[yy0:y1+4,x0:x1]); cell=Image.new('RGBA',(CELLW,CELLH))
      cell.paste(piece,(int(round(CELLW/2-cx)),int(round(FOOT-feet))),piece)
      c=np.array(cell).astype(float); A=c[...,3]>128; rgb=c[...,:3]
      mx=rgb.max(-1); mn=rgb.min(-1); sat=(mx-mn)/(mx+1e-6); vivid=(sat>0.5)&(mx>120)
      body=ndimage.binary_opening(A&~vivid,structure=np.ones((11,11)))
      lab,n=ndimage.label(body); sz=ndimage.sum(body,lab,range(1,n+1)); body=lab==(np.argmax(sz)+1)
      # nettoyage : petits débris et lignes du haut
      lab2,n2=ndimage.label(A); s2=ndimage.sum(A,lab2,range(1,n2+1))
      for i,v in enumerate(s2,1):
        if v<80: c[lab2==i,3]=0
      c[:24,:,3]=0
      lab3,n3=ndimage.label(c[...,3]>20)
      for i in range(1,n3+1):
        yy3=np.where((lab3==i).any(1))[0]
        if yy3.min()>FOOT-6: c[lab3==i,3]=0
      if slash and ri==2 and fi in (1,2): # atténue le slash
        bys=np.where(body.any(1))[0]; btop=bys.min(); yy,xx=np.mgrid[0:CELLH,0:CELLW]
        prot=((np.abs(xx-150)<=52)&(yy>=btop-4))|ndimage.binary_dilation(body,iterations=4)
        dist=ndimage.distance_transform_edt(~prot); k=np.clip(1-dist/22,0.3,1)
        c[...,3]*=k; c[...,:3]*=(0.85+0.15*k)[...,None]
      ys2,xs2=np.where(body); top=ys2.min(); ft=ys2.max(); h=ft-top
      def cxat(y):
        xx=np.where(body[int(y)])[0]; return (xx.min()+xx.max())/2 if len(xx) else 150
      sh=top+0.27*h; hip=top+0.55*h; cs=cxat(sh); chp=cxat(hip)
      ang=float(np.degrees(np.arctan2(cs-chp, hip-sh)))
      if ri in (0,1,4): ang*=0.4
      row.append([round(cs-150,1), round(FOOT-sh,1), round(ang,1)])
      sheet[ri*CELLH:(ri+1)*CELLH, fi*CELLW:(fi+1)*CELLW]=c.clip(0,255).astype(np.uint8)
    anc.append(row)
  im=Image.fromarray(sheet)
  q=im.quantize(colors=200,method=Image.FASTOCTREE,dither=Image.Dither.NONE)
  q.save(D+'out_'+name+'.png',optimize=True)
  ht=FOOT-np.where(sheet[:CELLH,:CELLW,3].any(1))[0].min()
  return {'b64':base64.b64encode(open(D+'out_'+name+'.png','rb').read()).decode(),'anc':anc,'h':int(ht)}
if __name__=='__main__':
 out={}
 for n in ['ecuyer','chev','enfer','mort','givre','smort','sfeu','shiver']:
  out[n]=proc(n); print(n, os.path.getsize(D+'out_'+n+'.png')//1024,'KB', 'h',out[n]['h'])
 json.dump(out,open(D+'evo.json','w'))
