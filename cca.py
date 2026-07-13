from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import localization

# get all the connected regions and groups them together
label_img = measure.label(localization.binary_car_image)

# get max and min height, width that a license plate can be
dimensions = (0.08 * label_img.shape[0], 0.2 * label_img.shape[0], 0.15 * label_img.shape[1], 0.4 * label_img.shape[1])
min_height, max_height, min_width, max_width = dimensions
plate_objects_cordinates = []
plate_like_objects = []
fig, (ax1) = plt.subplots(1, figsize=(12, 10))
ax1.imshow(localization.gray_car_image, cmap="gray")

# regionprops creates a list of properties of all the labelled regions
plate_count = 0
for region in regionprops(label_img):
    if region.area < 50:
        # if region is so small its likely not a license plate
        continue

    # bounding box coordinates

    min_row, min_col, max_row, max_col = region.bbox
    region_height = max_row - min_row
    region_width = max_col - min_col

    # ensuring region identified satisfies the condition of a standard license plate
    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
        plate_count += 1
        plate_like_objects.append(localization.binary_car_image[min_row:max_row,
                                  min_col:max_col])
        plate_objects_cordinates.append((min_row, min_col,
                                              max_row, max_col))
        rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=3, fill=False)
        ax1.add_patch(rectBorder)
        # draw bounding box

ax1.set_title(f"{plate_count} potential license plate regions")

# Save the image instead of showing it
plt.savefig("license_plate_detection.png", dpi=300, bbox_inches='tight')
print(f"✅ Image saved as license_plate_detection.png")
print(f"✅ Found {plate_count} potential license plate regions")
plt.close()