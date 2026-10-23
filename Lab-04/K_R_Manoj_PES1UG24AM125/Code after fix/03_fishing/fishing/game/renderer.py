"""
renderer: all pygame drawing lives here, kept separate from game logic.
Provides vibrant, polished graphics including layered water gradients,
animated bubbles, stylized boat with fishing rod, distinct fish rendering,
and a modern HUD with round-end summary modal.
"""

import math
import pygame

WIDTH, HEIGHT = 700, 500
SURFACE_Y = 80
MAX_DEPTH_Y = HEIGHT - 40

WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_SKY_TOP = (110, 185, 235)
COLOR_SKY_BOTTOM = (185, 225, 248)
COLOR_WATER_SURFACE = (32, 115, 185)
COLOR_WATER_DEEP = (12, 45, 95)
COLOR_BOAT_HULL = (135, 82, 46)
COLOR_BOAT_RIM = (95, 52, 28)
COLOR_BOAT_SEAT = (165, 110, 70)
COLOR_ROD = (70, 70, 75)
COLOR_LINE = (235, 240, 245)
COLOR_HOOK = (215, 220, 230)
COLOR_TEXT = (255, 255, 255)
COLOR_GOLD = (255, 215, 60)
COLOR_CARD_BG = (18, 30, 48, 220)

# Ambient bubbles cache
_BUBBLES = [
    {"x": 120, "y": 250, "r": 3, "speed": 0.4},
    {"x": 280, "y": 420, "r": 2, "speed": 0.5},
    {"x": 480, "y": 190, "r": 3, "speed": 0.3},
    {"x": 620, "y": 360, "r": 4, "speed": 0.6},
    {"x": 190, "y": 470, "r": 2, "speed": 0.45},
    {"x": 380, "y": 300, "r": 3, "speed": 0.35},
]


def _draw_sky(surface):
    """Draws a vertical gradient for the sky with sun and soft clouds."""
    for y in range(SURFACE_Y):
        ratio = y / SURFACE_Y
        r = int(COLOR_SKY_TOP[0] * (1 - ratio) + COLOR_SKY_BOTTOM[0] * ratio)
        g = int(COLOR_SKY_TOP[1] * (1 - ratio) + COLOR_SKY_BOTTOM[1] * ratio)
        b = int(COLOR_SKY_TOP[2] * (1 - ratio) + COLOR_SKY_BOTTOM[2] * ratio)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))

    # Sun glow and sun disc
    sun_pos = (WIDTH - 100, 35)
    sun_surface = pygame.Surface((80, 80), pygame.SRCALPHA)
    pygame.draw.circle(sun_surface, (255, 245, 180, 60), (40, 40), 36)
    pygame.draw.circle(sun_surface, (255, 235, 130, 110), (40, 40), 24)
    pygame.draw.circle(sun_surface, (255, 250, 210, 240), (40, 40), 16)
    surface.blit(sun_surface, (sun_pos[0] - 40, sun_pos[1] - 40))

    # Stylized clouds
    for cx, cy in [(130, 28), (160, 24), (190, 28), (420, 32), (450, 26), (480, 32)]:
        cloud_surf = pygame.Surface((60, 30), pygame.SRCALPHA)
        pygame.draw.ellipse(cloud_surf, (255, 255, 255, 90), (0, 0, 60, 30))
        surface.blit(cloud_surf, (cx - 30, cy - 15))


def _draw_water(surface):
    """Draws deep water gradient, surface ripples, and drifting bubbles."""
    water_height = HEIGHT - SURFACE_Y
    for y_offset in range(0, water_height, 2):
        ratio = y_offset / water_height
        r = int(COLOR_WATER_SURFACE[0] * (1 - ratio) + COLOR_WATER_DEEP[0] * ratio)
        g = int(COLOR_WATER_SURFACE[1] * (1 - ratio) + COLOR_WATER_DEEP[1] * ratio)
        b = int(COLOR_WATER_SURFACE[2] * (1 - ratio) + COLOR_WATER_DEEP[2] * ratio)
        pygame.draw.rect(surface, (r, g, b), (0, SURFACE_Y + y_offset, WIDTH, 2))

    # Surface water ripple line
    pygame.draw.line(surface, (120, 205, 255), (0, SURFACE_Y), (WIDTH, SURFACE_Y), 3)
    pygame.draw.line(surface, (200, 240, 255), (0, SURFACE_Y + 2), (WIDTH, SURFACE_Y + 2), 1)

    # Ambient bubbles update and draw
    for bubble in _BUBBLES:
        bubble["y"] -= bubble["speed"]
        if bubble["y"] < SURFACE_Y + 5:
            bubble["y"] = HEIGHT - 10
        bx, by = int(bubble["x"]), int(bubble["y"])
        pygame.draw.circle(surface, (140, 210, 255, 120), (bx, by), bubble["r"], 1)


