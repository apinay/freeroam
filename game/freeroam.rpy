
init python:
    from enum import Enum, unique

    def ceildiv(a, b):
        return -(a // -b)

    @unique
    class Direction(Enum):
        LEFT = "left"
        UP = "up"
        RIGHT = "right"
        DOWN = "down"

    def move(direction, toon, movement_mask):
        if toon:
            toon.move(direction, movement_mask)
        return

    def stop(direction, toon):
        if toon:
            toon.stop(direction)
        return

    class Toon(object):
        """Character toon for storing the Sprite variables"""
        def __init__(
            self, position_x, position_y, anchor_x, anchor_y, left_anim, up_anim, right_anim, down_anim, stationary_left, 
            stationary_up, stationary_right, stationary_down, animation_frames, speed, reduction, direction = Direction.RIGHT
        ):
            super(Toon, self).__init__()
            self.position_x = position_x
            self.position_y = position_y
            self.anchor_x = anchor_x
            self.anchor_y = anchor_y
            self.left_anim = left_anim
            self.up_anim = up_anim
            self.right_anim = right_anim
            self.down_anim = down_anim
            self.stationary_left = stationary_left
            self.stationary_up = stationary_up
            self.stationary_right = stationary_right
            self.stationary_down = stationary_down
            self.movement_anim_id = 0
            self.movement_anim_counter = 0
            self.direction = direction
            self.animation_frames = animation_frames
            self.speed = speed
            self.reduction = reduction
            self.still = True

        def get_current_image(self):
            if self.direction == Direction.RIGHT:
                return self.stationary_right if self.still else self.right_anim + "_" + str(self.movement_anim_id)
            if self.direction == Direction.UP:
                return self.stationary_up if self.still else self.up_anim + "_" + str(self.movement_anim_id)
            if self.direction == Direction.LEFT:
                return self.stationary_left if self.still else self.left_anim + "_" + str(self.movement_anim_id)
            if self.direction == Direction.DOWN:
                return self.stationary_down if self.still else self.down_anim + "_" + str(self.movement_anim_id)

        def stop(self, direction):
            self.still = True
            self.direction = direction
            self.movement_anim_counter = 0

        def _can_move(self, x, y, movement_mask):
            return renpy.load_surface(movement_mask).get_at((x,y)) == (255, 255, 255, 255)

        def move(self, direction, movement_mask=None):
            self.still = False
            self.direction = direction
            new_position_x = self.position_x - self.speed if self.direction == Direction.LEFT else self.position_x + self.speed if self.direction == Direction.RIGHT else self.position_x
            new_position_y = self.position_y - self.speed if self.direction == Direction.UP else self.position_y + self.speed if self.direction == Direction.DOWN else self.position_y

            if new_position_x > 20 and new_position_x < 1900 and new_position_y > 20 and new_position_y < 1060: # Check that the char is inside the screen.
                if (movement_mask and self._can_move(new_position_x, new_position_y, movement_mask)) or movement_mask == None:
                    self.position_x = new_position_x
                    self.position_y = new_position_y
                    self.movement_anim_counter = (self.movement_anim_counter + 1) % self.reduction
                    self.movement_anim_id = int(self.movement_anim_counter // (self.reduction / self.animation_frames))

# This is the basic screen
screen freeroam(movement_mask, toon):
    
    add toon.get_current_image() anchor (toon.anchor_x, toon.anchor_y) pos (toon.position_x, toon.position_y) zoom 2.5
    key [ "any_K_LEFT", "any_KP_LEFT", "any_a" ] action Function(move, Direction.LEFT, toon, movement_mask)    
    key [ "any_K_RIGHT", "any_KP_RIGHT", "any_d" ] action Function(move, Direction.RIGHT, toon, movement_mask)
    key [ "any_K_UP", "any_KP_UP", "any_w" ] action Function(move, Direction.UP, toon, movement_mask)
    key [ "any_K_DOWN", "any_KP_DOWN", "any_s" ] action Function(move, Direction.DOWN, toon, movement_mask)

    key [ "keyup_K_LEFT", "keyup_KP_LEFT", "keyup_a" ] action Function(stop, Direction.LEFT, toon)
    key [ "keyup_K_RIGHT", "keyup_KP_RIGHT", "keyup_d" ] action Function(stop, Direction.RIGHT, toon)
    key [ "keyup_K_UP", "keyup_KP_UP", "keyup_w" ] action Function(stop, Direction.UP, toon)
    key [ "keyup_K_DOWN", "keyup_KP_DOWN", "keyup_s" ] action Function(stop, Direction.DOWN, toon)
