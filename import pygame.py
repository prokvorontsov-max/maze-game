import pygame
pygame.init()

#class game
class Sprite:
    def __init__(self, x, y,img, w=24, h=24):
        self.img = pygame.image.load(img)
        self.rect = pygame.Rect(x, y, w, h)

    def draw(self, surface):
        surface.blit(self.img, (self.rect.x, self.rect.y))
        
        
    def collide_list(self, list_obj):
        for obj in list_obj:
            if self.rect.colliderect(obj.rect):
                return True
        return False

class Player(Sprite):
    def __init__(self, x, y, img):
        super().__init__(x, y, img)
        self.keys = 0
        self.hp = 5
        self.anim = 0

    def move(self):
        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT]:
            self.img = pygame.image.load("hero_l.png")
            self.anim += 1
            self.rect.x -= 4
            if self.collide_list(maze) or self.collide_list(doors) and self.keys == 0:
                self.rect.x += 4
        if key[pygame.K_RIGHT]:
            self.img = pygame.image.load("hero_r.png")
            self.anim += 1
            self.rect.x += 4
            if self.collide_list(maze) or self.collide_list(doors) and self.keys == 0:
                self.rect.x -= 4
        if key[pygame.K_UP]:
            self.img = pygame.image.load("hero_up_down.png")
            self.anim += 1
            self.rect.y -= 4
            if self.collide_list(maze) or self.collide_list(doors) and self.keys == 0:
                self.rect.y += 4
        if key[pygame.K_DOWN]:
            self.img = pygame.image.load("hero_up_down.png")
            self.anim += 1
            self.rect.y += 4
            if self.collide_list(maze) or self.collide_list(doors) and self.keys == 0:
                self.rect.y -= 4

    def update(self):
        if self.anim > 10:
            self.img = pygame.image.load("hero_start.png")
            self.anim = 0

        for obj in doors:
            if self.keys > 0 and self.rect.colliderect(obj.rect):
                obj.img = pygame.image.load("door_open.png")
                doors.remove(obj)
                self.keys -= 1
            

        for obj in keys:
            if self.rect.colliderect(obj.rect):
                keys.remove(obj)
                all_sprites.remove(obj)
                self.keys += 1
        for e in enemies:
            if self.rect.colliderect(e.rect):
                self.rect.x, self.rect.y = 24, 0
                self.hp -= 1
                hp[self.hp].img = pygame.image.load("hp_broken.png")


#draw maze
def draw_maze():
    x_maze, y_maze = 0, 0
    x, y = x_maze, y_maze
    for line in map_maze:
        for num in line:
            if num == "1":
               maze.append(Sprite(x, y, "wall.png"))
            elif num == "2":
                doors.append(Sprite(x, y, "door.png"))
            elif num == "3":
                keys.append(Sprite(x, y, "key.png"))
            elif num == "4":
                enemies.append(Enemy(x, y, "enemy.png", 2, 0))
            elif num == "5":
                enemies.append(Enemy(x, y, "enemy.png", 0, 2))
            x += 24
        x = x_maze
        y += 24
        
class Enemy(Sprite):
    def __init__(self, x, y, img, dx, dy): 
        super().__init__(x, y, img)
        self.dx = dx
        self.dy = dy
    
    def move(self, maze):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        if self.collide_list(maze):
            self.dx *= -1
            self.dy *= -1
            self.rect.x += self.dx
            self.rect.y += self.dy

# 24x48 - door
# 24x24 - wall, player, heart, key

# 1 — стіна
# 0 — прохід
# 2 — двері (декілька)
# 3 — ключі
# 4 — вороги рух ліво-право
# 5 — вороги рух вгору-вниз

FON = (133, 230, 255)
FONT_START = pygame.image.load("fon.png")

maze = []
doors = []
keys = []
enemies = []
hp = []

x, y = 350, 0
for i in range(5):
    hp.append(Sprite(x, y, "hp.png"))
    x += 26
    
map_maze = [
    "101111111111111111111",
    "100000100000100000001",
    "101110101010101011101",
    "101000101010101010101",
    "111011101011101010101",
    "100010001000001010201",
    "101110111111111010111",
    "100010140000000010151",
    "111010101110111110101",
    "100010101030100010001",
    "101110101111101011101",
    "101000100010001013101",
    "101011111020111010101",
    "102010001010001010001",
    "101111101111111010111",
    "101000100010000010031",
    "101010101010111111111",
    "101010001010000010001",
    "101011111011111010111",
    "10001400000031000002",
    "111111111111111111111"
]
draw_maze()
font = pygame.font.SysFont("Arial", 50)
font.italic = True
txt = font.render("MAZE GAME", True, (205, 0, 0))
btn_start = Sprite(200,300,"btn_play.png", 128, 128)
start = False
all_sprites = maze + doors + keys + enemies + hp 
hero = Player(24, 0, "hero_start.png")

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

end_game = False
end = Sprite(100, 0, "end.png")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not start:
            if btn_start.rect.collidepoint(event.pos):
                start = True
            
    screen.fill(FON)
    if not start:
        screen.blit(FONT_START, (0, 0))
        screen.blit(txt, (130, 150))
        btn_start.draw(screen)
    else:
        hero.draw(screen)

        if not end_game:
            hero.move()
            hero.update()
            for e in enemies:
                e.move(maze)
                

                            
            if hero.rect.right >= 500:
                end_game = True
                hero.img = pygame.image.load("hero_win.png")
                
            if hero.hp == 0:
                end_game = True
                hero.img = pygame.image.load("hero_lose.png")

            for obj in all_sprites:
                obj.draw(screen)
                
        else:
            hero.rect.x, hero.rect.y = 100, 220
            end.draw(screen)
        
    pygame.display.flip()
    clock.tick(40)

pygame.quit()
