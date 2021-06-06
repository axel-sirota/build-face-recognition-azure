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
        faces_to_check = [face.face_id for face in face_client.face.detect_with_url(url=url,
                                                                                    detection_model='detection_03',
                                                                                    recognition_model='recognition_04')]
        pretty_print(f'Faces in this Image: {faces_to_check}', indent=2)
        list_of_faces.extend(faces_to_check)
        similar_faces = face_client.face.find_similar(face_id=person1_face_id,
                                                      face_ids=faces_to_check,
                                                      mode='matchPerson')
        if not similar_faces:
            pretty_print('No similar faces to Person1 Face found in this Image', indent=2)
        for similar_face in similar_faces:
            pretty_print(similar_face, indent=8)

response = face_client.face.group(face_ids=list_of_faces)
print(f'Groups found: {response.groups}')
