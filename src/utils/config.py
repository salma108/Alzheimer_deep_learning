from dataclasses import dataclass
import yaml
import torch

@dataclass
class DatasetConfig:
    raw_dir: str
    split_dir: str
    img_size: int
    train_ratio: float
    val_ratio: float
    test_ratio: float

@dataclass
class TrainingConfig:
    batch_size: int
    num_workers: int
    epochs_resnet: int
    epochs_densenet: int
    epochs_vit: int
    lr_resnet: float
    lr_densenet: float
    lr_vit: float
    patience: int
    seed: int
    mixup_alpha: float
    cutmix_alpha: float
    mix_prob: float

@dataclass
class ModelConfig:
    num_labels: int

@dataclass
class GlobalConfig:
    dataset: DatasetConfig
    training: TrainingConfig
    models: ModelConfig

def load_config(path: str = "params.yaml") -> GlobalConfig:
    with open(path, "r", encoding="utf-8") as f:
        params = yaml.safe_load(f)

    # 🔥 Correction : forcer conversion en float
    for key in ["lr_resnet", "lr_densenet", "lr_vit"]:
        val = params["training"][key]
        if isinstance(val, str):
            params["training"][key] = float(val)

    return GlobalConfig(
        dataset=DatasetConfig(**params["dataset"]),
        training=TrainingConfig(**params["training"]),
        models=ModelConfig(**params["models"]),
    )

def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
