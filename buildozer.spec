[app]
title = Rogue Tower
package.name = roguetowr
package.domain = org.roguetowr

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_patterns = build/*,bin/*,.git/*

version = 1.0

requirements = python3,kivy,pygame

permissions = INTERNET

orientation = portrait

fullscreen = 1

android.permissions = INTERNET
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Kivy-specific settings
p4a.branch = develop
p4a.requirements = python3,kivy,pygame,pyjnius

# Build settings
log_level = 2
warn_on_root = 1
