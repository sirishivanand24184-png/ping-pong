import pygame
from game.game_engine import GameEngine

pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()
FPS = 60

engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True

    while running:
        SCREEN.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        engine.handle_input()
        engine.update()
        engine.render(SCREEN)

        winner = engine.check_game_over()
        if winner:
            # Display winner message
            font = pygame.font.SysFont("Arial", 50)
            text = font.render(f"{winner} Wins!", True, WHITE)
            rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
            SCREEN.blit(text, rect)
            pygame.display.flip()
            pygame.time.delay(1000)

            # Show replay menu
            new_score = engine.replay_menu(SCREEN)
            if new_score is None:
                running = False
            else:
                engine.winning_score = new_score
                engine.reset_game()
                continue

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
