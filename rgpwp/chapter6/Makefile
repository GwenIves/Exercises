generated_files := ui_newimagedlg.py qrc_resources.py

%.py: %.qrc
	pyrcc4 $< -o $@

%.py: %.ui
	pyuic4 $< -o $@

.PHONY: all
all: $(generated_files)

.PHONY: clean
clean:
	@rm -f $(generated_files)
	@rm -f *.pyc
