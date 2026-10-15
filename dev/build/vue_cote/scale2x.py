import numpy as np, sys
from PIL import Image
def s2x(a):  # Scale2x (EPX) : agrandit le pixel art en arrondissant les diagonales
    H, W = a.shape[:2]; P = np.pad(a, ((1, 1), (1, 1), (0, 0)), mode='edge')
    B, D, E, F, Hh = P[:-2, 1:-1], P[1:-1, :-2], P[1:-1, 1:-1], P[1:-1, 2:], P[2:, 1:-1]
    eq = lambda x, y: (x == y).all(-1)
    c = ~eq(B, Hh) & ~eq(D, F)
    o = np.zeros((H * 2, W * 2, a.shape[2]), a.dtype)
    o[0::2, 0::2] = np.where((c & eq(D, B))[..., None], D, E); o[0::2, 1::2] = np.where((c & eq(B, F))[..., None], F, E)
    o[1::2, 0::2] = np.where((c & eq(D, Hh))[..., None], D, E); o[1::2, 1::2] = np.where((c & eq(Hh, F))[..., None], F, E)
    return o
a = np.array(Image.open(sys.argv[1]).convert('RGBA')); a[a[..., 3] < 60] = 0
a = s2x(s2x(a)); im = Image.fromarray(a)
im.save(sys.argv[2], 'WEBP', quality=88, method=6, alpha_quality=100); print(im.size)
