import streamlit as st
import random
from utils.generator import gen_multiplication, gen_division

def show():
    st.markdown("## ✖️ Nhân & Chia Các Số Có Nhiều Chữ Số")

    tab1, tab2, tab3 = st.tabs(["📖 Lý Thuyết", "✏️ Luyện Tập", "🧮 Bảng Nhân"])

    with tab1:
        st.markdown("""
        ### 📌 Phép Nhân
        **Nhân số có nhiều chữ số với số có một chữ số:**
        ```
            1 234
          ×     6
          ──────
            7 404
        ```
        **Nhân số có nhiều chữ số với số có hai chữ số:**
        ```
            123
          ×  45
          ─────
            615   (123 × 5)
          4 920   (123 × 4, viết lùi 1 cột)
          ─────
          5 535
        ```

        ### 📌 Phép Chia
        **Chia hết:**  `a ÷ b = c`  (a = b × c)

        **Chia có dư:**  `a ÷ b = c (dư r)`  (a = b × c + r, với 0 ≤ r < b)

        **Ví dụ:** 4 567 ÷ 7 = 652 (dư 3)

        ### 🔑 Tính Chất
        | Tính chất | Công thức |
        |-----------|-----------|
        | Giao hoán | a × b = b × a |
        | Kết hợp   | (a × b) × c = a × (b × c) |
        | Phân phối | a × (b + c) = a×b + a×c |
        | Nhân với 1 | a × 1 = a |
        | Nhân với 0 | a × 0 = 0 |
        """)

    with tab2:
        st.markdown("### ✏️ Luyện Tập")
        col1, col2 = st.columns([1, 2])
        with col1:
            op = st.selectbox("Chọn phép tính:", ["Nhân ✖️", "Chia ➗", "Hỗn hợp 🔀"], key="mul_div_op")
            level = st.select_slider("Độ khó:", options=[1, 2, 3],
                                     format_func=lambda x: ["Dễ", "Trung bình", "Khó"][x-1],
                                     key="mul_div_level")
            num_q = st.slider("Số câu hỏi:", 3, 10, 5, key="mul_div_num")

        with col2:
            if st.button("🎲 Tạo Bài Tập Mới", key="gen_mul_div", use_container_width=True):
                problems = []
                for _ in range(num_q):
                    if op == "Nhân ✖️":
                        a, b, ans = gen_multiplication(level)
                        problems.append({"type": "mul", "a": a, "b": b, "ans": ans, "rem": None})
                    elif op == "Chia ➗":
                        a, b, q, r = gen_division(level)
                        problems.append({"type": "div", "a": a, "b": b, "ans": q, "rem": r})
                    else:
                        if random.random() > 0.5:
                            a, b, ans = gen_multiplication(level)
                            problems.append({"type": "mul", "a": a, "b": b, "ans": ans, "rem": None})
                        else:
                            a, b, q, r = gen_division(level)
                            problems.append({"type": "div", "a": a, "b": b, "ans": q, "rem": r})
                st.session_state["mul_div_problems"] = problems
                st.session_state["mul_div_user"] = {}

        if "mul_div_problems" in st.session_state:
            problems = st.session_state["mul_div_problems"]
            user = st.session_state.get("mul_div_user", {})

            for i, p in enumerate(problems):
                if p["type"] == "mul":
                    st.markdown(f"**Câu {i+1}:** {p['a']:,} × {p['b']:,} = ?".replace(",", "."))
                    user[f"{i}_q"] = st.number_input("", key=f"mul_{i}", value=0, step=1,
                                                      label_visibility="collapsed")
                    user[f"{i}_r"] = 0
                else:
                    st.markdown(f"**Câu {i+1}:** {p['a']:,} ÷ {p['b']:,} = ? (dư ?)".replace(",", "."))
                    c1, c2 = st.columns(2)
                    with c1:
                        user[f"{i}_q"] = st.number_input("Thương:", key=f"div_q_{i}", value=0, step=1)
                    with c2:
                        user[f"{i}_r"] = st.number_input("Số dư:", key=f"div_r_{i}", value=0, step=1)

            st.session_state["mul_div_user"] = user

            if st.button("✅ Kiểm Tra", key="check_mul_div", use_container_width=True):
                correct = 0
                for i, p in enumerate(problems):
                    uq = user.get(f"{i}_q", 0)
                    ur = user.get(f"{i}_r", 0)
                    if p["type"] == "mul":
                        ok = uq == p["ans"]
                        label = f"{p['a']:,} × {p['b']:,} = {p['ans']:,}".replace(",", ".")
                    else:
                        ok = uq == p["ans"] and ur == p["rem"]
                        label = f"{p['a']:,} ÷ {p['b']:,} = {p['ans']:,} (dư {p['rem']})".replace(",", ".")

                    if ok:
                        correct += 1
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {label} — Đúng!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: Đáp án đúng: {label}</div>', unsafe_allow_html=True)

                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Bạn đúng {correct}/{len(problems)} câu!")

    with tab3:
        st.markdown("### 🧮 Bảng Nhân Tương Tác")
        n = st.slider("Chọn bảng nhân:", 2, 9, 2)
        cols = st.columns(2)
        for i in range(1, 11):
            with cols[(i - 1) % 2]:
                st.markdown(f"**{n} × {i} = {n * i}**")

        st.markdown("---")
        st.markdown("### 🎯 Đố Vui Bảng Nhân")
        if st.button("🎲 Câu Hỏi Ngẫu Nhiên", key="times_table_quiz"):
            a = random.randint(2, 9)
            b = random.randint(1, 10)
            st.session_state["tt_q"] = (a, b, a * b)

        if "tt_q" in st.session_state:
            a, b, ans = st.session_state["tt_q"]
            st.markdown(f"### {a} × {b} = ?")
            user_tt = st.number_input("Đáp án:", key="tt_ans", value=0, step=1)
            if st.button("✅ Kiểm Tra", key="check_tt"):
                if user_tt == ans:
                    st.success(f"🎉 Đúng rồi! {a} × {b} = {ans}")
                    st.session_state.score += 1
                else:
                    st.error(f"❌ Sai! {a} × {b} = {ans}")
                st.session_state.total += 1
