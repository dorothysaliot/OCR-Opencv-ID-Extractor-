from flet import *
import shutil

def main(page:Page):
    location_file = Text("")

    def dialog_picker(e:FilePickerResultEvent):
        for x in e.files:
            shutil.copy(x.name, f"myUploads/{x.name}")
            location_file.value = f"myUploads/{x.name}"
            location_file.update()

    MyPick = FilePicker(on_result=dialog_picker)
    page.overlay.append(MyPick)

    page.add(
        Column([
            ElevatedButton("Insert File", 
                           on_click=lambda _: MyPick.pick_files()),
                           location_file
        ])
    )

flet.app(target = main)