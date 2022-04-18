import random

from PIL import Image, ImageFilter, ImageOps
from torchvision import transforms

MEAN, STD = (0.082811184, 0.22163138)


class GaussianBlur(object):
    def __init__(self, p):
        self.p = p

    def __call__(self, img):
        if random.random() < self.p:
            sigma = random.random() * 1.9 + 0.1
            return img.filter(ImageFilter.GaussianBlur(sigma))
        else:
            return img


class Solarization(object):
    def __init__(self, p):
        self.p = p

    def __call__(self, img):
        if random.random() < self.p:
            return ImageOps.solarize(img)
        else:
            return img


class BarlowAugment:
    def __init__(self):
        self.transform = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.RandomResizedCrop(20, interpolation=Image.BICUBIC),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomGrayscale(p=0.2),
                GaussianBlur(p=1.0),
                Solarization(p=0.0),
                transforms.ToTensor(),
                transforms.Normalize(mean=[MEAN], std=[STD]),
            ]
        )

        self.transform_weak = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomResizedCrop(20, interpolation=Image.BICUBIC),
                transforms.ToTensor(),
                transforms.Normalize(mean=[MEAN], std=[STD]),
            ]
        )
        self.transform_prime = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.RandomResizedCrop(20, interpolation=Image.BICUBIC),
                transforms.RandomHorizontalFlip(p=0.5),
                transforms.RandomGrayscale(p=0.2),
                GaussianBlur(p=0.1),
                Solarization(p=0.2),
                transforms.ToTensor(),
                transforms.Normalize(mean=[MEAN], std=[STD]),
            ]
        )

    def __call__(self, x):
        y1 = self.transform(x)
        # y1 = x
        y2 = self.transform_prime(x)
        return y1, y2