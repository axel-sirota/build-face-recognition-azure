from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from pprint import pprint

import os


# Do not worry about this function, it is for pretty printing the attributes!
def pretty_print(klass, indent=0):
    print(' ' * indent + type(klass).__name__ + ':')
    indent += 4
    for k, v in klass.__dict__.items():
        if '__dict__' in dir(v):
            pretty_print(v, indent)
        elif isinstance(v, list):
            for item in v:
                pretty_print(item, indent)
        else:
            print(' ' * indent + k + ': ' + str(v))


# Authenticate

subscription_key = os.environ["AZURE_COMPUTER_VISION_SUBSCRIPTION_KEY"]
endpoint = os.environ["AZURE_COMPUTER_VISION_ENDPOINT"]

face_client = FaceClient(endpoint, CognitiveServicesCredentials(subscription_key))

single_face_image_url = 'https://image.shutterstock.com/image-photo/attractive-aged-businesswoman-teacher-mentor-600w-1043108527.jpg'

detected_faces = face_client.face.detect_with_url(url=single_face_image_url, return_face_landmarks=True,
                                                  return_face_attributes=['Age', 'Gender', 'HeadPose', 'Emotion',
                                                                          'Glasses', 'Hair'])
print('Detected faces from image:')
for face in detected_faces:
    print(f'Face ID: {face.face_id}\n')
    print(f'Face Rectangle: {face.face_rectangle}\n')
    print(f'Face Attributes: {pretty_print(face.face_attributes)}\n')
    print(f'Face Landmarks: {pretty_print(face.face_landmarks)}\n')
    print('\n')
