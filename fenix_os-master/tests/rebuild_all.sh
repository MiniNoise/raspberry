#!/bin/bash

cd ../fenix_api
sudo python setup.py build
sudo python setup.py install
cd ../fenix_os
sudo python setup.py build
sudo python setup.py install
cd ../tests
