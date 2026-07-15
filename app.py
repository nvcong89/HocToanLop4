# ─── Imports ──────────────────────────────────────────────────
import os
import streamlit as st
from utils.ai_tutor import ask_ai
from utils.pdf_viewer import render_pdf_viewer, TOPIC_PAGES
from topics import (
    addition_subtraction,
    multiplication_division,
    fractions,
    geometry,
    measurement,
    word_problems,
)

# ─── Constants ────────────────────────────────────────────────
PDF_PATH = "data/toan4.pdf"

# ─── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="🎓 Toán Lớp 4",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS (gom toàn bộ vào 1 khối duy nhất) ────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Nunito', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102,126,234,0.3);
    }
    .main-header h1 { font-size: 2.5rem; font-weight: 800; margin: 0; }
    .main-header p  { font-size: 1.1rem; opacity: 0.9; margin: 0.5rem 0 0; }

    .topic-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin: 0.5rem 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 12px rgba(0,0,0,0.07);
        transition: transform 0.2s;
    }
    .topic-card:hover { transform: translateX(4px); }

    .score-box {
        background: linear-gradient(135deg, #11998e, #38ef7d);
        color: white;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        text-align: center;
        font-size: 1.3rem;
        font-weight: 700;
        margin: 1rem 0;
    }

    .correct-answer {
        background: #d4edda;
        border: 1px solid #28a745;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #155724;
        font-weight: 600;
    }

    .wrong-answer {
        background: #f8d7da;
        border: 1px solid #dc3545;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #721c24;
        font-weight: 600;
    }

    .hint-box {
        background: #fff3cd;
        border: 1px solid #ffc107;
        border-radius: 8px;
        padding: 0.8rem 1rem;
        color: #856404;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.5rem 1.5rem;
        transition: all 0.2s;
    }

    .sidebar-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #667eea;
        margin-bottom: 0.5rem;
    }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8f9ff 0%, #eef0ff 100%);
    }

    /* ── Author Card ── */
    .author-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecff 100%);
        border-radius: 16px;
        padding: 2rem 2.5rem;
        margin-top: 1rem;
        border: 1px solid #dde3ff;
        box-shadow: 0 4px 20px rgba(102,126,234,0.1);
    }
    .author-avatar {
        width: 80px; height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea, #764ba2);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2.2rem;
        margin: 0 auto 1rem auto;
        box-shadow: 0 4px 15px rgba(102,126,234,0.4);
    }
    .author-name {
        font-size: 1.5rem; font-weight: 800;
        color: #3d3d8f; text-align: center; margin-bottom: 0.3rem;
    }
    .author-title {
        font-size: 0.95rem; color: #667eea;
        text-align: center; font-weight: 600;
        margin-bottom: 1.2rem; letter-spacing: 0.5px;
    }
    .author-divider {
        border: none;
        border-top: 2px dashed #c5ceff;
        margin: 1rem 0;
    }
    .author-bio {
        color: #555; font-size: 0.97rem;
        line-height: 1.8; text-align: center;
    }
    .author-badge {
        display: inline-block;
        background: #667eea; color: white;
        border-radius: 20px; padding: 0.25rem 0.85rem;
        font-size: 0.82rem; font-weight: 700; margin: 0.2rem;
    }
    .author-footer {
        text-align: center; color: #999;
        font-size: 0.82rem; margin-top: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Session State Init ───────────────────────────────────────
defaults = {
    "score":         0,
    "total":         0,
    "current_topic": "🏠 Trang Chủ",
    "sgk_page":      1,
    "sgk_lesson":    "",
    "chat_history":  [],
    "history_fallback": [],
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ─── Sidebar Navigation ───────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">📚 Toán Lớp 4</div>', unsafe_allow_html=True)
    st.markdown("---")

    NAV_TOPICS = {
        "🏠 Trang Chủ"      : "home",
        "📖 Sách Giáo Khoa" : "sgk",
        "➕ Cộng & Trừ"     : "add_sub",
        "✖️ Nhân & Chia"    : "mul_div",
        "🍕 Phân Số"        : "fractions",
        "📐 Hình Học"       : "geometry",
        "📏 Đo Lường"       : "measurement",
        "📝 Toán Đố"        : "word_problems",
        "👨‍👩‍👧 Lịch Sử Làm Bài" : "history",
    }

    for label in NAV_TOPICS:
        if st.button(label, key=f"nav_{label}", use_container_width=True):
            st.session_state["current_topic"] = label
            # Chỉ reset điểm khi chuyển sang chủ đề luyện tập (không phải home/sgk/history)
            if NAV_TOPICS[label] not in ("home", "sgk", "history"):
                st.session_state["score"] = 0
                st.session_state["total"] = 0
            st.rerun()

    st.markdown("---")

    # ── Bảng điểm ─────────────────────────────────────────────
    if st.session_state["total"] > 0:
        pct = int(st.session_state["score"] / st.session_state["total"] * 100)
        st.markdown(f"""
        <div class="score-box">
            🏆 Điểm: {st.session_state["score"]}/{st.session_state["total"]}<br>
            <small>{pct}% chính xác</small>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔄 Reset Điểm", use_container_width=True):
        st.session_state["score"] = 0
        st.session_state["total"] = 0
        st.rerun()

    # ── AI Chat ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🤖 Hỏi Gia Sư AI")

    chat_container = st.container(height=250)
    with chat_container:
        for msg in st.session_state["chat_history"]:
            if msg["role"] == "user":
                st.markdown(f"🧒 **Em:** {msg['content']}")
            else:
                st.markdown(f"🤖 **Thầy:** {msg['content']}")

    user_input = st.chat_input("Hỏi thầy bất cứ điều gì...")
    if user_input:
        st.session_state["chat_history"].append({"role": "user", "content": user_input})
        with st.spinner("Thầy đang suy nghĩ..."):
            answer = ask_ai(user_input, st.session_state["chat_history"][:-1])
        st.session_state["chat_history"].append({"role": "assistant", "content": answer})
        st.rerun()

    if st.session_state["chat_history"]:
        if st.button("🗑️ Xóa lịch sử chat", use_container_width=True):
            st.session_state["chat_history"] = []
            st.rerun()

# ─── Main Content ─────────────────────────────────────────────
topic = st.session_state["current_topic"]

# ── Trang Chủ ─────────────────────────────────────────────────
if topic == "🏠 Trang Chủ":
    st.markdown("""
    <div class="main-header">
        <h1>🎓 Học Toán Lớp 4</h1>
        <p>Luyện tập thông minh · Bài tập tự động · Vui học mỗi ngày</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="topic-card"><h3>➕ Cộng & Trừ</h3>
        <p>Phép cộng, trừ các số có nhiều chữ số</p></div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="topic-card"><h3>🍕 Phân Số</h3>
        <p>Khái niệm, so sánh, cộng trừ phân số</p></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="topic-card"><h3>✖️ Nhân & Chia</h3>
        <p>Nhân chia số có nhiều chữ số, chia có dư</p></div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="topic-card"><h3>📐 Hình Học</h3>
        <p>Diện tích, chu vi hình chữ nhật, hình vuông</p></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="topic-card"><h3>📏 Đo Lường</h3>
        <p>Đơn vị đo độ dài, khối lượng, thời gian</p></div>""", unsafe_allow_html=True)
        st.markdown("""
        <div class="topic-card"><h3>📝 Toán Đố</h3>
        <p>Bài toán có lời văn thực tế</p></div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.info("👈 Chọn chủ đề ở thanh bên trái để bắt đầu luyện tập!")
    st.markdown("---")

    # ── Author Section ─────────────────────────────────────────
    st.markdown("""
    <div class="author-card">
        <div class="author-avatar">👨‍🏫</div>
        <div class="author-name">Nguyễn Văn Công</div>
        <div class="author-title">✍️ Tác Giả &amp; Nhà Phát Triển</div>
        <hr class="author-divider"/>
        <div class="author-bio">
            Ứng dụng <b>Học Toán Lớp 4</b> được xây dựng với mong muốn giúp các em học sinh
            luyện tập toán một cách <b>vui vẻ, hiệu quả</b> và <b>tự tin hơn</b> mỗi ngày.
            <br><br>
            Mọi bài tập đều được <b>tạo ngẫu nhiên tự động</b>, giúp các em có thể
            luyện tập không giới hạn mà không bị lặp lại đề cũ.
        </div>
        <br>
        <div style="text-align:center;">
            <span class="author-badge">📚 Giáo Dục</span>
            <span class="author-badge">🐍 Python</span>
            <span class="author-badge">⚡ Streamlit</span>
            <span class="author-badge">🎓 Toán Lớp 4</span>
        </div>
        <div class="author-footer">
            © 2026 Nguyễn Văn Công · Được tạo với ❤️ dành cho các em học sinh
        </div>
    </div>
    """, unsafe_allow_html=True)

# ── Các Chủ Đề Luyện Tập ──────────────────────────────────────
elif topic == "➕ Cộng & Trừ":
    addition_subtraction.show()

elif topic == "✖️ Nhân & Chia":
    multiplication_division.show()

elif topic == "🍕 Phân Số":
    fractions.show()

elif topic == "📐 Hình Học":
    geometry.show()

elif topic == "📏 Đo Lường":
    measurement.show()

elif topic == "📝 Toán Đố":
    word_problems.show()

elif topic == "👨‍👩‍👧 Lịch Sử Làm Bài":
    from utils.history import show_history_page
    show_history_page()

# ── Sách Giáo Khoa ────────────────────────────────────────────
elif topic == "📖 Sách Giáo Khoa":
    st.markdown("## 📖 Sách Giáo Khoa Toán 4")

    if not os.path.exists(PDF_PATH):
        st.error("⚠️ Không tìm thấy file PDF!")
        st.markdown(f"""
        **Hướng dẫn:**
        1. Tạo thư mục `data/` trong project
        2. Đặt file PDF sách toán vào đó
        3. Đổi tên thành `toan4.pdf`

        📁 Đường dẫn cần có: `{PDF_PATH}`
        """)
        st.stop()

    # Đọc tổng số trang thực tế từ PDF
    try:
        import fitz  # PyMuPDF
        _doc = fitz.open(PDF_PATH)
        MAX_PAGE = _doc.page_count
        _doc.close()
    except Exception:
        MAX_PAGE = 200  # fallback nếu chưa cài PyMuPDF

    # ── Nhảy nhanh theo chủ đề ────────────────────────────────
    st.markdown("### 🗂️ Nhảy Đến Chủ Đề")
    topic_cols = st.columns(len(TOPIC_PAGES))
    for i, (topic_key, lessons) in enumerate(TOPIC_PAGES.items()):
        with topic_cols[i]:
            first_page = list(lessons.values())[0]
            if st.button(
                topic_key,
                key=f"jump_{topic_key}",
                use_container_width=True,
                help=f"Nhảy đến trang {first_page}",
            ):
                st.session_state["sgk_page"]   = first_page
                st.session_state["sgk_lesson"] = list(lessons.keys())[0]
                st.rerun()

    st.markdown("---")

    # ── Điều hướng trang ──────────────────────────────────────
    current_page = st.session_state["sgk_page"]   # khai báo 1 lần duy nhất
    col_prev, col_page, col_next, col_goto, col_info = st.columns([1, 1.5, 1, 1, 2.5])

    with col_prev:
        if st.button("⬅️ Trước", use_container_width=True):
            st.session_state["sgk_page"]   = max(1, current_page - 1)
            st.session_state["sgk_lesson"] = ""
            st.rerun()

    with col_page:
        manual_page = st.number_input(
            "Trang:",
            min_value=1,
            max_value=MAX_PAGE,
            value=current_page,
            step=1,
            key="manual_page_input",
            label_visibility="collapsed",
        )

    with col_next:
        if st.button("Sau ➡️", use_container_width=True):
            st.session_state["sgk_page"]   = min(MAX_PAGE, current_page + 1)
            st.session_state["sgk_lesson"] = ""
            st.rerun()

    with col_goto:
        if st.button("📌 Đến Trang", use_container_width=True):
            st.session_state["sgk_page"]   = manual_page
            st.session_state["sgk_lesson"] = ""
            st.rerun()

    with col_info:
        lesson_name = st.session_state["sgk_lesson"]
        if lesson_name:
            st.info(f"📄 Trang **{current_page}** — {lesson_name}")
        else:
            st.info(f"📄 Đang xem trang **{current_page}**")

    st.markdown("---")

    # ── Slider chiều cao ──────────────────────────────────────
    viewer_height = st.slider(
        "Chiều cao khung xem:",
        min_value=400, max_value=1000,
        value=700, step=50,
        key="pdf_height",
    )

    # ── Render PDF ────────────────────────────────────────────
    render_pdf_viewer(PDF_PATH, page=current_page, height=viewer_height)

    # ── Mục lục bài học ───────────────────────────────────────
    st.markdown("---")
    st.markdown("### 📋 Mục Lục Bài Học")
    for topic_key, lessons in TOPIC_PAGES.items():
        with st.expander(f"{topic_key} — {len(lessons)} bài"):
            for lesson_name, page_num in lessons.items():
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"📌 {lesson_name}")
                with col_b:
                    if st.button(
                        f"Trang {page_num}",
                        key=f"toc_{topic_key}_{page_num}",
                        use_container_width=True,
                    ):
                        st.session_state["sgk_page"]   = page_num
                        st.session_state["sgk_lesson"] = lesson_name
                        st.rerun()
