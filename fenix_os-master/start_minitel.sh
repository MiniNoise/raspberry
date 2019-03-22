#!/bin/bash

cd fenix_os
sudo python ./setup.py build
sudo python ./setup.py install
cd ../tests
sudo python ./main.py
