import streamlit as st
import random
from utils.generator import gen_addition, gen_subtraction

def show():
    st.markdown("## ➕ Cộng & Trừ Các Số Có Nhiều Chữ Số")

    tab1, tab2, tab3 = st.tabs(["📖 Lý Thuyết", "✏️ Luyện Tập", "🎯 Kiểm Tra Nhanh"])

    # ── Tab 1: Theory ──────────────────────────────────────────
    with tab1:
        st.markdown("""
        ### 📌 Phép Cộng Các Số Có Nhiều Chữ Số
        **Quy tắc:**
        - Viết các số thẳng cột (hàng đơn vị thẳng hàng đơn vị, hàng chục thẳng hàng chục...)
        - Cộng từ phải sang trái
        - Nếu tổng ≥ 10 thì nhớ sang hàng tiếp theo

        **Ví dụ:**
        ```
          56 789
        + 34 256
        ────────
          91 045
        ```

        ### 📌 Phép Trừ Các Số Có Nhiều Chữ Số
        **Quy tắc:**
        - Viết số bị trừ ở trên, số trừ ở dưới, thẳng cột
        - Trừ từ phải sang trái
        - Nếu chữ số hàng trên nhỏ hơn hàng dưới thì mượn 1 từ hàng tiếp theo

        **Ví dụ:**
        ```
          73 456
        - 28 179
        ────────
          45 277
        ```

        ### 🔑 Tính Chất Phép Cộng
        | Tính chất | Công thức |
        |-----------|-----------|
        | Giao hoán | a + b = b + a |
        | Kết hợp   | (a + b) + c = a + (b + c) |
        | Cộng với 0 | a + 0 = a |
        """)

    # ── Tab 2: Practice ────────────────────────────────────────
    with tab2:
        st.markdown("### ✏️ Luyện Tập")

        col1, col2 = st.columns([1, 2])
        with col1:
            op = st.selectbox("Chọn phép tính:", ["Cộng ➕", "Trừ ➖", "Hỗn hợp 🔀"])
            level = st.select_slider("Độ khó:", options=[1, 2, 3],
                                     format_func=lambda x: ["Dễ", "Trung bình", "Khó"][x-1])
            num_q = st.slider("Số câu hỏi:", 3, 10, 5)

        with col2:
            if st.button("🎲 Tạo Bài Tập Mới", use_container_width=True):
                problems = []
                for _ in range(num_q):
                    if op == "Cộng ➕":
                        a, b, ans = gen_addition(level)
                        problems.append({"a": a, "b": b, "ans": ans, "op": "+"})
                    elif op == "Trừ ➖":
                        a, b, ans = gen_subtraction(level)
                        problems.append({"a": a, "b": b, "ans": ans, "op": "-"})
                    else:
                        if random.random() > 0.5:
                            a, b, ans = gen_addition(level)
                            problems.append({"a": a, "b": b, "ans": ans, "op": "+"})
                        else:
                            a, b, ans = gen_subtraction(level)
                            problems.append({"a": a, "b": b, "ans": ans, "op": "-"})
                st.session_state["add_sub_problems"] = problems
                st.session_state["add_sub_answers"] = {}
                st.session_state["add_sub_checked"] = False

        if "add_sub_problems" in st.session_state:
            problems = st.session_state["add_sub_problems"]
            answers = st.session_state.get("add_sub_answers", {})

            for i, p in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** &nbsp; {p['a']:,} {p['op']} {p['b']:,} = ?".replace(",", "."))
                answers[i] = st.number_input(
                    f"Đáp án câu {i+1}:",
                    value=0, step=1, key=f"add_sub_{i}",
                    label_visibility="collapsed"
                )

            st.session_state["add_sub_answers"] = answers

            if st.button("✅ Kiểm Tra Đáp Án", use_container_width=True):
                correct = 0
                for i, p in enumerate(problems):
                    if answers.get(i) == p["ans"]:
                        correct += 1
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {p["a"]:,} {p["op"]} {p["b"]:,} = <b>{p["ans"]:,}</b> — Đúng!</div>'.replace(",", "."), unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: Đáp án đúng là <b>{p["ans"]:,}</b> (bạn trả lời: {answers.get(i, 0):,})</div>'.replace(",", "."), unsafe_allow_html=True)

                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Bạn đúng {correct}/{len(problems)} câu!")

    # ── Tab 3: Quick Quiz ──────────────────────────────────────
    with tab3:
        st.markdown("### 🎯 Kiểm Tra Nhanh — Điền Số Còn Thiếu")
        st.markdown("Tìm số **?** trong các phép tính sau:")

        if st.button("🎲 Tạo Câu Hỏi Mới", key="quick_add"):
            quizzes = []
            for _ in range(4):
                a, b, ans = gen_addition(random.randint(1, 2))
                qtype = random.choice(["find_b", "find_a", "find_ans"])
                quizzes.append({"a": a, "b": b, "ans": ans, "qtype": qtype})
            st.session_state["quick_add_quiz"] = quizzes

        if "quick_add_quiz" in st.session_state:
            quizzes = st.session_state["quick_add_quiz"]
            user_ans = {}
            for i, q in enumerate(quizzes):
                if q["qtype"] == "find_ans":
                    st.markdown(f"**{i+1}.** {q['a']:,} + {q['b']:,} = **?**".replace(",", "."))
                    user_ans[i] = (st.number_input("", key=f"qa_{i}", value=0, step=1,
                                                    label_visibility="collapsed"), q["ans"])
                elif q["qtype"] == "find_b":
                    st.markdown(f"**{i+1}.** {q['a']:,} + **?** = {q['ans']:,}".replace(",", "."))
                    user_ans[i] = (st.number_input("", key=f"qa_{i}", value=0, step=1,
                                                    label_visibility="collapsed"), q["b"])
                else:
                    st.markdown(f"**{i+1}.** **?** + {q['b']:,} = {q['ans']:,}".replace(",", "."))
                    user_ans[i] = (st.number_input("", key=f"qa_{i}", value=0, step=1,
                                                    label_visibility="collapsed"), q["a"])

            if st.button("✅ Nộp Bài", key="submit_quick_add"):
                score = sum(1 for v, correct in user_ans.values() if v == correct)
                st.session_state.score += score
                st.session_state.total += len(quizzes)
                for i, (v, correct) in user_ans.items():
                    if v == correct:
                        st.markdown(f'<div class="correct-answer">✅ Câu {i+1}: {correct:,} — Đúng!</div>'.replace(",", "."), unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="wrong-answer">❌ Câu {i+1}: Đáp án đúng là {correct:,}</div>'.replace(",", "."), unsafe_allow_html=True)
