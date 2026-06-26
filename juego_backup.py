import pygame
import math
import random
import sys
import array
import os

# --- CONFIGURACIÓN ---
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

ANCHO_LOGICO, ALTO_LOGICO = 1280, 720
GRID_SIZE = 32
GRID_W = ANCHO_LOGICO // GRID_SIZE
GRID_H = ALTO_LOGICO // GRID_SIZE

# Detectar si es móvil por variable de entorno o tamaño de pantalla
ES_MOVIL = os.environ.get("KIVY_CORE_METRICS_DENSITY", "").lower() == "medium" or pygame.display.get_surface() is None
if ES_MOVIL:
    flags = pygame.FULLSCREEN
else:
    flags = pygame.FULLSCREEN | pygame.SCALED
VENTANA = pygame.display.set_mode((ANCHO_LOGICO, ALTO_LOGICO), flags)
pygame.display.set_caption("Rogue Tower: Master Edition")

# --- PALETA ---
COLORS = {
    "ui_bg": (43, 29, 14),
    "ui_border": (181, 142, 58),
    "text": (255, 250, 240),
    "btn_hover": (80, 50, 30),
    "btn_normal": (60, 40, 20),
    "btn_upgrade": (50, 100, 180),
    "grass_light": (58, 163, 68),
    "grass_dark": (45, 135, 55),
    "path_bosque": (194, 178, 128),
    "tree_trunk": (101, 67, 33),
    "tree_leaves": (34, 100, 34),
    "desert_light": (237, 201, 175),
    "desert_dark": (210, 180, 140),
    "sand_path": (180, 150, 120),
    "cactus": (46, 139, 87),
    "stone_light": (130, 130, 140),
    "stone_mid": (100, 100, 110),
    "stone_dark": (70, 70, 80),
    "wood_door": (101, 67, 33),
    "wood_detail": (70, 45, 20),
    "banner": (180, 40, 40),
}

font_ui = pygame.font.SysFont("Verdana", 10)
font_md = pygame.font.SysFont("Verdana", 12, bold=True)
font_lg = pygame.font.SysFont("Verdana", 24, bold=True)
font_xl = pygame.font.SysFont("Verdana", 40, bold=True)

PERFIL_JUGADOR = {
    "niveles_desbloqueados": 1,
    "oro_global": 0,
    "mejoras": {
        "dano": 0,
        "oro": 0,
        "torres": 0,
        "upg_veneno": 0,
        "upg_fuego": 0,
        "upg_arcana": 0,
    },
}

ARBOLES_MEJORAS = {
    "dano": [
        {"nombre": "Afilado I", "costo": 200, "desc": "Daño Global +10%"},
        {"nombre": "Afilado II", "costo": 500, "desc": "Daño Global +20%"},
        {"nombre": "Afilado III", "costo": 1000, "desc": "Daño Global +40%"},
    ],
    "oro": [
        {"nombre": "Codicia I", "costo": 200, "desc": "Oro x Kill +20%"},
        {"nombre": "Codicia II", "costo": 600, "desc": "Oro x Kill +40%"},
        {"nombre": "Codicia III", "costo": 1200, "desc": "Oro x Kill +70%"},
    ],
    "torres": [
        {"nombre": "Desbloqueo Tóxica", "costo": 300, "desc": "Habilita la Torre Tóxica"},
        {"nombre": "Desbloqueo Infernal", "costo": 800, "desc": "Habilita la Torre Infernal"},
        {"nombre": "Desbloqueo Arcana", "costo": 1500, "desc": "Habilita la Torre Arcana"},
    ],
    "upg_veneno": [
        {"nombre": "Toxina I", "costo": 300, "desc": "Daño base veneno +2"},
        {"nombre": "Toxina II", "costo": 600, "desc": "Duración de veneno +2 seg"},
        {"nombre": "Toxina III", "costo": 1200, "desc": "Daño base veneno +4"},
    ],
    "upg_fuego": [
        {"nombre": "Llama I", "costo": 400, "desc": "Daño de fuego +10"},
        {"nombre": "Llama II", "costo": 800, "desc": "Rango de ataque +20"},
        {"nombre": "Llama III", "costo": 1500, "desc": "Daño de fuego +20"},
    ],
    "upg_arcana": [
        {"nombre": "Runa I", "costo": 500, "desc": "Daño arcano +15"},
        {"nombre": "Runa II", "costo": 1000, "desc": "Vel. Ataque -10%"},
        {"nombre": "Runa III", "costo": 2500, "desc": "Daño en área (AoE)"},
    ],
}

TIPOS_TORRES = {
    "arquera": {
        "costo": 50,
        "rango": 120,
        "daño": 12,
        "cooldown": 35,
        "nombre": "Vigía",
        "color_top": (200, 180, 100),
        "color_side": (150, 130, 50),
        "altura": 28,
        "ancho": 20,
    },
    "canon": {
        "costo": 120,
        "rango": 100,
        "daño": 60,
        "cooldown": 90,
        "nombre": "Cañón",
        "color_top": (80, 80, 90),
        "color_side": (50, 50, 60),
        "altura": 24,
        "ancho": 24,
    },
    "hielo": {
        "costo": 80,
        "rango": 110,
        "daño": 5,
        "cooldown": 25,
        "nombre": "Frío",
        "color_top": (100, 240, 255),
        "color_side": (50, 150, 200),
        "altura": 32,
        "ancho": 20,
    },
    "veneno": {
        "costo": 150,
        "rango": 130,
        "daño": 4,
        "cooldown": 20,
        "nombre": "Tóxica",
        "color_top": (100, 255, 100),
        "color_side": (40, 100, 40),
        "altura": 30,
        "ancho": 18,
    },
    "fuego": {
        "costo": 200,
        "rango": 110,
        "daño": 25,
        "cooldown": 60,
        "nombre": "Infernal",
        "color_top": (255, 100, 50),
        "color_side": (150, 50, 20),
        "altura": 36,
        "ancho": 22,
    },
    "magia": {
        "costo": 250,
        "rango": 150,
        "daño": 45,
        "cooldown": 45,
        "nombre": "Arcana",
        "color_top": (180, 80, 255),
        "color_side": (100, 40, 150),
        "altura": 34,
        "ancho": 20,
    },
}

TIPOS_ENEMIGOS = {
    "goblin": {
        "hp": 20,
        "vel": 2.8,
        "reward": 5,
        "radio": 8,
        "nombre": "Goblin",
        "blindado": False,
    },
    "goblin_armor": {
        "hp": 40,
        "vel": 2.5,
        "reward": 8,
        "radio": 9,
        "nombre": "Goblin Blindado",
        "blindado": True,
    },
    "orco": {
        "hp": 60,
        "vel": 1.5,
        "reward": 15,
        "radio": 12,
        "nombre": "Orco",
        "blindado": False,
    },
    "orco_armor": {
        "hp": 120,
        "vel": 1.3,
        "reward": 25,
        "radio": 13,
        "nombre": "Orco Blindado",
        "blindado": True,
    },
    "golem": {
        "hp": 150,
        "vel": 0.8,
        "reward": 30,
        "radio": 16,
        "nombre": "Troll",
        "blindado": False,
    },
    "golem_armor": {
        "hp": 300,
        "vel": 0.7,
        "reward": 50,
        "radio": 17,
        "nombre": "Troll Blindado",
        "blindado": True,
    },
    "boss": {
        "hp": 1000,
        "vel": 0.5,
        "reward": 300,
        "radio": 35,
        "nombre": "REY OGRO",
        "blindado": True,
    },
}

CACHE_TORRES = {}

# --- UTILIDADES ---

def to_grid(px, py):
    return int(px // GRID_SIZE), int(py // GRID_SIZE)


def to_pixel(gx, gy):
    return gx * GRID_SIZE + GRID_SIZE // 2, gy * GRID_SIZE + GRID_SIZE // 2


def get_rect(gx, gy):
    return pygame.Rect(gx * GRID_SIZE, gy * GRID_SIZE, GRID_SIZE, GRID_SIZE)


def clamp(value, low, high):
    return max(low, min(high, value))


def draw_shadow(surf, x, y, radius):
    s = pygame.Surface((int(radius * 2.4), int(radius * 0.9)), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 80), s.get_rect())
    surf.blit(s, (x - radius * 1.2, y - radius * 0.45))


def shade(color, amount):
    return tuple(clamp(int(c + amount), 0, 255) for c in color)


