from skimage import measure
from skimage.measure import regionprops
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import localization

#Get all connected regions and group them

label_image = measure.label(localization.binary_car_image)
fig, (ax1) = plt.subplots(1, figsize=(10, 8))
ax1.imshow(localization.gray_car_image, cmap="gray")

#regionprops creates a list of props. of all the labeled regions
plate_count = 0
for region in regionprops(label_image):
    if region.area < 50:

        #if region is below 50 (small), likely not a license plate
        continue

    # bounding box coordinates :-)
    minRow, minCol, maxRow, maxCol = region.bbox
    rectBorder = patches.Rectangle(
        (minCol, minRow),
        maxCol - minCol,
        maxRow - minRow,
        edgecolor="red",
        linewidth=2,
        fill=False
    )
    ax1.add_patch(rectBorder)
    plate_count += 1
    # draww a red rectangle over regions

ax1.set_title(f"{plate_count} potential license plate regions")

# Save the image instead of showing it
plt.savefig("license_plate_detection.png", dpi=300, bbox_inches='tight')
print(f"Image saved as license_plate_detection.png")
print(f"{plate_count} potential license plate regions")

plt.close()