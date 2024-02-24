import PySimpleGUI as sg
import numpy as np
from PIL import Image, ImageTk
from sklearn.cluster import KMeans
import sys
import time

start_time = time.time() * 1000

def load_image(filename):
    return Image.open(filename)

def process_image(image):
    image_array = np.array(image)

    flattened_image = image_array.reshape((-1, 3))

    kmeans = KMeans(n_clusters=1, random_state=42).fit(flattened_image)
    centroid_color = kmeans.cluster_centers_.astype(int)[0]

    processed_image_array = np.full_like(flattened_image, centroid_color)
    
    processed_image = processed_image_array.reshape(image_array.shape)

    return Image.fromarray(processed_image), centroid_color

def main():
    sg.theme('LightGrey1')

    # Splash screen #
    #---------------#
    splash_layout = [
        [sg.Image(filename='logo.png', key="-LOAD-")],
        [sg.Text("by Third", font=('Trebuchet', 12))],
        [sg.Text("Version 1.0", font=('Trebuchet', 12))],
        [sg.Button("OK")]
    ]

    splash_window = sg.Window("KayNN loading...", splash_layout, finalize=True, margins=(5, 5))

    splash_event, _ = splash_window.read(timeout=5000)

    if splash_event == "OK" or splash_event == sg.WINDOW_CLOSED or (time.time() * 1000 - start_time) > 5000:
        splash_window.close()

    menu_def = [['Theme', ['LightGrey1', 'SystemDefault', 'DarkAmber', 'DarkGreen', 'DarkBlue', 'Black']],
                ['Help', 'About...']]

    layout = [
        [sg.Menu(menu_def, tearoff=True)],
        [sg.Text("Select an image to process:")],
        [sg.Input(key="-FILE-", enable_events=True, visible=False), sg.FileBrowse()],
        [sg.Image(key="-IMAGE-")],
        [sg.Text("Processed Color: ")],
        [sg.Text("RGB Value:", size=(10, 1)), sg.Text("    ", key="-RGB-")],
        [sg.Text("HEX Value:", size=(10, 1)), sg.Text("    ", key="-HEX-")],
        [sg.Button("Process"), sg.Button("Save Result", disabled=True), sg.Button("Change Theme")]
    ]

    window = sg.Window("KayNN", layout, resizable=True)

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event == "-FILE-":
            filename = values["-FILE-"]
            if filename:
                image = load_image(filename)
                window["-IMAGE-"].update(data=ImageTk.PhotoImage(image))
                window["Save Result"].update(disabled=False)
        elif event == "Process":
            if values["-FILE-"]:
                processed_image, color = process_image(load_image(values["-FILE-"]))
                window["-IMAGE-"].update(data=ImageTk.PhotoImage(processed_image))
                window["-RGB-"].update(f"({color[0]}, {color[1]}, {color[2]})")
                window["-HEX-"].update(f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}")
        elif event == "Save Result":
            if values["-FILE-"]:
                save_filename = sg.popup_get_file("Save processed image as:", save_as=True,
                                                   file_types=(("PNG files", "*.png"), ("JPEG files", "*.jpg")))
                if save_filename:
                    process_image(load_image(values["-FILE-"]))[0].save(save_filename)
        elif event == "Change Theme":
            selected_theme = sg.popup_get_text("Enter the theme name:")
            if selected_theme:
                sg.theme(selected_theme)

                sg.popup("Theme changed successfully! Please restart the program to apply the changes.")
                sys.exit()

    window.close()

if __name__ == "__main__":
    main()
