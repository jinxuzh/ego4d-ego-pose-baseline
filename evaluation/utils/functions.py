import argparse

import yaml
from easydict import EasyDict as edict


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count if self.count != 0 else 0


def update_config(config_file):
    with open(config_file) as f:
        config = edict(yaml.load(f, Loader=yaml.FullLoader))
        return config


def parse_args_function():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--cfg_file",
        default="configs/potter_pose_3d_ego4d.yaml",
        help="Config file path",
    )
    parser.add_argument(
        "--pretrained_ckpt",
        default="output/ckpt/POTTER_handPose_ego4d_manual+auto.pt",
        help="Pretrained potter-hand-pose-3d checkpoint",
    )
    parser.add_argument(
        "--cls_ckpt",
        default="eval/cls_s12.pth",
        help="Pretrained potter-cls checkpoint path",
    )
    parser.add_argument(
        "--anno_type",
        default="manual",
        help="Type of annotation: use manual or automatic data",
    )
    parser.add_argument(
        "--gpu_number",
        type=int,
        nargs="+",
        default=[0],
        help="Identifies the GPU number to use.",
    )
    parser.add_argument(
        "--output_dir",
        default="output/inference_output",
        help="Output directory where inference JSON result will be stored",
    )

    args = parser.parse_args()

    # Sanity check
    assert args.anno_type in ["manual", "auto"], f"Invalid anno_type: {args.anno_type}"
    return args
