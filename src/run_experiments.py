"""Run the full experiment grid (skips finished runs). Usage: python src/run_experiments.py [real|syn|ablation]"""
import subprocess
import sys

PY = sys.executable
SEEDS = [0, 1, 2]


def run(method, seed, target=None, tag=""):
    cmd = [PY, "-u", "src/train_classifier.py", "--method", method, "--seed", str(seed)]
    if target:
        cmd += ["--target", str(target)]
    if tag:
        cmd += ["--tag", tag]
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    part = sys.argv[1] if len(sys.argv) > 1 else "real"
    if part == "real":                      # methods that need no synthetic data
        for s in SEEDS:
            for m in ["baseline", "aug", "ros", "ros_aug"]:
                run(m, s)
    elif part == "syn":                     # main synthetic experiments (T = 1000 / 5000 images per class)
        for s in SEEDS:
            for m in ["syn", "syn_aug"]:
                for T in [1000, 5000]:
                    run(m, s, T)
    elif part == "ablation":                # effect of the amount of synthetic data (1 seed)
        for T in [250, 500, 2500]:
            run("syn", 0, T)
            run("syn_aug", 0, T)
