import pygame
from settings import PLAYER_SPEED, JUMP_STRENGTH, ATTACK_DAMAGE

def move(player, keys, left_key, right_key, jump_key, defend_key):
    """Handle player movement."""
    previous_state = player.state  # Track the previous state for resetting the animation
    is_moving = False  # Track whether the player is currently moving horizontally

    # Handle defending
    if keys[defend_key]:
        if player.state != "defend":
            print(f"Player started defending at position {player.rect.x}, {player.rect.y}")
        player.state = "defend"
        player.is_defending = True
        if not player.is_jumping:
            return
    else:
        if player.state == "defend":
            print(f"Player stopped defending at position {player.rect.x}, {player.rect.y}")
            player.state = "idle"
            player.is_defending = False

    # Prevent movement if attacking
    if player.state == "attack" and not player.is_jumping:
        return

    # Horizontal movement
    if keys[left_key]:  # Move left
        player.rect.x -= PLAYER_SPEED
        player.flip = True
        is_moving = True
    elif keys[right_key]:  # Move right
        player.rect.x += PLAYER_SPEED
        player.flip = False
        is_moving = True

    # Set state to "run" only if it's not already "run"
    if is_moving and not player.is_jumping and player.state != "run" and player.state != "attack" and player.state != "defend": 
        player.state = "run"

    # Jumping
    if keys[jump_key]:
        if player.jump_released and player.jump_count < 2:  # Allow double jumps
            player.velocity_y = JUMP_STRENGTH
            player.is_jumping = True
            player.jump_count += 1
            player.jump_released = False
            if player.state != "jump":
                player.state = "jump"  # Lock state to jump while in the air

    # Check if the jump key has been released
    if not keys[jump_key]:
        player.jump_released = True

    # Only transition to "idle" if player has completely stopped moving
    if not is_moving and not player.is_jumping and player.state not in ["idle", "attack", "defend"]:
        player.state = "idle"

    # Reset animation frame ONLY if the state changes
    if player.state != previous_state:
        player.current_frame = 0  # Reset animation frame only on actual state change


def attack(player, opponent):
    """Handle the player's attack and ensure proper conditions are met."""
    current_time = pygame.time.get_ticks()  # Get the current time in milliseconds
    cooldown_time = 500  # Attack cooldown time in milliseconds (adjust as needed)

    # Only allow attacking if the cooldown has expired
    if current_time - player.last_attack_time >= cooldown_time:
        # Check if player is facing the opponent and touching them
        if player.rect.colliderect(opponent.rect):  # Check for collision
            print(f"Collision detected: Player at {player.rect}, Opponent at {opponent.rect}")
            print(f"Player flip status: {player.flip} (True means facing left, False means facing right)")

            # Check if the player is facing the opponent
            if player.flip and opponent.rect.centerx < player.rect.centerx:  # Player facing left, opponent to the left
                if opponent.is_defending:  # Opponent is defending
                    if not opponent.flip:  # Opponent is facing left (towards the attacker)
                        print("Opponent is defending and facing the attacker. No damage dealt.")
                    else:  # Opponent is facing right (away from the attacker)
                        print("Opponent is defending but facing away from the attacker. Dealing damage.")
                        opponent.health -= ATTACK_DAMAGE
                        print(f"Player attacked opponent! Opponent's health: {opponent.health}")
                else:  # Opponent is not defending
                    print("Player is facing left and opponent is to the left. Dealing damage.")
                    opponent.health -= ATTACK_DAMAGE
                    print(f"Player attacked opponent! Opponent's health: {opponent.health}")
            elif not player.flip and opponent.rect.centerx > player.rect.centerx:  # Player facing right, opponent to the right
                if opponent.is_defending:  # Opponent is defending
                    if opponent.flip:  # Opponent is facing right (towards the attacker)
                        print("Opponent is defending and facing the attacker. No damage dealt.")
                    else:  # Opponent is facing left (away from the attacker)
                        print("Opponent is defending but facing away from the attacker. Dealing damage.")
                        opponent.health -= ATTACK_DAMAGE
                        print(f"Player attacked opponent! Opponent's health: {opponent.health}")
                else:  # Opponent is not defending
                    print("Player is facing right and opponent is to the right. Dealing damage.")
                    opponent.health -= ATTACK_DAMAGE
                    print(f"Player attacked opponent! Opponent's health: {opponent.health}")
            else:  # Player is not facing the opponent
                print("Player is NOT facing the opponent. No damage dealt.")
        else:
            print(f"No collision detected: Player at {player.rect}, Opponent at {opponent.rect}")

        player.state = "attack"  # Lock state to attack
        player.current_frame = 0  # Reset animation to start of attack
        player.last_attack_time = current_time  # Update the last attack time
    else:
        remaining_cooldown = cooldown_time - (current_time - player.last_attack_time)
