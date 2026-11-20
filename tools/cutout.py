import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

src, out, prev, gthr = sys.argv[1], sys.argv[2], sys.argv[3], float(sys.argv[4])
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float64)
H, W, _ = im.shape
Y, X = np.mgrid[0:H, 0:W]

# smooth sky regions: low gradient on a lightly blurred image
sm = np.stack([ndi.gaussian_filter(im[..., c], 1.4) for c in range(3)], -1)
grad = np.max([np.hypot(ndi.sobel(sm[..., c], 0), ndi.sobel(sm[..., c], 1)) / 8 for c in range(3)], axis=0)
flat = grad < gthr
lab, n = ndi.label(flat)
border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
border = border[border > 0]
sky = np.isin(lab, border)

# local sky colour from the confirmed sky, to judge enclosed flat regions
w = sky.astype(float)
def fill(sigma):
    den = ndi.gaussian_filter(w, sigma)
    return np.stack([ndi.gaussian_filter(im[..., c] * w, sigma) for c in range(3)], -1) / np.maximum(den, 1e-6)[..., None], den
B, den = fill(25)
B2, den2 = fill(80)
B = np.where((den > 0.05)[..., None], B, B2)
diff = np.linalg.norm(im - B, axis=2)

# enclosed flat regions that look like sky (e.g. inside the aileron spade triangles)
areas = ndi.sum(np.ones_like(flat), lab, range(1, n + 1))
mdiff = ndi.mean(diff, lab, range(1, n + 1))
encl = np.zeros(n + 1, bool)
encl[1:] = (mdiff < 14) & (areas > 30)
encl[border] = False
sky |= encl[lab] & flat

mx, mn = im.max(2), im.min(2)
sat = (mx - mn) / np.maximum(mx, 1)
smoke = (X > 0.86*W) & (Y > 0.6*H) & (sat < 0.2) & (mx > 60)
sky |= smoke
fg = ~sky
fg = ndi.binary_opening(fg, iterations=1)
lab2, n2 = ndi.label(fg)
sizes = ndi.sum(fg, lab2, range(1, n2 + 1))
main = lab2 == (1 + int(np.argmax(sizes)))
main = ndi.binary_fill_holes(main) & ~(sky & ~ndi.binary_fill_holes(main) | (encl[lab] & flat))

# soft edge: band around the boundary uses colour distance to local sky
band = ndi.binary_dilation(main, iterations=2) & ~ndi.binary_erosion(main, iterations=2)
soft = np.clip((diff - 6) / (34 - 6), 0, 1)
alpha = main.astype(float)
alpha[band] = soft[band]
alpha = ndi.gaussian_filter(alpha, 0.5)

a = np.clip(alpha, 1e-3, 1)[..., None]
fgc = np.clip((im - (1 - a) * B) / a, 0, 255)
fgc = np.where(alpha[..., None] > 0.97, im, fgc)
img = Image.fromarray(np.dstack([fgc, alpha * 255]).astype(np.uint8), "RGBA")
img = img.crop(img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
img.thumbnail((1100, 1100), Image.LANCZOS)
img.save(out, optimize=True)
print(img.size, "flat comps", n)
for name, col in (("dark", (23, 18, 26)), ("light", (244, 240, 234))):
    bg = Image.new("RGBA", img.size, col + (255,)); bg.alpha_composite(img); bg.convert("RGB").save(f"{prev}-{name}.png")
