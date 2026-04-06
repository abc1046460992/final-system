import urllib.request
from PIL import Image
import io

url = "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6b/WhatsApp.svg/512px-WhatsApp.svg.png"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    img_data = response.read()

img = Image.open(io.BytesIO(img_data))
img.save("whatsapp.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32)])
print("Icon downloaded and converted to whatsapp.ico successfully.")
