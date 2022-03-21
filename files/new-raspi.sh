#format SD card with balena etcher, and install the latest raspian
#create a file on the card named SSH (no file extension)
#find the ip of the raspberry, it is displayed at the first boot or found via Advanced IP Scanner (Windows) or nmap in linux
#install a X11 "X Server" on your machine, for instance VcXSrv in Windows 10, or xquartz for Mac OS X http://xquartz.macosforge.org/
#login via SSH, for instance PuTTy in Windows 10 (enable X11!)
#login with username: "pi" and password "raspberry"

#arduino:
mkdir -p ~/Applications
cd ~/Applications
wget https://downloads.arduino.cc/arduino-1.8.13-linuxarm.tar.xz
tar xvJf arduino-1.8.13-linuxarm.tar.xz
cd arduino-1.8.13/
./install.sh
rm ../arduino-1.8.13-linuxarm.tar.xz

#teensy:
cd /etc/udev/rules.d/
sudo wget https://www.pjrc.com/teensy/49-teensy.rules
cd ~
sudo mkdir Downloads
cd ~/Downloads
sudo wget https://www.pjrc.com/teensy/td_153/TeensyduinoInstall.linuxarm # compatible with arduino 1.8.13
sudo chmod 755 TeensyduinoInstall.linuxarm
./TeensyduinoInstall.linuxarm
#choose where you put the installation files in the GUI
sudo rm -rf TeensyduinoInstall.linuxarm

#for gui installation just use
pip3 install dearpygui
