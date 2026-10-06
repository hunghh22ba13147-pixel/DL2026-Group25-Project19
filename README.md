# DL2026-Group25-Project19: Can Synthetic Images Improve Imbalanced Classification?

[![PyTorch](https://img.shields.io/badge/PyTorch-2.5+-ee4c2c.svg)](https://pytorch.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Official source code and artifacts for the Final Project in Deep Learning (Academic Year 2026–2027, USTH).

- **Group ID**: Group 25
- **Project ID**: Project 19
- **Project Topic**: *Can Synthetic Images Improve Imbalanced Classification?*  
- **Research Target**: Benchmark class-conditional Generative Adversarial Networks (cGANs) against standard class-imbalance countermeasures (Conventional Data Augmentation, Random Oversampling) on CIFAR-10-LT (Imbalance Ratio = 100).

### Team Members (Group 25 - USTH)
| Member Name | Student ID | Email | Major | Role |
|---|---|---|:---:|---|
| **Hà Hiệp Hùng** | 22BA13147 | hunghh.22ba13147@usth.edu.vn | ICT | Project Leader, cGAN Architecture & DiffAugment |
| **Trương Việt Hoàng** | 22BA13145 | hoangtv.22ba13145@usth.edu.vn | ICT | Augmentation Specialist, Geometric & ROS Benchmarks |
| **Vũ Công Thành** | 22BA13290 | thanhvc.22ba13290@usth.edu.vn | ICT | Model Training, ResNet-32 Backbone & Optimizer |
| **Vương Minh Tuấn** | 22BA13316 | tuanvm.22ba13316@usth.edu.vn | ICT | Report & Documentation, Statistical Aggregation |
| **Nguyễn Tiến Đạt** | 22BA13066 | datnt.22ba13066@usth.edu.vn | ICT | Report & Documentation, Statistical Aggregation |
| **Nguyễn Trung Hiếu** | 22BA13138 | hieunt.22ba13138@usth.edu.vn | ICT | Generative Experiments, Synthetic Data Sampling |
| **Đặng Bình Dương** | 22BA13091 | duongdb.22ba13091@usth.edu.vn | DS | Data Engineering & Pipeline Architecture |

---

## 1. Repository Structure

```
DL2026-Group25-Project19/
├── data/                      # Dataset builders and downloaded official CIFAR-10 data
├── checkpoints/               # Trained models and cGAN weights (G_ema.pt)
├── figures/                   # Confusion matrices, recall graphs, synthetic samples
├── results/                   # JSON logs, summary CSV and summary markdown
├── src/                       # Production-grade Python source files
│   ├── data.py                # Deterministic CIFAR-10-LT split generator
│   ├── models.py              # ResNet-32 classifier & Spectral Norm Projection cGAN
│   ├── diffaug.py             # Differentiable Augmentation (DiffAugment)
│   ├── train_gan.py           # Class-balanced cGAN trainer (only seen on training set)
│   ├── generate_synthetic.py  # High-throughput synthetic image sampler
│   ├── train_classifier.py    # Standardized ResNet-32 classifier training engine
│   ├── run_experiments.py     # Reproducibility batch runner
│   ├── fid.py                 # Per-class Fréchet Inception Distance calculator
│   └── aggregate.py           # Statistical aggregation and visualization tool
├── DATA.md                    # Official dataset documentation & reproduction procedures
├── requirements.txt           # Python library dependencies
└── README.md                  # This file
```

---

## 2. Requirements & Installation

Hardware requirement: NVIDIA GPU with CUDA support (tested on RTX 3050 Ti & Tesla T4).

```bash
git clone https://github.com/YourOrg/DL2026-Group25-Project19.git
cd DL2026-Group25-Project19

python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 3. Step-by-Step Reproduction Guide

### Step 1: Prepare Long-Tailed Dataset (CIFAR-10-LT, IR=100)
Run the automated dataset builder. It will download the official CIFAR-10 dataset and apply the standard Cui et al. exponential decay profile:
```bash
python src/data.py --root data --imbalance 100 --seed 0
```
This produces `12,356` training images, `500` balanced validation images, and `10,000` balanced test images.

### Step 2: Train Class-Conditional GAN
Train the Spectral Normalized Projection cGAN with DiffAugment strictly on the LT training set:
```bash
python src/train_gan.py --data data/cifar10_lt_ir100_seed0.npz --steps 15000
```

### Step 3: Generate Synthetic Dataset
Sample synthetic images for minority classes to pad classes up to the target volume:
```bash
python src/generate_synthetic.py --ckpt checkpoints/cgan/G_ema.pt --per_class 5000
```

### Step 4: Run Classifier Experiments
Execute the standardized training runs (ResNet-32, Cosine LR, 10,000 SGD steps):
```bash
# 1. Real data benchmarks (Baseline, Conventional Augmentation, ROS, ROS+Aug across 3 seeds)
python src/run_experiments.py real

# 2. Synthetic augmentation benchmarks
python src/run_experiments.py syn
```

### Step 5: Aggregate Results and Generate Figures
Generate summary tables and paper-ready figures:
```bash
python src/aggregate.py
```
Outputs will be generated in `results/summary.md` and `figures/`.

---

## 4. Key Experimental Results (CIFAR-10-LT, IR=100)

Evaluated on the official balanced test set (10,000 images, 10 classes):

| Method | # Seeds | Balanced Acc (%) | Macro-F1 (%) | Many (0-2) | Medium (3-6) | Few (7-9) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Baseline (CE)** | 3 | 54.28 ± 2.13 | 52.14 ± 3.02 | 83.03% | 51.09% | 29.78% |
| **Conventional Augmentation** | 3 | 70.01 ± 0.32 | 69.60 ± 0.13 | 92.18% | 69.61% | 48.38% |
| **Random Oversampling (ROS)** | 3 | 45.23 ± 0.31 | 42.26 ± 1.54 | 70.01% | 44.19% | 21.83% |
| **Oversampling + Augmentation** | 3 | **70.09 ± 1.84** | **69.79 ± 1.99** | 89.37% | 69.67% | **51.37%** |
| **cGAN Synthetic (T=1000)** | 1 | 50.26 | 46.40 | 85.67% | 48.85% | 16.73% |
| **cGAN Synthetic (T=5000)** | 1 | 47.52 | 43.48 | 83.17% | 44.72% | 15.60% |

### Core Finding
> **Can Synthetic Images Improve Imbalanced Classification?**  
> Under extreme imbalance ($IR=100$), raw synthetic images from class-conditional GANs do **not** outperform conventional data augmentation or oversampling. In fact, high synthetic ratios introduce domain shift and distribution distortion on extreme minority classes (causing Mode Collapse & high FID), degrading tail recall. Conventional spatial augmentations remain significantly more sample-efficient and robust.

---

## 5. Artifacts and Links
- **Dataset Information**: See [DATA.md](DATA.md)
- **Trained Generator Checkpoints & Synthetic Images**: [Google Drive / Hugging Face Link](https://drive.google.com/)
- **Project Report**: `Group25_Project19_Report.pdf` (14 pages, formatted according to official template)
