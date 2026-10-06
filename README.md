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

## 1. End-to-End Project Pipeline

The repository implements a fully automated, reproducible 5-stage pipeline for benchmarking class-conditional generative models against conventional augmentation under extreme class imbalance:

```
[Official CIFAR-10]
        │
        ▼ (Stage 1: src/data.py)
┌────────────────────────────────────────────────────────────────────────┐
│  • Train Set (LT, IR=100): 12,356 images [4,950 down to 50 / class]   │
│  • Validation Set:           500 images [Disjoint, 50 / class]        │
│  • Test Set:              10,000 images [Balanced, 1,000 / class]     │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
                    ▼ (Stage 2: src/train_gan.py)    │
┌──────────────────────────────────────────────┐     │
│  Class-Conditional ResNet GAN                │     │
│  • Spectral Normalization + Projection D     │     │
│  • Differentiable Augmentation (DiffAugment) │     │
│  • Class-Balanced Batch Sampler + EMA        │     │
└───────────────────┬──────────────────────────┘     │
                    │                                │
                    ▼ (Stage 3: src/generate_synthetic.py)
┌──────────────────────────────────────────────┐     │
│  Synthetic Image Generation                  │     │
│  • Pad tail classes up to threshold T        │     │
│    (T = 1,000 or T = 5,000 images / class)   │     │
└───────────────────┬──────────────────────────┘     │
                    │                                │
                    └────────────────┬───────────────┘
                                     │
                                     ▼ (Stage 4: src/train_classifier.py)
┌────────────────────────────────────────────────────────────────────────┐
│  Standardized ResNet-32 Benchmark (467K Parameters)                    │
│  • Baseline (ERM)                  • Random Oversampling (ROS)         │
│  • Conventional Aug (Crop/Flip)    • ROS + Conventional Aug            │
│  • cGAN Synthetic (T=1000, 5000)   • cGAN Syn + Conv Aug (Hybrid)      │
└────────────────────────────────────┬───────────────────────────────────┘
                                     │
                                     ▼ (Stage 5: src/aggregate.py & src/build_report.py)
┌────────────────────────────────────────────────────────────────────────┐
│  Evaluation, Diagnostic Metrics & Deliverables                         │
│  • Balanced Accuracy, Macro-F1, Many / Medium / Few-shot Recall        │
│  • Per-Class Recall Curves & Normalized Confusion Matrices             │
│  • Automated PDF Report Compilation: Group25_Project19_Report.pdf      │
└────────────────────────────────────────────────────────────────────────┘
```

### Pipeline Stage Details:
1. **Stage 1 — Data Preparation & Deterministic Long-Tailed Induction (`src/data.py`):**
   Downloads official CIFAR-10 and applies exponential decay ($IR=100$) following Cui et al. (CVPR 2019), creating a strictly isolated 12,356-image long-tailed training set, 500 balanced validation images, and 10,000 balanced test images.
2. **Stage 2 — Class-Conditional Generative Modeling (`src/train_gan.py`):**
   Trains a Spectral-Normalized ResNet cGAN with Projection Discriminator and DiffAugment strictly on the 12,356 training images (zero validation/test exposure) using class-balanced batch sampling and EMA.
3. **Stage 3 — Synthetic Sampling & Dataset Balancing (`src/generate_synthetic.py`):**
   Samples high-fidelity synthetic images from $G_{ema}$ to pad minority classes up to target cardinality thresholds ($T=1000$ and $T=5000$).
4. **Stage 4 — Downstream Classifier Benchmarking (`src/train_classifier.py`, `src/run_experiments.py`):**
   Optimizes ResNet-32 across all 6 baseline and countermeasure configurations over multiple random seeds ($s \in \{0, 1, 2\}$) under identical SGD and cosine annealing schedules.
5. **Stage 5 — Statistical Aggregation & Report Generation (`src/aggregate.py`, `src/build_report.py`):**
   Aggregates multi-seed metrics ($\mu \pm \sigma$), generates publication-quality figures (`figures/`), and compiles the complete 11-page examination report [`Group25_Project19_Report.pdf`](Group25_Project19_Report.pdf).

---

## 2. Repository Structure

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

## 3. Requirements & Installation

Hardware requirement: NVIDIA GPU with CUDA support (tested on RTX 3060 Laptop & CUDA 12.4).

```bash
git clone https://github.com/hunghh22ba13147-pixel/DL2026-Group25-Project19.git
cd DL2026-Group25-Project19

python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

---

## 4. Step-by-Step Reproduction Guide

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

## 5. Key Experimental Results (CIFAR-10-LT, IR=100)

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

## 6. Artifacts and Deliverables
- **Dataset Information**: See [DATA.md](DATA.md)
- **Trained Generator Checkpoints & Synthetic Images**: Checkpoints stored under `checkpoints/cgan/G_ema.pt`
- **Project Report**: [`Group25_Project19_Report.pdf`](Group25_Project19_Report.pdf) (11 pages, formatted according to official USTH rubric)

