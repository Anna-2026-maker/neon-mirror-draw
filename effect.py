"""Reference Python implementation for mirrored neon drawing."""
import math, random, pygame

pygame.init()
screen = pygame.display.set_mode((1100, 760))
layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
clock = pygame.time.Clock()
paths, particles = [], []
mirror_enabled, drawing = True, False

def mirror(point):
    return screen.get_width() - point[0], point[1]

def emit(point, count=12):
    for _ in range(count):
        angle, speed = random.random()*math.tau, random.uniform(.5, 3)
        particles.append([*point, math.cos(angle)*speed, math.sin(angle)*speed, 50])

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m: mirror_enabled = not mirror_enabled
        if event.type == pygame.MOUSEBUTTONDOWN: drawing = True; paths.append([])
        if event.type == pygame.MOUSEBUTTONUP: drawing = False; emit(pygame.mouse.get_pos(), 60)
    if drawing:
        point = pygame.mouse.get_pos(); paths[-1].append(point); emit(point, 4)
    layer.fill((0, 0, 0, 0))
    for path in paths:
        if len(path)>1:
            pygame.draw.lines(layer, (255,35,174,220), False, path, 5)
            if mirror_enabled: pygame.draw.lines(layer, (255,35,174,220), False, [mirror(p) for p in path], 5)
    for p in particles:
        p[0]+=p[2]; p[1]+=p[3]; p[4]-=1
        pygame.draw.circle(layer,(255,55,190,max(0,p[4]*5)),(int(p[0]),int(p[1])),2)
    particles[:]=[p for p in particles if p[4]>0]
    screen.fill((3,2,4)); screen.blit(layer,(0,0)); pygame.display.flip(); clock.tick(60)
pygame.quit()