def mix_color(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_gloss_ellipse(surf, color, rect, outline=(20, 20, 20), border=1):
    rect = pygame.Rect(rect)
    pygame.draw.ellipse(surf, shade(color, -28), rect)
    inner = pygame.Rect(rect)
    inner.inflate_ip(-max(2, rect.w // 8), -max(2, rect.h // 8))
    pygame.draw.ellipse(surf, color, inner)
    shine = pygame.Rect(rect.x + rect.w * 0.18, rect.y + rect.h * 0.12, rect.w * 0.38, rect.h * 0.2)
    pygame.draw.ellipse(surf, shade(color, 55), shine)
    pygame.draw.ellipse(surf, outline, rect, border)


def draw_iso_block(surf, x, y, w, h, depth, top_color, side_color, outline=(30, 25, 20)):
    left = x - w // 2
    right = x + w // 2
    top = y - h
    front = [(left, top + depth), (right, top + depth), (right, y), (left, y)]
    top_poly = [(left, top + depth), (x, top), (right, top + depth), (x, top + depth * 2)]
    side_poly = [(right, top + depth), (x, top + depth * 2), (x, y + depth), (right, y)]
    pygame.draw.polygon(surf, shade(side_color, -25), side_poly)
    pygame.draw.polygon(surf, side_color, front)
    pygame.draw.polygon(surf, top_color, top_poly)
    pygame.draw.polygon(surf, outline, front, 1)
    pygame.draw.polygon(surf, outline, top_poly, 1)
    pygame.draw.line(surf, shade(top_color, 40), (left + 3, top + depth + 1), (x, top + 2), 1)


class SoundManager:
    def __init__(self):
        self.sounds = {}
        self._create_sounds()

    def _create_wave(self, freq_start, freq_end, duration, volume=0.5, tipo="sine"):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array.array('h')
        for i in range(n_samples):
            t = i / n_samples
            freq = freq_start + (freq_end - freq_start) * t
            if tipo == "noise":
                val = random.uniform(-1, 1) * 32767 * volume
            else:
                phase = 2 * math.pi * freq * (i / sample_rate)
                if tipo == "square":
                    val = 32767 * volume if math.sin(phase) >= 0 else -32767 * volume
                else:
                    val = math.sin(phase) * 32767 * volume
            val *= (1 - t)
            buf.append(int(clamp(val, -32767, 32767)))
        return pygame.mixer.Sound(buffer=buf)

    def _create_sounds(self):
        self.sounds["shoot"] = self._create_wave(800, 400, 0.08, 0.22)
        self.sounds["canon"] = self._create_wave(220, 70, 0.22, 0.38, tipo="square")
        self.sounds["hit"] = self._create_wave(180, 120, 0.05, 0.28)
        self.sounds["build"] = self._create_wave(320, 580, 0.18, 0.3)
        self.sounds["click"] = self._create_wave(1000, 1000, 0.05, 0.12)
        self.sounds["poison"] = self._create_wave(620, 820, 0.16, 0.3)
        self.sounds["fire"] = self._create_wave(0, 0, 0.4, 0.28, tipo="noise")
        self.sounds["magia"] = self._create_wave(1500, 2100, 0.22, 0.2)
        self.sounds["boss_spawn"] = self._create_wave(100, 50, 1.0, 0.8)
        self.sounds["gold"] = self._create_wave(1180, 1480, 0.1, 0.15)
        self.sounds["buy_upgrade"] = self._create_wave(420, 780, 0.28, 0.4)

    def play(self, nombre):
        if nombre in self.sounds:
            self.sounds[nombre].play()

SONIDOS = SoundManager()


class PathBuilder:
    @staticmethod
    def connect_grid(start, end):
        path = []
        x, y = start
        ex, ey = end
        while x != ex:
            path.append((x, y))
            x += 1 if ex > x else -1
        while y != ey:
            path.append((x, y))
            y += 1 if ey > y else -1
        path.append((ex, ey))
        return [node for i, node in enumerate(path) if i == 0 or node != path[i-1]]

    @staticmethod
    def generate_random_segment(start, end, keypoints_count=3):
        sx, sy = start
        ex, ey = end
        keypoints = [start]
        for i in range(keypoints_count):
            prog = (i + 1) / (keypoints_count + 1)
            kx = clamp(int(sx + (ex - sx) * prog + random.randint(-5, 5)), 1, GRID_W - 2)
            ky = clamp(int(sy + (ey - sy) * prog + random.randint(-5, 5)), 1, GRID_H - 2)
            keypoints.append((kx, ky))
        keypoints.append(end)
        full = []
        for i in range(len(keypoints) - 1):
            trecho = PathBuilder.connect_grid(keypoints[i], keypoints[i + 1])
            full.extend(trecho[1:] if i > 0 else trecho)
        return full

    @staticmethod
    def generate_infinite_paths(dificultad):
        destino = (GRID_W - 2, GRID_H // 2)
        path1 = PathBuilder.generate_random_segment((0, random.randint(GRID_H // 4, GRID_H * 3 // 4)), destino, keypoints_count=4)
        caminos = [path1]
        if dificultad == "facil":
            return caminos
        if dificultad == "medio":
            m = random.randint(len(path1) // 2, len(path1) - 2)
            tramo = PathBuilder.generate_random_segment((0, random.randint(1, GRID_H - 2)), path1[m], 2)
            caminos.append(tramo + path1[m + 1 :])
        if dificultad == "dificil":
            idx_a, idx_b = random.sample(range(len(path1) // 4, len(path1) - 2), 2)
            camino_a = PathBuilder.generate_random_segment((0, random.randint(1, GRID_H // 3)), path1[idx_a], 2) + path1[idx_a + 1 :]
            camino_b = PathBuilder.generate_random_segment((0, random.randint(GRID_H * 2 // 3, GRID_H - 2)), path1[idx_b], 2) + path1[idx_b + 1 :]
            caminos.extend([camino_a, camino_b])
        return caminos


class Particle:
    def __init__(self, x, y, color, speed=2, size=3, duration=20):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, math.pi * 2)
        vel = random.uniform(speed * 0.8, speed * 1.4)
        self.vx = math.cos(angle) * vel
        self.vy = math.sin(angle) * vel
        self.size = size
        self.life = duration
        self.max_life = duration

    def update(self, mult=1):
        self.x += self.vx * mult
        self.y += self.vy * mult
        self.life -= 1 * mult

    def draw(self, surf):
        if self.life > 0:
            radius = int(self.size * (self.life / self.max_life))
            if radius > 0:
                pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), radius)


class FloatingText:
    def __init__(self, x, y, text, color=(255, 255, 255), crit=False):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = 45
        self.vy = -1.7 if crit else -0.9
        self.font = font_lg if crit else font_md

    def update(self, mult=1):
        self.y += self.vy * mult
        self.life -= 1 * mult

    def draw(self, surf):
        if self.life > 0:
            alpha = min(255, int(self.life * 8))
            img = self.font.render(self.text, True, self.color)
            img.set_alpha(alpha)
            surf.blit(img, (int(self.x - img.get_width() // 2), int(self.y)))


class Enemy:
    def __init__(self, tipo, oleada, caminos):
        self.tipo = tipo
        self.data = TIPOS_ENEMIGOS[tipo]
        self.path = random.choice(caminos)
        self.waypoint_index = 0
        self.x, self.y = to_pixel(*self.path[0])
        multiplier = 1.0 + oleada * (0.35 if "boss" in tipo else 0.25)
        self.max_health = int(self.data["hp"] * multiplier)
        self.health = self.max_health
        self.speed_base = self.data["vel"]
        self.progress = 0
        self.anim_frame = random.randint(0, 100)
        self.freeze_timer = 0
        self.poison_stacks = 0
        self.poison_timer = 0
        self.fire_timer = 0
        self.damage_tick = 0
        if "boss" in tipo:
            SONIDOS.play("boss_spawn")

    def update(self, mult, session):
        self.anim_frame += 1 * mult
        self.damage_tick += 1 * mult
        if self.damage_tick >= 60:
            self.damage_tick = 0
            if self.poison_timer > 0:
                poison_damage = 2 * self.poison_stacks
                if PERFIL_JUGADOR["mejoras"]["upg_veneno"] >= 1:
                    poison_damage += 2
                if PERFIL_JUGADOR["mejoras"]["upg_veneno"] >= 3:
                    poison_damage += 2
                self.health -= poison_damage
                session.texts.append(FloatingText(self.x, self.y - 30, str(poison_damage), (100, 255, 100)))
                self.poison_timer -= 60
            if self.fire_timer > 0:
                self.health -= 5
                session.texts.append(FloatingText(self.x, self.y - 30, "5", (255, 150, 0)))
                self.fire_timer -= 60
        speed = self.speed_base * mult
        if self.freeze_timer > 0:
            speed *= 0.45
            self.freeze_timer -= 1 * mult
        if self.waypoint_index < len(self.path) - 1:
            target_x, target_y = to_pixel(*self.path[self.waypoint_index + 1])
            dx = target_x - self.x
            dy = target_y - self.y
            dist_sq = dx * dx + dy * dy
            distance = math.sqrt(dist_sq) if dist_sq > 0 else 0
            self.progress = self.waypoint_index * 1000 + (1000 - distance)
            if dist_sq < speed * speed or distance == 0:
                self.x, self.y = target_x, target_y
                self.waypoint_index += 1
            else:
                self.x += dx / distance * speed
                self.y += dy / distance * speed
            return False
        return True

    def draw(self, surf):
        radius = self.data["radio"] * (2 if "boss" in self.tipo else 1)
        draw_shadow(surf, self.x, self.y, radius)
        base = self.tipo.split("_")[0]
        bounce = math.sin(self.anim_frame * 0.18) * 2
        scale = 2.0 if "boss" in self.tipo else 1.0
        if base == "goblin":
            self._draw_goblin(surf, bounce, scale)
        elif base == "orco":
            self._draw_orc(surf, bounce, scale)
        elif base == "golem":
            self._draw_golem(surf, bounce, scale)
        elif base == "boss":
            self._draw_boss(surf, bounce, scale)
        if self.data.get("blindado") and "boss" not in self.tipo:
            self._draw_armor_overlay(surf, bounce, scale)
        if self.poison_stacks > 0:
            for i in range(min(3, self.poison_stacks)):
                pygame.draw.circle(surf, (0, 255, 0), (int(self.x - 6 + i * 6), int(self.y - 32 * scale + bounce)), 2)
        if self.fire_timer > 0:
            pygame.draw.circle(surf, (255, 120, 0), (int(self.x + random.randint(-5, 5)), int(self.y - 22 * scale + bounce)), random.randint(1, 3))
        if "boss" not in self.tipo and self.health < self.max_health:
            health_width = int((self.health / self.max_health) * 28)
            pygame.draw.rect(surf, (80, 0, 0), (self.x - 14, self.y - 50 * scale, 28, 4))
            pygame.draw.rect(surf, (0, 220, 0), (self.x - 14, self.y - 50 * scale, max(0, health_width), 4))

    def _draw_goblin(self, surf, bounce, scale):
        body_color = (62, 174, 72)
        x = int(self.x)
        y = int(self.y + bounce)
        draw_gloss_ellipse(surf, (54, 58, 46), (x - int(8 * scale), y - int(20 * scale), int(16 * scale), int(19 * scale)), border=max(1, int(scale)))
        pygame.draw.polygon(surf, (42, 125, 50), [(x - int(8 * scale), y - int(15 * scale)), (x - int(17 * scale), y - int(12 * scale)), (x - int(8 * scale), y - int(10 * scale))])
        pygame.draw.polygon(surf, (42, 125, 50), [(x + int(8 * scale), y - int(15 * scale)), (x + int(17 * scale), y - int(12 * scale)), (x + int(8 * scale), y - int(10 * scale))])
        draw_gloss_ellipse(surf, body_color, (x - int(7 * scale), y - int(22 * scale), int(14 * scale), int(13 * scale)), border=max(1, int(scale)))
        pygame.draw.polygon(surf, (45, 145, 60), [(x, y - int(14 * scale)), (x + int(9 * scale), y - int(7 * scale)), (x, y - int(5 * scale))])
        pygame.draw.circle(surf, (20, 20, 18), (x - int(3 * scale), y - int(17 * scale)), int(2 * scale))
        pygame.draw.circle(surf, (20, 20, 18), (x + int(3 * scale), y - int(17 * scale)), int(2 * scale))
        pygame.draw.circle(surf, (240, 255, 180), (x - int(3 * scale), y - int(17 * scale)), max(1, int(scale)))
        pygame.draw.circle(surf, (240, 255, 180), (x + int(3 * scale), y - int(17 * scale)), max(1, int(scale)))
        pygame.draw.line(surf, (95, 58, 28), (x + int(10 * scale), y - int(2 * scale)), (x + int(17 * scale), y - int(23 * scale)), max(2, int(2 * scale)))
        pygame.draw.circle(surf, (110, 245, 255), (x + int(17 * scale), y - int(23 * scale)), int(4 * scale))
        pygame.draw.circle(surf, (245, 255, 255), (x + int(16 * scale), y - int(24 * scale)), max(1, int(scale)))

    def _draw_orc(self, surf, bounce, scale):
        x = int(self.x)
        y = int(self.y + bounce)
        
        # Cuerpo principal - más musculoso y oscuro
        body_color = (110, 70, 50)  # Marrón oscuro menazante
        pygame.draw.ellipse(surf, body_color, (x - int(12 * scale), y - int(26 * scale), int(24 * scale), int(26 * scale)))
        
        # Sombreado del cuerpo para efecto 3D
        pygame.draw.ellipse(surf, (80, 50, 35), (x - int(11 * scale), y - int(25 * scale), int(22 * scale), int(3 * scale)))
        pygame.draw.ellipse(surf, (60, 40, 30), (x - int(12 * scale), y - int(15 * scale), int(24 * scale), int(2 * scale)))
        
        # Músculos del pecho
        pygame.draw.circle(surf, (130, 85, 60), (x - int(6 * scale), y - int(18 * scale)), int(4 * scale))
        pygame.draw.circle(surf, (130, 85, 60), (x + int(6 * scale), y - int(18 * scale)), int(4 * scale))
        
        # Brazos musculosos
        pygame.draw.ellipse(surf, (100, 60, 40), (x - int(14 * scale), y - int(15 * scale), int(5 * scale), int(16 * scale)))
        pygame.draw.ellipse(surf, (100, 60, 40), (x + int(10 * scale), y - int(15 * scale), int(5 * scale), int(16 * scale)))
        
        # Manos/puños
        pygame.draw.circle(surf, (90, 50, 30), (x - int(14 * scale), y - int(2 * scale)), int(3 * scale))
        pygame.draw.circle(surf, (90, 50, 30), (x + int(15 * scale), y - int(2 * scale)), int(3 * scale))
        
        # Cabeza - más grande y amenazante
        head_color = (130, 90, 70)
        pygame.draw.circle(surf, head_color, (x, y - int(32 * scale)), int(8 * scale))
        
        # Sombreado de cabeza
        pygame.draw.ellipse(surf, (100, 70, 55), (x - int(7 * scale), y - int(34 * scale), int(14 * scale), int(3 * scale)))
        
        # Mandíbula pronunciada
        pygame.draw.ellipse(surf, (100, 65, 50), (x - int(7 * scale), y - int(26 * scale), int(14 * scale), int(5 * scale)))
        pygame.draw.line(surf, (70, 45, 35), (x - int(7 * scale), y - int(23 * scale)), (x + int(7 * scale), y - int(23 * scale)), int(2 * scale))
        
        # Ojos malvados - rojizos
        pygame.draw.circle(surf, (50, 30, 20), (x - int(3 * scale), y - int(34 * scale)), int(2 * scale))
        pygame.draw.circle(surf, (50, 30, 20), (x + int(3 * scale), y - int(34 * scale)), int(2 * scale))
        pygame.draw.circle(surf, (220, 50, 50), (x - int(3 * scale), y - int(34 * scale)), int(1 * scale))
        pygame.draw.circle(surf, (220, 50, 50), (x + int(3 * scale), y - int(34 * scale)), int(1 * scale))
        
        # Cuernos - amenazantes
        pygame.draw.line(surf, (80, 60, 40), (x - int(5 * scale), y - int(38 * scale)), (x - int(8 * scale), y - int(45 * scale)), int(2 * scale))
        pygame.draw.line(surf, (80, 60, 40), (x + int(5 * scale), y - int(38 * scale)), (x + int(8 * scale), y - int(45 * scale)), int(2 * scale))
        
        # Púas/espinas en los hombros
        for i in [-1, 1]:
            pygame.draw.polygon(surf, (140, 100, 70), [(x + int(i * 12 * scale), y - int(20 * scale)), (x + int(i * 15 * scale), y - int(22 * scale)), (x + int(i * 12 * scale), y - int(16 * scale))])

    def _draw_golem(self, surf, bounce, scale):
        x = int(self.x)
        y = int(self.y + bounce)
        w = int(24 * scale)
        h = int(28 * scale)
        draw_iso_block(surf, x, y, w, h, int(6 * scale), (145, 148, 154), (98, 100, 108))
        pygame.draw.line(surf, (62, 62, 68), (x - int(10 * scale), y - h + int(5 * scale)), (x + int(9 * scale), y - int(4 * scale)), int(2 * scale))
        pygame.draw.line(surf, (74, 54, 34), (x + int(9 * scale), y - h + int(2 * scale)), (x - int(8 * scale), y - int(8 * scale)), int(2 * scale))
        pygame.draw.circle(surf, (126, 128, 136), (x, y - int(32 * scale)), int(8 * scale))
        pygame.draw.circle(surf, (160, 165, 170), (x - int(2 * scale), y - int(35 * scale)), int(3 * scale))
        pygame.draw.circle(surf, (70, 230, 255), (x - int(3 * scale), y - int(32 * scale)), max(1, int(2 * scale)))
        pygame.draw.circle(surf, (70, 230, 255), (x + int(3 * scale), y - int(32 * scale)), max(1, int(2 * scale)))
        pygame.draw.line(surf, (200, 200, 180), (x - int(3 * scale), y - int(32 * scale)), (x - int(8 * scale), y - int(40 * scale)), int(2 * scale))
        pygame.draw.line(surf, (200, 200, 180), (x + int(3 * scale), y - int(32 * scale)), (x + int(8 * scale), y - int(40 * scale)), int(2 * scale))
        club_x, club_y = x - int(15 * scale), y - int(15 * scale)
        pygame.draw.line(surf, (90, 60, 40), (club_x, club_y), (club_x - int(6 * scale), club_y - int(15 * scale)), int(5 * scale))
        pygame.draw.circle(surf, (150, 150, 150), (club_x - int(6 * scale), club_y - int(15 * scale)), int(4 * scale))

    def _draw_armor_overlay(self, surf, bounce, scale):
        x = int(self.x)
        y = int(self.y + bounce)
        steel = (150, 158, 168)
        dark = (62, 68, 78)
        pygame.draw.arc(surf, shade(steel, 35), (x - int(13 * scale), y - int(31 * scale), int(26 * scale), int(18 * scale)), math.pi, math.pi * 2, max(2, int(2 * scale)))
        pygame.draw.rect(surf, steel, (x - int(9 * scale), y - int(24 * scale), int(18 * scale), int(10 * scale)), border_radius=int(3 * scale))
        pygame.draw.rect(surf, dark, (x - int(9 * scale), y - int(24 * scale), int(18 * scale), int(10 * scale)), max(1, int(scale)), border_radius=int(3 * scale))
        pygame.draw.line(surf, shade(steel, 45), (x - int(7 * scale), y - int(22 * scale)), (x + int(6 * scale), y - int(22 * scale)), max(1, int(scale)))
        pygame.draw.circle(surf, (220, 215, 170), (x, y - int(19 * scale)), max(1, int(2 * scale)))

    def _draw_boss(self, surf, bounce, scale):
        x = int(self.x)
        y = int(self.y + bounce)
        
        # CUERPO PRINCIPAL - Gigante y musculoso
        body_color = (80, 35, 35)  # Rojo sangre oscuro
        pygame.draw.rect(surf, body_color, (x - int(20 * scale), y - int(48 * scale), int(40 * scale), int(50 * scale)), border_radius=int(8 * scale))
        
        # Sombreado gradual del cuerpo
        pygame.draw.rect(surf, (60, 25, 25), (x - int(20 * scale), y - int(48 * scale), int(40 * scale), int(4 * scale)), border_radius=int(8 * scale))
        pygame.draw.rect(surf, (50, 20, 20), (x - int(20 * scale), y - int(30 * scale), int(40 * scale), int(2 * scale)))
        
        # Pecho - músculos definidos
        pygame.draw.circle(surf, (100, 45, 45), (x - int(7 * scale), y - int(30 * scale)), int(6 * scale))
        pygame.draw.circle(surf, (100, 45, 45), (x + int(7 * scale), y - int(30 * scale)), int(6 * scale))
        pygame.draw.line(surf, (60, 25, 25), (x, y - int(36 * scale)), (x, y - int(20 * scale)), int(2 * scale))
        
        # Brazos gigantescos
        pygame.draw.ellipse(surf, (90, 40, 40), (x - int(22 * scale), y - int(25 * scale), int(6 * scale), int(28 * scale)))
        pygame.draw.ellipse(surf, (90, 40, 40), (x + int(17 * scale), y - int(25 * scale), int(6 * scale), int(28 * scale)))
        
        # Puños enormes de guerra
        pygame.draw.circle(surf, (100, 50, 50), (x - int(22 * scale), y + int(2 * scale)), int(5 * scale))
        pygame.draw.circle(surf, (100, 50, 50), (x + int(22 * scale), y + int(2 * scale)), int(5 * scale))
        
        # CABEZA - Enorme y aterradora
        head_color = (110, 55, 55)
        pygame.draw.circle(surf, head_color, (x, y - int(52 * scale)), int(14 * scale))
        
        # Sombreado de cabeza 3D
        pygame.draw.ellipse(surf, (80, 40, 40), (x - int(12 * scale), y - int(56 * scale), int(24 * scale), int(4 * scale)))
        pygame.draw.ellipse(surf, (60, 30, 30), (x - int(10 * scale), y - int(52 * scale), int(20 * scale), int(2 * scale)))
        
        # Mandíbula prominente y amenazante
        pygame.draw.ellipse(surf, (90, 45, 45), (x - int(11 * scale), y - int(42 * scale), int(22 * scale), int(8 * scale)))
        pygame.draw.line(surf, (60, 25, 25), (x - int(11 * scale), y - int(37 * scale)), (x + int(11 * scale), y - int(37 * scale)), int(2 * scale))
        
        # OJOS - Terroríficos con brillo demoníaco
        # Blanco del ojo
        pygame.draw.circle(surf, (255, 255, 255), (x - int(6 * scale), y - int(54 * scale)), int(3 * scale))
        pygame.draw.circle(surf, (255, 255, 255), (x + int(6 * scale), y - int(54 * scale)), int(3 * scale))
        # Pupila roja
        pygame.draw.circle(surf, (200, 20, 20), (x - int(5 * scale), y - int(54 * scale)), int(2 * scale))
        pygame.draw.circle(surf, (200, 20, 20), (x + int(7 * scale), y - int(54 * scale)), int(2 * scale))
        # Brillo mágico
        pygame.draw.circle(surf, (255, 100, 100), (x - int(5 * scale), y - int(55 * scale)), int(1 * scale))
        pygame.draw.circle(surf, (255, 100, 100), (x + int(7 * scale), y - int(55 * scale)), int(1 * scale))
        
        # CUERNOS - Enormes y curvos
        pygame.draw.line(surf, (60, 40, 30), (x - int(8 * scale), y - int(62 * scale)), (x - int(14 * scale), y - int(72 * scale)), int(3 * scale))
        pygame.draw.line(surf, (60, 40, 30), (x + int(8 * scale), y - int(62 * scale)), (x + int(14 * scale), y - int(72 * scale)), int(3 * scale))
        # Tips de cuernos - amenazantes
        pygame.draw.circle(surf, (40, 25, 15), (x - int(14 * scale), y - int(72 * scale)), int(2 * scale))
        pygame.draw.circle(surf, (40, 25, 15), (x + int(14 * scale), y - int(72 * scale)), int(2 * scale))
        
        # CORONA/CORONA DE PODER - Aspecto aterrador
        crown_y = y - int(68 * scale)
        pygame.draw.polygon(surf, (200, 160, 20), [(x - int(16 * scale), crown_y), (x - int(12 * scale), crown_y - int(8 * scale)), (x - int(6 * scale), crown_y), (x, crown_y - int(10 * scale)), (x + int(6 * scale), crown_y), (x + int(12 * scale), crown_y - int(8 * scale)), (x + int(16 * scale), crown_y)])
        pygame.draw.polygon(surf, (150, 120, 10), [(x - int(16 * scale), crown_y), (x - int(12 * scale), crown_y - int(8 * scale)), (x - int(6 * scale), crown_y), (x, crown_y - int(10 * scale)), (x + int(6 * scale), crown_y), (x + int(12 * scale), crown_y - int(8 * scale)), (x + int(16 * scale), crown_y)], 2)
        
        # Joyas en la corona - brillan
        for offset in [-8, 0, 8]:
            pygame.draw.circle(surf, (255, 50, 50), (x + int(offset * scale), crown_y - int(5 * scale)), int(2 * scale))
            pygame.draw.circle(surf, (255, 100, 100), (x + int(offset * scale), crown_y - int(5 * scale)), int(1 * scale))
        
        # PÚAS/ESPINAS - Por todo el cuerpo
        spikes = [(x - int(18 * scale), y - int(20 * scale)), (x + int(18 * scale), y - int(20 * scale)), (x - int(18 * scale), y - int(10 * scale)), (x + int(18 * scale), y - int(10 * scale))]
        for spike_x, spike_y in spikes:
            pygame.draw.polygon(surf, (150, 70, 70), [(spike_x, spike_y), (spike_x - int(2 * scale), spike_y - int(6 * scale)), (spike_x + int(2 * scale), spike_y - int(6 * scale))])
        
        # ARMA - Hacha de poder
        axe_x = x + int(26 * scale)
        axe_y = y - int(10 * scale)
        pygame.draw.line(surf, (60, 50, 30), (axe_x, axe_y + int(20 * scale)), (axe_x, axe_y - int(35 * scale)), int(3 * scale))
        pygame.draw.rect(surf, (150, 100, 50), (axe_x - int(8 * scale), axe_y - int(35 * scale), int(16 * scale), int(8 * scale)), border_radius=int(2 * scale))
        pygame.draw.rect(surf, (200, 150, 70), (axe_x - int(7 * scale), axe_y - int(34 * scale), int(14 * scale), int(2 * scale)))
        pygame.draw.circle(surf, (180, 180, 180), (axe_x, axe_y - int(35 * scale)), int(4 * scale))

    def is_dead(self):
        return self.health <= 0


class Tower:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.stats = TIPOS_TORRES[tipo]
        self.level = 1
        self.timer = 0
        self._apply_global_improvements()

    def _apply_global_improvements(self):
        boost = 1.0 + 0.10 * PERFIL_JUGADOR["mejoras"]["dano"]
        if PERFIL_JUGADOR["mejoras"]["dano"] == 3:
            boost = 1.40
        self.damage = int(self.stats["daño"] * boost)
        self.range = self.stats["rango"]
        self.cooldown = self.stats["cooldown"]
        if self.tipo == "fuego":
            if PERFIL_JUGADOR["mejoras"]["upg_fuego"] >= 1:
                self.damage += 10
            if PERFIL_JUGADOR["mejoras"]["upg_fuego"] >= 2:
                self.range += 20
            if PERFIL_JUGADOR["mejoras"]["upg_fuego"] >= 3:
                self.damage += 20
        elif self.tipo == "magia":
            if PERFIL_JUGADOR["mejoras"]["upg_arcana"] >= 1:
                self.damage += 15
            if PERFIL_JUGADOR["mejoras"]["upg_arcana"] >= 2:
                self.cooldown = max(5, int(self.cooldown * 0.9))
        self.range_sq = self.range * self.range
        self.rect = pygame.Rect(self.x - 15, self.y - 15, 30, 30)
        SONIDOS.play("build")

    def upgrade_cost(self):
        return int(self.stats["costo"] * (0.8 * self.level))

    def upgrade(self):
        self.level += 1
        self.damage = int(self.damage * 1.25)
        self.cooldown = max(5, int(self.cooldown * 0.95))
        self.range = int(self.range * 1.05)
        self.range_sq = self.range * self.range
        SONIDOS.play("build")

    def can_attack(self, enemy):
        dx = enemy.x - self.x
        dy = enemy.y - self.y
        return dx * dx + dy * dy <= self.range_sq

    def update(self, session):
        if self.timer > 0:
            self.timer -= 1
            return
        targets = [e for e in session.enemies if self.can_attack(e)]
        if not targets:
            return
        target = max(targets, key=lambda enemy: enemy.progress)
        projectile_x = self.x
        projectile_y = self.y - (self.stats["altura"] + self.level * 1.2)
        session.projectiles.append(Projectile(projectile_x, projectile_y, target, self.damage, self.tipo))
        self.timer = self.cooldown
        sound = {
            "canon": "canon",
            "veneno": "poison",
            "fuego": "fire",
            "magia": "magia",
        }.get(self.tipo, "shoot")
        SONIDOS.play(sound)

    def draw(self, surf):
        self._draw_pseudo3d_tower(surf)

    def _draw_pseudo3d_tower(self, surf):
        key = f"{self.tipo}_{self.level}"
        if key not in CACHE_TORRES:
            data = self.stats
            h = int(data["altura"] + self.level * 1.5)
            w = data["ancho"] + 20
            surf_img = pygame.Surface((w + 34, h + 42), pygame.SRCALPHA)
            cx = surf_img.get_width() // 2
            cy = surf_img.get_height() - 8
            pygame.draw.ellipse(surf_img, (0, 0, 0, 85), (cx - w // 2 - 6, cy - 10, w + 12, 14))
            draw_iso_block(surf_img, cx, cy, w + 10, 12, 7, shade(data["color_side"], 22), shade(data["color_side"], -24))
            draw_iso_block(surf_img, cx, cy - 8, w, h, 8, shade(data["color_top"], 10), data["color_side"])
            for stripe in range(3):
                sx = cx - w // 2 + 7 + stripe * max(7, w // 4)
                pygame.draw.line(surf_img, shade(data["color_side"], -35), (sx, cy - h + 7), (sx, cy - 11), 1)
                pygame.draw.line(surf_img, shade(data["color_side"], 38), (sx + 1, cy - h + 7), (sx + 1, cy - 11), 1)
            top = pygame.Rect(cx - w // 2 + 3, cy - h - 19, w - 6, 14)
            pygame.draw.ellipse(surf_img, shade(data["color_top"], -25), top.move(0, 4))
            pygame.draw.ellipse(surf_img, data["color_top"], top)
            pygame.draw.ellipse(surf_img, shade(data["color_top"], 60), (top.x + 5, top.y + 2, max(8, top.w // 2), 4))
            pygame.draw.ellipse(surf_img, (20, 20, 20), top, 1)
            if self.tipo == "arquera":
                pygame.draw.polygon(surf_img, (124, 72, 42), [(cx - 14, cy - h - 16), (cx + 6, cy - h - 34), (cx + 24, cy - h - 16)])
                pygame.draw.polygon(surf_img, (214, 186, 94), [(cx - 9, cy - h - 17), (cx + 6, cy - h - 29), (cx + 19, cy - h - 17)])
                pygame.draw.line(surf_img, (70, 42, 24), (cx + 6, cy - h - 32), (cx + 6, cy - h - 17), 2)
            elif self.tipo == "canon":
                pygame.draw.rect(surf_img, (42, 42, 48), (cx - 6, cy - h - 18, 24, 10), border_radius=4)
                pygame.draw.circle(surf_img, (16, 16, 18), (cx + 18, cy - h - 13), 6)
                pygame.draw.line(surf_img, (130, 130, 140), (cx - 3, cy - h - 16), (cx + 15, cy - h - 16), 2)
            elif self.tipo == "hielo":
                pygame.draw.polygon(surf_img, (220, 255, 255), [(cx, cy - h - 30), (cx - 12, cy - h - 10), (cx + 12, cy - h - 10)])
                pygame.draw.polygon(surf_img, (105, 210, 255), [(cx, cy - h - 30), (cx + 12, cy - h - 10), (cx + 1, cy - h - 14)])
                pygame.draw.line(surf_img, (255, 255, 255), (cx - 3, cy - h - 25), (cx - 9, cy - h - 12), 2)
            elif self.tipo == "veneno":
                pygame.draw.rect(surf_img, (22, 72, 30), (cx - 8, cy - h - 19, 16, 14), border_radius=5)
                pygame.draw.circle(surf_img, (70, 255, 110), (cx, cy - h - 22), 6)
                pygame.draw.circle(surf_img, (210, 255, 190), (cx - 2, cy - h - 24), 2)
                pygame.draw.circle(surf_img, (95, 205, 70), (cx + 9, cy - h - 11), 3)
            elif self.tipo == "fuego":
                pygame.draw.polygon(surf_img, (255, 90, 25), [(cx - 11, cy - h - 14), (cx + 10, cy - h - 14), (cx + 3, cy - h - 38), (cx - 3, cy - h - 26)])
                pygame.draw.polygon(surf_img, (255, 220, 80), [(cx - 5, cy - h - 15), (cx + 5, cy - h - 15), (cx, cy - h - 30)])
                pygame.draw.circle(surf_img, (255, 140, 0), (cx, cy - h - 20), 5)
            elif self.tipo == "magia":
                pygame.draw.circle(surf_img, (120, 60, 170), (cx, cy - h - 18), 13)
                pygame.draw.circle(surf_img, (220, 140, 255), (cx, cy - h - 20), 9)
                pygame.draw.circle(surf_img, (255, 255, 255), (cx - 3, cy - h - 23), 3)
                pygame.draw.arc(surf_img, (255, 210, 255), (cx - 15, cy - h - 34, 30, 30), 0.1, 2.9, 1)
            for i in range(self.level):
                pygame.draw.circle(surf_img, (255, 225, 70), (cx - 8 + i * 6, cy - h + 8), 2)
                pygame.draw.circle(surf_img, (120, 82, 18), (cx - 8 + i * 6, cy - h + 8), 2, 1)
            CACHE_TORRES[key] = (surf_img, cx, cy)
        image, anc_x, anc_y = CACHE_TORRES[key]
        surf.blit(image, (int(self.x - anc_x), int(self.y - anc_y)))


class Projectile:
    def __init__(self, x, y, target, damage, tipo):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.tipo = tipo
        self.active = True
        self.speed = 16 if tipo == "magia" else 12

    def update(self, session, mult=1):
        if not self.active or self.target.is_dead():
            self.active = False
            return None
        tx = self.target.x
        ty = self.target.y - 10
        dx = tx - self.x
        dy = ty - self.y
        dist_sq = dx * dx + dy * dy
        step = self.speed * mult
        if dist_sq < step * step or dist_sq == 0:
            self._hit(session)
            self.active = False
            return "hit"
        distance = math.sqrt(dist_sq)
        self.x += dx / distance * step
        self.y += dy / distance * step
        return None

    def _hit(self, session):
        self.target.health -= self.damage
        color = {
            "fuego": (255, 100, 0),
            "hielo": (100, 200, 255),
            "canon": (255, 80, 80),
            "magia": (255, 120, 255),
        }.get(self.tipo, (255, 255, 255))
        session.texts.append(FloatingText(self.target.x, self.target.y - 15, str(self.damage), color, crit=self.tipo in ["canon", "magia"]))
        for _ in range(7 if self.tipo in ["canon", "magia"] else 4):
            session.vfx.append(Particle(self.target.x, self.target.y, color, speed=3 if self.tipo in ["canon", "magia"] else 1.4, size=2))
        if self.tipo == "hielo":
            self.target.freeze_timer = 90
        elif self.tipo == "veneno":
            self.target.poison_stacks += 1
            self.target.poison_timer = 300 + (120 if PERFIL_JUGADOR["mejoras"]["upg_veneno"] >= 2 else 0)
        elif self.tipo == "fuego":
            self.target.fire_timer = 180
        if self.tipo == "magia" and PERFIL_JUGADOR["mejoras"]["upg_arcana"] >= 3:
            for enemy in session.enemies:
                if enemy is not self.target:
                    if (enemy.x - self.target.x) ** 2 + (enemy.y - self.target.y) ** 2 < 80 ** 2:
                        splash = int(self.damage * 0.5)
                        enemy.health -= splash
                        session.texts.append(FloatingText(enemy.x, enemy.y - 15, str(splash), (200, 50, 200)))
                        for _ in range(4):
                            session.vfx.append(Particle(enemy.x, enemy.y, (255, 120, 255), speed=2))
        SONIDOS.play("hit")

    def draw(self, surf):
        color = {
            "hielo": (140, 230, 255),
            "veneno": (100, 255, 100),
            "fuego": (255, 130, 0),
            "magia": (255, 100, 255),
        }.get(self.tipo, (255, 255, 180))
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), 4 if self.tipo == "magia" else 3)


class GameSession:
    def __init__(self, modo, max_waves=None, nivel=1, dificultad_infinita="facil"):
        self.modo = modo
        self.max_waves = max_waves
        self.nivel = nivel
        self.dificultad = dificultad_infinita
        self.selected_tower = None
        self._build_map()
        self._reset_state()
        self._create_ui_buttons()
        self._render_background()
        self.start_wave()

    def _build_map(self):
        self.es_desierto = self.modo == "campana" and self.nivel == 5
        if self.modo == "infinito":
            self.paths = PathBuilder.generate_infinite_paths(self.dificultad)
            self.bg_color = COLORS["grass_light"]
            self.grid_color = COLORS["grass_dark"]
            self.path_color = COLORS["path_bosque"]
        else:
            self.paths = [CAMINO_BOSQUE] if not self.es_desierto else [RUTA_1, RUTA_2, RUTA_3]
            self.bg_color = COLORS["desert_light"] if self.es_desierto else COLORS["grass_light"]
            self.grid_color = COLORS["desert_dark"] if self.es_desierto else COLORS["grass_dark"]
            self.path_color = COLORS["sand_path"] if self.es_desierto else COLORS["path_bosque"]
        self.path_cells = {cell for path in self.paths for cell in path}
        self.decorations = []
        goal = self.paths[0][-1]
        for _ in range(40):
            dx = random.randint(1, GRID_W - 2)
            dy = random.randint(1, GRID_H - 2)
            if (dx, dy) not in self.path_cells and abs(dx - goal[0]) >= 3 and abs(dy - goal[1]) >= 3:
                self.decorations.append(to_pixel(dx, dy))

    def _reset_state(self):
        self.money = 450
        self.lives = 20
        self.wave = 1
        self.gold_earned = 0
        self.enemies = []
        self.towers = []
        self.projectiles = []
        self.vfx = []
        self.texts = []
        self.spawn_timer = 0
        self.enemies_remaining = 0
        self.boss_target = None
        self.state = "JUGANDO"
        self.paused = False
        self.speed = 1
        self.tower_choice = "arquera"

    def _create_ui_buttons(self):
        # Botón unificado de menú/salida - más grande para móvil
        self.btn_menu = pygame.Rect(10, 10, 120, 40)
        self.btn_speed = pygame.Rect(ANCHO_LOGICO - 180, 10, 60, 25)
        self.btn_pause = pygame.Rect(ANCHO_LOGICO - 100, 10, 60, 25)
        self.btn_upgrade = pygame.Rect(ANCHO_LOGICO // 2 - 70, ALTO_LOGICO - 70, 140, 45)
        unlocked = PERFIL_JUGADOR["mejoras"]["torres"]
        available = ["arquera", "canon", "hielo"]
        if unlocked >= 1:
            available.append("veneno")
        if unlocked >= 2:
            available.append("fuego")
        if unlocked >= 3:
            available.append("magia")
        self.tower_buttons = []
        start_x = (ANCHO_LOGICO - (len(available) * 110 - 10)) // 2
        for i, tipo in enumerate(available):
            self.tower_buttons.append({"rect": pygame.Rect(start_x + i * 110, ALTO_LOGICO - 80, 100, 65), "tipo": tipo})

    def _render_background(self):
        self.background = pygame.Surface((ANCHO_LOGICO, ALTO_LOGICO))
        self.background.fill(self.bg_color)
        for gx in range(GRID_W):
            for gy in range(GRID_H):
                cell = (gx, gy)
                rect = get_rect(gx, gy)
                if cell in self.path_cells:
                    pygame.draw.rect(self.background, self.path_color, rect)
                    edge_color = shade(self.path_color, -30)
                    if (gx - 1, gy) not in self.path_cells:
                        pygame.draw.line(self.background, edge_color, rect.topleft, rect.bottomleft, 2)
                    if (gx + 1, gy) not in self.path_cells:
                        pygame.draw.line(self.background, edge_color, rect.topright, rect.bottomright, 2)
                    if (gx, gy - 1) not in self.path_cells:
                        pygame.draw.line(self.background, shade(self.path_color, 18), rect.topleft, rect.topright, 2)
                    if (gx, gy + 1) not in self.path_cells:
                        pygame.draw.line(self.background, edge_color, rect.bottomleft, rect.bottomright, 2)
                    for k in range(3):
                        px = rect.x + ((gx * 17 + gy * 29 + k * 11) % GRID_SIZE)
                        py = rect.y + ((gx * 31 + gy * 13 + k * 7) % GRID_SIZE)
                        pebble = shade(self.path_color, -20 if k % 2 else 24)
                        pygame.draw.circle(self.background, pebble, (px, py), 1)
                else:
                    base = self.grid_color if (gx + gy) % 2 == 0 else self.bg_color
                    pygame.draw.rect(self.background, base, rect)
                    tint = shade(base, 16 if (gx * 3 + gy * 5) % 4 == 0 else -10)
                    if self.es_desierto:
                        pygame.draw.line(self.background, tint, (rect.x + 4, rect.y + 8), (rect.x + 26, rect.y + 4), 1)
                        pygame.draw.line(self.background, shade(base, -18), (rect.x + 7, rect.y + 24), (rect.x + 28, rect.y + 28), 1)
                    else:
                        for k in range(2):
                            bx = rect.x + ((gx * 19 + gy * 7 + k * 14) % GRID_SIZE)
                            by = rect.y + ((gx * 11 + gy * 23 + k * 9) % GRID_SIZE)
                            pygame.draw.line(self.background, tint, (bx, by), (bx + 3, by - 5), 1)
                    pygame.draw.rect(self.background, shade(base, -18), rect, 1)
        for px, py in self.decorations:
            if self.es_desierto:
                self._draw_cactus(self.background, px, py)
            else:
                self._draw_tree(self.background, px, py)
        castle_x, castle_y = to_pixel(*self.paths[0][-1])
        draw_shadow(self.background, castle_x, castle_y + 10, 70)
        self._draw_castle(self.background, castle_x, castle_y)

    def start_wave(self):
        self.boss_target = None
        if self.modo == "campana" and self.wave > self.max_waves:
            self.state = "VICTORIA"
            if self.nivel == PERFIL_JUGADOR["niveles_desbloqueados"]:
                PERFIL_JUGADOR["niveles_desbloqueados"] += 1
            PERFIL_JUGADOR["oro_global"] += self.gold_earned
            return
        self.enemies_remaining = 1 if self.wave % 5 == 0 else 5 + self.wave * 2

    def update(self):
        if self.state != "JUGANDO" or self.paused:
            return
        for _ in range(1 if self.speed == 1 else 2):
            if self.enemies_remaining > 0:
                self.spawn_timer += 1
                if self.spawn_timer > 60:
                    self.spawn_timer = 0
                    enemy_type = self._choose_enemy_type()
                    enemy = Enemy(enemy_type, self.wave, self.paths)
                    self.enemies.append(enemy)
                    if "boss" in enemy_type:
                        self.boss_target = enemy
                    self.enemies_remaining -= 1
            elif not self.enemies:
                self.wave += 1
                self.start_wave()
            for tower in self.towers:
                tower.update(self)
            for projectile in self.projectiles[:]:
                result = projectile.update(self)
                if not projectile.active:
                    self.projectiles.remove(projectile)
            for enemy in self.enemies[:]:
                if enemy.is_dead():
                    self._handle_enemy_killed(enemy)
                    continue
                arrived = enemy.update(1, self)
                if arrived:
                    self.enemies.remove(enemy)
                    if enemy is self.boss_target:
                        self.boss_target = None
                    self.lives -= 5 if "boss" in enemy.tipo else 1
                    if self.lives <= 0:
                        self.state = "DERROTA"
                        PERFIL_JUGADOR["oro_global"] += self.gold_earned
            for v in self.vfx[:]:
                v.update(1)
                if v.life <= 0:
                    self.vfx.remove(v)
            for text in self.texts[:]:
                text.update(1)
                if text.life <= 0:
                    self.texts.remove(text)

    def _choose_enemy_type(self):
        if self.wave % 5 == 0:
            return "boss"
        if self.wave < 3:
            return "goblin"
        probability = random.random()
        if self.wave < 6:
            return "goblin" if probability < 0.7 else "orco"
        if probability < 0.4:
            return "goblin"
        if probability < 0.8:
            return "orco"
        return "golem"

    def _gold_multiplier(self):
        level = PERFIL_JUGADOR["mejoras"]["oro"]
        return 1.0 + (0.2 * level if level < 3 else 0.7)

    def _handle_enemy_killed(self, enemy):
        reward = int(enemy.data["reward"] * self._gold_multiplier())
        self.money += reward
        self.gold_earned += reward
        SONIDOS.play("gold")
        self.texts.append(FloatingText(enemy.x, enemy.y, f"+${reward}", (255, 215, 0)))
        for _ in range(10):
            self.vfx.append(Particle(enemy.x, enemy.y, (255, 220, 0), speed=2))
        if enemy is self.boss_target:
            self.boss_target = None
        if enemy in self.enemies:
            self.enemies.remove(enemy)

    def draw(self):
        VENTANA.blit(self.background, (0, 0))
        if self.selected_tower:
            overlay = pygame.Surface((self.selected_tower.range * 2, self.selected_tower.range * 2), pygame.SRCALPHA)
            pygame.draw.circle(overlay, (255, 255, 255, 32), (self.selected_tower.range, self.selected_tower.range), self.selected_tower.range)
            VENTANA.blit(overlay, (self.selected_tower.x - self.selected_tower.range, self.selected_tower.y - self.selected_tower.range))
        for obj in sorted(self.enemies + self.towers, key=lambda item: getattr(item, "y", 0)):
            if isinstance(obj, Enemy):
                obj.draw(VENTANA)
            else:
                obj.draw(VENTANA)
        for projectile in self.projectiles:
            projectile.draw(VENTANA)
        for v in self.vfx:
            v.draw(VENTANA)
        for text in self.texts:
            text.draw(VENTANA)
        if self.boss_target:
            self._draw_boss_bar()
        self._draw_ui()
        if self.state != "JUGANDO":
            self._draw_end_overlay()

    def _draw_ui(self):
        pygame.draw.rect(VENTANA, COLORS["ui_bg"], (0, ALTO_LOGICO - 90, ANCHO_LOGICO, 90))
        pygame.draw.line(VENTANA, COLORS["ui_border"], (0, ALTO_LOGICO - 90), (ANCHO_LOGICO, ALTO_LOGICO - 90), 3)
        mx, my = pygame.mouse.get_pos()
        
        # Botón unificado de MENU/SALIR arriba a la izquierda (mejorado)
        btn_color = COLORS["btn_hover"] if self.btn_menu.collidepoint(mx, my) else (150, 50, 50)
        pygame.draw.rect(VENTANA, btn_color, self.btn_menu, border_radius=5)
        pygame.draw.rect(VENTANA, (200, 100, 100), self.btn_menu, 2, border_radius=5)
        menu_text = font_md.render("MENU/X", True, COLORS["text"])
        VENTANA.blit(menu_text, (self.btn_menu.centerx - menu_text.get_width() // 2, self.btn_menu.centery - menu_text.get_height() // 2))
        
        if self.selected_tower:
            tower = self.selected_tower
            cost = tower.upgrade_cost()
            pygame.draw.rect(VENTANA, COLORS["btn_normal"], self.btn_upgrade, border_radius=8)
            pygame.draw.rect(VENTANA, COLORS["ui_border"], self.btn_upgrade, 2, border_radius=8)
            label = font_lg.render(f"{TIPOS_TORRES[tower.tipo]['nombre']} Lv{tower.level}", True, COLORS["text"])
            VENTANA.blit(label, (50, ALTO_LOGICO - 65))
            color = COLORS["btn_upgrade"] if self.money >= cost else (100, 100, 100)
            pygame.draw.rect(VENTANA, color, self.btn_upgrade, border_radius=8)
            pygame.draw.rect(VENTANA, COLORS["ui_border"], self.btn_upgrade, 2, border_radius=8)
            txt = font_md.render(f"UPGRADE ${cost}", True, COLORS["text"])
            VENTANA.blit(txt, (self.btn_upgrade.centerx - txt.get_width() // 2, self.btn_upgrade.centery - txt.get_height() // 2))
            VENTANA.blit(font_ui.render("Click fuera para cancelar", True, (170, 170, 170)), (self.btn_upgrade.right + 10, ALTO_LOGICO - 50))
        else:
            for btn in self.tower_buttons:
                rect = btn["rect"]
                tipo = btn["tipo"]
                data = TIPOS_TORRES[tipo]
                active = self.tower_choice == tipo
                color = COLORS["btn_hover"] if rect.collidepoint(mx, my) else COLORS["btn_normal"]
                pygame.draw.rect(VENTANA, color, rect, border_radius=5)
                if active:
                    pygame.draw.rect(VENTANA, COLORS["ui_border"], (rect.x - 2, rect.y - 2, rect.w + 4, rect.h + 4), border_radius=5)
                pygame.draw.rect(VENTANA, COLORS["ui_border"], rect, 2, border_radius=5)
                pygame.draw.circle(VENTANA, data["color_top"], (rect.x + 20, rect.centery), 10)
                VENTANA.blit(font_ui.render(data["nombre"], True, COLORS["text"]), (rect.x + 35, rect.y + 12))
                VENTANA.blit(font_ui.render(f"${data['costo']}", True, (255, 215, 0)), (rect.x + 35, rect.y + 30))
        pygame.draw.rect(VENTANA, COLORS["btn_normal"], self.btn_pause, border_radius=5)
        VENTANA.blit(font_ui.render("PAUSA", True, COLORS["text"]), (self.btn_pause.x + 10, self.btn_pause.y + 5))
        pygame.draw.rect(VENTANA, COLORS["btn_normal"], self.btn_speed, border_radius=5)
        VENTANA.blit(font_ui.render(f"x{self.speed}", True, COLORS["text"]), (self.btn_speed.x + 20, self.btn_speed.y + 5))
        status = font_lg.render(f"Oro {self.money}   Vida {self.lives}   Oleada {self.wave}", True, COLORS["text"])
        VENTANA.blit(status, (120, 10))

    def _draw_end_overlay(self):
        overlay = pygame.Surface((ANCHO_LOGICO, ALTO_LOGICO), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        VENTANA.blit(overlay, (0, 0))
        title = font_xl.render(self.state, True, (255, 255, 255))
        VENTANA.blit(title, (ANCHO_LOGICO // 2 - title.get_width() // 2, ALTO_LOGICO // 2 - 60))
        earned = font_md.render(f"Oro conseguido: {self.gold_earned}", True, (255, 215, 0))
        continue_text = font_md.render("Click para volver al menú", True, (210, 210, 210))
        VENTANA.blit(earned, (ANCHO_LOGICO // 2 - earned.get_width() // 2, ALTO_LOGICO // 2))
        VENTANA.blit(continue_text, (ANCHO_LOGICO // 2 - continue_text.get_width() // 2, ALTO_LOGICO // 2 + 40))

    def _draw_boss_bar(self):
        bar_width = 400
        bar_height = 20
        x = ANCHO_LOGICO // 2 - bar_width // 2
        y = 110
        pygame.draw.rect(VENTANA, (50, 0, 0), (x, y, bar_width, bar_height))
        ratio = max(0.0, self.boss_target.health / self.boss_target.max_health)
        pygame.draw.rect(VENTANA, (200, 0, 0), (x, y, int(bar_width * ratio), bar_height))
        pygame.draw.rect(VENTANA, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        title = font_lg.render("¡¡REY OGRO!!", True, (200, 50, 50))
        VENTANA.blit(title, (ANCHO_LOGICO // 2 - title.get_width() // 2, 80))

    def click(self, mx, my):
        if self.state != "JUGANDO":
            SONIDOS.play("click")
            return "salir"
        if self.btn_menu.collidepoint(mx, my):
            SONIDOS.play("click")
            PERFIL_JUGADOR["oro_global"] += self.gold_earned
            return "salir"
        if self.btn_pause.collidepoint(mx, my):
            SONIDOS.play("click")
            self.paused = not self.paused
            return
        if self.btn_speed.collidepoint(mx, my):
            SONIDOS.play("click")
            self.speed = 2 if self.speed == 1 else 1
            return
        if my > ALTO_LOGICO - 90:
            SONIDOS.play("click")
            if self.selected_tower:
                if self.btn_upgrade.collidepoint(mx, my):
                    cost = self.selected_tower.upgrade_cost()
                    if self.money >= cost:
                        self.money -= cost
                        self.selected_tower.upgrade()
                return
            for btn in self.tower_buttons:
                if btn["rect"].collidepoint(mx, my):
                    self.tower_choice = btn["tipo"]
                    return
            return
        tower_hit = next((tower for tower in self.towers if tower.rect.collidepoint(mx, my)), None)
        if tower_hit:
            SONIDOS.play("click")
            self.selected_tower = tower_hit
            return
        self.selected_tower = None
        gx, gy = to_grid(mx, my)
        if self.money >= TIPOS_TORRES[self.tower_choice]["costo"]:
            if (gx, gy) not in self.path_cells and not any(to_grid(t.x, t.y) == (gx, gy) for t in self.towers):
                self.towers.append(Tower(*to_pixel(gx, gy), self.tower_choice))
                self.money -= TIPOS_TORRES[self.tower_choice]["costo"]
                SONIDOS.play("build")

    def _draw_tree(self, surf, x, y):
        draw_shadow(surf, x, y + 2, 14)
        pygame.draw.rect(surf, shade(COLORS["tree_trunk"], -22), (x - 5, y - 12, 10, 23), border_radius=2)
        pygame.draw.rect(surf, COLORS["tree_trunk"], (x - 4, y - 13, 7, 22), border_radius=2)
        pygame.draw.line(surf, shade(COLORS["tree_trunk"], 32), (x - 1, y - 11), (x - 1, y + 7), 1)
        pygame.draw.circle(surf, shade(COLORS["tree_leaves"], -22), (x, y - 17), 14)
        pygame.draw.circle(surf, COLORS["tree_leaves"], (x - 5, y - 20), 11)
        pygame.draw.circle(surf, (41, 122, 45), (x - 11, y - 11), 10)
        pygame.draw.circle(surf, (48, 136, 50), (x + 8, y - 11), 11)
        pygame.draw.circle(surf, (74, 166, 68), (x - 4, y - 24), 4)

    def _draw_cactus(self, surf, x, y):
        draw_shadow(surf, x, y + 18, 13)
        dark = shade(COLORS["cactus"], -28)
        light = shade(COLORS["cactus"], 36)
        pygame.draw.rect(surf, dark, (x - 6, y - 21, 12, 42), border_radius=6)
        pygame.draw.rect(surf, COLORS["cactus"], (x - 4, y - 22, 9, 41), border_radius=5)
        pygame.draw.line(surf, light, (x - 1, y - 18), (x - 1, y + 16), 1)
        pygame.draw.rect(surf, dark, (x - 13, y - 10, 9, 6), border_radius=3)
        pygame.draw.rect(surf, COLORS["cactus"], (x - 13, y - 20, 6, 16), border_radius=3)
        pygame.draw.line(surf, light, (x - 10, y - 17), (x - 10, y - 7), 1)
        pygame.draw.rect(surf, dark, (x + 4, y + 5, 10, 6), border_radius=3)
        pygame.draw.rect(surf, COLORS["cactus"], (x + 8, y - 6, 6, 17), border_radius=3)
        pygame.draw.line(surf, light, (x + 11, y - 3), (x + 11, y + 8), 1)
        for sy in range(y - 14, y + 16, 8):
            pygame.draw.circle(surf, (235, 225, 190), (x + 5, sy), 1)

    def _draw_castle(self, surf, cx, cy):
        def block(x, y, w, h, c1, c2):
            pygame.draw.rect(surf, c1, (x - w // 2, y - h, w, h))
            pygame.draw.rect(surf, COLORS["stone_dark"], (x - w // 2, y - h, w, h), 1)
            pygame.draw.rect(surf, c2, (x - w // 2, y - h - 5, w, 5))
            pygame.draw.rect(surf, COLORS["stone_dark"], (x - w // 2, y - h - 5, w, 5), 1)
        off_x = 50
        h_tower = 50
        h_wall = 30
        h_center = 40
        w_tower = 25
        block(cx - off_x, cy - 10 - 30, w_tower, h_tower, COLORS["stone_mid"], COLORS["stone_light"])
        block(cx + off_x, cy - 10 - 30, w_tower, h_tower, COLORS["stone_mid"], COLORS["stone_light"])
        pygame.draw.rect(surf, COLORS["stone_dark"], (cx - off_x + 10, cy - 10 - h_wall, off_x * 2 - 20, h_wall))
        pygame.draw.rect(surf, COLORS["stone_mid"], (cx - off_x + 10, cy - 10 - h_wall - 5, off_x * 2 - 20, 5))
        block(cx, cy - 15, 50, h_center, COLORS["stone_mid"], COLORS["stone_light"])
        pygame.draw.polygon(surf, COLORS["stone_dark"], [(cx - 25, cy - 15 - h_center), (cx + 25, cy - 15 - h_center), (cx, cy - 35 - h_center)])
        pygame.draw.rect(surf, COLORS["wood_door"], (cx - 15, cy + 10, 30, h_wall - 5))
        pygame.draw.line(surf, COLORS["wood_detail"], (cx, cy + 10), (cx, cy + h_wall + 5), 2)
        pygame.draw.rect(surf, (50, 50, 50), (cx - 15, cy + 15, 30, 5))
        pygame.draw.rect(surf, (50, 50, 50), (cx - 15, cy + h_wall - 5, 30, 5))
        for tx in [cx - off_x, cx + off_x]:
            pygame.draw.line(surf, COLORS["wood_detail"], (tx, cy + 10 - h_tower - 10), (tx, cy + 10 - h_tower - 35), 2)
            pygame.draw.polygon(surf, COLORS["banner"], [(tx, cy + 10 - h_tower - 35), (tx + 15, cy + 10 - h_tower - 30), (tx, cy + 10 - h_tower - 25)])


class SkillMenu:
    def __init__(self):
        self.btn_back = pygame.Rect(ANCHO_LOGICO // 2 - 150, ALTO_LOGICO - 70, 300, 50)
        self.titles = {
            "dano": "Poder Global",
            "oro": "Riqueza Global",
            "torres": "Ingeniería",
            "upg_veneno": "Maestría Tóxica",
            "upg_fuego": "Maestría Infernal",
            "upg_arcana": "Maestría Arcana",
        }

    def draw(self):
        VENTANA.fill(COLORS["ui_bg"])
        pygame.draw.rect(VENTANA, COLORS["ui_border"], (20, 20, ANCHO_LOGICO - 40, ALTO_LOGICO - 40), 3)
        title = font_xl.render("ÁRBOL DE HABILIDADES", True, COLORS["ui_border"])
        VENTANA.blit(title, (ANCHO_LOGICO // 2 - title.get_width() // 2, 30))
        gold = font_md.render(f"Oro: {PERFIL_JUGADOR['oro_global']}", True, (255, 215, 0))
        VENTANA.blit(gold, (ANCHO_LOGICO // 2 - gold.get_width() // 2, 65))
        mx, my = pygame.mouse.get_pos()
        rows = ["dano", "oro", "torres", "upg_veneno", "upg_fuego", "upg_arcana"]
        for row_index, key in enumerate(rows):
            y_base = 105 + row_index * 90
            locked = False
            if key == "upg_veneno" and PERFIL_JUGADOR["mejoras"]["torres"] < 1:
                locked = True
            elif key == "upg_fuego" and PERFIL_JUGADOR["mejoras"]["torres"] < 2:
                locked = True
            elif key == "upg_arcana" and PERFIL_JUGADOR["mejoras"]["torres"] < 3:
                locked = True
            color = COLORS["text"] if not locked else (140, 140, 140)
            VENTANA.blit(font_md.render(self.titles[key], True, color), (50, y_base))
            level = PERFIL_JUGADOR["mejoras"][key]
            for col_index, node in enumerate(ARBOLES_MEJORAS[key]):
                x_base = 320 + col_index * 300
                rect = pygame.Rect(x_base, y_base - 10, 220, 60)
                if locked:
                    state = "BLOQUEADO"
                elif col_index < level:
                    state = "COMPRADO"
                elif col_index == level:
                    state = "DISPONIBLE"
                else:
                    state = "BLOQUEADO"
                if col_index < len(ARBOLES_MEJORAS[key]) - 1:
                    line_color = (100, 255, 100) if state == "COMPRADO" else (100, 100, 100)
                    pygame.draw.line(VENTANA, line_color, (rect.right, rect.centery), (x_base + 300, rect.centery), 3)
                can_buy = PERFIL_JUGADOR["oro_global"] >= node["costo"]
                bg_color = (30, 80, 30) if state == "COMPRADO" else COLORS["btn_normal"]
                border_color = (100, 255, 100) if state == "COMPRADO" else COLORS["ui_border"]
                if state == "BLOQUEADO":
                    bg_color = (30, 20, 20)
                    border_color = (80, 80, 80)
                elif state == "DISPONIBLE":
                    if rect.collidepoint(mx, my) and can_buy:
                        bg_color = COLORS["btn_hover"]
                    border_color = (255, 215, 0)
                pygame.draw.rect(VENTANA, bg_color, rect, border_radius=6)
                pygame.draw.rect(VENTANA, border_color, rect, 2, border_radius=6)
                VENTANA.blit(font_md.render(node["nombre"], True, COLORS["text"] if state != "BLOQUEADO" else (160, 160, 160)), (rect.x + 8, rect.y + 5))
                VENTANA.blit(font_ui.render(node["desc"], True, (220, 220, 220) if state != "BLOQUEADO" else (120, 120, 120)), (rect.x + 8, rect.y + 25))
                if state == "COMPRADO":
                    VENTANA.blit(font_md.render("?", True, (100, 255, 100)), (rect.right - 25, rect.centery - 10))
                elif state == "DISPONIBLE":
                    cost_color = (255, 215, 0) if can_buy else (255, 100, 100)
                    VENTANA.blit(font_md.render(f"${node['costo']}", True, cost_color), (rect.x + 8, rect.bottom - 20))
        hover = COLORS["btn_hover"] if self.btn_back.collidepoint(mx, my) else COLORS["btn_normal"]
        pygame.draw.rect(VENTANA, hover, self.btn_back, border_radius=8)
        pygame.draw.rect(VENTANA, COLORS["ui_border"], self.btn_back, 2, border_radius=8)
        back_text = font_md.render("VOLVER AL MENÚ", True, COLORS["text"])
        VENTANA.blit(back_text, (self.btn_back.centerx - back_text.get_width() // 2, self.btn_back.centery - back_text.get_height() // 2))

    def click(self, mx, my):
        SONIDOS.play("click")
        if self.btn_back.collidepoint(mx, my):
            return "volver"
        rows = ["dano", "oro", "torres", "upg_veneno", "upg_fuego", "upg_arcana"]
        for row_index, key in enumerate(rows):
            locked = False
            if key == "upg_veneno" and PERFIL_JUGADOR["mejoras"]["torres"] < 1:
                locked = True
            elif key == "upg_fuego" and PERFIL_JUGADOR["mejoras"]["torres"] < 2:
                locked = True
            elif key == "upg_arcana" and PERFIL_JUGADOR["mejoras"]["torres"] < 3:
                locked = True
            if locked:
                continue
            level = PERFIL_JUGADOR["mejoras"][key]
            if level < len(ARBOLES_MEJORAS[key]):
                node = ARBOLES_MEJORAS[key][level]
                x_base = 320 + level * 300
                rect = pygame.Rect(x_base, 105 + row_index * 90 - 10, 220, 60)
                if rect.collidepoint(mx, my) and PERFIL_JUGADOR["oro_global"] >= node["costo"]:
                    PERFIL_JUGADOR["oro_global"] -= node["costo"]
                    PERFIL_JUGADOR["mejoras"][key] += 1
                    SONIDOS.play("buy_upgrade")
        return None


class MenuPrincipal:
    def __init__(self):
        self._load_background_image()
        self.btn_infinite = pygame.Rect(ANCHO_LOGICO // 2 - 150, 150, 300, 50)
        self.btn_campaign = pygame.Rect(ANCHO_LOGICO // 2 - 150, 220, 300, 50)
        self.btn_skills = pygame.Rect(ANCHO_LOGICO // 2 - 150, 290, 300, 50)
        self.btn_exit = pygame.Rect(ANCHO_LOGICO // 2 - 150, 600, 300, 50)
        self.campaign_mode = False
        self.difficulty_mode = False
        self.level_buttons = [
            {"rect": pygame.Rect(ANCHO_LOGICO // 2 - 200, 280 + i * 60, 400, 50), "id": i + 1, "text": f"Nivel {i + 1}: {'Bosque Antiguo' if i < 4 else 'DESIERTO (Final)'}"}
            for i in range(5)
        ]
        self.btn_diff_easy = pygame.Rect(ANCHO_LOGICO // 2 - 150, 250, 300, 60)
        self.btn_diff_medium = pygame.Rect(ANCHO_LOGICO // 2 - 150, 330, 300, 60)
        self.btn_diff_hard = pygame.Rect(ANCHO_LOGICO // 2 - 150, 410, 300, 60)
        self.btn_back = pygame.Rect(ANCHO_LOGICO // 2 - 150, 600, 300, 50)

    def _load_background_image(self):
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        menu_image = None
        for name in os.listdir(base_dir):
            if name.startswith("menu."):
                menu_image = os.path.join(base_dir, name)
                break
        self.bg_image = None
        if menu_image:
            try:
                self.bg_image = pygame.image.load(menu_image).convert()
                self.bg_image = pygame.transform.scale(self.bg_image, (ANCHO_LOGICO, ALTO_LOGICO))
            except Exception:
                self.bg_image = None

    def _draw_button(self, rect, text, active=True):
        mx, my = pygame.mouse.get_pos()
        col = COLORS["btn_hover"] if rect.collidepoint(mx, my) and active else COLORS["btn_normal"]
        if not active:
            col = (30, 20, 10)
        pygame.draw.rect(VENTANA, COLORS["ui_border"], (rect.x - 2, rect.y - 2, rect.w + 4, rect.h + 4), border_radius=8)
        pygame.draw.rect(VENTANA, col, rect, border_radius=8)
        text_img = font_lg.render(text, True, COLORS["text"] if active else (120, 120, 120))
        VENTANA.blit(text_img, (rect.centerx - text_img.get_width() // 2, rect.centery - text_img.get_height() // 2))

    def draw(self):
        if self.bg_image:
            VENTANA.blit(self.bg_image, (0, 0))
            fade = pygame.Surface((ANCHO_LOGICO, ALTO_LOGICO), pygame.SRCALPHA)
            fade.fill((0, 0, 0, 100))
            VENTANA.blit(fade, (0, 0))
        else:
            VENTANA.fill(COLORS["ui_bg"])
        pygame.draw.rect(VENTANA, COLORS["ui_border"], (40, 40, ANCHO_LOGICO - 80, ALTO_LOGICO - 80), 3)
        title_shadow = font_xl.render("ROGUE TOWER: GRID EDITION", True, (0, 0, 0))
        VENTANA.blit(title_shadow, (ANCHO_LOGICO // 2 - title_shadow.get_width() // 2 + 2, 52))
        title = font_xl.render("ROGUE TOWER: GRID EDITION", True, COLORS["ui_border"])
        VENTANA.blit(title, (ANCHO_LOGICO // 2 - title.get_width() // 2, 50))
        gold = font_lg.render(f"Oro Global: {PERFIL_JUGADOR['oro_global']}", True, (255, 215, 0))
        VENTANA.blit(gold, (50, 50))
        if self.difficulty_mode:
            label = font_lg.render("SELECCIONA DIFICULTAD", True, COLORS["text"])
            VENTANA.blit(label, (ANCHO_LOGICO // 2 - label.get_width() // 2, 150))
            self._draw_button(self.btn_diff_easy, "FÁCIL")
            self._draw_button(self.btn_diff_medium, "MEDIO")
            self._draw_button(self.btn_diff_hard, "DIFÍCIL")
            self._draw_button(self.btn_back, "VOLVER")
        elif not self.campaign_mode:
            self._draw_button(self.btn_infinite, "MODO INFINITO")
            self._draw_button(self.btn_campaign, "CAMPAÑA")
            self._draw_button(self.btn_skills, "SKILL TREE")
            self._draw_button(self.btn_exit, "SALIR")
        else:
            for button in self.level_buttons:
                unlocked = button["id"] <= PERFIL_JUGADOR["niveles_desbloqueados"]
                self._draw_button(button["rect"], button["text"] if unlocked else "BLOQUEADO", unlocked)
            self._draw_button(self.btn_back, "VOLVER")

    def click(self, mx, my):
        SONIDOS.play("click")
        if self.difficulty_mode:
            if self.btn_diff_easy.collidepoint(mx, my):
                return "inf_facil"
            if self.btn_diff_medium.collidepoint(mx, my):
                return "inf_medio"
            if self.btn_diff_hard.collidepoint(mx, my):
                return "inf_dificil"
            if self.btn_back.collidepoint(mx, my):
                self.difficulty_mode = False
            return None
        if not self.campaign_mode:
            if self.btn_infinite.collidepoint(mx, my):
                self.difficulty_mode = True
            elif self.btn_campaign.collidepoint(mx, my):
                self.campaign_mode = True
            elif self.btn_skills.collidepoint(mx, my):
                return "abrir_mejoras"
            elif self.btn_exit.collidepoint(mx, my):
                sys.exit()
            return None
        if self.btn_back.collidepoint(mx, my):
            self.campaign_mode = False
            return None
        for button in self.level_buttons:
            if button["rect"].collidepoint(mx, my) and button["id"] <= PERFIL_JUGADOR["niveles_desbloqueados"]:
                return f"lvl_{button['id']}"
        return None


def create_predefined_paths():
    def connect(a, b):
        return PathBuilder.connect_grid(a, b)
    kp_bosque = [(0, 5), (8, 5), (8, 15), (20, 15), (20, 8), (30, 8), (30, 12), (GRID_W - 1, 12)]
    bosque = []
    for i in range(len(kp_bosque) - 1):
        tramo = connect(kp_bosque[i], kp_bosque[i + 1])
        bosque.extend(tramo[:-1])
    bosque.append(kp_bosque[-1])
    final_pt = (GRID_W - 2, GRID_H // 2)
    mid_pt = (GRID_W // 2 + 5, GRID_H // 2)
    ruta1 = []
    for p1, p2 in zip([(0, 4), (10, 4), (15, 8), mid_pt], [(10, 4), (15, 8), mid_pt, final_pt]):
        tramo = connect(p1, p2)
        ruta1.extend(tramo[:-1])
    ruta1.append(final_pt)
    ruta2 = []
    for p1, p2 in zip([(0, GRID_H // 2), (10, GRID_H // 2), mid_pt], [(10, GRID_H // 2), mid_pt, final_pt]):
        tramo = connect(p1, p2)
        ruta2.extend(tramo[:-1])
    ruta2.append(final_pt)
    ruta3 = []
    for p1, p2 in zip([(0, GRID_H - 5), (10, GRID_H - 5), (15, GRID_H - 8), mid_pt], [(10, GRID_H - 5), (15, GRID_H - 8), mid_pt, final_pt]):
        tramo = connect(p1, p2)
        ruta3.extend(tramo[:-1])
    ruta3.append(final_pt)
    return bosque, ruta1, ruta2, ruta3

CAMINO_BOSQUE, RUTA_1, RUTA_2, RUTA_3 = create_predefined_paths()


def main():
    reloj = pygame.time.Clock()
    estado = "MENU"
    menu = MenuPrincipal()
    skills = SkillMenu()
    partida = None
    while True:
        reloj.tick(60)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                if estado == "JUEGO":
                    PERFIL_JUGADOR["oro_global"] += partida.gold_earned
                    estado = "MENU"
                    partida = None
                elif estado == "MEJORAS":
                    estado = "MENU"
                else:
                    sys.exit()
            # Soporte para mouse
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mx, my = pygame.mouse.get_pos()
                if estado == "MENU":
                    resultado = menu.click(mx, my)
                    if resultado == "abrir_mejoras":
                        estado = "MEJORAS"
                    elif resultado and resultado.startswith("inf_"):
                        dificultad = resultado.split("_")[1]
                        partida = GameSession("infinito", dificultad_infinita=dificultad)
                        estado = "JUEGO"
                        menu.difficulty_mode = False
                    elif resultado and resultado.startswith("lvl_"):
                        nivel = int(resultado.split("_")[1])
                        partida = GameSession("campana", max_waves=10 if nivel == 1 else 20, nivel=nivel)
                        estado = "JUEGO"
                elif estado == "MEJORAS":
                    if skills.click(mx, my) == "volver":
                        estado = "MENU"
                elif estado == "JUEGO":
                    if partida.click(mx, my) == "salir":
                        estado = "MENU"
                        partida = None
            # Soporte para táctil (FINGERDOWN)
            if evento.type == pygame.FINGERDOWN:
                mx = int(evento.x * ANCHO_LOGICO)
                my = int(evento.y * ALTO_LOGICO)
                if estado == "MENU":
                    resultado = menu.click(mx, my)
                    if resultado == "abrir_mejoras":
                        estado = "MEJORAS"
                    elif resultado and resultado.startswith("inf_"):
                        dificultad = resultado.split("_")[1]
                        partida = GameSession("infinito", dificultad_infinita=dificultad)
                        estado = "JUEGO"
                        menu.difficulty_mode = False
                    elif resultado and resultado.startswith("lvl_"):
                        nivel = int(resultado.split("_")[1])
                        partida = GameSession("campana", max_waves=10 if nivel == 1 else 20, nivel=nivel)
                        estado = "JUEGO"
                elif estado == "MEJORAS":
                    if skills.click(mx, my) == "volver":
                        estado = "MENU"
                elif estado == "JUEGO":
                    if partida.click(mx, my) == "salir":
                        estado = "MENU"
                        partida = None
        if estado == "MENU":
            menu.draw()
        elif estado == "MEJORAS":
            skills.draw()
        elif estado == "JUEGO":
            partida.update()
            partida.draw()
        pygame.display.flip()


if __name__ == "__main__":
    main()
