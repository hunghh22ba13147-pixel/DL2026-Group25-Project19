"""Generate synthetic images (per_class for every class) with the trained EMA generator and save
them as uint8 arrays plus a 10x10 preview grid. The generator is used in eval mode (BN running statistics)."""
import argparse
import os

import numpy as np
import torch

from data import CLASS_NAMES
from models import Generator


@torch.no_grad()
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default="checkpoints/cgan/G_ema.pt")
    ap.add_argument("--per_class", type=int, default=5000)
    ap.add_argument("--out", default="data/synthetic_cgan.npz")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--grid", default="figures/synthetic_grid.png")
    a = ap.parse_args()
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(a.seed)
    ck = torch.load(a.ckpt, map_location=dev)
    G = Generator(ck["nz"], ch=ck.get("gch", 256)).to(dev).eval()
    G.load_state_dict(ck["G_ema"])
    xs, ys = [], []
    for c in range(10):
        imgs = []
        for i in range(0, a.per_class, 500):
            n = min(500, a.per_class - i)
            z = torch.randn(n, ck["nz"], device=dev)
            im = G(z, torch.full((n,), c, device=dev, dtype=torch.long))
            imgs.append(((im + 1) * 127.5).round().clamp(0, 255).byte().permute(0, 2, 3, 1).cpu().numpy())
        xs.append(np.concatenate(imgs)); ys.append(np.full(a.per_class, c))
    np.savez_compressed(a.out, x=np.concatenate(xs), y=np.concatenate(ys))
    print("saved", a.out)

    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(os.path.dirname(a.grid), exist_ok=True)
    fig, ax = plt.subplots(10, 10, figsize=(10, 10.5))
    for c in range(10):
        for j in range(10):
            ax[c, j].imshow(xs[c][j]); ax[c, j].axis("off")
        ax[c, 0].set_title(CLASS_NAMES[c], fontsize=8, loc="left")
    plt.tight_layout(); plt.savefig(a.grid, dpi=150)


if __name__ == "__main__":
    main()
