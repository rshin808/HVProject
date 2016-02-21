HVProject
=========
# Overview
This is the TEST controller code for the High Voltage Modules.  

Note: The TESTS are in the HV/TESTS directory  

# Requirements  
sudo apt-get install python-dev  
sudo apt-get install i2c-tools  
sudo apt-get install build-essential libi2c-dev libffi-dev
sudo pip install cffi
sudo pip install smbus-cffi

mkdir python-spi  
cd python-spi  
wget https://raw.github.com/doceme/py-spidev/master/setup.py  
wget https://raw.github.com/doceme/py-spidev/master/spidev_module.c  
wget https://raw.github.com/doceme/py-spidev/master/README.md  
wget https://raw.github.com/doceme/py-spidev/master/CHANGELOG.md  
sudo python setup.py install
