from manim import *
from common.helpers import *

# PROTO_DEF = "A"
PROTO_DEF = """
syntax = "proto3";

import "google/protobuf/empty.proto";

enum MoveDirection {
  MOVE_FORWARD = 0;
  MOVE_BACKWARD = 1;
  MOVE_LEFT = 2;
  MOVE_RIGHT = 3;
}

message MoveRequest {
  MoveDirection direction = 1;
  float duration = 2;
}

// Define the service for streaming keyboard input
service RobotControl {
  // Unary RPC: The client sends a MoveRequest. Asyhcronously moves the robot.
  rpc Move(MoveRequest) returns (google.protobuf.Empty);
}
"""


class gRPC(MovingCameraScene):
    def construct(self):

        self.next_section(name="Intro", skip_animations=False) 
        # Save original camera position
        self.camera.frame.save_state()

        grpc = RectangleWithText("gRPC", color="blue", font_size=36)
        self.play(Create(grpc))
        self.wait(1.0)

        grpc.save_state()

        grpc_text = VGroup(
            Text("google"),
            Text("Remote"),
            Text("Procedure"),
            Text("Call"),
        ).arrange(RIGHT, buff=0.2).scale(1).move_to(grpc)
        self.play(Transform(grpc[1], grpc_text), Transform(grpc[0], SurroundingRectangle(grpc_text, color="blue"))) # letter by letter
        self.wait()
        self.play(Restore(grpc))

        self.next_section(name="Contract", skip_animations=False) 
        contract = RectangleWithText("Contract\n(.proto)", color="green").move_to(grpc)
        self.play(Transform(grpc, contract))
        self.wait(1.0)

        proto_rect = Rectangle(width=3.4, height=2, color="orange", stroke_width=1)
        proto_msg = Text(PROTO_DEF).move_to(proto_rect.get_center())
        proto_msg.scale_to_fit_width(proto_rect.width)
        proto_msg.scale_to_fit_height(proto_rect.height)

        proto = VGroup(proto_rect, proto_msg)
        self.play(Transform(grpc, proto))
   
        # Zoom in
        self.play(self.camera.frame.animate.move_to(proto).set_width(proto.width * 1.4))
        self.wait(3.0)

        # Zoom out
        self.play(Restore(self.camera.frame))
        self.play(Transform(grpc, contract))
        self.play(grpc.animate.to_edge(UP))

        self.next_section(name="Client-Server", skip_animations=False)

        client = RectangleWithText("Client\nService", color="green").to_edge(LEFT, buff=2).shift(UP)
        server = RectangleWithText("Server\nService", color="green").to_edge(RIGHT, buff=2).shift(UP)

        self.play(Create(client), Create(server))

        arrow_l = Arrow( grpc.get_left(),client, buff=0.1, color="blue")
        label_client = Text("Generates Stubs", font_size=24).next_to(arrow_l.get_top(), LEFT , buff=0.1)

        arrow_r = Arrow(grpc.get_right(), server, buff=0.1, color="blue")
        label_server = Text("Generates Stubs", font_size=24).next_to(arrow_r.get_top(), RIGHT, buff=0.1)

        self.play(GrowArrow(arrow_l), GrowArrow(arrow_r))
        self.play(Write(label_client), Write(label_server))
        
        self.wait(1.0)

        self.next_section(name="User Code", skip_animations=False)

        user_server_code = RectangleWithText("User Service\nImplementation", color="purple").move_to(server.get_bottom() + DOWN * 1.5)
        server_arrow_up = Arrow(user_server_code.get_top(), server.get_bottom(), buff=0.1, color="blue")
        
        user_client_code = RectangleWithText("User Service\nImplementation", color="purple").move_to(client.get_bottom() + DOWN * 1.5)
        client_arrow_up = Arrow(user_client_code.get_top(), client.get_bottom(), buff=0.1, color="blue")


        self.play(Create(user_server_code), Create(server_arrow_up), Create(user_client_code), Create(client_arrow_up))
        self.wait(2.0)
        User = SurroundingRectangle(VGroup(user_server_code, user_client_code), color="yellow", buff=0.3)

        self.play(Create(User))

        d_a = DoubleArrow(user_client_code.get_right(), user_server_code.get_left(), buff=0.0, color="red")

        self.play(GrowArrow(d_a))

        communication_label = Text("Proto-defined messages", font_size=24).next_to(d_a, UP, buff=0.2)
        line = Line(communication_label.get_top(), grpc.get_bottom(), buff=0.1, color="orange")
        self.play(Write(communication_label), Create(line))
        self.wait(3.0)

        # Animate unary call
        message_dot = Dot(color=BLUE, radius=0.1).move_to(user_client_code.get_right())
        request_type = Text("Unary Call (Request-Reply)", font_size=24).next_to(User, DOWN, buff=0.2)

        self.play(FadeIn(message_dot), FadeIn(request_type))
        self.play(FadeIn(request_type))
        self.play(message_dot.animate.move_to(user_server_code.get_left()), run_time=1, rate_func=linear)
        self.play(message_dot.animate.move_to(user_client_code.get_right()), run_time=1, rate_func=linear)
        self.play(FadeOut(message_dot), FadeOut(request_type))
        self.wait(2.0)

        # Server Stream
        request_type = Text("Server Streaming", font_size=24).next_to(User, DOWN, buff=0.2)
        self.play(FadeIn(request_type))

        stream_path = Line(user_server_code.get_left(), user_client_code.get_right())
        stream_dots = VGroup(*[Dot(color="green", radius=0.08) for _ in range(10)])
        stream_anims = [MoveAlongPath(dot, stream_path, run_time=1.2, rate_func=linear) for dot in stream_dots]
        self.play(AnimationGroup(*stream_anims, lag_ratio=0.12))
        self.play(FadeOut(stream_dots), FadeOut(request_type))

        # Client Stream
        request_type = Text("Client Streaming", font_size=24).next_to(User, DOWN, buff=0.2)
        self.play(FadeIn(request_type))

        stream_path = Line(user_client_code.get_right(), user_server_code.get_left())
        stream_dots = VGroup(*[Dot(color="green", radius=0.08) for _ in range(10)])
        stream_anims = [MoveAlongPath(dot, stream_path, run_time=1.2, rate_func=smooth) for dot in stream_dots]
        self.play(AnimationGroup(*stream_anims, lag_ratio=0.12))
        self.play(FadeOut(stream_dots), FadeOut(request_type))

        # BiDi Stream
        request_type = Text("Bi-Directional Streaming", font_size=24).next_to(User, DOWN, buff=0.2)
        self.play(FadeIn(request_type)) 
        stream_path_client = Line(user_client_code.get_right(), user_server_code.get_left())
        stream_path_server = Line(user_server_code.get_left(), user_client_code.get_right())
        stream_dots_client = VGroup(*[Dot(color="green", radius=0.08) for _ in range(10)])
        stream_dots_server = VGroup(*[Dot(color="blue", radius=0.08) for _ in range(10)])
        stream_anims_client = [MoveAlongPath(dot, stream_path_client, run_time=1.2, rate_func=smooth) for dot in stream_dots_client]
        stream_anims_server = [MoveAlongPath(dot, stream_path_server, run_time=1.2, rate_func=linear) for dot in stream_dots_server]
        self.play(AnimationGroup(
            AnimationGroup(*stream_anims_client, lag_ratio=0.12),
            AnimationGroup(*stream_anims_server, lag_ratio=0.12),
        ))
        self.play(FadeOut(stream_dots_client), FadeOut(stream_dots_server), FadeOut(request_type))
        self.wait(2.0)
        

        