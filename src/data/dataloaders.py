from pathlib import Path
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from src.utils.config import load_config
from src.data.preprocessing import get_transforms

def create_dataloaders():
  cfg=load_config()
  train_tf,val_tf=get_transforms(cfg.dataset.img_size)
  split=Path(cfg.dataset.split_dir)
  train_ds=ImageFolder(split/'train',transform=train_tf)
  val_ds=ImageFolder(split/'val',transform=val_tf)
  test_ds=ImageFolder(split/'test',transform=val_tf)
  train_dl=DataLoader(train_ds,batch_size=cfg.training.batch_size,shuffle=True,
                      num_workers=cfg.training.num_workers,pin_memory=True)
  val_dl=DataLoader(val_ds,batch_size=cfg.training.batch_size,shuffle=False,
                    num_workers=cfg.training.num_workers,pin_memory=True)
  test_dl=DataLoader(test_ds,batch_size=cfg.training.batch_size,shuffle=False,
                     num_workers=cfg.training.num_workers,pin_memory=True)
  return train_dl,val_dl,test_dl,train_ds.classes
