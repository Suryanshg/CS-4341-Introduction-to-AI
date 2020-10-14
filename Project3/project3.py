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
    data = np.concatenate((x_data, y_data)) # Concatenating the x_data and y_data for uniform shuffling in future
    dataSet[index].append(data)

train_data = []
val_data = []
test_data = []

for data in dataSet: # Doing Stratified Sampling
    upperLimit60 = int(len(data) * 0.6)
    upperLimit75 = int(len(data) * 0.75)
    train_data.extend(data[0:upperLimit60+1])
    val_data.extend(data[upperLimit60+1:upperLimit75+1])
    test_data.extend(data[upperLimit75+1:])

# Performing Random Shuffling
np.random.shuffle(train_data)
np.random.shuffle(test_data)
np.random.shuffle(val_data)

# Segregating Concatenated data into respective x and y data
x_train = []
y_train = []

for data in train_data:
    x_train.append(data[0:len(data)-10])
    y_train.append(data[len(data)-10:])

x_val = []
y_val = []

for data in val_data:
    x_val.append(data[0:len(data)-10])
    y_val.append(data[len(data)-10:])

x_test = []
y_test = []

for data in test_data:
    x_test.append(data[0:len(data)-10])
    y_test.append(data[len(data)-10:])


# Model Template

model = Sequential() # declare model
model.add(Dense(10, input_shape=(28*28, ), kernel_initializer='he_normal')) # first layer
model.add(Activation('sigmoid'))

# model.add(Dense(2, kernel_initializer='he_normal')) # second layer
# model.add(Activation('relu'))

model.add(Dense(10, kernel_initializer='he_normal')) # last layer
model.add(Activation('softmax'))


# Compile Model
model.compile(optimizer='sgd',
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

#Train Model
history = model.fit(np.array(x_train), np.array(y_train),  validation_data = (np.array(x_val), np.array(y_val)), epochs=10, batch_size=512)


#Report Results
#print(history.history)
prediction = model.predict(np.array(x_test))
# x = model.evaluate(np.array(x_test), np.array(y_test), verbose=1)
print(np.argmax(prediction[0]))
print(np.argmax(y_test[0]))