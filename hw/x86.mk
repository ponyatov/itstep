BR_DEFCONFIG = qemu_x86
CPU ?= i486

firmware: firmware/bzImage firmware/rootfs.iso

firmware/%.iso: $(BR)/output/images/%.iso9660
	cp $< $@

emu: firmware/bzImage
	qemu-system-i386 -m 512M -kernel $<

#qemu-system-arm -enable-kvm -M virt -cpu host \
#-kernel zImage -initrd core-image-minimal-qemuarm.cpio.gz \
#-nographic -serial stdio -monitor none
