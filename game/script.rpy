
define SPEED = 5            # How many pixels each impulse moves the char

# Remember that REDUCTION should be divisible by ANIMATION_FRAMES or some of the frames (mainly last) will play for shorter time
define REDUCTION = 8        # How many impulses before we flip to next animation frame, should be at least the number of frames
define ANIMATION_FRAMES = 2 # How many animation frames


image bg_walk_down_0 = "sprites/bg_front_1.png"
image bg_walk_down_1 = "sprites/bg_front_3.png"
image bg_down_still = "sprites/bg_front_2.png"

image bg_walk_left_0 = "sprites/bg_left_1.png"
image bg_walk_left_1 = "sprites/bg_left_3.png"
image bg_left_still = "sprites/bg_left_2.png"

image bg_walk_right_0 = "sprites/bg_right_1.png"
image bg_walk_right_1 = "sprites/bg_right_3.png"
image bg_right_still = "sprites/bg_right_2.png"

image bg_walk_up_0 = "sprites/bg_back_1.png"
image bg_walk_up_1 = "sprites/bg_back_3.png"
image bg_up_still = "sprites/bg_back_2.png"

# Anchor without zoom 17, 32
define beach_girl = Toon(40, 840, 42, 80, "bg_walk_left", "bg_walk_up", "bg_walk_right", "bg_walk_down", "bg_left_still", "bg_up_still", "bg_right_still", "bg_down_still", ANIMATION_FRAMES, SPEED, REDUCTION, Direction.RIGHT)


screen game_scene(background, movement_mask, toon):
    add background
    use freeroam(movement_mask, toon)

label show_freeroam_room(background, movement_mask, toon):
    while True:
        show screen game_scene(background, movement_mask, toon)
        $ exit = ui.interact()
    return

image road = "road.png"

label start:
    $ movement_mask = "road_mask.png"
    call show_freeroam_room("road", movement_mask, beach_girl) from _call_show_freeroam_room

    "You've created a new Ren'Py game."

    return
