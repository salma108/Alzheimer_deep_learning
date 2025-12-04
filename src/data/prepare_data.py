import os, random, shutil
from pathlib import Path
from PIL import Image
from tqdm import tqdm
from src.utils.config import load_config

def split_and_clean():
  cfg = load_config()
  random.seed(cfg.training.seed)

  raw_dir = Path(cfg.dataset.raw_dir)
  split_dir = Path(cfg.dataset.split_dir)
  train_dir = split_dir / "train"
  val_dir = split_dir / "val"
  test_dir = split_dir / "test"
  for d in [train_dir, val_dir, test_dir]:
    d.mkdir(parents=True, exist_ok=True)

  classes = [c for c in os.listdir(raw_dir) if (raw_dir / c).is_dir()]
  print("Classes :", classes)

  for cls in classes:
    src = raw_dir / cls
    dst_tr, dst_va, dst_te = train_dir/cls, val_dir/cls, test_dir/cls
    for d in [dst_tr, dst_va, dst_te]:
      d.mkdir(parents=True, exist_ok=True)
    files = [f for f in os.listdir(src) if (src/f).is_file()]
    random.shuffle(files)
    n_total = len(files)
    n_train = int(cfg.dataset.train_ratio * n_total)
    n_val = int(cfg.dataset.val_ratio * n_total)
    tr = files[:n_train]
    va = files[n_train:n_train+n_val]
    te = files[n_train+n_val:]
    for f in tr: shutil.copy(src/f, dst_tr/f)
    for f in va: shutil.copy(src/f, dst_va/f)
    for f in te: shutil.copy(src/f, dst_te/f)
    print(f"{cls}: {len(tr)} train / {len(va)} val / {len(te)} test")

  # nettoyage images corrompues sur train
  for cls in classes:
    cls_dir = train_dir/cls
    for f in tqdm(os.listdir(cls_dir), desc=f"Check {cls}"):
      p = cls_dir/f
      try:
        Image.open(p).verify()
      except Exception:
        print("Suppression corrompue:", p)
        os.remove(p)

if __name__ == "__main__":
  split_and_clean()
