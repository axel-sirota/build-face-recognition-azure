import os
import time

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

person_list = face_client.large_person_group_person.list(large_person_group_id='1')
person_map = {}
for person in person_list:
    person_map[person.person_id] = person.name

for file in os.listdir('test'):
    pretty_print(f'Testing File: {file}')
    for url in open(f'test/{file}').readlines():
        pretty_print(f'URL: {url}', 2)
