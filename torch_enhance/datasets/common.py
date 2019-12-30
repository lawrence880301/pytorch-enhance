import os
import torch
from PIL import Image


BSDS300_URL = "http://www2.eecs.berkeley.edu/Research/Projects/CS/vision/bsds/BSDS300-images.tgz"
BSDS500_URL = "http://www.eecs.berkeley.edu/Research/Projects/CS/vision/grouping/BSR/BSR_bsds500.tgz"
SET5_URL = 'https://raw.github.com/IsaacCorley/pytorch-enhance/master/data/Set5.zip'
SET14_URL = 'https://raw.github.com/IsaacCorley/pytorch-enhance/master/data/Set14.zip'
T91_URL = 'https://raw.github.com/IsaacCorley/pytorch-enhance/master/data/T91.zip'
HISTORICAL_URL = 'https://raw.github.com/IsaacCorley/pytorch-enhance/master/data/historical.zip'


class DatasetFolder(torch.utils.data.Dataset):
    def __init__(
        self,
        data_dir,
        lr_transform=None,
        hr_transform=None,
        color_space="RGB",
        extensions=[""],
    ):
        super(DatasetFolder, self).__init__()

        self.data_dir = data_dir
        self.lr_transform = lr_transform
        self.hr_transform = hr_transform
        self.color_space = color_space
        self.extensions = extensions

        self.file_names = [
            os.path.join(self.data_dir, x)
            for x in os.listdir(self.data_dir)
            if self.is_valid_file(x)
        ]

    def __getitem__(self, idx):
        lr = load_img(self.file_names[idx])
        hr = lr.copy()
        if self.lr_transform:
            lr = self.lr_transform(lr)
        if self.target_transform:
            hr = self.hr_transform(hr)

        return lr, hr

    def __len__(self):
        return len(self.file_names)

    def is_image_file(self, file_name):
        return any(file_name.endswith(ext) for ext in self.extensions)

    def load_img(self, file_path):
        return Image.open(file_path).convert(self.color_space)