def _draw_boat(surface, hook):
    """Draws a wooden rowboat with a fishing rod extending over the water."""
    bx = int(hook.x)
    by = SURFACE_Y

    # Boat hull polygon
    hull_points = [
        (bx - 55, by - 18),
        (bx + 40, by - 18),
        (bx + 52, by - 4),
        (bx + 35, by + 4),
        (bx - 45, by + 4),
        (bx - 55, by - 8),
    ]
    pygame.draw.polygon(surface, COLOR_BOAT_HULL, hull_points)
    pygame.draw.polygon(surface, COLOR_BOAT_RIM, hull_points, 2)

    # Boat interior seat
    pygame.draw.rect(surface, COLOR_BOAT_SEAT, (bx - 20, by - 14, 30, 6))

    # Fishing rod extending from boat toward hook line
    rod_start = (bx - 10, by - 14)
    rod_tip = (bx, by - 26)
    pygame.draw.line(surface, COLOR_ROD, rod_start, rod_tip, 3)

    # Line from rod tip to hook
    pygame.draw.line(surface, COLOR_LINE, rod_tip, (bx, int(hook.y)), 1)


def _draw_hook(surface, hook):
    """Draws a metallic fishing hook with glint and curved barb."""
    hx, hy = int(hook.x), int(hook.y)

    # Eyelet and shank
    pygame.draw.circle(surface, COLOR_HOOK, (hx, hy - 4), 3, 1)
    pygame.draw.line(surface, COLOR_HOOK, (hx, hy - 4), (hx, hy + 4), 2)

    # Curved bend & sharp barb
    hook_curve = [
        (hx, hy + 4),
        (hx + 3, hy + 7),
        (hx + 7, hy + 6),
        (hx + 8, hy + 2),
    ]
    pygame.draw.lines(surface, COLOR_HOOK, False, hook_curve, 2)
    # Shiny glint
    pygame.draw.circle(surface, (255, 255, 255), (hx, hy - 2), 1)


def draw_scene(surface, hook, fish_list):
    """Renders the complete game scene: environment, boat, hook, and fish."""
    _draw_sky(surface)
    _draw_water(surface)
    _draw_boat(surface, hook)
    _draw_hook(surface, hook)

    for fish in fish_list:
        if hasattr(fish, "draw"):
            fish.draw(surface)
        else:
            pygame.draw.ellipse(surface, fish.color, fish.get_rect())


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    """Renders text with a subtle dark drop shadow for high readability."""
    shadow = font.render(text, True, (20, 25, 35))
    surface.blit(shadow, (pos[0] + 1, pos[1] + 1))
    main_surf = font.render(text, True, color)
    surface.blit(main_surf, pos)


