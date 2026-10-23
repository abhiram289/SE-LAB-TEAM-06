"""
GameEngine: owns the hook, fish, score, and round timer.
Runs one frame's worth of game logic and handles events and drawing.
"""

import math
import pygame

from game.hook import Hook, IDLE, CASTING, RETRACTING
from game.fish import Fish, SlowFish, FastFish, GoldenFish
from game.catch import check_catch
from game.renderer import (
    WIDTH,
    HEIGHT,
    SURFACE_Y,
    MAX_DEPTH_Y,
    draw_scene,
    draw_text,
    draw_hud,
    draw_game_over_modal,
)


class GameEngine:
    ROUND_DURATION = 30

    def __init__(self):
        self.hook = Hook(
            x=WIDTH / 2,
            surface_y=SURFACE_Y,
            max_depth_y=MAX_DEPTH_Y,
            speed=5,
        )
        self.score = 0
        self.high_score = 0
        self.remaining_time = float(self.ROUND_DURATION)
        self.round_over = False
        self.start_time = pygame.time.get_ticks()
        self.hooked_fish = None
        self.floating_popups = []  # List of floating score indicators
        self.reset_fish()

    def reset_fish(self):
        """Initializes a rich school of fish with varied depths, speeds, and types."""
        self.fish_list = [
            SlowFish(x=90, y=165, speed=1.5),
            FastFish(x=540, y=225, speed=-3.5),
            SlowFish(x=230, y=285, speed=2.0),
            FastFish(x=430, y=345, speed=-4.0),
            SlowFish(x=150, y=405, speed=1.6),
            GoldenFish(x=620, y=445, speed=-5.2),
        ]

    def handle_event(self, event):
        """Processes keyboard input for casting and round reset."""
        if event.type == pygame.KEYDOWN:
            if not self.round_over:
                # Task 3: Player-controlled casting via Space or Down Arrow
                if event.key in (pygame.K_SPACE, pygame.K_DOWN, pygame.K_s):
                    if self.hook.state == IDLE:
                        self.hook.start_cast()
            else:
                # Task 4: Restart round via R, Space, or Enter
                if event.key in (pygame.K_r, pygame.K_SPACE, pygame.K_RETURN):
                    self.new_round()

    def new_round(self):
        """Resets round state, timer, score, hook, and fish."""
        self.high_score = max(self.high_score, self.score)
        self.score = 0
        self.remaining_time = float(self.ROUND_DURATION)
        self.start_time = pygame.time.get_ticks()
        self.round_over = False
        self.hooked_fish = None
        self.floating_popups.clear()
        self.hook.reset()
        self.reset_fish()

    def add_score_popup(self, text, x, y, color=(255, 230, 80)):
        """Spawns an animated floating score text on catch."""
        self.floating_popups.append({
            "text": text,
            "x": float(x),
            "y": float(y),
            "life": 45,  # Frames alive
            "color": color,
        })

    def update(self):
        """Updates game state each frame."""
        # Task 4: Round timer countdown
        if self.round_over:
            return

        elapsed = (pygame.time.get_ticks() - self.start_time) / 1000.0
        self.remaining_time = max(0.0, self.ROUND_DURATION - elapsed)

        if self.remaining_time <= 0.0:
            self.round_over = True
            self.remaining_time = 0.0
            self.hooked_fish = None
            self.hook.reset()
            self.high_score = max(self.high_score, self.score)
            return

        # Update hook
        self.hook.update()

        # Update swimming fish
        for fish in self.fish_list:
            fish.update(WIDTH)

        # Handle hooked fish and surface scoring
        if self.hooked_fish is not None:
            self.hooked_fish.x = self.hook.x
            self.hooked_fish.y = self.hook.y

            # Scored only when hook completely returns to surface (IDLE state)
            if self.hook.state == IDLE:
                pts = self.hooked_fish.point_value
                self.score += pts
                self.high_score = max(self.high_score, self.score)
                self.add_score_popup(f"+{pts}", self.hook.x + 12, self.hook.surface_y - 12)
                self.hooked_fish = None

                # If all fish caught, repopulate so player can keep playing
                if len(self.fish_list) == 0:
                    self.reset_fish()
        elif self.hook.state != IDLE:
            # Task 1: Check catch only when hook is actively in the water
            caught = check_catch(self.hook, self.fish_list)

            if caught is not None:
                self.fish_list.remove(caught)
                self.hooked_fish = caught
                self.hooked_fish.x = self.hook.x
                self.hooked_fish.y = self.hook.y
                self.hook.catch_fish()

        # Update floating score popups
        for popup in self.floating_popups:
            popup["y"] -= 0.8
            popup["life"] -= 1
        self.floating_popups = [p for p in self.floating_popups if p["life"] > 0]

    def draw(self, surface, font):
        """Renders the scene, HUD, floating popups, and game-over modal."""
        # 1. Main scene (water, boat, hook, fish)
        draw_list = list(self.fish_list)
        if self.hooked_fish is not None:
            draw_list.append(self.hooked_fish)

        draw_scene(surface, self.hook, draw_list)

        # 2. Floating score popups
        for popup in self.floating_popups:
            alpha_ratio = min(1.0, popup["life"] / 20.0)
            c = popup["color"]
            draw_text(surface, font, popup["text"], (int(popup["x"]), int(popup["y"])), color=c)

        # 3. HUD badges (Score, Time, Cast Prompt)
        font_large = pygame.font.SysFont("consolas", 28, bold=True)
        draw_hud(
            surface,
            font,
            font_large,
            self.score,
            self.remaining_time,
            self.hook.state,
            self.high_score,
        )

        # 4. Task 4: Game Over overlay when round concludes
        if self.round_over:
            draw_game_over_modal(
                surface,
                font_large,
                font,
                self.score,
                self.high_score,
            )