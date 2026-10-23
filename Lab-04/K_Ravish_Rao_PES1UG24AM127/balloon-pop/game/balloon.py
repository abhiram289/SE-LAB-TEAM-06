"""
Balloon: falls from the top of the screen. The player must pop it
before it reaches the bottom. Balloons vary in size - this matters for
how click detection should work.
"""

import pygame

BALLOON_TYPES = {
    "normal": {
        "color": (70, 130, 220),
        "points": 10,
    },
    "bonus": {
        "color": (50, 180, 90),
        "points": 30,
    },
    "penalty": {
        "color": (220, 60, 60),
        "points": -10,
    },
}



class Balloon:
    def __init__(self, x, y, radius, speed, color=None, balloon_type="normal"):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed
        self.balloon_type = balloon_type

        type_info = BALLOON_TYPES[balloon_type]
        self.color = color if color is not None else type_info["color"]
        self.points = type_info["points"]

    def update(self):
        self.y += self.speed

    def is_past_bottom(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius), int(self.y - self.radius),
            self.radius * 2, self.radius * 2,
        )
