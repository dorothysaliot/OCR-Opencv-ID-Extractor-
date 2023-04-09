from flet import *
import os
import pytesseract
from PIL import Image as img
import re
from PIL import ImageEnhance

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
        enhancer = ImageEnhance.Contrast(img_pro)
        image = enhancer.enhance(2)
        text = pytesseract.image_to_string(image,lang="eng")
        
        print(text)

        with open("result.txt", "w") as file:
            file.write(text)

        with open("result.txt", mode="r") as file:
            text = file.read()


        #create sections
        sections ={}
        lines = text.split("/n")
        current_section = ''

        i = 1
        for line in lines:
            if line.strip() == "":
                continue
            if "Apelyido" in line:
                current_section = "section_3"
                i += 1
            elif "Mga Pangalan" in line:
                current_section = "section_4"
                i += 1
            elif "Gitnang Apelyido" in line:
                current_section = "section_5"
                i += 1
            elif "Petsa ng Kapanganakan" in line:
                current_section = "section_6"
                i += 1
            elif "Tirahan" in line:
                current_section = "section_7"
                i += 1
            elif len(line.strip() == 16 and line.strip().isdigit()):
                current_section = "section_2"
                i += 1
            else:
                current_section = f"section_{i}"
            sections[current_section] = line.strip()
            i += 1
        print(sections)

    
            #SET EACH SECTIONS
        id_num.value = sections['section_1']
        last_name.value = sections['section_2']
        first_name.value = sections['section_3']
        middle_name.value = sections['section_4']
        dob.value = sections['section_5']
        address.value = sections['section_6']
        img_preview.src = f"{os.getcwd()/{img_loc.value}}"

        page.snack_bar  = Snackbar(
                Text("Success get from image ", size=30),
                bgcolor="green"
            )
        page.snack_bar.open = True
        page.update()


    page.add(
        Column([
        img_loc,
        ElevatedButton("Process your image",
                       bgcolor="blue",
                       color="white",
                       on_click=processimg),
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