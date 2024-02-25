from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from sklearn.cluster import KMeans
import cv2
import numpy as np
import os

class ColorDetectionApp(App):
    def build(self):
        self.title = 'Color Detection App'
        self.selected_image = None

        layout = BoxLayout(orientation='vertical', padding=10)

        file_chooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg', '*.gif'])
        file_chooser.bind(on_submit=self.on_file_selected)

        self.image_preview = Image(allow_stretch=True)
        layout.add_widget(self.image_preview)

        self.rgb_label = Label(text='RGB: ')
        self.hex_label = Label(text='Hex: ')
        layout.add_widget(self.rgb_label)
        layout.add_widget(self.hex_label)

        detect_button = Button(text='Detect Color', size_hint=(None, None), size=(150, 50))
        detect_button.bind(on_press=self.detect_color)
        layout.add_widget(detect_button)

        layout.add_widget(file_chooser)
        return layout

    def on_file_selected(self, instance, selection, touch):
        self.selected_image = selection[0]
        self.image_preview.source = self.selected_image

    def detect_color(self, instance):
        if self.selected_image:
            image = cv2.imread(self.selected_image)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            height, width = image.shape[:2]
            new_height = int(height * 200 / max(height, width))
            new_width = int(width * 200 / max(height, width))
            image = cv2.resize(image, (new_width, new_height))
            image_flattened = image.reshape((-1, 3))

            kmeans = KMeans(n_clusters=1)
            kmeans.fit(image_flattened)
            dominant_color = kmeans.cluster_centers_[0]

            dominant_color = np.uint8([[[dominant_color[0], dominant_color[1], dominant_color[2]]]])

            rgb_value = tuple(dominant_color[0][0][::-1])

            self.rgb_label.text = f'RGB: {rgb_value}'
            hex_value = '#{:02x}{:02x}{:02x}'.format(*rgb_value)
            self.hex_label.text = f'Hex: {hex_value}'

            texture = Texture.create(size=(1, 1))
            buffer = np.uint8([[[rgb_value[0], rgb_value[1], rgb_value[2]]]])
            texture.blit_buffer(buffer.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.image_preview.texture = texture

if __name__ == '__main__':
    ColorDetectionApp().run()
