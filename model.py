from keras.models import Sequential
from keras.layers import Dense,Activation
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.core import Flatten,Dropout
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
import csv
from subprocess import check_output,call
import matplotlib.image as mpimg
import numpy as np
import math
import argparse

def gen_data_list(data_folder):
    """ generate list with information about all data points. Each data point is
    represented in the following manner:
    #0:c_image_path#1:l_image_path#2:r_image_path#3:s_angle#4:throttle#5:brake#6:speed
    """
    csv_files = str(check_output(['find','../'+data_folder,'-name','*.csv']),'utf-8')
    csv_files = csv_files.splitlines()

    data_list = []
    recovery_data_multiplier = 2
    right_turn_data_multiplier = 8
    for csv_file in csv_files:
        r = csv.reader(open(csv_file))
        file_entries = []
        file_entries += r
        data_list += file_entries
        if 'right_turn' in csv_file:
            for i in range(1,right_turn_data_multiplier):
                data_list += file_entries
        elif 'recovery' in csv_file:
            for i in range(1,recovery_data_multiplier):
                data_list += file_entries
    return shuffle(data_list,random_state=314159)

def normalize(image):
    image.astype('float32')
    image = image / 255.0
    image -= 0.5
    return image

def data_generator(data_list,batch_size):
    inputs = []
    targets = []
    size = 0
    while True:
        for data_point in data_list:
            image = mpimg.imread(data_point[0])
            image = [normalize(image)]
            steer_angle = [float(data_point[3])]
            inputs += image
            targets += steer_angle
            size += 1
            if size == batch_size:
                yield (np.array(inputs),np.array(targets))
                size = 0
                inputs = []
                targets = []
    

model = Sequential()
#first conv layer
model.add(Convolution2D(24,5,5,border_mode='valid', input_shape=(160,320,3)))
model.add(MaxPooling2D(dim_ordering='th'))
model.add(Activation('relu'))
#model.add(Dropout(0.1))
#second conv layer
model.add(Convolution2D(36,5,5,border_mode='valid'))
model.add(MaxPooling2D(dim_ordering='th'))
model.add(Activation('relu'))
#model.add(Dropout(0.1))
#third conv layer
model.add(Convolution2D(48,5,5,border_mode='valid'))
model.add(MaxPooling2D(dim_ordering='th'))
model.add(Activation('relu'))
#model.add(Dropout(0.1))
#fourth conv layer
model.add(Convolution2D(64,3,3,border_mode='valid'))
model.add(MaxPooling2D(dim_ordering='th'))
model.add(Activation('relu'))
#model.add(Dropout(0.1))
#fifth conv layer
model.add(Convolution2D(64,3,3,border_mode='valid'))
model.add(MaxPooling2D(dim_ordering='th'))
model.add(Activation('relu'))
#model.add(Dropout(0.1))
model.add(Flatten())
#first fully connected layer
model.add(Dense(100))
model.add(Activation('relu'))
#second fully connected layer
model.add(Dense(50))
model.add(Activation('relu'))
#third fully connected layer
model.add(Dense(10))
model.add(Activation('relu'))
#output layer
model.add(Dense(1))

model.compile(optimizer='adam',loss='mse',metrics=['accuracy'])

parser = argparse.ArgumentParser()
parser.add_argument('data',type=str,help='Please provice name of data directory')
args = parser.parse_args()
data_list = gen_data_list(args.data)
num_data_points = len(data_list)
print("data list has: ",num_data_points," entries")
batch_size = 32
validation_percent = 0.05
num_validation_points  = int(validation_percent*num_data_points)
num_train_points = num_data_points - num_validation_points
validation_list = data_list[0:num_validation_points]
train_list = data_list[num_validation_points:]
validation_samples = batch_size * math.ceil(num_validation_points/batch_size)
train_samples_per_epoch = batch_size * math.ceil(num_train_points/batch_size)
valid_gen = data_generator(validation_list,batch_size)
train_gen = data_generator(train_list,batch_size)
#print("first entry is:")
#print(next(data_gen))

history = model.fit_generator(train_gen,train_samples_per_epoch,nb_epoch=1,validation_data=valid_gen,\
                                  nb_val_samples=validation_samples)

print('training result: ',history.history)

#save model to file
model.save_weights('model.h5')
f = open('model.json','w')
f.write(model.to_json())
