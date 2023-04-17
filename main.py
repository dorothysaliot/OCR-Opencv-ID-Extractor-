from flet import *
import os
import pytesseract
from PIL import Image as img
import re
import cv2


#to do:
#read pytesseract documentation
#dynamically allocate the section of the characters 
#dynamically fill the age
#enhance filter to detect character
#browse a file




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
        #image prepocess using opencv section
        img = cv2.imread(img_loc.value)
        # img_pro = img.open(img_loc.value)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

        #Use the correct page segmentation mode
        text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')
        # text = pytesseract.image_to_string(gray, lang='eng')
        # text = pytesseract.image_to       _string(img,lang="eng")
        #Use region of interest (ROI) detection


        print(text)

        with open("result.txt", "w") as file:
            file.write(text)

        with open("result.txt", mode="r") as file:
            text = file.read()


        #create sections
        sections ={}
        lines = text.split("\n")
        current_section = ''

        i = 1
       
        for line in lines:
            if line.strip() == "":
                continue
            if "Apelyido" in line:
                current_section = "section_8"
                i += 1
            elif "Mga Pangalan" in line:
                current_section = "section_14"
                i += 1
            elif "Gitnang Apelyido" in line:
                current_section = "section_17"
                i += 1
            elif "Petsa ng Kapanganakan" in line:
                current_section = "section_20"
                i += 1
            elif "Tirahan" in line:
                current_section = "section_23"
                i += 1
            elif len(line.strip()) == 16:
                current_section = "section_8"
                i += 1
            else:
                current_section = f"section_{i}"
            sections[current_section] = line.strip()
            i += 1
        print(sections)

    
            #SET EACH SECTIONS
        id_num.value = sections['section_6']
        last_name.value = sections['section_10']
        first_name.value = sections['section_14']
        middle_name.value = sections['section_17']
        dob.value = sections['section_20']
        address.value = sections['section_23']
        # img_preview.src = f"{os.getcwd()/{img_loc.value}}"

        # page.snack_bar  = Snackbar(
        #     Text("Success get from image ", size=30),
        #     bgcolor="green"
        #     )
        # page.snack_bar.open = True
        page.update()


    page.add(
        Column([
            img_loc,
            ElevatedButton("Process your image",
                       bgcolor="blue",
                       color="white",
                       on_click=processimg),
            # Text("Your Result in Image", weight="bold"),
            # img_preview,
            id_num,
            last_name,
            first_name,
            middle_name,
            dob,
            address
        ])
    )

flet.app(target=main)

