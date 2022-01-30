from os import getcwd


def create_model(PATH, id):
    import cv2 as cv
    import os
    import pathlib
    data = pathlib.Path(PATH)
    files = {'me': [], 'not-me': []}
    path = os.path.join(os.getcwd(), 'Dataset', str(id), 'ME')
    for image in os.listdir(path):
        if (image.endswith(".jpg")):
            files['me'].append(os.path.join(path, image))
    print('\n',files['me'][:3], '\n')
    # for dir in data.glob(os.path.join(os.getcwd(), 'Dataset', str(id), 'ME', '*.jpg')):
    #     files['me'].append(dir)
        
    path = os.path.join(os.getcwd(), 'Dataset', str(id), 'NOT-ME')
    for image in os.listdir(path):
        if (image.endswith(".jpg")):
            files['not-me'].append(os.path.join(path, image))
    print('\n',files['not-me'][:3], '\n')
    
    files_labels = {'me': 0, 'not-me': 1}

    # Loading all the directories as images
    img_size = [224, 224]               # Do list instead of tuple (this is done to add the third color channel later with east) but convert to tuple in cv2
    x= []
    y= []

    for label, list_dir in files.items():                       # To extract the key and the value from the dictionary
        for dir in list_dir:
            # print(str(dir))
            img = cv.imread(str(dir))
            img = cv.resize(img, tuple(img_size))
            # Saving the images into x
            x.append(img)
            # Adding in the label
            y.append(files_labels[label])
    import numpy as np
    x = np.array(x)
    y= np.array(y)

    from sklearn.model_selection import train_test_split

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state=0, shuffle=True)
    x_train = x_train / 255
    x_test = x_test / 255

    import keras    
    from keras.preprocessing.image import ImageDataGenerator
    train_datagen = ImageDataGenerator(
      rotation_range=10,
      shear_range=0.2,
      horizontal_flip=True,
      vertical_flip=False,
      fill_mode='nearest')

    # train_generator is actually an iterator
    train_generator = train_datagen.flow(x_train, y_train, batch_size=10)


    x_train_final = []
    y_train_final = []

    for i in range(30):
        images, labels = train_generator.next()
        data = list(zip(images, labels))
        for image, label in data:
            x_train_final.append(image)
            y_train_final.append(label)

    x_train_final = np.array(x_train_final)
    y_train_final = np.array(y_train_final)

    from keras.applications.mobilenet import MobileNet
    # Here we load the ResNet model with the trained weights of imagenet but not includeing the final layer as well will add additional layers
    # over here to train for our application

    res_net_base = MobileNet(input_shape= img_size + [3], weights='imagenet', include_top=False)
    # Supplying weights="imagenet" indicates that we want to use the pre-trained ImageNet weights for the respective model.

    # Setting all the current layers as non-trainable
    for layer in res_net_base.layers:
        layer.trainable = False

    from keras.layers import Dense, GlobalMaxPooling2D

    # Here we will be adding a maxPooling layer)
    add_layer1 = GlobalMaxPooling2D()

    # Adding the final dense layer (only 1 as it is a binary class)
    add_layer2 = Dense(1, activation='sigmoid')

    # Compiling the model
    final_model = keras.Sequential([res_net_base, 
                                add_layer1,
                                add_layer2])
    import tensorflow as tf
    # tf.keras.losses.BinaryCrossentropy

    final_model.compile(
        optimizer='adam',
        loss = tf.keras.losses.BinaryCrossentropy(),
        metrics=['accuracy']
    )

    final_model.fit(x_train_final, y_train_final, epochs = 5, batch_size=10, validation_data=(x_test, y_test))


    final_model.save(os.path.join(os.getcwd(), 'Models', str(id) + '.h5'))