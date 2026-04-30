import pygame
import math
import random
import sys
import array
import os

# --- CONFIGURACIÓN E INICIALIZACIÓN ---
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1, buffer=512)

ANCHO_LOGICO, ALTO_LOGICO = 1280, 720
GRID_SIZE = 32
GRID_W = ANCHO_LOGICO // GRID_SIZE
GRID_H = ALTO_LOGICO // GRID_SIZE

flags = pygame.FULLSCREEN | pygame.SCALED
VENTANA = pygame.display.set_mode((ANCHO_LOGICO, ALTO_LOGICO), flags)
pygame.display.set_caption("Rogue Tower: Master Edition")

# --- PERFIL GLOBAL DEL JUGADOR Y ÁRBOLES DE MEJORAS ---
PERFIL_JUGADOR = {
    "niveles_desbloqueados": 1,
    "oro_global": 0,
    "mejoras": {
        "dano": 0,       # Daño Global
        "oro": 0,        # Oro Global
        "torres": 0,     # Desbloqueos de Torres
        "upg_veneno": 0, # Maestría Tóxica
        "upg_fuego": 0,  # Maestría Infernal
        "upg_arcana": 0  # Maestría Arcana
    }
}

ARBOLES_MEJORAS = {
    "dano": [
        {"nombre": "Afilado I", "costo": 200, "desc": "Daño Global +10%"},
        {"nombre": "Afilado II", "costo": 500, "desc": "Daño Global +20%"},
        {"nombre": "Afilado III", "costo": 1000, "desc": "Daño Global +40%"}
    ],
    "oro": [
        {"nombre": "Codicia I", "costo": 200, "desc": "Oro x Kill +20%"},
        {"nombre": "Codicia II", "costo": 600, "desc": "Oro x Kill +40%"},
        {"nombre": "Codicia III", "costo": 1200, "desc": "Oro x Kill +70%"}
    ],
    "torres": [
        {"nombre": "Desbloqueo Tóxica", "costo": 300, "desc": "Habilita la Torre Tóxica"},
        {"nombre": "Desbloqueo Infernal", "costo": 800, "desc": "Habilita la Torre Infernal"},
        {"nombre": "Desbloqueo Arcana", "costo": 1500, "desc": "Habilita la Torre Arcana"}
    ],
    "upg_veneno": [
        {"nombre": "Toxina I", "costo": 300, "desc": "Daño base veneno +2"},
        {"nombre": "Toxina II", "costo": 600, "desc": "Duración de veneno +2 seg"},
        {"nombre": "Toxina III", "costo": 1200, "desc": "Daño base veneno +4"}
    ],
    "upg_fuego": [
        {"nombre": "Llama I", "costo": 400, "desc": "Daño de fuego +10"},
        {"nombre": "Llama II", "costo": 800, "desc": "Rango de ataque +20"},
        {"nombre": "Llama III", "costo": 1500, "desc": "Daño de fuego +20"}
    ],
    "upg_arcana": [
        {"nombre": "Runa I", "costo": 500, "desc": "Daño arcano +15"},
        {"nombre": "Runa II", "costo": 1000, "desc": "Vel. Ataque (Cooldown -10%)"},
        {"nombre": "Runa III", "costo": 2500, "desc": "Daño en Área (AoE Splash)"}
    ]
}

