"""Aggregate results/*.json -> results/summary.md, results/summary.csv and figures."""
import glob
import json
import os
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

CLASS = ["airplane", "automobile", "bird", "cat", "deer", "dog", "frog", "horse", "ship", "truck"]
NAMES = {"baseline": "Baseline (CE)", "aug": "Conventional aug.", "ros": "Random oversampling",
         "ros_aug": "Oversampling + aug.", "syn": "cGAN synthetic", "syn_aug": "cGAN synthetic + aug."}


def key(r):
    return (r["method"], r["target"])


def label(k):
    return NAMES[k[0]] + (f" (T={k[1]})" if k[1] else "")


def main():
    runs = defaultdict(list)
    for f in glob.glob("results/*_s*.json"):
        r = json.load(open(f)); runs[key(r)].append(r)
    order = sorted(runs, key=lambda k: (list(NAMES).index(k[0]), k[1] or 0))
    ms = lambda v: f"{100 * np.mean(v):.2f} ± {100 * np.std(v):.2f}"
    rows = ["| Method | #seeds | Acc (balanced) | Macro-F1 | Many | Medium | Few |", "|---|---|---|---|---|---|---|"]
    csv = ["method,target,seeds,acc,acc_std,f1,f1_std,many,medium,few"]
    for k in order:
        R = runs[k]
        g = lambda n: [r[n] for r in R]
        rows.append(f"| {label(k)} | {len(R)} | {ms(g('acc'))} | {ms(g('macro_f1'))} | {ms(g('many'))} | "
                    f"{ms(g('medium'))} | {ms(g('few'))} |")
        csv.append(",".join(map(str, [k[0], k[1], len(R), np.mean(g('acc')), np.std(g('acc')), np.mean(g('macro_f1')),
                                      np.std(g('macro_f1')), np.mean(g('many')), np.mean(g('medium')), np.mean(g('few'))])))
    open("results/summary.md", "w").write("\n".join(rows) + "\n")
    open("results/summary.csv", "w").write("\n".join(csv) + "\n")
    print("\n".join(rows))

    # per-class recall figure (main methods)
    os.makedirs("figures", exist_ok=True)
    main_keys = [k for k in order if k[1] in (None, 5000, 1000)]
    plt.figure(figsize=(11, 4.5)); w = 0.8 / max(len(main_keys), 1)
    for i, k in enumerate(main_keys):
        rec = np.mean([r["recall"] for r in runs[k]], 0)
        plt.bar(np.arange(10) + i * w, rec, w, label=label(k))
    plt.xticks(np.arange(10) + 0.4, CLASS, rotation=30); plt.ylabel("Recall (test)")
    plt.legend(fontsize=6, ncol=2); plt.tight_layout(); plt.savefig("figures/per_class_recall.png", dpi=200)
    plt.close()

    # ablation on T
    abl = defaultdict(dict)
    for k in runs:
        if k[1]:
            abl[k[0]][k[1]] = np.mean([r["macro_f1"] for r in runs[k] if r["seed"] == 0])
    if abl:
        plt.figure(figsize=(5, 3.5))
        for m, d in abl.items():
            xs = sorted(d); plt.plot(xs, [100 * d[x] for x in xs], "o-", label=NAMES[m])
        for m in ("baseline", "ros"):
            if (m, None) in runs:
                v = np.mean([r["macro_f1"] for r in runs[(m, None)] if r["seed"] == 0]) * 100
                plt.axhline(v, ls="--", c="gray", lw=0.8); plt.text(xs[0], v, NAMES[m], fontsize=6)
        plt.xscale("log"); plt.xlabel("Images per class after adding synthetic (T)"); plt.ylabel("Test macro-F1 (%)")
        plt.legend(fontsize=7); plt.tight_layout(); plt.savefig("figures/ablation_T.png", dpi=200); plt.close()

    # confusion matrices for a few methods (seed 0)
    sel = [k for k in order if k in [("baseline", None), ("ros_aug", None), ("syn_aug", 5000), ("syn", 5000)]]
    if sel:
        fig, ax = plt.subplots(1, len(sel), figsize=(4.2 * len(sel), 4))
        ax = np.atleast_1d(ax)
        for a_, k in zip(ax, sel):
            cm = np.array([r for r in runs[k] if r["seed"] == 0][0]["confusion"], float)
            cm /= cm.sum(1, keepdims=True)
            a_.imshow(cm, cmap="Blues", vmin=0, vmax=1); a_.set_title(label(k), fontsize=8)
            a_.set_xticks(range(10)); a_.set_yticks(range(10)); a_.set_xticklabels(CLASS, rotation=90, fontsize=6)
            a_.set_yticklabels(CLASS, fontsize=6)
        plt.tight_layout(); plt.savefig("figures/confusion_matrices.png", dpi=200); plt.close()


if __name__ == "__main__":
    main()
