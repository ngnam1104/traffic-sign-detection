import numpy as np

names = ['Accident area', 'Be careful', 'Bicycles keep right', 'Bicycles only', 'Camera', 'Children ahead', 'Control', 'Cross-village road', 'Crossroads', 'Crosswalk', 'Curve to the left', 'Curve to the right', 'Cyclists', 'Dangerous crosswinds', 'Dip', 'Do not enter for vehicular traffic', 'End of maximum speed limit 100kph', 'End of maximum speed limit 10kph', 'End of maximum speed limit 20kph', 'End of maximum speed limit 30kph', 'End of maximum speed limit 40kph', 'End of maximum speed limit 45kph', 'End of maximum speed limit 50kph', 'End of maximum speed limit 60kph', 'End of maximum speed limit 70kph', 'End of maximum speed limit 80kph', 'End of overtaking prohibition', 'Fork road on right rear', 'Give way', 'Keep right side', 'Limited-access road', 'Maintain Safe Distance', 'Maximum height 1.8m', 'Maximum height 2.1m', 'Maximum height 2.2m', 'Maximum height 2.4m', 'Maximum height 2.5m', 'Maximum height 2.8m', 'Maximum height 2.9m', 'Maximum height 2m', 'Maximum height 3.2m', 'Maximum height 3.5m', 'Maximum height 3.8m', 'Maximum height 3m', 'Maximum height 4.2m', 'Maximum height 4.5m', 'Maximum height 4.8m', 'Maximum height 4m', 'Maximum height 5.3m', 'Maximum height 5.5m', 'Maximum height 5m', 'Maximum speed limit 100kph', 'Maximum speed limit 10kph', 'Maximum speed limit 110kph', 'Maximum speed limit 120kph', 'Maximum speed limit 15kph', 'Maximum speed limit 20kph', 'Maximum speed limit 25kph', 'Maximum speed limit 30kph', 'Maximum speed limit 35kph', 'Maximum speed limit 40kph', 'Maximum speed limit 50kph', 'Maximum speed limit 5kph', 'Maximum speed limit 60kph', 'Maximum speed limit 70kph', 'Maximum speed limit 80kph', 'Maximum speed limit 90kph', 'Maximum weight 10t', 'Maximum weight 13t', 'Maximum weight 15t', 'Maximum weight 2.5t', 'Maximum weight 20t', 'Maximum weight 2t', 'Maximum weight 30t', 'Maximum weight 35t', 'Maximum weight 40t', 'Maximum weight 50t', 'Maximum weight 55t', 'Maximum weight 5t', 'Maximum weight 8t', 'Maximum weight per axle 10t', 'Maximum weight per axle 12t', 'Maximum weight per axle 13t', 'Maximum weight per axle 14t', 'Maximum weight per axle 18t', 'Maximum weight per axle 6t', 'Maximum weight per axle 8t', 'Maximum width 2.5m', 'Maximum width 3.2m', 'Maximum width 3.5m', 'Maximum width 3m', 'Maximum width 4.3m', 'Maximum width 4.5m', 'Maximum width 4m', 'Merging traffic on left', 'Merging traffic on right', 'Minimum speed limit 100kph', 'Minimum speed limit 110kph', 'Minimum speed limit 50kph', 'Minimum speed limit 60kph', 'Minimum speed limit 70kph', 'Minimum speed limit 80kph', 'Minimum speed limit 90kph', 'Motor keep right', 'Motor vehicles keep left', 'Motorcycles only', 'Multiple curves', 'No U-turns', 'No bicycles', 'No bicycles and motorcycles', 'No bicycles and pedestrians', 'No buses', 'No electric tricycles', 'No entry for both vehicular traffic and pedestrians', 'No freight bikes', 'No freight vehicles', 'No handcarts', 'No honking', 'No horse-drawn vehicles', 'No left and right turns', 'No left and right turns for busses', 'No left and right turns for freight vehicles', 'No left and right turns for motor vehicles', 'No left turn', 'No left turn for busses', 'No left turn for motor vehicles', 'No motor tricycles', 'No motor vehicles', 'No motorcycles', 'No motorcycles and freight vehicles', 'No overtaking', 'No passenger bikes', 'No pedestrians', 'No proceed straight', 'No proceed straight and left turns', 'No proceed straight and right turns', 'No proceed straight for freight vehicles', 'No proceed straight for motor vehicles', 'No right turn', 'No right turn for buses', 'No right turn for motor vehicles', 'No small passenger vehicles', 'No stop', 'No stopping', 'No tractors', 'No trailers and truck', 'No vehicles carrying dangerous goods', 'Offset road junctions from the right', 'Overflow road', 'Pedestrian crossing ahead', 'Pedestrians only', 'Proceed straight', 'Proceed straight or turn left', 'Proceed straight or turn right', 'Railroad ahead with safety barriers', 'Riverbank on left', 'Road narrows on both sides', 'Road narrows on right', 'Roadworks ahead', 'Roundabout', 'Side road junction ahead on the left', 'Side road junction ahead on the right', 'Slow down', 'Steep descent', 'Stop', 'T-junction ahead', 'Traffic lights ahead', 'Tunnel ahead', 'Turn left', 'Turn left or right', 'Turn left or right to detour', 'Turn on lights for driving through tunnel', 'Turn right', 'Two-way traffic ahead', 'U-turn']

