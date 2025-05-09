import os
import shutil

# Đường dẫn
image_test_dir = 'datasets/images/test'
label_test_dir = 'datasets/labels/test'
image_val_dir = 'datasets/images/val'
label_val_dir = 'datasets/labels/val'

# Tạo thư mục val nếu chưa tồn tại
os.makedirs(image_val_dir, exist_ok=True)
os.makedirs(label_val_dir, exist_ok=True)

# Lấy danh sách ảnh test
test_images = [f for f in os.listdir(image_test_dir) if f.endswith('.jpg')]

moved = 0
for img_file in test_images:
    img_id = os.path.splitext(img_file)[0]
    label_file = f"{img_id}.txt"
    label_path = os.path.join(label_test_dir, label_file)

    # Kiểm tra nếu có nhãn tương ứng
    if os.path.exists(label_path):
        # Di chuyển ảnh
        shutil.move(os.path.join(image_test_dir, img_file),
                    os.path.join(image_val_dir, img_file))
        # Di chuyển nhãn
        shutil.move(label_path,
                    os.path.join(label_val_dir, label_file))
        moved += 1
    else:
        print(f"Nhãn không tồn tại cho ảnh: {img_file}")

    if moved >= 1000:
        break

print(f"Đã chuyển {moved} ảnh + nhãn từ test sang val.")

# Các tập cần xử lý
splits = ['train', 'val', 'test']

for split in splits:
    image_dir = f'datasets/images/{split}'
    label_dir = f'datasets/labels/{split}'

    # Tạo thư mục labels nếu chưa có
    os.makedirs(label_dir, exist_ok=True)

    # Duyệt qua tất cả ảnh .jpg trong thư mục ảnh
    image_files = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    count_created = 0

    for img_file in image_files:
        img_id = os.path.splitext(img_file)[0]
        label_file = f"{img_id}.txt"
        label_path = os.path.join(label_dir, label_file)

        # Nếu chưa có file nhãn thì tạo file rỗng
        if not os.path.exists(label_path):
            with open(label_path, 'w') as f:
                pass
            count_created += 1

    print(f"[{split.upper()}] Đã tạo {count_created} file nhãn rỗng.")
