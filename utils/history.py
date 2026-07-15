import os
import json
from datetime import datetime
import streamlit as st

HISTORY_FILE = "data/history.json"


def save_attempt(topic_name, activity_type, details, score, total):
    """Lưu kết quả làm bài của học sinh.

    Hỗ trợ ghi file JSON cục bộ, nếu gặp lỗi ghi file (như phân quyền hoặc cloud ephemeral fs)
    sẽ tự động lưu trữ tạm thời vào st.session_state['history_fallback'].
    """
    record = {
        "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "topic": topic_name,
        "activity": activity_type,
        "score": score,
        "total": total,
        "details": details,
    }

    if "history_fallback" not in st.session_state:
        st.session_state["history_fallback"] = []

    try:
        # Tạo thư mục data nếu chưa có
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

        history = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                try:
                    history = json.load(f)
                    if not isinstance(history, list):
                        history = []
                except Exception:
                    history = []

        history.append(record)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except Exception:
        # Fallback lưu vào Session State nếu không ghi được file
        st.session_state["history_fallback"].append(record)


def load_history():
    """Tải toàn bộ lịch sử kết quả từ tệp tin cục bộ kết hợp với session fallback."""
    history = []
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                history = json.load(f)
                if not isinstance(history, list):
                    history = []
        except Exception:
            pass

    fallback = st.session_state.get("history_fallback", [])
    # Kết hợp hai danh sách, tránh trùng lặp bản ghi trùng khớp hoàn toàn
    combined = list(history)
    for item in fallback:
        if item not in combined:
            combined.append(item)
    return combined


def clear_history():
    """Xóa lịch sử bài làm (cả trên tệp và bộ nhớ tạm)."""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
    except Exception:
        pass
    st.session_state["history_fallback"] = []


def import_history(uploaded_data):
    """Khôi phục dữ liệu từ tệp tin JSON tải lên."""
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

    try:
        os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(merged, f, ensure_ascii=False, indent=2)
        st.session_state["history_fallback"] = []
        return True, f"Khôi phục thành công {len(valid_records)} bài làm!"
    except Exception:
        st.session_state["history_fallback"] = merged
        return (
            True,
            f"Khôi phục tạm thời {len(valid_records)} bài làm vào Session State (Do không thể ghi đè file)!",
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
    with st.expander("💾 Sao Lưu & Phục Hồi Dữ Liệu (Streamlit Cloud)", expanded=False):
        st.markdown("""
        *Lưu ý: Nếu ứng dụng này được deploy trên Streamlit Cloud, dữ liệu lịch sử có thể bị mất khi máy chủ restart. 
        Phụ huynh hãy tải xuống file sao lưu để lưu giữ trên máy tính cá nhân và khôi phục khi cần thiết.*
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
