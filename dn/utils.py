import pickle
import random

import numpy as np
import torch


def deterministic(args):
    random.seed(args.seed)  # python random generator
    np.random.seed(args.seed)  # numpy random generator

    torch.manual_seed(args.seed)
    torch.cuda.manual_seed_all(args.seed)

    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True


def load_image_data_pickle(path):
    with open(path, "rb") as f:
        data = pickle.load(f)
    return data