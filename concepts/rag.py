from manim import *

from common.helpers import *

config.frame_rate = 30
FLOW_RUNTIME = 1.2
STEP_RUNTIME = 0.4


class RAGDiagram(Scene):
    def construct(self):
        # ── Intro ──────────────────────────────────────────────────────
        self.next_section(name="Intro", skip_animations=False)

        rag = RectangleWithText("RAG", color=BLUE, font_size=44)
        self.play(Create(rag))
        self.wait(0.5)

        rag_text = VGroup(
            Text("Retrieval"),
            Text("Augmented"),
            Text("Generation"),
        ).arrange(RIGHT, buff=0.25).scale(0.85).move_to(rag)
        self.play(
            Transform(rag[1], rag_text),
            Transform(rag[0], SurroundingRectangle(rag_text, color=BLUE)),
        )
        self.wait(0.8)
        self.play(FadeOut(rag))

        # ── Phase 1  Indexing ──────────────────────────────────────────
        self.next_section(name="Indexing", skip_animations=False)

        phase_label = Text("Indexing", font_size=34, weight=BOLD, color=BLUE_B)
        phase_label.to_edge(UP, buff=0.35)
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
            '"What is the capital of Brazil?"',
            font_size=18,
            color=YELLOW,
        )
        doc_box = SurroundingRectangle(doc_sentence, color=YELLOW, buff=0.14)
        doc = VGroup(doc_box, doc_sentence)
        doc_label = Text("Sentence / Prompt", font_size=14, color=YELLOW)

        token_vec = _make_text_matrix([["t1"], ["t2"], ["t3"]], color=YELLOW)
        token_sub = Text("Tokens", font_size=13, color=YELLOW)

        doc_col = VGroup(doc_label, doc, token_vec, token_sub).arrange(DOWN, buff=0.15)

        # 2) Embedding Model  +  weight matrix
        embed_model = RectangleWithText("Embedding\nModel", color=TEAL, font_size=20)

        weight_matrix = _make_text_matrix(
            [["w11", "w12", "w13"],
             ["w21", "w22", "w23"],
             ["w31", "w32", "w33"]],
            color=TEAL,
        )
        weight_sub = Text("Weights", font_size=13, color=TEAL)

        embed_col = VGroup(embed_model, weight_matrix, weight_sub).arrange(DOWN, buff=0.15)

        # 3) "=" sign (plain, vertically centered later)
        equals_sign = Text("=", font_size=22)

        # 4) Embedding vector  +  result matrix
        vec_text = Text("[0.71, -0.33, 0.58, ...]", font_size=16, color=GREEN)
        vec_box = SurroundingRectangle(vec_text, color=GREEN, buff=0.12)
        vec_group = VGroup(vec_box, vec_text)
        vec_label = Text("Embedding", font_size=14, color=GREEN)

        result_vec = _make_text_matrix([["0.71"], ["-0.33"], ["0.58"]], color=GREEN)
        result_sub = Text("Vector", font_size=13, color=GREEN)

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

        # Show the output embedding box
        self.play(FadeIn(vec_label), FadeIn(vec_group))
        self.wait(0.3)

        # Animate dot from sentence through embed model into embedding
        arrow_style = dict(buff=0.05, stroke_width=4, tip_length=0.18)
        arrow_doc_to_embed = Arrow(doc.get_right(), embed_model.get_left(), color=WHITE, **arrow_style)
        arrow_embed_to_vec = Arrow(embed_model.get_right(), vec_group.get_left(), color=WHITE, **arrow_style)
        self.play(GrowArrow(arrow_doc_to_embed), GrowArrow(arrow_embed_to_vec))

        dot = Dot(color=YELLOW, radius=0.07).move_to(doc.get_right())
        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, arrow_doc_to_embed), run_time=FLOW_RUNTIME)
        self.play(MoveAlongPath(dot, arrow_embed_to_vec), run_time=FLOW_RUNTIME)
        self.play(Indicate(vec_group, color=GREEN), FadeOut(dot))
        self.wait(0.3)

        # Update caption
        caption2 = Text(
            "Similar meanings → nearby vectors",
            font_size=22,
            color=WHITE,
            slant=ITALIC,
        )
        caption2.to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, caption2))
        self.wait(0.8)

        # Arrow into Vector DB + storage animation
        arrow_vec_to_db = Arrow(vec_group.get_right(), db.get_left(), color=PURPLE, **arrow_style)
        self.play(GrowArrow(arrow_vec_to_db), Create(db))

        store_dot = Dot(color=GREEN, radius=0.07).move_to(vec_group.get_right())
        self.play(FadeIn(store_dot))
        self.play(MoveAlongPath(store_dot, arrow_vec_to_db), run_time=FLOW_RUNTIME)
        self.play(Indicate(db, color=PURPLE_A), FadeOut(store_dot))
        self.wait(0.3)

        # Show stored vectors
        self.play(FadeIn(stored_vecs, shift=DOWN * 0.15))

        # Final caption
        caption3 = Text(
            "Vectors are stored for fast similarity search",
            font_size=22,
            color=WHITE,
            slant=ITALIC,
        )
        caption3.to_edge(DOWN, buff=0.4)
        self.play(Transform(caption, caption3))
        self.wait(1.5)
