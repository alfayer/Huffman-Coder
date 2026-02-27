@echo off
chcp 65001 > nul  REM 设置为 UTF-8 代码页
setlocal enabledelayedexpansion

echo ========================================
echo Huffman build script
echo ========================================

REM 使用 UTF-8 编码的中文输出（不需要转义）
echo make dir...
if not exist build\obj mkdir build\obj
if not exist build\bin mkdir build\bin
echo make dir done!

echo compile main.cpp...
g++ -c main.cpp -o build\obj\main.o -g -Wall
if errorlevel 1 (
    echo main.cpp compile failed
    exit /b 1
) else (
    echo main.cpp compile success
)

echo compile Huffman.cpp...
g++ -c Huffman.cpp -o build\obj\Huffman.o -g -Wall
if errorlevel 1 (
    echo Huffman.cpp compile failed
    exit /b 1
) else (
    echo Huffman.cpp compile success
)

echo link...
g++ -o build\bin\program.exe build\obj\main.o build\obj\Huffman.o
if errorlevel 1 (
    echo link failed
    exit /b 1
) else (
    echo link success
)

echo ========================================
echo build done!
echo runnable file: %CD%\build\bin\program.exe
echo ========================================

set /p RUN=run now?(y/n): 
if /i "%RUN%"=="y" (
    echo running...
    echo ----------------------------------------
    build\bin\program.exe
    echo ----------------------------------------
    echo terminate program.
)

pause