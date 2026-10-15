import os,json,base64,io,numpy as np
from PIL import Image
R='/home/claude/itch/demons/'
DIRROWS={'S':2,'SE':1,'E':0}
SH=json.load(open('/home/claude/grimloom/build/shifts2.json'))
ARCH={'Demon Spawn 6','Demon Spawn 7','Demon Spawn 10','Imp 7'}
def shift(folder,a):
    if a=='walk': return 0
    d=SH.get(folder,{})
    if a in ('idle','taunt'):
        v=d.get(a); return v[0] if v and v[1]>10 else 0
    if a.startswith('atk') and folder in ARCH: return 0
    v=d.get(a) if a.startswith('atk') else None
    if v and v[1]>=10: return v[0]
    v=d.get('atk'); return v[0] if v and v[1]>=10 else 7
def key(folder): return folder.lower().replace('demon spawn ','spawn').replace('demon beast ','beast').replace('demon elite ','elite').replace('imp ','imp')
def find(folder,names):
    for n in names:
        if os.path.exists(R+folder+'/'+n+'.png'): return n
    return None
def load(folder,name):
    a=np.array(Image.open(R+folder+'/'+name+'.png').convert('RGBA')).astype(np.int32)
    ef=R+folder+'/Effects/'+name+'.png'
    if os.path.exists(ef):
        e=np.array(Image.open(ef).convert('RGBA')).astype(np.int32)
        if e.shape==a.shape:
            ea=e[...,3:4]/255.0
            rgb=np.clip(a[...,:3]+e[...,:3]*ea,0,255)
            a[...,:3]=np.where(a[...,3:4]>0,rgb,e[...,:3]); a[...,3]=np.maximum(a[...,3],e[...,3])
    return a.astype(np.uint8)
out={};total=0
for folder in sorted(os.listdir(R)):
    k=key(folder); big=k.startswith('beast') or k=='spawn1'
    anims={'walk':find(folder,['Run'] if k.startswith('imp') else ['Walk']),'atk':find(folder,['Attack 1']),'hit':find(folder,['TakeDamage 1']),'die':find(folder,['Die 1'])}
    if big or k.startswith('elite'): anims.update({'atk2':find(folder,['Attack 2']),'atk3':find(folder,['Attack 3']),'idle':find(folder,['Idle','Idle 1']),'taunt':find(folder,['Taunt'])})
    if k=='spawn1': anims.update({'atk4':find(folder,['Attack 4']),'atk5':find(folder,['Attack 5']),'atk6':find(folder,['Attack 6']),'roll':find(folder,['Roll 1'])})
    anims={a:n for a,n in anims.items() if n}
    frames={};x0=y0=999;x1=y1=0
    for a,n in anims.items():
        sh=load(folder,n);nf=sh.shape[1]//128;step=2 if nf>=12 else 1
        for d,row0 in DIRROWS.items():
            row=(row0+shift(folder,a))%8
            L=[]
            for i in range(0,nf,step):
                c=sh[row*128:(row+1)*128,i*128:(i+1)*128];ys,xs=np.where(c[...,3]>0)
                if len(xs): x0=min(x0,xs.min());x1=max(x1,xs.max());y0=min(y0,ys.min());y1=max(y1,ys.max())
                L.append(c)
            frames[(a,d)]=L
    cw,ch=x1-x0+1,y1-y0+1;cols=max(len(v) for v in frames.values());rows=len(frames)
    sheet=Image.new('RGBA',(cw*cols,ch*rows));meta={}
    for r,((a,d),L) in enumerate(frames.items()):
        for i,c in enumerate(L): sheet.paste(Image.fromarray(c[y0:y1+1,x0:x1+1]),(i*cw,r*ch))
        meta[a+'_'+d]=[r,len(L)]
    c=frames[('walk','S')][0];foot=y1-np.where(c[...,3]>0)[0].max()
    b=io.BytesIO();sheet.quantize(256,method=Image.FASTOCTREE).save(b,'PNG',optimize=True)
    out[k]={'src':'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode(),'cw':int(cw),'ch':int(ch),'foot':int(foot),'anims':meta}
    total+=len(b.getvalue());print(k,cw,ch,rows,cols,len(b.getvalue())//1024,'KB',flush=True)
open('/home/claude/grimloom/assets_dem.js','w').write('ASSETS.DEM = '+json.dumps(out,separators=(',',':'))+';')
print('total',total//1024,'KB')
