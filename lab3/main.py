import pygame
from pygame.locals import *
import random
from queue import PriorityQueue

width = 900
height = 700

width, height = 1280, 980

gravity = 10
gravity = 20

filetoparse = "xi - ANiMA (Kuo Kyoka) [4K Lv.4].osu"
filetoparse = "xi - ANiMA (Kuo Kyoka) [Kyou's 4K Lv.9].osu"

FPS = 60

# time in milliseconds
TIME = 0

SCORE = 0

priorityQDummy = 0

x1, x2, x3, x4 = 100, 200 + 14, 300 + 28, 400 + 42
start_y = 0

receptor_y = height -200
receptor_x_offset = 14

# meassured in frames
framesToHitBottom = ( receptor_y - start_y ) / gravity

# meassured in milliseconds
timeToHitBottom = framesToHitBottom * 1000 / FPS

sky_blue = (135, 206, 235)

screen = pygame.display.set_mode((width, height))

left_arrow = pygame.image.load("left.png")
right_arrow = pygame.image.load("right.png")
up_arrow = pygame.image.load("up.png")
down_arrow = pygame.image.load("down.png")

evaluation_0 = pygame.image.load("mania-hit0@2x.png")
evaluation_100 = pygame.image.load("mania-hit100@2x.png")
evaluation_200 = pygame.image.load("mania-hit200@2x.png")
evaluation_300 = pygame.image.load("mania-hit300@2x.png")

