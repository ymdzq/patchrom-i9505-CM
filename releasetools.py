import common
import edify_generator

def RemoveDeviceAssert(info):
  edify = info.script
  for i in xrange(len(edify.script)):
    if "ro.product" in edify.script[i]:
      edify.script[i] = ''
      return

def AddLoki(info):
  info.script.script = [cmd for cmd in info.script.script if not "boot.img" in cmd]
  info.script.script = [cmd for cmd in info.script.script if not "show_progress(0.100000, 0);" in cmd]
  info.script.AppendExtra('package_extract_file("boot.img", "/tmp/boot.img");')
  info.script.AppendExtra('assert(run_program("/sbin/sh", "/system/etc/loki.sh") == 0);')
  info.script.AppendExtra('ifelse(is_substring("I337", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/gsm/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("I545", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/cdma/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("I545", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/vzw/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("I545", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox sed -i \'s/ro.com.google.clientidbase=android-google/ro.com.google.clientidbase=android-verizon/g\' /system/build.prop"));')
  info.script.AppendExtra('ifelse(is_substring("L720", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/cdma/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("M919", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/gsm/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("R970", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/cdma/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("I9505", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/gsm/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("I9507", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/gsm/* /system/"));')
  info.script.AppendExtra('ifelse(is_substring("I9508", getprop("ro.bootloader")), run_program("/sbin/sh", "-c", "busybox cp -R /system/blobs/gsm/* /system/"));')

def AddLinksForFirmware(info):
  edify = info.script
  firmware_assert = """symlink("/firmware-mdm/image/acdb.mbn", "/system/etc/firmware/acdb.mbn");
symlink("/firmware-mdm/image/apps.mbn", "/system/etc/firmware/apps.mbn");
symlink("/firmware-mdm/image/dsp1.mbn", "/system/etc/firmware/dsp1.mbn");
symlink("/firmware-mdm/image/dsp2.mbn", "/system/etc/firmware/dsp2.mbn");
symlink("/firmware-mdm/image/dsp3.mbn", "/system/etc/firmware/dsp3.mbn");
symlink("/firmware-mdm/image/efs1.mbn", "/system/etc/firmware/efs1.mbn");
symlink("/firmware-mdm/image/efs2.mbn", "/system/etc/firmware/efs2.mbn");
symlink("/firmware-mdm/image/efs3.mbn", "/system/etc/firmware/efs3.mbn");
symlink("/firmware-mdm/image/mdm_acdb.img", "/system/etc/firmware/mdm_acdb.img");
symlink("/firmware-mdm/image/rpm.mbn", "/system/etc/firmware/rpm.mbn");
symlink("/firmware-mdm/image/sbl1.mbn", "/system/etc/firmware/sbl1.mbn");
symlink("/firmware-mdm/image/sbl2.mbn", "/system/etc/firmware/sbl2.mbn");
symlink("/firmware/image/q6.b00", "/system/etc/firmware/q6.b00");
symlink("/firmware/image/q6.b01", "/system/etc/firmware/q6.b01");
symlink("/firmware/image/q6.b03", "/system/etc/firmware/q6.b03");
symlink("/firmware/image/q6.b04", "/system/etc/firmware/q6.b04");
symlink("/firmware/image/q6.b05", "/system/etc/firmware/q6.b05");
symlink("/firmware/image/q6.b06", "/system/etc/firmware/q6.b06");
symlink("/firmware/image/q6.mdt", "/system/etc/firmware/q6.mdt");
symlink("/firmware/image/tzapps.b00", "/system/etc/firmware/tzapps.b00");
symlink("/firmware/image/tzapps.b01", "/system/etc/firmware/tzapps.b01");
symlink("/firmware/image/tzapps.b02", "/system/etc/firmware/tzapps.b02");
symlink("/firmware/image/tzapps.b03", "/system/etc/firmware/tzapps.b03");
symlink("/firmware/image/tzapps.mdt", "/system/etc/firmware/tzapps.mdt");
symlink("/firmware/image/vidc.b00", "/system/etc/firmware/vidc.b00");
symlink("/firmware/image/vidc.b01", "/system/etc/firmware/vidc.b01");
symlink("/firmware/image/vidc.b02", "/system/etc/firmware/vidc.b02");
symlink("/firmware/image/vidc.b03", "/system/etc/firmware/vidc.b03");
symlink("/firmware/image/vidc.mdt", "/system/etc/firmware/vidc.mdt");
"""
  for i in xrange(len(edify.script)):
    if "symlink(" in edify.script[i] and "Roboto-Bold.ttf" in edify.script[i]:
      edify.script[i] = firmware_assert + 'symlink("/system/fonts/Roboto-Bold.ttf", "/system/fonts/DroidSans-Bold.ttf");'
      return

#def AddArgsForFormatSystem(info):
  #edify = info.script
  #for i in xrange(len(edify.script)):
    #if "format(" in edify.script[i] and "mmcblk0p16" in edify.script[i]:
      #edify.script[i] = 'format("ext4", "EMMC", "/dev/block/mmcblk0p16", "0", "/system");'
      #return

def WritePolicyConfig(info):
  try:
    file_contexts = info.input_zip.read("META/file_contexts")
    common.ZipWriteStr(info.output_zip, "file_contexts", file_contexts)
  except KeyError:
    print "warning: file_context missing from target;"

def InstallImage(img_name, img_file, partition, info):
  common.ZipWriteStr(info.output_zip, img_name, img_file)
  info.script.AppendExtra(('package_extract_file("' + img_name + '", "' + partition + '");'))

def FullOTA_InstallEnd(info):
  RemoveDeviceAssert(info)
  AddLinksForFirmware(info)
  AddLoki(info)

def IncrementalOTA_InstallEnd(info):
  RemoveDeviceAssert(info)
