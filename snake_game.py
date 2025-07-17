import pygame
import random
import sys

pygame.init()

# Screen setup
width, height = 600, 600
game_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = game_screen.get_size()  # Update width and height based on full screen
pygame.display.set_caption("Snack Attack! 🐍🍎")  # 🎉 Fun title
clock = pygame.time.Clock()

# Colors
GREEN = (0, 200, 0)
BLACKISH = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (180, 180, 180)

# Fonts
font = pygame.font.SysFont("arial", 35)
big_font = pygame.font.SysFont("arial", 50)

# Snake setup
snake_size = 20
snake_speed = 10
snake_x, snake_y = width // 2, height // 2
change_x, change_y = 0, 0
snake_body = [(snake_x, snake_y)]

# Food setup
food_x = random.randrange(0, width - snake_size, snake_size)
food_y = random.randrange(0, height - snake_size, snake_size)

# Score
score = 0

# Difficulty selector
def select_difficulty():
    global snake_speed
    selecting = True
    while selecting:
        game_screen.fill(GREEN)
        #  Show welcome text
        title_font = pygame.font.SysFont("arial", 50, bold=True)
        title_text = title_font.render("WELCOME TO SNACK ATTACK!", True, (0, 0, 0))
        game_screen.blit(title_text, (width // 2 - title_text.get_width() // 2, 40))
        title = big_font.render("Choose Difficulty", True, BLACKISH)
        easy = font.render("1. Easy", True, BLACKISH)
        medium = font.render("2. Medium", True, BLACKISH)
        hard = font.render("3. Hard", True, BLACKISH)
        game_screen.blit(title, (width // 2 - title.get_width() // 2, 100))
        game_screen.blit(easy, (width // 2 - easy.get_width() // 2, 200))
        game_screen.blit(medium, (width // 2 - medium.get_width() // 2, 260))
        game_screen.blit(hard, (width // 2 - hard.get_width() // 2, 320))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    snake_speed = 5
                    selecting = False
                elif event.key == pygame.K_2:
                    snake_speed = 10
                    selecting = False
                elif event.key == pygame.K_3:
                    snake_speed = 16
                    selecting = False

# Game over screen
def game_over():
    global snake_body, snake_x, snake_y, change_x, change_y, score
    over = True
    while over:
        game_screen.fill(GREEN)
        over_text = big_font.render("Game Over!", True, RED)
        retry_text = font.render("Press R to Restart or Q to Quit", True, BLACKISH)
        game_screen.blit(over_text, (width // 2 - over_text.get_width() // 2, 200))
        game_screen.blit(retry_text, (width // 2 - retry_text.get_width() // 2, 280))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset everything
                    snake_x, snake_y = width // 2, height // 2
                    change_x, change_y = 0, 0
                    snake_body = [(snake_x, snake_y)]
                    score = 0
                    return
                elif event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

# Main game loop
def main():
    global snake_x, snake_y, change_x, change_y, snake_body, food_x, food_y, score

    select_difficulty()

    running = True
    while running:
        clock.tick(snake_speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and change_x == 0:
                    change_x = -snake_size
                    change_y = 0
                elif event.key == pygame.K_RIGHT and change_x == 0:
                    change_x = snake_size
                    change_y = 0
                elif event.key == pygame.K_UP and change_y == 0:
                    change_x = 0
                    change_y = -snake_size
                elif event.key == pygame.K_DOWN and change_y == 0:
                    change_x = 0
                    change_y = snake_size

        snake_x += change_x
        snake_y += change_y

        # Wall collision wrap-around
        snake_x %= width
        snake_y %= height

        # Add new head
        snake_body.append((snake_x, snake_y))
        
        # Check food collision
        if abs(snake_x - food_x) < snake_size and abs(snake_y - food_y) < snake_size:
            food_x = random.randrange(0, width - snake_size, snake_size)
            food_y = random.randrange(0, height - snake_size, snake_size)
            score += 1
        else:
            del snake_body[0]  # Keep length same unless food eaten

        # Check self collision
        if (snake_x, snake_y) in snake_body[:-1]:
            game_over()

        # Draw
        game_screen.fill(GREEN)

        # Draw food
        pygame.draw.ellipse(game_screen, RED, [food_x, food_y, snake_size, snake_size])

        # Draw snake
        for i in range(len(snake_body)):
            color = WHITE if i == len(snake_body) - 1 else BLACKISH
            x, y = snake_body[i]
            pygame.draw.ellipse(game_screen, color, [x, y, snake_size, snake_size])

        # Score
        score_text = font.render(f"Score: {score}", True, BLACKISH)
        game_screen.blit(score_text, (10, 10))

        pygame.display.update()

    pygame.quit()

main()
