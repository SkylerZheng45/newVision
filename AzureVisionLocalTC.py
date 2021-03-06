from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import json
import cv2
from array import array
import os
from PIL import Image
import sys
import time



import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('thirdeye-c428c-firebase-adminsdk-nkzeg-5fdfaed1e1.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://thirdeye-c428c.firebaseio.com/'
})


ref = db.reference('/')




computervision_client=None
def auth_azure():
    # <snippet_vars>
    # Add your Computer Vision subscription key to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()
    # Add your Computer Vision endpoint to your environment variables.
    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
    else:
        print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()
    # </snippet_vars>

    # <snippet_client>
    global computervision_client
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

def update_distance(om_result):
    db.reference('user/').update({
        "distance": om_result[1],
        "label": om_result[0]
    })

def send_description(local_image_path):
    local_image = open(local_image_path, "rb")

    # Call API
    is_API_ok=False
    description_result=None
    while not is_API_ok:
        is_API_ok=True
        try:
            description_result = computervision_client.describe_image_in_stream(local_image)
        except:
            print('Description API Failed. Retrying ...')
            time.sleep(1)
            auth_azure()
            is_API_ok=False

    # Get the captions (descriptions) from the response, with confidence level
    #print("Description of local image: ")

    if db.reference('/user/request').get():
        print("got request")
        if (len(description_result.captions) == 0):
            print("No description detected.")
        else:
            for caption in description_result.captions:
                #print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
                db.reference('user/').update({
                    "description": caption.text
                })
                print(caption.text)
                break
        db.reference('user/').update({
            "request":False,
        })

# def send_description(local_image_path):
#     local_image = open(local_image_path, "rb")
#
#     # Call API
#     description_result = computervision_client.describe_image_in_stream(local_image)
#
#     # Get the captions (descriptions) from the response, with confidence level
#     #print("Description of local image: ")
#
#     while(True):
#         time.sleep(0.5)
#         if db.reference('/user/request').get():
#             print("got request")
#             if (len(description_result.captions) == 0):
#                 print("No description detected.")
#             else:
#                 for caption in description_result.captions:
#                     #print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
#                     db.reference('user/').update({
#                         "description": caption.text
#                     })
#                     break
#             db.reference('user/').update({
#                 "request":False,
#             })
#     print()
    '''
    END - Describe an Image - local
    '''


def detect_image(local_image_path):
    list_for_camera = []
    '''
    Describe an Image - local
    This example describes the contents of an image with the confidence score.
    '''
    #print("===== Describe an Image - local =====")
    # Open local image file
    #local_image = open(local_image_path, "rb")
    #
    # # Call API
    #description_result = computervision_client.describe_image_in_stream(local_image)
    #
    # # Get the captions (descriptions) from the response, with confidence level
    # #print("Description of local image: ")
    #
    # if (len(description_result.captions) == 0):
    #     print("No description detected.")
    # else:
    #     for caption in description_result.captions:
    #         #print("'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100))
    #         db.reference('user/').update({
    #             "description": caption.text,
    #         })
    #         break
    # print()
    #
    #
    # '''
    # END - Describe an Image - local
    # '''

    '''
    Detect Objects - local
    This example detects different kinds of objects with bounding boxes in a local image.
    '''
    #print("===== Detect Objects - local =====")
    # Get local image with different objects in it
    local_image_path_objects = local_image_path
    local_image_objects = open(local_image_path_objects, "rb")
    # Call API with local image
    is_API_ok=False
    detect_objects_results_local=None
    while not is_API_ok:
        is_API_ok=True
        try:
            detect_objects_results_local = computervision_client.detect_objects_in_stream(local_image_objects)
        except:
            print('Detection API Failed. Retrying ...')
            time.sleep(1)
            auth_azure()
            is_API_ok=False

    # Print results of detection with bounding boxes
    #print("Detecting objects in local image:")
    if len(detect_objects_results_local.objects) == 0:
        print("No objects detected.")
    else:
        for object in detect_objects_results_local.objects:
            #print("object at location {}, {}, {}, {}".format( \
                # object.rectangle.x, object.rectangle.x + object.rectangle.w, \
                # object.rectangle.y, object.rectangle.y + object.rectangle.h))
            temp_list = []
            temp_list.append(object.rectangle.x)
            temp_list.append(object.rectangle.y)
            temp_list.append(object.rectangle.w)
            temp_list.append(object.rectangle.h)
            list_for_camera.append([temp_list,object.object_property])
            # list_for_camera.append(temp_list)
            # list_for_camera.append(object.object_property)
    #print()
    '''
    END - Detect Objects - local
    '''
    # '''
    # Tag an Image - local
    # This example returns a tag (key word) for each thing in the image.
    # '''
    # print("===== Tag an Image - local =====")
    # # Open local image file
    # local_image = open(local_image_path, "rb")
    # # Call API local image
    # tags_result_local = computervision_client.tag_image_in_stream(local_image)
    #
    # # Print results with confidence score
    # print("Tags in the local image: ")
    # if (len(tags_result_local.tags) == 0):
    #     print("No tags detected.")
    # else:
    #     for tag in tags_result_local.tags:
    #         print("'{}' with confidence {:.2f}%".format(tag.name, tag.confidence * 100))
    # print()
    # '''
    # END - Tag an Image - local
    # '''

    return list_for_camera

auth_azure()


# local_image_path = "dog-and-cat-cover.jpg"
# print(detect_image(local_image_path))
# send_description(local_image_path)
