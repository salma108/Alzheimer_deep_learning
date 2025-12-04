import random, numpy as np, torch
from PIL import ImageEnhance
from torchvision import transforms

class RandAugment:
  def __init__(self, n=2, m=9):
    self.n=n; self.m=m
    self.ops=[self._rot,self._bri,self._con,self._sha,self._col]

  def _rot(self,img):
    deg=(self.m/30)*30
    return img.rotate(random.uniform(-deg,deg))

  def _bri(self,img):
    f=1+(self.m/30)*0.5
    return ImageEnhance.Brightness(img).enhance(f)

  def _con(self,img):
    f=1+(self.m/30)*0.5
    return ImageEnhance.Contrast(img).enhance(f)

  def _sha(self,img):
    f=1+(self.m/30)*0.5
    return ImageEnhance.Sharpness(img).enhance(f)

  def _col(self,img):
    f=1+(self.m/30)*0.5
    return ImageEnhance.Color(img).enhance(f)

  def __call__(self,img):
    for op in random.choices(self.ops,k=self.n):
      img=op(img)
    return img

class MixUpCutMix:
  def __init__(self,mixup_alpha=0.2,cutmix_alpha=1.0,prob=0.5):
    self.mixup_alpha=mixup_alpha
    self.cutmix_alpha=cutmix_alpha
    self.prob=prob

  def mixup(self,x,y):
    bs=x.size(0)
    lam=np.random.beta(self.mixup_alpha,self.mixup_alpha)
    idx=torch.randperm(bs).to(x.device)
    mx=lam*x+(1-lam)*x[idx]
    return mx,y,y[idx],lam

  def cutmix(self,x,y):
    bs=x.size(0)
    lam=np.random.beta(self.cutmix_alpha,self.cutmix_alpha)
    idx=torch.randperm(bs).to(x.device)
    _,_,H,W=x.size()
    cr=(1-lam)**0.5
    cw,ch=int(W*cr),int(H*cr)
    cx,cy=np.random.randint(0,W),np.random.randint(0,H)
    x1,y1=max(cx-cw//2,0),max(cy-ch//2,0)
    x2,y2=min(cx+cw//2,W),min(cy+ch//2,H)
    x[:,:,y1:y2,x1:x2]=x[idx,:,y1:y2,x1:x2]
    lam=1-((x2-x1)*(y2-y1)/(W*H))
    return x,y,y[idx],lam

  def __call__(self,x,y):
    if random.random()>self.prob:
      return x,y,y,1.0
    if random.random()>0.5:
      return self.mixup(x,y)
    else:
      return self.cutmix(x,y)

def get_transforms(img_size):
  ra=RandAugment()
  train=transforms.Compose([
    transforms.Resize((img_size,img_size)),
    transforms.Lambda(lambda img: ra(img)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(brightness=0.2,contrast=0.2),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3,[0.5]*3),
  ])
  val=transforms.Compose([
    transforms.Resize((img_size,img_size)),
    transforms.ToTensor(),
    transforms.Normalize([0.5]*3,[0.5]*3),
  ])
  return train,val
