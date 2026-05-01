# Rogue Tower - Guía de Compilación para Móvil

## 📱 Opción 1: APK para Android (Recomendado)

### Requisitos:
- Python 3.9+
- Java Development Kit (JDK 11+)
- Android SDK/NDK
- Buildozer

### Instalación de Buildozer:

```bash
pip install buildozer cython
```

### Compilar APK:

```bash
buildozer android debug
```

El APK generado estará en: `bin/roguetowr-1.0-debug.apk`

### Compilar APK Optimizado (Release):

```bash
buildozer android release
```

---

## 🖥️ Opción 2: Ejecutable de Escritorio (.exe para Windows)

### Requiere:
- PyInstaller

### Instalación:

```bash
pip install pyinstaller
```

### Compilar EXE:

```bash
pyinstaller --onefile --windowed --icon=icon.ico juego.py
```

El .exe estará en: `dist/juego.exe`

---

## 🚀 Opción 3: Ejecutable Portátil (Distribuir fácilmente)

La carpeta `build/` contiene un ejecutable ya compilado (`juego.spec`). 
Puedes compartir los archivos en `dist/` con tus amigos.

---

## 📋 Características Agregadas:

✅ Controles táctiles para móvil  
✅ Botón X en esquina superior derecha para salir  
✅ Compatible con mouse en escritorio  
✅ Pantalla completa optimizada  

---

## 📞 Solución de Problemas:

**Error: "Java not found"**  
→ Instala JDK 11+ y agrega a PATH

**Error: "Android SDK not found"**  
→ Configura ANDROID_SDK_ROOT en variables de entorno

**La compilación es muy lenta**  
→ Es normal la primera vez, descarga ~2GB de dependencias

---

## 💡 Alternativa: Usar WSL2 + Linux

Si tienes problemas en Windows, instala WSL2 y ejecuta en Ubuntu:

```bash
sudo apt-get install python3-pip openjdk-11-jdk
pip3 install buildozer cython
buildozer android debug
```
