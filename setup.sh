cd tabi-master && virtualenv -p /usr/bin/python2.7 ve-tabi && source ve-tabi/bin/activate && cd ..
cd mabo-master && make && cd ..
cd tabi-master && python setup.py install
