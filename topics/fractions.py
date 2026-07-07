import streamlit as st
import random
from math import gcd
from utils.generator import gen_fraction_compare, gen_fraction_add_sub

def simplify(n, d):
    g = gcd(abs(n), abs(d))
    return n // g, d // g

def show():
    st.markdown("## 🍕 Phân Số")

    # ── Liên kết SGK ──────────────────────────────────────────
    from utils.pdf_viewer import render_page_links
    with st.expander("📖 Xem trang SGK liên quan", expanded=False):
        render_page_links("🍕 Phân Số")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📖 Lý Thuyết", "⚖️ So Sánh", "➕ Cộng/Trừ", "🔢 Rút Gọn"
    ])

    with tab1:
        st.markdown("""
        ### 📌 Phân Số Là Gì?
        Phân số có dạng **a/b** (b ≠ 0), trong đó:
        - **a** là **tử số** (phần được lấy)
        - **b** là **mẫu số** (chia thành bao nhiêu phần bằng nhau)

        **Ví dụ:** 3/4 nghĩa là chia 1 cái bánh thành 4 phần bằng nhau, lấy 3 phần.

        ### 📌 So Sánh Phân Số
        - Cùng mẫu số: so sánh tử số
        - Khác mẫu số: quy đồng mẫu số rồi so sánh

        ### 📌 Rút Gọn Phân Số
        Chia cả tử và mẫu cho **ƯCLN** của chúng.

        **Ví dụ:** 6/8 → ƯCLN(6,8) = 2 → 6÷2 / 8÷2 = **3/4**

        ### 📌 Phân Số Bằng Nhau
        a/b = c/d khi a × d = b × c
        """)

        # Visual fraction display
        st.markdown("### 🎨 Minh Họa Phân Số")
        col1, col2 = st.columns(2)
        with col1:
            demo_n = st.number_input("Tử số:", 1, 10, 3, key="demo_n")
        with col2:
            demo_d = st.number_input("Mẫu số:", 1, 10, 4, key="demo_d")

        if demo_d > 0 and demo_n <= demo_d:
            filled = "🟦" * demo_n + "⬜" * (demo_d - demo_n)
            st.markdown(f"**{demo_n}/{demo_d}** = {filled}")
            st.markdown(f"Phần được tô màu: **{demo_n}** trong **{demo_d}** phần bằng nhau")
        elif demo_n > demo_d:
            st.warning("Đây là phân số lớn hơn 1 (phân số giả)!")

    with tab2:
        st.markdown("### ⚖️ So Sánh Phân Số")
        if st.button("🎲 Tạo Bài So Sánh", key="gen_compare"):
            problems = [gen_fraction_compare() for _ in range(5)]
            st.session_state["frac_compare"] = problems
            st.session_state["frac_compare_ans"] = {}

        if "frac_compare" in st.session_state:
            problems = st.session_state["frac_compare"]
            user_signs = {}

            for i, (n1, d1, n2, d2, correct_sign) in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** {n1}/{d1} ☐ {n2}/{d2}")
                user_signs[i] = st.selectbox(
                    f"Chọn dấu câu {i+1}:",
                    [">", "<", "="],
                    key=f"cmp_{i}",
                    label_visibility="collapsed"
                )

            if st.button("✅ Kiểm Tra So Sánh", key="check_compare"):
                correct = 0
                for i, (n1, d1, n2, d2, correct_sign) in enumerate(problems):
                    if user_signs[i] == correct_sign:
                        correct += 1
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {n1}/{d1} {correct_sign} {n2}/{d2} — Đúng!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: {n1}/{d1} <b>{correct_sign}</b> {n2}/{d2} (bạn chọn: {user_signs[i]})</div>', unsafe_allow_html=True)
                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Đúng {correct}/{len(problems)} câu!")

    with tab3:
        st.markdown("### ➕ Cộng & Trừ Phân Số Cùng Mẫu")
        op_frac = st.radio("Phép tính:", ["Cộng ➕", "Trừ ➖"], horizontal=True)

        if st.button("🎲 Tạo Bài Cộng/Trừ", key="gen_frac_add"):
            op = "add" if op_frac == "Cộng ➕" else "sub"
            problems = [gen_fraction_add_sub(op) for _ in range(5)]
            st.session_state["frac_add_problems"] = problems
            st.session_state["frac_add_op"] = op

        if "frac_add_problems" in st.session_state:
            problems = st.session_state["frac_add_problems"]
            op = st.session_state.get("frac_add_op", "add")
            user_ans = {}

            for i, (n1, d1, n2, d2, rn, rd, sym) in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** {n1}/{d1} {sym} {n2}/{d2} = ?/? (rút gọn nếu được)")
                c1, c2 = st.columns(2)
                with c1:
                    user_ans[f"{i}_n"] = st.number_input("Tử số:", key=f"fan_{i}", value=0, step=1)
                with c2:
                    user_ans[f"{i}_d"] = st.number_input("Mẫu số:", key=f"fad_{i}", value=1, step=1)

            if st.button("✅ Kiểm Tra", key="check_frac_add"):
                correct = 0
                for i, (n1, d1, n2, d2, rn, rd, sym) in enumerate(problems):
                    un = user_ans.get(f"{i}_n", 0)
                    ud = user_ans.get(f"{i}_d", 1)
                    # Accept equivalent fractions
                    ok = (un == rn and ud == rd) or (ud != 0 and rn * ud == rd * un)
                    if ok:
                        correct += 1
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {n1}/{d1} {sym} {n2}/{d2} = {rn}/{rd} — Đúng!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: Đáp án đúng = {rn}/{rd}</div>', unsafe_allow_html=True)
                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Đúng {correct}/{len(problems)} câu!")

    with tab4:
        st.markdown("### 🔢 Rút Gọn Phân Số")
        if st.button("🎲 Tạo Bài Rút Gọn", key="gen_simplify"):
            problems = []
            for _ in range(5):
                d = random.choice([4, 6, 8, 9, 10, 12, 15, 16, 18, 20])
                g_val = random.choice([g for g in range(2, d) if d % g == 0])
                n_simplified = random.randint(1, d // g_val - 1)
                n = n_simplified * g_val
                d_orig = d
                rn, rd = simplify(n, d_orig)
                problems.append((n, d_orig, rn, rd))
            st.session_state["simplify_problems"] = problems

        if "simplify_problems" in st.session_state:
            problems = st.session_state["simplify_problems"]
            user_ans = {}

            for i, (n, d, rn, rd) in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** Rút gọn phân số **{n}/{d}**")
                c1, c2 = st.columns(2)
                with c1:
                    user_ans[f"{i}_n"] = st.number_input("Tử số:", key=f"sn_{i}", value=0, step=1)
                with c2:
                    user_ans[f"{i}_d"] = st.number_input("Mẫu số:", key=f"sd_{i}", value=1, step=1)

            if st.button("✅ Kiểm Tra Rút Gọn", key="check_simplify"):
                correct = 0
                for i, (n, d, rn, rd) in enumerate(problems):
                    un = user_ans.get(f"{i}_n", 0)
                    ud = user_ans.get(f"{i}_d", 1)
                    ok = (un == rn and ud == rd)
                    if ok:
                        correct += 1
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {n}/{d} = {rn}/{rd} — Đúng!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: {n}/{d} rút gọn = {rn}/{rd}</div>', unsafe_allow_html=True)
                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Đúng {correct}/{len(problems)} câu!")
