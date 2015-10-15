#!/system/bin/sh
if [ -f /system/etc/recovery-transform.sh ]; then
  exec sh /system/etc/recovery-transform.sh 8366080 b85723f3cce22098826574c4830f908c1c6f1780 6137856 503e4bf7c9af1a287cd44429d381482fe7f17123
fi

if ! applypatch -c EMMC:/dev/block/platform/msm_sdcc.1/by-name/recovery:8366080:b85723f3cce22098826574c4830f908c1c6f1780; then
  log -t recovery "Installing new recovery image"
  applypatch -b /system/etc/recovery-resource.dat EMMC:/dev/block/platform/msm_sdcc.1/by-name/boot:6137856:503e4bf7c9af1a287cd44429d381482fe7f17123 EMMC:/dev/block/platform/msm_sdcc.1/by-name/recovery b85723f3cce22098826574c4830f908c1c6f1780 8366080 503e4bf7c9af1a287cd44429d381482fe7f17123:/system/recovery-from-boot.p
else
  log -t recovery "Recovery image already installed"
fi
