#!/usr/bin/env python3
"""Tự động chạy model YOLO Pose pre-trained để tạo khung nhãn COCO Keypoints 1.0 ban đầu.

Sau khi chạy xong, bạn có thể:
1. Nạp file annotations/coco_keypoints/person_keypoints_default.json này lên CVAT (Upload Annotations -> COCO Keypoints 1.0).
2. Hoặc chuyển đổi trực tiếp sang nhãn YOLO pose để kiểm tra/tinh chỉnh.
"""

import json
from pathlib import Path
from PIL import Image
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
IMAGES_DIR = ROOT / "dataset/images/train"
OUTPUT_COCO = ROOT / "annotations/coco_keypoints/person_keypoints_default.json"

KEYPOINT_NAMES = [
    "nose", "left_eye", "right_eye", "left_ear", "right_ear",
    "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
    "left_wrist", "right_wrist", "left_hip", "right_hip",
    "left_knee", "right_knee", "left_ankle", "right_ankle"
]

SKELETON_EDGES = [
    [16, 14], [14, 12], [17, 15], [15, 13], [12, 13],
    [6, 12], [7, 13], [6, 7], [6, 8], [7, 9],
    [8, 10], [9, 11], [2, 3], [1, 2], [1, 3],
    [2, 4], [3, 5], [4, 6], [5, 7]
]

def main():
    print("Đang tải model YOLO11 Pose (yolo11x-pose.pt)...")
    model = YOLO("yolo11x-pose.pt")

    images_list = []
    annotations_list = []
    ann_id = 1

    img_files = sorted(IMAGES_DIR.glob("*.jpg"))
    if not img_files:
        print(f"Không tìm thấy ảnh nào trong {IMAGES_DIR}")
        return

    for img_id, img_path in enumerate(img_files, start=1):
        with Image.open(img_path) as img:
            w, h = img.size

        images_list.append({
            "id": img_id,
            "width": w,
            "height": h,
            "file_name": img_path.name,
            "license": 0,
            "flickr_url": "",
            "coco_url": "",
            "date_captured": 0
        })

        results = model.predict(source=str(img_path), conf=0.3, verbose=False)
        result = results[0]

        if result.boxes is not None and result.keypoints is not None:
            boxes = result.boxes.xywh.cpu().numpy()  # [center_x, center_y, width, height]
            classes = result.boxes.cls.cpu().numpy()
            kpts = result.keypoints.data.cpu().numpy()  # [N, 17, 3] (x, y, conf)

            for i in range(len(boxes)):
                if int(classes[i]) != 0:  # chỉ lấy person
                    continue
                cx, cy, bw, bh = boxes[i]
                x1 = float(cx - bw / 2.0)
                y1 = float(cy - bh / 2.0)
                bw = float(bw)
                bh = float(bh)

                person_kpts = kpts[i]  # 17x3
                coco_kpts = []
                num_kpts = 0

                for k in range(17):
                    kx, ky, conf = person_kpts[k]
                    # Nếu điểm rơi ngoài ảnh -> v=0
                    if kx < 0 or kx > w or ky < 0 or ky > h:
                        coco_kpts.extend([0.0, 0.0, 0])
                    elif conf < 0.35:
                        # Điểm độ tự tin thấp/bị che -> v=1 (ước lượng toạ độ)
                        coco_kpts.extend([round(float(kx), 2), round(float(ky), 2), 1])
                        num_kpts += 1
                    else:
                        coco_kpts.extend([round(float(kx), 2), round(float(ky), 2), 2])
                        num_kpts += 1

                annotations_list.append({
                    "id": ann_id,
                    "image_id": img_id,
                    "category_id": 1,
                    "segmentation": [],
                    "area": round(bw * bh, 2),
                    "bbox": [round(x1, 2), round(y1, 2), round(bw, 2), round(bh, 2)],
                    "iscrowd": 0,
                    "attributes": {"occluded": False},
                    "keypoints": coco_kpts,
                    "num_keypoints": num_kpts
                })
                ann_id += 1

    coco_data = {
        "licenses": [{"name": "", "id": 0, "url": ""}],
        "info": {
            "contributor": "", "date_created": "", "description": "",
            "url": "", "version": "", "year": ""
        },
        "categories": [{
            "id": 1,
            "name": "person",
            "supercategory": "",
            "keypoints": KEYPOINT_NAMES,
            "skeleton": SKELETON_EDGES
        }],
        "images": images_list,
        "annotations": annotations_list
    }

    OUTPUT_COCO.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_COCO, "w", encoding="utf-8") as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=2)

    print(f"Đã tạo thành công {len(annotations_list)} skeleton cho {len(images_list)} ảnh tại {OUTPUT_COCO}")

if __name__ == "__main__":
    main()
