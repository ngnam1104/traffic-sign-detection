import os
from PIL import Image, ImageDraw, ImageFont

# Danh sách tên nhãn tương ứng với class ID
class_names = [
    "pl80", "w9", "p6", "ph4.2", "i8", "w14", "w33", "pa13", "im", "w58",
    "pl90", "il70", "p5", "pm55", "pl60", "ip", "p11", "pdd", "wc", "i2r",
    "w30", "pmr", "p23", "pl15", "pm10", "pss", "w1", "p4", "w38", "w50",
    "w34", "pw3.5", "iz", "w39", "w11", "p1n", "pr70", "pd", "pnl", "pg",
    "ph5.3", "w66", "il80", "pb", "pbm", "pm5", "w24", "w67", "w49", "pm40",
    "ph4", "w45", "i4", "w37", "ph2.6", "pl70", "ph5.5", "i14", "i11", "p7",
    "p29", "pne", "pr60", "pm13", "ph4.5", "p12", "p3", "w40", "pl5", "w13",
    "pr10", "p14", "i4l", "pr30", "pw4.2", "w16", "p17", "ph3", "i9", "w15",
    "w35", "pa8", "pt", "pr45", "w17", "pl30", "pcs", "pctl", "pr50", "ph4.4",
    "pm46", "pm35", "i15", "pa12", "pclr", "i1", "pcd", "pbp", "pcr", "w28",
    "ps", "pm8", "w18", "w2", "w52", "ph2.9", "ph1.8", "pe", "p20", "w36",
    "p10", "pn", "pa14", "w54", "ph3.2", "p2", "ph2.5", "w62", "w55", "pw3",
    "pw4.5", "i12", "ph4.3", "phclr", "i10", "pr5", "i13", "w10", "p26", "w26",
    "p8", "w5", "w42", "il50", "p13", "pr40", "p25", "w41", "pl20", "ph4.8",
    "pnlc", "ph3.3", "w29", "ph2.1", "w53", "pm30", "p24", "p21", "pl40", "w27",
    "pmb", "pc", "i6", "pr20", "p18", "ph3.8", "pm50", "pm25", "i2", "w22",
    "w47", "w56", "pl120", "ph2.8", "i7", "w12", "pm1.5", "pm2.5", "w32", "pm15",
    "ph5", "w19", "pw3.2", "pw2.5", "pl10", "il60", "w57", "w48", "w60", "pl100",
    "pr80", "p16", "pl110", "w59", "w64", "w20", "ph2", "p9", "il100", "w31",
    "w65", "ph2.4", "pr100", "p19", "ph3.5", "pa10", "pcl", "pl35", "p15", "w7",
    "pa6", "phcs", "w43", "p28", "w6", "w3", "w25", "pl25", "il110", "p1",
    "w46", "pn-2", "w51", "w44", "w63", "w23", "pm20", "w8", "pmblr", "w4",
    "i5", "il90", "w21", "p27", "pl50", "pl65", "w61", "ph2.2", "pm2", "i3",
    "pa18", "pw4"
]

def draw_bounding_boxes_for_image(images_dir, labels_dir, target_img_id):
    img_filename = target_img_id + '.jpg'
    img_path = os.path.join(images_dir, img_filename)
    label_filename = target_img_id + '.txt'
    label_path = os.path.join(labels_dir, label_filename)
    
    if not os.path.exists(img_path):
        print(f"⚠️ Ảnh không tồn tại: {img_path}")
        return
    if not os.path.exists(label_path):
        print(f"⚠️ Nhãn không tồn tại: {label_path}")
        return
    
    with Image.open(img_path) as img:
        draw = ImageDraw.Draw(img)
        img_w, img_h = img.size

        try:
            font = ImageFont.truetype("arial.ttf", size=16)
        except IOError:
            font = ImageFont.load_default()

        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            parts = line.strip().split()
            cls_id = int(parts[0])
            x_center, y_center, width, height = map(float, parts[1:])
            xmin = int((x_center - width / 2) * img_w)
            ymin = int((y_center - height / 2) * img_h)
            xmax = int((x_center + width / 2) * img_w)
            ymax = int((y_center + height / 2) * img_h)

            label = class_names[cls_id] if cls_id < len(class_names) else f"class_{cls_id}"

            # Vẽ khung và tên nhãn
            draw.rectangle([xmin, ymin, xmax, ymax], outline="red", width=3)
            draw.text((xmin + 2, ymin + 2), label, fill="yellow", font=font)

        img.show()

# Gọi hàm
target_img_id = '73'
draw_bounding_boxes_for_image("datasets/images/test", "datasets/labels/test", target_img_id)
