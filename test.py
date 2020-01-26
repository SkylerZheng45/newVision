from AzureVisionLocal import detect_image
from PIL import Image
import io
from io import BytesIO


# im = Image.open('goose.jpg')
# buf = io.BytesIO()
# im.save(buf, format='JPEG')
# byte_im = buf.getvalue()
# file_like = BytesIO(byte_im)

import cv2

im = cv2.imread('goose.jpg')
im_resize = cv2.resize(im, (500, 500))

is_success, im_buf_arr = cv2.imencode(".jpg", im_resize)
byte_im = im_buf_arr.tobytes()
file_like = BytesIO(byte_im)

import cv2

# img = Image.open('goose.jpg', mode='r')
# imgByteArr = io.BytesIO()
# img.save(imgByteArr, format='JPEG')
# imgByteArr = imgByteArr.getvalue().encode('iso-8859-1')
# file_like = BytesIO(imgByteArr)


detect_image(file_like)