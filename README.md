# Nút cạnh LG V60 ThinQ — in 3D

Mô hình nút bấm cạnh thay thế cho LG V60 ThinQ (âm lượng +/−, Google Assistant, nguồn — một mẫu chung), dựng bằng [text-to-cad](https://github.com/earthtojake/text-to-cad) / build123d, để in resin (SLA).

> **Bản phác thảo.** Chỉ chiều dài lỗ (8–8.5 mm) là số đo thật; các kích thước khác suy ra từ tỉ lệ trên ảnh sản phẩm (sai số ±15–20%). In thử rồi chỉnh.

## File

| Đường dẫn | Nội dung |
| --- | --- |
| `src/v60_button.py` | Mô hình có tham số (hằng số ở đầu file) |
| `STL/`, `3MF/`, `STEP/` | File xuất để in / mở trong CAD khác |
| `ref/` | Ảnh tham khảo nút thật |
| `docs/SESSION.md` | Ghi chép phiên làm việc: quyết định, tỉ lệ, những gì đã thử |

Kích thước hiện tại: 8.86 × 2.03 × 2.92 mm (nắp 8.05 × 2.03 × 1.42, đế dày 1.0, chốt 1.0 × 1.0 × 0.5).

## Chạy lại

```bash
uv tool install cad
cad server start
cad run src/v60_button.py
cad model dfm <id> --process printing --technology sla
cad model export <id> STL/v60_button.stl 3MF/v60_button.3mf --tolerance 0.01
cad model export <id> STEP/v60_button.step
```

In: nghiêng ~45°, support ở mặt sau (phía chốt), không đặt support lên mặt trên nắp.
