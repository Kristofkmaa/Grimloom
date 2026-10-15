import json,base64,io
from PIL import Image
import numpy as np
P='/home/claude/grimloom/assets_dem.js'
s=open(P).read(); d=json.loads(s[s.index('{'):s.rindex('}')+1])
for k,v in d.items():
  im=np.array(Image.open(io.BytesIO(base64.b64decode(v['src'].split(',')[1]))).convert('RGBA'))
  r,n=v['anims']['walk_S']; hs=[];xs=[]
  for i in range(n):
    c=im[r*v['ch']:(r+1)*v['ch'], i*v['cw']:(i+1)*v['cw'],3]; ys=np.where(c.max(1)>0)[0]; hs.append(v['ch']-v['foot']-ys.min()); cols=np.where(c.max(0)>0)[0]; xs.append((cols.min()+cols.max())/2)
  v['bh']=int(np.median(hs)); v['ax']=round(float(np.median(xs)),1)
open(P,'w').write('ASSETS.DEM = '+json.dumps(d,separators=(',',':'))+';\n')
