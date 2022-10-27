"""
Simple program to show moving a sprite with the keyboard.

This program uses the Arcade library found at http://arcade.academy

Artwork from https://kenney.nl/assets/space-shooter-redux

"""

import arcade
import random



SPRITE_SCALING = 0.4

# Set the size of the screen
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Variables controlling the player
PLAYER_LIVES = 5
PLAYER_SPEED_X = 5
PLAYER_SPEED_Y = 5
PLAYER_START_X = SCREEN_WIDTH / 2
PLAYER_START_Y = SCREEN_HEIGHT / 2
PLAYER_SHOT_SPEED = 4
OBSTACLE_SPEED = 6
DASHING_TIME = 1
DASHING_SPEED = 5
DASH_COOLDOWN = 0.75
OBSTACLE_HARMLESS_TIME = 2.5
OBSTACLE_HARMLESS_ALPHA = 100
OBSTACLE_HARMLESS_SPEED_FACTOR = 0.3
# length of a level in seconds
LEVEL_TIME = 20

TAKING_DAMAGE_TIME = 0.75
LIVES_TAKING_DAMAGE = 1
LIVES_GOTTEN_BY_POWER_UP = 1
DASH_ALPHA = 150



DASHING_KEY = arcade.key.SPACE

class Player(arcade.Sprite):
    """
    The player
    """

    def __init__(self, **kwargs):
        """
        Setup new Player object
        """


        # How much to scale the graphics
        kwargs['scale'] = SPRITE_SCALING

        # Pass arguments to class arcade.Sprite
        super().__init__(**kwargs)

        self.taking_damage_timer = 0
        self.taking_damage_path = "images/playerShip1_red.png"
        self.normal_path = "images/playerShip1_blue.png"

        self.texture = arcade.load_texture(self.normal_path)

        self.player_lives = PLAYER_LIVES

        self.wanted_angle = 0

        self.score = 0

        self.is_dashing = False
        self.dashing_time_left = 0
        self.dash_cooldown = 0

    def dash(self):
        """
        Enable Dashing
        """
        if not self.is_dashing and self.dash_cooldown <= 0:
            self.is_dashing = True
            self.dashing_time_left = DASHING_TIME
            self.dash_cooldown = DASH_COOLDOWN
            self.alpha = DASH_ALPHA

    def taking_damage(self):
        if self.taking_damage_timer == 0:
            self.taking_damage_timer = TAKING_DAMAGE_TIME
            self.texture = arcade.load_texture(self.taking_damage_path)
            self.player_lives -= LIVES_TAKING_DAMAGE


    def getting_life(self, number_of_lives):
        self.player_lives += number_of_lives

    def update(self, delta_time):
        """
        Move the sprite
        """
        if self.is_dashing:
            self.dashing_time_left -= delta_time
            if self.dashing_time_left <= 0:
                self.is_dashing = False
                self.dashing_time_left = 0
                self.alpha = 255

        if self.taking_damage_timer > 0:
            self.taking_damage_timer -= delta_time
        elif self.taking_damage_timer <= 0:
            self.texture = arcade.load_texture(self.normal_path)
            self.taking_damage_timer = 0

        d = self.angle - self.wanted_angle
        self.angle -= d / 10
        #if self.wanted_angle < 0:
        #    if self.angle > self.wanted_angle:
        #        self.angle -= delta_time
        #else:
        #    if self.angle < self.wanted_angle:
        #        self.angle += delta_time

        # Update center_x
        if self.is_dashing:
            self.center_x += self.change_x * DASHING_SPEED
            self.center_y += self.change_y * DASHING_SPEED
        else:
            self.center_x += self.change_x
            self.center_y += self.change_y

        # Don't let the player move off-screen
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1
        elif self.bottom < 0:
            self.bottom = 0

        if not self.is_dashing:
            self.dash_cooldown -= delta_time

