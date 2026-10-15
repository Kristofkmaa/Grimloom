import numpy as np
from scipy import ndimage
from PIL import Image
def defringe(im, it=3):
  a=np.array(im.convert('RGBA')).astype(np.int32); r,g,b,al=a[...,0],a[...,1],a[...,2],a[...,3]
  mag=(r>60)&(b>60)&(np.minimum(r,b)-g>28)&(r>=0.65*b)&(b>=0.42*r)
  removed=0
  for _ in range(it):
    A=al>16
    edge=A&ndimage.binary_dilation(~A,structure=np.ones((3,3)))
    kill=edge&A&mag
    removed+=kill.sum(); al[kill]=0
  # pixels de bord restants : retire la teinte magenta résiduelle
  A=al>16; edge=A&ndimage.binary_dilation(~A,structure=np.ones((3,3)),iterations=2)
  sp=np.clip(np.minimum(r,b)-g-10,0,None)*edge*(r>=0.7*b)
  r2=np.clip(r-sp*0.8,0,255); b2=np.clip(b-sp*0.8,0,255)
  # alpha : les bords semi-transparents deviennent nets
  out=np.dstack([r2,g,b2,al]).astype(np.uint8)
  return Image.fromarray(out,'RGBA'),removed
