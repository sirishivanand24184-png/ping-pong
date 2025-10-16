import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)

        self.winning_score = 5  # Default winning score

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        # Move the ball
        self.ball.move()

        # Check collisions with paddles
        self.ball.check_collision(self.player, self.ai)

        # Check for scoring
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()

        # AI movement
        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        # Draw paddles and ball
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self, screen):
        """
        Checks if either player or AI reached the winning score.
        Returns True if game is over, else False.
        """
        font = pygame.font.SysFont("Arial", 50)
        message = None

        if self.player_score >= self.winning_score:
            message = "Player Wins!"
        elif self.ai_score >= self.winning_score:
            message = "AI Wins!"

        if message:
            # Draw message
            text = font.render(message, True, WHITE)
            text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
            screen.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.delay(2000)  # Pause so player sees message
            return True  # Game over

        return False  # Continue game

    def replay_menu(self, screen):
        """
        Displays replay options and waits for user input.
        Returns the new winning score or None if exiting.
        """
        font = pygame.font.SysFont("Arial", 40)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]

        screen.fill((0, 0, 0))
        for i, text_option in enumerate(options):
            text = font.render(text_option, True, WHITE)
            rect = text.get_rect(center=(self.width // 2, 150 + i*60))
            screen.blit(text, rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        return 2  # Best of 3 → 2 wins
                    elif event.key == pygame.K_5:
                        return 3  # Best of 5 → 3 wins
                    elif event.key == pygame.K_7:
                        return 4  # Best of 7 → 4 wins
                    elif event.key == pygame.K_ESCAPE:
                        return None

    def reset_game(self):
        """Reset scores and ball for a new round"""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
