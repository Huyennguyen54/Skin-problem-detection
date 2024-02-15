# -*- coding: utf-8 -*-
"""skindetection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vQTV2xZFWoMUgUf_R4DsdDLsmylVDp-3
"""

!pip install openai==0.28
!pip install Pillow matplotlib

!pip install roboflow

from roboflow import Roboflow
from PIL import Image
from google.colab import userdata
import openai
import os
import matplotlib.pyplot as plt

rf = Roboflow(api_key=userdata.get('roboflow_api_key'))
project = rf.workspace().project("skin-problems-detection-jp4jv")
model = project.version(4).model
url = "https://images-as.eucerin.com/~/media/eucerin/local/vn/tan-nhang-la-gi/tan-nhang-la-gi-1.jpg?h=433&w=650&la=vi-vn"
predict_dict =model.predict(url,hosted=True, confidence=40, overlap=30).json()
pre = predict_dict['predictions']
list_issue = set()
for i in range(len(pre)):
  list_issue.add(pre[i]['class'])
list_issue = list(list_issue)
issue_string = ', '.join(map(str,list_issue))
print(issue_string)

import matplotlib.pyplot as plt
model.predict(url, hosted= True, confidence=30, overlap=30).save("prediction.jpg")
img = Image.open('prediction.jpg')
plt.imshow(img)
plt.show()

openai.api_key =userdata.get('OPENAI_API_KEY')

def generate_skin_care(skin_issue):
  content = f"Tell the user that they have {skin_issue}, begin with It looks like you may have... and then give them advice about skincare "
  response =  openai.ChatCompletion.create(
    model="gpt-3.5-turbo-1106",
    messages=[
      {"role": "system", "content": "You are a helpful assistant about skin "},
      {"role": "user", "content": content},
    ]
  )
  advice = response['choices'][0]["message"]["content"]
  return(advice)

if issue_string == {}:
  advice = 'It looks like you have taken good care of your skin. Keep maintaining your regular skincare routine'
else:
  advice = generate_skin_care(issue_string)
print(advice)

