"""Nút cạnh LG V60 ThinQ (âm lượng +/-, Assistant, nguồn dùng chung một mẫu), in resin (SLA).

Cấu tạo theo ảnh hàng thật (ref/vn-11134207-...jpg, ref/img1.jpg, ref/images.jpg):
nắp kim loại (thò ra ngoài khung) + đế nhựa đen phía sau có tai ở hai đầu
+ chốt nhấn công tắc ở giữa mặt sau. Bản in gộp thành một khối.

Trục: X = dọc theo nút, Y = theo chiều dày máy, Z = hướng bấm (+Z quay ra ngoài).

Số đo duy nhất có thật: lỗ trên khung dài 8–8.5 mm (người dùng đo).
Mọi kích thước khác là PHÁC THẢO theo tỉ lệ đo trên ảnh, quy về chiều dài đó:
- bề rộng lỗ ≈ 0.27 × chiều dài lỗ        (ảnh chụp tay: lỗ trống trên khung)
- cao nắp ≈ 0.7 × rộng nắp                (ảnh Shopee: mặt cắt ở đầu nắp)
- bo góc đầu nắp ≈ 0.4 × rộng nắp         (đầu chữ nhật bo góc lớn, không tròn hẳn)
- tai đế nhô ≈ 0.05 × dài nắp mỗi đầu     (ảnh Shopee: tai đen ở hai đầu)
- dài chốt ≈ 0.12 × dài nắp, rộng ≈ 0.5 × rộng nắp, cao ≈ 0.4 × dày đế
Ảnh độ phân giải thấp và có phối cảnh: sai số mỗi tỉ lệ khoảng ±15–20%.

Check: cad model dfm "$ID" --process printing --technology sla
"""

import build123d as bd
from bd_materials import resins
from cad import model

# --- Số đo thật ---
HOLE_LENGTH = 8.25     # đo: 8–8.5 mm, lấy giữa khoảng
CLEARANCE = 0.1        # khe hở mỗi bên giữa nắp và lỗ

# --- Tỉ lệ từ ảnh ---
HOLE_WIDTH_RATIO = 0.27     # rộng lỗ / dài lỗ
CAP_HEIGHT_RATIO = 0.70     # cao nắp / rộng nắp
END_RADIUS_RATIO = 0.40     # bo góc đầu nắp / rộng nắp
TAB_RATIO = 0.05            # tai mỗi đầu / dài nắp
NUB_LENGTH_RATIO = 0.12     # dài chốt / dài nắp
NUB_WIDTH_RATIO = 0.50      # rộng chốt / rộng nắp
NUB_HEIGHT_RATIO = 0.40     # cao chốt / dày đế

# --- Giới hạn in resin ---
BASE_THICKNESS = 1.0        # ảnh cho ~0.9–1.0; tối thiểu 1.0 để tai resin không gãy
TOP_CHAMFER = 0.15          # vát cạnh mặt trên (kiểu cạnh phay bóng)


def side_button(hole_length=HOLE_LENGTH, clearance=CLEARANCE, base_thickness=BASE_THICKNESS):
    hole_width = HOLE_WIDTH_RATIO * hole_length

    cap_length = hole_length - 2 * clearance
    cap_width = hole_width - 2 * clearance
    cap_height = CAP_HEIGHT_RATIO * cap_width
    end_radius = END_RADIUS_RATIO * cap_width

    base_length = cap_length + 2 * TAB_RATIO * cap_length

    nub_length = max(1.0, NUB_LENGTH_RATIO * cap_length)       # SLA: chốt tự do ≥ 1.0
    nub_width = NUB_WIDTH_RATIO * cap_width
    nub_height = max(0.5, NUB_HEIGHT_RATIO * base_thickness)  # SLA: chốt ≥ 0.5

    z_base = nub_height
    z_cap = nub_height + base_thickness

    # Nắp: chữ nhật bo góc lớn ở hai đầu, vát cạnh trên
    cap = bd.extrude(
        bd.RectangleRounded(cap_length, cap_width, end_radius), amount=cap_height
    ).moved(bd.Location((0, 0, z_cap)))
    cap = bd.chamfer(cap.edges().group_by(bd.Axis.Z)[-1], TOP_CHAMFER)

    # Đế: cùng bề rộng, dài hơn nắp làm tai giữ
    base = bd.extrude(
        bd.RectangleRounded(base_length, cap_width, 0.3), amount=base_thickness
    ).moved(bd.Location((0, 0, z_base)))

    # Chốt nhấn ở giữa mặt sau
    nub = bd.extrude(
        bd.RectangleRounded(nub_length, nub_width, 0.15), amount=nub_height
    )

    part = cap + base + nub
    part.label = "v60_side_button"
    part.material = resins.standard()
    part.color = "#2b2f36"

    bb = part.bounding_box()
    assert abs(bb.size.X - base_length) < 1e-3, bb.size
    assert abs(bb.size.Y - cap_width) < 1e-3, bb.size
    assert abs(bb.size.Z - (nub_height + base_thickness + cap_height)) < 1e-3, bb.size
    return part


@model
def v60_button():
    return side_button()


if __name__ == "__main__":
    v60_button()
