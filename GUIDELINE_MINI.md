# Mini guideline - nhóm: Cá nhân  |  người gán: Trần Bình Minh  |  ngày: 16/09/2026

> Điền file này **trong lúc** gán nhãn, không phải sau khi xong. Mỗi lần bạn dừng lại
> hơn 10 giây để phân vân, đó là một dòng phải ghi vào đây.

## 1. Luật bắt buộc (đã thống nhất cả lớp - không sửa)

- Bộ 17 điểm COCO, đúng tên, đúng thứ tự. Lấy từ file `.SVG` chung.
- Mọi người trong ảnh đều có **đủ 17 điểm**. Điểm không dùng được thì gắn cờ, không xoá.
- Trái/phải tính theo **cơ thể người**, không theo bức ảnh.
- Bị che, còn trong khung -> `v = 1`, **vẫn đặt chấm** ở vị trí ước lượng.
- Ra ngoài mép ảnh -> `v = 0`, **không** đặt chấm.
- Không dùng `Hidden` (`h`) - nó không được lưu vào file.

## 2. Luật của nhóm bạn (phải điền)

| Tình huống | Luật nhóm bạn chọn | Vì sao |
| --- | --- | --- |
| Hông của người mặc quần áo dài | Đặt tại tâm khớp nối giữa thân và đùi, suy ra từ hướng hai chân; nếu còn trong ảnh nhưng không thấy rõ thì `v=1`. | Hông là mốc giải phẫu, không phải điểm nhìn thấy trên quần áo. |
| Tai bị tóc hoặc mũ bảo hiểm che một phần | Nếu vị trí tai vẫn nằm trong ảnh, ước lượng theo mắt và đường viền đầu, đặt `v=1`. | Vật che không làm khớp ra ngoài khung. |
| Người bị cắt ở mép ảnh (chỉ thấy từ hông trở lên) | Khớp đã vượt mép ảnh dùng `v=0`; khớp còn trong ảnh nhưng bị vật che dùng `v=1`. | Phân biệt vị trí không tồn tại trong ảnh với vị trí cần ước lượng. |
| Cổ tay nằm sau tay lái / sau thân mình | Ước lượng theo hướng cẳng tay, đặt chấm và `v=1` nếu cổ tay còn trong ảnh. | Giữ liên tục chuỗi vai - khuỷu - cổ tay. |
| Hai người chồng lên nhau | Hoàn thành đủ 17 điểm cho từng người; chỉ gán điểm về cơ thể đang xét, kể cả khi các box chồng nhau. | Tránh kéo khớp của một người sang cơ thể khác. |
| Người nhỏ đến mức nào thì không gán nữa | Vẫn gán mọi người xuất hiện trong tập core; chỉ dùng `v=0` cho khớp ngoài mép ảnh, không bỏ cả người vì nhỏ. | Đây là yêu cầu độ bao phủ của lab. |

Với mỗi luật, chèn **một ảnh mẫu** (screenshot từ CVAT) thay vì chỉ viết một câu.
Slide 12 nói rõ: khớp không có bề mặt nhìn thấy được thì phải có ảnh mẫu, không phải
một câu văn chung chung.

## 3. Ba ca mơ hồ đã gặp (bắt buộc, ghi ít nhất 3)

Ảnh tham chiếu: [`train_03.jpg`](outputs/vis_train/train_03.jpg), [`train_15.jpg`](outputs/vis_train/train_15.jpg).

### Ca 1 - ảnh `train_03.jpg`, người thứ `1`, khớp `right_wrist`

- Mơ hồ ở chỗ nào: cổ tay nằm gần phần xe đạp và bị che một phần.
- Bạn quyết thế nào: giữ chấm cổ tay theo hướng cẳng tay và dùng `v=1` nếu vị trí vẫn trong ảnh.
- Vì sao: xe đạp che bề mặt nhìn thấy, không đưa cổ tay ra ngoài mép ảnh.
- Nếu người khác quyết ngược lại thì model học sai cái gì: coi vật che là mất keypoint, làm giảm khả năng dự đoán cổ tay khi có vật thể phía trước.

### Ca 2 - ảnh `train_15.jpg`, người thứ `1`, khớp `left_wrist`

- Mơ hồ ở chỗ nào: tay người lái chồng lên tay lái và thân xe máy.
- Bạn quyết thế nào: suy ra vị trí từ cẳng tay; dùng `v=1` khi vị trí còn trong ảnh.
- Vì sao: chuỗi vai - khuỷu - cổ tay cho phép ước lượng hợp lý hơn việc xoá khớp.
- Nếu người khác quyết ngược lại thì model học sai cái gì: model không học được tư thế tay khi điều khiển xe máy.

### Ca 3 - ảnh `train_03.jpg`, người thứ `3`, khớp `left_ankle`

- Mơ hồ ở chỗ nào: người nhỏ ở mép dưới ảnh, mắt cá chân khó nhìn rõ và gần mép ảnh.
- Bạn quyết thế nào: chỉ dùng `v=0` nếu vị trí mắt cá chân thật sự vượt mép ảnh; nếu còn trong ảnh nhưng mờ hoặc bị che thì đặt `v=1`.
- Vì sao: kích thước nhỏ không phải lý do bỏ keypoint hay bỏ người.
- Nếu người khác quyết ngược lại thì model học sai cái gì: model sẽ học thiếu phần chân đối với người ở xa hoặc ở sát mép ảnh.

## 4. Sau khi so visibility report với bạn cùng nhóm

- Không áp dụng: bài thực hiện cá nhân, chưa có nhãn của bạn cùng nhóm để so sánh.
- Khi có yêu cầu kiểm chéo, ưu tiên so tỷ lệ `v=1` của `left_ankle` (38%) và `right_ankle` (34%) trước khi so từng ảnh.
