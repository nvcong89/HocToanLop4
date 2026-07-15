import json
from datetime import datetime
import streamlit as st
from streamlit_local_storage import LocalStorage

# Khởi tạo đối tượng LocalStorage ở client
localS = LocalStorage()


def load_history():
    """Tải toàn bộ lịch sử kết quả từ Browser Local Storage.

    Sử dụng cơ chế cache trong st.session_state['history_cached'] để tối ưu hóa hiệu năng
    và tránh độ trễ bất đồng bộ (async lag) của Streamlit Custom Components.
    """
    if "history_cached" in st.session_state:
        return st.session_state["history_cached"]

    try:
        val = localS.getItem("student_history")
    except Exception:
        val = None

    if val is not None:
        history = []
        try:
            raw_str = None
            if isinstance(val, str):
                raw_str = val
            elif isinstance(val, dict):
                raw_str = (
                    val.get("value")
                    if isinstance(val.get("value"), str)
                    else json.dumps(val.get("value"), ensure_ascii=False)
                )

            if raw_str:
                history = json.loads(raw_str)
            elif isinstance(val, list):
                history = val
        except Exception:
            history = []

        # Lưu vào cache để sử dụng lập tức cho các lần chạy sau
        st.session_state["history_cached"] = history
        return history

    # Trong khi chờ LocalStorage tải, trả về danh sách fallback trong Session State
    return st.session_state.get("history_fallback", [])


def save_attempt(topic_name, activity_type, details, score, total):
    """Lưu kết quả làm bài của học sinh trực tiếp vào Browser Local Storage."""
    record = {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "topic": topic_name,
        "activity": activity_type,
        "score": score,
        "total": total,
        "details": details,
    }

    history = load_history()

    # Tránh lưu trùng lặp bản ghi
    if record not in history:
        history.append(record)

    # Cập nhật cache và bộ nhớ fallback
    st.session_state["history_cached"] = history
    st.session_state["history_fallback"] = history

    # Đồng bộ ghi vào Browser Local Storage dưới dạng chuỗi JSON
    try:
        localS.setItem("student_history", json.dumps(history, ensure_ascii=False))
    except Exception:
        pass


def clear_history():
    """Xóa lịch sử bài làm trong cả cache và Browser Local Storage."""
    st.session_state.pop("history_cached", None)
    st.session_state["history_fallback"] = []
    try:
        localS.setItem("student_history", "[]")
    except Exception:
        pass


def import_history(uploaded_data):
    """Khôi phục dữ liệu từ tệp tin JSON tải lên trình duyệt."""
    if not isinstance(uploaded_data, list):
        return False, "Dữ liệu không đúng định dạng JSON danh sách!"

    valid_records = []
    for record in uploaded_data:
        if (
            isinstance(record, dict)
            and "timestamp" in record
            and "topic" in record
            and "activity" in record
            and "score" in record
            and "total" in record
        ):
            valid_records.append(record)

    if not valid_records:
        return False, "Không tìm thấy bản ghi lịch sử làm bài hợp lệ!"

    current = load_history()
    merged = list(current)
    for r in valid_records:
        if r not in merged:
            merged.append(r)

    # Ghi vào bộ nhớ đệm
    st.session_state["history_cached"] = merged
    st.session_state["history_fallback"] = merged

    # Ghi đè vào Local Storage
    try:
        localS.setItem("student_history", json.dumps(merged, ensure_ascii=False))
        return True, f"Khôi phục thành công {len(valid_records)} bài làm!"
    except Exception as e:
        return (
            True,
            f"Khôi phục tạm thời {len(valid_records)} bài làm vào Bộ nhớ tạm (Lỗi LocalStorage: {str(e)})!",
        )


