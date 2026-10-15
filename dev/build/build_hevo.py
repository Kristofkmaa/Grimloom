import sys,json,base64,os
sys.path.insert(0,'/home/claude/grimloom/build')
from build_evo import proc,D
from PIL import Image
CH,CW=320,300
def scale_rows(name):
  im=Image.open(D+'out_'+name+'.png').convert('RGBA')
  for ri in (2,3):
    for fi in range(4):
      box=(fi*CW,ri*CH,(fi+1)*CW,(ri+1)*CH); c=im.crop(box)
      if not c.getbbox(): continue
      w,h=int(CW*1.1),int(CH*1.1); b=c.resize((w,h),Image.NEAREST)
      # pied (150,300) fixe
      ox,oy=int(150*1.1-150),int(300*1.1-300); b=b.crop((ox,oy,ox+CW,oy+CH))
      im.paste((0,0,0,0),box); im.paste(b,box[:2])
  q=im.quantize(colors=200,method=Image.FASTOCTREE,dither=Image.Dither.NONE); q.save(D+'out_'+name+'.png',optimize=True)
def run(name):
  r=proc(name,slash=False); scale_rows(name)
  for ri in (2,3):
    r['anc'][ri]=[[round(a*1.1,1),round(b*1.1,1),g] for a,b,g in r['anc'][ri]]
  r['b64']=base64.b64encode(open(D+'out_'+name+'.png','rb').read()).decode(); return r
ref=json.load(open(D+'hunter.json'))
out={}
for n in ['h_novice','h_ombre','h_sang','h_argent','h_faucheur','h_seigsang','h_grandinq']:
  r=run(n); r['anc']=ref['anc']; out[n]=r; print(n,os.path.getsize(D+'out_'+n+'.png')//1024,'KB h',r['h'])
json.dump(out,open(D+'hevo.json','w'))
