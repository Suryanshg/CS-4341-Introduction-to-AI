from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.utils import to_categorical
import numpy as np
import matplotlib.pyplot as plt

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
    np.random.shuffle(data) # Performing Random Shuffling
    upperLimit60 = int(len(data) * 0.6)
    upperLimit75 = int(len(data) * 0.75)
    train_data.extend(data[0:upperLimit60])
    val_data.extend(data[upperLimit60:upperLimit75])
    test_data.extend(data[upperLimit75:])

# np.random.shuffle(train_data)
# np.random.shuffle(test_data)
# np.random.shuffle(val_data)

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
model.add(Dense(100, input_shape=(28*28, ), kernel_initializer='random_normal')) # first layer
model.add(Activation('relu'))

model.add(Dense(200, kernel_initializer='random_normal')) # Second layer
model.add(Activation('selu'))

model.add(Dense(300, kernel_initializer='random_normal')) # Third layer
model.add(Activation('tanh'))

# model.add(Dense(50, kernel_initializer='random_normal')) # Fourth layer
# model.add(Activation('relu'))

model.add(Dense(10, kernel_initializer='he_normal')) # last layer
model.add(Activation('softmax'))


# Compile Model
model.compile(optimizer='sgd',
              loss='categorical_crossentropy', 
              metrics=['accuracy'])

#Train Model
history = model.fit(np.array(x_train), np.array(y_train),  validation_data = (np.array(x_val), np.array(y_val)), epochs=250, batch_size=128)


#Report Results
val_accuracy = history.history['val_accuracy']
train_accuracy = history.history['accuracy']

# Plotting Learning curves for Training and Validation Data

plt.plot(range(250),train_accuracy,'r', label = 'Training Accuracy')
plt.plot(range(250),val_accuracy,'b', label = 'Validation Accuracy')
plt.legend(loc='lower right')
plt.xlabel('Number of Epochs')
plt.ylabel('Training / Validation Accuracy')
plt.show()




x = model.evaluate(np.array(x_test), np.array(y_test), verbose=1)
print ("Accuracy of Test Set is: ", str(x[1]))

prediction = model.predict(np.array(x_test))

# Detection of 3 Misclassified Images
count = 0
misClassifiedImages = []
for i in range(len(y_test)):
    if(np.argmax(y_test[i]) != np.argmax(prediction[i])):
        img = np.array(x_test[i]).reshape(28,28)
        misClassifiedImages.append(img)
        count+=1
    if count==3:
        break

for image in misClassifiedImages:
    plt.imshow(image, cmap = 'gray', vmin = 0, vmax = 255)    
    plt.show()


# Constructing Confusion Matrix
confusionMatrix = []
for i in range(10):
    l = []
    for j in range(10):
        l.append(0)
    confusionMatrix.append(l)

for i in range(len(y_test)):
    true_val = np.argmax(y_test[i])
    predicted_val = np.argmax(prediction[i])
    confusionMatrix[true_val][predicted_val]+= 1

# Printing Confusion Matrix
print("Confusion Matrix is:")
print("   0 1 2 3 4 5 6 7 8 9")
print("   -------------------")
for i in range(10):
    print(str(i)+"| ",end = '')
    for j in range(10):
        print(str(confusionMatrix[i][j]) + " ",end = '')
    print()

# Saving model
model.save("best_trained_model")




