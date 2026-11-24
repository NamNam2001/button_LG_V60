# Session: 2026-11-21 → 2026-11-24

**Started:** 2026-11-21 ~23:15
**Last Updated:** 2026-11-24 22:35
**Project:** D:\Work\WORK\CAD\button_LG_V60
**Topic:** Cài text-to-cad và dựng mô hình nút cạnh LG V60 ThinQ để in 3D (resin)

---

## What We Are Building

Nút bấm cạnh thay thế cho điện thoại LG V60 ThinQ (âm lượng +, âm lượng −, Google Assistant, nguồn — cả 4 cùng một mẫu), in 3D bằng resin (SLA). Mô hình là script Python build123d chạy bằng `cad` của dự án text-to-cad (https://github.com/earthtojake/text-to-cad), xuất STL/3MF/STEP.

Cấu tạo nút thật (từ ảnh sản phẩm trong `ref/`): nắp kim loại (thò ra ngoài khung, đầu chữ nhật bo góc lớn, mặt trên phẳng vát cạnh) + đế nhựa đen phía sau dài hơn nắp, có tai giữ ở hai đầu + chốt nhấn công tắc ở giữa mặt sau. Bản in gộp thành một khối.

---

## What WORKED (with evidence)

- **Cài `cad` 0.11.15 bằng `uv tool install cad`** — confirmed by: `cad doctor` chạy không lỗi.
- **Plugin text-to-cad cho Claude Code** (`claude plugin marketplace add earthtojake/text-to-cad#latest` + `claude plugin install text-to-cad@earthtojake`) — confirmed by: "Successfully installed plugin", skill `text-to-cad:cad` xuất hiện.
- **Mô hình `src/v60_button.py`** — confirmed by: `cad run` build OK, bounds 8.855 × 2.027 × 2.919 mm; mặt cắt đo bằng script: nắp 8.05 × 2.03, đế 8.855, chốt 1.0 × 1.0.
- **Kiểm tra in SLA** — confirmed by: `cad model dfm <id> --process printing --technology sla` → OK, 0 lỗi, 2 cảnh báo (mặt dưới đế lơ lửng, cần support).
- **Export** — confirmed by: `STEP/v60_button.step`, `STL/v60_button.stl`, `3MF/v60_button.3mf` đã ghi (STL/3MF với `--tolerance 0.01`).

---

## What Did NOT Work (and why)

- **`irm https://www.texttocad.dev/install.ps1 | iex`** — bị bộ phân loại quyền của Claude Code chặn (tải script từ internet rồi chạy thẳng). Dùng cài thủ công thay thế.
- **Tìm kích thước phím V60 trên internet** — không có nguồn công khai (không có service manual, bản vẽ, CAD hay STL của phím). Chỉ có kích thước thân máy 169.3 × 77.6 × 8.9 mm.
- **Đọc Shopee bằng WebFetch** — trả HTTP 200 rỗng (render bằng JS, chặn bot). AliExpress cũng không render nội dung; witrigs.com trả 429.
- **Ước lượng chiều dài nút từ ảnh render mặt lưng** — ra ~10 mm, nhưng người dùng đo lỗ thật 8–8.5 mm → ảnh render phóng to khoảng 20%. Đừng dùng ảnh render để lấy kích thước tuyệt đối.
- **Đế/tai dày 0.6 mm** — dfm SLA báo lỗi `printing.wall_unsupported` (< 1 mm). Đã nâng lên 1.0 mm. Chốt dài 0.97 mm cũng bị lỗi tương tự → nâng lên 1.0 mm.

---

## What Has NOT Been Tried Yet

- In thử 1 nút và lắp vào máy để chỉnh khe hở / độ nhô.
- Đo thật: bề rộng lỗ, độ dày thành khung, độ nhô nút, khoảng trống bên trong tới công tắc.
- Cắt lớp bằng skill `text-to-cad:print3d` (OrcaSlicer) — chỉ hỗ trợ FDM; với resin dùng slicer của máy resin.

---

## Current State of Files

| File | Status | Notes |
| --- | --- | --- |
| `src/v60_button.py` | PASS: Bản phác thảo | Có tham số; chỉ HOLE_LENGTH = 8.25 là số đo thật, còn lại theo tỉ lệ ảnh |
| `STL/v60_button.stl`, `3MF/v60_button.3mf`, `STEP/v60_button.step` | PASS | Xuất từ bản phác thảo hiện tại |
| `ref/*.jpg, *.png` | Tham khảo | Ảnh sản phẩm (Shopee, HC, Maxbhi, didongcaocap), ảnh cắt mép máy |

---

## Decisions Made

- **Một mẫu chung cho cả 4 nút** — ảnh Shopee/HC bán 4 (hoặc 3) nút giống hệt nhau; ảnh render cho các nút dài gần bằng nhau.
- **In resin (SLA), không phải FDM** — nút ~9 × 2 × 3 mm, FDM đầu 0.4 không đủ chính xác.
- **Gộp nắp + đế thành một khối** khi in.
- **Lỗ 8.25 mm (giữa 8–8.5), khe hở 0.1 mm/bên** → nắp 8.05 mm.
- **Tỉ lệ từ ảnh:** rộng lỗ 0.27 × dài lỗ; cao nắp 0.7 × rộng nắp; bo góc đầu 0.4 × rộng nắp; tai 5% dài nắp mỗi đầu; chốt 12% dài nắp, rộng 0.5 × rộng nắp. Sai số ±15–20%.
- **Đế và chốt tối thiểu 1.0 mm** — theo quy tắc SLA cho tường/chốt tự do.

---

## Blockers & Open Questions

- Bề rộng lỗ (đang ~2.23 mm theo tỉ lệ ảnh) — dễ sai nhất, cần đo.
- Khoảng trống bên trong khung có đủ cho đế 1.0 mm + chốt 0.5 mm không.

---

## Exact Next Step

In thử 1 nút từ `STL/v60_button.stl` (resin, nghiêng ~45°, support ở mặt sau, không đặt support lên mặt trên nắp), lắp thử, rồi chỉnh các hằng số ở đầu `src/v60_button.py` và chạy lại `cad run src/v60_button.py` + export.

---

## Environment & Setup Notes

```bash
cad server start                      # server phải chạy trước
cad run src/v60_button.py             # build, in ra id + link viewer
cad model dfm <id> --process printing --technology sla
cad model export <id> STEP/v60_button.step
cad model export <id> STL/v60_button.stl 3MF/v60_button.3mf --tolerance 0.01
```

Model id: `be677321-03fe-52fb-9624-c7b859133036` (cố định theo đường dẫn script + tên hàm).
