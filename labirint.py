# Разработай свою игру в этом файле!
from pygame import *
from random import randint, choice

#база
class Baza(sprite.Sprite):
    def __init__(self, x, y, w, h, filename, health):
        super().__init__()
        self.health = health
        self.rect = Rect(x,y,w,h)
        self.image = transform.scale(image.load(filename), (w,h))
        self.x_speed, self.y_speed = 0, 0


    def draw(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

#пули
class Bullet(Baza):
    def __init__ (self, x, y, w, h, filename, health, speed):
        Baza.__init__(self, x, y, w, h, filename, health)
        if speed != 0:
            self.speed = speed
        else:
            self.speed = choice([-2, 2])

    def update(self):
        self.rect.x += self.speed
        if self.rect.x > W + 10:
            self.kill()

#хорошие
class Hero(Baza):
    def update (self):
        self.rect.x += self.x_speed
        self.rect.y += self.y_speed

        touched = sprite.spritecollide(self,walls,False)
        if self.x_speed > 0:
            for wall in touched:
                self.rect.right = min(wall.rect.x,self.rect.right)
            
            if self.rect.right > W: self.rect.right = W 

        if self.x_speed < 0:  
            for wall in touched:
                self.rect.x = max(wall.rect.right,self.rect.x)
            
            if self.rect.x < 0: self.rect.x = 0 

        if self.y_speed > 0:
            for wall in touched:
                self.rect.bottom = min(wall.rect.y,self.rect.bottom)

        if self.y_speed < 0:    
            for wall in touched:
                self.rect.y = max(wall.rect.bottom,self.rect.y)

        touched = sprite.spritecollide(self,enemies,False)
        if touched:
            global game_mode
            game_mode = 'defeat'
        
        self.draw()

    def fire(self):
        bullet = Bullet(self.rect.x, self.rect.y, 45, 45, 'sfera.png', 10, self.x_speed)
        bullets.add(bullet)

#злодеи
class Enemy(Baza):
    def update(self):
        if self.rect.right >= W:
            self.x_speed = -2 - randint(0, 2)

        if self.rect.x < 350:
            self.x_speed = +2 + randint(0, 2)
        
        self.rect.x += self.x_speed
        self.draw()


class ShooterEnemy(Baza):
    def update(self):
        if self.rect.bottom >= H:
            self.y_speed = -2 - randint(0, 2)

        if self.rect.top < 0:
            self.y_speed = 2 + randint(0, 2)

        if randint(0,100) == 100:
            self.fire()

        self.rect.y += self.y_speed
        self.draw()

    def fire(self):
        b = Bullet(self.rect.x, self.rect.y, 45, 45, 'shoot.png', 10, self.x_speed)
        enemy_bullets.add(b)
    
#стены
class Wall_picture(Baza):
    def update(self):
        self.draw()
#цвета стен
class Wall_color(sprite.Sprite):
    def __init__(self,x,y,w,h,color):
        super().__init__()
        self.rect = Rect(x,y,w,h)
        self.color = color
        walls.add(self)

    def draw(self):
        draw.rect(win,self.color,self.rect)
    
    def update(self):
        self.draw()

#дисплей
W, H = 1000, 1000
win = display.set_mode((1000, 1000)) #, flags = FULLSCREEN
display.set_caption('Mortal Kombat')
display.set_icon(image.load('icon.png'))

#фоны
background = image.load('fonmk.jpg')
background = transform.scale(background, (W, H))
defeat_background = image.load('bad.jpg')
win_background = image.load('scorpionw.jpeg')

#персонажи
scorpion = Hero(x = 100, y = 800, w = 125, h = 125, filename = 'scorpion.png', health = 10)

enemies = sprite.Group()
shao_khan = Enemy(x = 500, y = 600, w = 150, h = 150, filename = 'shao-khan.png', health = 10)
enemies.add(shao_khan)
shao_khan.x_speed = -1

#пули
bullets = sprite.Group()

# победа
final = Baza(x = 450, y = 875, w = 175,  h = 175, filename = 'skulls.png', health = 10)
win_background = Baza(x = 0, y = 0, w = 1000,  h = 1000, filename = 'scorpionw.jpeg', health = 10)
# с убийством
fatality1 = Baza(x = 0, y = 0, w = 400,  h = 200, filename = 'fatality.jpg', health = 10)
# без него
winner = Baza(x = 10, y = 50, w = 400,  h = 200, filename = 'win.png', health = 10)

# поражение
defeat_background = Baza(x = 0, y = 0, w = 1000,  h = 1000, filename = 'shao-khan_winner.jpg', health = 10)
fatality2 = Baza(x = 0, y = 799, w = 1000,  h = 200, filename = 'fatality.jpg', health = 10)

# стены
walls = sprite.Group()
Wall_color(x=300,y=200,w=50,h=800,color =(255,162,0))
Wall_color(x=150,y=500,w=600,h=50,color =(255,162,0))
Wall_color(x=735,y=800,w=50,h=200,color =(255,162,0))
# рамка
Wall_color(x=0,y=0,w=1,h=1000,color =(255,162,0))
Wall_color(x=0,y=0,w=1000,h=1,color =(255,162,0))
Wall_color(x=999,y=0,w=1,h=1000,color =(255,162,0))
Wall_color(x=150,y=999,w=300,h=1,color =(255,162,0))
Wall_color(x=550,y=999,w=450,h=1,color =(255,162,0))

game_mode = 'game'
run = True

timer = time.Clock()

while run:
    for e in event.get():
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            exit()

        if e.type == KEYDOWN and e.key == K_d:
            scorpion.x_speed = 3
            scorpion.y_speed = 0

        if e.type == KEYDOWN and e.key == K_a:
            scorpion.x_speed = -3
            scorpion.y_speed = 0

        if e.type == KEYDOWN and e.key == K_s:
            scorpion.y_speed = 3
            scorpion.x_speed = 0

        if e.type == KEYDOWN and e.key == K_w:
            scorpion.y_speed = -3
            scorpion.x_speed = 0
        
        if e.type == KEYUP:
            if e.key == K_w or e.key == K_s:
                scorpion.y_speed = 0
            if e.key == K_a or e.key == K_d:
                scorpion.x_speed = 0
            if e.key == K_SPACE:
                scorpion.fire()
    
    if game_mode == 'game':
        win.blit(background,(0,0))

        scorpion.update()
        for enemy in enemies:
            enemy.update()

        walls.update()
        final.draw()

        bullets.update()
        bullets.draw(win)
    
        if sprite.collide_rect(scorpion, final):
            if len(enemies) == 0:
                game_mode = 'kill_final'
            else:
                game_mode = 'not_kill_final'
    
    if game_mode == 'kill_final':
        win_background.draw()
        fatality1.draw()
    
    if game_mode == 'not_kill_final':
        win_background.draw()
        winner.draw()

    if game_mode == 'defeat':
        defeat_background.draw()
        fatality2.draw()
    
    sprite.groupcollide(enemies, bullets, True, True)
    sprite.groupcollide(walls, bullets, False, True)

    timer.tick(120)
    display.update()
