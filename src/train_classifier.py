"""Train / evaluate a ResNet-32 on CIFAR-10-LT with one of several imbalance strategies.

methods
  baseline : real data only, plain cross-entropy
  aug      : real data + conventional augmentation (random-crop + horizontal flip)
  ros      : random over-sampling (class-balanced sampling with replacement), no augmentation
  ros_aug  : random over-sampling + conventional augmentation
  syn      : real + cGAN synthetic images (classes padded up to --target images), no augmentation
  syn_aug  : real + cGAN synthetic images + conventional augmentation

All methods use the same architecture, optimiser, and *number of SGD steps* (same compute budget).
The checkpoint is selected on a balanced validation set (accuracy); the balanced test set is used once.
"""
import argparse
import json
import os
import time

import numpy as np
import torch
import torch.nn.functional as F

from data import CIFAR_MEAN, CIFAR_STD, FEW, MANY, MEDIUM, CLASS_NAMES, load
from models import ResNet32


def to_t(x, dev):
    return torch.from_numpy(x).permute(0, 3, 1, 2).contiguous().to(dev)  # uint8 NCHW


def normalize(xb, mean, std):
    return (xb.float().div(255) - mean) / std


def crop_flip(xb, pad=4):
    B, C, H, W = xb.shape
    xp = F.pad(xb, (pad, pad, pad, pad))
    iy = torch.randint(0, 2 * pad + 1, (B,), device=xb.device)
    ix = torch.randint(0, 2 * pad + 1, (B,), device=xb.device)
    ar = torch.arange(H, device=xb.device)
    rows = (iy[:, None] + ar)[:, :, None]
    cols = (ix[:, None] + ar)[:, None, :]
    out = xp[torch.arange(B, device=xb.device)[:, None, None], :, rows, cols].permute(0, 3, 1, 2)
    flip = torch.rand(B, device=xb.device) < 0.5
    return torch.where(flip[:, None, None, None], out.flip(3), out)


@torch.no_grad()
def predict(model, x, mean, std, bs=1000):
    model.eval()
    out = []
    for i in range(0, len(x), bs):
        with torch.autocast("cuda", dtype=torch.bfloat16):
            out.append(model(normalize(x[i:i + bs], mean, std)).argmax(1))
    return torch.cat(out).cpu().numpy()


