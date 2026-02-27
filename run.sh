#!/bin/bash
# Windows Git Bash 构建脚本
# 保存为 build.sh，使用 Git Bash 运行

# 颜色定义（Git Bash 支持 ANSI 颜色）
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 定义变量（使用正斜杠，Git Bash 支持）
OBJ_DIR="build/obj"
BIN_DIR="build/bin"
TARGET="$BIN_DIR/program.exe"

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Huffman 编码项目构建脚本${NC}"
echo -e "${BLUE}========================================${NC}"

# 创建目录
echo -e "${YELLOW}创建目录...${NC}"
mkdir -p "$OBJ_DIR" "$BIN_DIR"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 目录创建成功${NC}"
else
    echo -e "${RED}✗ 目录创建失败${NC}"
    exit 1
fi

# 编译 main.cpp
echo -e "${YELLOW}编译 main.cpp...${NC}"
g++ -c main.cpp -o "$OBJ_DIR/main.o" -g -Wall
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ main.cpp 编译成功${NC}"
else
    echo -e "${RED}✗ main.cpp 编译失败${NC}"
    exit 1
fi

# 编译 Huffman.cpp
echo -e "${YELLOW}编译 Huffman.cpp...${NC}"
g++ -c Huffman.cpp -o "$OBJ_DIR/Huffman.o" -g -Wall
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Huffman.cpp 编译成功${NC}"
else
    echo -e "${RED}✗ Huffman.cpp 编译失败${NC}"
    exit 1
fi

# 链接
echo -e "${YELLOW}链接程序...${NC}"
g++ -o "$TARGET" "$OBJ_DIR/main.o" "$OBJ_DIR/Huffman.o"
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ 链接成功${NC}"
else
    echo -e "${RED}✗ 链接失败${NC}"
    exit 1
fi

# 显示文件信息
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}构建完成！${NC}"
echo -e "可执行文件: ${YELLOW}$(cygpath -w "$TARGET")${NC}"  # cygpath 转换 Windows 路径
if [ -f "$TARGET" ]; then
    SIZE=$(stat -c%s "$TARGET")
    echo -e "文件大小: ${YELLOW}$SIZE 字节${NC}"
fi
echo -e "${BLUE}========================================${NC}"

# 询问是否运行
read -p "是否现在运行程序？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}运行程序...${NC}"
    echo -e "${BLUE}----------------------------------------${NC}"
    "./$TARGET"
    echo -e "${BLUE}----------------------------------------${NC}"
    echo -e "${GREEN}程序运行结束${NC}"
fi