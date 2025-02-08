import glob
from PIL import Image, ExifTags, ImageEnhance
import numpy as np

# Sources and settings
main_photo_names = ["Choix2.jpeg"]
tile_photos_path = "Tiles\\*"
tile_size = (66, 66)
tile_alpha = 120
photo_alpha = 160
increase_factor = 1.94 #size
contrast_factor = 1.1 #contrast
brightness_factor = 0.9 #brightness
brightness_factor_more_tiles = 1.25 #brightens the tile
brightness_factor_less_tiles = 0.75 #darkens the tile

# Get all tiles
tile_paths = []
for file in glob.glob(tile_photos_path):
    tile_paths.append(file)

# Import and resize all tiles
tiles = []
for path in tile_paths:
    tile = Image.open(path)
    tile.putalpha(tile_alpha)
    try:
        # Find the orientation based on orientation in folder
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break

        exif = tile._getexif()
        if exif[orientation] == 3:
            tile=tile.rotate(180, expand=True)
        elif exif[orientation] == 6:
            tile=tile.rotate(270, expand=True)
        elif exif[orientation] == 8:
            tile=tile.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError, TypeError):
        # cases: image don't have getexif
        pass

    width, height = tile.size   # Get dimensions
    if width > height:
        left = (width - height)/2
        top = 0
        right = (width + height)/2
        bottom = height
    else:
        left = 0
        top = (height - width)/2
        right = width
        bottom = (height + width)/2

    # Crop the center of the image
    tile = tile.crop((left, top, right, bottom))
    tile = tile.resize(tile_size)
    tiles.append(tile)

    #Add darker and brighter tiles
    # enhancer = ImageEnhance.Brightness(tile)
    # brighter_tile = enhancer.enhance(brightness_factor_more_tiles)
    # tiles.append(brighter_tile)
    # enhancer = ImageEnhance.Brightness(tile)
    # darker_tile = enhancer.enhance(brightness_factor_less_tiles)
    # tiles.append(darker_tile)

print("Tiles generated!")

# Calculate dominant color
colors = []
for tile in tiles:
    mean_color = np.array(tile).mean(axis=0).mean(axis=0)
    colors.append(mean_color)

# Rotate and resize photo

for main_photo_name in main_photo_names:
    
    main_photo_path = f'Input/{main_photo_name}'
    photo_name = main_photo_name.split('.')[0]
    output_name = f'Mosaiques/{photo_name}_mosa'
    output_contrast_name =f'Mosaiques/{photo_name}_mosa_more_contrast'

    main_photo = Image.open(main_photo_path)

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation]=='Orientation':
            break

    exif = main_photo._getexif()
    if exif:
        if exif[orientation] == 3:
            main_photo=main_photo.rotate(180, expand=True)
        elif exif[orientation] == 6:
            main_photo=main_photo.rotate(270, expand=True)
        elif exif[orientation] == 8:
            main_photo=main_photo.rotate(90, expand=True)

    output = main_photo.resize((int(main_photo.size[0]*increase_factor), int(main_photo.size[1]*increase_factor)))

    # Pixelate (resize) main photo
    width = int(np.round(output.size[0] / tile_size[0]))
    height = int(np.round(output.size[1] / tile_size[1]))

    resized_photo = output.resize((width, height))

    # Empty integer array to store indices of tiles
    closest_tiles = np.zeros((width, height), dtype=np.uint32)

    for i in range(width):
        for j in range(height):
            pixel = resized_photo.getpixel((i, j))  # Getthe pixel color at (i, j)
            distances = [sum([(a_i - b_i)**2 for a_i, b_i in zip(pixel, col)]) for col in colors]
            closest = min(range(len(distances)), key=distances.__getitem__) #index of the closest picture
            closest_tiles[i, j] = closest        # We only need the index

    # Create an output image
    #output = Image.new('RGB', main_photo.size)
    #output = main_photo.copy()
    output.putalpha(photo_alpha)

    # Draw tiles
    for i in range(width):
        for j in range(height):
            # Offset of tile
            x, y = i*tile_size[0], j*tile_size[1]
            # Index of tile
            index = closest_tiles[i, j]
            # Draw tile
            #output.paste(tiles[index], (x, y))
            #new_tile = tiles[index].copy()
            output.alpha_composite(tiles[index], (x, y))

    # Save output
    output.putalpha(255)
    output.save(f'{output_name}.png')
    # (output.convert('RGB')).save(f'{output_name}.jpeg')
    enhancer = ImageEnhance.Brightness(output)
    output = enhancer.enhance(brightness_factor)
    enhancer = ImageEnhance.Contrast(output)
    output = enhancer.enhance(contrast_factor)
    output.save(f'{output_contrast_name}.png')
    # (output.convert('RGB')).save(f'{output_contrast_name}.jpeg')
    print(f'Photo {photo_name} générée !')