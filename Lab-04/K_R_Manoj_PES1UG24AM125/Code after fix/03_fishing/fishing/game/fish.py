"""
Fish: swims horizontally at a fixed depth, wrapping around when it exits the screen.

Task 2:
Introduces multiple fish types with distinct movement speeds, point values,
colors, and dimensions.
- SlowFish: slow-moving, calm blue color, awards 10 points.
- FastFish: fast-darting, vibrant coral-orange color, awards 30 points.
- GoldenFish: rare high-speed golden fish, awards 50 points.
"""

import math
import pygame


class Fish:
    def __init__(
        self,
        x,
        y,
        speed,
        width=36,
        height=18,
        point_value=10,
        color=(70, 180, 225),
    ):
        self.x = float(x)
        self.y = float(y)
        self.speed = float(speed)
        self.width = width
        self.height = height
        self.point_value = point_value
        self.color = color

    def update(self, screen_width):
        """Move horizontally and smoothly wrap around screen edges."""
        self.x += self.speed

        # Smooth wrap: only wrap once the entire fish has left the screen
        if self.speed > 0 and self.x - self.width / 2 > screen_width:
            self.x = -self.width / 2
        elif self.speed < 0 and self.x + self.width / 2 < 0:
            self.x = screen_width + self.width / 2

    def get_rect(self):
        """Returns the axis-aligned bounding box centered at (self.x, self.y)."""
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            int(self.width),
            int(self.height),
        )

    def draw(self, surface):
        """Renders an attractive fish with directional tail fin and eye."""
        rect = self.get_rect()
        cx, cy = int(self.x), int(self.y)
        w, h = int(self.width), int(self.height)

        # 1. Tail fin based on movement direction
        tail_length = int(w * 0.3)
        tail_spread = int(h * 0.7)
        if self.speed >= 0:
            # Moving right -> tail on left
            tail_points = [
                (cx - w // 2 + 2, cy),
                (cx - w // 2 - tail_length, cy - tail_spread),
                (cx - w // 2 - tail_length, cy + tail_spread),
            ]
        else:
            # Moving left -> tail on right
            tail_points = [
                (cx + w // 2 - 2, cy),
                (cx + w // 2 + tail_length, cy - tail_spread),
                (cx + w // 2 + tail_length, cy + tail_spread),
            ]
        pygame.draw.polygon(surface, self.color, tail_points)

        # 2. Body ellipse
        pygame.draw.ellipse(surface, self.color, rect)

        # 3. Eye with pupil
        eye_radius = max(2, int(h * 0.16))
        pupil_radius = max(1, eye_radius // 2)
        if self.speed >= 0:
            eye_x = cx + int(w * 0.25)
        else:
            eye_x = cx - int(w * 0.25)
        eye_y = cy - int(h * 0.15)

        pygame.draw.circle(surface, (255, 255, 255), (eye_x, eye_y), eye_radius)
        pupil_dx = 1 if self.speed >= 0 else -1
        pygame.draw.circle(
            surface, (20, 20, 30), (eye_x + pupil_dx, eye_y), pupil_radius
        )


class SlowFish(Fish):
    """A steady, low-value fish that is easy to catch."""

    def __init__(self, x, y, speed=1.5, **kwargs):
        kwargs.setdefault("width", 36)
        kwargs.setdefault("height", 18)
        kwargs.setdefault("point_value", 10)
        kwargs.setdefault("color", (70, 180, 225))
        super().__init__(x, y, speed, **kwargs)


class FastFish(Fish):
    """A rapid, high-value fish that requires good timing."""

    def __init__(self, x, y, speed=4.0, **kwargs):
        kwargs.setdefault("width", 48)
        kwargs.setdefault("height", 22)
        kwargs.setdefault("point_value", 30)
        kwargs.setdefault("color", (255, 105, 75))
        super().__init__(x, y, speed, **kwargs)


class GoldenFish(Fish):
    """A rare, swift golden fish with high point value."""

    def __init__(self, x, y, speed=5.5, **kwargs):
        kwargs.setdefault("width", 30)
        kwargs.setdefault("height", 15)
        kwargs.setdefault("point_value", 50)
        kwargs.setdefault("color", (255, 215, 0))
        super().__init__(x, y, speed, **kwargs)