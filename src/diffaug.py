"""Differentiable Augmentation (DiffAugment, Zhao et al., NeurIPS 2020):
colour + translation + cutout, applied to BOTH real and fake images when training the discriminator."""
import torch
import torch.nn.functional as F


def rand_brightness(x):
    return x + (torch.rand(x.size(0), 1, 1, 1, dtype=x.dtype, device=x.device) - 0.5)


def rand_saturation(x):
    m = x.mean(dim=1, keepdim=True)
    return (x - m) * (torch.rand(x.size(0), 1, 1, 1, dtype=x.dtype, device=x.device) * 2) + m


def rand_contrast(x):
    m = x.mean(dim=[1, 2, 3], keepdim=True)
    return (x - m) * (torch.rand(x.size(0), 1, 1, 1, dtype=x.dtype, device=x.device) + 0.5) + m


def rand_translation(x, ratio=0.125):
    sx, sy = int(x.size(2) * ratio + 0.5), int(x.size(3) * ratio + 0.5)
    tx = torch.randint(-sx, sx + 1, size=[x.size(0), 1, 1], device=x.device)
    ty = torch.randint(-sy, sy + 1, size=[x.size(0), 1, 1], device=x.device)
    gb, gx, gy = torch.meshgrid(torch.arange(x.size(0), device=x.device),
                                torch.arange(x.size(2), device=x.device),
                                torch.arange(x.size(3), device=x.device), indexing="ij")
    gx = torch.clamp(gx + tx + 1, 0, x.size(2) + 1)
    gy = torch.clamp(gy + ty + 1, 0, x.size(3) + 1)
    xp = F.pad(x, [1, 1, 1, 1, 0, 0, 0, 0])
    return xp.permute(0, 2, 3, 1).contiguous()[gb, gx, gy].permute(0, 3, 1, 2)


def rand_cutout(x, ratio=0.5):
    cs = (int(x.size(2) * ratio + 0.5), int(x.size(3) * ratio + 0.5))
    ox = torch.randint(0, x.size(2) + (1 - cs[0] % 2), size=[x.size(0), 1, 1], device=x.device)
    oy = torch.randint(0, x.size(3) + (1 - cs[1] % 2), size=[x.size(0), 1, 1], device=x.device)
    gb, gx, gy = torch.meshgrid(torch.arange(x.size(0), device=x.device),
                                torch.arange(cs[0], device=x.device),
                                torch.arange(cs[1], device=x.device), indexing="ij")
    gx = torch.clamp(gx + ox - cs[0] // 2, 0, x.size(2) - 1)
    gy = torch.clamp(gy + oy - cs[1] // 2, 0, x.size(3) - 1)
    mask = torch.ones(x.size(0), x.size(2), x.size(3), dtype=x.dtype, device=x.device)
    mask[gb, gx, gy] = 0
    return x * mask.unsqueeze(1)


def diff_augment(x):
    x = rand_brightness(x)
    x = rand_saturation(x)
    x = rand_contrast(x)
    x = rand_translation(x)
    x = rand_cutout(x)
    return x.contiguous()
