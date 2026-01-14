from manim import *

from common.helpers import *

config.frame_rate = 30
FLOW_RUNTIME = 1.6
STEP_RUNTIME = 0.35

class MCPDiagram(Scene):
    def construct(self):
        self.next_section(name="Intro", skip_animations=False)

        mcp = RectangleWithText("MCP", color="blue", font_size=40)
        self.play(Create(mcp))
        self.wait(0.4)

        mcp_text = VGroup(
            Text("Model"),
            Text("Context"),
            Text("Protocol"),
        ).arrange(RIGHT, buff=0.25).scale(0.9).move_to(mcp)
        self.play(
            Transform(mcp[1], mcp_text),
            Transform(mcp[0], SurroundingRectangle(mcp_text, color="blue"))
        )
        self.wait(0.4)

        self.play(FadeOut(mcp))

        self.next_section(name="Actors", skip_animations=False)

        user = RectangleWithText("User / App", color="yellow", font_size=30)
        llm = RectangleWithText("LLM", color="blue", font_size=34)
        mcp_client = RectangleWithText("MCP Client", color="blue", font_size=34)
        mcp_server = RectangleWithText("MCP Server", color="blue", font_size=34)
        tools = RectangleWithText("Tools / Resources", color="green", font_size=30)

        tools_examples = VGroup(
            Text("Robot", font_size=22),
            Text("Databases", font_size=22),
            Text("APIs", font_size=22),
            Text("Files", font_size=22),
            Text("Sensors", font_size=22),
        ).arrange(DOWN, buff=0.1).set_color("green")

        group_top = VGroup(llm, mcp_client, mcp_server).arrange(DOWN, buff=0.6)
        user.next_to(mcp_client, LEFT, buff=0.6)
        tools.next_to(mcp_server, DOWN, buff=0.6)
        tools_examples.next_to(tools, DOWN, buff=0.25)
        scene_group = VGroup(group_top, user, tools, tools_examples).move_to(ORIGIN).shift(LEFT * 1.5)

        self.play(Create(group_top), Create(user), Create(tools), FadeIn(tools_examples))
        self.wait(0.3)

        arrow_buff = 0.0
        arrow_style = dict(buff=arrow_buff, stroke_width=6, tip_length=0.3)
        user_to_client = Arrow(user.get_right(), mcp_client.get_left(), color="yellow", **arrow_style)
        client_to_user = Arrow(mcp_client.get_left(), user.get_right(), color="yellow", **arrow_style)
        llm_to_client = Arrow(llm.get_bottom(), mcp_client.get_top(), color="blue", **arrow_style)
        client_to_server = Arrow(mcp_client.get_bottom(), mcp_server.get_top(), color="blue", **arrow_style)
        server_to_tools = Arrow(mcp_server.get_bottom(), tools.get_top(), color="green", **arrow_style)
        tools_to_server = Arrow(tools.get_top(), mcp_server.get_bottom(), color="green", **arrow_style)

        self.play(GrowArrow(user_to_client), GrowArrow(client_to_user))
        self.play(GrowArrow(llm_to_client), GrowArrow(client_to_server))
        self.play(GrowArrow(server_to_tools), GrowArrow(tools_to_server))
        self.wait(0.4)

        self.next_section(name="Schema", skip_animations=False)

        schema = RectangleWithText("Server declares\nCapabilities", color="orange", font_size=28)
        schema.next_to(mcp_server, RIGHT, buff=0.7)
        schema_line = Line(schema.get_left(), mcp_server.get_right(), color="orange")
        self.play(Create(schema), Create(schema_line))
        self.wait(0.5)

        self.next_section(name="Flow", skip_animations=False)

        request_text = Text('"Move the robot"', font_size=22, color="yellow").next_to(user, UP, buff=0.2)
        self.play(FadeIn(request_text))

        step_anchor = (DOWN * (config.frame_height / 2) + RIGHT * (config.frame_width / 2)) + UP * 0.9 + LEFT * 3.0
        step_label = Text("User request", font_size=28).move_to(step_anchor)
        self.play(Write(step_label), run_time=STEP_RUNTIME)

        path_client_to_llm = llm_to_client.copy().reverse_direction()
        path_server_to_client = client_to_server.copy().reverse_direction()
        path_tools_to_server = tools_to_server

        dot = Dot(color=WHITE, radius=0.08).move_to(user_to_client.get_start())
        self.play(FadeIn(dot))
        self.play(MoveAlongPath(dot, user_to_client), run_time=FLOW_RUNTIME, rate_func=smooth)

        self.play(
            Transform(step_label, Text("LLM interprets intent", font_size=28).move_to(step_anchor)),
            run_time=STEP_RUNTIME,
        )
        self.play(
            MoveAlongPath(dot, path_client_to_llm),
            run_time=FLOW_RUNTIME,
            rate_func=smooth,
        )
        self.play(MoveAlongPath(dot, llm_to_client), run_time=FLOW_RUNTIME, rate_func=smooth)

        self.play(
            Transform(step_label, Text("Client calls robot tool", font_size=28).move_to(step_anchor)),
            run_time=STEP_RUNTIME,
        )
        self.play(
            MoveAlongPath(dot, client_to_server),
            run_time=FLOW_RUNTIME,
            rate_func=smooth,
        )

        robot_highlight = SurroundingRectangle(tools_examples[0], color="yellow", buff=0.05)
        self.play(
            Transform(step_label, Text("Server invokes robot", font_size=28).move_to(step_anchor)),
            Create(robot_highlight),
            run_time=STEP_RUNTIME,
        )
        self.play(
            MoveAlongPath(dot, server_to_tools),
            run_time=FLOW_RUNTIME,
            rate_func=smooth,
        )
        self.play(MoveAlongPath(dot, path_tools_to_server), run_time=FLOW_RUNTIME * 0.8, rate_func=smooth)

        
        self.play(
            MoveAlongPath(dot, path_server_to_client),
            run_time=FLOW_RUNTIME * 0.8,
            rate_func=smooth,
        )
        self.play(
            Transform(step_label, Text("LLM processes result", font_size=28).move_to(step_anchor)),
            run_time=STEP_RUNTIME,
        )
        self.play(MoveAlongPath(dot, path_client_to_llm), run_time=FLOW_RUNTIME * 0.8, rate_func=smooth)
        
        self.play(MoveAlongPath(dot, llm_to_client), run_time=FLOW_RUNTIME * 0.8, rate_func=smooth)
        self.play(
            Transform(step_label, Text("Result returns to user", font_size=28).move_to(step_anchor)),
            run_time=STEP_RUNTIME,
        )
        self.play(
            MoveAlongPath(dot, client_to_user),
            run_time=FLOW_RUNTIME * 0.8,
            rate_func=smooth,
        )

        
        self.wait(0.2)

        self.play(FadeOut(dot), FadeOut(step_label), FadeOut(robot_highlight), FadeOut(request_text))
        self.wait(0.2)
