[app]
title = Rolex Day-Date-Month
package.name = rolexwatch
package.domain = org.cyril
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy
orientation = portrait
android.wakelock = True
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True
android.ant_path = /usr/share/ant

[buildozer]
log_level = 2
warn_on_root = 1
