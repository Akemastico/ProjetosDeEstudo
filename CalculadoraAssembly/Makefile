ASM = nasm
ASM_FLAGS = -f elf64
LD = ld
TARGET = main
SRC = main.asm
OBJ = main.o

# Regra principal
all: $(TARGET)

# Como gerar o executável (liga o objeto)
$(TARGET): $(OBJ)
	$(LD) $(OBJ) -o $(TARGET)

# Como gerar o arquivo objeto (monta o assembly)
$(OBJ): $(SRC)
	$(ASM) $(ASM_FLAGS) $(SRC) -o $(OBJ)

# Limpa os arquivos gerados
clean:
	rm -f $(OBJ) $(TARGET)