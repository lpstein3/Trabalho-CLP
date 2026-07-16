CC = gcc
CFLAGS = -Wall -O3 -fPIC
LDFLAGS = -shared

SRC_DIR = src
TARGET = $(SRC_DIR)/libmandel.so

all: $(TARGET)

$(TARGET): $(SRC_DIR)/mandelbrot.c
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)

run: all
	python gui/main.py