import numpy as np
from skimage.transform import resize
from skimage import measure
from skimage.measure import regionprops
from skimage.io import imsave
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import cca
import os

# Create directories for saving
os.makedirs("detected_characters", exist_ok=True)
os.makedirs("resized_characters", exist_ok=True)

license_plate = np.invert(cca.plate_like_objects[2])

labelled_plate = measure.label(license_plate)

fig, ax1 = plt.subplots(1, figsize=(12, 6))
ax1.imshow(license_plate, cmap="gray")

character_dimensions = (0.35 * license_plate.shape[0], 0.60 * license_plate.shape[0], 0.05 * license_plate.shape[1],
                        0.15 * license_plate.shape[1])
min_height, max_height, min_width, max_width = character_dimensions

characters = []
counter = 0
column_list = []
character_count = 0

for region in regionprops(labelled_plate):
    y0, x0, y1, x1 = region.bbox
    region_height = y1 - y0
    region_width = x1 - x0

    if region_height > min_height and region_height < max_height and region_width < max_width and region_width > min_width:
        character_count += 1
        ROI = license_plate[y0:y1, x0:x1]

        rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red", linewidth=3, fill=False)
        ax1.add_patch(rect_border)

        resize_char = resize(ROI, (20, 20))
        characters.append(resize_char)

        # Save the original cropped character
        imsave(f"detected_characters/character_{character_count}.png", ROI)

        # Save the resized character (20x20)
        imsave(f"resized_characters/resized_char_{character_count}.png", resize_char)

        print(f"  - Character {character_count}: saved original + resized (20x20)")

        column_list.append(x0)

# Add title
ax1.set_title(f"Detected {character_count} characters on license plate")

# Save the main image
plt.savefig("license_plate_characters.png", dpi=300, bbox_inches='tight')
print(f"\n✅ Image saved as license_plate_characters.png")
print(f"✅ Found {character_count} characters")
print(f"✅ Original characters saved in 'detected_characters' folder")
print(f"✅ Resized characters (20x20) saved in 'resized_characters' folder")
plt.close()