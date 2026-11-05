import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter
Image.MAX_IMAGE_PIXELS=None
im=Image.open('/tmp/bmdx/shadedrelief.jpg').convert('RGB').resize((5400,2700),Image.LANCZOS)
a=np.asarray(im).astype(np.float32)
L=0.299*a[...,0]+0.587*a[...,1]+0.114*a[...,2]
ocean=(a[...,2]>a[...,0]+20)&(a[...,2]>a[...,1]+2)
land=(~ocean).astype(np.float32)
num=gaussian_filter(L*land,14,mode='wrap'); den=gaussian_filter(land,14,mode='wrap')
B=np.where(den>1e-3,num/np.maximum(den,1e-3),128)
D=(L-B)*land
edge=gaussian_filter(land,1.5); D*=np.clip((edge-0.5)*2,0,1)
print('std',D[land>0].std())
out=(128+D*2.2).clip(0,255).astype(np.uint8)
Image.fromarray(out).resize((4320,2160),Image.LANCZOS).save('/home/claude/atlas/maps/relief.jpg',quality=74,optimize=True)
Image.fromarray(out).crop((2600,500,3600,1100)).save('/tmp/bmdx/relief_crop.png')
import os; print(os.path.getsize('/home/claude/atlas/maps/relief.jpg'))
