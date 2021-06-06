import os

from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials


# Do not worry about this function, it is for pretty printing the attributes!
def pretty_print(klass, indent=0):
    if '__dict__' in dir(klass):
        print(' ' * indent + type(klass).__name__ + ':')
        indent += 4
        for k, v in klass.__dict__.items():
            if '__dict__' in dir(v):
                pretty_print(v, indent)
            elif isinstance(v, list):
                print(' ' * indent + k + ':')
                for item in v:
                    pretty_print(item, indent)
            else:
                print(' ' * indent + k + ': ' + str(v))
    else:
        indent += 4
        print(' ' * indent + klass)


# Authenticate

subscription_key = os.environ["AZURE_COMPUTER_VISION_SUBSCRIPTION_KEY"]
endpoint = os.environ["AZURE_COMPUTER_VISION_ENDPOINT"]

face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))

face_to_find_similars_url = open('faces/person1.txt').readlines()[0]
person1_face_id = face_client.face.detect_with_url(url=face_to_find_similars_url, detection_model='detection_03',
                                                   recognition_model='recognition_04', return_face_id=True)[0].face_id

list_of_faces = []
for file in os.listdir('test'):
    pretty_print(f'\nTesting File: {file}\n')
    for url in open(f'test/{file}').readlines():
        pretty_print(f'URL: {url}', indent=2)
