CC      = gcc
CFLAGS  = -O2 -shared -fPIC -DRC_SHARED \
          -I rcheevos/include \
          -I rcheevos/src
LDFLAGS = -lz -lm

SRCS = \
  rcheevos/src/rc_compat.c \
  rcheevos/src/rc_util.c \
  rcheevos/src/rc_version.c \
  rcheevos/src/rcheevos/alloc.c \
  rcheevos/src/rcheevos/condition.c \
  rcheevos/src/rcheevos/condset.c \
  rcheevos/src/rcheevos/consoleinfo.c \
  rcheevos/src/rcheevos/format.c \
  rcheevos/src/rcheevos/lboard.c \
  rcheevos/src/rcheevos/memref.c \
  rcheevos/src/rcheevos/operand.c \
  rcheevos/src/rcheevos/rc_validate.c \
  rcheevos/src/rcheevos/richpresence.c \
  rcheevos/src/rcheevos/runtime.c \
  rcheevos/src/rcheevos/runtime_progress.c \
  rcheevos/src/rcheevos/trigger.c \
  rcheevos/src/rcheevos/value.c \
  rcheevos/src/rhash/aes.c \
  rcheevos/src/rhash/cdreader.c \
  rcheevos/src/rhash/hash.c \
  rcheevos/src/rhash/hash_disc.c \
  rcheevos/src/rhash/hash_encrypted.c \
  rcheevos/src/rhash/hash_rom.c \
  rcheevos/src/rhash/hash_zip.c \
  rcheevos/src/rhash/md5.c \
  rcheevos/src/rapi/rc_api_common.c \
  rcheevos/src/rapi/rc_api_editor.c \
  rcheevos/src/rapi/rc_api_info.c \
  rcheevos/src/rapi/rc_api_runtime.c \
  rcheevos/src/rapi/rc_api_user.c

TARGET = librcheevos.so

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $^ $(LDFLAGS) -o $@

clean:
	rm -f $(TARGET)
