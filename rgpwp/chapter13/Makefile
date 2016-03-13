generated_files := qrc_resources.py

%.py: %.qrc
	pyrcc4 $< -o $@

.PHONY: all
all: $(generated_files)

.PHONY: clean
clean:
	@rm -f $(generated_files)
	@rm -f *.pyc
