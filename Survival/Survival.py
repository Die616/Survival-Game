import os
import pygame
import math
import random

# Inicializar pygame
pygame.init()

# Velocidad bucles
clock = pygame.time.Clock()

# Directorio actual ***evitar rutas absolutas***
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

# Direccion para score
data_folder_path = os.path.join(script_dir, "data", "score")

# Dimensiones de la ventana
w_screen = 1600
h_screen = 1024

# Crear ventana
def create_window():
    screen = pygame.display.set_mode((w_screen, h_screen))
    return screen

# Crear documento score
def create_score_file():
    score_file_path = os.path.join(data_folder_path, "Score.txt")
    try:
        with open(score_file_path, "x") as file:
            file.write("0")
    except FileExistsError:
        pass

# Guarda el score mas alto
def save_score(score):
    high_score = load_score()
    if score > high_score:
        score_file_path = os.path.join(data_folder_path, "Score.txt")
        with open(score_file_path, "w") as file:
            file.write(str(score))

# Carga documento score
def load_score():
    score_file_path = os.path.join(data_folder_path, "Score.txt")
    try:
        with open(score_file_path, "r") as file:
            return int(file.read())
    except FileExistsError:
        return 0

# Crear mixer
def play_music(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)

# Pantalla de inicio
def start_screen():
    start_music_path = os.path.join("data", "ost", "start_music.mp3")
    play_music(start_music_path)

    start = True
    in_game = False
    screen = create_window()
    
    start_img_path = os.path.join("data", "img", "start_screen.png")
    start_img = pygame.image.load(start_img_path).convert()
    start_img = pygame.transform.scale(start_img, (w_screen, h_screen))
    
    screen_rect = screen.get_rect()

    start_font = pygame.font.Font(None, 100)
    quit_font = pygame.font.Font(None, 50)

    start_text = start_font.render("Press Space to Start", True, (0, 0, 0))
    quit_text = quit_font.render("Q to quit", True, (0, 0, 0))

    start_rect = start_text.get_rect(center=(screen_rect.centerx, screen_rect.centery - 50))
    quit_rect = quit_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 50))



    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start = False
                    in_game = True
                elif event.key == pygame.K_q:
                    pygame.quit()
                    return
    
        screen.blit(start_img, (0, 0))
        screen.blit(start_text, start_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        clock.tick(30)
    
    if in_game:
        game()

# Pantalla Game Over
def game_over_screen(screen, score):
    save_score(score)
    game_over_music_path = os.path.join("data", "ost", "end_music.mp3")
    play_music(game_over_music_path)


    game_over_img_path = os.path.join("data", "img", "game_over_screen.png")
    game_over_img = pygame.image.load(game_over_img_path).convert()
    game_over_img = pygame.transform.scale(game_over_img, (w_screen, h_screen))
    game_over_font = pygame.font.Font(None, 200)
    score_font = pygame.font.Font(None, 100)
    high_score_font = pygame.font.Font(None, 50)
    reset_font = pygame.font.Font(None, 50)
    quit_font = pygame.font.Font(None, 50)

    game_over_text = game_over_font.render("Game Over", True, (0, 0, 0))
    score_text = score_font.render("Score: {}".format(score), True, (0, 0, 0))
    high_score_text = high_score_font.render("High Score: {}".format(load_score()), True, (0, 0, 0))
    reset_text = reset_font.render("R to Reset", True, (0, 0, 0))
    quit_text = quit_font.render("Q to quit", True, (0, 0, 0))

    screen_rect = screen.get_rect()
    game_over_rect = game_over_text.get_rect(center=(screen_rect.centerx, screen_rect.centery - 50))
    score_rect = score_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 50))
    high_score_rect = high_score_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 110))
    reset_rect = reset_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 150))
    quit_rect = quit_text.get_rect(center=(screen_rect.centerx, screen_rect.centery + 180))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game()
                if event.key == pygame.K_q:
                    pygame.quit()
        
        screen.blit(game_over_img, (0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(reset_text, reset_rect)
        screen.blit(quit_text, quit_rect)
        screen.blit(high_score_text, high_score_rect)
        pygame.display.flip()

# Crear fondo
def create_background():
    background_img_path = os.path.join("data", "img", "background.png")
    background_img = pygame.image.load(background_img_path).convert()
    background_img = pygame.transform.scale(background_img, (w_screen, h_screen))
    return background_img

# Personaje
class Character:
    charactert_img = os.path.join("data", "img", "character.png")

    def __init__(self, x, y, character_img_path, scale, max_bullets):
        self.x = x
        self.y = y
        self.health = 100
        self.is_shooting = False
        self.bullets = []
        self.max_bullets = max_bullets
        self.image = pygame.image.load(character_img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width()* scale), int(self.image.get_height() * scale)))
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def damage(self, amount):
        self.health -= amount
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        for bullet in self.bullets:
            bullet.draw(screen)

