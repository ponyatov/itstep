BR_DEFCONFIG = raspberrypi3
CPU = BCM2837

FW_RPI_VER = 1.20190819
FW_RPI     = fw_rpi_$(FW_RPI_VER)
FW_RPI_GZ  = $(FW_RPI).tar.gz
firmware-rpi3: $(GZ)/$(FW_RPI_GZ)
	mkdir -p $(FW)/$(HW)/$(FW_RPI) ;\
	cd $(FW)/$(HW)/$(FW_RPI) 
	# ;\
	# tar zx < $<
$(GZ)/$(FW_RPI_GZ):
	wget -c -O $@ https://github.com/raspberrypi/firmware/archive/$(FW_RPI_VER).tar.gz
