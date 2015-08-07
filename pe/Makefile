sources := $(wildcard chapter_??/*.erl)
binaries :=  $(subst .erl,.beam,$(sources))

.PHONY: clean
clean:
	rm -f $(binaries) 2>/dev/null
