import pygame

SCREEN_WIDTH = 400
SCREEN_HEIGHT  = 500

pygame.init()

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("pygame sound test")

clock = pygame.time.Clock()

pygame.mixer.music.load('음악.ogg')

playing = True
while playing:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            playing = False
            pygame.quit()

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_UP:
                pygame.mixer.music.play(-1)
                print("Play")

            if event.key == pygame.K_DOWN:
                pygame.mixer.music.stop()
                print("Stop")

    clock.tick(60)
