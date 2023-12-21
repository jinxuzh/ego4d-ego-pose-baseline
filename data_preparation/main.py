import copy
import json
import os
import time

import cv2
import imageio
import numpy as np
import pandas as pd
import torch
from dataloader import ego_pose_anno_loader
from projectaria_tools.core import calibration
from torch.utils.data import Dataset
from tqdm import tqdm
from utils.config import create_arg_parse
from utils.reader import PyAvReader


def undistort_aria_img(args):
    for split in args.splits:
        img_input_root = os.path.join(args.gt_output_dir, "image", split)


def extract_aria_img(args):
    for split in args.splits:
        img_output_dir = os.path.join(args.gt_output_dir, "image", split)


def save_test_gt_anno(output_dir, gt_anno_private):
    # 1. Save private annotated test JSON file
    with open(
        os.path.join(output_dir, f"ego_pose_gt_anno_test_private.json"), "w"
    ) as f:
        json.dump(gt_anno_private, f, indent=4)
    # 2. Exclude GT 3D joints and valid flag information for public un-annotated test file
    gt_anno_public = copy.deepcopy(gt_anno_private)
    for _, take_anno in gt_anno_public.items():
        for _, frame_anno in take_anno.items():
            for k in ["left_hand", "right_hand", "left_hand_valid", "right_hand_valid"]:
                frame_anno.pop(k)
    # 3. Save public un-annotated test JSON file
    with open(os.path.join(output_dir, f"ego_pose_gt_anno_test_public.json"), "w") as f:
        json.dump(gt_anno_public, f, indent=4)


def create_gt_anno(args):
    """
    Creates ground truth annotation file for train, val and test split. For
    test split creates two versions:
    - public: doesn't have GT 3D joints and valid flag information, used for
    public to do local inference
    - private: has GT 3D joints and valid flag information, used for server
    to evaluate model performance
    """
    for split in args.splits:
        # Get ground truth annotation
        gt_anno = ego_pose_anno_loader(args, split, args.anno_type)
        gt_anno_output_dir = os.path.join(
            args.gt_output_dir, "annotation", args.anno_type
        )
        os.makedirs(gt_anno_output_dir, exist_ok=True)
        # Save ground truth JSON file
        if split in ["train", "val"]:
            with open(
                os.path.join(gt_anno_output_dir, f"ego_pose_gt_anno_{split}.json"),
                "w",
            ) as f:
                json.dump(gt_anno.db, f, indent=4)
        # For test split, create two versions of GT-anno
        else:
            save_test_gt_anno(gt_anno_output_dir, gt_anno.db)


def main(args):
    for step in args.steps:
        if step == "gt_anno":
            create_gt_anno(args)
        elif step == "raw_image":
            extract_aria_img(args)
        elif step == "undistort_image":
            undistort_aria_img(args)


if __name__ == "__main__":
    # TODO: Change default path in args
    args = create_arg_parse()
    main(args)
