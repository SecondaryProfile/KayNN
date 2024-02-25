from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.graphics.texture import Texture
import cv2
import numpy as np
import platform

class ColorDetectionApp(App):
    def build(self):
        self.title = 'Color Detection App'
        self.selected_image = None

        layout = BoxLayout(orientation='vertical', padding=10)

        file_button = Button(text='Select Image', size_hint=(None, None), size=(150, 50))
        file_button.bind(on_press=self.open_file_chooser)
        layout.add_widget(file_button)

        self.image_preview = Image(allow_stretch=True)
        layout.add_widget(self.image_preview)

        self.rgb_label = Label(text='RGB: ')
        self.hex_label = Label(text='Hex: ')
        layout.add_widget(self.rgb_label)
        layout.add_widget(self.hex_label)

        detect_button = Button(text='Detect Color', size_hint=(None, None), size=(150, 50))
        detect_button.bind(on_press=self.detect_color)
        layout.add_widget(detect_button)

        return layout

    def open_file_chooser(self, instance):
        def on_selection(instance, selection, touch):
            if selection:
                self.selected_image = selection[0]
                self.image_preview.source = self.selected_image
                popup.dismiss()

        content = BoxLayout(orientation='vertical')
        file_chooser = FileChooserListView(path='C:\\Users' if platform.system() == 'Windows' else '/Users/', filters=['*.png', '*.jpg', '*.jpeg', '*.gif'])
        file_chooser.bind(on_submit=on_selection)
        content.add_widget(file_chooser)
        popup = Popup(title='Select Image', content=content, size_hint=(None, None), size=(400, 400))
        popup.open()

    def detect_color(self, instance):
        if self.selected_image:
            image = cv2.imread(self.selected_image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            pixels = image.reshape((-1, 3))
            pixels = np.float32(pixels)

            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            flags = cv2.KMEANS_RANDOM_CENTERS
            _, labels, centers = cv2.kmeans(pixels, 1, None, criteria, 10, flags)

            centers = np.uint8(centers)

            rgb_value = tuple(centers[0])

            self.rgb_label.text = f'RGB: {rgb_value}'
            hex_value = '#{:02x}{:02x}{:02x}'.format(*rgb_value)
            self.hex_label.text = f'Hex: {hex_value}'

            texture = Texture.create(size=(1, 1))
            buffer = np.uint8([[[rgb_value[0], rgb_value[1], rgb_value[2]]]])
            texture.blit_buffer(buffer.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.image_preview.texture = texture

if __name__ == '__main__':
    ColorDetectionApp().run()
