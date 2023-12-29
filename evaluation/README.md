# 3D Hand Pose Estimation Baseline Model 
Implementation of ego-pose-potter, a 3D hand pose estimation baseline model based on [POTTER](https://github.com/zczcwh/POTTER/tree/main) in [Ego4D](https://github.com/facebookresearch/Ego4d) Ego-Pose Benchmark.


## Download Data

To perform model evaluation or training, you need to have 1. ground truth annotation files 2. corresponding undistorted Aria images 3. pretrained model weight. Follow instruction below to download necessary data.

### Step 1: Download ground truth annotation file

Download ground truth annotation file from [here](https://drive.google.com/drive/folders/1F7pz21ejW6J5Eu6Mhhzm9HQ0neFrxrul?usp=sharing) and put it at `<gt_anno_dir>`.

### Step 2: Download Aria images

Download undistorted Aria images from [here](https://drive.google.com/drive/folders/1R2v-xdiQ919sBGgL_MQZtsgsB4BTxVQl?usp=sharing) and put it at `<aria_img_dir>`. (TODO: add train and val images)

### Step 3: Download model weight
Download pretrained model weight of ego-pose-potter from [here](https://drive.google.com/drive/folders/1WSvV7wvmYBvFhB5KwK6PRXwV5dpHd9Hf?usp=sharing).


## Evaluation

To evaluate the model performance, the model output need to be saved as a single JSON file with specific format:
```
{
    "<take_uid>": {
        "<frame_number>": {
                "left_hand": [],
                "right_hand": []     
        }
    }
}
```

You can also find one sample inference output JSON file from [here](https://drive.google.com/file/d/1t9U3Em_Y5sjTN5_4GZ6S6rnYUNI5L943/view?usp=sharing).

Follow instructions below to perform ego-pose-potter model inference and evaluation to get the metric value.

### Step 1: Inference
Perform inference of pretrained model on manual test set, and save the inference output as a single JSON file. It will be stored at `output/inference_output/` by default. 
```
python3 inference.py \
    --pretrained_ckpt <pretrained_ckpt> \
    --gt_anno_dir <gt_anno_dir> \
    --aria_img_dir <aria_img_dir>
```

### Step 2: Evaluate
Evaluate the model performance based on user inference output (which is at `<pred_path>`) and ground truth test JSON file (which is at `<gt_path>`). Remember to set `offset` if the user inference output is offset by hand wrist. 
```
python3 evaluate.py \
    --pred_path <pred_path> \
    --gt_path <gt_path> \
    --offset 
```