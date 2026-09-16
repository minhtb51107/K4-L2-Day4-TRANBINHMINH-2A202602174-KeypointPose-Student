# Báo cáo Ngày 4 - Keypoint & Pose

Họ tên: Trần Bình Minh   Nhóm: Cá nhân   Ngày: 16/09/2026

## 1. Nhãn của tôi

| Chỉ số | Giá trị |
| --- | ---: |
| Số ảnh đã gán | 20 |
| Số skeleton | 32 |
| v=2 / v=1 / v=0 | 439 / 105 / 0 |
| Thời gian trung bình mỗi ảnh | Chưa ghi nhận |

Ba khớp có `%v=1` cao nhất:

1. `left_ankle` (38%)
2. `right_ankle` (34%)
3. `left_eye` và `left_ear` (31%)

Các mắt cá chân có tỷ lệ `v=1` cao nhất vì thường ở xa, gần mép dưới ảnh hoặc bị phương tiện che. Tai và mắt cũng thường bị tóc, mũ bảo hiểm hoặc góc quay che. Đây là các vùng khó quan sát, nhưng vẫn phải giữ keypoint khi chúng còn trong khung ảnh.

## 2. Chấm với gold

Snapshot trước rework được lưu tại `outputs/eval_vs_gold_before_rework.json`.

| Chỉ số | Trước rework | Sau rework |
| --- | ---: | ---: |
| OKS trung bình | 0.9276 | 0.9626 |
| OKS@0.50 | 0.9310 | 0.9060 |
| OKS@0.75 | 0.8966 | 0.9060 |
| Lỗi `dao_trai_phai` | 0 | 0 |
| Lỗi `nham_nguoi` | 0 | 0 |
| Lỗi `xoa_khop_bi_che` | 3 | 0 |

**Tôi đã sửa gì giữa hai lần chạy**

- Chạy lại pre-annotation bằng YOLO11x-Pose trên 20 ảnh rồi chuyển lại nhãn COCO Keypoints sang YOLO Pose.
- Kết quả mới ghép đủ 29 người Gold và không còn khớp `v=0`; có 3 skeleton dự đoán thừa cần được ghi nhận.
- Không dùng các mục `co_khac_gold` và `gold_khong_gan_nhan` làm lỗi trừ điểm OKS.

**Lỗi đảo trái/phải của tôi xảy ra ở ảnh nào?**

Không có lỗi đảo trái/phải trong lần chấm hiện tại.

## 3. Kiểm chéo

Bạn cùng nhóm: Không áp dụng (bài cá nhân)

Không có bài của đối tác để tạo `visibility_compare.md`. Trạng thái và mẫu kiểm chéo được ghi tại `reports/review_partner.md`.

| Khớp | Bạn | Họ | Lệch | Nguyên nhân (guideline hay gán sai?) |
| --- | ---: | ---: | ---: | --- |
| Không áp dụng | 38% (`left_ankle`) | | | Bài cá nhân |
| Không áp dụng | 34% (`right_ankle`) | | Bài cá nhân |

Luật mới đã bổ sung vào `GUIDELINE_MINI.md` sau khi thống nhất:

- Không áp dụng cho bài cá nhân. Luật visibility đang dùng được ghi tại `GUIDELINE_MINI.md`.

## 4. Model

Notebook Colab đã chạy xong trên GPU và kết quả được lưu trong `outputs/eval_model.json`.

| Chỉ số | yolo26n-pose gốc | Sau fine-tune | Chênh |
| --- | ---: | ---: | ---: |
| pose_mAP50 | 0.8450 | 0.8450 | 0.0000 |
| pose_mAP50-95 | 0.6853 | 0.6908 | +0.0055 |
| pose_precision | 0.9734 | 0.9792 | +0.0058 |
| pose_recall | 0.8462 | 0.8462 | 0.0000 |
| box_mAP50-95 | 0.8119 | 0.8041 | -0.0078 |

Năm câu trả lời phân tích model chưa thể hoàn thành khi chưa có `outputs/eval_model.json` và ảnh dự đoán từ notebook.
Notebook đã tạo `outputs/eval_model.json`. Pose mAP50-95 tăng nhẹ 0.0055 và precision tăng 0.0058, trong khi box mAP50-95 giảm 0.0078; điều này cho thấy 20 ảnh có cải thiện nhỏ ở keypoint nhưng chưa đủ dữ liệu để cải thiện ổn định khả năng phát hiện box.

1. `pose_mAP50-95` tăng `0.0055` (từ `0.6853` lên `0.6908`). 20 ảnh giúp model cải thiện rất nhẹ việc đặt keypoint trong kiểu ảnh của bài, nhưng box mAP50-95 giảm `0.0078`, cho thấy dữ liệu ít chưa đủ để cải thiện ổn định phát hiện người.
2. Chênh lệch box mAP50-95 và pose mAP50-95 là `0.1266` trước fine-tune và `0.1133` sau fine-tune. Model tìm người dễ hơn tìm chính xác từng khớp, đặc biệt ở ảnh có người nhỏ hoặc bị xe/vật thể che.
3. Ở `outputs/model_predictions/test/test_02.jpg`, model tạo một phát hiện người điểm thấp `0.31` ở góc trái bên cạnh người thật điểm `0.90`. Đây là lỗi **nhầm người/false positive**, vì vùng đó không phải một người hoàn chỉnh; model vẫn vẽ keypoint lên vật thể hoặc hình dạng nền.
4. OKS thấp nhất giữa model và nhãn của tôi là `train_10` với `0.718`. Đây là ảnh cần đối chiếu trực tiếp giữa prediction và `outputs/vis_train/train_10.jpg`; chỉ số thấp cho thấy model và nhãn bất đồng đáng kể, nhưng không đủ để kết luận bên nào đúng nếu không có Gold/quan sát ảnh gốc.
5. Skeleton khớp Gold thấp nhất là ở `train_15.jpg` (`0.8678` trong lần ghép hiện hành), đồng thời model cũng có bất đồng ở ảnh này (`0.813` và lệch số người `model 2 / bạn 3`). Hai kết quả cùng chỉ ra `train_15` là ảnh khó vì nhiều người và phương tiện chồng lấn; lỗi có tính chất của ảnh khó hơn là bằng chứng riêng lẻ rằng toàn bộ guideline sai.

## 5. Một rule evidence bạn đã dùng

Ở `train_03.jpg`, người #1, `right_wrist` nằm sau hoặc sát phần xe đạp nhưng vẫn thuộc vùng ảnh. Vì vậy keypoint cần được ước lượng theo hướng cẳng tay và đánh dấu `v=1`, không dùng `v=0`. `v=0` chỉ phù hợp khi cổ tay đã vượt mép ảnh, tức không còn vị trí để đặt chấm. Rule này giúp model vẫn học pose tay khi có vật thể che phía trước.