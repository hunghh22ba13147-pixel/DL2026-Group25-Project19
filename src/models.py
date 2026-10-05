import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils import spectral_norm as sn


# ---------------------------------------------------------------- classifier
class BasicBlock(nn.Module):
    def __init__(self, cin, cout, stride=1):
        super().__init__()
        self.conv1 = nn.Conv2d(cin, cout, 3, stride, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(cout)
        self.conv2 = nn.Conv2d(cout, cout, 3, 1, 1, bias=False)
        self.bn2 = nn.BatchNorm2d(cout)
        self.shortcut = nn.Sequential()
        if stride != 1 or cin != cout:
            self.shortcut = nn.Sequential(nn.Conv2d(cin, cout, 1, stride, bias=False), nn.BatchNorm2d(cout))

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.bn2(self.conv2(out))
        return F.relu(out + self.shortcut(x))


class ResNet32(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, 1, 1, bias=False)
        self.bn1 = nn.BatchNorm2d(16)
        cin, layers = 16, []
        for cout, stride in [(16, 1), (32, 2), (64, 2)]:
            blocks = []
            for s in [stride] + [1] * 4:
                blocks.append(BasicBlock(cin, cout, s))
                cin = cout
            layers.append(nn.Sequential(*blocks))
        self.layer1, self.layer2, self.layer3 = layers
        self.fc = nn.Linear(64, num_classes)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.layer3(self.layer2(self.layer1(x)))
        return self.fc(F.adaptive_avg_pool2d(x, 1).flatten(1))


# ---------------------------------------------------------------- conditional GAN
class CondBN(nn.Module):
    """Class-conditional batch norm."""

    def __init__(self, ch, num_classes):
        super().__init__()
        self.bn = nn.BatchNorm2d(ch, affine=False)
        self.gamma = nn.Embedding(num_classes, ch)
        self.beta = nn.Embedding(num_classes, ch)
        nn.init.ones_(self.gamma.weight)
        nn.init.zeros_(self.beta.weight)

    def forward(self, x, y):
        return self.bn(x) * self.gamma(y)[:, :, None, None] + self.beta(y)[:, :, None, None]


class GBlock(nn.Module):
    def __init__(self, cin, cout, num_classes):
        super().__init__()
        self.b1, self.b2 = CondBN(cin, num_classes), CondBN(cout, num_classes)
        self.c1 = nn.Conv2d(cin, cout, 3, 1, 1)
        self.c2 = nn.Conv2d(cout, cout, 3, 1, 1)
        self.sc = nn.Conv2d(cin, cout, 1)

    def forward(self, x, y):
        h = F.interpolate(F.relu(self.b1(x, y)), scale_factor=2)
        h = self.c1(h)
        h = self.c2(F.relu(self.b2(h, y)))
        return h + self.sc(F.interpolate(x, scale_factor=2))


class Generator(nn.Module):
    def __init__(self, nz=128, nc=10, ch=256):
        super().__init__()
        self.nz, self.ch = nz, ch
        self.fc = nn.Linear(nz, 4 * 4 * ch)
        self.blocks = nn.ModuleList([GBlock(ch, ch, nc) for _ in range(3)])
        self.bn = nn.BatchNorm2d(ch)
        self.out = nn.Conv2d(ch, 3, 3, 1, 1)

    def forward(self, z, y):
        h = self.fc(z).view(-1, self.ch, 4, 4)
        for b in self.blocks:
            h = b(h, y)
        return torch.tanh(self.out(F.relu(self.bn(h))))


class DBlock(nn.Module):
    def __init__(self, cin, cout, down=True, first=False):
        super().__init__()
        self.c1 = sn(nn.Conv2d(cin, cout, 3, 1, 1))
        self.c2 = sn(nn.Conv2d(cout, cout, 3, 1, 1))
        self.sc = sn(nn.Conv2d(cin, cout, 1))
        self.down, self.first = down, first

    def forward(self, x):
        h = x if self.first else F.relu(x)
        h = self.c2(F.relu(self.c1(h)))
        s = self.sc(x)
        if self.down:
            h, s = F.avg_pool2d(h, 2), F.avg_pool2d(s, 2)
        return h + s


class Discriminator(nn.Module):
    """ResNet discriminator with projection conditioning (Miyato & Koyama, 2018)."""

    def __init__(self, nc=10, ch=128):
        super().__init__()
        self.blocks = nn.Sequential(DBlock(3, ch, True, True), DBlock(ch, ch, True),
                                    DBlock(ch, ch, False), DBlock(ch, ch, False))
        self.fc = sn(nn.Linear(ch, 1))
        self.embed = sn(nn.Embedding(nc, ch))

    def forward(self, x, y):
        h = F.relu(self.blocks(x)).sum(dim=(2, 3))
        return self.fc(h).squeeze(1) + (self.embed(y) * h).sum(1)
