#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

rm -rf bin/*
#rm -rf builds/*

rm -rf releng/airootfs/usr/local/share/secux-apps
rm -rf releng/airootfs/usr/local/share/secux-installer
rm -rf releng/airootfs/usr/local/share/kirt-app
git clone --depth=1 https://github.com/kolbanidze/secux-installer.git releng/airootfs/usr/local/share/secux-installer
git clone --depth=1 https://github.com/kolbanidze/secux-apps.git releng/airootfs/usr/local/share/secux-apps
git clone --depth=1 https://github.com/kirt-king/test_app.git releng/airootfs/usr/local/share/kirt-app
touch releng/airootfs/usr/local/share/secux-installer/production.conf
touch releng/airootfs/usr/local/share/secux-installer/offline_installation.conf
rm -rf releng/airootfs/var/cache/pacman/offline-repo/*
cp /var/cache/pacman/offline-repo/* releng/airootfs/var/cache/pacman/offline-repo

rm releng/airootfs/etc/pacman.conf
cp releng/airootfs/etc/pacman_offline.conf releng/airootfs/etc/pacman.conf

cd releng/airootfs/usr/local/share/secux-installer
./collect_python_packages.sh
cd ../../../../../..

mkarchiso -v -w bin/ -o bin/ releng/
mv bin/*.iso builds/secux-offline-"$(date +"%d-%B-%H-%M")".iso

# Online
#rm -rf bin/*
#rm releng/airootfs/usr/local/share/secux-installer/offline_installation.conf
#rm releng/airootfs/etc/pacman.conf
#cp releng/airootfs/etc/pacman_online.conf releng/airootfs/etc/pacman.conf
#rm -rf releng/airootfs/var/cache/pacman/offline-repo/*
#mkarchiso -v -w bin/ -o bin/ releng/
#mv bin/*.iso builds/secux-web-"$(date +"%d-%B")".iso
