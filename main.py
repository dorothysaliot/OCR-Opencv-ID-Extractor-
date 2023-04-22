from flet import *
import os
import pytesseract
from PIL import Image as img
import re
import cv2
import shutil


#main function
def main(page:Page):
    page.scroll = "auto"

    #text fields
    id_num = TextField(label="ID Number")
    last_name = TextField(label="Last Name")
    first_name = TextField(label="First Name")
    middle_name = TextField(label="Middle Name")
    dob = TextField(label="Date of Birth")
    address = TextField(label="Address")

  
    #function for file picker
    location_file = Text("")

    def dialog_picker(e:FilePickerResultEvent):
        for x in e.files:
            shutil.copy(x.name, f"myUploads/{x.name}")
            location_file.value = f"myUploads/{x.name}"
            location_file.update()
    
    MyPick = FilePicker(on_result=dialog_picker)
    page.overlay.append(MyPick)


    #function to process image
    def processimg(e):
        file = str(location_file.value)
        #pre process image using opencv
        img = cv2.imread(file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
        #image to text using pytesseract 
        #Use the correct page segmentation mode 
        text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')

        print(text)

        #write the file from extracted data
        with open("result.txt", "w") as file:
            file.write(text)

        with open("result.txt", mode="r") as file:
            text = file.read()


        #create sections to identify region of interest
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

    
        
        id_num.value = sections['section_6']
        last_name.value = sections['section_10']
        first_name.value = sections['section_14']
        middle_name.value = sections['section_17']
        dob.value = sections['section_20']
        address.value = sections['section_23']
       
        page.update()


    #add the graphical user interface to the page
    page.add(
        Column([
           
            ElevatedButton("Choose File", 
                           on_click=lambda _: MyPick.pick_files()),
            ElevatedButton("Process your image",
                       bgcolor="blue",
                       color="white",
                       on_click=processimg),
            location_file,
            id_num,
            last_name,
            first_name,
            middle_name,
            dob,
            address
        ])
    )

flet.app(target=main)

