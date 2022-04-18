import argparse
import pickle

import torch
from torch.utils.data import DataLoader

from dn.data import ImageData, MyDS
from dn.models import DualNet
from dn.trainer import Trainer
from dn.utils import deterministic, load_image_data_pickle, logger, metric

parser = argparse.ArgumentParser(description="DualNet-Image")
args = parser.parse_args()

if __name__ == "__main__":
    deterministic(args.seed)
    data = load_image_data_pickle(args.path)
    train_loader = data.dloader
    test_loader = DataLoader(
        data.test_ds, batch_size=args.test_batch_size, shuffle=False
    )
    model = DualNet(slow=args.slow_learner, fast=args.fast_learner)
    trainer = Trainer(
        model,
        train_loader,
        test_loader,
        args.lr,
        args.epochs,
        metric=metric,
        logger=logger,
    )
    trainer.train()
    trainer.test()
    logger.checkpoint()
    logger.out()