class LeftArrow(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = left_arrow
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

class RightArrow(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = right_arrow
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

class UpArrow(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = up_arrow
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

class DownArrow(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = down_arrow
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

class LeftReceptor(pygame.sprite.Sprite):
    def __init__(self, screen, pos=(x1 + receptor_x_offset, receptor_y)):
        super().__init__()
        
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = pygame.image.load("leftReceptor.png")
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

class RightReceptor(pygame.sprite.Sprite):
    def __init__(self, screen, pos=(x2 + receptor_x_offset, receptor_y)):
        super().__init__()
        
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = pygame.image.load("rightReceptor.png")
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

class UpReceptor(pygame.sprite.Sprite):
    def __init__(self, screen, pos=(x3 + receptor_x_offset, receptor_y)):
        super().__init__()
        
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = pygame.image.load("upReceptor.png")
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

class DownReceptor(pygame.sprite.Sprite):
    def __init__(self, screen, pos=(x4 + receptor_x_offset, receptor_y)):
        super().__init__()
        
        self.screen = screen
        self.image = pygame.Surface((45, 30), pygame.SRCALPHA)
        self.present_img = pygame.image.load("downReceptor.png")
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0]
        self.pos_y = pos[1]

class Evaluation(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((0,0), pygame.SRCALPHA)
        self.present_img = pygame.image.load("mania-hit0@2x.png")
        self.rect = self.image.get_rect(center=(x1 + x2  //2, height // 2))
        self.pos_x = x1 + x2  //2
        self.pos_y = height // 2

particle_image = pygame.image.load("particle.png")

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, screen):
        super().__init__()
        self.screen = screen
        self.image = pygame.Surface((0,0), pygame.SRCALPHA)
        self.present_img = particle_image
        # downscale image
        self.present_img = pygame.transform.scale(self.present_img, (75, 75))
        self.rect = self.image.get_rect(center=pos)
        self.pos_x = pos[0] + 20
        self.pos_y = pos[1] + 25
        self.vel_x = random.randint(-10, 10)
        self.vel_y = random.randint(-10, 10)
        self.lifetime = 30
        
def parseOsuFile(filename):
    global priorityQDummy
    with open(filename, "r") as f:
        lines = f.readlines()
        
        # find index of "[HitObjects]" line
        for i, line in enumerate(lines):
            if line == "[HitObjects]\n":
                break

        # parse hit objects
        hit_objects = lines[i+1:]
        hit_objects = [obj.split(",") for obj in hit_objects]
        #               x           y           time           type         hit_sound    endTime:hitSample
        hit_objects = [(int(obj[0]), int(obj[1]), int(obj[2]), int(obj[3]), int(obj[4]), int(obj[5].split(":")[0])) for obj in hit_objects]
        hit_obj_dicts = list()
        for obj in hit_objects:
            hit_obj_dict = dict()
            hit_obj_dict.update({
                "x": obj[0],
                "y": obj[1],
                "time": obj[2],
                "type": obj[3],
                "hit_sound": obj[4],
                "endTime": obj[5]
            })
            hit_obj_dicts.append(hit_obj_dict)
        
        hoq = PriorityQueue()
        
        
        for obj in hit_obj_dicts:
            priorityQDummy += 1
            hoq.put((obj["time"], priorityQDummy, obj))

        return hoq

def updateTime():
    global TIME
    
    # add 1 frame in milliseconds
    TIME += 1000 / FPS

def updateArrow(arrows):
    for arrow in arrows:
        arrow.pos_y += gravity
        arrow.rect.center = (arrow.pos_x, arrow.pos_y)

def initArrow(pos=(100, 100), type="left"):
    if type == "left":
        return LeftArrow(pos, screen)
    elif type == "right":
        return RightArrow(pos, screen)
    elif type == "up":
        return UpArrow(pos, screen)
    elif type == "down":
        return DownArrow(pos, screen)

def drawArrow(arrows):
    for arrow in arrows:
        screen.blit(arrow.present_img, arrow.rect)

def spawnArrows(arrows, hoq):
    global priorityQDummy
    if hoq.empty():
        return

    gets = (hoq.get(), hoq.get(), hoq.get(), hoq.get())
    
    for gotten in gets:
        
        next_obj = gotten[2]
        next_obj_time = next_obj["time"]

        if next_obj_time <= TIME:
            if next_obj["x"] == 64:
                arrows.append(initArrow((x1, start_y), "left"))
            if next_obj["x"] == 192:
                arrows.append(initArrow((x2, start_y), "right"))
            if next_obj["x"] == 320:
                arrows.append(initArrow((x3, start_y), "up"))
            if next_obj["x"] == 448:
                arrows.append(initArrow((x4, start_y), "down"))

        else:
            priorityQDummy += 1
            hoq.put((next_obj_time, priorityQDummy, next_obj))

def despawnArrows(arrows):
    for arrow in arrows:
        if arrow.pos_y > height:
            arrows.remove(arrow)

def drawReceptors(receptors):
    for receptor in receptors:
        screen.blit(receptor.present_img, receptor.rect)

def evaluateHit(arrows, receptor_hit, evaluation):
    for arrow in arrows:
        if arrow.pos_x == x1 and receptor_hit == 0 \
        or arrow.pos_x == x2 and receptor_hit == 1 \
        or arrow.pos_x == x3 and receptor_hit == 2 \
        or arrow.pos_x == x4 and receptor_hit == 3:
            distance = abs(arrow.pos_y - receptor_y)
            global SCORE
            if distance < 50:
                SCORE += 300
                evaluation.present_img = evaluation_300
            elif distance < 100:
                SCORE += 200
                evaluation.present_img = evaluation_200
            elif distance < 150:
                SCORE += 100
                evaluation.present_img = evaluation_100
            else:
                SCORE += 0
                evaluation.present_img = evaluation_0


            arrows.remove(arrow)
            break

def updateParticles(particles):
    for particle in particles:
        # downscale image
        particle.present_img = pygame.transform.scale(particle.present_img, (particle.lifetime, particle.lifetime))
        particle.pos_x += particle.vel_x
        particle.pos_y += particle.vel_y
        particle.vel_x *= 0.9
        particle.vel_y *= 0.9
        particle.rect.center = (particle.pos_x, particle.pos_y)
        particle.lifetime -= 1
        if particle.lifetime <= 0:
            particles.remove(particle)

def spawnParticles(particles, pos):
    for i in range(10):
        particles.append(Particle(pos, screen))

def keyPress(key, receptors, arrows, evaluation, particles):
    # keys: "y", "x", ",", "."
    if key == "y":
        evaluateHit(arrows, 0, evaluation)
        spawnParticles(particles, (x1, receptor_y))
    elif key == "x":
        evaluateHit(arrows, 1, evaluation)
        spawnParticles(particles, (x2, receptor_y))
    elif key == ",":
        evaluateHit(arrows, 2, evaluation)
        spawnParticles(particles, (x3, receptor_y))
    elif key == ".":
        evaluateHit(arrows, 3, evaluation)
        spawnParticles(particles, (x4, receptor_y))
    
def keyRelease(key, receptors):
    pass

def drawScore(text_score, text_rect_score):
    screen.blit(text_score, text_rect_score)
    
def drawEvaluation(evaluation):
    screen.blit(evaluation.present_img, evaluation.rect)

def drawParticles(particles):
    for particle in particles:
        screen.blit(particle.present_img, particle.rect)

def main():

    pygame.init()
    pygame.display.set_caption("Mania")
    clock = pygame.time.Clock()
    running = True

    MUSICSTART = pygame.USEREVENT + 1
    pygame.time.set_timer(MUSICSTART, int(timeToHitBottom) - 200)
    pygame.mixer.music.load('anima.mp3')

    arrows = list()
    arrows.append(initArrow((x1, 100), "left"))
    arrows.append(initArrow((x2, 100), "right"))
    arrows.append(initArrow((x3, 100), "up"))
    arrows.append(initArrow((x4, 100), "down")) 

    receptors = (LeftReceptor(screen), RightReceptor(screen), UpReceptor(screen), DownReceptor(screen))

    hoq = parseOsuFile(filetoparse)
    # hoq = parseOsuFile()

    evaluation = Evaluation(screen)

    particles = list()

    while running:
        # set background color to sky blue
        screen.fill(sky_blue)
        clock.tick(60)
        updateTime()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == MUSICSTART:
                print("music start")
                pygame.mixer.music.play(-1)
                pygame.time.set_timer(MUSICSTART, 0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    keyPress("y", receptors, arrows, evaluation, particles)
                elif event.key == pygame.K_x:
                    keyPress("x", receptors, arrows, evaluation, particles)
                elif event.key == pygame.K_COMMA:
                    keyPress(",", receptors, arrows, evaluation, particles)
                elif event.key == pygame.K_PERIOD:
                    keyPress(".", receptors, arrows, evaluation, particles)
        
        font = pygame.font.Font('freesansbold.ttf', 32)
        text_score = font.render(f'Score: {SCORE}', True, (0, 0, 0))
        text_rect_score = text_score.get_rect()
        text_rect_score.center = (width // 2 + 100, 25)
        drawScore(text_score, text_rect_score)

        drawEvaluation(evaluation)

        spawnArrows(arrows, hoq)
        despawnArrows(arrows)
        updateArrow(arrows)
        drawArrow(arrows)

        updateParticles(particles)
        drawParticles(particles)

        drawReceptors(receptors)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()