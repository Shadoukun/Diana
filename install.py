import subprocess
import os
import site
import platform


platform = platform.system()

if platform == 'Linux':
    print("Platform is Linux.")
    # Python site-package directory
    site_packages = "/usr/local/lib/python3.6/site-packages"
    # 2to3 location
    twoToThree = "/usr/bin/2to3"

if platform == "Windows":
    print("Platform is Windows.")
    # Python site-package directory
    site_packages = "C:\\Python36\\Lib\\site-packages"
    # 2to3 location
    twoToThree = "C:\\Python36\\Tools\\scripts\\2to3.py"

# install packages
pkg_install = subprocess.call(["pip", "install", "-r", "requirements.txt"], shell=True)

# convert flickr_api to python3
flickr_api = site_packages + "\\flickr_api"
subprocess.call([twoToThree, "-n", flickr_api, "-w"], shell=True)