def draw_banner(surface, font, text):
    """Draws a centered banner notification across the screen."""
    surf = font.render(text, True, COLOR_GOLD)
    rect = surf.get_rect(
        center=(surface.get_width() // 2, surface.get_height() // 2)
    )
    # Background pill
    bg_rect = rect.inflate(28, 14)
    bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
    pygame.draw.rect(bg_surf, COLOR_CARD_BG, bg_surf.get_rect(), border_radius=10)
    pygame.draw.rect(bg_surf, (100, 160, 220, 180), bg_surf.get_rect(), 2, border_radius=10)
    surface.blit(bg_surf, bg_rect.topleft)
    surface.blit(surf, rect)


def draw_hud(surface, font_small, font_large, score, remaining_time, hook_state, high_score=0):
    """Draws modern translucent HUD badges for Score, Timer, and Cast Prompt."""
    # Score badge (Top Left)
    score_text = f"SCORE: {score}"
    score_surf = font_small.render(score_text, True, COLOR_TEXT)
    s_rect = score_surf.get_rect(topleft=(18, 16))
    s_bg = pygame.Rect(12, 10, s_rect.width + 16, s_rect.height + 12)
    bg_surf = pygame.Surface(s_bg.size, pygame.SRCALPHA)
    pygame.draw.rect(bg_surf, (20, 35, 55, 200), bg_surf.get_rect(), border_radius=8)
    pygame.draw.rect(bg_surf, (70, 130, 190, 140), bg_surf.get_rect(), 1, border_radius=8)
    surface.blit(bg_surf, s_bg.topleft)
    draw_text(surface, font_small, score_text, (18, 16))

    # Timer badge (Top Right)
    time_int = max(0, int(math.ceil(remaining_time)))
    time_text = f"TIME: {time_int}s"
    if time_int <= 5:
        time_color = (255, 80, 80)  # Urgent red
    elif time_int <= 10:
        time_color = (255, 210, 60)  # Warning amber
    else:
        time_color = (130, 240, 160)  # Healthy green

    t_surf = font_small.render(time_text, True, time_color)
    t_rect = t_surf.get_rect(topright=(WIDTH - 20, 16))
    t_bg = pygame.Rect(t_rect.left - 8, 10, t_rect.width + 16, t_rect.height + 12)
    t_bg_surf = pygame.Surface(t_bg.size, pygame.SRCALPHA)
    pygame.draw.rect(t_bg_surf, (20, 35, 55, 200), t_bg_surf.get_rect(), border_radius=8)
    pygame.draw.rect(t_bg_surf, (70, 130, 190, 140), t_bg_surf.get_rect(), 1, border_radius=8)
    surface.blit(t_bg_surf, t_bg.topleft)
    draw_text(surface, font_small, time_text, t_rect.topleft, color=time_color)

    # Cast key prompt (Center Top when IDLE)
    if hook_state == "idle":
        prompt_text = "Press [SPACE] to Cast"
        p_surf = font_small.render(prompt_text, True, (240, 245, 255))
        p_rect = p_surf.get_rect(center=(WIDTH // 2, 22))
        p_bg = p_rect.inflate(20, 10)
        p_bg_surf = pygame.Surface(p_bg.size, pygame.SRCALPHA)
        pygame.draw.rect(p_bg_surf, (15, 30, 50, 180), p_bg_surf.get_rect(), border_radius=8)
        pygame.draw.rect(p_bg_surf, (80, 150, 220, 130), p_bg_surf.get_rect(), 1, border_radius=8)
        surface.blit(p_bg_surf, p_bg.topleft)
        draw_text(surface, font_small, prompt_text, p_rect.topleft, color=(240, 245, 255))


def draw_game_over_modal(surface, font_title, font_body, score, high_score):
    """Draws a premium game-over modal with score summary and restart prompt."""
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((8, 18, 32, 175))
    surface.blit(overlay, (0, 0))

    card_w, card_h = 440, 240
    card_rect = pygame.Rect((WIDTH - card_w) // 2, (HEIGHT - card_h) // 2, card_w, card_h)
    card_surf = pygame.Surface((card_w, card_h), pygame.SRCALPHA)
    pygame.draw.rect(card_surf, (22, 38, 62, 245), card_surf.get_rect(), border_radius=16)
    pygame.draw.rect(card_surf, COLOR_GOLD, card_surf.get_rect(), 3, border_radius=16)
    surface.blit(card_surf, card_rect.topleft)

    # Modal header
    title_surf = font_title.render("ROUND FINISHED!", True, COLOR_GOLD)
    surface.blit(title_surf, title_surf.get_rect(center=(WIDTH // 2, card_rect.top + 45)))

    # Scores
    score_surf = font_body.render(f"Final Score: {score} pts", True, (255, 255, 255))
    surface.blit(score_surf, score_surf.get_rect(center=(WIDTH // 2, card_rect.top + 105)))

    best_surf = font_body.render(f"Best Score:  {high_score} pts", True, (140, 225, 255))
    surface.blit(best_surf, best_surf.get_rect(center=(WIDTH // 2, card_rect.top + 140)))

    # Restart button prompt
    prompt_surf = font_body.render("Press [R] or [SPACE] to Play Again", True, (255, 235, 140))
    surface.blit(prompt_surf, prompt_surf.get_rect(center=(WIDTH // 2, card_rect.top + 195)))