class PowerUp(arcade.Sprite):
    def __init__(self):

        super().__init__("images/power-ups/pill_red.png", SPRITE_SCALING * 3.2)

        self.center_x = random.randint(0,SCREEN_WIDTH)
        self.center_y = random.randint(0,SCREEN_HEIGHT)
        self.power_up_despawn_cooldown = 5
        self.alpha = 255
        self.power_up_function = random.choice([self.life_up, self.score_up])

    def on_update(self, delta_time):

        self.power_up_despawn_cooldown -= delta_time

        if self.power_up_despawn_cooldown <= 0:
            self.kill_yourself()

    def kill_yourself(self):
        self.kill()


    def score_up(self, player):
        pass

    def life_up(self, player):
        player.getting_life(LIVES_GOTTEN_BY_POWER_UP)

class Obstacle(arcade.Sprite):
    """
    obstacles to dodge
    """

    obstacle_max_speed = 3

    types = {
        1: {
            "vectors": [
                [1, 0], # right
                [-1, 0],  # left
                [0, 1], # up
                [0, -1], # down
                [1, 1],
                [-1, -1],
                [1, -1],
                [-1, 1]
            ],
            "graphics": "images/Meteors/meteorGrey_med2.png",
            # "scaling": random.randint(3, 8)
        },
        2: {
            "vectors": [
                [1, 0],  # right
                [-1, 0],  # left
                [0, 1],  # up
                [0, -1],  # down
                [1, 1],
                [-1, -1],
                [1, -1],
                [-1, 1]
            ],
            "graphics": "images/Meteors/meteorBrown_med3.png",
            # "scaling": random.randint(4, 9)
        },
        3: {
            "vectors": [
                [1, 0],  # right
                [-1, 0],  # left
                [0, 1],  # up
                [0, -1],  # down
                [1, 1],
                [-1, -1],
                [1, -1],
                [-1, 1]
            ],
            "graphics": "images/Meteors/meteorGrey_tiny2.png",
            # "scaling": random.randint(4, 9),
        }
    }
    def __init__(self, speed, type=1, spawn_on_edge=False):

        super().__init__(Obstacle.types[type]["graphics"], SPRITE_SCALING * random.randint(4, 9))

        if spawn_on_edge:
            spawn_positions = [
                (random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT), # Top edge
                (SCREEN_WIDTH, random.randint(0, SCREEN_HEIGHT)), # Right
                (0, random.randint(0, SCREEN_HEIGHT)), # Left
                (random.randint(0, SCREEN_WIDTH), 0) #
            ]
            self.center_x, self.center_y = random.choice(spawn_positions)
        else:
            self.center_x = random.randint(0, SCREEN_WIDTH)
            self.center_y = random.randint(0, SCREEN_HEIGHT)

        self.speed_x, self.speed_y = random.choice(Obstacle.types[type]["vectors"])

        # random speed noise for obstacles
        self.speed_noise = random.uniform(0.6, 1.5)
        self.change_x *= speed * self.speed_noise
        self.change_y *= speed * self.speed_noise

        self.change_angle = random.uniform(-1, 1)

        self.alpha = OBSTACLE_HARMLESS_ALPHA

        if spawn_on_edge is False:
            self.harmless_timer = OBSTACLE_HARMLESS_TIME
            self.is_harmless = True
        else:
            self.harmless_timer = 0
            self.is_harmless = False

    def on_update(self, delta_time):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left > SCREEN_WIDTH:
            self.kill()
        elif self.right < 0:
            self.kill()
        elif self.bottom > SCREEN_HEIGHT:
            self.kill()
        elif self.top < 0:
            self.kill()

        if self.harmless_timer > 0:
            self.is_harmless = True
            self.alpha = min(255 / self.harmless_timer, 255)
            self.harmless_timer -= delta_time
        else:
            self.is_harmless = False
            self.alpha = 255

        if self.is_harmless:
            self.change_x = self.speed_x * OBSTACLE_HARMLESS_SPEED_FACTOR
            self.change_y = self.speed_y * OBSTACLE_HARMLESS_SPEED_FACTOR
            self.angle += self.change_angle * OBSTACLE_HARMLESS_SPEED_FACTOR
        else:
            self.change_x = self.speed_x
            self.change_y = self.speed_y
            self.angle += self.change_angle

