import os
import unittest
os.environ["SDL_VIDEODRIVER"] = "dummy"
import pygame
pygame.init()

from game.hook import Hook, IDLE, CASTING, RETRACTING
from game.fish import Fish, SlowFish, FastFish, GoldenFish
from game.catch import check_catch
from game.game_engine import GameEngine
from game.renderer import WIDTH, HEIGHT, SURFACE_Y, MAX_DEPTH_Y


class TestFishingGame(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()

    def test_task1_catch_detection_no_overlap(self):
        """Hook and fish at same depth but separated horizontally should NOT catch."""
        hook = Hook(x=350, surface_y=80, max_depth_y=460)
        hook.y = 200
        hook.state = CASTING

        # Fish at same depth (y=200) but far to left (x=100)
        fish = Fish(x=100, y=200, speed=2, width=36, height=18)
        self.assertIsNone(check_catch(hook, [fish]))

        # Fish at same depth (y=200) but far to right (x=600)
        fish_right = Fish(x=600, y=200, speed=-2, width=36, height=18)
        self.assertIsNone(check_catch(hook, [fish_right]))

    def test_task1_catch_detection_with_overlap(self):
        """Hook and fish overlapping both horizontally and vertically should catch."""
        hook = Hook(x=350, surface_y=80, max_depth_y=460, width=14, height=14)
        hook.y = 200
        hook.state = CASTING

        # Fish overlapping hook
        overlapping_fish = Fish(x=352, y=202, speed=2, width=36, height=18)
        self.assertEqual(check_catch(hook, [overlapping_fish]), overlapping_fish)

    def test_task2_multiple_fish_types(self):
        """SlowFish and FastFish have distinct speed, point_value, color and size."""
        slow = SlowFish(x=100, y=180)
        fast = FastFish(x=100, y=280)
        gold = GoldenFish(x=100, y=380)

        self.assertNotEqual(slow.speed, fast.speed)
        self.assertLess(abs(slow.speed), abs(fast.speed))
        self.assertNotEqual(slow.point_value, fast.point_value)
        self.assertLess(slow.point_value, fast.point_value)
        self.assertNotEqual(slow.color, fast.color)
        self.assertNotEqual((slow.width, slow.height), (fast.width, fast.height))
        self.assertGreater(gold.point_value, fast.point_value)

    def test_task2_fish_scoring_values(self):
        """Verify correct point value is awarded when fish reaches surface."""
        slow = SlowFish(x=350, y=80, speed=1)
        self.engine.hooked_fish = slow
        self.engine.hook.state = IDLE
        self.engine.update()
        self.assertEqual(self.engine.score, slow.point_value)

        fast = FastFish(x=350, y=80, speed=4)
        self.engine.hooked_fish = fast
        self.engine.hook.state = IDLE
        self.engine.update()
        self.assertEqual(self.engine.score, slow.point_value + fast.point_value)

    def test_task2_fish_wrap_around(self):
        """Test smooth wrap-around of fish across boundaries."""
        fish_right = Fish(x=WIDTH + 50, y=200, speed=2, width=40)
        fish_right.update(WIDTH)
        self.assertEqual(fish_right.x, -fish_right.width / 2)

        fish_left = Fish(x=-50, y=200, speed=-2, width=40)
        fish_left.update(WIDTH)
        self.assertEqual(fish_left.x, WIDTH + fish_left.width / 2)

    def test_task3_player_controlled_casting(self):
        """Hook should remain IDLE until player presses cast."""
        self.assertEqual(self.engine.hook.state, IDLE)

        # Update without input should keep it IDLE
        self.engine.update()
        self.assertEqual(self.engine.hook.state, IDLE)

        # Trigger cast event (SPACE)
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.engine.handle_event(event)
        self.assertEqual(self.engine.hook.state, CASTING)

        # Subsequent cast during cast should NOT reset or interrupt
        self.engine.hook.y = 150
        self.engine.handle_event(event)
        self.assertEqual(self.engine.hook.state, CASTING)
        self.assertEqual(self.engine.hook.y, 150)

    def test_task3_auto_retract_at_max_depth(self):
        """Hook should travel down to max depth and retract automatically."""
        self.engine.hook.start_cast()
        self.assertEqual(self.engine.hook.state, CASTING)

        # Fast forward until it reaches max depth
        for _ in range(200):
            self.engine.hook.update()
            if self.engine.hook.state == RETRACTING:
                break
        self.assertEqual(self.engine.hook.state, RETRACTING)

        # Fast forward until it returns to surface
        for _ in range(200):
            self.engine.hook.update()
            if self.engine.hook.state == IDLE:
                break
        self.assertEqual(self.engine.hook.state, IDLE)
        self.assertEqual(self.engine.hook.y, self.engine.hook.surface_y)

    def test_task4_round_timer_countdown_and_game_over(self):
        """30-second round timer expires and ends round."""
        self.assertEqual(self.engine.ROUND_DURATION, 30)
        self.assertFalse(self.engine.round_over)

        # Simulate 31 seconds passing
        self.engine.start_time = pygame.time.get_ticks() - 31000
        self.engine.update()

        self.assertTrue(self.engine.round_over)
        self.assertEqual(self.engine.remaining_time, 0)

        # No casting or catching allowed after round is over
        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.engine.handle_event(event)
        self.assertEqual(self.engine.hook.state, IDLE)

    def test_task4_round_reset(self):
        """Pressing R after round over resets timer, score, and state."""
        self.engine.round_over = True
        self.engine.score = 50
        self.engine.remaining_time = 0

        event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_r)
        self.engine.handle_event(event)

        self.assertFalse(self.engine.round_over)
        self.assertEqual(self.engine.score, 0)
        self.assertEqual(self.engine.remaining_time, 30)
        self.assertEqual(self.engine.hook.state, IDLE)

    def test_rendering_headless(self):
        """Ensure full draw cycle executes without exceptions."""
        surface = pygame.Surface((WIDTH, HEIGHT))
        font = pygame.font.SysFont("consolas", 20)
        self.engine.draw(surface, font)

        # Also test round_over draw
        self.engine.round_over = True
        self.engine.draw(surface, font)


if __name__ == "__main__":
    unittest.main()
