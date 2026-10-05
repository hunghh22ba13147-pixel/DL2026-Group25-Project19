# DATA.md — Dataset description and reproduction

## 1. Source (official dataset)
- **CIFAR-10** (Krizhevsky, 2009) — official page: <https://www.cs.toronto.edu/~kriz/cifar.html>
  (`cifar-10-python.tar.gz`, 60,000 32×32 RGB images, 10 classes, 50,000 train / 10,000 test).
- Downloaded automatically by `torchvision.datasets.CIFAR10(download=True)` (torchvision ≥ 0.20, MD5-checked).
- **CIFAR-10-LT** is *not* downloaded from a third party: it is derived deterministically from the official
  files by `src/data.py` (protocol of Cui et al., CVPR 2019; Cao et al., NeurIPS 2019).

## 2. Data splits (imbalance ratio 100, seed 0)
| Split | Source | Size | Distribution |
|---|---|---|---|
| Train (long-tailed) | official CIFAR-10 train | **12,356** | `[4950, 2997, 1796, 1077, 645, 387, 232, 139, 83, 50]` (airplane … truck) |
| Validation | official CIFAR-10 train, images **not** in the LT train set | 500 | 50 / class (balanced) |
| Test | official CIFAR-10 test | 10,000 | 1,000 / class (balanced) |

- Profile: `n_c = floor(5000 · (1/100)^(c/9))`, capped at 4,950 so that 50 images/class stay free for validation
  (imbalance ratio = 4950/50 = 99 ≈ 100).
- Per class, a seeded random permutation (`np.random.RandomState(0)`) of the official training images is drawn: the first
  `n_c` images form the train set, the last 50 form the validation set (an assertion checks that they never overlap).
- Class groups used in the analysis: **many** = airplane, automobile, bird; **medium** = cat, deer, dog, frog;
  **few** = horse, ship, truck.
- The test set is used **once per run** (after choosing the checkpoint on the validation set).
  The generative model only ever sees the long-tailed *train* split.

## 3. Preprocessing
- Images are kept as `uint8` arrays; the classifier normalises with CIFAR-10 mean `(0.4914, 0.4822, 0.4465)` and
  std `(0.2470, 0.2435, 0.2616)` on-the-fly.
- Conventional augmentation (methods `aug`, `ros_aug`, `syn_aug`): random crop 32 (padding 4) + horizontal flip.
- cGAN: images scaled to `[-1, 1]`, random horizontal flip + DiffAugment (colour, translation, cutout).

## 4. Synthetic dataset (generated, not downloaded)
- `src/generate_synthetic.py` generates **5,000 images per class** (50,000 total, 32×32) from the trained conditional GAN
  (`checkpoints/cgan/G_ema.pt`); experiments use the first `T − n_c` images of class `c` (T = target images/class).
- Download link of the generated data and generator weights: **<ADD_LINK_HERE>** (Google Drive / HuggingFace).

## 5. Reproduce
```bash
pip install -r requirements.txt
python src/data.py                       # -> data/cifar10_lt_ir100_seed0.npz (+ stats json)
python src/train_gan.py --steps 15000    # -> checkpoints/cgan/G_ema.pt
python src/generate_synthetic.py         # -> data/synthetic_cgan.npz, figures/synthetic_grid.png
```