class PlayerShot(arcade.Sprite):
    """
    A shot fired by the Player
    """

    def __init__(self, center_x=0, center_y=0):
        """
        Setup new PlayerShot object
        """

        # Set the graphics to use for the sprite
        super().__init__("images/Lasers/laserBlue01.png", SPRITE_SCALING)

        self.center_x = center_x
        self.center_y = center_y
        self.change_y = PLAYER_SHOT_SPEED

    def update(self):
        """
        Move the sprite
        """

        # Update y position
        self.center_y += self.change_y

        # Remove shot when over top of screen
        if self.bottom > SCREEN_HEIGHT:
            self.kill()

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height)

        print(self.get_viewport())

        self.level_timer = None
        self.mode = None
        self.respawn_powerup = 0

        # Variable that will hold a list of shots fired by the player
        self.player_shot_list = None
        self.obstacle_list = None
        self.power_ups_list = None
        self.number_of_obstacles = None

        # Set up the player info
        self.player_sprite = None

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        self.current_level = None

        # Get list of joysticks
        joysticks = arcade.get_joysticks()

        if joysticks:
            print("Found {} joystick(s)".format(len(joysticks)))

            # Use 1st joystick found
            self.joystick = joysticks[0]

            # Communicate with joystick
            self.joystick.open()

            # Map joysticks functions to local functions
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyaxis_motion = self.on_joyaxis_motion
            self.joystick.on_joyhat_motion = self.on_joyhat_motion

        else:
            print("No joysticks found")
            self.joystick = None

            # self.joystick.
        # Set the background color
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """
        # if you'r in startscreen, mode = "IN_START_SCREEN"
        # if you'r in game, mode = "IN_GAME"
        # if you'r in deathscreen, mode = "DEATH_SCREEN"
        self.mode = "IN_START_SCREEN"

        # Sprite lists
        self.player_shot_list = arcade.SpriteList()
        self.power_ups_list = arcade.SpriteList()

        #creating a power up when you start the game
        self.power_ups_list.append(PowerUp())

        self.current_level = 0
        self.obstacle_speed = OBSTACLE_SPEED

        self.number_of_obstacles = 65

        if self.mode == "IN_GAME":
            self.new_level()
        else:
            pass

    def set_mode(self, new_mode):
        print("changemode", new_mode)

        if new_mode == "IN_START_SCREEN":
            pass

        elif new_mode == "IN_GAME":
            # Create a Player object
            self.player_sprite = Player(
                center_x=PLAYER_START_X,
                center_y=PLAYER_START_Y
            )

            self.new_level()
            self.power_ups_list.append(PowerUp())

        self.mode = new_mode

    def new_level(self):

        self.level_timer = LEVEL_TIME

        self.obstacle_list = arcade.SpriteList()
        self.number_of_obstacles += self.current_level
        self.current_level += 1

        # Increases obstacle_speed with 50%
        self.obstacle_speed *= 1.5

        for i in range(self.number_of_obstacles):
            self.obstacle_list.append(Obstacle(speed=self.obstacle_speed, type=random.randint(1, 3)))

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()

        if self.mode == "IN_GAME":

            # Draw the obstacles
            self.obstacle_list.draw()

            self.power_ups_list.draw()

            # Draw the player sprite
            self.player_sprite.draw()

            # Draw players score on screen
            arcade.draw_text(
                "LIVES: {}".format(self.player_sprite.player_lives),  # Text to show
                10,  # X position
                SCREEN_HEIGHT - 20,  # Y positon
                arcade.color.WHITE  # Color of text
            )

            arcade.draw_text(
                "score: {}".format(int(self.player_sprite.score) * 10),  # Text to show
                10,  # X position
                SCREEN_HEIGHT - 40,  # Y positon
                arcade.color.WHITE  # Color of text
            )

            arcade.draw_text(
                "Next level in: {}".format(int(self.level_timer)),  # Text to show
                10,  # X position
                SCREEN_HEIGHT - 60,  # Y positon
                arcade.color.WHITE  # Color of text
            )

            arcade.draw_text(
                "Level: {}".format(int(self.current_level)),  # Text to show
                10,  # X position
                SCREEN_HEIGHT - 80,  # Y positon
                arcade.color.WHITE  # Color of text
            )

        elif self.mode == "IN_START_SCREEN":
            arcade.draw_text(
                "{}".format("press space to start"),  # Text to show
                SCREEN_WIDTH/2 -250,  # X position
                SCREEN_HEIGHT/2,  # Y positon
                arcade.color.WHITE,  # Color of text
                50
            )
        elif self.mode == "DEATH_SCREEN":
            arcade.draw_text(
                "{}".format("you die press space to return to start screen"),  # Text to show
                SCREEN_WIDTH/2 -375,  # X position
                SCREEN_HEIGHT/2,  # Y positon
                arcade.color.WHITE,  # Color of text
                30
            )

    def on_update(self, delta_time):
        """
        Movement and game logic
        """

        self.power_ups_list.on_update()

        if self.mode == "IN_GAME":

            # Calculate player speed based on the keys pressed
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0

            """
            check_for_collisions
            """

            obstacles_colliding_with_player = arcade.check_for_collision_with_list(
                self.player_sprite, self.obstacle_list
            )
            for o in obstacles_colliding_with_player:
                if self.player_sprite.is_dashing is False and not o.is_harmless:
                    self.player_sprite.taking_damage()

            power_ups_colliding_with_player = arcade.check_for_collision_with_list(
                self.player_sprite, self.power_ups_list
            )
            for pu in power_ups_colliding_with_player:
                pu.power_up_function(self.player_sprite)
                pu.kill_yourself()


            #respawns powerup

            if self.respawn_powerup <= 0:
                self.respawn_powerup = 8

            if self.respawn_powerup <= 0:
                self.respawn_powerup = 8

            self.respawn_powerup -= delta_time

            if self.respawn_powerup <= 0:
                self.power_ups_list.append(PowerUp())




            # Move player with keyboard
            if self.left_pressed and not self.right_pressed:
                self.player_sprite.change_x = -PLAYER_SPEED_X

            if self.right_pressed and not self.left_pressed:
                self.player_sprite.change_x = PLAYER_SPEED_X

            if self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = PLAYER_SPEED_Y

            if self.down_pressed and not self.up_pressed:
                self.player_sprite.change_y = - PLAYER_SPEED_Y

            if self.player_sprite.change_x > 0 and self.player_sprite.change_y == 0:
                self.player_sprite.wanted_angle = self.player_sprite.angle - 90 - self.player_sprite.angle

            if self.player_sprite.change_x > 0 and self.player_sprite.change_y > 0:
                self.player_sprite.wanted_angle = self.player_sprite.angle - 45 - self.player_sprite.angle

            if self.player_sprite.change_x == 0 and self.player_sprite.change_y > 0:
                self.player_sprite.wanted_angle = self.player_sprite.angle - 0 - self.player_sprite.angle

            if self.player_sprite.change_x < 0 and self.player_sprite.change_y == 0:
                self.player_sprite.wanted_angle = self.player_sprite.angle - -90 - self.player_sprite.angle

            if self.player_sprite.change_x == 0 and self.player_sprite.change_y < 0:
                self.player_sprite.wanted_angle = self.player_sprite.angle - -180 - self.player_sprite.angle

            if self.player_sprite.change_x < 0 and self.player_sprite.change_y < 0:
                self.player_sprite.wanted_angle = self.player_sprite.angle - -225 - self.player_sprite.angle

            if self.player_sprite.change_x < 0 and self.player_sprite.change_y > 0:
                self.player_sprite.wanted_angle = 45

            if self.player_sprite.change_x > 0 and self.player_sprite.change_y < 0:
                self.player_sprite.wanted_angle = -135

            # Move player with joystick if present
            if self.joystick:
                self.player_sprite.change_x = round(self.joystick.x) * PLAYER_SPEED_X
                self.player_sprite.change_y = round(self.joystick.y) * PLAYER_SPEED_Y * -1
                if round(self.joystick.x) == 1:
                    self.player_sprite.angle = -90
                elif round(self.joystick.x) == -1:
                    self.player_sprite.angle = 90
                elif round(self.joystick.y) == 1:
                    self.player_sprite.angle = 180
                elif round(self.joystick.y) == -1:
                    self.player_sprite.angle = 0

            # Update player sprite
            self.player_sprite.update(delta_time)

            # add missing obstacles
            while len(self.obstacle_list) < self.number_of_obstacles:
                self.obstacle_list.append(Obstacle(speed=self.obstacle_speed, type=random.randint(1, 3), spawn_on_edge=True))

            # Update the player shots
            for o in self.obstacle_list:
                o.on_update(delta_time)

            self.level_timer -= delta_time

            if self.level_timer <= 0:
                self.new_level()

            if self.obstacle_speed > Obstacle.obstacle_max_speed:
                self.obstacle_speed = Obstacle.obstacle_max_speed

            # score system: time = more score
            self.player_sprite.score += int((10.0 * delta_time) * 10)

            if self.player_sprite.player_lives < 1:
                print("your final score is", int(self.player_sprite.score * 10))
                #exit(0)
                self.set_mode("DEATH_SCREEN")
                self.player_sprite.player_lives = 5
                #self.player_sprite.score = 0
                self.current_level = 0
                if self.mode == "DEATH_SCREEN":
                    """
                    arcade.draw_text(
                        "{}".format("your final score is", int(self.player_score * 10)),  # Text to show
                        SCREEN_WIDTH / 2 - 375,  # X position
                        SCREEN_HEIGHT / 2 - 200,  # Y positon
                        arcade.color.WHITE,  # Color of text
                        30
                    )
                    """
        else:
            pass

    def on_key_press(self, key, modifiers):
        """
        Called whenever a key is pressed.
        """

        # Track state of arrow keys
        if key == arcade.key.UP:
            self.up_pressed = True
        elif key == arcade.key.DOWN:
            self.down_pressed = True
        elif key == arcade.key.LEFT:
            self.left_pressed = True
        elif key == arcade.key.RIGHT:
            self.right_pressed = True

        if self.mode == "IN_GAME":
            if key == DASHING_KEY:
                self.player_sprite.dash()

        print("Key pressed:", key)

        if self.mode == "IN_START_SCREEN":
            if key == arcade.key.SPACE:
                self.set_mode("IN_GAME")

        elif self.mode == "IN_GAME":
            if key == DASHING_KEY:
                self.player_sprite.dash()

        elif self.mode == "DEATH_SCREEN":
            if key == arcade.key.SPACE:
                self.set_mode("IN_START_SCREEN")

        else:
            exit("you a failure you no mean to exist")


        print(self.mode)

    def on_key_release(self, key, modifiers):
        """
        Called whenever a key is released.
        """

        if key == arcade.key.UP:
            self.up_pressed = False
        elif key == arcade.key.DOWN:
            self.down_pressed = False
        elif key == arcade.key.LEFT:
            self.left_pressed = False
        elif key == arcade.key.RIGHT:
            self.right_pressed = False

    def on_joybutton_press(self, joystick, button_no):
        # print("Button pressed:", button_no)
        # Press the fire key
        self.on_key_press(DASHING_KEY, [])
        pass
    def on_joybutton_release(self, joystick, button_no):
        # print("Button released:", button_no)
        pass
    def on_joyaxis_motion(self, joystick, axis, value):
        print("Joystick axis {}, value {}".format(axis, value))


    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        # print("Joystick hat ({}, {})".format(hat_x, hat_y))
        pass


def main():
    """
    Main method
    """

    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()