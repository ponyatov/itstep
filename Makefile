MODULE = $(notdir $(CURDIR))

CWD = $(CURDIR)
GZ  = $(CWD)/gz
TMP = $(CWD)/tmp
SRC = $(TMP)/src
FW  = $(CWD)/firmware

BR_VER = 2019.05.2

BR     = buildroot-$(BR_VER)
BR_GZ  = $(BR).tar.gz

.PHONY: os dirs gz src build firmware emu doc wiki merge update 

APP ?= os
HW  ?= x86

include app/$(APP).mk
include hw/$(HW).mk
include cpu/$(CPU).mk
include arch/$(ARCH).mk

###########################################
	
DOC = README.md wiki/*.md

doc: docs/index.html
docs/index.html: $(DOC) Makefile
	pandoc --metadata pagetitle=" " -f gfm -t html -s --toc -o $@ $(DOC)

wiki:
	cd wiki ; git pull -v
#	git clone -o gh git@github.com:ponyatov/itstep.wiki.git wiki

########################################### OS

os: dirs gz src build firmware

dirs:
	mkdir -p $(GZ) $(TMP) $(SRC) $(FW) $(FW)/$(HW)

distclean:
	$(MAKE) -C $(BR) distclean ; rm -rf $(SRC)
	
gz: $(GZ)/$(BR_GZ)

CONFIG_MK  =        	   $(CWD)/app/$(APP).mk $(CWD)/hw/$(HW).mk
CONFIG_MK +=		 	   $(CWD)/cpu/$(CPU).mk $(CWD)/arch/$(ARCH).mk
CONFIG_BR  = $(CWD)/all.br $(CWD)/app/$(APP).br $(CWD)/hw/$(HW).br
CONFIG_BR += 			   $(CWD)/cpu/$(CPU).br $(CWD)/arch/$(ARCH).br

CONFIG_BB = $(CWD)/app/$(APP).bbox

CONFIG_KR  = $(CWD)/all.kernel $(CWD)/hw/$(HW).kernel
CONFIG_KR += $(CWD)/cpu/$(CPU).kernel $(CWD)/arch/$(ARCH).kernel

EXTRA_BB = $(CWD)/buildroot:$(CWD)/gambox:$(CWD)/netkit:$(CWD)/iot

build: $(BR)/.config
	cd $(BR) ; make menuconfig && make
$(BR)/.config: $(BR)/README Makefile $(CONFIG_BR) $(CONFIG_BB) $(CONFIG_MK)
	cd $(BR) ; make BR2_EXTERNAL=\"$(EXTRA_BB)\" $(BR_DEFCONFIG)_defconfig
	cat $(CONFIG_BR) >> $@
	echo BR2_DL_DIR=\"$(CWD)/gz\" >> $@
	echo BR2_ROOTFS_OVERLAY=\"$(CWD)/rootfs\" >> $@
	echo BR2_LINUX_KERNEL_CONFIG_FRAGMENT_FILES=\"$(CONFIG_KR)\" >> $@
	echo BR2_LINUX_KERNEL_CUSTOM_LOGO_PATH=\"$(CWD)/wiki/logo.png\" >> $@
	echo BR2_PACKAGE_BUSYBOX_CONFIG_FRAGMENT_FILES=\"$(CONFIG_BB)\" >> $@

src: buildroot
buildroot: $(BR)/README
	ln -fs $(BR) buildroot
$(BR)/README: $(GZ)/$(BR_GZ)
	tar zx < $< && touch $@

$(GZ)/$(BR_GZ):
	wget -c -O $@ https://github.com/buildroot/buildroot/archive/$(BR_VER).tar.gz
	
firmware/%: $(BR)/output/images/%
	cp $< $@
	
MERGE  = Makefile README.md .gitignore
MERGE += app hw cpu arch all.* firmware rootfs src buildroot*
MERGE += mex
MERGE += metaL

.PHONY: merge release
merge:
	git checkout master
	git checkout ponyatov -- $(MERGE) 
#	$(MAKE) wiki ; $(MAKE) doc

.PHONY: debian
debian:
	$(MAKE) -C docker

.PHONY: dock
dock: Dockerfile .dockerignore 
	docker build -t itstep .
	docker run --rm -it -v $(CWD):/itstep itstep mc

.PHONY: update requirements.txt
update:
	pip install -U pip
	pip install -U -r requirements.txt

requirements.txt:
	pip freeze | grep -v 0.0.0 > $@
