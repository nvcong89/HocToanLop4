import streamlit as st
import random
from utils.generator import gen_unit_conversion

def show():
    st.markdown("## 📏 Đo Lường")

    # ── Liên kết SGK ──────────────────────────────────────────
    from utils.pdf_viewer import render_page_links
    with st.expander("📖 Xem trang SGK liên quan", expanded=False):
        render_page_links("📏 Đo Lường")

    tab1, tab2, tab3 = st.tabs(["📖 Bảng Đơn Vị", "✏️ Đổi Đơn Vị", "⏰ Thời Gian"])

    with tab1:
        st.markdown("""
        ### 📏 Đơn Vị Đo Độ Dài
        | Đơn vị | Ký hiệu | Quy đổi |
        |--------|---------|---------|
        | Ki-lô-mét | km | 1 km = 1 000 m |
        | Mét | m | 1 m = 10 dm |
        | Đề-xi-mét | dm | 1 dm = 10 cm |
        | Xen-ti-mét | cm | 1 cm = 10 mm |
        | Mi-li-mét | mm | — |

        ### ⚖️ Đơn Vị Đo Khối Lượng
        | Đơn vị | Ký hiệu | Quy đổi |
        |--------|---------|---------|
        | Tấn | t | 1 t = 10 tạ = 1 000 kg |
        | Tạ | — | 1 tạ = 10 yến = 100 kg |
        | Yến | — | 1 yến = 10 kg |
        | Ki-lô-gam | kg | 1 kg = 1 000 g |
        | Gam | g | — |

        ### ⏰ Đơn Vị Đo Thời Gian
        | Đơn vị | Quy đổi |
        |--------|---------|
        | 1 thế kỷ | = 100 năm |
        | 1 năm | = 12 tháng = 365 ngày |
        | 1 tuần | = 7 ngày |
        | 1 ngày | = 24 giờ |
        | 1 giờ | = 60 phút |
        | 1 phút | = 60 giây |
        """)

    with tab2:
        st.markdown("### ✏️ Luyện Đổi Đơn Vị")
        unit_type = st.radio("Loại đơn vị:", ["Độ dài", "Khối lượng", "Thời gian"], horizontal=True)
        num_q = st.slider("Số câu:", 3, 30, 5, key="meas_num")

        type_map = {"Độ dài": "length", "Khối lượng": "weight", "Thời gian": "time"}

        if st.button("🎲 Tạo Bài Đổi Đơn Vị", key="gen_unit"):
            problems = [gen_unit_conversion(type_map[unit_type]) for _ in range(num_q)]
            st.session_state["unit_problems"] = problems
            st.session_state["unit_user"] = {}

        if "unit_problems" in st.session_state:
            problems = st.session_state["unit_problems"]
            user = st.session_state.get("unit_user", {})

            for i, (val, from_u, to_u, ans) in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** {val} {from_u} = ? {to_u}")
                user[i] = st.number_input("", key=f"unit_{i}", value=0, step=1,
                                           label_visibility="collapsed")

            st.session_state["unit_user"] = user

            if st.button("✅ Kiểm Tra Đổi Đơn Vị", key="check_unit"):
                correct = 0
                details = []
                for i, (val, from_u, to_u, ans) in enumerate(problems):
                    stu_val = user.get(i, 0)
                    is_ok = (stu_val == ans)
                    details.append({
                        "question": f"{val} {from_u} = ? {to_u}",
                        "correct_answer": f"{ans} {to_u}",
                        "student_answer": f"{stu_val} {to_u}",
                        "is_correct": is_ok
                    })
                    if is_ok:
                        correct += 1
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {val} {from_u} = {ans} {to_u} — Đúng!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: {val} {from_u} = {ans} {to_u}</div>', unsafe_allow_html=True)
                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Đúng {correct}/{len(problems)} câu!")
                
                # Lưu lịch sử
                from utils.history import save_attempt
                save_attempt("📏 Đo Lường", "Đổi Đơn Vị", details, correct, len(problems))

    with tab3:
        st.markdown("### ⏰ Bài Tập Thời Gian")
        if st.button("🎲 Tạo Bài Thời Gian", key="gen_time"):
            time_problems = []
            for _ in range(4):
                ptype = random.choice(["elapsed", "clock_read", "convert"])
                if ptype == "elapsed":
                    h1 = random.randint(6, 11)
                    m1 = random.choice([0, 15, 30, 45])
                    duration_h = random.randint(0, 3)
                    duration_m = random.choice([0, 15, 30, 45])
                    total_m = h1 * 60 + m1 + duration_h * 60 + duration_m
                    h2 = total_m // 60 % 24
                    m2 = total_m % 60
                    time_problems.append({
                        "type": "elapsed",
                        "q": f"Bắt đầu lúc {h1:02d}:{m1:02d}, kéo dài {duration_h} giờ {duration_m} phút. Kết thúc lúc mấy giờ?",
                        "ans": f"{h2:02d}:{m2:02d}",
                        "ans_val": h2 * 60 + m2
                    })
                else:
                    val, from_u, to_u, ans = gen_unit_conversion("time")
                    time_problems.append({
                        "type": "convert",
                        "q": f"{val} {from_u} = ? {to_u}",
                        "ans": str(ans),
                        "ans_val": ans
                    })
            st.session_state["time_problems"] = time_problems

        if "time_problems" in st.session_state:
            time_problems = st.session_state["time_problems"]
            user_time = {}

            for i, tp in enumerate(time_problems):
                st.markdown(f"**Câu {i+1}:** {tp['q']}")
                if tp["type"] == "elapsed":
                    user_time[i] = st.text_input("Giờ kết thúc (HH:MM):", key=f"tp_{i}",
                                                   placeholder="VD: 09:30")
                else:
                    user_time[i] = st.text_input("Đáp án:", key=f"tp_{i}")

            if st.button("✅ Kiểm Tra Thời Gian", key="check_time"):
                correct = 0
                details = []
                for i, tp in enumerate(time_problems):
                    user_val = user_time.get(i, "").strip()
                    is_ok = (user_val == tp["ans"])
                    details.append({
                        "question": tp["q"],
                        "correct_answer": tp["ans"],
                        "student_answer": user_val,
                        "is_correct": is_ok
                    })
                    if is_ok:
                        correct += 1
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {tp["ans"]} — Đúng!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: Đáp án đúng là <b>{tp["ans"]}</b></div>', unsafe_allow_html=True)
                st.session_state.score += correct
                st.session_state.total += len(time_problems)
                st.success(f"🎉 Đúng {correct}/{len(time_problems)} câu!")
                
                # Lưu lịch sử
                from utils.history import save_attempt
                save_attempt("📏 Đo Lường", "Bài Tập Thời Gian", details, correct, len(time_problems))

