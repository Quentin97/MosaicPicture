# MosaicPicture (Photo Mosaic Generator)

This Python script replaces an image with thousands of small images (tiles) by matching their average RGB values. The result is a mosaic effect where the original photo is reconstructed using smaller pictures.

## Features
- Automatically extracts and processes tiles from a folder.
- Matches each tile to the most similar region of the main image using color averaging.
- Supports image enhancement options (brightness, contrast adjustments).
- Handles image rotation based on EXIF data.

## Installation
### Prerequisites
Ensure you have Python installed (>=3.7). Then, install the required dependencies:

```sh
pip install pillow numpy
```

## Usage
1. Place your main image inside the `Input/` folder.
2. Place your tile images inside the `Tiles/` folder.
3. Run the script:

```sh
python photo_mosaic.py
```

### Configuration
You can modify the following parameters inside the script:
- `main_photo_names`: List of images to process.
- `tile_size`: The dimensions of each tile.
- `increase_factor`: Scale factor for the output image.
- `brightness_factor`, `contrast_factor`: Adjust the final image appearance.

## Output
- The generated mosaic images are saved in the `Mosaiques/` folder with names like `original_mosa.png` and `original_mosa_more_contrast.png`.

## Example
### Input Image:
*(original photo to be transformed)*

### Output Mosaic:
*(mosaic image composed of tiles)*

## License
This project is released under the GNU General Public License v3.0 (GPLv3) with a Non-Commercial Clause. The game code can be modified and shared, but it may not be used for commercial purposes without explicit written permission from the authors.

## Author
Quentin Gontier

