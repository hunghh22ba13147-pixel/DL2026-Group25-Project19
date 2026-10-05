"""Train a class-conditional GAN (SN-ResNet projection cGAN + DiffAugment + EMA) on the
long-tailed TRAIN split only (validation / test images are never seen by the generator).

Real batches are drawn with class-balanced sampling so that tail classes are learnt as often as head classes.
"""
import argparse
import copy
import os
import time

import numpy as np
import torch
import torch.nn.functional as F

from data import load
from diffaug import diff_augment
from models import Discriminator, Generator


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data/cifar10_lt_ir100_seed0.npz")
    ap.add_argument("--out", default="checkpoints/cgan")
    ap.add_argument("--steps", type=int, default=30000, help="generator steps")
    ap.add_argument("--n_dis", type=int, default=2)
    ap.add_argument("--bs", type=int, default=64)
    ap.add_argument("--nz", type=int, default=128)
    ap.add_argument("--gch", type=int, default=128)
    ap.add_argument("--dch", type=int, default=64)
    ap.add_argument("--seed", type=int, default=0)
    a = ap.parse_args()

    torch.manual_seed(a.seed); np.random.seed(a.seed)
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    os.makedirs(a.out, exist_ok=True)

    d = load(a.data)
    x = torch.from_numpy(d["x_train"]).permute(0, 3, 1, 2).float().div(127.5).sub(1).to(dev)
    y = torch.from_numpy(d["y_train"]).long().to(dev)
    cls_idx = [torch.where(y == c)[0] for c in range(10)]
    max_n = max(len(i) for i in cls_idx)
    lens = torch.tensor([len(i) for i in cls_idx], device=dev)
    table = torch.stack([torch.cat([i, i.new_zeros(max_n - len(i))]) for i in cls_idx])  # (10, max_n)

    def real_batch():
        yb = torch.randint(0, 10, (a.bs,), device=dev)          # class-balanced
        pos = (torch.rand(a.bs, device=dev) * lens[yb]).long()
        xb = x[table[yb, pos]]
        flip = torch.rand(a.bs, device=dev) < 0.5
        xb = torch.where(flip[:, None, None, None], xb.flip(3), xb)
        return xb, yb

    G, D = Generator(a.nz, ch=a.gch).to(dev), Discriminator(ch=a.dch).to(dev)
    G_ema = copy.deepcopy(G).eval()
    oG = torch.optim.Adam(G.parameters(), 2e-4, betas=(0.0, 0.9))
    oD = torch.optim.Adam(D.parameters(), 2e-4, betas=(0.0, 0.9))
    ac = lambda: torch.autocast("cuda", dtype=torch.bfloat16)

    t0 = time.time()
    for step in range(1, a.steps + 1):
        for _ in range(a.n_dis):
            xr, yr = real_batch()
            with ac():
                with torch.no_grad():
                    xf = G(torch.randn(a.bs, a.nz, device=dev), yr)
                lossD = (F.relu(1 - D(diff_augment(xr), yr).float()).mean()
                         + F.relu(1 + D(diff_augment(xf.float()), yr).float()).mean())
            oD.zero_grad(set_to_none=True); lossD.backward(); oD.step()

        yg = torch.randint(0, 10, (a.bs,), device=dev)
        with ac():
            lossG = -D(diff_augment(G(torch.randn(a.bs, a.nz, device=dev), yg).float()), yg).float().mean()
        oG.zero_grad(set_to_none=True); lossG.backward(); oG.step()

        with torch.no_grad():
            for pe, p in zip(G_ema.parameters(), G.parameters()):
                pe.mul_(0.999).add_(p, alpha=0.001)
            for be, b in zip(G_ema.buffers(), G.buffers()):
                be.copy_(b)

        if step % 500 == 0:
            print(f"step {step}/{a.steps} lossD {lossD.item():.3f} lossG {lossG.item():.3f} "
                  f"[{time.time() - t0:.0f}s]", flush=True)
        if step % 5000 == 0 or step == a.steps:
            torch.save({"G_ema": G_ema.state_dict(), "nz": a.nz, "gch": a.gch, "step": step}, os.path.join(a.out, "G_ema.pt"))
    print("done")


if __name__ == "__main__":
    main()
