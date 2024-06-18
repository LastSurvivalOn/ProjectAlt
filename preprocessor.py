from PIL import Image
import os
import datetime
import h5py
import numpy as np
import cv2

class Preprocessor:
    def __init__(self, folder_name='data\\true', new_folder_name='resized_images\\true', size=(256, 256)):
        self.folder_name = folder_name
        self.new_folder_name = new_folder_name
        self.size = size
        self.images = os.listdir(self.folder_name)
        self.resized_images = []
        
    def resize_image(self, image):
        img = Image.open(os.path.join(self.folder_name, image))
        img = img.resize(self.size)
        img.save(os.path.join(self.new_folder_name, image))
        
    def resize_cycle(self):
        for image in self.images:
            try:
                self.resize_image(image)
                self.resized_images.append(image)
                print(f"Resized {len(self.resized_images)}/{len(self.images)} images")
            except:
                print(f"Error with resizing {image}")
        return len(self.resized_images)
    
    def full_cycle(self):
        if not os.path.exists(self.new_folder_name):
            os.makedirs(self.new_folder_name)
        print(f"Resized {self.resize_cycle()} images")
        
    def rename_images(self, name):
        current_time = datetime.datetime.now()
        files=os.listdir(self.new_folder_name)
        ch = current_time.hour
        cm = current_time.minute
        cs = current_time.second
        for i, image in enumerate(files):
            try:
                    os.rename(os.path.join(self.new_folder_name, image), os.path.join(self.new_folder_name, f"{ch}{cm}{cs}_{name}"+str(i)+".jpg"))
            except:
                print(f"Error with renaming {image}")
        print(f"Renamed {len(files)} images")
        
    def create_bin_dataset(self, true_folder="data\\true", false_folder="data\\false", dataset_name="dataset", RGB=True):
        true_images = [os.path.join(true_folder, img) for img in os.listdir(true_folder)]
        false_images = [os.path.join(false_folder, img) for img in os.listdir(false_folder)]
        num_timages = len(true_images)
        num_fimages = len(false_images)
        num_images = num_timages + num_fimages
        labels_array = np.zeros((num_images, 1), dtype=np.uint8)
        labels_array[:num_timages] = 1
        
        images = np.zeros((num_images, 256, 256, 3), dtype=np.uint8)

        for i in range(num_timages):
            img = cv2.imread(true_images[i])
            if RGB: img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            images[i] = img
        
        for i in range(num_fimages):
            img = cv2.imread(false_images[i])
            if RGB: img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            images[num_timages+i] = img
        
        file = h5py.File(f"{dataset_name}.h5", "w")

        imset=file.create_dataset(
            "images", np.shape(images), h5py.h5t.STD_U8BE, data=images
        )
        lset=file.create_dataset(
            "labels", np.shape(labels_array), h5py.h5t.STD_U8BE, data=labels_array
        )
        
        file.close()
        return imset, lset
        

preprocessor=Preprocessor(folder_name="data\\ManualHandling\\false", new_folder_name="resized_images\\false")
# preprocessor.full_cycle()
# preprocessor.rename_images('false_images')
preprocessor.create_bin_dataset(true_folder="resized_images\\true", false_folder="resized_images\\false")
