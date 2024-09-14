from PIL import Image

class Floorplan:
    def __init__(self, path):
        self.path = path
        self.image = Image.open(path)
        self.width, self.height = self.image.size

    def get_image(self):
        return self.image

    def get_size(self):
        return self.width, self.height

    def save_image(self, new_path):
        self.image.save(new_path)

    def show_image(self):
        self.image.show()

    def resize_image(self, new_width, new_height):
        # Verwende Image.Resampling.LANCZOS anstelle von Image.ANTIALIAS
        resized_image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return resized_image
