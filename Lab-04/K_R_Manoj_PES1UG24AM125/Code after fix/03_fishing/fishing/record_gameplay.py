"""
Utility script to record 10-second gameplay videos for the lab submission checklist.

Usage:
  python record_gameplay.py --mode after       # Automatically simulates & records 10s of fixed gameplay
  python record_gameplay.py --mode before      # Simulates the starter bug (depth-only catch) for 10s
  python record_gameplay.py --mode play        # Opens playable window and records 10s of your gameplay
"""

import sys
import os
import argparse
import numpy as np
import cv2
import pygame

from game.renderer import WIDTH, HEIGHT, WINDOW_SIZE, SURFACE_Y, MAX_DEPTH_Y, COLOR_TEXT
from game.hook import Hook, IDLE, CASTING, RETRACTING
from game.fish import Fish, SlowFish, FastFish
from game.catch import check_catch
from game.game_engine import GameEngine


def record_after(output_path="gameplay_after.mp4", duration_sec=10, fps=30):
    """Simulates realistic gameplay demonstrating fixed catch detection, distinct fish, player cast, and timer."""
    print(f"Recording {duration_sec}s demo of AFTER (fixed) gameplay to {output_path}...")
    pygame.init()
    surface = pygame.Surface(WINDOW_SIZE)
    font = pygame.font.SysFont("consolas", 20, bold=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (WIDTH, HEIGHT))

    engine = GameEngine()
    total_frames = int(duration_sec * fps)

    for frame_idx in range(total_frames):
        # Cast at specific frames to showcase player control
        if frame_idx in (15, 140, 260) and engine.hook.state == IDLE:
            engine.hook.start_cast()

        engine.update()
        engine.draw(surface, font)

        # Convert pygame surface to BGR frame for OpenCV
        rgb_str = pygame.image.tostring(surface, "RGB")
        frame = np.frombuffer(rgb_str, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(bgr_frame)

    writer.release()
    pygame.quit()
    print(f"Successfully saved {output_path} ({os.path.getsize(output_path)} bytes).")


def record_before(output_path="gameplay_before.mp4", duration_sec=10, fps=30):
    """Simulates starter behavior demonstrating the bug (fish caught from far away by depth)."""
    print(f"Recording {duration_sec}s demo of BEFORE (buggy) gameplay to {output_path}...")
    pygame.init()
    surface = pygame.Surface(WINDOW_SIZE)
    font = pygame.font.SysFont("consolas", 20, bold=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (WIDTH, HEIGHT))

    # Starter engine simulation
    hook = Hook(x=WIDTH / 2, surface_y=SURFACE_Y, max_depth_y=MAX_DEPTH_Y, speed=5)
    fish_list = [
        Fish(x=90, y=180, speed=2, point_value=10, color=(80, 180, 220)),
        Fish(x=580, y=280, speed=-2, point_value=10, color=(80, 180, 220)),
        Fish(x=150, y=380, speed=3, point_value=10, color=(80, 180, 220)),
    ]
    hooked_fish = None
    score = 0
    total_frames = int(duration_sec * fps)

    for _ in range(total_frames):
        # Auto-loop casting (starter behavior)
        if hook.state == IDLE:
            hook.start_cast()

        hook.update()
        for f in fish_list:
            f.update(WIDTH)

        if hooked_fish is not None:
            hooked_fish.x = hook.x
            hooked_fish.y = hook.y
            if hook.state == IDLE:
                score += hooked_fish.point_value
                hooked_fish = None
        else:
            # STARTER BUG: Only compares depth within 10px!
            for f in fish_list:
                if abs(hook.y - f.y) < 10:
                    fish_list.remove(f)
                    hooked_fish = f
                    hooked_fish.x = hook.x
                    hooked_fish.y = hook.y
                    hook.catch_fish()
                    break

        # Render starter style
        from game import renderer
        draw_list = list(fish_list)
        if hooked_fish is not None:
            draw_list.append(hooked_fish)

        surface.fill((140, 200, 230), pygame.Rect(0, 0, WIDTH, SURFACE_Y))
        surface.fill((30, 90, 150), pygame.Rect(0, SURFACE_Y, WIDTH, HEIGHT - SURFACE_Y))
        pygame.draw.rect(surface, (120, 80, 50), (int(hook.x - 40), SURFACE_Y - 20, 80, 22))
        pygame.draw.line(surface, (240, 240, 240), (int(hook.x), SURFACE_Y), (int(hook.x), int(hook.y)), 2)
        pygame.draw.circle(surface, (220, 220, 220), (int(hook.x), int(hook.y)), 7)
        for f in draw_list:
            pygame.draw.ellipse(surface, f.color, f.get_rect())

        # Annotate with bug explanation overlay
        renderer.draw_text(surface, font, f"Score: {score}", (10, 10))
        renderer.draw_text(surface, font, "[STARTER BUG]: Hook snags fish across screen by depth!", (10, 36), color=(255, 100, 100))

        rgb_str = pygame.image.tostring(surface, "RGB")
        frame = np.frombuffer(rgb_str, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(bgr_frame)

    writer.release()
    pygame.quit()
    print(f"Successfully saved {output_path} ({os.path.getsize(output_path)} bytes).")


def record_interactive(output_path="gameplay_interactive.mp4", duration_sec=10, fps=60):
    """Opens an interactive pygame window, records your actions for 10 seconds."""
    print(f"Opening interactive window for {duration_sec}s recording to {output_path}...")
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Fishing Lab - Recording...")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 20, bold=True)

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(output_path, fourcc, fps, (WIDTH, HEIGHT))

    engine = GameEngine()
    total_frames = int(duration_sec * fps)
    frame_count = 0

    running = True
    while running and frame_count < total_frames:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.handle_event(event)

        engine.update()
        engine.draw(screen, font)
        pygame.display.flip()

        rgb_str = pygame.image.tostring(screen, "RGB")
        frame = np.frombuffer(rgb_str, dtype=np.uint8).reshape((HEIGHT, WIDTH, 3))
        bgr_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        writer.write(bgr_frame)

        frame_count += 1
        clock.tick(fps)

    writer.release()
    pygame.quit()
    print(f"Recorded {frame_count} frames to {output_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record 10-second gameplay videos")
    parser.add_argument("--mode", choices=["after", "before", "play", "both"], default="both")
    args = parser.parse_args()

    if args.mode in ("before", "both"):
        record_before()
    if args.mode in ("after", "both"):
        record_after()
    if args.mode == "play":
        record_interactive()
