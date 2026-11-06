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

# (str) Application versioning
version = 0.1

# (list) Application requirements (pinned to versions known to work together)
requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0

# (str) Supported orientation (landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Keep the screen on (adds the WAKE_LOCK permission) - good for a clock
android.wakelock = True

# (list) The Android archs to build for (arm64-v8a covers the BlackBerry KEY2)
android.archs = arm64-v8a

# (bool) Accept the Android SDK license automatically (needed in CI)
android.accept_sdk_license = True

# (str) Use the Ant installed by apt instead of downloading it
android.ant_path = /usr/share/ant

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug with command output)
log_level = 2

# (int) Warn if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1
