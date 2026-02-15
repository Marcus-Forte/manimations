from manim import *

from common.helpers import *

config.frame_rate = 30
FLOW_RUNTIME = 1.2
STEP_RUNTIME = 0.4


class RAGDiagram(Scene):
    def construct(self):
        # ── Intro ──────────────────────────────────────────────────────
        # self.next_section(name="Intro", skip_animations=False)

        # rag = RectangleWithText("RAG", color=BLUE, font_size=44)
        # self.play(Create(rag))
        # self.wait(0.5)

        # rag_text = VGroup(
        #     Text("Retrieval"),
        #     Text("Augmented"),
        #     Text("Generation"),
        # ).arrange(RIGHT, buff=0.25).scale(0.85).move_to(rag)
        # self.play(
        #     Transform(rag[1], rag_text),
        #     Transform(rag[0], SurroundingRectangle(rag_text, color=BLUE)),
        # )
        # self.wait(0.8)
        # self.play(FadeOut(rag))

        # ── Phase 1  Indexing ──────────────────────────────────────────
        self.next_section(name="Indexing", skip_animations=False)

        phase_label = Text("Indexing", font_size=34, weight=BOLD, color=BLUE_B)
        phase_label.to_edge(UP, buff=0.55)
        self.play(Write(phase_label), run_time=STEP_RUNTIME)

        # ── Helper: bracket-wrapped matrix ────────────────────────────
        def _make_text_matrix(rows, color=WHITE, font_size=16):
            """Bracket-wrapped grid of Text cells with properly sized brackets."""
            cell_groups = VGroup()
            for row_vals in rows:
                row_group = VGroup(
                    *[Text(v, font_size=font_size, color=color) for v in row_vals]
                ).arrange(RIGHT, buff=0.18)
                cell_groups.add(row_group)
            cell_groups.arrange(DOWN, buff=0.08)
            # Brackets that actually match content height
            content_h = cell_groups.height + 0.15
            l_bracket = Text("[", font_size=14, color=color)
            l_bracket.stretch_to_fit_height(content_h)
            l_bracket.next_to(cell_groups, LEFT, buff=0.06)
            r_bracket = Text("]", font_size=14, color=color)
            r_bracket.stretch_to_fit_height(content_h)
            r_bracket.next_to(cell_groups, RIGHT, buff=0.06)
            return VGroup(l_bracket, cell_groups, r_bracket)

        # ── Build column groups (box + matrix underneath) ─────────────
        # 1) Sentence / Prompt  +  token vector
        doc_sentence = Text(
            '"... Capital of Brazil is Brasília ..."',
            font_size=18,
            color=YELLOW,
        )
        doc_box = SurroundingRectangle(doc_sentence, color=YELLOW, buff=0.14)
        doc = VGroup(doc_box, doc_sentence)
        doc_label = Text("Document", font_size=14, color=YELLOW)

        token_vec = _make_text_matrix([["t1"], ["t2"], ["t3"]], color=YELLOW)
        token_sub = Text("Tokens", font_size=18, color=YELLOW)

        doc_col = VGroup(doc_label, doc, token_vec, token_sub).arrange(DOWN, buff=0.15)

        # 2) Embedding Model  +  weight matrix
        embed_model = RectangleWithText("Embedding\nModel", color=TEAL, font_size=20)

        weight_matrix = _make_text_matrix(
            [["w11", "w12", "w13"],
             ["w21", "w22", "w23"],
             ["w31", "w32", "w33"]],
            color=TEAL,
        )
        weight_sub = Text("Weights", font_size=18, color=TEAL)

        embed_col = VGroup(embed_model, weight_matrix, weight_sub).arrange(DOWN, buff=0.15)

        # 3) "=" sign (plain, vertically centered later)
        equals_sign = Text("=", font_size=22)

        # 4) Embedding vector  +  result matrix
        vec_text = Text("[0.71, -0.33, 0.58, ...]", font_size=16, color=GREEN)
        vec_box = SurroundingRectangle(vec_text, color=GREEN, buff=0.12)
        vec_group = VGroup(vec_box, vec_text)
        vec_label = Text("Embedding", font_size=14, color=GREEN)

        result_vec = _make_text_matrix([["0.71"], ["-0.33"], ["0.58"]], color=GREEN)
        result_sub = Text("Vector", font_size=18, color=GREEN)

        vec_col = VGroup(vec_label, vec_group, result_vec, result_sub).arrange(DOWN, buff=0.15)

        # 5) Vector DB
        db = RectangleWithText("Vector DB", color=PURPLE, font_size=20)
        stored_vecs = VGroup(
            Text("v1", font_size=16, color=GREEN_B),
            Text("v2", font_size=16, color=GREEN_B),
            Text("v3", font_size=16, color=GREEN_B),
            Text("...", font_size=16, color=GREEN_B),
        ).arrange(DOWN, buff=0.08)
        db_col = VGroup(db, stored_vecs).arrange(DOWN, buff=0.2)

        # ── "x" sign between doc_col and embed_col
        times_sign = Text("x", font_size=20)

        # ── Lay out everything in one horizontal row ──────────────────
        full_row = VGroup(doc_col, times_sign, embed_col, equals_sign, vec_col, db_col).arrange(
            RIGHT, buff=0.4
        )
        full_row.move_to(ORIGIN).shift(DOWN * 0.1)
        # Scale to fit frame if needed
        if full_row.width > config.frame_width - 0.8:
            full_row.scale_to_fit_width(config.frame_width - 0.8)

        # Vertically center the operator signs with the matrices
        times_sign.move_to([times_sign.get_x(), weight_matrix.get_y(), 0])
        equals_sign.move_to([equals_sign.get_x(), weight_matrix.get_y(), 0])

        # ── Animate ──────────────────────────────────────────────────
        # Show sentence + tokens
        self.play(FadeIn(doc_label), FadeIn(doc))
        self.wait(0.2)
        self.play(FadeIn(token_vec), FadeIn(token_sub))
        self.wait(0.3)

        # Show embedding model + weights
        self.play(FadeIn(times_sign), Create(embed_model))
        self.play(FadeIn(weight_matrix), FadeIn(weight_sub))
        self.wait(0.3)

        # Show = and result
        self.play(FadeIn(equals_sign))
        self.play(FadeIn(result_vec), FadeIn(result_sub))
        self.wait(0.3)

        # Caption: embeddings capture meaning
        caption = Text(
            "Embeddings capture semantic meaning as numbers",
            font_size=22,
            color=WHITE,
            slant=ITALIC,
        )
        caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(caption, shift=UP * 0.2))
        self.wait(1.0)

        # Show the output embedding box + arrows
        self.play(FadeIn(vec_label), FadeIn(vec_group))
        self.wait(0.3)

        arrow_style = dict(buff=0.05, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=999)
        arrow_doc_to_embed = Arrow(doc.get_right(), embed_model.get_left(), color=WHITE, **arrow_style)
        arrow_embed_to_vec = Arrow(embed_model.get_right(), vec_group.get_left(), color=WHITE, **arrow_style)
        self.play(GrowArrow(arrow_doc_to_embed), GrowArrow(arrow_embed_to_vec))
        self.wait(0.3)

        # Update caption
        caption2 = Text(
            "Similar meanings → nearby vectors directions",
            font_size=22,
            color=WHITE,
            slant=ITALIC,
        )
        caption2.to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, caption2))
        self.wait(0.8)

        # Arrow into Vector DB + storage
        arrow_vec_to_db = Arrow(vec_group.get_right(), db.get_left(), color=PURPLE, **arrow_style)
        self.play(GrowArrow(arrow_vec_to_db), Create(db))
        self.wait(0.3)

        # Show stored vectors
        self.play(FadeIn(stored_vecs, shift=DOWN * 0.15))

        # Final caption for phase 1
        caption3 = Text(
            "Vectors are stored for fast similarity search",
            font_size=22,
            color=WHITE,
            slant=ITALIC,
        )
        caption3.to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, caption3))
        self.wait(1.5)

        # ── Transition to Phase 2 ────────────────────────────────────
        all_phase1 = VGroup(
            phase_label, doc_col, times_sign, embed_col, equals_sign, vec_col, db_col,
            arrow_doc_to_embed, arrow_embed_to_vec, arrow_vec_to_db, caption,
        )
        self.play(FadeOut(all_phase1))

        # ── Phase 2  Retrieval ────────────────────────────────────────
        self.next_section(name="Retrieval", skip_animations=False)

        phase2_label = Text("Retrieval", font_size=34, weight=BOLD, color=BLUE_B)
        phase2_label.to_edge(UP, buff=0.55)
        self.play(Write(phase2_label), run_time=STEP_RUNTIME)

        # Layout:  User Query → Embed → Query Vector → Vector DB → Result

        # User query
        query_sentence = Text(
            '"What is the capital of Brazil?"',
            font_size=18,
            color=YELLOW,
        )
        query_box = SurroundingRectangle(query_sentence, color=YELLOW, buff=0.14)
        query = VGroup(query_box, query_sentence)
        query_label = Text("User Query", font_size=14, color=YELLOW)

        query_tokens = _make_text_matrix([["q1"], ["q2"], ["q3"]], color=YELLOW)
        query_tokens_sub = Text("Tokens", font_size=18, color=YELLOW)

        query_col = VGroup(query_label, query, query_tokens, query_tokens_sub).arrange(DOWN, buff=0.15)

        # Embedding model (reuse style)
        embed2 = RectangleWithText("Embedding\nModel", color=TEAL, font_size=20)

        weight_matrix2 = _make_text_matrix(
            [["w11", "w12", "w13"],
             ["w21", "w22", "w23"],
             ["w31", "w32", "w33"]],
            color=TEAL,
        )
        weight_sub2 = Text("Weights", font_size=18, color=TEAL)

        embed2_col = VGroup(embed2, weight_matrix2, weight_sub2).arrange(DOWN, buff=0.15)

        # = sign
        equals2 = Text("=", font_size=22)

        # Query vector
        qvec_text = Text("[0.69, -0.30, 0.55, ...]", font_size=16, color=GREEN)
        qvec_box = SurroundingRectangle(qvec_text, color=GREEN, buff=0.12)
        qvec_group = VGroup(qvec_box, qvec_text)
        qvec_label = Text("Query Embedding", font_size=14, color=GREEN)

        qresult_vec = _make_text_matrix([["0.69"], ["-0.30"], ["0.55"]], color=GREEN)
        qresult_sub = Text("Vector", font_size=18, color=GREEN)

        qvec_col = VGroup(qvec_label, qvec_group, qresult_vec, qresult_sub).arrange(DOWN, buff=0.15)

        # x sign
        times2 = Text("x", font_size=20)

        # Vector DB (with stored vectors)
        db2 = RectangleWithText("Vector DB", color=PURPLE, font_size=20)
        sim_lines = VGroup(
            Text("cos(q, v1) = 0.97 ✓", font_size=14, color=GREEN_B),
            Text("cos(q, v2) = 0.31", font_size=14, color=RED_B),
            Text("cos(q, v3) = 0.18", font_size=14, color=RED_B),
        ).arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        db2_col = VGroup(db2, sim_lines).arrange(DOWN, buff=0.2)

        # Lay out Phase 2 row
        full_row2 = VGroup(query_col, times2, embed2_col, equals2, qvec_col, db2_col).arrange(
            RIGHT, buff=0.4
        )
        full_row2.move_to(ORIGIN).shift(DOWN * 0.1)
        if full_row2.width > config.frame_width - 0.8:
            full_row2.scale_to_fit_width(config.frame_width - 0.8)

        # Vertically center operators with matrices
        times2.move_to([times2.get_x(), weight_matrix2.get_y(), 0])
        equals2.move_to([equals2.get_x(), weight_matrix2.get_y(), 0])

        # ── Animate Phase 2 ──────────────────────────────────────────

        # Show query + tokens
        self.play(FadeIn(query_label), FadeIn(query))
        self.wait(0.2)
        self.play(FadeIn(query_tokens), FadeIn(query_tokens_sub))
        self.wait(0.3)

        # Embedding model + weights
        self.play(FadeIn(times2), Create(embed2))
        self.play(FadeIn(weight_matrix2), FadeIn(weight_sub2))
        self.wait(0.3)

        # = and result vector
        self.play(FadeIn(equals2))
        self.play(FadeIn(qresult_vec), FadeIn(qresult_sub))
        self.wait(0.3)

        # Show query embedding box + arrows
        self.play(FadeIn(qvec_label), FadeIn(qvec_group))

        arrow2_style = dict(buff=0.05, stroke_width=4, tip_length=0.18, max_tip_length_to_length_ratio=1, max_stroke_width_to_length_ratio=999)
        arrow_q_to_embed = Arrow(query.get_right(), embed2.get_left(), color=WHITE, **arrow2_style)
        arrow_embed_to_qvec = Arrow(embed2.get_right(), qvec_group.get_left(), color=WHITE, **arrow2_style)
        self.play(GrowArrow(arrow_q_to_embed), GrowArrow(arrow_embed_to_qvec))
        self.wait(0.3)

        # Caption
        r_caption = Text(
            "The query is embedded with the same model",
            font_size=22,
            color=WHITE,
            slant=ITALIC,
        )
        r_caption.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(r_caption, shift=UP * 0.2))
        self.wait(0.8)

        # Arrow to Vector DB + similarity search
        arrow_qvec_to_db = Arrow(qvec_group.get_right(), db2.get_left(), color=PURPLE, **arrow2_style)
        self.play(GrowArrow(arrow_qvec_to_db), Create(db2))
        self.wait(0.3)

        r_caption2 = Text(
            "Cosine similarity finds the closest stored vector",
            font_size=22,
            color=WHITE,
            slant=ITALIC,
        )
        r_caption2.to_edge(DOWN, buff=0.4)
        self.play(Transform(r_caption, r_caption2))

        # Show similarity scores
        self.play(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in sim_lines], lag_ratio=0.15))
        self.wait(0.5)

        # Show retrieved result
        result_text = Text(
            '→ "Brasília"',
            font_size=24,
            color=GREEN,
            weight=BOLD,
        )
        result_text.next_to(db2, RIGHT, buff=0.4)
        # Keep it inside the frame
        if result_text.get_right()[0] > config.frame_width / 2 - 0.2:
            result_text.next_to(db2_col, DOWN, buff=0.3)

        r_caption3 = Text(
            "The most relevant chunk is retrieved",
            font_size=22,
            color=WHITE,
            slant=ITALIC,
        )
        r_caption3.to_edge(DOWN, buff=0.4)
        self.play(Transform(r_caption, r_caption3), FadeIn(result_text, shift=UP * 0.15))
        self.wait(1.5)
