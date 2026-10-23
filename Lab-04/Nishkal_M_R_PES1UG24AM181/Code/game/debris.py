import pygame


class Debris:
    """A sliced-off piece of a block that tumbles and falls out of the arena."""

    GRAVITY = 0.55

    def __init__(self, x, y, width, height, color, vx, spin):
        self.width = max(2, int(width))
        self.height = int(height)
        self.cx = x + width / 2      # centre position
        self.cy = y + height / 2
        self.vx = vx
        self.vy = -2.0               # small upward pop before falling
        self.angle = 0.0
        self.spin = spin
        self.alpha = 255

        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, color, surf.get_rect(), border_radius=4)
        pygame.draw.rect(surf, (245, 245, 250), surf.get_rect(), width=2, border_radius=4)
        self.base = surf

    def update(self):
        self.vy += self.GRAVITY
        self.cx += self.vx
        self.cy += self.vy
        self.angle += self.spin
        self.alpha = max(0, self.alpha - 2)

    def is_gone(self, screen_height):
        return self.cy - self.height > screen_height or self.alpha <= 0

    def shift(self, dy):
        self.cy += dy

    def render(self, surface):
        rotated = pygame.transform.rotate(self.base, self.angle)
        rotated.set_alpha(self.alpha)
        surface.blit(rotated, rotated.get_rect(center=(int(self.cx), int(self.cy))))
