import pygame
from .paddle import Paddle
from .ball import Ball

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

        self.winning_score = 5  # default winning score

        # Initialize mixer and load sounds
        pygame.mixer.init()
        self.snd_paddle = pygame.mixer.Sound("game/sounds/c526-ff1d-45cc-b5b1-96cffef61635.wav")
        self.snd_wall = pygame.mixer.Sound("game/sounds/125d-3ee9-45d0-a829-ddd13acf2636.wav")
        self.snd_score = pygame.mixer.Sound("game/sounds/f488-6425-4a09-a991-f37628fcb262.wav")

        # Link ball to engine for playing sounds
        self.ball.game_engine = self

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player.move(-10, self.height)
        if keys[pygame.K_s]:
            self.player.move(10, self.height)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)

        # Score logic
        if self.ball.x <= 0:
            self.ai_score += 1
            self.snd_score.play()
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.snd_score.play()
            self.ball.reset()

        self.ai.auto_track(self.ball, self.height)

    def render(self, screen):
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

    def check_game_over(self):
        if self.player_score >= self.winning_score:
            return "Player"
        elif self.ai_score >= self.winning_score:
            return "AI"
        return None

    def replay_menu(self, screen):
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

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        return 2
                    elif event.key == pygame.K_5:
                        return 3
                    elif event.key == pygame.K_7:
                        return 4
                    elif event.key == pygame.K_ESCAPE:
                        return None

    def reset_game(self):
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2
