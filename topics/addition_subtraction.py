import streamlit as st
import random
from utils.generator import gen_addition, gen_subtraction
from utils.ai_tutor import explain_wrong_answer, generate_hint


def show():
    st.markdown("## ➕ Cộng & Trừ Các Số Có Nhiều Chữ Số")

    # ── Liên kết SGK ──────────────────────────────────────────
    from utils.pdf_viewer import render_page_links
    with st.expander("📖 Xem trang SGK liên quan", expanded=False):
        render_page_links("➕ Cộng & Trừ")

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
                st.session_state["add_sub_answers"]  = {}
                st.session_state["add_sub_checked"]  = False
                # Reset AI state
                st.session_state.pop("prac_wrong_list",   None)
                st.session_state.pop("prac_hint_text",    None)
                st.session_state.pop("prac_explain_text", None)

        if "add_sub_problems" in st.session_state:
            problems = st.session_state["add_sub_problems"]
            answers  = st.session_state.get("add_sub_answers", {})

            for i, p in enumerate(problems):
                st.markdown(f"**Câu {i+1}:** &nbsp; {p['a']:,} {p['op']} {p['b']:,} = ?".replace(",", "."))
                answers[i] = st.number_input(
                    f"Đáp án câu {i+1}:",
                    value=0, step=1, key=f"add_sub_{i}",
                    label_visibility="collapsed"
                )

            st.session_state["add_sub_answers"] = answers

            if st.button("✅ Kiểm Tra Đáp Án", use_container_width=True):
                correct    = 0
                wrong_list = []
                details    = []

                for i, p in enumerate(problems):
                    is_ok = (answers.get(i) == p["ans"])
                    q_str = f"{p['a']} {p['op']} {p['b']}"
                    details.append({
                        "question": q_str,
                        "correct_answer": str(p["ans"]),
                        "student_answer": str(answers.get(i, 0)),
                        "is_correct": is_ok
                    })
                    if is_ok:
                        correct += 1
                        st.markdown(
                            f'<div class="correct-answer">✅ Câu {i+1}: '
                            f'{p["a"]:,} {p["op"]} {p["b"]:,} = <b>{p["ans"]:,}</b> — Đúng!</div>'
                            .replace(",", "."),
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="wrong-answer">❌ Câu {i+1}: '
                            f'Đáp án đúng là <b>{p["ans"]:,}</b> '
                            f'(bạn trả lời: {answers.get(i, 0):,})</div>'
                            .replace(",", "."),
                            unsafe_allow_html=True
                        )
                        wrong_list.append({
                            "question": q_str,
                            "correct":  str(p["ans"]),
                            "student":  str(answers.get(i, 0)),
                        })

                st.session_state.score += correct
                st.session_state.total += len(problems)
                st.success(f"🎉 Bạn đúng {correct}/{len(problems)} câu!")
                st.session_state["prac_wrong_list"] = wrong_list
                
                # Lưu lịch sử
                from utils.history import save_attempt
                save_attempt("➕ Cộng & Trừ", "Luyện Tập", details, correct, len(problems))
                # Reset nội dung AI cũ khi kiểm tra lại
                st.session_state.pop("prac_hint_text",    None)
                st.session_state.pop("prac_explain_text", None)

            # ── AI hỗ trợ ─────────────────────────────────────
            wrong_list = st.session_state.get("prac_wrong_list", [])
            if wrong_list:
                st.markdown("---")
                st.markdown("#### 🤖 Hỗ Trợ AI")

                wrong_labels = [
                    f"Câu: {w['question']} (bạn trả lời '{w['student']}')"
                    for w in wrong_list
                ]
                selected_idx = 0
                if len(wrong_list) > 1:
                    selected = st.selectbox(
                        "Chọn câu muốn hỏi AI:",
                        wrong_labels,
                        key="prac_select_wrong"
                    )
                    selected_idx = wrong_labels.index(selected)
                chosen = wrong_list[selected_idx]

                col_hint, col_explain = st.columns(2)

                with col_hint:
                    if st.button("💡 Gợi ý", key="prac_hint"):
                        with st.spinner("AI đang nghĩ..."):
                            st.session_state["prac_hint_text"] = generate_hint(
                                chosen["question"], "Cộng Trừ Số Có Nhiều Chữ Số"
                            )
                    if "prac_hint_text" in st.session_state:
                        st.info(f"💡 {st.session_state['prac_hint_text']}")

                with col_explain:
                    if st.button("🤖 Giải thích", key="prac_explain"):
                        with st.spinner("AI đang giải thích..."):
                            st.session_state["prac_explain_text"] = explain_wrong_answer(
                                question       = chosen["question"],
                                correct_answer = chosen["correct"],
                                student_answer = chosen["student"],
                                topic          = "Cộng Trừ Số Có Nhiều Chữ Số"
                            )
                    if "prac_explain_text" in st.session_state:
                        st.warning(f"🤖 {st.session_state['prac_explain_text']}")

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
            # Reset AI state
            st.session_state.pop("quiz_wrong_list",   None)
            st.session_state.pop("quiz_hint_text",    None)
            st.session_state.pop("quiz_explain_text", None)

        if "quick_add_quiz" in st.session_state:
            quizzes  = st.session_state["quick_add_quiz"]
            user_ans = {}

            for i, q in enumerate(quizzes):
                if q["qtype"] == "find_ans":
                    st.markdown(f"**{i+1}.** {q['a']:,} + {q['b']:,} = **?**".replace(",", "."))
                    user_ans[i] = (
                        st.number_input("", key=f"qa_{i}", value=0, step=1,
                                        label_visibility="collapsed"),
                        q["ans"],
                        f"{q['a']} + {q['b']} = ?"
                    )
                elif q["qtype"] == "find_b":
                    st.markdown(f"**{i+1}.** {q['a']:,} + **?** = {q['ans']:,}".replace(",", "."))
                    user_ans[i] = (
                        st.number_input("", key=f"qa_{i}", value=0, step=1,
                                        label_visibility="collapsed"),
                        q["b"],
                        f"{q['a']} + ? = {q['ans']}"
                    )
                else:
                    st.markdown(f"**{i+1}.** **?** + {q['b']:,} = {q['ans']:,}".replace(",", "."))
                    user_ans[i] = (
                        st.number_input("", key=f"qa_{i}", value=0, step=1,
                                        label_visibility="collapsed"),
                        q["a"],
                        f"? + {q['b']} = {q['ans']}"
                    )

            if st.button("✅ Nộp Bài", key="submit_quick_add"):
                score      = 0
                wrong_list = []
                details    = []

                for i, (v, correct_val, question_str) in user_ans.items():
                    is_ok = (v == correct_val)
                    details.append({
                        "question": question_str,
                        "correct_answer": str(correct_val),
                        "student_answer": str(v),
                        "is_correct": is_ok
                    })
                    if is_ok:
                        score += 1
                        st.markdown(
                            f'<div class="correct-answer">✅ Câu {i+1}: '
                            f'{correct_val:,} — Đúng!</div>'.replace(",", "."),
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f'<div class="wrong-answer">❌ Câu {i+1}: '
                            f'Đáp án đúng là {correct_val:,}</div>'.replace(",", "."),
                            unsafe_allow_html=True
                        )
                        wrong_list.append({
                            "question": question_str,
                            "correct":  str(correct_val),
                            "student":  str(v),
                        })

                st.session_state.score += score
                st.session_state.total += len(quizzes)
                st.success(f"🎉 Bạn đúng {score}/{len(quizzes)} câu!")
                st.session_state["quiz_wrong_list"] = wrong_list
                
                # Lưu lịch sử
                from utils.history import save_attempt
                save_attempt("➕ Cộng & Trừ", "Kiểm Tra Nhanh", details, score, len(quizzes))
                # Reset nội dung AI cũ khi nộp bài lại
                st.session_state.pop("quiz_hint_text",    None)
                st.session_state.pop("quiz_explain_text", None)

            # ── AI hỗ trợ ─────────────────────────────────────
            wrong_list = st.session_state.get("quiz_wrong_list", [])
            if wrong_list:
                st.markdown("---")
                st.markdown("#### 🤖 Hỗ Trợ AI")

                wrong_labels = [
                    f"Câu: {w['question']} (bạn trả lời '{w['student']}')"
                    for w in wrong_list
                ]
                selected_idx = 0
                if len(wrong_list) > 1:
                    selected = st.selectbox(
                        "Chọn câu muốn hỏi AI:",
                        wrong_labels,
                        key="quiz_select_wrong"
                    )
                    selected_idx = wrong_labels.index(selected)
                chosen = wrong_list[selected_idx]

                col_hint, col_explain = st.columns(2)

                with col_hint:
                    if st.button("💡 Gợi ý", key="quiz_hint"):
                        with st.spinner("AI đang nghĩ..."):
                            st.session_state["quiz_hint_text"] = generate_hint(
                                chosen["question"], "Cộng Trừ Số Có Nhiều Chữ Số"
                            )
                    if "quiz_hint_text" in st.session_state:
                        st.info(f"💡 {st.session_state['quiz_hint_text']}")

                with col_explain:
                    if st.button("🤖 Giải thích", key="quiz_explain"):
                        with st.spinner("AI đang giải thích..."):
                            st.session_state["quiz_explain_text"] = explain_wrong_answer(
                                question       = chosen["question"],
                                correct_answer = chosen["correct"],
                                student_answer = chosen["student"],
                                topic          = "Cộng Trừ Số Có Nhiều Chữ Số"
                            )
                    if "quiz_explain_text" in st.session_state:
                        st.warning(f"🤖 {st.session_state['quiz_explain_text']}")
