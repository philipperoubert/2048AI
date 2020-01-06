# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 19:37:03 2020

@author: Thomas
"""
import tensorflow as tf
from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())

if tf.test.gpu_device_name():
    print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
else:
    print("Please install GPU version of TF")