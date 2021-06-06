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
        faces_detected = face_client.face.detect_with_url(url=url, detection_model='detection_03')
        for face in faces_detected:
            face_id = face.person1_face_id
            response = face_client.face.identify(face_ids=[face_id], large_person_group_id='1')
            person_id_recognized = response[0].candidates[0].person_id if len(response[0].candidates) > 0 else None
            if person_id_recognized:
                pretty_print(f'Person: {person_map[person_id_recognized]} was recognized', 4)

