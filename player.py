import pygame
import os
from settings import PLAYER_WIDTH, PLAYER_HEIGHT, GRAVITY
from action import move, attack


class Player:
    def __init__(self, x, y, color, image_folder, added_height=0):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT + added_height)  # Collision box
        self.color = color
        self.velocity_y = 0
        self.is_jumping = False
        self.jump_count = 0
        self.jump_released = True
        self.health = 100
        self.on_platform = False
        self.current_frame = 0  # Tracks the current animation frame
        self.animation_timer = 0  # Tracks time between animation frames
        self.attack_animation_timer = 0  # Tracks time specifically for the attack animation
        self.state = "idle"  # Default state: 'idle', 'run', 'jump', 'attack', etc.
        self.flip = False  # Whether the image should be flipped horizontally
        self.last_attack_time = 0  # Tracks the last time the player attacked (for cooldown)
        self.is_defending = False

        # Load all animations
        self.animations = self.load_animations(image_folder)

    def load_animations(self, folder):
        """Load all animations from the specified folder."""
        animations = {
            "idle": [pygame.image.load(os.path.join(folder, "default.png"))],
            "run": [pygame.image.load(os.path.join(folder, "runAnimation", f"run{i}.png")) for i in range(1, 9)],
            "jump": [pygame.image.load(os.path.join(folder, "jumpAnimation", f"jump{i}.png")) for i in range(1, 8)],
            "attack": [pygame.image.load(os.path.join(folder, "attack", f"attack{i}.png")) for i in range(1, 4)],
            "defend": [pygame.image.load(os.path.join(folder, "protect", f"protect{i}.png")) for i in range(1, 3)],
        }

        # Scale all images to match PLAYER_WIDTH and PLAYER_HEIGHT
        for key, frames in animations.items():
            animations[key] = [pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT)) for frame in frames]

        return animations

    def update_animation(self, fps=60):
        """Update the player's animation frame based on the current state."""
        # Ensure the current state exists in animations; fallback to 'idle' if not
        if self.state not in self.animations:
            self.state = "idle"

        # Ensure there are frames to cycle through
        if len(self.animations[self.state]) == 0:
            return

        # Frames per animation update (controls animation speed)
        frames_per_update = fps // 15  # Default animation speed for all states except attack
        attack_frames_per_update = fps // 4  # Slower animation for attack

        # Handle attack animation
        if self.state == "attack":
            self.attack_animation_timer += 1
            if self.attack_animation_timer >= attack_frames_per_update:
                previous_frame = self.current_frame
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])  # Cycle through frames
                self.attack_animation_timer = 0  # Reset the attack animation timer

                # Handle attack animation finishing
                if self.current_frame == len(self.animations[self.state]) - 1:  # Last frame of attack animation
                    keys = pygame.key.get_pressed()  # Check current movement keys
                    if keys[pygame.K_a] or keys[pygame.K_d]:  # Player is moving
                        self.state = "run"
                    else:  # Player is stationary
                        self.state = "idle"
                    self.current_frame = 0  # Reset animation frame for new state
        elif self.state == "defend":
            self.current_frame = min(self.current_frame + 1, len(self.animations[self.state]) - 1)  # Freeze on last frame
        # Handle jump animation
        elif self.state == "jump":
            self.animation_timer += 1
            if self.animation_timer >= frames_per_update:
                previous_frame = self.current_frame

                # Upward movement (frames 1-3)
                if self.velocity_y < 0:  # Player is moving up
                    if self.current_frame < 3:  # Progress through frames 1, 2, and 3
                        self.current_frame += 1
                    else:  # Stay on frame 3 until the velocity becomes positive
                        self.current_frame = 3

                # Downward movement (frames 4-5)
                elif self.velocity_y > 0:  # Player is moving down
                    if self.current_frame < 4:  # Jump directly to frame 4 for downward motion
                        self.current_frame = 4
                    elif self.current_frame < 5:  # Play frame 5 after frame 4
                        self.current_frame += 1

                self.animation_timer = 0  # Reset the timer

        # Standard animation for all other states
        else:
            self.animation_timer += 1
            if self.animation_timer >= frames_per_update:
                previous_frame = self.current_frame
                self.current_frame = (self.current_frame + 1) % len(self.animations[self.state])  # Cycle through frames
                self.animation_timer = 0  # Reset the timer

    def move(self, keys, left_key, right_key, jump_key, defend_key):
        """Delegate movement logic to `action.move`."""
        move(self, keys, left_key, right_key, jump_key, defend_key)

    def attack(self, opponent):
        """Delegate attack logic to `action.attack`."""
        attack(self, opponent)

    def apply_gravity(self):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

    def check_collision_with_platforms(self, platforms):
        """Check for collision with platforms and handle landing."""
        self.on_platform = False
        for platform in platforms:
            # Check if the player lands on a platform
            if self.rect.colliderect(platform) and self.velocity_y >= 0:
                if abs(self.rect.bottom - platform.top) <= max(10, abs(self.velocity_y)):
                    # Snap the player to the platform
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.is_jumping = False
                    self.on_platform = True
                    self.jump_count = 0  # Reset double jump count

                    # Update the state ONLY if landing after a jump
                    if self.state == "jump":
                        if not (keys := pygame.key.get_pressed())[pygame.K_a] and not keys[pygame.K_d]:
                            new_state = "idle"
                        else:
                            new_state = "run"

                        # Only reset the animation frame if the state actually changes
                        if self.state != new_state:
                            print(f"State changed from {self.state} to {new_state} after landing.")
                            self.state = new_state
                            self.current_frame = 0

                    break

    def draw(self, screen):
        """Render the current frame of the player's animation."""
        if self.state not in self.animations:
            self.state = "idle"

        frame = self.animations[self.state][self.current_frame]
        if self.flip:
            frame = pygame.transform.flip(frame, True, False)  # Flip horizontally if needed

        # Draw the current animation frame
        screen.blit(frame, (self.rect.x, self.rect.y))

    def draw_health_bar(self, screen, x, y, border_color=(0, 0, 0), bg_color=(255, 0, 0), fg_color=(0, 255, 0)):
        """
        Draws an improved, larger health bar with a border, background, and foreground.

        Args:
            screen: Pygame surface to draw on.
            x: X-coordinate of the health bar.
            y: Y-coordinate of the health bar.
            border_color: Color of the border (default black).
            bg_color: Background color for the health bar (default red).
            fg_color: Foreground color for the health bar (default green).
        """
        bar_width = 300  # Bigger width for the health bar
        bar_height = 40  # Bigger height for the health bar
        border_thickness = 5  # Thicker border

        # Draw the border
        pygame.draw.rect(screen, border_color, (x - border_thickness, y - border_thickness, 
                                                bar_width + 2 * border_thickness, bar_height + 2 * border_thickness))

        # Draw the background (red part)
        pygame.draw.rect(screen, bg_color, (x, y, bar_width, bar_height))

        # Calculate current health width
        current_health_width = max(0, (self.health / 100) * bar_width)

        # Draw the foreground (green part)
        pygame.draw.rect(screen, fg_color, (x, y, current_health_width, bar_height))

        # Add health percentage text
        font = pygame.font.SysFont("Arial", 28, bold=True)  # Bigger, bold font
        health_text = font.render(f"{self.health:.0f}/100", True, (255, 255, 255))  # White text
        screen.blit(health_text, (x + bar_width // 2 - health_text.get_width() // 2, y + bar_height // 2 - health_text.get_height() // 2))
