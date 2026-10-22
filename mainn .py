import pygame
import random
import math
import sys
import os

# ============================================================
# BLADE MASTER 2D
# 2D SIDE-VIEW SWORD FIGHTING
# ============================================================

pygame.init()


# ============================================================
# AUDIO
# ============================================================

SOUND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds")
SOUND_CACHE = {}
AUDIO_ENABLED = True

def load_sound(file_name):
    if not AUDIO_ENABLED:
        return None
    if file_name in SOUND_CACHE:
        return SOUND_CACHE[file_name]

    path = os.path.join(SOUND_DIR, file_name)
    if not os.path.exists(path):
        return None

    try:
        sound = pygame.mixer.Sound(path)
        SOUND_CACHE[file_name] = sound
        return sound
    except (pygame.error, OSError):
        return None


def play_sound(file_name):
    sound = load_sound(file_name)
    if sound is not None:
        try:
            sound.play()
        except pygame.error:
            pass


SOUND_FILES = {
    "light": "sword_slash.wav",
    "heavy": "sword_heavy.wav",
    "skill": "sword_skill.wav",
    "hit": "hit.wav",
    "parry": "parry.wav",
    "dodge": "dodge.wav",
    "counter": "counter.wav",
    "victory": "victory.wav",
    "defeat": "defeat.wav",
}

# ============================================================
# CONFIG
# ============================================================

WIDTH = 1100
HEIGHT = 650
FPS = 60

GROUND_Y = 500
ARENA_LEFT = 70
ARENA_RIGHT = WIDTH - 70

PLAYER_HP = 750
BOT_HP = 1000

START_GOLD = 10000

LIGHT_DAMAGE = 25
HEAVY_DAMAGE = 65
SKILL_DAMAGE = 120
COUNTER_DAMAGE = 60

WHITE = (245, 245, 245)
BLACK = (8, 10, 18)

BG_TOP = (12, 18, 35)
BG_BOTTOM = (25, 32, 52)

RED = (239, 68, 68)
GREEN = (34, 197, 94)
BLUE = (59, 130, 246)
CYAN = (6, 182, 212)
YELLOW = (245, 158, 11)
PURPLE = (168, 85, 247)
GRAY = (100, 116, 139)
DARK = (25, 34, 52)


# ============================================================
# FONTS
# ============================================================

FONT_TITLE = pygame.font.SysFont("arial", 42, bold=True)
FONT_BIG = pygame.font.SysFont("arial", 30, bold=True)
FONT_MED = pygame.font.SysFont("arial", 21, bold=True)
FONT = pygame.font.SysFont("arial", 17)
FONT_SMALL = pygame.font.SysFont("arial", 13)


# ============================================================
# HELPERS
# ============================================================

def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def draw_text(surface, text, x, y, color=WHITE,
              font=FONT, center=False):

    img = font.render(str(text), True, color)

    if center:
        rect = img.get_rect(center=(x, y))
    else:
        rect = img.get_rect(topleft=(x, y))

    surface.blit(img, rect)


def draw_bar(surface, x, y, width, height,
             value, maximum, color):

    pygame.draw.rect(
        surface,
        (45, 50, 65),
        (x, y, width, height),
        border_radius=6
    )

    if maximum > 0:
        ratio = clamp(value / maximum, 0, 1)

        pygame.draw.rect(
            surface,
            color,
            (x, y, int(width * ratio), height),
            border_radius=6
        )


# ============================================================
# PARTICLE
# ============================================================

class Particle:

    def __init__(self, x, y, color):

        self.x = x
        self.y = y

        self.vx = random.uniform(-180, 180)
        self.vy = random.uniform(-220, -40)

        self.life = random.uniform(0.25, 0.6)

        self.color = color
        self.size = random.randint(3, 7)

    def update(self, dt):

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.vy += 600 * dt

        self.life -= dt

    def draw(self, surface):

        if self.life <= 0:
            return

        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            self.size
        )


# ============================================================
# FIGHTER
# ============================================================

