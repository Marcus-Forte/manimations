from manim import *
import numpy as np

config.frame_rate = 30

class EventBusDiagram(Scene):
    def construct(self):
        bus_line = Line(LEFT * 4, RIGHT * 4, stroke_width=12, color=BLUE)
        bus_label = Text("Event Bus", weight=BOLD, font_size=32).next_to(
            bus_line, RIGHT, buff=0.3
        )
        bus_group = VGroup(bus_line, bus_label)
        bus_y = bus_line.get_center()[1]

        producer_names = ["Producer A", "Producer B"]
        consumer_names = ["Consumer A", "Consumer B"]
        events = ["Event A", "Event B"]

        publishers = VGroup(
            *[self._circle_node(name, GREEN) for name in producer_names]
        )
        subscribers = VGroup(
            *[self._circle_node(name, YELLOW) for name in consumer_names]
        )

        publishers.arrange(RIGHT, buff=1.2).next_to(bus_line, UP, buff=1.4)
        subscribers.arrange(RIGHT, buff=1.2).next_to(bus_line, DOWN, buff=1.4)

        # Put Consumer A on the right so messages travel across the bus to reach it.
        subscriber_positions = [sub.get_center() for sub in subscribers]
        if len(subscribers) >= 2:
            subscribers[0].move_to(subscriber_positions[1])
            subscribers[1].move_to(subscriber_positions[0])

        inbound = VGroup()
        inbound_labels = VGroup()
        for pub, label_text in zip(publishers, events):
            start = pub.get_bottom()
            end = np.array([pub.get_center()[0], bus_y, 0])
            arrow = Arrow(start, end, buff=0.05, color=GREEN)
            label = Text(f"Pub: {label_text}", font_size=20, color=GREEN).next_to(
                arrow, RIGHT, buff=0.1
            )
            inbound.add(arrow)
            inbound_labels.add(label)
            
        outbound = VGroup()
        outbound_labels = VGroup()
        for sub, label_text in zip(subscribers, events):
            start = sub.get_top()
            end = np.array([sub.get_center()[0], bus_y, 0])
            arrow = Arrow(start, end, buff=0.05, color=YELLOW)
            label = Text(f"Sub: {label_text}", font_size=20, color=YELLOW).next_to(
                arrow, RIGHT, buff=0.1
            )
            outbound.add(arrow)
            outbound_labels.add(label)

        self.play(FadeIn(bus_group))
        self.play(
            LaggedStart(
                *[FadeIn(node, shift=UP * 0.2) for node in publishers], lag_ratio=0.15
            )
        )
        self.play(
            LaggedStart(
                *[FadeIn(node, shift=DOWN * 0.2) for node in subscribers],
                lag_ratio=0.15,
            )
        )
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in outbound], lag_ratio=0.1))
        self.play(LaggedStart(*[FadeIn(label, shift=UP * 0.05) for label in outbound_labels], lag_ratio=0.1))
        self.play(LaggedStart(*[GrowArrow(arrow) for arrow in inbound], lag_ratio=0.1))
        self.play(LaggedStart(*[FadeIn(label, shift=UP * 0.05) for label in inbound_labels], lag_ratio=0.1))

        # Animate messages traveling from each producer, through the bus, to a subscriber.
        for pub, sub, label in zip(publishers, subscribers, events):
            path = VMobject()
            path.set_points_as_corners(
                [
                    pub.get_bottom(),
                    np.array([pub.get_center()[0], bus_y, 0]),
                    np.array([sub.get_center()[0], bus_y, 0]),
                    sub.get_top(),
                ]
            )

            dot = Dot(color=YELLOW).move_to(pub.get_bottom())

            self.add(dot)
            self.play(MoveAlongPath(dot, path), run_time=1.8, rate_func=linear)

        self.play(Indicate(bus_line, color=BLUE_C, scale_factor=1.02))

    def _circle_node(self, name: str, color) -> VGroup:
        rect = RoundedRectangle(
            corner_radius=0.12, width=2.0, height=0.9, color=color, fill_opacity=0.15
        )
        label = Text(name, font_size=24).move_to(rect.get_center())
        return VGroup(rect, label)
