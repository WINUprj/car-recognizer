from tensorflow import keras

def init():
    # read model
    with open('model.json', 'r') as json_file:
        loaded_model_json = json_file.read()
    loaded_model = keras.models.model_from_json(loaded_model_json)
    loaded_model.load_weights('model.h5')

    print('Model loaded successfully')

    loaded_model.compile(loss='sparse_categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])

    return loaded_model

