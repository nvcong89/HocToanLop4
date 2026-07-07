import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
import os

# ─── Mapping chủ đề → trang SGK ──────────────────────────────
TOPIC_PAGES = {
    "➕ Cộng & Trừ": {
        "Cộng các số có nhiều chữ số":       13,
        "Trừ các số có nhiều chữ số":        16,
        "Tính chất giao hoán của phép cộng": 19,
        "Tính chất kết hợp của phép cộng":   20,
    },
    "✖️ Nhân & Chia": {
        "Nhân với số có một chữ số":          26,
        "Tính chất giao hoán của phép nhân":  28,
        "Nhân với số có hai chữ số":          35,
        "Chia cho số có một chữ số":          45,
        "Chia cho số có hai chữ số":          79,
    },
    "🍕 Phân Số": {
        "Phân số":                            106,
        "Phân số bằng nhau":                  109,
        "Rút gọn phân số":                    112,
        "Quy đồng mẫu số":                    114,
        "So sánh phân số":                    117,
        "Cộng hai phân số cùng mẫu":          126,
        "Trừ hai phân số cùng mẫu":           131,
    },
    "📐 Hình Học": {
        "Góc nhọn, góc tù, góc bẹt":          49,
        "Hai đường thẳng vuông góc":           50,
        "Hình chữ nhật":                       53,
        "Hình vuông":                          55,
        "Diện tích hình chữ nhật":             103,
        "Diện tích hình vuông":                105,
    },
    "📏 Đo Lường": {
        "Bảng đơn vị đo độ dài":               22,
        "Bảng đơn vị đo khối lượng":           24,
        "Giây, thế kỷ":                        25,
        "Đề-ca-mét vuông, héc-tô-mét vuông":   97,
        "Mi-li-mét vuông, bảng đơn vị đo diện tích": 99,
    },
    "📝 Toán Đố": {
        "Tìm hai số khi biết tổng và hiệu":    47,
        "Toán đố dạng rút về đơn vị":          138,
    },
}


def load_pdf_bytes(pdf_path: str) -> bytes | None:
    """Đọc file PDF trả về bytes."""
    if not os.path.exists(pdf_path):
        return None
    with open(pdf_path, "rb") as f:
        return f.read()


def render_pdf_viewer(pdf_path: str, page: int = 1, height: int = 700):
    """
    Hiển thị PDF dùng streamlit-pdf-viewer.
    Tự động chọn tham số đúng theo version đang cài.
    """
    pdf_bytes = load_pdf_bytes(pdf_path)
    if pdf_bytes is None:
        st.error(f"⚠️ Không tìm thấy file PDF tại: `{pdf_path}`")
        st.info("Hãy đặt file PDF vào thư mục `data/` và đặt tên `toan4.pdf`")
        return

    import streamlit_pdf_viewer as spv_module
    import inspect

    # Lấy danh sách tham số hàm pdf_viewer đang cài
    supported_params = inspect.signature(pdf_viewer).parameters

    kwargs = {
        "input":  pdf_bytes,
        "width":  700,
        "height": height,
    }

    # Thêm tham số trang nếu version hỗ trợ
    if "starting_page" in supported_params:
        kwargs["starting_page"] = page
    elif "page" in supported_params:
        kwargs["page"] = page

    # Thêm render_text nếu hỗ trợ
    if "render_text" in supported_params:
        kwargs["render_text"] = True

    pdf_viewer(**kwargs)


def render_page_links(topic: str):
    """Hiển thị các nút liên kết trang SGK cho từng chủ đề."""
    if topic not in TOPIC_PAGES:
        return

    lessons = TOPIC_PAGES[topic]
    st.markdown("#### 📌 Xem Nhanh Trang SGK")

    cols = st.columns(3)
    for idx, (lesson_name, page_num) in enumerate(lessons.items()):
        with cols[idx % 3]:
            if st.button(
                f"📄 Trang {page_num} — {lesson_name}",
                key=f"pglink_{topic}_{page_num}",
                use_container_width=True,
                help=f"Mở SGK trang {page_num}: {lesson_name}"
            ):
                st.session_state["sgk_page"]      = page_num
                st.session_state["sgk_lesson"]    = lesson_name
                st.session_state["current_topic"] = "📖 Sách Giáo Khoa"
                st.rerun()
