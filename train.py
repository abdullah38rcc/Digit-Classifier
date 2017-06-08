# Arda Mavi

import os
import numpy as np
from get_dataset import get_dataset
from get_model import get_model, save_model
from keras.callbacks import ModelCheckpoint, TensorBoard
from keras.preprocessing.image import ImageDataGenerator

def train_model(model, X, X_test, Y, Y_test):

    batch_size = 100
    epochs = 5

    checkpoints = []
    if not os.path.exists('Data/Checkpoints/'):
        os.makedirs('Data/Checkpoints/')
    checkpoints.append(ModelCheckpoint('Data/Checkpoints/best_weights.h5', monitor='val_loss', verbose=0, save_best_only=True, save_weights_only=True, mode='auto', period=1))
    checkpoints.append(TensorBoard(log_dir='Data/Checkpoints/./logs', histogram_freq=0, write_graph=True, write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None))

    # Creates live data:
    # For better yield. The duration of the training is extended.

    # If you don't want, use this:
    # model.fit(X, Y, batch_size=batch_size, epochs=epochs, validation_data=(X_test, Y_test), shuffle=True, callbacks=checkpoints)

    generated_data = ImageDataGenerator(featurewise_center=False, samplewise_center=False, featurewise_std_normalization=False, samplewise_std_normalization=False, zca_whitening=False, rotation_range=0,  width_shift_range=0.1, height_shift_range=0.1, horizontal_flip = True, vertical_flip = False)
    generated_data.fit(X)

    model.fit_generator(generated_data.flow(X, Y, batch_size=batch_size), steps_per_epoch=X.shape[0]/6, epochs=epochs, validation_data=(X_test, Y_test), callbacks=checkpoints)

    return model

def main():
    X, X_test, Y, Y_test = get_dataset()
    model = train_model(get_model(), X, X_test, Y, Y_test)
    save_model(model)
    return model

if __name__ == '__main__':
    main()
