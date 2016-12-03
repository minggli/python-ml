import os
import pandas as pd
import numpy as np
import warnings
from utils import delete_folders, extract, pic_resize, batch_iter
from GradientDescent import GradientDescent
from sklearn import model_selection
import tensorflow as tf
warnings.filterwarnings('ignore')

# coding: utf-8

__author__ = 'Ming Li'

"""This application forms a submission from Ming Li in regards to leaf kaggle challenge challenge on Kaggle community"""

# params

dir_path = 'leaf/images/'
pid_label, pid_name = extract('leaf/train.csv')
pic_names = [i.name for i in os.scandir(dir_path) if i.is_file() and i.name.endswith('.jpg')]
input_shape = (96, 96)
m = input_shape[0] * input_shape[1]  # num of flat array
n = len(set(pid_name.values()))


# load image into tensor

sess = tf.Session()

# declare placeholders

x = tf.placeholder(dtype=tf.float32, shape=[None, m], name='feature')  # pixels as features
y_ = tf.placeholder(dtype=tf.float32, shape=[None, n], name='label')  # 99 classes in 1D tensor

# declare variables

W = tf.Variable(tf.zeros([m, n]))
b = tf.Variable(tf.zeros([n]))

init = tf.global_variables_initializer()
sess.run(init)

y = tf.matmul(x, W) + b

# loss function
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y, y_))
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


# First Convolution Layer
W_conv1 = weight_variable([5, 5, 1, 32])
b_conv1 = bias_variable([32])

x_image = tf.reshape(x, [-1, input_shape[0], input_shape[1], 1])

h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

# Second layer
W_conv2 = weight_variable([5, 5, 32, 64])
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# Densely connected layer
W_fc1 = weight_variable([24 * 24 * 64, 1024])
b_fc1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 24*24*64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

# Dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# Readout layer
W_fc2 = weight_variable([1024, n])
b_fc2 = bias_variable([n])

y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2


cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(y_conv, y_))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

init = tf.global_variables_initializer()
sess.run(init)


def main():

    print('\n\n\n\n starting cross validation... \n\n\n\n')

    for batch in batches:
        i = batch[0]
        x_batch, y_batch = zip(*batch[1])
        x_batch = np.array(x_batch)
        y_batch = np.array(y_batch)
        if i % 5 == 0:
            train_accuracy = accuracy.eval(feed_dict={x: valid_x, y_: valid_y, keep_prob: 1.0}, session=sess)
            print("step {0}, training accuracy {1}".format(i, train_accuracy))
        train_step.run(feed_dict={x: x_batch, y_: y_batch, keep_prob: 0.5}, session=sess)

# cross validation of training photos

cross_val = True
delete = True

if delete:
    delete_folders()

kf_iterator = model_selection.StratifiedKFold(n_splits=5, shuffle=True, random_state=1)  # Stratified
train_x = list(pid_name.keys())  # leaf id
train_y = list(pid_name.values())  # leaf species names

for train_index, valid_index in kf_iterator.split(train_x, train_y):

    leaf_images = dict()  # temp dictionary of re-sized leaf images
    train = list()  # array of image and label in 1D array
    valid = list()  # array of image and label in 1D array

    train_id = [train_x[idx] for idx in train_index]
    valid_id = [train_x[idx] for idx in valid_index]

    for filename in pic_names:

        pid = int(filename.split('.')[0])
        leaf_images[pid] = pic_resize(dir_path + filename, size=input_shape, pad=True)

        if pid in train_id:
            directory = dir_path + 'train/' + pid_name[pid]
            train.append((np.array(leaf_images[pid]).flatten(), np.array(pid_label[pid])))

        elif pid in valid_id:
            directory = dir_path + 'validation/' + pid_name[pid]
            valid.append((np.array(leaf_images[pid]).flatten(), np.array(pid_label[pid])))

        else:
            directory = dir_path + 'test'

        if not os.path.exists(directory):
            os.makedirs(directory)

        leaf_images[pid].save(directory + '/' + filename)

    train = np.array(train)
    valid = np.array(valid)

    # create batches
    batches = batch_iter(data=train, batch_size=50, num_epochs=30)
    valid_x = np.array([i[0] for i in valid])
    valid_y = np.array([i[1] for i in valid])

    main()

    if not cross_val:
        break

