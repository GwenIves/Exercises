generated_files := ui_ticket_order.py

%.py: %.ui
	pyuic4 $< -o $@

.PHONY: all
all: $(generated_files)

.PHONY: clean
clean:
	@rm -f $(generated_files)
	@rm -f *.pyc
