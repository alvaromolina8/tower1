# 📱 Guía Completa: Compilar a APK para Android

## 🎯 Objetivo
Convertir tu juego Pygame en un APK que puedas instalar en Android y compartir con amigos.

---

## 📋 Requisitos Previos (IMPORTANTE)

### 1. Java Development Kit (JDK)
**¿Por qué?** Android Build Tools necesita Java.

**Pasos:**
1. Ve a: https://adoptium.net/
2. Descarga **Adoptium OpenJDK 11 LTS**
3. Ejecuta el instalador
4. **IMPORTANTE:** Marca "Add to PATH" durante la instalación
5. Verifica: Abre PowerShell y escribe:
   ```powershell
   java -version
   ```
   Debes ver algo como `openjdk version "11.0.x"`

### 2. Python 3.9+
```powershell
python --version
```
Si no tienes, descarga desde: https://www.python.org/downloads/

### 3. Espacio en Disco
- Mínimo: **3 GB libres**
- Para compilación rápida: **5 GB libres**

---

## 🔧 Instalación de Herramientas

### Paso 1: Instalar Buildozer
```powershell
pip install buildozer cython
```

### Paso 2: Instalar Dependencias Adicionales
```powershell
pip install -r requirements.txt
```

### Paso 3: Verificar Instalación
```powershell
buildozer --version
```

---

## 🚀 Compilar a APK

### Método 1: Automático (Recomendado)
```powershell
python compilar.py --apk
```

### Método 2: Manual
```powershell
buildozer android debug
```

### ⏳ Qué Esperar

**Primera compilación:**
- Descarga: Android SDK, NDK, Gradle (~2GB)
- Tiempo: 15-30 minutos
- Requiere internet estable

**Compilaciones posteriores:**
- Tiempo: 5-10 minutos
- Más rápido (ya tiene dependencias)

---

## 📍 Dónde Encontrar tu APK

Después de compilar exitosamente:

```
Tu Proyecto/
└── bin/
    └── roguetowr-1.0-debug.apk  ← AQUÍ ESTÁ
```

Ruta completa: `bin\roguetowr-1.0-debug.apk`

---

## 📱 Instalar en Tu Teléfono

### Opción A: Desde la PC (Recomendado)
1. Conecta tu teléfono Android a la PC
2. Abre PowerShell en la carpeta del juego
3. Ejecuta:
   ```powershell
   adb install bin/roguetowr-1.0-debug.apk
   ```

### Opción B: Manual (Sin PC)
1. Transfiere el archivo `.apk` a tu teléfono
2. En el teléfono: abre el archivo
3. Toca "Instalar"
4. ¡Listo! El juego está en tu móvil

### Opción C: Compartir Archivo
1. Envía por email: `bin/roguetowr-1.0-debug.apk`
2. Tu amigo descarga y abre en Android
3. El sistema lo instala automáticamente

---

## ⚠️ Solución de Problemas

### Error: "command not found: java"
```
❌ Java no está instalado o no está en PATH
```
**Solución:**
1. Descarga JDK desde https://adoptium.net/
2. Instala y marca "Add to PATH"
3. Reinicia PowerShell
4. Intenta de nuevo

### Error: "Could not find android sdk"
```
❌ Android SDK no está descargado
```
**Solución:**
1. Espera a que Buildozer lo descargue (primera vez)
2. Verifica conexión a internet
3. Intenta de nuevo

### Error: "Gradle build failed"
```
❌ Error compilando el proyecto
```
**Solución:**
```powershell
buildozer android clean
buildozer android debug
```

### Compilación muy lenta
- Esto es **NORMAL** en primera compilación
- Se descargan ~2GB
- Paciencia: puede tardar 30+ minutos
- Toma café ☕

### El APK se genera pero es muy grande (>100MB)
```
❌ Esto indica que se incluyó todo
```
**Solución:**
```powershell
buildozer android release
```
Esto optimiza el tamaño (~30-50MB)

---

## 🎯 Compilación Release (APK Final)

Una vez que todo funciona:

```powershell
buildozer android release
```

Esto crea:
- `bin/roguetowr-1.0-release.apk` (más pequeño, optimizado)

---

## 📤 Compartir tu Juego

### Por Email
```
1. Adjunta: bin/roguetowr-1.0-debug.apk
2. Envía a tus amigos
3. Ellos hacen tap en el archivo para instalar
```

### Por WhatsApp/Telegram
```
1. Comprime: bin/roguetowr-1.0-debug.apk (si es muy grande)
2. Envía como archivo
3. Tus amigos lo descargan e instalan
```

### Por Drive/Dropbox
```
1. Sube el APK a Google Drive
2. Comparte el link
3. Tus amigos descargan e instalan
```

### Por Servidor Web
```
1. Sube a tu servidor: domain.com/roguetowr.apk
2. Tus amigos descargan desde el navegador
3. Instalan desde descargas
```

---

## 🔐 Notas de Seguridad

⚠️ **APK Debug vs Release:**
- **Debug**: Solo para pruebas, más grande
- **Release**: Firmado, para distribución real

Para distribución final, usa:
```powershell
buildozer android release
```

---

## 💡 Tips y Trucos

### Reducir Tiempo de Compilación
```powershell
# No compilar siempre desde cero
buildozer android debug --no-strip
```

### Ver Logs Detallados
```powershell
buildozer android debug -v
```

### Limpiar y Compilar de Nuevo
```powershell
buildozer android clean
buildozer android debug
```

### Compilar solo para ARM64 (más rápido)
Edita `buildozer.spec`:
```
android.archs = arm64-v8a
```

---

## 📊 Checklist Final

- [ ] Java instalado y verificado
- [ ] Python 3.9+
- [ ] Buildozer instalado
- [ ] 3+ GB de espacio libre
- [ ] Conexión a internet estable
- [ ] Ejecuté: `python compilar.py --apk`
- [ ] Espéré a que termine (15-30 min)
- [ ] APK generado en `bin/roguetowr-1.0-debug.apk`
- [ ] Instalé en mi teléfono
- [ ] ¡Compartí con amigos! 🎮

---

## 🎉 ¡Listo!

Tu juego está en formato APK y listo para compartir.

**Próximos pasos:**
1. Prueba en tu teléfono
2. Invita a tus amigos
3. ¡A jugar!

---

## 📞 Contacto/Soporte

Si tienes problemas, verifica que:
- Java está instalado: `java -version`
- Python funciona: `python --version`
- Tienes internet estable
- Tienes espacio en disco

¡Buen juego! 🚀
