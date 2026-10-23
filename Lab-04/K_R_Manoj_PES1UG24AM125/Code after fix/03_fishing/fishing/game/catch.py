"""
catch: hook-vs-fish catch detection.

Fix for Task 1:
The starter code checked only vertical proximity (`abs(hook.y - fish.y) < 10`),
causing fish anywhere on screen to be caught as long as their depth matched.
This implementation performs full 2D bounding-box collision detection between
the hook and the fish.
"""


def check_catch(hook, fish_list):
    """
    Returns the first fish that genuinely overlaps with the hook, or None.
    Collision is determined using bounding box overlap (both horizontal and vertical).
    """
    hook_rect = hook.get_rect() if hasattr(hook, "get_rect") else None

    for fish in fish_list:
        if hook_rect is not None and hasattr(fish, "get_rect"):
            if hook_rect.colliderect(fish.get_rect()):
                return fish
        elif (
            abs(hook.x - fish.x) < (hook.width + fish.width) / 2
            and abs(hook.y - fish.y) < (hook.height + fish.height) / 2
        ):
            return fish

    return None