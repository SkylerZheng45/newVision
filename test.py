from AzureVisionLocal import detect_image
from PIL import Image
import io


im = Image.open('goose.jpg')
buf = io.BytesIO()
im.save(buf, format='JPEG')
byte_im = buf.getvalue()


detect_image(byte_im)