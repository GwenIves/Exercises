############### Definitions

main_sources := $(wildcard *.cpp)

sources := $(main_sources)

dependencies := $(subst .cpp,.d,$(sources))
objects := $(subst .cpp,.o,$(sources))

executables := $(subst .cpp,,$(main_sources))

WARNINGS := -Werror --pedantic -Wall -Wextra -Winit-self -Wswitch-default -Wfloat-equal -Wshadow -Wwrite-strings
CXXFLAGS += $(WARNINGS) -std=c++11 -O3

.o:
	$(LINK.cc) $^ -o $@

############### Top level targets

.PHONY: build
build: $(executables)

.PHONY: all
all: build tags

.PHONY: clean
clean:
	@echo "Deleting all executables"
	@rm -f $(executables) 2>/dev/null
	@echo "Deleting all object files"
	@rm -f $(objects) 2>/dev/null
	@echo "Deleting all dependency files"
	@rm -f $(dependencies)
	@echo "Deleting all archive files"
	@rm -f *.a

.PHONY: distclean
distclean: clean
	@echo "Deleting all generated files"
	@rm -f tags

tags: $(sources)
	ctags --recurse=yes

############### Dependency generation

INCLUDE_DEPS := $(if $(findstring $(MAKECMDGOALS),clean distclean tags),N,Y)

# $(call make-dependencies,source-file,object-file,depend-file)
define make-dependencies
  $(CXX) -x c++         \
         -MM            \
         -MF $3         \
         -MP            \
         -MT $2         \
         -MT $3         \
         $(CPPFLAGS)    \
         $1
endef

ifeq "$(INCLUDE_DEPS)" "Y"
  -include $(dependencies)
endif

############### Explicit dependencies and rules

%.d: %.cpp
	$(call make-dependencies, $<,$(subst .d,.o,$@),$@)
