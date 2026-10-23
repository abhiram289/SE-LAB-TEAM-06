"""
Hook: the player's fishing hook.

Moves only vertically at a fixed horizontal position.
Task 3 changes hook behavior so the player controls when the hook casts,
preventing any new cast from interrupting an in-progress cast.
"""

import pygame

IDLE = "idle"
CASTING = "casting"
RETRACTING = "retracting"


class Hook:
    def __init__(self, x, surface_y, max_depth_y, speed=4, width=14, height=14):
        self.x = float(x)
        self.surface_y = float(surface_y)
        self.max_depth_y = float(max_depth_y)
        self.y = float(surface_y)
        self.speed = speed
        self.width = width
        self.height = height
        self.state = IDLE

    def start_cast(self):
        """
        Initiates a cast downward if and only if the hook is currently IDLE.
        Does not interrupt a cast that is already active or retracting.
        """
        if self.state != IDLE:
            return

        self.state = CASTING
        self.y = self.surface_y

    def update(self):
        """Updates the hook position and state machine."""
        if self.state == CASTING:
            self.y += self.speed
            if self.y >= self.max_depth_y:
                self.y = self.max_depth_y
                self.state = RETRACTING
        elif self.state == RETRACTING:
            self.y -= self.speed
            if self.y <= self.surface_y:
                self.y = self.surface_y
                self.state = IDLE

    def catch_fish(self):
        """Called when a fish has been snagged; immediately heads back to surface."""
        self.state = RETRACTING

    def reset(self):
        """Resets hook to the surface boat position in IDLE state."""
        self.state = IDLE
        self.y = self.surface_y

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )
