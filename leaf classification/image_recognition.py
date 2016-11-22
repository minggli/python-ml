import numpy as np
import os, sys
import matplotlib.pyplot as plt


__author__ = 'Ming Li'
# This application forms a submission from Ming in regards to leaf classification challenge on Kaggle community

path = 'leaf/images/'
pic_names = {i: path + str(i) + '.jpg' for i in range(1, 1585, 1)}


# exploring possible feature

pic = pic_names[99]