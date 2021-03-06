import streamlit as st
import requests
import io
from PIL import ImageFont, ImageDraw, Image
import json

st.title('顔認証アプリ')


with open('secrets.json') as f:
    secret_json = json.load(f)
subscription_key = secret_json['SUBSCRIPTION_KEY']
assert subscription_key
face_api_url = 'https://1026streamlit.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue()
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes':'age,gender',
    }

    res = requests.post(face_api_url, params=params,
                         headers=headers, data=binary_img)
    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        age_data = result['faceAttributes']
        draw = ImageDraw.Draw(img)
        name = str(age_data['gender'])+str(int(age_data['age']))
        font_size = max(16, int(rect['width'] / len(name)))
        font = ImageFont.truetype("arial.ttf", font_size)
        draw.text((rect['left'],rect['top']-font_size), name, fill='green', font=font)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill =None,width = 5,outline ='green')
    st.image(img, caption='Uploaded Image.',use_column_width=True)