def show_history_page():
    """Hiển thị giao diện Lịch Sử Làm Bài cho phụ huynh."""
    st.markdown("""
    <div class="main-header">
        <h1>👨‍👩‍👧 Nhật Ký Học Tập Của Con</h1>
        <p>Báo cáo chi tiết kết quả làm bài tập tự luyện và thi thử</p>
    </div>
    """, unsafe_allow_html=True)

    history = load_history()

    if not history:
        st.info("🧒 Bé chưa thực hiện bài luyện tập nào. Hãy khuyến khích bé chọn một chủ đề học ở menu bên trái nhé!")

        # Vẫn cho phép nhập file backup cũ ở màn hình trống
        with st.expander("📥 Nhập Lịch Sử Cũ (Từ File Backup)", expanded=True):
            uploaded_file = st.file_uploader(
                "Tải lên tệp sao lưu lịch sử (.json):", type="json", key="empty_import"
            )
            if uploaded_file is not None:
                try:
                    data = json.load(uploaded_file)
                    success, msg = import_history(data)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                except Exception as e:
                    st.error(f"Lỗi đọc file: {str(e)}")
        return

    # ── 1. Thống kê tổng quan ─────────────────────────────────────────
    total_attempts = len(history)
    total_questions = sum(h["total"] for h in history)
    total_correct = sum(h["score"] for h in history)
    avg_accuracy = int(total_correct / total_questions * 100) if total_questions > 0 else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tổng số bài đã làm", f"{total_attempts} lượt")
    with col2:
        st.metric("Tổng số câu hỏi", f"{total_questions} câu")
    with col3:
        st.metric("Tỷ lệ đúng trung bình", f"{avg_accuracy}%")

    st.markdown("---")

    # ── 2. Sao lưu & Khôi phục ───────────────────────────────────────
    with st.expander("💾 Sao Lưu & Phục Hồi Dữ Liệu", expanded=False):
        st.markdown("""
        *Lịch sử học tập của con hiện được tự động lưu trữ trên trình duyệt của thiết bị này (iPad/Máy tính).*
        *Nếu phụ huynh muốn xem lịch sử của con trên một thiết bị khác, hãy tải xuống file sao lưu ở thiết bị này và tải lên thiết bị mới.*
        """)

        col_down, col_up = st.columns(2)
        with col_down:
            history_json = json.dumps(history, ensure_ascii=False, indent=2)
            st.download_button(
                label="📥 Tải xuống lịch sử làm bài (JSON)",
                data=history_json,
                file_name=f"lich_su_toan_4_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True,
            )

        with col_up:
            uploaded_file = st.file_uploader(
                "Tải lên tệp sao lưu cũ để nhập dữ liệu:", type="json", key="active_import"
            )
            if uploaded_file is not None:
                try:
                    data = json.load(uploaded_file)
                    success, msg = import_history(data)
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                except Exception as e:
                    st.error(f"Lỗi đọc file: {str(e)}")

    st.markdown("---")

    # ── 3. Phân tích theo chủ đề ──────────────────────────────────────
    st.markdown("### 📊 Tiến Độ Theo Từng Chủ Đề")
    breakdown = {}
    for h in history:
        t = h["topic"]
        if t not in breakdown:
            breakdown[t] = {"attempts": 0, "score": 0, "total": 0}
        breakdown[t]["attempts"] += 1
        breakdown[t]["score"] += h["score"]
        breakdown[t]["total"] += h["total"]

    # Tạo bảng markdown
    table_md = "| Chủ Đề Toán Học | Số Lượt Làm | Đúng / Tổng Số Câu | Tỷ Lệ Chính Xác |\n"
    table_md += "| :--- | :---: | :---: | :---: |\n"
    for t, stat in breakdown.items():
        acc = int(stat["score"] / stat["total"] * 100) if stat["total"] > 0 else 0
        table_md += f"| {t} | **{stat['attempts']}** | {stat['score']}/{stat['total']} | **{acc}%** |\n"
    st.markdown(table_md)

    st.markdown("---")

    # ── 4. Nhật ký chi tiết các lần làm bài ────────────────────────────
    st.markdown("### 🕒 Nhật Ký Làm Bài Chi Tiết (Mới nhất trước)")

    for idx, h in enumerate(reversed(history)):
        title = f"🕒 {h['timestamp']} — {h['topic']} ({h['activity']}) — Kết quả: {h['score']}/{h['total']} câu đúng"
        with st.expander(title):
            for i, det in enumerate(h.get("details", [])):
                q_text = det.get("question", "")
                stu_ans = det.get("student_answer", "")
                corr_ans = det.get("correct_answer", "")
                is_ok = det.get("is_correct", False)

                if is_ok:
                    st.markdown(
                        f'<div class="correct-answer" style="margin-bottom: 8px;">'
                        f'✅ <b>Câu {i+1}:</b> {q_text}<br>'
                        f'Con trả lời: <b>{stu_ans}</b> — Đúng!</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div class="wrong-answer" style="margin-bottom: 8px;">'
                        f'❌ <b>Câu {i+1}:</b> {q_text}<br>'
                        f'Con trả lời: <b>{stu_ans}</b> (Đáp án đúng là: <b>{corr_ans}</b>)</div>',
                        unsafe_allow_html=True,
                    )

    # ── 5. Xóa lịch sử ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### ⚙️ Cài đặt")
    if st.checkbox("⚠️ Tôi muốn xóa toàn bộ lịch sử học tập hiện tại"):
        if st.button("🗑️ Xác Nhận Xóa Vĩnh Viễn", type="primary", use_container_width=True):
            clear_history()
            st.success("Đã xóa toàn bộ lịch sử làm bài!")
            st.rerun()
