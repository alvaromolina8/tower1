@echo off
REM Script para compilar Rogue Tower para diferentes plataformas

echo.
echo =========================================
echo ROGUE TOWER - COMPILADOR MULTI-PLATAFORMA
echo =========================================
echo.
echo Selecciona una opcion:
echo 1. APK para Android (requiere Buildozer)
echo 2. EXE para Windows (requiere PyInstaller)
echo 3. Compilar ambos
echo 4. Ver requisitos
echo 5. Salir
echo.

setlocal enabledelayedexpansion
set /p choice="Ingresa tu opcion (1-5): "

if "%choice%"=="1" goto build_apk
if "%choice%"=="2" goto build_exe
if "%choice%"=="3" goto build_both
if "%choice%"=="4" goto show_requirements
if "%choice%"=="5" exit /b 0
goto invalid

:build_apk
echo.
echo Compilando APK para Android...
echo Verificando Buildozer...
python -m pip list | find "buildozer" >nul
if %errorlevel% neq 0 (
    echo Buildozer no encontrado. Instalando...
    pip install buildozer cython
)
echo Iniciando compilacion...
buildozer android debug
echo.
echo APK generado en: bin\roguetowr-1.0-debug.apk
pause
exit /b 0

:build_exe
echo.
echo Compilando EXE para Windows...
echo Verificando PyInstaller...
python -m pip list | find "pyinstaller" >nul
if %errorlevel% neq 0 (
    echo PyInstaller no encontrado. Instalando...
    pip install pyinstaller
)
echo Iniciando compilacion...
pyinstaller --onefile --windowed juego.py -n "Rogue Tower"
echo.
echo EXE generado en: dist\Rogue Tower.exe
pause
exit /b 0

:build_both
echo.
echo Compilando APK...
python -m pip list | find "buildozer" >nul
if %errorlevel% neq 0 (
    pip install buildozer cython
)
buildozer android debug
echo APK completado en: bin\roguetowr-1.0-debug.apk
echo.
echo Compilando EXE...
python -m pip list | find "pyinstaller" >nul
if %errorlevel% neq 0 (
    pip install pyinstaller
)
pyinstaller --onefile --windowed juego.py -n "Rogue Tower"
echo EXE completado en: dist\Rogue Tower.exe
pause
exit /b 0

:show_requirements
echo.
echo REQUISITOS POR PLATAFORMA:
echo.
echo === PARA APK (Android) ===
echo - Python 3.9+
echo - Java Development Kit (JDK 11+)
echo - Android SDK/NDK
echo - Buildozer: pip install buildozer cython
echo - Disk: ~2-3 GB
echo.
echo === PARA EXE (Windows) ===
echo - Python 3.7+
echo - PyInstaller: pip install pyinstaller
echo - Disk: ~500 MB
echo.
echo === PARA DISTRIBUCION ===
echo - Los APK/EXE generados pueden compartirse con amigos
echo - En Android: transferir .apk y instalar manualmente
echo - En Windows: compartir .exe generado
echo.
pause
exit /b 0

:invalid
echo Opcion no valida. Intenta de nuevo.
pause
goto build_apk