# Bala
class Bullet:
    def __init__(self, x, y, radius, color, speed, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = speed
        self.direction = direction
    
    def move(self):
        if self.direction == "up":
            self.y -= self.speed
        if self.direction == "down":
            self.y += self.speed
        if self.direction == "left":
            self.x -= self.speed
        if self.direction == "right":
            self.x += self.speed
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

# Enemigo
class Enemy:
    enemy_img = os.path.join("data", "img", "enemy.png")

    def __init__(self, x, y, enemy_img_path, speed):
        self.x = x
        self.y = y
        self.hitbox_scale = 0.5
        self.health = 50
        self.is_alive = True
        self.is_defeated = False
        self.speed = speed
        self.image = pygame.image.load(enemy_img_path).convert_alpha()
    
    def draw(self, screen):
        if self.is_alive:
            screen.blit(self.image, (self.x, self.y))
    
    def follow_character(self, character):
        if self.is_alive:
            dx = character.x - self.x
            dy = character.y - self.y
            distance = math.sqrt(dx**2 + dy**2)
            if distance != 0:
                dx /= distance
                dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed
    
    def receive_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.is_defeated = True

    def check_collision(self, character):
        enemy_rect = self.image.get_rect(topleft=(self.x, self.y))
        scaled_width = int(enemy_rect.width * self.hitbox_scale)
        scaled_height = int(enemy_rect.height * self.hitbox_scale)
        scaled_rect = pygame.Rect(enemy_rect.center, (scaled_width, scaled_height))
        scaled_rect.center = enemy_rect.center

        character_rect = character.image.get_rect(topleft=(character.x, character.y))
        return scaled_rect.colliderect(character_rect)    

# Checar colicion de la bala con enemigo
def bullet_collision_enemy(bullet, enemy):
    bullet_rect = pygame.Rect(bullet.x - bullet.radius, bullet.y - bullet.radius, bullet.radius * 2, bullet.radius * 2)
    enemy_rect = enemy.image.get_rect(topleft=(enemy.x, enemy.y))
    return bullet_rect.colliderect(enemy_rect)

# Actualizar balas
def update_bullets(character, enemies):
    bullets_to_remove = []
    enemies_to_remove = []

    for bullet in character.bullets:
        bullet.move()
        if bullet.y < 0 or bullet.y > h_screen or bullet.x < 0 or bullet.x > w_screen:
            bullets_to_remove.append(bullet)
        else:
            for enemy in enemies:
                if enemy.is_alive and bullet_collision_enemy(bullet, enemy):
                    enemy.receive_damage(10)
                    print("*hit*")
                    bullets_to_remove.append(bullet)
                if not enemy.is_alive:
                    enemies_to_remove.append(enemy)
                    break

    for bullet in bullets_to_remove:
        character.bullets.remove(bullet)
        print("Bala eliminada")
    for enemy in enemies_to_remove:
        enemies.remove(enemy)
        print("Enemigo eliminado")

# Movimiento del personaje
def character_move(character):
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    
    new_x = character.x + dx
    new_y = character.y + dy

    if 0 <= new_x <= w_screen - character.image.get_width():
        character.x = new_x
    if 0 <= new_y <= h_screen - character.image.get_height():
        character.y = new_y

# Movimiento de las balas
def bullets_move(character):
    keys = pygame.key.get_pressed()
    character.is_shooting = keys[pygame.K_UP] or keys[pygame.K_DOWN] or keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]
    
    if character.is_shooting and len(character.bullets) < character.max_bullets:
        if keys[pygame.K_UP]:
            bullet = Bullet(character.x, character.y, character.image.get_width() // 8, (255, 255, 0), 5, "up")
            character.bullets.append(bullet)
            print("bala creada")
        if keys[pygame.K_DOWN]:
            bullet = Bullet(character.x, character.y, character.image.get_width() // 8, (255, 255, 0), 5, "down")
            character.bullets.append(bullet)
            print("bala creada")
        if keys[pygame.K_LEFT]:
            bullet = Bullet(character.x, character.y, character.image.get_width() // 8, (255, 255, 0), 5, "left")
            character.bullets.append(bullet)
            print("bala creada")
        if keys[pygame.K_RIGHT]:
            bullet = Bullet(character.x, character.y, character.image.get_width() // 8, (255, 255, 0), 5, "right")
            character.bullets.append(bullet)
            print("bala creada")

# Render puntaje
def render_score(screen, score):
    score_font = pygame.font.Font(None, 40)
    high_score_font = pygame.font.Font(None, 50)

    score_text = score_font.render("Score: {}".format(score), True, (255, 255, 255))
    high_score_text = high_score_font.render("High Score: {}".format(load_score()), True, (255, 255, 255))
    
    screen.blit(score_text, (10, 50))
    screen.blit(high_score_text, (10, 10))

# Render vida
def render_health_character(screen, character):
    health_font = pygame.font.Font(None, 40)

    health_text = health_font.render("Helath {}".format(character.health), True, (255, 255, 255))

    screen.blit(health_text, (100, 100))


# Crear documento score
create_score_file()


# Ciclo del juego
def game():
    
    # Sonido daño a personaje
    damage_sound_path = os.path.join("data", "ost", "damage_sound.mp3")
    damage_sound = pygame.mixer.Sound(damage_sound_path)
    damage_sound.set_volume(0.25)
    
    # Sonido muerte de enemigo
    enemy_dead_sound_path = os.path.join("data", "ost", "enemy_dead.mp3")
    enemy_dead_sound = pygame.mixer.Sound(enemy_dead_sound_path)

    # Musica pantalla de juego
    game_music_path = os.path.join("data", "ost", "game_music.mp3")
    play_music(game_music_path)
    
    # 
    screen = create_window()
    background = create_background()
    
    # 
    character = Character(100, 100, Character.charactert_img, 0.5, 1)
    enemies = [Enemy(500, 500, Enemy.enemy_img, 0.25)]
    max_enemies_on_screen = 3
    enemy_spawn_chance = 0.02
    score = 0

    w_enemy = enemies[0].image.get_width()
    h_enemy = enemies[0].image.get_height()

    end_game = False
    while not end_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game = True

        
        for enemy in enemies:
            enemy.follow_character(character)
            if enemy.check_collision(character):
                if enemy.is_alive:
                    damage_sound.play()
                    character.damage(1)

            if enemy.is_defeated:
                enemy_dead_sound.play()
                enemies.remove(enemy)
                enemy.is_alive = False
                score += 1
                
        if len(enemies) < max_enemies_on_screen:
            if random.random() < enemy_spawn_chance:
                new_enemy_x = random.randint(0, w_screen - w_enemy)
                new_enemy_y = random.randint(0, h_screen - h_enemy)
                new_enemy = Enemy(new_enemy_x, new_enemy_y, Enemy.enemy_img, 0.25)
                enemies.append(new_enemy)


        if character.health <= 0:
            game_over_screen(screen, score)

        update_bullets(character, enemies)
        character_move(character)
        bullets_move(character)
        screen.blit(background, (0, 0))
        character.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        render_score(screen, score)
        render_health_character(screen, character)
        pygame.display.flip()
    
    pygame.quit()

# Inicia el juego
start_screen()