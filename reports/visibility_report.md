# Visibility report

- Thư mục nhãn: `dataset\labels\train`
- 20 ảnh, 32 skeleton, trung bình 17.0 khớp có v > 0 mỗi người
- Tổng: v=2 439 | v=1 105 | v=0 0

| # | Khớp | v=2 | v=1 | v=0 | %v=1 |
| ---: | --- | ---: | ---: | ---: | ---: |
| 0 | nose | 25 | 7 | 0 | 22% |
| 1 | left_eye | 22 | 10 | 0 | 31% |
| 2 | right_eye | 24 | 8 | 0 | 25% |
| 3 | left_ear | 22 | 10 | 0 | 31% |
| 4 | right_ear | 24 | 8 | 0 | 25% |
| 5 | left_shoulder | 32 | 0 | 0 | 0% |
| 6 | right_shoulder | 32 | 0 | 0 | 0% |
| 7 | left_elbow | 28 | 4 | 0 | 12% |
| 8 | right_elbow | 28 | 4 | 0 | 12% |
| 9 | left_wrist | 26 | 6 | 0 | 19% |
| 10 | right_wrist | 27 | 5 | 0 | 16% |
| 11 | left_hip | 30 | 2 | 0 | 6% |
| 12 | right_hip | 30 | 2 | 0 | 6% |
| 13 | left_knee | 24 | 8 | 0 | 25% |
| 14 | right_knee | 24 | 8 | 0 | 25% |
| 15 | left_ankle | 20 | 12 | 0 | 38% |
| 16 | right_ankle | 21 | 11 | 0 | 34% |

## Đọc bảng này thế nào

1. Khớp nào có **%v=1 cao**: khớp hay bị che. Cổ tay và hông thường là hai vị trí cần xem lại guideline trước khi kết luận.
2. Khớp nào có **v=0 cao bất thường**: mọi người đang dùng Outside ở chỗ đáng lẽ là Occluded. Đó là lỗi số 3 của slide 46, và nó xoá thẳng khớp đó khỏi bảng điểm OKS.
3. Khi so hai người: **lệch lớn = bất đồng về guideline**, không phải về bức ảnh. Sửa guideline trước, sửa nhãn sau.
