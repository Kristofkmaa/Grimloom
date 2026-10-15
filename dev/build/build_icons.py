import json,base64,io,colorsys
from PIL import Image
import numpy as np
SRC='/home/claude/itch/raven/Free - Raven Fantasy Icons/Full Spritesheet/32x32.png'
im=Image.open(SRC).convert('RGBA')
def rng(r,cs): return [(r,c) for c in cs]
A=range(16)
POOLS={
 'arme':[(r,c) for r in range(90,113) for c in A if not ((r in (92,97,102) and c>=13))],
 'casque':rng(119,A)+rng(122,A)+rng(125,A)+rng(128,range(3,6))+rng(129,range(12,16))+rng(114,range(7,10)),
 'plastron':rng(116,A)+rng(117,A)+rng(118,A)+rng(120,A)+rng(123,A)+rng(126,A)+rng(130,A)+rng(131,A)+rng(113,range(10,16))+rng(114,range(0,7))+rng(128,range(0,3)),
 'jambieres':rng(121,A)+rng(124,A)+rng(127,A)+rng(135,range(14,16)),
 'gants':rng(135,range(7,14))+rng(128,range(9,12))+[(92,15),(97,15),(102,15)],
 'bottes':rng(115,range(12,16))+rng(135,range(0,7))+rng(128,range(6,9)),
 'anneau':rng(115,range(2,7))+rng(128,range(12,16))+rng(136,range(8,16)),
 'amulette':rng(115,range(7,12))+rng(129,range(0,5))+rng(136,range(0,8)),
}
def tier(t):
    a=np.array(t).astype(float); m=(a[...,3]>200); px=a[m][:,:3]
    lum=px.mean(1); px=px[lum>70]
    if len(px)<10: return 0
    r,g,b=px.mean(0)/255; h,s,v=colorsys.rgb_to_hsv(r,g,b); h*=360
    if s<0.22 or (v<0.45 and 15<h<45): return 0
    if 70<=h<165: return 1
    if 165<=h<255: return 2
    if 255<=h<320: return 3
    if 15<=h<42: return 4
    if 42<=h<70: return 6
    return 5
tiles=[];meta={}
for slot,cells in POOLS.items():
    T=[[] for _ in range(7)]
    for (r,c) in cells:
        t=im.crop((c*32,r*32,c*32+32,r*32+32))
        if np.array(t)[...,3].max()==0: continue
        T[tier(t)].append(len(tiles)); tiles.append(t)
    # chaque rareté doit avoir au moins une icône : on emprunte au voisin le plus proche
    for i in range(7):
        if not T[i]:
            for d in (1,-1,2,-2,3,-3,4,-4,5,-5,6,-6):
                j=i+d
                if 0<=j<7 and T[j]: T[i]=T[j][:]; break
    meta[slot]=T
    print(slot,[len(x) for x in T])
cols=32; rows=(len(tiles)+cols-1)//cols
sheet=Image.new('RGBA',(cols*32,rows*32))
for i,t in enumerate(tiles): sheet.paste(t,((i%cols)*32,(i//cols)*32))
b=io.BytesIO(); sheet.save(b,'PNG',optimize=True)
open('/home/claude/grimloom/assets_icons.js','w').write('ASSETS.icons = '+json.dumps({'src':'data:image/png;base64,'+base64.b64encode(b.getvalue()).decode(),'cols':cols,'pool':meta},separators=(',',':'))+';\n')
print(len(tiles),'icons',len(b.getvalue())//1024,'KB')
sheet.save('/tmp/claude-0/-home-claude/71fc310b-fbb5-544f-990e-69912a380c75/scratchpad/icons_sheet.png')
