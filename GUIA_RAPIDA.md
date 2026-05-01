# 🎮 Rogue Tower - Guía de Actualización Móvil

## ✨ Cambios Realizados

Tu juego ha sido actualizado con:

### ✅ Controles Táctiles
- **Tap en pantalla** para construir torres (igual que click de mouse)
- **Tap en botones** de control funciona en móvil y desktop
- **Soporte para touch events** en Pygame

### ✅ Botón de Salida Mejorado
- **Nuevo botón X** en la esquina **superior derecha**
- Disponible **durante el juego** sin necesidad de ESC
- Se guarda tu progreso automáticamente

### ✅ Optimización para Móvil
- Interfaz adaptada a pantallas táctiles
- Soporte para ambas orientaciones
- Mejor rendimiento en dispositivos móviles

---

## 🚀 Compilar el Juego

### **Opción 1: Ejecutable Rápido para Windows**

```bash
python compilar.py --exe
```

Esto genera `RogueTower.exe` que puedes compartir directamente.

### **Opción 2: APK para Android**

```bash
python compilar.py --apk
```

Requisitos previos:
- Instalar **Java Development Kit (JDK 11+)**
  - Descargar desde: https://adoptium.net/
  - Agregar a PATH

Luego ejecutar:
```bash
python compilar.py --apk
```

### **Opción 3: Menú Interactivo**

```bash
python compilar.py
```

Se abrirá un menú donde puedes seleccionar qué compilar.

---

## 📱 Cómo Compartir con Amigos

### Windows
1. Ejecuta: `python compilar.py --exe`
2. Comparte el archivo: `dist/RogueTower.exe`
3. Tus amigos solo necesitan hacer doble click

### Android
1. Ejecuta: `python compilar.py --apk`
2. Comparte: `bin/roguetowr-1.0-debug.apk`
3. En Android: descarga el archivo y toca para instalar
4. O usa: `adb install roguetowr-1.0-debug.apk`

### Distribuir Online
- Sube el .exe o .apk a:
  - Google Drive
  - Dropbox
  - WeTransfer
  - Tu servidor

---

## 🎮 Cómo Jugar en Móvil

### Controles
| Acción | Desktop | Móvil |
|--------|---------|-------|
| Construir Torre | Click | Tap |
| Seleccionar Torre | Click | Tap |
| Mejorar Torre | Click | Tap |
| Cambiar Torre | Click | Tap |
| Pausar | Click Botón | Tap Botón |
| Salir | ESC o X | Tap X (esquina) |

---

## ⚠️ Solución de Problemas

### "ModuleNotFoundError: No module named 'pygame'"
```bash
pip install pygame
```

### Error compilando APK: "Java not found"
1. Instala JDK: https://adoptium.net/
2. Agrega `JAVA_HOME` a variables de entorno

### Error en PyInstaller
```bash
pip install --upgrade pyinstaller
```

### La compilación tarda mucho
- Es normal la primera vez (~10-30 min para APK)
- Se descargan dependencias (~2GB)
- Conexión a internet estable recomendada

---

## 📊 Tamaños Aproximados

- **EXE (Windows)**: ~50-100 MB
- **APK (Android)**: ~30-50 MB
- **Código fuente**: ~50 KB

---

## 🔧 Archivos Incluidos

```
tower/
├── juego.py              # Juego principal (actualizado)
├── compilar.py          # Herramienta compilación Python
├── compilar.bat         # Herramienta compilación Batch
├── buildozer.spec       # Configuración Android
├── requirements.txt     # Dependencias
├── COMPILAR_MOVIL.md   # Guía detallada
└── GUIA_RAPIDA.md      # Esta guía
```

---

## 💡 Consejos

1. **Instala dependencias primero:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Prueba en desktop antes de Android:**
   ```bash
   python juego.py
   ```

3. **Para Android en Windows, usa WSL2:**
   - Abre "Ejecutar" (Win+R)
   - Escribe: `wsl`
   - Instala Ubuntu
   - Ejecuta compilar desde allí

---

## 🎯 Próximos Pasos

1. ✅ Prueba el juego en desktop (mismo `juego.py`)
2. ⬜ Compila para tu plataforma preferida
3. ⬜ Comparte con amigos
4. ⬜ ¡A jugar!

---

## 📞 Soporte

Si tienes problemas, verifica:
- Python 3.7+ instalado: `python --version`
- Pygame funciona: `python -c "import pygame; print('OK')"`
- JDK instalado (para APK): `java -version`

¡Que disfrutes el juego! 🎮
