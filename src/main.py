import asyncio
import pygame
from settings import WIDTH,HEIGHT,PIPE_SPAWN,POPULATION_SIZE,MAX_SPEEDUP,START_X as BIRD_X
from bird import Bird
from pipe import Pipe
from genalg import next_gen

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.Font(None, 40)
clock = pygame.time.Clock()

loops = 1
best_score = 0
generation = 1
birds = [Bird() for _ in range(POPULATION_SIZE)]
saved_birds = []
pipes = [Pipe()]

def get_next_pipe():
    for pipe in pipes:
        if (pipe.x > BIRD_X):
            return pipe
    return pipes[0] if len(pipes) > 0 else None


def add_pipe():
    if (len(pipes) > 0):
        p = pipes[-1]
        if (p.x <= PIPE_SPAWN):
            pipes.append(Pipe())

def export_data():
    print("not implemented yet")


async def main():
    global loops, best_score, generation, birds, saved_birds, pipes, running

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    loops *= 2
                    loops = min(MAX_SPEEDUP,loops)
                elif event.key == pygame.K_LEFT:
                    loops = int(loops/2)
                    loops = max(1,loops)
                elif event.key == pygame.K_RETURN:
                    export_data()
        
        #loops = 5 if superspeed else 1
        for i in range(loops):
            target_pipe = get_next_pipe()

            for bird in birds[:]:
                bird.think(target_pipe)
                bird.update(target_pipe)
                if (bird.check_lose(pipes)):
                    saved_birds.append(bird)
                    birds.remove(bird)

            for pipe in pipes[:]:
                pipe.update()

                if not pipe.scored and pipe.x < BIRD_X:
                    pipe.scored = True
                    for bird in birds:
                        bird.score += 1
                        bird.fitness += 500
                if (pipe.top.right < 0):
                    pipes.remove(pipe)

            add_pipe()

            if (len(birds) == 0):
                pipes = [Pipe()]
                birds = next_gen(saved_birds)
                saved_birds = []
                generation += 1

        screen.fill((167, 200, 255))
        for pipe in pipes:
            pipe.show(screen)
        for bird in birds:
            bird.show(screen)
        
        best_score = max(best_score,birds[0].score)
        info_surf = font.render(f"Gen: {generation}, Alive: {len(birds)}, Score: {birds[0].score} \nBest Score: {best_score}, {loops}x speed", True, (255,255,255))
        screen.blit(info_surf, (20,20))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())
