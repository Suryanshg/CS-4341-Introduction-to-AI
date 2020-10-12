from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical
import numpy as np

# Preprocessing data
imgData = np.load('images.npy')
labelData = np.load('labels.npy')

flatImgData=[] # Flattened image data from 28X28 matrix to a vector of 784 values
for i in range(len(imgData)):
    flatImgData.append(imgData[i].flatten())

oneHotVectors = to_categorical(labelData)

dataSet = [] # List of classes of image data, indexed by their truth values for labels.
for i in range(10):
    dataSet.append([])  

for i in range(len(flatImgData)): # Setting up the dataSet according to classes
    index = np.argmax(oneHotVectors[i])
    x_data = flatImgData[i]
    y_data = oneHotVectors[i]
    data = np.concatenate((x_data, y_data))
    dataSet[index].append(data)

# for data in dataSet: # Shuffling the vectors for each classes randomly
#     np.random.shuffle(data)

# train_data = []
# for data in dataSet:
#     upperLimit = int(len(data) * 0.6)
#     x_data = data[0:upperLimit+1]
#     y_data = []







    


    


# Model Template

model = Sequential() # declare model
model.add(Dense(10, input_shape=(28*28, ), kernel_initializer='he_normal')) # first layer
model.add(Activation('relu'))
#
#
#
# Fill in Model Here
#
#
model.add(Dense(10, kernel_initializer='he_normal')) # last layer
model.add(Activation('softmax'))


# Compile Model
model.compile(optimizer='sgd',
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

# Train Model
#history = model.fit(x_train, y_train,  validation_data = (x_val, y_val), epochs=10, batch_size=512)


# Report Results

#print(history.history)
#model.predict()