# --- FUNCIONES AUXILIARES GRID ---
def to_grid(px, py): return int(px // GRID_SIZE), int(py // GRID_SIZE)
def to_pixel(gx, gy): return gx * GRID_SIZE + GRID_SIZE // 2, gy * GRID_SIZE + GRID_SIZE // 2
def get_rect(gx, gy): return pygame.Rect(gx * GRID_SIZE, gy * GRID_SIZE, GRID_SIZE, GRID_SIZE)

# --- SISTEMA DE SONIDO ---
class GeneradorSonidos:
    def __init__(self):
        self.sonidos = {}
        self.crear_sonidos()

    def crear_onda(self, freq_start, freq_end, duration, volume=0.5, tipo="sine"):
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buf = array.array('h')
        for i in range(n_samples):
            t = i / n_samples
            freq = freq_start + (freq_end - freq_start) * t
            if tipo == "noise": val = random.uniform(-1, 1) * 32767 * volume
            else: val = 32767 * volume if math.sin(2 * math.pi * freq * (i / sample_rate)) > 0 else -32767 * volume
            val *= (1 - t)
            buf.append(int(val))
        return pygame.mixer.Sound(buffer=buf)

    def crear_sonidos(self):
        self.sonidos["shoot"] = self.crear_onda(800, 400, 0.1, 0.2)
        self.sonidos["canon"] = self.crear_onda(200, 50, 0.3, 0.4)
        self.sonidos["hit"] = self.crear_onda(150, 100, 0.05, 0.3)
        self.sonidos["build"] = self.crear_onda(300, 600, 0.2, 0.3)
        self.sonidos["click"] = self.crear_onda(1000, 1000, 0.05, 0.1)
        self.sonidos["poison"] = self.crear_onda(600, 800, 0.15, 0.3)
        self.sonidos["fire"] = self.crear_onda(0, 0, 0.4, 0.3, tipo="noise")
        self.sonidos["magia"] = self.crear_onda(1500, 2000, 0.2, 0.2) 
        self.sonidos["boss_spawn"] = self.crear_onda(100, 50, 1.0, 0.8)
        self.sonidos["gold"] = self.crear_onda(1200, 1500, 0.1, 0.15) 
        self.sonidos["buy_upgrade"] = self.crear_onda(400, 800, 0.3, 0.4) 

    def play(self, nombre):
        if nombre in self.sonidos: self.sonidos[nombre].play()

SONIDOS = GeneradorSonidos()

# --- PALETA DE COLORES ---
C_UI_BG, C_UI_BORDER, C_TEXTO = (43, 29, 14), (181, 142, 58), (255, 250, 240)
C_BTN_HOVER, C_BTN_NORMAL, C_BTN_UPGRADE = (80, 50, 30), (60, 40, 20), (50, 100, 180)
C_CESPED_CLARO, C_CESPED_OSCURO, C_CAMINO = (58, 163, 68), (45, 135, 55), (194, 178, 128)
C_ARBOL_TRONCO, C_ARBOL_HOJAS = (101, 67, 33), (34, 100, 34)
C_ARENA_CLARO, C_ARENA_OSCURO, C_CAMINO_DESIERTO, C_CACTUS = (237, 201, 175), (210, 180, 140), (180, 150, 120), (46, 139, 87)
C_PIEDRA_CLARO, C_PIEDRA_MEDIO, C_PIEDRA_OSCURO = (130, 130, 140), (100, 100, 110), (70, 70, 80)
C_MADERA_PUERTA, C_MADERA_DETALLE, C_ESTANDARTE = (101, 67, 33), (70, 45, 20), (180, 40, 40)

# --- DATOS DEL JUEGO ---
TIPOS_TORRES = {
    "arquera": {"costo": 50, "rango": 120, "daño": 12, "cooldown": 35, "nombre": "Vigía", "color_top": (200, 180, 100), "color_side": (150, 130, 50), "altura": 25, "ancho": 18},
    "canon": {"costo": 120, "rango": 100, "daño": 60, "cooldown": 90, "nombre": "Cañón", "color_top": (80, 80, 90), "color_side": (50, 50, 60), "altura": 20, "ancho": 22},
    "hielo": {"costo": 80, "rango": 110, "daño": 5, "cooldown": 25, "nombre": "Hielo", "color_top": (100, 240, 255), "color_side": (50, 150, 200), "altura": 30, "ancho": 18},
    "veneno": {"costo": 150, "rango": 130, "daño": 4, "cooldown": 20, "nombre": "Tóxica", "color_top": (100, 255, 100), "color_side": (40, 100, 40), "altura": 28, "ancho": 16},
    "fuego": {"costo": 200, "rango": 110, "daño": 25, "cooldown": 60, "nombre": "Infernal", "color_top": (255, 100, 50), "color_side": (150, 50, 20), "altura": 35, "ancho": 20},
    "magia": {"costo": 250, "rango": 150, "daño": 45, "cooldown": 45, "nombre": "Arcana", "color_top": (180, 80, 255), "color_side": (100, 40, 150), "altura": 32, "ancho": 18}
}

TIPOS_ENEMIGOS = {
    "goblin":       {"hp": 20, "vel": 2.8, "reward": 5, "radio": 8, "nombre": "Goblin", "blindado": False},
    "goblin_armor": {"hp": 40, "vel": 2.5, "reward": 8, "radio": 9, "nombre": "Goblin Blindado", "blindado": True},
    "orco":         {"hp": 60, "vel": 1.5, "reward": 15, "radio": 12, "nombre": "Orco", "blindado": False},
    "orco_armor":   {"hp": 120, "vel": 1.3, "reward": 25, "radio": 13, "nombre": "Orco Blindado", "blindado": True},
    "golem":        {"hp": 150, "vel": 0.8, "reward": 30, "radio": 16, "nombre": "Troll", "blindado": False},
    "golem_armor":  {"hp": 300, "vel": 0.7, "reward": 50, "radio": 17, "nombre": "Troll Blindado", "blindado": True},
    "boss":         {"hp": 1000, "vel": 0.5, "reward": 300, "radio": 35, "nombre": "REY OGRO", "blindado": True}
}

font_ui = pygame.font.SysFont("Verdana", 10)
font_md = pygame.font.SysFont("Verdana", 12, bold=True) # Reducida para caber en 6 filas
font_lg = pygame.font.SysFont("Verdana", 24, bold=True)
font_xl = pygame.font.SysFont("Verdana", 40, bold=True)

# --- DEFINICIÓN DE CAMINOS ---
def connect_grid(p1, p2):
    path, gx, gy, ex, ey = [], p1[0], p1[1], p2[0], p2[1]
    while gx != ex: path.append((gx, gy)); gx += 1 if ex > gx else -1
    while gy != ey: path.append((gx, gy)); gy += 1 if ey > gy else -1
    path.append((ex, ey))
    clean = [path[0]]
    for i in range(1, len(path)):
        if path[i] != path[i-1]: clean.append(path[i])
    return clean

kp_bosque = [(0, 5), (8, 5), (8, 15), (20, 15), (20, 8), (30, 8), (30, 12), (GRID_W-1, 12)]
CAMINO_BOSQUE = sum([connect_grid(kp_bosque[i], kp_bosque[i+1])[:-1] for i in range(len(kp_bosque)-1)], []) + [kp_bosque[-1]]

final_pt, mid_pt = (GRID_W-2, GRID_H // 2), (GRID_W // 2 + 5, GRID_H // 2)
RUTA_1 = sum([connect_grid(p1, p2)[:-1] for p1, p2 in zip([(0, 4), (10, 4), (15, 8), mid_pt], [(10, 4), (15, 8), mid_pt, final_pt])], []) + [final_pt]
RUTA_2 = sum([connect_grid(p1, p2)[:-1] for p1, p2 in zip([(0, GRID_H//2), (10, GRID_H//2), mid_pt], [(10, GRID_H//2), mid_pt, final_pt])], []) + [final_pt]
RUTA_3 = sum([connect_grid(p1, p2)[:-1] for p1, p2 in zip([(0, GRID_H-5), (10, GRID_H-5), (15, GRID_H-8), mid_pt], [(10, GRID_H-5), (15, GRID_H-8), mid_pt, final_pt])], []) + [final_pt]

# --- CACHÉ DE DIBUJADO DE TORRES ---
CACHE_TORRES = {}
def obtener_imagen_torre(tipo, nivel):
    key = f"{tipo}_{nivel}"
    if key not in CACHE_TORRES:
        datos = TIPOS_TORRES[tipo]
        h, w = datos["altura"] + (nivel * 1.5), datos["ancho"]
        surf = pygame.Surface((w + 20, h + 10), pygame.SRCALPHA)
        c_top, c_side = datos["color_top"], datos["color_side"]
        cx, cy = surf.get_width() // 2, surf.get_height()
        
        rect_f = pygame.Rect(cx - w//2, cy - h, w, h)
        pygame.draw.rect(surf, c_side, rect_f)
        pygame.draw.rect(surf, (20,20,20), rect_f, 1)
        
        if tipo == "arquera": pygame.draw.polygon(surf, (150, 50, 50), [(cx - w//2 - 3, cy - h), (cx + w//2 + 3, cy - h), (cx, cy - h - 18)])
        elif tipo == "canon": pygame.draw.rect(surf, c_top, (cx - w//2, cy - h - 5, w, 10)); pygame.draw.circle(surf, (0,0,0), (cx, cy - h), 4)
        elif tipo == "hielo": pygame.draw.polygon(surf, c_top, [(cx, cy - h - 18), (cx - 6, cy - h - 6), (cx + 6, cy - h - 6)])
        elif tipo == "veneno": pygame.draw.rect(surf, c_top, (cx - 4, cy - h - 10, 8, 10)); pygame.draw.circle(surf, (0, 255, 0), (cx, cy - h - 12), 5)
        elif tipo == "fuego": pygame.draw.polygon(surf, c_top, [(cx - 6, cy - h), (cx + 6, cy - h), (cx, cy - h - 20)]); pygame.draw.circle(surf, (255, 50, 0), (cx, cy - h - 10), 4)
        elif tipo == "magia": 
            pygame.draw.polygon(surf, c_top, [(cx - 8, cy - h), (cx + 8, cy - h), (cx, cy - h - 15)])
            pygame.draw.circle(surf, (255, 100, 255), (cx, cy - h - 20), 6)

        for i in range(nivel): pygame.draw.circle(surf, (255, 255, 0), (cx - 6 + (i*5), cy - h + 5), 2)
        CACHE_TORRES[key] = (surf, cx, cy)
    return CACHE_TORRES[key]

# --- DIBUJADOS ESTÁTICOS ORIGINALES ---
def dibujar_arbol(surf, x, y):
    pygame.draw.rect(surf, C_ARBOL_TRONCO, (x-4, y-10, 8, 20))
    pygame.draw.circle(surf, C_ARBOL_HOJAS, (x, y-15), 12)
    pygame.draw.circle(surf, (40, 110, 40), (x-8, y-8), 9)
    pygame.draw.circle(surf, (40, 110, 40), (x+8, y-8), 9)

def dibujar_cactus(surf, x, y):
    pygame.draw.rect(surf, C_CACTUS, (x-5, y-20, 10, 40), border_radius=5)
    pygame.draw.rect(surf, C_CACTUS, (x-12, y-10, 8, 5), border_radius=2)
    pygame.draw.rect(surf, C_CACTUS, (x-12, y-20, 5, 15), border_radius=2)
    pygame.draw.rect(surf, C_CACTUS, (x+5, y+5, 8, 5), border_radius=2)
    pygame.draw.rect(surf, C_CACTUS, (x+8, y-5, 5, 15), border_radius=2)

def dibujar_castillo_completo(surf, cx, cy):
    cx_draw, cy_draw = cx, cy - 10
    def _bloque(x, y, w, h, c1, c2):
        pygame.draw.rect(surf, c1, (x - w//2, y - h, w, h)); pygame.draw.rect(surf, C_PIEDRA_OSCURO, (x - w//2, y - h, w, h), 1)
        pygame.draw.rect(surf, c2, (x - w//2, y - h - 5, w, 5)); pygame.draw.rect(surf, C_PIEDRA_OSCURO, (x - w//2, y - h - 5, w, 5), 1)
    off_x, off_y_back, off_y_front = 50, -30, 20
    h_torre, h_muro, h_centro, w_torre = 50, 30, 40, 25
    _bloque(cx_draw - off_x, cy_draw + off_y_back, w_torre, h_torre, C_PIEDRA_MEDIO, C_PIEDRA_CLARO)
    _bloque(cx_draw + off_x, cy_draw + off_y_back, w_torre, h_torre, C_PIEDRA_MEDIO, C_PIEDRA_CLARO)
    pygame.draw.rect(surf, C_PIEDRA_OSCURO, (cx_draw - off_x + 10, cy_draw + off_y_back - h_muro, off_x*2 - 20, h_muro))
    pygame.draw.rect(surf, C_PIEDRA_MEDIO, (cx_draw - off_x + 10, cy_draw + off_y_back - h_muro - 5, off_x*2 - 20, 5))
    _bloque(cx_draw, cy_draw - 5, 50, h_centro, C_PIEDRA_MEDIO, C_PIEDRA_CLARO)
    pygame.draw.polygon(surf, C_PIEDRA_OSCURO, [(cx_draw-25, cy_draw-h_centro-5), (cx_draw+25, cy_draw-h_centro-5), (cx_draw, cy_draw-h_centro-25)])
    _bloque(cx_draw + off_x, cy_draw + off_y_front, w_torre, h_torre, C_PIEDRA_MEDIO, C_PIEDRA_CLARO)
    pygame.draw.rect(surf, C_PIEDRA_OSCURO, (cx_draw + 15, cy_draw + off_y_front - h_muro, off_x - 15 - 10, h_muro))
    pygame.draw.rect(surf, C_PIEDRA_OSCURO, (cx_draw - off_x + 10, cy_draw + off_y_front - h_muro, off_x - 15 - 10, h_muro))
    rect_puerta = pygame.Rect(cx_draw - 15, cy_draw + off_y_front - h_muro + 5, 30, h_muro - 5)
    pygame.draw.rect(surf, C_MADERA_PUERTA, rect_puerta)
    pygame.draw.line(surf, C_MADERA_DETALLE, (cx_draw, rect_puerta.top), (cx_draw, rect_puerta.bottom), 2) 
    pygame.draw.rect(surf, (50,50,50), (cx_draw - 15, rect_puerta.top + 5, 30, 5))
    pygame.draw.rect(surf, (50,50,50), (cx_draw - 15, rect_puerta.bottom - 10, 30, 5))
    _bloque(cx_draw - off_x, cy_draw + off_y_front, w_torre, h_torre, C_PIEDRA_MEDIO, C_PIEDRA_CLARO)
    for tx in [cx_draw - off_x, cx_draw + off_x]:
        pygame.draw.line(surf, C_MADERA_DETALLE, (tx, cy_draw + off_y_front - h_torre - 10), (tx, cy_draw + off_y_front - h_torre - 35), 2)
        pygame.draw.polygon(surf, C_ESTANDARTE, [(tx, cy_draw + off_y_front - h_torre - 35), (tx + 15, cy_draw + off_y_front - h_torre - 30), (tx, cy_draw + off_y_front - h_torre - 25)])

def dibujar_sombra(surf, x, y, radio):
    s = pygame.Surface((int(radio*2.2), int(radio)), pygame.SRCALPHA)
    pygame.draw.ellipse(s, (0, 0, 0, 70), (0, 0, int(radio*2.2), int(radio)))
    surf.blit(s, (x - radio*1.1, y - radio//2))

def dibujar_monstruo(surf, x, y, enemigo):
    base_tipo = enemigo.tipo.split("_")[0] 
    bounce = math.sin(enemigo.anim_frame * 0.2) * 2
    scale = 2.0 if "boss" in enemigo.tipo else 1.0 
    
    if base_tipo == "goblin":
        pygame.draw.ellipse(surf, (70, 40, 70), (x-6*scale, y-(14*scale)+bounce, 12*scale, 14*scale))
        head_y = int(y-(16*scale)+bounce)
        pygame.draw.circle(surf, (60, 160, 60), (x, head_y), 5*scale)
        pygame.draw.polygon(surf, (60, 160, 60), [(x, head_y), (x+8*scale, head_y+2*scale), (x, head_y+4*scale)])
        pygame.draw.polygon(surf, (50, 30, 50), [(x-6*scale, head_y), (x+6*scale, head_y), (x-2*scale, head_y-10*scale)])
        staff_x = x + 8*scale
        pygame.draw.line(surf, (100, 70, 30), (staff_x, y+bounce), (staff_x, y-20*scale+bounce), 2)
        pygame.draw.circle(surf, (100, 255, 255), (int(staff_x), int(y-20*scale+bounce)), int(3 + math.sin(enemigo.anim_frame * 0.5) * 1))
    elif base_tipo == "orco":
        pygame.draw.ellipse(surf, (160, 120, 100), (x-10*scale, y-(22*scale)+bounce, 20*scale, 22*scale))
        pygame.draw.rect(surf, (80, 50, 20), (x-8*scale, y-(15*scale)+bounce, 16*scale, 8*scale))
        pygame.draw.circle(surf, (150, 150, 150), (x, int(y-(11*scale)+bounce)), 3*scale)
        head_y = int(y-(24*scale)+bounce)
        pygame.draw.circle(surf, (160, 120, 100), (x, head_y), 6*scale)
        pygame.draw.rect(surf, (100, 100, 100), (x-6*scale, head_y-6*scale, 12*scale, 5*scale))
        axe_x, axe_y = x + 12*scale, y - 10*scale + bounce
        pygame.draw.line(surf, (100, 70, 30), (axe_x, axe_y+5), (axe_x, axe_y-15), 3)
        pygame.draw.polygon(surf, (180, 180, 180), [(axe_x, axe_y-12), (axe_x+8, axe_y-8), (axe_x, axe_y-4)])
    elif base_tipo == "golem": 
        pygame.draw.rect(surf, (110, 110, 120), (x-12*scale, y-(28*scale)+bounce, 24*scale, 28*scale), border_radius=5)
        pygame.draw.line(surf, (50, 30, 10), (x-12*scale, y-(28*scale)+bounce), (x+12*scale, y-bounce), 3)
        pygame.draw.line(surf, (50, 30, 10), (x+12*scale, y-(28*scale)+bounce), (x-12*scale, y-bounce), 3)
        head_y = int(y-(32*scale)+bounce)
        pygame.draw.circle(surf, (100, 100, 110), (x, head_y), 7*scale)
        pygame.draw.line(surf, (200, 200, 180), (x-3*scale, head_y), (x-8*scale, head_y-8*scale), 2)
        pygame.draw.line(surf, (200, 200, 180), (x+3*scale, head_y), (x+8*scale, head_y-8*scale), 2)
        club_x, club_y = x - 15*scale, y - 15*scale + bounce
        pygame.draw.line(surf, (90, 60, 40), (club_x, club_y), (club_x-5, club_y-15), 5)
        pygame.draw.circle(surf, (150, 150, 150), (int(club_x-5), int(club_y-15)), 4)
    elif base_tipo == "boss":
        pygame.draw.rect(surf, (60, 20, 20), (x-15*scale, y-(40*scale)+bounce, 30*scale, 40*scale))
        pygame.draw.circle(surf, (200, 170, 50), (x, int(y-(25*scale)+bounce)), 10*scale)
        head_y = int(y-(45*scale)+bounce)
        pygame.draw.circle(surf, (80, 40, 40), (x, head_y), 12*scale)
        pygame.draw.polygon(surf, (255, 215, 0), [(x-12*scale, head_y-5), (x-6*scale, head_y-15), (x, head_y-5), (x+6*scale, head_y-15), (x+12*scale, head_y-5)])
        pygame.draw.line(surf, (50, 50, 50), (x+20*scale, y), (x+20*scale, y-40*scale), 4)
        pygame.draw.circle(surf, (200, 50, 50), (int(x+20*scale), int(y-40*scale)), 8*scale)

    if "armor" in enemigo.tipo:
        shoulder_y = y - (15 if base_tipo=="goblin" else 25)*scale + bounce
        pygame.draw.polygon(surf, (180, 180, 190), [(x-8*scale, shoulder_y), (x-12*scale, shoulder_y-5*scale), (x-4*scale, shoulder_y-5*scale)])
        pygame.draw.polygon(surf, (180, 180, 190), [(x+8*scale, shoulder_y), (x+12*scale, shoulder_y-5*scale), (x+4*scale, shoulder_y-5*scale)])

    if enemigo.veneno_stacks > 0:
        for i in range(min(3, enemigo.veneno_stacks)): pygame.draw.circle(surf, (0, 255, 0), (x - 6 + (i*6), int(y - 35*scale + bounce)), 2)
    if enemigo.fuego_timer > 0:
        pygame.draw.circle(surf, (255, 100, 0), (x + random.randint(-5, 5), y - 20*scale + bounce + random.randint(-5, 5)), random.randint(1, 3))

# --- VFX ---
class Particula:
    def __init__(self, x, y, color, speed=2, size=3, duration=20):
        self.x, self.y, self.color = x, y, color
        angle = random.uniform(0, math.pi * 2)
        vel = random.uniform(speed*0.5, speed*1.5)
        self.vx, self.vy = math.cos(angle) * vel, math.sin(angle) * vel
        self.size, self.vida, self.vida_max = size, duration, duration

    def update(self, mult=1):
        self.x += self.vx * mult; self.y += self.vy * mult; self.vida -= 1 * mult
    def draw(self, surf):
        if self.vida > 0:
            s = int(self.size * (self.vida / self.vida_max))
            if s > 0: pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), s)

class TextoFlotante:
    def __init__(self, x, y, texto, color=(255, 255, 255), is_crit=False):
        self.x, self.y, self.texto, self.color = x, y, texto, color
        self.vida = 45
        self.vy = -1.5 if is_crit else -0.8
        self.fuente = font_lg if is_crit else font_md

    def update(self, mult=1):
        self.y += self.vy * mult; self.vida -= 1 * mult
    def draw(self, surf):
        if self.vida > 0:
            alpha = min(255, self.vida * 10)
            t = self.fuente.render(self.texto, True, self.color)
            t.set_alpha(alpha)
            surf.blit(t, (int(self.x - t.get_width()//2), int(self.y)))

# --- CLASES LÓGICAS ---
class Enemigo:
    def __init__(self, tipo, oleada, caminos):
        self.tipo, self.datos = tipo, TIPOS_ENEMIGOS[tipo]
        self.camino_grid = random.choice(caminos)
        self.waypoint_index = 0
        self.x, self.y = to_pixel(*self.camino_grid[0])
        self.max_salud = int(self.datos["hp"] * (1.0 + oleada * (0.5 if "boss" in tipo else 0.3)))
        if "boss" in tipo: SONIDOS.play("boss_spawn")
        self.salud, self.velocidad_base = self.max_salud, self.datos["vel"]
        self.anim_frame = random.randint(0, 100)
        self.congelado_timer, self.veneno_stacks, self.veneno_timer, self.fuego_timer, self.tick_damage_timer = 0, 0, 0, 0, 0
        self.progreso = 0 

    def update(self, speed_mult, partida):
        self.anim_frame += 1 * speed_mult
        self.tick_damage_timer += 1 * speed_mult
        if self.tick_damage_timer >= 60:
            self.tick_damage_timer = 0
            if self.veneno_timer > 0:
                # Daño veneno modificado por UPG_VENENO
                dmg = 2 * self.veneno_stacks
                if PERFIL_JUGADOR["mejoras"]["upg_veneno"] >= 1: dmg += 2
                if PERFIL_JUGADOR["mejoras"]["upg_veneno"] >= 3: dmg += 2
                
                self.salud -= dmg
                partida.textos.append(TextoFlotante(self.x, self.y-30, str(dmg), (100, 255, 100)))
                self.veneno_timer -= 60
            if self.fuego_timer > 0:
                self.salud -= 5
                partida.textos.append(TextoFlotante(self.x, self.y-30, "5", (255, 150, 0)))
                self.fuego_timer -= 60
                
        speed = self.velocidad_base * speed_mult
        if self.congelado_timer > 0: speed *= 0.5; self.congelado_timer -= 1 * speed_mult
        
        if self.waypoint_index < len(self.camino_grid) - 1:
            tx, ty = to_pixel(*self.camino_grid[self.waypoint_index + 1])
            dist_sq = (tx - self.x)**2 + (ty - self.y)**2
            dist_real = math.sqrt(dist_sq) if dist_sq > 0 else 0
            self.progreso = (self.waypoint_index * 1000) + (1000 - dist_real)
            
            if dist_sq < speed**2: self.x, self.y = tx, ty; self.waypoint_index += 1
            else:
                self.x += (tx - self.x) / dist_real * speed
                self.y += (ty - self.y) / dist_real * speed
        else: return True
        return False

class Torre:
    def __init__(self, x, y, tipo):
        self.x, self.y, self.tipo, self.stats = x, y, tipo, TIPOS_TORRES[tipo]
        self.timer, self.nivel = 0, 1
        
        # APLICAMOS MEJORA GLOBAL DE DAÑO
        boost_global = 1.0 + (0.10 * PERFIL_JUGADOR["mejoras"]["dano"])
        if PERFIL_JUGADOR["mejoras"]["dano"] == 3: boost_global = 1.40
        
        self.danio = self.stats["daño"]
        self.rango = self.stats["rango"]
        self.cooldown = self.stats["cooldown"]
        
        # APLICAMOS MEJORAS ESPECÍFICAS DE TORRE
        if self.tipo == "fuego":
            if PERFIL_JUGADOR["mejoras"]["upg_fuego"] >= 1: self.danio += 10
            if PERFIL_JUGADOR["mejoras"]["upg_fuego"] >= 2: self.rango += 20
            if PERFIL_JUGADOR["mejoras"]["upg_fuego"] >= 3: self.danio += 20
        elif self.tipo == "magia":
            if PERFIL_JUGADOR["mejoras"]["upg_arcana"] >= 1: self.danio += 15
            if PERFIL_JUGADOR["mejoras"]["upg_arcana"] >= 2: self.cooldown = int(self.cooldown * 0.9)
            
        self.danio = int(self.danio * boost_global)
        self.rango_sq = self.rango ** 2 
        self.rect = pygame.Rect(x-15, y-15, 30, 30)
        SONIDOS.play("build")

    def calcular_costo_upgrade(self): return int(self.stats["costo"] * (0.8 * self.nivel))

    def mejorar(self):
        self.nivel += 1
        self.danio = int(self.danio * 1.25)
        self.cooldown = max(5, int(self.cooldown * 0.95))
        SONIDOS.play("build")

    def update(self, partida, speed_mult=1):
        if self.timer > 0:
            self.timer -= 1 * speed_mult
            return
        enemigos_en_rango = [e for e in partida.enemigos if (e.x - self.x)**2 + (e.y - self.y)**2 < self.rango_sq]
        if enemigos_en_rango:
            objetivo = max(enemigos_en_rango, key=lambda en: en.progreso)
            h = self.stats["altura"] + (self.nivel * 1.5)
            partida.proyectiles.append(Proyectil(self.x, self.y - h, objetivo, self.danio, self.tipo))
            self.timer = self.cooldown
            snd = "canon" if self.tipo=="canon" else "poison" if self.tipo=="veneno" else "fire" if self.tipo=="fuego" else "magia" if self.tipo=="magia" else "shoot"
            SONIDOS.play(snd)

class Proyectil:
    def __init__(self, x, y, target, danio, tipo):
        self.x, self.y, self.target, self.danio, self.tipo = x, y, target, danio, tipo
        self.activo = True
        self.velocidad = 15 if tipo == "magia" else 10

    def update(self, partida, speed_mult=1):
        if self.target.salud <= 0: self.activo = False; return None
        tx, ty = self.target.x, self.target.y - 10
        dist_x, dist_y = tx - self.x, ty - self.y
        dist_sq = dist_x**2 + dist_y**2
        paso = self.velocidad * speed_mult
        
        if dist_sq < paso**2:
            self.target.salud -= self.danio
            c_dmg = (255, 100, 0) if self.tipo=="fuego" else (100, 200, 255) if self.tipo=="hielo" else (255, 50, 50) if self.tipo=="canon" else (255, 100, 255) if self.tipo=="magia" else (255, 255, 255)
            partida.textos.append(TextoFlotante(tx, ty-15, str(self.danio), c_dmg, is_crit=(self.tipo in ["canon", "magia"])))
            for _ in range(5 if self.tipo not in ["canon", "magia"] else 15): partida.vfx.append(Particula(tx, ty, c_dmg, speed=3 if self.tipo in ["canon", "magia"] else 1.5))

            if self.tipo == "hielo": self.target.congelado_timer = 90
            elif self.tipo == "veneno": 
                self.target.veneno_stacks += 1
                duracion = 300
                if PERFIL_JUGADOR["mejoras"]["upg_veneno"] >= 2: duracion += 120 # +2s
                self.target.veneno_timer = duracion
            elif self.tipo == "fuego": self.target.fuego_timer = 180
            
            # --- NUEVO: AOE DE MAGIA TIER 3 ---
            if self.tipo == "magia" and PERFIL_JUGADOR["mejoras"]["upg_arcana"] >= 3:
                for e in partida.enemigos:
                    if e != self.target and (e.x - tx)**2 + (e.y - ty)**2 < 80**2: # Radio de explosión arcana
                        dmg_splash = int(self.danio * 0.5)
                        e.salud -= dmg_splash
                        partida.textos.append(TextoFlotante(e.x, e.y-15, str(dmg_splash), (200, 50, 200)))
                        for _ in range(3): partida.vfx.append(Particula(e.x, e.y, (255, 100, 255), speed=2))

            self.activo = False
            SONIDOS.play("hit")
            return "hit"
            
        dist = math.sqrt(dist_sq)
        self.x += (dist_x/dist) * paso; self.y += (dist_y/dist) * paso
        return None

# --- GENERADOR INFINITO ---
def generar_tramo_grid_aleatorio(pg_inicio, pg_fin, keypoints_count=3):
    sx, sy = pg_inicio; ex, ey = pg_fin
    keypoints = [pg_inicio]
    for i in range(keypoints_count):
        prog = (i + 1) / (keypoints_count + 1)
        kx = max(1, min(GRID_W-2, int(sx + (ex - sx) * prog + random.randint(-5, 5))))
        ky = max(1, min(GRID_H-2, int(sy + (ey - sy) * prog + random.randint(-5, 5))))
        keypoints.append((kx, ky))
    keypoints.append(pg_fin)
    full_path = []
    for i in range(len(keypoints)-1):
        tramo = connect_grid(keypoints[i], keypoints[i+1])
        full_path.extend(tramo[1:] if i > 0 else tramo)
    return full_path

def generar_caminos_infinito_grid(dificultad):
    final_pt = (GRID_W - 2, GRID_H // 2)
    path1 = generar_tramo_grid_aleatorio((0, random.randint(GRID_H//4, GRID_H*3//4)), final_pt, keypoints_count=4)
    caminos = [path1]
    if dificultad == "facil": return caminos
    elif dificultad == "medio":
        m_idx = random.randint(len(path1)//2, len(path1)-2)
        p2 = generar_tramo_grid_aleatorio((0, random.randint(1, GRID_H-2)), path1[m_idx], 2)
        caminos.append(p2 + path1[m_idx+1:])
    elif dificultad == "dificil":
        idx_a, idx_b = random.sample(range(len(path1)//4, len(path1)-2), 2)
        caminos.append(generar_tramo_grid_aleatorio((0, random.randint(1, GRID_H//3)), path1[idx_a], 2) + path1[idx_a+1:])
        caminos.append(generar_tramo_grid_aleatorio((0, random.randint(GRID_H*2//3, GRID_H-2)), path1[idx_b], 2) + path1[idx_b+1:])
    return caminos

# --- GESTOR DE PARTIDA ---
class Partida:
    def __init__(self, modo, max_oleadas=None, nivel=1, dificultad_infinita="facil"):
        self.modo, self.max_oleadas, self.nivel_campana = modo, max_oleadas, nivel
        self.es_desierto = False
        
        if self.modo == "infinito":
            self.caminos_grid = generar_caminos_infinito_grid(dificultad_infinita)
            self.color_fondo, self.color_grid, self.color_camino = C_CESPED_CLARO, C_CESPED_OSCURO, C_CAMINO
        else:
            self.es_desierto = (nivel == 5)
            if self.es_desierto: self.caminos_grid, self.color_fondo, self.color_grid, self.color_camino = [RUTA_1, RUTA_2, RUTA_3], C_ARENA_CLARO, C_ARENA_OSCURO, C_CAMINO_DESIERTO
            else: self.caminos_grid, self.color_fondo, self.color_grid, self.color_camino = [CAMINO_BOSQUE], C_CESPED_CLARO, C_CESPED_OSCURO, C_CAMINO
        
        self.celdas_camino_set = {celda for camino in self.caminos_grid for celda in camino}
        cgx, cgy = self.caminos_grid[0][-1]
        self.decoracion = []
        for _ in range(40):
            dgx, dgy = random.randint(1, GRID_W-2), random.randint(1, GRID_H-2)
            if (dgx, dgy) not in self.celdas_camino_set and (abs(dgx - cgx) >= 3 or abs(dgy - cgy) >= 3):
                self.decoracion.append(to_pixel(dgx, dgy))

        self.dinero, self.vidas, self.oleada = 450, 20, 1
        self.oro_acumulado = 0
        self.enemigos, self.torres, self.proyectiles, self.vfx, self.textos = [], [], [], [], []
        self.spawn_timer, self.enemigos_restantes, self.boss_actual = 0, 0, None 
        self.estado, self.pausa, self.velocidad = "JUGANDO", False, 1
        self.torre_ui_seleccionada = "arquera"
        self.torre_mapa_seleccionada = None
        
        self.btn_menu = pygame.Rect(10, 10, 80, 25)
        self.btn_speed = pygame.Rect(ANCHO_LOGICO - 180, 10, 60, 25)
        self.btn_pause = pygame.Rect(ANCHO_LOGICO - 100, 10, 60, 25)
        self.btn_upgrade = pygame.Rect(ANCHO_LOGICO//2 - 70, ALTO_LOGICO - 70, 140, 45)
        
        # OBTENER TORRES DESBLOQUEADAS
        nivel_torres = PERFIL_JUGADOR["mejoras"]["torres"]
        torres_disp = ["arquera", "canon", "hielo"]
        if nivel_torres >= 1: torres_disp.append("veneno")
        if nivel_torres >= 2: torres_disp.append("fuego")
        if nivel_torres >= 3: torres_disp.append("magia")
        
        self.btns_torres = []
        start_x = (ANCHO_LOGICO - (len(torres_disp) * 110 - 10)) // 2
        for i, k in enumerate(torres_disp):
            self.btns_torres.append({"rect": pygame.Rect(start_x + i*110, ALTO_LOGICO-80, 100, 65), "tipo": k})

        self.superficie_fondo = pygame.Surface((ANCHO_LOGICO, ALTO_LOGICO))
        self.pre_renderizar_fondo()
        self.iniciar_oleada()

    def pre_renderizar_fondo(self):
        self.superficie_fondo.fill(self.color_fondo)
        for gx in range(GRID_W):
            for gy in range(GRID_H):
                if (gx, gy) in self.celdas_camino_set: pygame.draw.rect(self.superficie_fondo, self.color_camino, get_rect(gx, gy))
                elif (gx + gy) % 2 == 0: pygame.draw.rect(self.superficie_fondo, self.color_grid, get_rect(gx, gy))

        for (dx, dy) in self.decoracion:
            if self.es_desierto: dibujar_cactus(self.superficie_fondo, dx, dy)
            else: dibujar_arbol(self.superficie_fondo, dx, dy)
        
        cx, cy = to_pixel(*self.caminos_grid[0][-1])
        dibujar_sombra(self.superficie_fondo, cx, cy+10, 70)
        dibujar_castillo_completo(self.superficie_fondo, cx, cy)

    def iniciar_oleada(self):
        self.boss_actual = None
        if self.modo == "campana" and self.oleada > self.max_oleadas:
            self.estado = "VICTORIA"
            if self.nivel_campana == PERFIL_JUGADOR["niveles_desbloqueados"]: PERFIL_JUGADOR["niveles_desbloqueados"] += 1
            PERFIL_JUGADOR["oro_global"] += self.oro_acumulado
            return
        self.enemigos_restantes = 1 if self.oleada % 5 == 0 else 5 + (self.oleada * 2)

    def update(self):
        if self.estado != "JUGANDO" or self.pausa: return
        for _ in range(1 if self.velocidad == 1 else 2):
            if self.enemigos_restantes > 0:
                self.spawn_timer += 1
                if self.spawn_timer > 60:
                    tipo_spawn = "boss" if self.oleada % 5 == 0 else "goblin"
                    if self.oleada % 5 != 0:
                        rnd = random.random()
                        if self.oleada < 3: tipo_spawn = "goblin"
                        elif self.oleada < 6: tipo_spawn = "goblin" if rnd < 0.7 else "orco"
                        else: tipo_spawn = "goblin" if rnd < 0.4 else "orco" if rnd < 0.8 else "golem"
                        if self.oleada >= 10 and random.random() < 0.4: tipo_spawn += "_armor"
                    
                    e = Enemigo(tipo_spawn, self.oleada, self.caminos_grid)
                    self.enemigos.append(e)
                    if "boss" in tipo_spawn: self.boss_actual = e
                    self.enemigos_restantes -= 1; self.spawn_timer = 0
            elif len(self.enemigos) == 0:
                self.oleada += 1; self.iniciar_oleada()

            for t in self.torres: t.update(self, 1)
            for p in self.proyectiles[:]:
                res = p.update(self, 1)
                if not p.activo: 
                    self.proyectiles.remove(p)
                    if res == "hit" and p.target.salud <= 0 and p.target in self.enemigos:
                        boost_oro = 1.0
                        if PERFIL_JUGADOR["mejoras"]["oro"] == 1: boost_oro = 1.20
                        elif PERFIL_JUGADOR["mejoras"]["oro"] == 2: boost_oro = 1.40
                        elif PERFIL_JUGADOR["mejoras"]["oro"] == 3: boost_oro = 1.70
                        
                        reward = int(p.target.datos["reward"] * boost_oro)
                        self.dinero += reward; self.oro_acumulado += reward
                        SONIDOS.play("gold")
                        self.textos.append(TextoFlotante(p.target.x, p.target.y, f"+${reward}", (255, 215, 0)))
                        for _ in range(10): self.vfx.append(Particula(p.target.x, p.target.y, (200, 30, 30), speed=2))
                        self.enemigos.remove(p.target)

            for e in self.enemigos[:]:
                llegado = e.update(1, self)
                if e.salud <= 0: 
                    self.enemigos.remove(e)
                    if e == self.boss_actual: self.boss_actual = None
                elif llegado:
                    self.vidas -= 5 if "boss" in e.tipo else 1
                    self.enemigos.remove(e)
                    if e == self.boss_actual: self.boss_actual = None
                    if self.vidas <= 0:
                        self.estado = "DERROTA"
                        PERFIL_JUGADOR["oro_global"] += self.oro_acumulado

            for v in self.vfx[:]: 
                v.update(1)
                if v.vida <= 0: self.vfx.remove(v)
            for tx in self.textos[:]: 
                tx.update(1)
                if tx.vida <= 0: self.textos.remove(tx)

    def dibujar(self):
        VENTANA.blit(self.superficie_fondo, (0, 0))

        render_list = [{"y": e.y, "obj": e, "tipo": "enemigo"} for e in self.enemigos] + [{"y": t.y, "obj": t, "tipo": "torre"} for t in self.torres]
        render_list.sort(key=lambda item: item["y"])
        
        for item in render_list:
            obj = item["obj"]
            if item["tipo"] == "enemigo":
                r = obj.datos["radio"] * (2 if "boss" in obj.tipo else 1)
                dibujar_sombra(VENTANA, obj.x, obj.y, r)
                dibujar_monstruo(VENTANA, int(obj.x), int(obj.y), obj)
                if "boss" not in obj.tipo and obj.salud < obj.max_salud:
                    pygame.draw.rect(VENTANA, (50,0,0), (obj.x-10, obj.y-45, 20, 3))
                    pygame.draw.rect(VENTANA, (0,255,0), (obj.x-10, obj.y-45, max(0, (obj.salud / obj.max_salud) * 20), 3))
            elif item["tipo"] == "torre":
                dibujar_sombra(VENTANA, obj.x, obj.y, 15)
                img, anc_x, anc_y = obtener_imagen_torre(obj.tipo, obj.nivel)
                VENTANA.blit(img, (int(obj.x) - anc_x, int(obj.y) - anc_y))
                if obj == self.torre_mapa_seleccionada:
                    s = pygame.Surface((obj.rango*2, obj.rango*2), pygame.SRCALPHA)
                    pygame.draw.circle(s, (255, 255, 255, 40), (obj.rango, obj.rango), obj.rango)
                    VENTANA.blit(s, (obj.x - obj.rango, obj.y - obj.rango))

        for p in self.proyectiles:
            c = (0, 255, 255) if p.tipo == "hielo" else (0, 255, 0) if p.tipo == "veneno" else (255, 100, 0) if p.tipo == "fuego" else (255, 100, 255) if p.tipo == "magia" else (255, 255, 0)
            pygame.draw.circle(VENTANA, c, (int(p.x), int(p.y)), 3)

        for v in self.vfx: v.draw(VENTANA)
        for tx in self.textos: tx.draw(VENTANA)

        if self.boss_actual:
            t_boss = font_lg.render("¡¡REY OGRO!!", True, (200, 50, 50))
            VENTANA.blit(t_boss, (ANCHO_LOGICO//2 - t_boss.get_width()//2, 80))
            x_bar, y_bar, w_bar, h_bar = ANCHO_LOGICO//2 - 200, 110, 400, 20
            pygame.draw.rect(VENTANA, (50, 0, 0), (x_bar, y_bar, w_bar, h_bar))
            pygame.draw.rect(VENTANA, (200, 0, 0), (x_bar, y_bar, w_bar * max(0, self.boss_actual.salud / self.boss_actual.max_salud), h_bar))
            pygame.draw.rect(VENTANA, (255, 255, 255), (x_bar, y_bar, w_bar, h_bar), 2)

        self.dibujar_ui()

        if self.estado != "JUGANDO":
            s = pygame.Surface((ANCHO_LOGICO, ALTO_LOGICO), pygame.SRCALPHA); s.fill((0, 0, 0, 200)); VENTANA.blit(s, (0,0))
            t = font_xl.render(self.estado, True, (255, 255, 255))
            t2 = font_md.render(f"Oro conseguido: {self.oro_acumulado}", True, (255, 215, 0))
            t3 = font_md.render("Click para ir al Menu", True, (200, 200, 200))
            VENTANA.blit(t, (ANCHO_LOGICO//2 - t.get_width()//2, ALTO_LOGICO//2 - 60))
            VENTANA.blit(t2, (ANCHO_LOGICO//2 - t2.get_width()//2, ALTO_LOGICO//2))
            VENTANA.blit(t3, (ANCHO_LOGICO//2 - t3.get_width()//2, ALTO_LOGICO//2 + 40))

    def dibujar_ui(self):
        pygame.draw.rect(VENTANA, C_UI_BG, (0, ALTO_LOGICO-90, ANCHO_LOGICO, 90))
        pygame.draw.line(VENTANA, C_UI_BORDER, (0, ALTO_LOGICO-90), (ANCHO_LOGICO, ALTO_LOGICO-90), 3)
        mx, my = pygame.mouse.get_pos()
        
        if self.torre_mapa_seleccionada:
            t = self.torre_mapa_seleccionada
            costo = t.calcular_costo_upgrade()
            VENTANA.blit(font_lg.render(f"{TIPOS_TORRES[t.tipo]['nombre']} Lvl {t.nivel}", True, C_TEXTO), (50, ALTO_LOGICO-65))
            col = (80, 130, 210) if self.btn_upgrade.collidepoint(mx, my) and self.dinero >= costo else (C_BTN_UPGRADE if self.dinero >= costo else (100, 100, 100))
            pygame.draw.rect(VENTANA, col, self.btn_upgrade, border_radius=8)
            pygame.draw.rect(VENTANA, C_UI_BORDER, self.btn_upgrade, 2, border_radius=8)
            txt_up = font_md.render(f"UPGRADE ${costo}", True, C_TEXTO)
            VENTANA.blit(txt_up, (self.btn_upgrade.centerx - txt_up.get_width()//2, self.btn_upgrade.centery - 10))
            VENTANA.blit(font_ui.render("Click fuera -> Volver", True, (150, 150, 150)), (self.btn_upgrade.right + 10, ALTO_LOGICO - 50))
        else:
            for btn in self.btns_torres:
                rect, tipo, datos = btn["rect"], btn["tipo"], TIPOS_TORRES[btn["tipo"]]
                if self.torre_ui_seleccionada == tipo: pygame.draw.rect(VENTANA, C_UI_BORDER, (rect.x-2, rect.y-2, rect.w+4, rect.h+4), border_radius=5)
                pygame.draw.rect(VENTANA, C_BTN_HOVER if rect.collidepoint(mx, my) else C_BTN_NORMAL, rect, border_radius=5)
                pygame.draw.rect(VENTANA, C_UI_BORDER, rect, 2, border_radius=5)
                pygame.draw.circle(VENTANA, datos["color_top"], (rect.x+20, rect.centery), 10)
                VENTANA.blit(font_ui.render(datos["nombre"], True, C_TEXTO), (rect.x + 35, rect.y + 12))
                VENTANA.blit(font_ui.render(f"${datos['costo']}", True, (255, 215, 0)), (rect.x + 35, rect.y + 30))

        pygame.draw.rect(VENTANA, (150, 50, 50), self.btn_menu, border_radius=5)
        VENTANA.blit(font_ui.render("MENU (ESC)", True, C_TEXTO), (self.btn_menu.x+10, self.btn_menu.y+5))
        pygame.draw.rect(VENTANA, C_BTN_NORMAL, self.btn_pause, border_radius=5)
        VENTANA.blit(font_ui.render("PAUSA", True, C_TEXTO), (self.btn_pause.x+10, self.btn_pause.y+5))
        pygame.draw.rect(VENTANA, C_BTN_NORMAL, self.btn_speed, border_radius=5)
        VENTANA.blit(font_ui.render("x2", True, C_TEXTO), (self.btn_speed.x+22, self.btn_speed.y+5))
        VENTANA.blit(font_lg.render(f"💰 {self.dinero}   ❤️ {self.vidas}   ⚔️ Oleada {self.oleada}", True, C_TEXTO), (120, 10))

    def click(self, mx, my):
        if self.estado != "JUGANDO": 
            if self.estado == "JUGANDO": PERFIL_JUGADOR["oro_global"] += self.oro_acumulado
            SONIDOS.play("click")
            return "salir"
            
        if self.btn_menu.collidepoint(mx, my): 
            PERFIL_JUGADOR["oro_global"] += self.oro_acumulado
            SONIDOS.play("click")
            return "salir"
            
        if self.btn_pause.collidepoint(mx, my): SONIDOS.play("click"); self.pausa = not self.pausa; return
        if self.btn_speed.collidepoint(mx, my): SONIDOS.play("click"); self.velocidad = 2 if self.velocidad == 1 else 1; return

        if my > ALTO_LOGICO - 90:
            SONIDOS.play("click")
            if self.torre_mapa_seleccionada:
                if self.btn_upgrade.collidepoint(mx, my):
                    costo = self.torre_mapa_seleccionada.calcular_costo_upgrade()
                    if self.dinero >= costo: self.dinero -= costo; self.torre_mapa_seleccionada.mejorar()
            else:
                for btn in self.btns_torres:
                    if btn["rect"].collidepoint(mx, my): self.torre_ui_seleccionada = btn["tipo"]
            return

        torre_click = next((t for t in self.torres if t.rect.collidepoint(mx, my)), None)
        if torre_click:
            SONIDOS.play("click")
            self.torre_mapa_seleccionada = torre_click
        else:
            self.torre_mapa_seleccionada = None
            costo = TIPOS_TORRES[self.torre_ui_seleccionada]["costo"]
            gx, gy = to_grid(mx, my)
            valido = (gx, gy) not in self.celdas_camino_set and not any(to_grid(t.x, t.y) == (gx, gy) for t in self.torres)
            if self.dinero >= costo and valido:
                self.torres.append(Torre(*to_pixel(gx, gy), self.torre_ui_seleccionada))
                self.dinero -= costo

# --- NUEVO MENÚ DE MEJORAS (SKILL TREE 6 FILAS) ---
class MenuMejoras:
    def __init__(self):
        self.btn_back = pygame.Rect(ANCHO_LOGICO//2 - 150, ALTO_LOGICO - 70, 300, 50)
        self.titulos = {
            "dano": "Poder Global (Daño extra)", 
            "oro": "Riqueza Global (Oro extra)", 
            "torres": "Ingeniería (Desbloqueos)",
            "upg_veneno": "Maestría: Tóxica",
            "upg_fuego": "Maestría: Infernal",
            "upg_arcana": "Maestría: Arcana"
        }

    def dibujar(self):
        VENTANA.fill(C_UI_BG)
        pygame.draw.rect(VENTANA, C_UI_BORDER, (20, 20, ANCHO_LOGICO-40, ALTO_LOGICO-40), 3)
        
        tit = font_lg.render("ÁRBOL DE HABILIDADES", True, C_UI_BORDER)
        VENTANA.blit(tit, (ANCHO_LOGICO//2 - tit.get_width()//2, 30))
        
        oro = font_md.render(f"Oro: {PERFIL_JUGADOR['oro_global']} 💰", True, (255, 215, 0))
        VENTANA.blit(oro, (ANCHO_LOGICO//2 - oro.get_width()//2, 65))

        mx, my = pygame.mouse.get_pos()
        
        filas = ["dano", "oro", "torres", "upg_veneno", "upg_fuego", "upg_arcana"]
        
        for row_idx, key in enumerate(filas):
            y_base = 105 + (row_idx * 90)
            
            # Verificar si la fila de maestría está desbloqueada
            fila_bloqueada = False
            if key == "upg_veneno" and PERFIL_JUGADOR["mejoras"]["torres"] < 1: fila_bloqueada = True
            elif key == "upg_fuego" and PERFIL_JUGADOR["mejoras"]["torres"] < 2: fila_bloqueada = True
            elif key == "upg_arcana" and PERFIL_JUGADOR["mejoras"]["torres"] < 3: fila_bloqueada = True

            color_titulo = C_TEXTO if not fila_bloqueada else (100, 100, 100)
            VENTANA.blit(font_md.render(self.titulos[key], True, color_titulo), (50, y_base))
            
            nodos = ARBOLES_MEJORAS[key]
            nivel_actual = PERFIL_JUGADOR["mejoras"][key]
            
            for col_idx, nodo in enumerate(nodos):
                x_base = 320 + (col_idx * 300)
                rect_nodo = pygame.Rect(x_base, y_base - 10, 220, 60)
                
                if fila_bloqueada: estado = "BLOQUEADO"
                else:
                    if col_idx < nivel_actual: estado = "COMPRADO"
                    elif col_idx == nivel_actual: estado = "DISPONIBLE"
                    else: estado = "BLOQUEADO"
                
                if col_idx < len(nodos) - 1:
                    color_linea = (100, 255, 100) if estado == "COMPRADO" else (100, 100, 100)
                    pygame.draw.line(VENTANA, color_linea, (rect_nodo.right, rect_nodo.centery), (x_base + 300, rect_nodo.centery), 3)

                alcanza = PERFIL_JUGADOR["oro_global"] >= nodo["costo"]
                col_bg = C_BTN_NORMAL
                col_borde = C_UI_BORDER
                
                if estado == "COMPRADO": col_bg, col_borde = (30, 80, 30), (100, 255, 100)
                elif estado == "BLOQUEADO": col_bg, col_borde = (30, 20, 20), (80, 80, 80)
                elif estado == "DISPONIBLE":
                    if rect_nodo.collidepoint(mx, my) and alcanza: col_bg = C_BTN_HOVER
                    col_borde = (255, 215, 0)
                
                pygame.draw.rect(VENTANA, col_bg, rect_nodo, border_radius=6)
                pygame.draw.rect(VENTANA, col_borde, rect_nodo, 2, border_radius=6)
                
                VENTANA.blit(font_md.render(nodo["nombre"], True, C_TEXTO if estado != "BLOQUEADO" else (150, 150, 150)), (rect_nodo.x + 8, rect_nodo.y + 5))
                VENTANA.blit(font_ui.render(nodo["desc"], True, (200, 200, 200)), (rect_nodo.x + 8, rect_nodo.y + 25))
                
                if estado == "COMPRADO": VENTANA.blit(font_md.render("✓", True, (100, 255, 100)), (rect_nodo.right - 25, rect_nodo.centery - 10))
                elif estado == "DISPONIBLE":
                    VENTANA.blit(font_md.render(f"${nodo['costo']}", True, (255, 215, 0) if alcanza else (255, 100, 100)), (rect_nodo.x + 8, rect_nodo.bottom - 20))

        col_back = C_BTN_HOVER if self.btn_back.collidepoint(mx, my) else C_BTN_NORMAL
        pygame.draw.rect(VENTANA, col_back, self.btn_back, border_radius=8)
        pygame.draw.rect(VENTANA, C_UI_BORDER, self.btn_back, 2, border_radius=8)
        tb = font_md.render("VOLVER AL MENÚ", True, C_TEXTO)
        VENTANA.blit(tb, (self.btn_back.centerx - tb.get_width()//2, self.btn_back.centery - tb.get_height()//2))

    def click(self, mx, my):
        SONIDOS.play("click")
        if self.btn_back.collidepoint(mx, my): return "volver"
        
        filas = ["dano", "oro", "torres", "upg_veneno", "upg_fuego", "upg_arcana"]
        for row_idx, key in enumerate(filas):
            fila_bloqueada = False
            if key == "upg_veneno" and PERFIL_JUGADOR["mejoras"]["torres"] < 1: fila_bloqueada = True
            elif key == "upg_fuego" and PERFIL_JUGADOR["mejoras"]["torres"] < 2: fila_bloqueada = True
            elif key == "upg_arcana" and PERFIL_JUGADOR["mejoras"]["torres"] < 3: fila_bloqueada = True
            
            if fila_bloqueada: continue

            y_base = 105 + (row_idx * 90)
            nivel_actual = PERFIL_JUGADOR["mejoras"][key]
            
            if nivel_actual < len(ARBOLES_MEJORAS[key]):
                nodo = ARBOLES_MEJORAS[key][nivel_actual]
                x_base = 320 + (nivel_actual * 300)
                rect_nodo = pygame.Rect(x_base, y_base - 10, 220, 60)
                
                if rect_nodo.collidepoint(mx, my) and PERFIL_JUGADOR["oro_global"] >= nodo["costo"]:
                    PERFIL_JUGADOR["oro_global"] -= nodo["costo"]
                    PERFIL_JUGADOR["mejoras"][key] += 1 
                    SONIDOS.play("buy_upgrade")
        return None

# --- MENÚ PRINCIPAL ---
class MenuPrincipal:
    def __init__(self):
        # 1. LÓGICA DE CARGA DE IMAGEN (Incrustada o local)
        if hasattr(sys, '_MEIPASS'):
            directorio_base = sys._MEIPASS
        else:
            directorio_base = os.path.dirname(os.path.abspath(__file__))
            
        archivos_en_carpeta = []
        try:
            archivos_en_carpeta = os.listdir(directorio_base)
        except Exception:
            pass

        # Rastreador: Busca el primer archivo que empiece por "menu"
        archivo_menu = "menu.png" 
        for archivo in archivos_en_carpeta:
            if archivo.startswith("menu."):
                archivo_menu = archivo
                break
                
        self.ruta_imagen = os.path.join(directorio_base, archivo_menu)
        
        try:
            self.bg_image = pygame.image.load(self.ruta_imagen).convert()
            self.bg_image = pygame.transform.scale(self.bg_image, (ANCHO_LOGICO, ALTO_LOGICO))
        except Exception:
            self.bg_image = None 

        # 2. DEFINICIÓN DE BOTONES
        self.btn_inf = pygame.Rect(ANCHO_LOGICO//2 - 150, 150, 300, 50)
        self.btn_camp = pygame.Rect(ANCHO_LOGICO//2 - 150, 220, 300, 50)
        self.btn_mej = pygame.Rect(ANCHO_LOGICO//2 - 150, 290, 300, 50) 
        self.btn_exit = pygame.Rect(ANCHO_LOGICO//2 - 150, 600, 300, 50)
        self.modo_campana = False
        self.modo_dificultad = False
        
        self.btn_lvls = []
        for i in range(5):
            r = pygame.Rect(ANCHO_LOGICO//2 - 200, 280 + (i*60), 400, 50)
            nombre = f"Nivel {i+1}: " + ("Bosque Antiguo" if i < 4 else "DESIERTO (Final)")
            self.btn_lvls.append({"r": r, "id": i+1, "txt": nombre})
        
        self.btn_diff_facil = pygame.Rect(ANCHO_LOGICO//2 - 150, 250, 300, 60)
        self.btn_diff_medio = pygame.Rect(ANCHO_LOGICO//2 - 150, 330, 300, 60)
        self.btn_diff_dificil = pygame.Rect(ANCHO_LOGICO//2 - 150, 410, 300, 60)
        self.btn_back = pygame.Rect(ANCHO_LOGICO//2 - 150, 600, 300, 50)

    def dibujar_btn(self, r, txt, activo=True):
        mx, my = pygame.mouse.get_pos()
        col = C_BTN_HOVER if (r.collidepoint(mx, my) and activo) else C_BTN_NORMAL
        if not activo: col = (30, 20, 10)
        pygame.draw.rect(VENTANA, C_UI_BORDER, (r.x-2, r.y-2, r.w+4, r.h+4), border_radius=8)
        pygame.draw.rect(VENTANA, col, r, border_radius=8)
        t = font_lg.render(txt, True, C_TEXTO if activo else (100, 100, 100))
        VENTANA.blit(t, (r.centerx - t.get_width()//2, r.centery - t.get_height()//2))

    def dibujar(self):
        # 3. LÓGICA DE DIBUJADO EN PANTALLA
        if self.bg_image is not None:
            VENTANA.blit(self.bg_image, (0, 0))
            s = pygame.Surface((ANCHO_LOGICO, ALTO_LOGICO), pygame.SRCALPHA)
            s.fill((0, 0, 0, 100))
            VENTANA.blit(s, (0,0))
        else: 
            VENTANA.fill(C_UI_BG)

        pygame.draw.rect(VENTANA, C_UI_BORDER, (40, 40, ANCHO_LOGICO-80, ALTO_LOGICO-80), 3)
        tit_sombra = font_xl.render("ROGUE TOWER: GRID EDITION", True, (0, 0, 0))
        VENTANA.blit(tit_sombra, (ANCHO_LOGICO//2 - tit_sombra.get_width()//2 + 2, 52))
        tit = font_xl.render("ROGUE TOWER: GRID EDITION", True, C_UI_BORDER)
        VENTANA.blit(tit, (ANCHO_LOGICO//2 - tit.get_width()//2, 50))
        
        oro_txt = font_lg.render(f"Oro Global: {PERFIL_JUGADOR['oro_global']}", True, (255, 215, 0))
        VENTANA.blit(oro_txt, (50, 50))
        
        if self.modo_dificultad:
            t = font_lg.render("SELECCIONA DIFICULTAD", True, C_TEXTO)
            VENTANA.blit(t, (ANCHO_LOGICO//2 - t.get_width()//2, 150))
            self.dibujar_btn(self.btn_diff_facil, "FÁCIL")
            self.dibujar_btn(self.btn_diff_medio, "MEDIO")
            self.dibujar_btn(self.btn_diff_dificil, "DIFÍCIL")
            self.dibujar_btn(self.btn_back, "VOLVER")
        elif not self.modo_campana:
            self.dibujar_btn(self.btn_inf, "MODO INFINITO")
            self.dibujar_btn(self.btn_camp, "CAMPAÑA")
            self.dibujar_btn(self.btn_mej, "SKILL TREE") 
            self.dibujar_btn(self.btn_exit, "SALIR")
        else:
            for b in self.btn_lvls:
                unlocked = b["id"] <= PERFIL_JUGADOR["niveles_desbloqueados"]
                self.dibujar_btn(b["r"], b["txt"] if unlocked else "BLOQUEADO", unlocked)
            self.dibujar_btn(self.btn_back, "VOLVER")

    def click(self, mx, my):
        SONIDOS.play("click")
        if self.modo_dificultad:
            if self.btn_diff_facil.collidepoint(mx, my): return "inf_facil"
            if self.btn_diff_medio.collidepoint(mx, my): return "inf_medio"
            if self.btn_diff_dificil.collidepoint(mx, my): return "inf_dificil"
            if self.btn_back.collidepoint(mx, my): self.modo_dificultad = False
        elif not self.modo_campana:
            if self.btn_inf.collidepoint(mx, my): self.modo_dificultad = True
            if self.btn_camp.collidepoint(mx, my): self.modo_campana = True
            if self.btn_mej.collidepoint(mx, my): return "abrir_mejoras"
            if self.btn_exit.collidepoint(mx, my): sys.exit()
        else:
            if self.btn_back.collidepoint(mx, my): self.modo_campana = False
            for b in self.btn_lvls:
                if b["r"].collidepoint(mx, my):
                    if b["id"] <= PERFIL_JUGADOR["niveles_desbloqueados"]: return f"lvl_{b['id']}"
def main():
    reloj = pygame.time.Clock()
    estado = "MENU"
    menu = MenuPrincipal()
    tienda = MenuMejoras()
    partida = None
    
    while True:
        reloj.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT: sys.exit()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                if estado == "JUEGO": 
                    PERFIL_JUGADOR["oro_global"] += partida.oro_acumulado
                    estado = "MENU"; partida = None
                elif estado == "MEJORAS": estado = "MENU"
                else: sys.exit()
            
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mx, my = pygame.mouse.get_pos()
                
                if estado == "MENU":
                    res = menu.click(mx, my)
                    if res == "abrir_mejoras":
                        estado = "MEJORAS"
                    elif res and "inf_" in res:
                        diff = res.split("_")[1]
                        partida = Partida("infinito", dificultad_infinita=diff)
                        estado = "JUEGO"
                        menu.modo_dificultad = False 
                    elif res and "lvl" in res:
                        l = int(res.split("_")[1])
                        partida = Partida("campana", max_oleadas=10 if l == 1 else 20, nivel=l)
                        estado = "JUEGO"
                
                elif estado == "MEJORAS":
                    if tienda.click(mx, my) == "volver":
                        estado = "MENU"

                elif estado == "JUEGO":
                    if partida.click(mx, my) == "salir":
                        estado = "MENU"
                        partida = None
                        
        if estado == "MENU": menu.dibujar()
        elif estado == "MEJORAS": tienda.dibujar()
        elif estado == "JUEGO": 
            partida.update()
            partida.dibujar()
            
        pygame.display.flip()

if __name__ == "__main__":
    main()