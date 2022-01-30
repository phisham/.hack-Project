from spacy import load


"""
data = {
        'id': id
        }
"""

def save_member(PATH, id):
    import shutil
    import os
    shutil.copytree(PATH, os.path.join(PATH, 'ME'))
    shutil.copytree(os.path.join(os.getcwd(), 'not_me_data'), os.path.join(PATH, 'NOT-ME'))
    from model_train import create_model
    create_model(PATH, id)

    return {'res': 0}

def request(data):

    from tensorflow.keras.models import load_model
    import os
    import cv2 as cv
    import numpy as np

    PATH = os.path.join(os.getcwd(), 'Dataset', str(data['id']))
    print("\n", PATH, '\n')
    img_size = [224,224]
    print('\n', os.path.join(PATH, str(data['id'])+'.jpg'), '\n')
    image = cv.resize(cv.imread(os.path.join(PATH, str(data['id'])+'.jpg')), tuple(img_size))
    image = image/255
    image = np.array([image])

    for model in os.listdir(os.path.join(os.getcwd(), 'Models')):
        model = load_model(os.path.join(os.getcwd(), 'Models', model))

        result = model.predict(image)

        if 1 - float(result) >= 0.75:
            return {'res': -1}
        else:
            continue
    return save_member(PATH, data['id'])

# for file in :

value = request({'id':1})
print(value)