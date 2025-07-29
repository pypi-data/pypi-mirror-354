import os
import msgpack
import pygame as pg
from io import BytesIO

class AssetManager:
    def __init__(self, game):
        self.game = game
        self.root = os.path.join(self.game.build_dir, "assets.aab")
        self.scene_assets = {}

        self.load_aab_file()

    @property
    def selected_scene(self):
        return self.game.scene_manager.selected_scene or "all-scenes"

    def load_aab_file(self):
        if os.path.exists(self.root):
            try:
                with open(self.root, "rb") as file:
                    self.scene_assets = msgpack.unpackb(file.read())
            except Exception:
                self.scene_assets = {}  # Reset assets if file is corrupt
        else:
            self.scene_assets = {}
            with open(self.root, "wb") as file:
                file.write(msgpack.packb({}))

    def _surface_to_png_bytes(self, surface):
        buffer = BytesIO()
        pg.image.save(surface, buffer, "PNG")
        return buffer.getvalue()

    def save_image(self, scene_name, path, image: pg.Surface):
        image_data = {
            "size": image.get_size(),
            "raw-data": self._surface_to_png_bytes(image)
        }

        # Load existing assets
        if os.path.exists(self.root):
            with open(self.root, "rb") as file:
                assets = msgpack.unpackb(file.read())
        else:
            assets = {}

        # Ensure the scene exists in assets
        if scene_name not in assets:
            assets[scene_name] = {}

        # Save the image data under the correct scene key
        assets[scene_name][path] = image_data

        # Write updated assets back to the file
        with open(self.root, "wb") as file:
            file.write(msgpack.packb(assets, use_bin_type=True))


    def load_image(self, scene_name, path):
        with open(self.root, "rb") as file:
            assets = msgpack.unpackb(file.read())

        if scene_name in assets and path in assets[scene_name]:
            image_data = assets[scene_name][path]
            return pg.image.load(BytesIO(image_data["raw-data"]))
        return None

    def get_image(self, scene_name, path):
        if not self.scene_assets.get(self.selected_scene):
            self.scene_assets[self.selected_scene] = {}

        # First, check if the asset exists in `.aab`
        image = self.load_image(scene_name, path)
        if image:
            self.scene_assets[self.selected_scene][path] = image
            return image

        # If not in `.aab`, check disk and save the asset immediately
        if os.path.exists(path):
            image = pg.image.load(path)

            # Ensure it's saved to `.aab` before returning
            self.save_image(self.selected_scene, path, image)

            # Also store it in `scene_assets`
            self.scene_assets[self.selected_scene][path] = image
            return image

        raise FileNotFoundError(f"Image not found: {path} in scene {scene_name}")
