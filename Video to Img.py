import cv2
import os
import random

dataset_path = "/Users/jingwenshi/Desktop/Dataset/"

# Create Train, Test, and Valid folders with subfolders
folders = ['Train', 'Test', 'Valid']
subfolders = ['12%', '37%', '62%', '87%']

for folder in folders:
    for subfolder in subfolders:
        os.makedirs(os.path.join(folder, subfolder), exist_ok=True)

# Loop through all files in the directory
for video in os.listdir(dataset_path):
    # Check if the file has a .MOV extension
    if video.endswith(".MOV"):
        path = os.path.join(dataset_path, video)
        cam = cv2.VideoCapture(path)

        video_name = video[:-4]

        try:
            if not os.path.exists("temp_data"):
                os.makedirs("temp_data")
        except OSError:
            print('Error: Creating directory of data')

        currentframe = 0
        images = []

        while True:
            ret, frame = cam.read()

            if ret:
                if currentframe % 15 == 0:
                    name = f'./temp_data/{video_name}_' + str(currentframe) + '_' + video_name[-3:] + '.jpg'
                    print('Creating...' + name)
                    cv2.imwrite(name, frame)
                    images.append(name)
                currentframe += 1

            else:
                break

        cam.release()

        # Shuffle the images and assign them to Train, Test, and Valid folders
        random.shuffle(images)
        num_images = len(images)
        test_images = images[:num_images // 5]
        valid_images = images[num_images // 5:2 * num_images // 5]
        train_images = images[2 * num_images // 5:]

        for img_path in train_images + test_images + valid_images:
            img_name = os.path.basename(img_path)
            folder = "Train" if img_path in train_images else "Test" if img_path in test_images else "Valid"
            subfolder = img_name.split('_')[2][:3]  # Extract the percentage from the image name
            print(subfolder)
            dest_path = os.path.join(folder, subfolder, img_name)
            os.rename(img_path, dest_path)

# Remove the temp_data folder
os.rmdir("temp_data")
