import json
import os
from PIL import Image

# Đường dẫn chính
base_dir = 'datasets'
json_path = os.path.join(base_dir, 'annotations_all.json')

images_dir = os.path.join(base_dir, 'images')
labels_dir = os.path.join(base_dir, 'labels')

# Tạo thư mục labels/train và labels/test nếu chưa có
os.makedirs(os.path.join(labels_dir, 'train'), exist_ok=True)
os.makedirs(os.path.join(labels_dir, 'test'), exist_ok=True)

# Đọc file JSON
with open(json_path, 'r') as f:
    data = json.load(f)

categories = data.get('types')
if categories is None:
    raise ValueError("❌ Không tìm thấy danh sách nhãn trong JSON (types)")
category2id = {cat: idx for idx, cat in enumerate(categories)}
imgs = data.get('imgs', {})

if not imgs:
    raise ValueError("❌ Không tìm thấy thông tin ảnh trong JSON (imgs)")

for img_id, img_info in imgs.items():
    rel_path = img_info['path']  # ví dụ: 'train/62627.jpg'
    split = 'train' if 'train' in rel_path else 'test'

    img_path = os.path.join(images_dir, split, os.path.basename(rel_path))
    label_path = os.path.join(labels_dir, split, os.path.splitext(os.path.basename(rel_path))[0] + '.txt')

    try:
        with Image.open(img_path) as im:
            img_w, img_h = im.size
    except FileNotFoundError:
        print(f"⚠️ Không tìm thấy ảnh: {img_path}")
        continue

    lines = []
    for obj in img_info['objects']:
        cat = obj['category']
        if cat not in category2id:
            print(f"⚠️ Nhãn không hợp lệ: {cat}")
            continue

        cls_id = category2id[cat]
        bbox = obj['bbox']
        xmin, ymin = bbox['xmin'], bbox['ymin']
        xmax, ymax = bbox['xmax'], bbox['ymax']

        # Kiểm tra tính hợp lệ của bounding box
        if xmin >= xmax or ymin >= ymax:
            print(f"⚠️ Bounding box không hợp lệ: {bbox}")
            continue

        # Chuyển sang định dạng YOLO
        x_center = ((xmin + xmax) / 2) / img_w
        y_center = ((ymin + ymax) / 2) / img_h
        width = (xmax - xmin) / img_w
        height = (ymax - ymin) / img_h

        lines.append(f"{cls_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    # Ghi file nhãn
    if lines:
        with open(label_path, 'w') as f:
            f.write('\n'.join(lines))
    else:
        print(f"⚠️ Không có nhãn cho ảnh: {img_path}")
