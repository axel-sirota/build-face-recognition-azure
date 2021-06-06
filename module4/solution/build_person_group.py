import os
import time

from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import TrainingStatusType
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

face_client.large_person_group.create(large_person_group_id='1', name='businesspeople')
for person_file in os.listdir("faces"):
    person_name = person_file.split(".")[0]
    person = face_client.large_person_group_person.create(large_person_group_id='1', name=person_name)
    for image_url in open(f"faces/{person_file}", 'r').readlines():
        face_client.large_person_group_person.add_face_from_url(large_person_group_id='1',
                                                                person_id=person.person_id,
                                                                url=image_url)
for person in face_client.large_person_group_person.list(large_person_group_id='1'):
    pretty_print(person)

face_client.large_person_group.train(large_person_group_id='1')
for i in range(10):
    response = face_client.large_person_group.get_training_status(large_person_group_id='1')
    if response.status != TrainingStatusType.succeeded:
        time.sleep(5)
    else:
        print('Training Succeeded')
        break

print('Done')

# face_client.large_person_group.delete(large_person_group_id='1')
