
APP ?= os
HW ?= x86

include app/$(APP).mk
include hw/$(HW).mk
include cpu/$(CPU).mk

###########################################
	
DOC = README.md wiki/*.md
.PHONY: doc wiki
doc: docs/index.html
docs/index.html: $(DOC) Makefile
	pandoc --metadata pagetitle=" " -f gfm -t html -s --toc -o $@ $(DOC)

wiki:
	cd wiki ; git pull -v
#	git clone -o gh git@github.com:ponyatov/itstep.wiki.git wiki

########################################### OS

BR_VER = 2019.02.4
BR     = buildroot-$(BR_VER)
BR_GZ  = $(BR).tar.gz

MODULE = $(notdir $(CURDIR))

CWD = $(CURDIR)
GZ  = $(CWD)/gz
TMP = $(CWD)/tmp
SRC = $(TMP)/src
FW  = $(CWD)/firmware

os: dirs gz src build

dirs:
	mkdir -p $(GZ) $(TMP) $(SRC) $(FW)
	
gz: $(GZ)/$(BR_GZ)

build: $(BR)/.config
	cd $(BR) ; make menuconfig && make
$(BR)/.config: $(BR)/README all.br app/$(APP).br hw/$(HW).br cpu/$(CPU).br \
				Makefile app/$(APP).mk hw/$(HW).mk cpu/$(CPU).mk
	cd $(BR) ; make $(BR_DEFCONFIG)_defconfig
	cat all.br app/$(APP).br hw/$(HW).br cpu/$(CPU).br >> $@
	echo "BR2_DL_DIR=\"$(CWD)/gz\"" >> $@
	echo BR2_ROOTFS_OVERLAY=\"$(CWD)/rootfs\" >> $@

src: buildroot
buildroot: $(BR)/README
	ln -fs $(BR) buildroot
$(BR)/README: $(GZ)/$(BR_GZ)
	tar zx < $< && touch $@

$(GZ)/$(BR_GZ):
	wget -c -O $@ https://github.com/buildroot/buildroot/archive/$(BR_VER).tar.gz

.PHONY: update release
update:
	git checkout master
	git checkout ponyatov -- Makefile app hw cpu all.br rootfs README.md
	$(MAKE) wiki ; $(MAKE) doc