def metrics(y, p):
    cm = np.zeros((10, 10), dtype=int)
    for t, q in zip(y, p):
        cm[t, q] += 1
    rec = cm.diagonal() / cm.sum(1)
    prec = cm.diagonal() / np.maximum(cm.sum(0), 1)
    f1 = 2 * prec * rec / np.maximum(prec + rec, 1e-12)
    return dict(acc=float((y == p).mean()), macro_f1=float(f1.mean()), recall=rec.tolist(),
                many=float(rec[MANY].mean()), medium=float(rec[MEDIUM].mean()), few=float(rec[FEW].mean()),
                confusion=cm.tolist())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", required=True, choices=["baseline", "aug", "ros", "ros_aug", "syn", "syn_aug"])
    ap.add_argument("--data", default="data/cifar10_lt_ir100_seed0.npz")
    ap.add_argument("--syn", default="data/synthetic_cgan.npz")
    ap.add_argument("--target", type=int, default=1000, help="images per class after adding synthetic data")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--steps", type=int, default=10000)
    ap.add_argument("--bs", type=int, default=128)
    ap.add_argument("--lr", type=float, default=0.1)
    ap.add_argument("--wd", type=float, default=5e-4)
    ap.add_argument("--warmup", type=int, default=500)
    ap.add_argument("--eval_every", type=int, default=250)
    ap.add_argument("--tag", default="")
    ap.add_argument("--out", default="results")
    a = ap.parse_args()

    name = f"{a.method}{('_T' + str(a.target)) if a.method.startswith('syn') else ''}{a.tag}_s{a.seed}"
    os.makedirs(a.out, exist_ok=True)
    if os.path.exists(os.path.join(a.out, name + ".json")):
        print("exists, skipping", name); return

    torch.manual_seed(a.seed); np.random.seed(a.seed)
    dev = torch.device("cuda")
    mean = torch.tensor(CIFAR_MEAN, device=dev).view(1, 3, 1, 1)
    std = torch.tensor(CIFAR_STD, device=dev).view(1, 3, 1, 1)

    d = load(a.data)
    x_tr, y_tr = d["x_train"], d["y_train"]
    n_real = len(y_tr)
    if a.method.startswith("syn"):
        s = np.load(a.syn)
        sx, sy = s["x"], s["y"]
        add_x, add_y = [], []
        for c in range(10):
            need = max(0, a.target - int((y_tr == c).sum()))
            idx = np.where(sy == c)[0][:need]
            add_x.append(sx[idx]); add_y.append(sy[idx])
        x_tr = np.concatenate([x_tr] + add_x); y_tr = np.concatenate([y_tr] + add_y)
    counts = np.bincount(y_tr, minlength=10)
    print(name, "train size", len(y_tr), "counts", counts.tolist(), flush=True)

    X, Y = to_t(x_tr, dev), torch.from_numpy(y_tr).long().to(dev)
    Xv, Yv = to_t(d["x_val"], dev), d["y_val"]
    Xt, Yt = to_t(d["x_test"], dev), d["y_test"]
    use_aug = a.method.endswith("aug")
    if a.method.startswith("ros"):
        w = (1.0 / torch.tensor(counts, dtype=torch.float, device=dev))[Y]    # class-balanced sampling
    else:
        w = torch.ones(len(Y), device=dev)                                    # uniform sampling

    model = ResNet32().to(dev).to(memory_format=torch.channels_last)
    opt = torch.optim.SGD(model.parameters(), lr=a.lr, momentum=0.9, weight_decay=a.wd)

    def lr_at(t):
        if t < a.warmup:
            return a.lr * (t + 1) / a.warmup
        return 0.5 * a.lr * (1 + np.cos(np.pi * (t - a.warmup) / (a.steps - a.warmup)))

    best, best_state, best_step, log = -1, None, 0, []
    t0 = time.time()
    for step in range(a.steps):
        model.train()
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        idx = torch.multinomial(w, a.bs, replacement=True)
        xb, yb = X[idx], Y[idx]
        if use_aug:
            xb = crop_flip(xb)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss = F.cross_entropy(model(normalize(xb, mean, std)), yb)
        opt.zero_grad(set_to_none=True); loss.backward(); opt.step()

        if (step + 1) % a.eval_every == 0:
            va = metrics(Yv, predict(model, Xv, mean, std))["acc"]
            log.append((step + 1, float(loss.item()), va))
            if va >= best:
                best, best_step = va, step + 1
                best_state = {k: v.clone() for k, v in model.state_dict().items()}
            if (step + 1) % 2000 == 0:
                print(f"  step {step + 1} loss {loss.item():.3f} val_bal_acc {va:.4f} best {best:.4f} [{time.time() - t0:.0f}s]", flush=True)

    model.load_state_dict(best_state)
    res = metrics(Yt, predict(model, Xt, mean, std))
    res.update(method=a.method, target=a.target if a.method.startswith("syn") else None, seed=a.seed,
               best_step=best_step, best_val_acc=best, train_size=int(len(y_tr)), train_counts=counts.tolist(),
               n_real=int(n_real), log=log, class_names=CLASS_NAMES, steps=a.steps,
               seconds=time.time() - t0)
    json.dump(res, open(os.path.join(a.out, name + ".json"), "w"))
    print(f"RESULT {name}: acc {res['acc']:.4f} macroF1 {res['macro_f1']:.4f} many {res['many']:.3f} "
          f"med {res['medium']:.3f} few {res['few']:.3f}", flush=True)


if __name__ == "__main__":
    main()
