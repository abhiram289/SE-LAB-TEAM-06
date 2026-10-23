
"""
GameEngine: owns all balloons, spawns new ones, and handles clicks.

Starter version: one balloon type (random size, fixed points), no
lives system yet, no timer yet. Click detection also has a known bug
(see game/click_detection.py) that Task 1 asks you to fix.
"""

import random
import pygame

from game.balloon import Balloon, BALLOON_TYPES
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 45
POINTS_PER_POP = 10
ROUND_DURATION = 30


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.time_left = ROUND_DURATION
        self.start_ticks = None

    def reset_round(self):
        self.balloons = []
        self.frames_until_spawn = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.time_left = ROUND_DURATION
        self.start_ticks = None

    def _spawn_balloon(self):
        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)

        balloon_type = random.choice(list(BALLOON_TYPES.keys()))

        self.balloons.append(
            Balloon(
                x=x,
                y=-radius,
                radius=radius,
                speed=speed,
                balloon_type=balloon_type,
            )
        )

    def handle_click(self, pos):
        if self.game_over:
            return

        popped = check_pop(self.balloons, pos)
        if popped is not None:
            self.balloons.remove(popped)
            self.score += popped.points

    def update(self):
        if self.game_over:
            return

        if self.start_ticks is None:
            self.start_ticks = pygame.time.get_ticks()

        elapsed_seconds = (
            pygame.time.get_ticks() - self.start_ticks
        ) // 1000

        self.time_left = max(0, ROUND_DURATION - elapsed_seconds)

        if self.time_left <= 0:
            self.game_over = True
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_balloon()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        remaining_balloons = []

        for b in self.balloons:
            b.update()

            if b.is_past_bottom(HEIGHT):
                self.lives -= 1

                if self.lives <= 0:
                    self.lives = 0
                    self.game_over = True
                    break
            else:
                remaining_balloons.append(b)

        self.balloons = remaining_balloons

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(
            surface, font, f"Score: {self.score}", (10, 10)
        )
        renderer.draw_text(
            surface, font, f"Lives: {self.lives}", (10, 38)
        )
        renderer.draw_text(
            surface, font, f"Time: {self.time_left}", (10, 66)
        )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"GAME OVER - Final Score: {self.score}",
            )