class Fighter:

    def __init__(self, name, color, max_hp):

        self.name = name
        self.color = color

        self.max_hp = max_hp
        self.hp = max_hp

        self.max_stamina = 100
        self.stamina = 100

        self.x = 250
        self.y = GROUND_Y

        self.width = 55
        self.height = 110

        self.facing = 1

        self.stance = "MID"

        self.light_cd = 0
        self.heavy_cd = 0
        self.skill_cd = 0

        self.attack_timer = 0
        self.attack_type = None

        self.parry_timer = 0
        self.dodge_timer = 0
        self.stun_timer = 0

        self.hit_flash = 0

        self.alive = True

        self.last_action = "Sẵn sàng"

    # --------------------------------------------------------

    def reset(self, x):

        self.hp = self.max_hp
        self.stamina = self.max_stamina

        self.x = x
        self.y = GROUND_Y

        self.facing = 1

        self.stance = "MID"

        self.light_cd = 0
        self.heavy_cd = 0
        self.skill_cd = 0

        self.attack_timer = 0
        self.attack_type = None

        self.parry_timer = 0
        self.dodge_timer = 0
        self.stun_timer = 0

        self.hit_flash = 0

        self.alive = True

        self.last_action = "Sẵn sàng"

    # --------------------------------------------------------

    def update(self, dt):

        self.light_cd = max(0, self.light_cd - dt)
        self.heavy_cd = max(0, self.heavy_cd - dt)
        self.skill_cd = max(0, self.skill_cd - dt)

        self.attack_timer = max(0, self.attack_timer - dt)

        self.parry_timer = max(0, self.parry_timer - dt)
        self.dodge_timer = max(0, self.dodge_timer - dt)
        self.stun_timer = max(0, self.stun_timer - dt)

        self.hit_flash = max(0, self.hit_flash - dt)

        self.stamina = min(
            self.max_stamina,
            self.stamina + dt * 18
        )

    # --------------------------------------------------------

    def rect(self):

        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height),
            self.width,
            self.height
        )

    # --------------------------------------------------------

    def center_y(self):

        return self.y - self.height // 2


# ============================================================
# GAME
# ============================================================

