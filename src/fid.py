"""Per-class FID between synthetic images and the full official CIFAR-10 training images of the same class
(5,000 real images / class, used ONLY as a reference distribution for measuring image quality).
Needs: pip install pytorch-fid  (Inception weights are downloaded automatically)."""
import argparse
import json

import numpy as np
import torch
from scipy import linalg

from data import CLASS_NAMES, load


@torch.no_grad()
def feats(model, x, dev, bs=200):
    out = []
    for i in range(0, len(x), bs):
        b = torch.from_numpy(x[i:i + bs]).permute(0, 3, 1, 2).float().div(255).to(dev)
        out.append(model(b)[0].squeeze(-1).squeeze(-1).cpu().numpy())
    return np.concatenate(out)


def fid(f1, f2):
    m1, m2 = f1.mean(0), f2.mean(0)
    s1, s2 = np.cov(f1, rowvar=False), np.cov(f2, rowvar=False)
    cs, _ = linalg.sqrtm(s1.dot(s2), disp=False)
    cs = cs.real
    return float(((m1 - m2) ** 2).sum() + np.trace(s1) + np.trace(s2) - 2 * np.trace(cs))


def main():
    from pytorch_fid.inception import InceptionV3
    from torchvision.datasets import CIFAR10
    ap = argparse.ArgumentParser()
    ap.add_argument("--syn", default="data/synthetic_cgan.npz")
    ap.add_argument("--n", type=int, default=1000, help="synthetic images per class")
    ap.add_argument("--out", default="results/fid.json")
    a = ap.parse_args()
    dev = torch.device("cuda")
    net = InceptionV3([InceptionV3.BLOCK_INDEX_BY_DIM[2048]]).to(dev).eval()
    tr = CIFAR10("data/cifar10_official", train=True, download=True)
    xa, ya = np.asarray(tr.data), np.asarray(tr.targets)
    syn = np.load(a.syn)
    lt = load("data/cifar10_lt_ir100_seed0.npz")
    res = {}
    for c in range(10):
        ref = feats(net, xa[ya == c], dev)
        fs = feats(net, syn["x"][syn["y"] == c][:a.n], dev)
        # reference point: the (small) real long-tailed train set of the class vs the same reference
        fr = feats(net, lt["x_train"][lt["y_train"] == c], dev)
        res[CLASS_NAMES[c]] = {"fid_synthetic": fid(fs, ref), "n_real_lt": int(len(fr))}
        print(CLASS_NAMES[c], res[CLASS_NAMES[c]], flush=True)
    json.dump(res, open(a.out, "w"), indent=2)


if __name__ == "__main__":
    main()
