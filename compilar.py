#!/usr/bin/env python3
"""
Compilador para Rogue Tower - Genera ejecutables fácilmente
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def install_dependency(package):
    """Instala una dependencia si no está presente"""
    try:
        __import__(package.replace("-", "_"))
        return True
    except ImportError:
        print(f"📦 Instalando {package}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True

def build_exe_windows():
    """Compila a EXE para Windows usando PyInstaller"""
    print("\n🖥️  Compilando EXE para Windows...")
    
    if not install_dependency("pyinstaller"):
        print("❌ Error instalando PyInstaller")
        return False
    
    try:
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--onefile",
            "--windowed",
            "--name=RogueTower",
            "--icon=NONE",
            "juego.py"
        ], check=True)
        
        exe_path = Path("dist") / "RogueTower.exe"
        if exe_path.exists():
            print(f"✅ EXE compilado exitosamente: {exe_path}")
            print(f"📍 Ubicación: {exe_path.absolute()}")
            return True
        else:
            print("❌ El EXE no se generó correctamente")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la compilación: {e}")
        return False

def build_apk_android():
    """Compila a APK para Android usando Buildozer"""
    print("\n📱 Compilando APK para Android...")
    
    if not install_dependency("buildozer"):
        print("❌ Error instalando Buildozer")
        return False
    
    if not install_dependency("cython"):
        print("❌ Error instalando Cython")
        return False
    
    try:
        print("⚠️  NOTA: La primera compilación puede tardar 10-30 minutos")
        print("⚠️  Requiere Java Development Kit (JDK 11+) instalado")
        
        subprocess.run(["buildozer", "android", "debug"], check=True)
        
        apk_path = Path("bin") / "roguetowr-1.0-debug.apk"
        if apk_path.exists():
            print(f"✅ APK compilado exitosamente: {apk_path}")
            print(f"📍 Ubicación: {apk_path.absolute()}")
            print("📲 Para instalar en Android: adb install " + str(apk_path))
            return True
        else:
            print("❌ El APK no se generó correctamente")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en la compilación: {e}")
        print("💡 Verifica que tienes JDK 11+ instalado")
        return False

def show_menu():
    """Muestra el menú principal"""
    print("\n" + "="*50)
    print("🎮 ROGUE TOWER - COMPILADOR MULTI-PLATAFORMA 🎮")
    print("="*50)
    print("\nOpciones de compilación:")
    print("1. 💻 Compilar EXE para Windows")
    print("2. 📱 Compilar APK para Android")
    print("3. ⚡ Compilar ambos")
    print("4. ℹ️  Ver requisitos")
    print("5. ❌ Salir")
    print("\n" + "-"*50)

def show_requirements():
    """Muestra los requisitos por plataforma"""
    reqs = """
╔══════════════════════════════════════════════════════════════╗
║              REQUISITOS POR PLATAFORMA                       ║
╚══════════════════════════════════════════════════════════════╝

📦 PARA COMPILAR A EXE (Windows):
   - Python 3.7+
   - PyInstaller (se instala automáticamente)
   - ~500 MB de espacio
   - Tiempo: ~2-5 minutos
   
   Comando: compilar.py --exe

📦 PARA COMPILAR A APK (Android):
   - Python 3.9+
   - Java Development Kit (JDK 11+) ⚠️ OBLIGATORIO
   - Android SDK/NDK
   - Buildozer y Cython (se instalan automáticamente)
   - ~2-3 GB de espacio
   - Tiempo: 10-30 minutos (primera vez)
   - Internet: ~2GB de descargas
   
   Comando: compilar.py --apk

💡 RECOMENDACIONES:

   • Para distribución rápida: usa EXE en Windows
   • Para Android: necesitas JDK instalado
   • Si tienes problemas: usa WSL2 + Ubuntu
   
   Descargar JDK desde:
   https://adoptium.net/ (Adoptium OpenJDK 11 LTS)

✅ VERIFICAR INSTALACIONES:
   python --version
   java -version  (para Android)
"""
    print(reqs)

def main():
    """Función principal"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--exe":
            if build_exe_windows():
                sys.exit(0)
            else:
                sys.exit(1)
        elif sys.argv[1] == "--apk":
            if build_apk_android():
                sys.exit(0)
            else:
                sys.exit(1)
        elif sys.argv[1] == "--help":
            print("Uso: compilar.py [opción]")
            print("  --exe    Compilar a EXE")
            print("  --apk    Compilar a APK")
            print("  --help   Mostrar esta ayuda")
            sys.exit(0)
    
    while True:
        show_menu()
        choice = input("Selecciona una opción (1-5): ").strip()
        
        if choice == "1":
            if build_exe_windows():
                input("\n✅ Presiona Enter para continuar...")
            else:
                input("\n❌ Presiona Enter para continuar...")
                
        elif choice == "2":
            if build_apk_android():
                input("\n✅ Presiona Enter para continuar...")
            else:
                input("\n❌ Presiona Enter para continuar...")
                
        elif choice == "3":
            print("\n⚡ Compilando ambos...")
            exe_ok = build_exe_windows()
            apk_ok = build_apk_android()
            
            print("\n" + "="*50)
            print("📊 RESUMEN:")
            print(f"  EXE: {'✅ OK' if exe_ok else '❌ ERROR'}")
            print(f"  APK: {'✅ OK' if apk_ok else '❌ ERROR'}")
            print("="*50)
            input("\nPresiona Enter para continuar...")
            
        elif choice == "4":
            show_requirements()
            input("\nPresiona Enter para continuar...")
            
        elif choice == "5":
            print("\n👋 ¡Hasta luego!")
            sys.exit(0)
        else:
            print("❌ Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Compilación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
