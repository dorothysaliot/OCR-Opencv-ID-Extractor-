from flet import *
import os
import pytesseract
from PIL import Image as img
import re

def main(page:Page):
    page.scroll = "auto"

    img_loc = TextField(label="Image Name")
    id_num = TextField(label="ID Number")
    last_name = TextField(label="Last Name")
    first_name = TextField(label="First Name")
    middle_name = TextField(label="Middle Name")
    dob = TextField(label="Date of Birth")
    address = TextField(label="Address")

    #preview image
    img_preview = Image(src=False,width=150,height=150)

    #function to process img
    def processimg(e):
        img_pro = img.open(img_loc.value)
        text = pytesseract.image_to_string(img_pro,lang="fil")
        print(text)

        with open("result.txt", "w") as file:
            file.write(text)

        with open("result.txt", mode="r", encoding="utf-8") as file:
            file.read(text)


        #create sections
        sections ={}
        lines = text.split("/n")
        current_section = ''

        i = 1
        for line in lines:
            if line.strip() == "":
                continue










    page.add(
        Column([
        img_loc,
        ElevatedButton("Process your image",
                       bgcolor="blue",
                       color="white"),
                    #    on_click=processimg),
        Text("Your Result in Image", weight="bold"),
        img_preview,
        id_num,
        last_name,
        first_name,
        middle_name,
        dob,
        address

        
        ])
    )

flet.app(target=main)