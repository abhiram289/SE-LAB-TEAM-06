import random
import pygame
from game.block import Block
from game.debris import Debris


class GameEngine:
    # Task 2 tuning
    PERFECT_TOLERANCE = 6      # px offset still counted as a perfect drop
    PERFECT_BONUS = 5          # bonus points, multiplied by the current streak
    RESTORE_AMOUNT = 8         # px of width given back per perfect (streak >= 2)
    POPUP_FRAMES = 60

    # Task 4: sky colours as (height, top colour, bottom colour) keyframes
    SKY_KEYFRAMES = [
        (0,  (60, 130, 205),  (150, 210, 245)),   # clear day
        (8,  (70, 95, 180),   (250, 170, 110)),   # sunset
        (16, (45, 35, 110),   (190, 90, 130)),    # dusk
        (26, (12, 14, 50),    (60, 50, 120)),     # night
        (38, (3, 3, 14),      (18, 18, 50)),      # space
    ]

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.block_height = 28
        self.base_width = 180

        self.font_title = pygame.font.SysFont(None, 38)
        self.font_hud = pygame.font.SysFont(None, 28)
        self.font_big = pygame.font.SysFont(None, 46)

        self.reset()

    def get_color(self, index):
        palette = [
            (230, 75, 75),   # Crimson
            (240, 140, 45),  # Orange
            (245, 210, 50),  # Gold
            (60, 195, 110),  # Green
            (50, 150, 240),  # Blue
            (165, 80, 225),  # Purple
        ]
        return palette[index % len(palette)]

    def reset(self):
        self.score = 0          # tower height (blocks stacked)
        self.bonus = 0          # bonus points from perfect drops
        self.perfect_streak = 0
        self.popups = []        # [text, x, y, frames_left]
        self.debris = []        # falling off-cut pieces
        self.sky_height = 0.0   # eased height used for the background
        self.stars = [(random.randint(0, self.width), random.randint(0, self.height), random.randint(1, 2))
                      for _ in range(70)]
        self.game_over = False

        base_x = (self.width - self.base_width) // 2
        base_y = self.height - 60
        base_block = Block(base_x, base_y, self.base_width, self.block_height, self.get_color(0), speed=0)
        self.stack = [base_block]

        self.spawn_active_block()

    def spawn_active_block(self):
        top_block = self.stack[-1]
        next_y = top_block.y - self.block_height - 4
        speed = min(10.0, 4.5 + (len(self.stack) * 0.35))
        color = self.get_color(len(self.stack))

        start_x = 25 if random.choice([True, False]) else self.width - 25 - top_block.width
        self.active_block = Block(start_x, next_y, top_block.width, self.block_height, color, speed=speed)

    def drop_block(self):
        if self.game_over:
            return

        top_block = self.stack[-1]
        act = self.active_block

        left = max(act.x, top_block.x)
        right = min(act.x + act.width, top_block.x + top_block.width)
        overlap = right - left

        is_successful_drop = overlap > 0

        if is_successful_drop:
            is_perfect = abs(act.x - top_block.x) <= self.PERFECT_TOLERANCE

            if is_perfect:
                # Snap flush with the tower: no trimming at all.
                self.perfect_streak += 1
                new_x, new_width = top_block.x, top_block.width

                # Two or more perfects in a row give some lost width back.
                if self.perfect_streak >= 2:
                    restore = min(self.RESTORE_AMOUNT, self.base_width - new_width)
                    new_width += restore
                    new_x -= restore / 2
                    new_x = max(20, min(new_x, self.width - 20 - new_width))

                points = self.PERFECT_BONUS * self.perfect_streak
                self.bonus += points
                label = "PERFECT!" if self.perfect_streak == 1 else f"PERFECT! x{self.perfect_streak}"
                self.popups.append([f"{label}  +{points}", self.width // 2, act.y - 10, self.POPUP_FRAMES])
            else:
                self.perfect_streak = 0
                new_x, new_width = left, max(10.0, overlap)
                self.spawn_debris(act, left, right)

            new_block = Block(new_x, act.y, new_width, self.block_height, act.color, speed=0)
            self.stack.append(new_block)
            self.score += 1

            if new_block.y < 180:
                shift_amount = self.block_height + 4
                for b in self.stack:
                    b.y += shift_amount
                for p in self.popups:
                    p[2] += shift_amount
                for d in self.debris:
                    d.shift(shift_amount)

            self.spawn_active_block()
        else:
            # Complete miss: the whole block tumbles away.
            direction = 1 if (act.x + act.width / 2) > (top_block.x + top_block.width / 2) else -1
            self.debris.append(Debris(act.x, act.y, act.width, act.height, act.color,
                                      vx=1.5 * direction, spin=-4.0 * direction))
            self.game_over = True

    def spawn_debris(self, act, left, right):
        """Turn each trimmed overhang of the active block into a falling piece."""
        if left - act.x > 0.5:                       # overhang on the left
            self.debris.append(Debris(act.x, act.y, left - act.x, act.height, act.color,
                                      vx=-1.6, spin=5.0))
        right_edge = act.x + act.width
        if right_edge - right > 0.5:                 # overhang on the right
            self.debris.append(Debris(right, act.y, right_edge - right, act.height, act.color,
                                      vx=1.6, spin=-5.0))

    def handle_event(self, event):
        if self.game_over:
            if (event.type == pygame.KEYDOWN and event.key in (pygame.K_r, pygame.K_SPACE)) or \
               (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1):
                self.reset()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.drop_block()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.drop_block()

    def sky_colors(self, h):
        frames = self.SKY_KEYFRAMES
        if h >= frames[-1][0]:
            return frames[-1][1], frames[-1][2]
        for (h0, t0, b0), (h1, t1, b1) in zip(frames, frames[1:]):
            if h0 <= h <= h1:
                k = (h - h0) / (h1 - h0)
                lerp = lambda a, b: tuple(int(a[i] + (b[i] - a[i]) * k) for i in range(3))
                return lerp(t0, t1), lerp(b0, b1)
        return frames[0][1], frames[0][2]

    def draw_sky(self, screen):
        top, bottom = self.sky_colors(self.sky_height)
        for y in range(self.height):
            k = y / (self.height - 1)
            color = tuple(int(top[i] + (bottom[i] - top[i]) * k) for i in range(3))
            pygame.draw.line(screen, color, (0, y), (self.width, y))

        # Stars fade in once the tower reaches the night sky.
        star_alpha = max(0.0, min(1.0, (self.sky_height - 16) / 10))
        if star_alpha > 0:
            level = int(255 * star_alpha)
            for x, y, r in self.stars:
                pygame.draw.circle(screen, (level, level, level), (x, y), r)

    def update(self):
        # Ease the background toward the current tower height so it shifts smoothly.
        self.sky_height += (self.score - self.sky_height) * 0.04

        if not self.game_over:
            self.active_block.update(self.width)

        for d in self.debris:
            d.update()
        self.debris = [d for d in self.debris if not d.is_gone(self.height)]

        for p in self.popups:
            p[2] -= 0.8
            p[3] -= 1
        self.popups = [p for p in self.popups if p[3] > 0]

    def render(self, screen):
        self.draw_sky(screen)

        title_surf = self.font_title.render("Skyscraper Stack", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 16))

        score_surf = self.font_hud.render(f"Height: {self.score}   Bonus: {self.bonus}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 54))

        for b in self.stack:
            b.render(screen)

        for d in self.debris:
            d.render(screen)

        if not self.game_over:
            self.active_block.render(screen)

        for text, x, y, frames in self.popups:
            surf = self.font_big.render(text, True, (255, 240, 120))
            surf.set_alpha(min(255, frames * 8))
            screen.blit(surf, (x - surf.get_width() // 2, y))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 195))
            screen.blit(overlay, (0, 0))

            over_surf = self.font_big.render("TOWER COLLAPSED!", True, (240, 75, 75))
            screen.blit(over_surf, (self.width // 2 - over_surf.get_width() // 2, self.height // 2 - 40))

            final_surf = self.font_hud.render(f"Final Height: {self.score}   Bonus: {self.bonus}", True, (255, 255, 255))
            screen.blit(final_surf, (self.width // 2 - final_surf.get_width() // 2, self.height // 2 + 10))

            restart_surf = self.font_hud.render("Press [Space] or [R] to Play Again", True, (200, 200, 200))
            screen.blit(restart_surf, (self.width // 2 - restart_surf.get_width() // 2, self.height // 2 + 50))