# Đây là input dạng văn bản, ví dụ:
raw_input_text = """Accident area	
6
Be careful	
48
Bicycles keep right	
417
Bicycles only	
443
Camera	
38
Children ahead	
176
Control	
2
Cross-village road	
19
Crossroads	
122
Crosswalk	
341
Curve to the left	
2
Curve to the right	
7
Cyclists	
2
Dangerous crosswinds	
2
Dip	
2
Do not enter for vehicular traffic	
2097
End of maximum speed limit 100kph	
2
End of maximum speed limit 10kph	
1
End of maximum speed limit 20kph	
18
End of maximum speed limit 30kph	
14
End of maximum speed limit 40kph	
201
End of maximum speed limit 45kph	
2
End of maximum speed limit 50kph	
16
End of maximum speed limit 60kph	
21
End of maximum speed limit 70kph	
5
End of maximum speed limit 80kph	
3
End of overtaking prohibition	
12
Fork road on right rear	
2
Give way	
155
Keep right side	
1587
Limited-access road	
734
Maintain Safe Distance	
2
Maximum height 1.8m	
2
Maximum height 2.1m	
2
Maximum height 2.2m	
14
Maximum height 2.4m	
2
Maximum height 2.5m	
12
Maximum height 2.8m	
3
Maximum height 2.9m	
3
Maximum height 2m	
6
Maximum height 3.2m	
2
Maximum height 3.5m	
9
Maximum height 3.8m	
1
Maximum height 3m	
23
Maximum height 4.2m	
25
Maximum height 4.5m	
186
Maximum height 4.8m	
5
Maximum height 4m	
120
Maximum height 5.3m	
1
Maximum height 5.5m	
1
Maximum height 5m	
120
Maximum speed limit 100kph	
664
Maximum speed limit 10kph	
27
Maximum speed limit 110kph	
32
Maximum speed limit 120kph	
296
Maximum speed limit 15kph	
50
Maximum speed limit 20kph	
158
Maximum speed limit 25kph	
7
Maximum speed limit 30kph	
596
Maximum speed limit 35kph	
5
Maximum speed limit 40kph	
1368
Maximum speed limit 50kph	
1028
Maximum speed limit 5kph	
485
Maximum speed limit 60kph	
821
Maximum speed limit 70kph	
149
Maximum speed limit 80kph	
865
Maximum speed limit 90kph	
45
Maximum weight 10t	
19
Maximum weight 13t	
1
Maximum weight 15t	
12
Maximum weight 2.5t	
1
Maximum weight 20t	
157
Maximum weight 2t	
6
Maximum weight 30t	
108
Maximum weight 35t	
5
Maximum weight 40t	
4
Maximum weight 50t	
4
Maximum weight 55t	
138
Maximum weight 5t	
5
Maximum weight 8t	
2
Maximum weight per axle 10t	
8
Maximum weight per axle 12t	
3
Maximum weight per axle 13t	
22
Maximum weight per axle 14t	
58
Maximum weight per axle 18t	
1
Maximum weight per axle 6t	
1
Maximum weight per axle 8t	
1
Maximum width 2.5m	
1
Maximum width 3.2m	
15
Maximum width 3.5m	
2
Maximum width 3m	
5
Maximum width 4.3m	
4
Maximum width 4.5m	
3
Maximum width 4m	
9
Merging traffic on left	
63
Merging traffic on right	
198
Minimum speed limit 100kph	
131
Minimum speed limit 110kph	
21
Minimum speed limit 50kph	
34
Minimum speed limit 60kph	
483
Minimum speed limit 70kph	
14
Minimum speed limit 80kph	
294
Minimum speed limit 90kph	
76
Motor keep right	
9
Motor vehicles keep left	
330
Motorcycles only	
70
Multiple curves	
4
No U-turns	
395
No bicycles	
114
No bicycles and motorcycles	
72
No bicycles and pedestrians	
95
No buses	
209
No electric tricycles	
5
No entry for both vehicular traffic and pedestrians	
68
No freight bikes	
63
No freight vehicles	
815
No handcarts	
6
No honking	
1538
No horse-drawn vehicles	
15
No left and right turns	
3
No left and right turns for busses	
3
No left and right turns for freight vehicles	
9
No left and right turns for motor vehicles	
1
No left turn	
283
No left turn for busses	
6
No left turn for motor vehicles	
85
No motor tricycles	
70
No motor vehicles	
360
No motorcycles	
182
No motorcycles and freight vehicles	
353
No overtaking	
46
No passenger bikes	
31
No pedestrians	
55
No proceed straight	
36
No proceed straight and left turns	
4
No proceed straight and right turns	
3
No proceed straight for freight vehicles	
5
No proceed straight for motor vehicles	
2
No right turn	
123
No right turn for buses	
2
No right turn for motor vehicles	
19
No small passenger vehicles	
49
No stop	
7
No stopping	
2973
No tractors	
34
No trailers and truck	
14
No vehicles carrying dangerous goods	
152
Offset road junctions from the right	
2
Overflow road	
3
Pedestrian crossing ahead	
394
Pedestrians only	
9
Proceed straight	
17
Proceed straight or turn left	
4
Proceed straight or turn right	
6
Railroad ahead with safety barriers	
8
Riverbank on left	
2
Road narrows on both sides	
2
Road narrows on right	
20
Roadworks ahead	
112
Roundabout	
6
Side road junction ahead on the left	
19
Side road junction ahead on the right	
34
Slow down	
80
Steep descent	
9
Stop	
31
T-junction ahead	
9
Traffic lights ahead	
15
Tunnel ahead	
3
Turn left	
17
Turn left or right	
4
Turn left or right to detour	
1
Turn on lights for driving through tunnel	
3
Turn right	
38
Two-way traffic ahead	
4
U-turn	
13
"""

# Chuyển input thô thành list
lines = [line.strip() for line in raw_input_text.strip().splitlines() if line.strip()]

# Xây dựng dict từ input
label_quantity_dict = {}
for i in range(0, len(lines), 2):
    label = lines[i]
    quantity = int(lines[i + 1])
    label_quantity_dict[label] = quantity

# Tạo mảng số lượng tương ứng với mảng `names`
quantities = [label_quantity_dict.get(name, 0) for name in names]
quantities = np.array(quantities)

alpha_t = 1 / np.log(quantities + 1e-6 + 1)  # cộng 1 tránh log(0), +1e-6 tránh chia 0
alpha_t = 1 / np.log(quantities + 1 + 1e-6)  # tạo alpha_t
mean_alpha = alpha_t.mean()                   # tính trung bình
alpha_t = alpha_t / mean_alpha                # chuẩn hóa để kỳ vọng = 1

print([round(x, 3) for x in alpha_t])

