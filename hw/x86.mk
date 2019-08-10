BR_DEFCONFIG = qemu_x86
CPU ?= i486

firmware: firmware/bzImage firmware/rootfs.iso9660

emu: firmware/bzImage
	qemu-system-i386 -m 512M -kernel $<

#qemu-system-arm -enable-kvm -M virt -cpu host \
#-kernel zImage -initrd core-image-minimal-qemuarm.cpio.gz \
#-nographic -serial stdio -monitor none
