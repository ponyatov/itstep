firmware: $(FW)/$(HW)/bzImage $(FW)/$(HW)/$(APP)_$(HW).iso

$(FW)/$(HW)/$(APP)_$(HW).iso: $(BR)/output/images/rootfs.iso9660
	cp $< $@

emu: $(FW)/$(HW)/bzImage
	qemu-system-i386 -m 512M -kernel $<

#qemu-system-arm -enable-kvm -M virt -cpu host \
#-kernel zImage -initrd core-image-minimal-qemuarm.cpio.gz \
#-nographic -serial stdio -monitor none
