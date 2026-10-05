"""Build CIFAR-10-LT (imbalance ratio 100) from the *official* CIFAR-10 dataset.

Protocol (fully deterministic, see DATA.md):
  * train : exponential profile n_c = floor(5000 * (1/IR) ** (c / 9)) images per class,
            sampled from the official CIFAR-10 training set -> 12,406 images for IR=100.
  * val   : 50 images / class (balanced, 500 total) drawn from the official training
            images that were NOT selected for the long-tailed train set (no overlap).
  * test  : the official CIFAR-10 test set (10,000 images, 1,000 / class, balanced).
"""
import argparse
import json
import os

import numpy as np

CLASS_NAMES = ["airplane", "automobile", "bird", "cat", "deer",
               "dog", "frog", "horse", "ship", "truck"]
MANY, MEDIUM, FEW = [0, 1, 2], [3, 4, 5, 6], [7, 8, 9]
CIFAR_MEAN = np.array([0.4914, 0.4822, 0.4465], dtype=np.float32)
CIFAR_STD = np.array([0.2470, 0.2435, 0.2616], dtype=np.float32)


def lt_counts(imbalance=100, n_max=5000, num_classes=10):
    return [int(n_max * (1.0 / imbalance) ** (c / (num_classes - 1))) for c in range(num_classes)]


def build(root="data", imbalance=100, seed=0, val_per_class=50):
    from torchvision.datasets import CIFAR10

    tr = CIFAR10(root=os.path.join(root, "cifar10_official"), train=True, download=True)
    te = CIFAR10(root=os.path.join(root, "cifar10_official"), train=False, download=True)
    x_all, y_all = np.asarray(tr.data), np.asarray(tr.targets)
    rng = np.random.RandomState(seed)
    counts = [min(n, 5000 - val_per_class) for n in lt_counts(imbalance)]  # keep 50/class free for val

    tr_idx, va_idx = [], []
    for c in range(10):
        idx = rng.permutation(np.where(y_all == c)[0])
        tr_idx += idx[:counts[c]].tolist()
        # validation comes from images not used for training (end of the permutation)
        va_idx += idx[-val_per_class:].tolist()
    tr_idx, va_idx = np.array(tr_idx), np.array(va_idx)
    assert len(set(tr_idx) & set(va_idx)) == 0, "train/val overlap"

    out = dict(
        x_train=x_all[tr_idx], y_train=y_all[tr_idx],
        x_val=x_all[va_idx], y_val=y_all[va_idx],
        x_test=np.asarray(te.data), y_test=np.asarray(te.targets),
        train_idx=tr_idx, val_idx=va_idx,
    )
    os.makedirs(root, exist_ok=True)
    path = os.path.join(root, f"cifar10_lt_ir{imbalance}_seed{seed}.npz")
    np.savez_compressed(path, **out)
    with open(os.path.join(root, f"cifar10_lt_ir{imbalance}_stats.json"), "w") as f:
        json.dump({"imbalance_ratio": imbalance, "seed": seed, "train_counts": counts,
                   "num_train": int(len(tr_idx)), "num_val": int(len(va_idx)),
                   "num_test": int(len(out["y_test"]))}, f, indent=2)
    print("train counts:", counts, "total", len(tr_idx))
    print("saved", path)
    return path


def load(path):
    d = np.load(path)
    return {k: d[k] for k in d.files}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="data")
    ap.add_argument("--imbalance", type=int, default=100)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()
    build(a.root, a.imbalance, a.seed)
