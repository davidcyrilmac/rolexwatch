[app]

# (str) Title of your application
title = Rolex Day-Date-Month

# (str) Package name
package.name = rolexwatch

# (str) Package domain (needed for android/ios packaging)
package.domain = org.cyril

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (leave empty to include all)
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning (method 1)
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Keep the screen on (adds the WAKE_LOCK permission) - good for a clock
android.wakelock = True

# (list) The Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (bool) Accept the Android SDK license automatically (needed in CI)
android.accept_sdk_license = True

# (str) Use the Ant installed by apt instead of downloading it
android.ant_path = /usr/share/ant

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug with command output)
log_level = 2

# (int) Warn if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (int) Log level (0 = error only, 1 = info, 2 = debug with command output)
log_level = 2

# (int) Warn if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
