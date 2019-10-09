firmware: $(FW)/$(HW)/uImage firmware-$(HW)

emu: $(FW)/$(HW)/uImage
	qemu-system-arm -m 512M -kernel $<
