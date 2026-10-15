import sys, json, base64, io
from PIL import Image
import numpy as np
from scipy import ndimage
path, name, k = sys.argv[1], sys.argv[2], float(sys.argv[3]); keep = len(sys.argv) > 4
im=Image.open(path).convert('RGBA'); a=np.array(im).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]
kk=(g>130)&(g-np.maximum(r,b)>50); sp=(~kk)&(g>np.maximum(r,b)); a[...,1]=np.where(sp,np.maximum(r,b),g)
al=~kk; lab,n=ndimage.label(al); sz=ndimage.sum(al,lab,range(1,n+1)); al=np.isin(lab,1+np.where(sz>=25)[0]); a[...,3]=np.where(al,255,0)
src=Image.fromarray(a.astype('uint8')); W,H=src.size; cw,ch=W/4,H/3; S=float(__import__('os').environ.get('ES','0.22')); OC=round(max(cw,ch)*S); FOOT=round(OC*0.9)
out=Image.new('RGBA',(OC*4,OC*3))
for ri in range(3):
  for ci in range(4):
    c=src.crop((round(ci*cw),round(ri*ch),round((ci+1)*cw),round((ri+1)*ch)))
    if not c.getbbox(): continue
    sm=c.resize((round(c.width*S),round(c.height*S)),Image.LANCZOS); arr=np.array(sm); arr[...,3]=np.where(arr[...,3]>110,255,0); sm=Image.fromarray(arr)
    bb=sm.getbbox(); out.alpha_composite(sm,(ci*OC+(OC-sm.width)//2, ri*OC+((OC-sm.height)//2 if keep else FOOT-bb[3])))
f=np.array(out.crop((0,0,OC,OC)))[...,3]; ys=np.where(f.any(1))[0]; xs=np.where(f.any(0))[0]
m={'cw':OC,'ch':OC,'foot':OC-FOOT,'bh':int(FOOT-ys[0]),'k':k,'spd':0.5,'ax':float((xs[0]+xs[-1])/2),'anims':{'walk_S':[0,4],'atk_S':[1,4],'hit_S':[2,1],'die_S':[2,4],'idle_S':[0,1]}}
b=io.BytesIO(); out.save(b,'PNG',optimize=True); m['src']='data:image/png;base64,'+base64.b64encode(b.getvalue()).decode()
json.dump(m,open(name+'.json','w')); out.resize((out.width*3,out.height*3),Image.NEAREST).save(name+'_big.png'); print({x:y for x,y in m.items() if x!='src'})
