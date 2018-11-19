1. apt-get install systool

2. systool -m kvm_intel -v | grep -i nexted
Y

3. cat /sys/module/kvm_intel/parameters/nested
Y

4. Create & Run VM
-enable-kvm -cpu qemu64,+vmx

5. Verify VM VMX
root@demo-oVirt-Node:~# cat /proc/cpuinfo | grep vmx
flags		: fpu de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pse36 clflush mmx fxsr sse sse2 syscall nx lm rep_good nopl pni vmx cx16 x2apic hypervisor lahf_lm tpr_shadow vnmi flexpriority ept vpid
 