class BladeMaster:

    def __init__(self):

        self.screen = pygame.display.set_mode(
            (WIDTH, HEIGHT)
        )

        pygame.display.set_caption(
            "Blade Master 2D"
        )

        self.clock = pygame.time.Clock()

        self.state = "MENU"

        self.player = Fighter(
            "KAEL",
            BLUE,
            PLAYER_HP
        )

        self.enemy = Fighter(
            "RYU",
            RED,
            BOT_HP
        )

        self.player.reset(300)
        self.enemy.reset(800)

        self.gold = START_GOLD

        self.weapon_level = 1
        self.armor_level = 1

        self.message = ""
        self.message_timer = 0

        self.winner = None

        self.particles = []

        self.hit_effect_timer = 0

        self.screen_shake = 0

        self.bot_think = 0
        self.bot_attack_cd = 0

        self.background_offset = 0

    # ========================================================
    # MENU
    # ========================================================

    def menu(self):

        self.draw_background()

        draw_text(
            self.screen,
            "BLADE MASTER",
            WIDTH // 2,
            70,
            YELLOW,
            FONT_TITLE,
            True
        )

        draw_text(
            self.screen,
            "2D SIDE-VIEW SWORD FIGHTING",
            WIDTH // 2,
            120,
            GRAY,
            FONT_MED,
            True
        )

        # Character card

        pygame.draw.rect(
            self.screen,
            DARK,
            (100, 180, 420, 260),
            border_radius=15
        )

        pygame.draw.rect(
            self.screen,
            BLUE,
            (100, 180, 420, 260),
            2,
            border_radius=15
        )

        draw_text(
            self.screen,
            "KAEL",
            140,
            215,
            BLUE,
            FONT_BIG
        )

        draw_text(
            self.screen,
            "Kiếm Sĩ Lang Thang",
            140,
            255,
            WHITE
        )

        draw_text(
            self.screen,
            "HP: 750",
            140,
            300,
            GREEN
        )

        draw_text(
            self.screen,
            "Stamina: 100",
            140,
            330,
            YELLOW
        )

        draw_text(
            self.screen,
            "Đánh nhanh và cân bằng",
            140,
            370,
            GRAY
        )

        # Boss card

        pygame.draw.rect(
            self.screen,
            DARK,
            (580, 180, 420, 260),
            border_radius=15
        )

        pygame.draw.rect(
            self.screen,
            RED,
            (580, 180, 420, 260),
            2,
            border_radius=15
        )

        draw_text(
            self.screen,
            "RYU",
            620,
            215,
            RED,
            FONT_BIG
        )

        draw_text(
            self.screen,
            "Hắc Kiếm Sĩ - BOSS",
            620,
            255,
            WHITE
        )

        draw_text(
            self.screen,
            "HP: 1000",
            620,
            300,
            RED
        )

        draw_text(
            self.screen,
            "AI: Tự động né + parry",
            620,
            330,
            YELLOW
        )

        draw_text(
            self.screen,
            "Cực kỳ hung hãn",
            620,
            370,
            GRAY
        )

        # Gold

        draw_text(
            self.screen,
            f"Vàng: {self.gold}",
            WIDTH // 2,
            475,
            YELLOW,
            FONT_MED,
            True
        )

        draw_text(
            self.screen,
            "[ENTER] Bắt đầu trận đấu",
            WIDTH // 2,
            525,
            WHITE,
            FONT_MED,
            True
        )

        draw_text(
            self.screen,
            "[S] Shop      [Q] Thoát",
            WIDTH // 2,
            565,
            GRAY,
            FONT,
            True
        )

    # ========================================================
    # SHOP
    # ========================================================

    def shop(self):

        self.draw_background()

        draw_text(
            self.screen,
            "CHỢ RÈN",
            WIDTH // 2,
            60,
            YELLOW,
            FONT_TITLE,
            True
        )

        draw_text(
            self.screen,
            f"Vàng: {self.gold}",
            WIDTH // 2,
            110,
            WHITE,
            FONT_MED,
            True
        )

        # Weapon

        pygame.draw.rect(
            self.screen,
            DARK,
            (130, 180, 360, 300),
            border_radius=15
        )

        draw_text(
            self.screen,
            "KIẾM",
            170,
            215,
            YELLOW,
            FONT_BIG
        )

        draw_text(
            self.screen,
            f"Cấp: {self.weapon_level}",
            170,
            270,
            WHITE
        )

        draw_text(
            self.screen,
            "+10 sát thương đòn nhẹ",
            170,
            310,
            GRAY
        )

        draw_text(
            self.screen,
            "+20 sát thương đòn nặng",
            170,
            340,
            GRAY
        )

        draw_text(
            self.screen,
            f"Giá: 1000 vàng",
            170,
            400,
            YELLOW
        )

        draw_text(
            self.screen,
            "[1] Nâng cấp",
            170,
            440,
            GREEN
        )

        # Armor

        pygame.draw.rect(
            self.screen,
            DARK,
            (610, 180, 360, 300),
            border_radius=15
        )

        draw_text(
            self.screen,
            "GIÁP",
            650,
            215,
            CYAN,
            FONT_BIG
        )

        draw_text(
            self.screen,
            f"Cấp: {self.armor_level}",
            650,
            270,
            WHITE
        )

        draw_text(
            self.screen,
            "-5% sát thương nhận",
            650,
            310,
            GRAY
        )

        draw_text(
            self.screen,
            f"Giá: 1000 vàng",
            650,
            400,
            YELLOW
        )

        draw_text(
            self.screen,
            "[2] Nâng cấp",
            650,
            440,
            GREEN
        )

        draw_text(
            self.screen,
            "[ESC] Quay lại",
            WIDTH // 2,
            560,
            GRAY,
            FONT_MED,
            True
        )

    # ========================================================
    # BACKGROUND
    # ========================================================

    def draw_background(self):

        for y in range(HEIGHT):

            ratio = y / HEIGHT

            color = (
                int(BG_TOP[0] * (1-ratio) + BG_BOTTOM[0] * ratio),
                int(BG_TOP[1] * (1-ratio) + BG_BOTTOM[1] * ratio),
                int(BG_TOP[2] * (1-ratio) + BG_BOTTOM[2] * ratio),
            )

            pygame.draw.line(
                self.screen,
                color,
                (0, y),
                (WIDTH, y)
            )

        # Moon

        pygame.draw.circle(
            self.screen,
            (220, 225, 240),
            (900, 120),
            45
        )

        # Buildings

        for i in range(12):

            x = i * 110

            h = 80 + (i * 37) % 150

            pygame.draw.rect(
                self.screen,
                (17, 24, 40),
                (x, GROUND_Y - h, 90, h)
            )

            for wy in range(
                GROUND_Y - h + 20,
                GROUND_Y - 10,
                30
            ):

                pygame.draw.rect(
                    self.screen,
                    (80, 90, 110),
                    (x + 15, wy, 12, 12)
                )

        # Ground

        pygame.draw.rect(
            self.screen,
            (40, 46, 58),
            (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y)
        )

        pygame.draw.line(
            self.screen,
            YELLOW,
            (0, GROUND_Y),
            (WIDTH, GROUND_Y),
            3
        )

        # Arena lines

        for x in range(0, WIDTH, 100):

            pygame.draw.line(
                self.screen,
                (50, 57, 70),
                (x, GROUND_Y),
                (x + 60, HEIGHT),
                1
            )

    # ========================================================
    # GAMEPLAY
    # ========================================================

    def gameplay(self):

        self.draw_background()

        self.draw_fighter(self.player)
        self.draw_fighter(self.enemy)

        self.draw_hud()

        self.draw_particles()

        if self.hit_effect_timer > 0:

            pygame.draw.circle(
                self.screen,
                YELLOW,
                (
                    WIDTH // 2,
                    HEIGHT // 2
                ),
                int(60 * self.hit_effect_timer),
                3
            )

    # ========================================================
    # FIGHTER DRAW
    # ========================================================

    def draw_fighter(self, fighter):

        rect = fighter.rect()

        if fighter.hit_flash > 0:
            color = WHITE
        else:
            color = fighter.color

        # Shadow

        pygame.draw.ellipse(
            self.screen,
            (10, 10, 15),
            (
                fighter.x - 40,
                GROUND_Y - 8,
                80,
                18
            )
        )

        # Legs

        pygame.draw.line(
            self.screen,
            color,
            (fighter.x - 12, fighter.y - 30),
            (fighter.x - 15, fighter.y),
            10
        )

        pygame.draw.line(
            self.screen,
            color,
            (fighter.x + 12, fighter.y - 30),
            (fighter.x + 15, fighter.y),
            10
        )

        # Body

        pygame.draw.rect(
            self.screen,
            color,
            (
                rect.x + 8,
                rect.y + 25,
                rect.width - 16,
                55
            ),
            border_radius=8
        )

        # Head

        pygame.draw.circle(
            self.screen,
            (230, 190, 160),
            (
                int(fighter.x),
                int(fighter.y - 95)
            ),
            20
        )

        # Hair

        pygame.draw.arc(
            self.screen,
            BLACK,
            (
                fighter.x - 22,
                fighter.y - 118,
                44,
                45
            ),
            math.pi,
            math.pi * 2,
            7
        )

        # Sword

        sword_start_x = fighter.x + fighter.facing * 15
        sword_start_y = fighter.y - 55

        sword_length = 65

        if fighter.attack_timer > 0:

            sword_length = 100

            # Attack slash

            if fighter.attack_type == "skill":

                pygame.draw.arc(
                    self.screen,
                    PURPLE,
                    (
                        fighter.x - 90,
                        fighter.y - 120,
                        180,
                        150
                    ),
                    -1.2,
                    1.2,
                    8
                )

            else:

                pygame.draw.arc(
                    self.screen,
                    YELLOW,
                    (
                        fighter.x - 70,
                        fighter.y - 100,
                        150,
                        130
                    ),
                    -1.2,
                    1.2,
                    6
                )

        sword_end_x = sword_start_x + fighter.facing * sword_length

        pygame.draw.line(
            self.screen,
            WHITE,
            (sword_start_x, sword_start_y),
            (sword_end_x, sword_start_y - 25),
            6
        )

        pygame.draw.line(
            self.screen,
            YELLOW,
            (sword_start_x, sword_start_y),
            (sword_end_x, sword_start_y - 25),
            2
        )

        # Parry shield

        if fighter.parry_timer > 0:

            pygame.draw.circle(
                self.screen,
                CYAN,
                (
                    int(fighter.x),
                    int(fighter.y - 60)
                ),
                55,
                4
            )

        # Dodge

        if fighter.dodge_timer > 0:

            pygame.draw.circle(
                self.screen,
                BLUE,
                (
                    int(fighter.x),
                    int(fighter.y - 55)
                ),
                65,
                3
            )

        # Name

        draw_text(
            self.screen,
            fighter.name,
            fighter.x,
            fighter.y - 140,
            fighter.color,
            FONT_SMALL,
            True
        )

    # ========================================================
    # HUD
    # ========================================================

    def draw_hud(self):

        # Player

        pygame.draw.rect(
            self.screen,
            DARK,
            (20, 20, 360, 100),
            border_radius=10
        )

        draw_text(
            self.screen,
            "KAEL",
            35,
            30,
            BLUE,
            FONT_MED
        )

        draw_bar(
            self.screen,
            35,
            60,
            220,
            15,
            self.player.hp,
            self.player.max_hp,
            GREEN
        )

        draw_text(
            self.screen,
            f"{int(self.player.hp)}/{self.player.max_hp}",
            265,
            58,
            WHITE,
            FONT_SMALL
        )

        draw_bar(
            self.screen,
            35,
            82,
            220,
            10,
            self.player.stamina,
            self.player.max_stamina,
            YELLOW
        )

        # Enemy

        pygame.draw.rect(
            self.screen,
            DARK,
            (WIDTH - 380, 20, 360, 100),
            border_radius=10
        )

        draw_text(
            self.screen,
            "RYU - BOSS",
            WIDTH - 365,
            30,
            RED,
            FONT_MED
        )

        draw_bar(
            self.screen,
            WIDTH - 365,
            60,
            220,
            15,
            self.enemy.hp,
            self.enemy.max_hp,
            RED
        )

        draw_text(
            self.screen,
            f"{int(self.enemy.hp)}/{self.enemy.max_hp}",
            WIDTH - 135,
            58,
            WHITE,
            FONT_SMALL
        )

        draw_bar(
            self.screen,
            WIDTH - 365,
            82,
            220,
            10,
            self.enemy.stamina,
            self.enemy.max_stamina,
            YELLOW
        )

        # Center

        draw_text(
            self.screen,
            "BLADE MASTER",
            WIDTH // 2,
            30,
            YELLOW,
            FONT_MED,
            True
        )

        draw_text(
            self.screen,
            f"Vàng: {self.gold}",
            WIDTH // 2,
            65,
            YELLOW,
            FONT_SMALL,
            True
        )

        # Controls

        controls = (
            "A/D: Di chuyển | E: Đánh nhẹ | Y: Đòn nặng | "
            "Z: Parry | X: Né | C: Skill | V: Phản công"
        )

        pygame.draw.rect(
            self.screen,
            DARK,
            (130, HEIGHT - 50, WIDTH - 260, 35),
            border_radius=8
        )

        draw_text(
            self.screen,
            controls,
            WIDTH // 2,
            HEIGHT - 32,
            WHITE,
            FONT_SMALL,
            True
        )

    # ========================================================
    # PARTICLES
    # ========================================================

    def spawn_particles(self, x, y, color):

        for _ in range(18):

            self.particles.append(
                Particle(
                    x,
                    y,
                    color
                )
            )

    def draw_particles(self):

        for particle in self.particles:

            particle.draw(self.screen)

    def update_particles(self, dt):

        for particle in self.particles:

            particle.update(dt)

        self.particles = [
            p for p in self.particles
            if p.life > 0
        ]

    # ========================================================
    # DAMAGE
    # ========================================================

    def deal_damage(self, attacker, defender, damage):

        if not defender.alive:
            return

        # Dodge

        if defender.dodge_timer > 0:

            defender.last_action = "NÉ THÀNH CÔNG!"
            play_sound(SOUND_FILES["dodge"])

            attacker.stun_timer = 0.8

            self.spawn_particles(
                defender.x,
                defender.y - 60,
                CYAN
            )

            return

        # Parry

        if defender.parry_timer > 0:

            defender.last_action = "PARRY!"
            play_sound(SOUND_FILES["parry"])

            attacker.stun_timer = 1.4

            self.spawn_particles(
                defender.x,
                defender.y - 60,
                WHITE
            )

            return

        # Stance

        multiplier = 1.0

        if defender.stance == "LOW":
            multiplier *= 0.8

        # Armor

        if defender is self.player:

            multiplier *= max(
                0.25,
                1 - (self.armor_level - 1) * 0.05
            )

        real_damage = damage * multiplier

        defender.hp -= real_damage

        defender.hit_flash = 0.15
        play_sound(SOUND_FILES["hit"])

        self.hit_effect_timer = 0.2

        self.screen_shake = 0.12

        self.spawn_particles(
            defender.x,
            defender.y - 60,
            RED if defender is self.player else YELLOW
        )

        if defender.hp <= 0:

            defender.hp = 0
            defender.alive = False

            if defender is self.enemy:

                self.end_game(True)

            else:

                self.end_game(False)

    # ========================================================
    # ATTACK
    # ========================================================

    def attack(self, attacker, defender, attack_type):

        if not attacker.alive:
            return

        if attacker.stun_timer > 0:
            return

        distance = abs(
            attacker.x - defender.x
        )

        if attack_type == "light":

            if attacker.light_cd > 0:
                return

            if attacker.stamina < 10:
                return

            attacker.stamina -= 10

            attacker.light_cd = 0.45

            attacker.attack_timer = 0.18

            attacker.attack_type = "light"

            attacker.last_action = "Đánh nhẹ!"
            play_sound(SOUND_FILES["light"])

            damage = LIGHT_DAMAGE

            damage += (
                self.weapon_level - 1
            ) * 10

            if distance < 105:

                self.deal_damage(
                    attacker,
                    defender,
                    damage
                )

        elif attack_type == "heavy":

            if attacker.heavy_cd > 0:
                return

            if attacker.stamina < 25:
                return

            attacker.stamina -= 25

            attacker.heavy_cd = 1.2

            attacker.attack_timer = 0.35

            attacker.attack_type = "heavy"

            attacker.last_action = "ĐÒN NẶNG!"
            play_sound(SOUND_FILES["heavy"])

            damage = HEAVY_DAMAGE

            damage += (
                self.weapon_level - 1
            ) * 20

            if distance < 125:

                self.deal_damage(
                    attacker,
                    defender,
                    damage
                )

        elif attack_type == "skill":

            if attacker.skill_cd > 0:
                return

            if attacker.stamina < 40:
                return

            attacker.stamina -= 40

            attacker.skill_cd = 5

            attacker.attack_timer = 0.5

            attacker.attack_type = "skill"

            attacker.last_action = "SKILL!"
            play_sound(SOUND_FILES["skill"])

            if distance < 160:

                self.deal_damage(
                    attacker,
                    defender,
                    SKILL_DAMAGE,
                )

    # ========================================================
    # PLAYER
    # ========================================================

    def update_player(self, dt):

        if not self.player.alive:
            return

        if self.player.stun_timer > 0:
            return

        keys = pygame.key.get_pressed()

        speed = 280

        if keys[pygame.K_LSHIFT]:

            speed *= 1.35

        if keys[pygame.K_a]:

            self.player.x -= speed * dt

            self.player.facing = -1

        if keys[pygame.K_d]:

            self.player.x += speed * dt

            self.player.facing = 1

        self.player.x = clamp(
            self.player.x,
            ARENA_LEFT,
            ARENA_RIGHT
        )

    # ========================================================
    # BOT AI
    # ========================================================

    def update_bot(self, dt):

        bot = self.enemy
        player = self.player

        if not bot.alive:
            return

        if bot.stun_timer > 0:
            return

        distance = abs(
            bot.x - player.x
        )

        bot.facing = (
            -1 if bot.x > player.x else 1
        )

        # Di chuyển tới người chơi

        if distance > 110:

            bot.x += (
                bot.facing
                * 160
                * dt
            )

        # Không chạy khỏi map

        bot.x = clamp(
            bot.x,
            ARENA_LEFT,
            ARENA_RIGHT
        )

        self.bot_think -= dt
        self.bot_attack_cd -= dt

        # AI đổi stance

        if self.bot_think <= 0:

            self.bot_think = random.uniform(
                0.2,
                0.5
            )

            choice = random.random()

            if player.stance == "HIGH":

                bot.stance = "LOW"

            elif player.stance == "LOW":

                bot.stance = "HIGH"

            else:

                if choice < 0.5:
                    bot.stance = "MID"
                elif choice < 0.75:
                    bot.stance = "HIGH"
                else:
                    bot.stance = "LOW"

        # AI phòng thủ

        if distance < 170:

            roll = random.random()

            if roll < 0.025:

                bot.parry_timer = 0.35

                bot.stamina = max(
                    0,
                    bot.stamina - 12
                )

                bot.last_action = "BOT PARRY!"

            elif roll < 0.045:

                bot.dodge_timer = 0.35

                bot.stamina = max(
                    0,
                    bot.stamina - 12
                )

                bot.x += (
                    bot.facing
                    * -80
                )

                bot.last_action = "BOT NÉ!"

        # Tấn công

        if distance < 120 and self.bot_attack_cd <= 0:

            self.bot_attack_cd = random.uniform(
                0.35,
                0.8
            )

            roll = random.random()

            if roll < 0.18:

                self.attack(
                    bot,
                    player,
                    "skill"
                )

            elif roll < 0.55:

                self.attack(
                    bot,
                    player,
                    "heavy"
                )

            else:

                self.attack(
                    bot,
                    player,
                    "light"
                )

    # ========================================================
    # INPUT
    # ========================================================

    def handle_key(self, key):

        if self.state == "MENU":

            if key == pygame.K_RETURN:

                self.start_match()

            elif key == pygame.K_s:

                self.state = "SHOP"

            elif key == pygame.K_q:

                pygame.quit()
                sys.exit()

        elif self.state == "SHOP":

            if key == pygame.K_ESCAPE:

                self.state = "MENU"

            elif key == pygame.K_1:

                self.upgrade_weapon()

            elif key == pygame.K_2:

                self.upgrade_armor()

        elif self.state == "PLAYING":

            if key == pygame.K_e:

                self.attack(
                    self.player,
                    self.enemy,
                    "light"
                )

            elif key == pygame.K_y:

                self.attack(
                    self.player,
                    self.enemy,
                    "heavy"
                )

            elif key == pygame.K_c:

                self.attack(
                    self.player,
                    self.enemy,
                    "skill"
                )

            elif key == pygame.K_z:

                if self.player.stamina >= 12:

                    self.player.stamina -= 12

                    self.player.parry_timer = 0.4
                    play_sound(SOUND_FILES["parry"])

                    self.player.last_action = "PARRY!"

            elif key == pygame.K_x:

                if self.player.stamina >= 15:

                    self.player.stamina -= 15

                    self.player.dodge_timer = 0.4
                    play_sound(SOUND_FILES["dodge"])

                    self.player.x += (
                        self.player.facing
                        * 90
                    )

                    self.player.x = clamp(
                        self.player.x,
                        ARENA_LEFT,
                        ARENA_RIGHT
                    )

                    self.player.last_action = "NÉ!"

            elif key == pygame.K_v:

                if self.enemy.stun_timer > 0:

                    self.attack(
                        self.player,
                        self.enemy,
                        "heavy"
                    )

                    self.player.last_action = "PHẢN CÔNG!"
                    play_sound(SOUND_FILES["counter"])

                else:

                    self.player.last_action = "Phản công trượt!"

            elif key == pygame.K_1:

                self.player.stance = "HIGH"
                self.player.last_action = "Thế HIGH"

            elif key == pygame.K_2:

                self.player.stance = "MID"
                self.player.last_action = "Thế MID"

            elif key == pygame.K_3:

                self.player.stance = "LOW"
                self.player.last_action = "Thế LOW"

            elif key == pygame.K_ESCAPE:

                self.state = "MENU"

        elif self.state == "GAMEOVER":

            if key in (
                pygame.K_RETURN,
                pygame.K_SPACE
            ):

                self.state = "MENU"

    # ========================================================
    # SHOP
    # ========================================================

    def upgrade_weapon(self):

        if self.gold >= 1000:

            self.gold -= 1000

            self.weapon_level += 1

            self.show_message(
                "Đã nâng cấp KIẾM!"
            )

        else:

            self.show_message(
                "Không đủ vàng!"
            )

    def upgrade_armor(self):

        if self.gold >= 1000:

            self.gold -= 1000

            self.armor_level += 1

            self.show_message(
                "Đã nâng cấp GIÁP!"
            )

        else:

            self.show_message(
                "Không đủ vàng!"
            )

    # ========================================================
    # START MATCH
    # ========================================================

    def start_match(self):

        self.player.reset(300)
        self.enemy.reset(800)

        self.player.max_hp = PLAYER_HP
        self.player.hp = PLAYER_HP

        self.enemy.max_hp = BOT_HP
        self.enemy.hp = BOT_HP

        self.state = "PLAYING"

        self.particles.clear()

        self.winner = None

    # ========================================================
    # END GAME
    # ========================================================

    def end_game(self, won):

        if self.state != "PLAYING":
            return

        self.winner = won

        if won:
            play_sound(SOUND_FILES["victory"])

            self.gold += 2000

            self.message = (
                "CHIẾN THẮNG! +2000 VÀNG"
            )

        else:
            play_sound(SOUND_FILES["defeat"])

            self.gold = max(
                0,
                self.gold - 1000
            )

            self.message = (
                "THẤT BẠI! -1000 VÀNG"
            )

        self.state = "GAMEOVER"

    # ========================================================
    # MESSAGE
    # ========================================================

    def show_message(self, text):

        self.message = text

        self.message_timer = 2

    # ========================================================
    # GAMEOVER
    # ========================================================

    def draw_gameover(self):

        overlay = pygame.Surface(
            (WIDTH, HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill(
            (0, 0, 0, 190)
        )

        self.screen.blit(
            overlay,
            (0, 0)
        )

        if self.winner:

            title = "CHIẾN THẮNG!"
            color = GREEN

        else:

            title = "THẤT BẠI!"
            color = RED

        draw_text(
            self.screen,
            title,
            WIDTH // 2,
            230,
            color,
            FONT_TITLE,
            True
        )

        draw_text(
            self.screen,
            self.message,
            WIDTH // 2,
            300,
            WHITE,
            FONT_BIG,
            True
        )

        draw_text(
            self.screen,
            f"Vàng hiện tại: {self.gold}",
            WIDTH // 2,
            350,
            YELLOW,
            FONT_MED,
            True
        )

        draw_text(
            self.screen,
            "[ENTER] Chơi lại",
            WIDTH // 2,
            420,
            WHITE,
            FONT_MED,
            True
        )

        draw_text(
            self.screen,
            "[ESC] Menu",
            WIDTH // 2,
            460,
            GRAY,
            FONT_MED,
            True
        )

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):

        self.player.update(dt)
        self.enemy.update(dt)

        self.update_particles(dt)

        self.hit_effect_timer = max(
            0,
            self.hit_effect_timer - dt
        )

        self.message_timer = max(
            0,
            self.message_timer - dt
        )

        if self.state == "PLAYING":

            self.update_player(dt)

            self.update_bot(dt)

    # ========================================================
    # RENDER
    # ========================================================

    def render(self):

        if self.state == "MENU":

            self.menu()

        elif self.state == "SHOP":

            self.shop()

        elif self.state == "PLAYING":

            self.gameplay()

        elif self.state == "GAMEOVER":

            self.gameplay()
            self.draw_gameover()

        pygame.display.flip()

    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        running = True

        while running:

            dt = self.clock.tick(FPS) / 1000

            dt = min(dt, 0.05)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    running = False

                elif event.type == pygame.KEYDOWN:

                    self.handle_key(event.key)

            self.update(dt)

            self.render()

        pygame.quit()
        sys.exit()


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    game = BladeMaster()

    game.run()
 