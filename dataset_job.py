import torchvision.transforms as transforms
from torch.utils.data import DataLoader,Dataset
from torch.utils.data import random_split
import h5py
import matplotlib.pyplot as plt
import torch

class IMAGE_DS(Dataset):
    def __init__(self, root):
        self.root = root
        file = h5py.File(root, "r")
        self.images = file['images']
        #self.labels = file['labels']
        self.labels = torch.from_numpy(file['labels'][:])
        self.transform = transforms.Compose([transforms.ToPILImage(), transforms.ToTensor()])
        self.transformed_images = [self.transform(image) for image in self.images]
        self.len = len(self.labels)        

    def __len__(self):
        return self.len

    def __getitem__(self, idx):
        return self.transform(self.images[idx]), self.labels[idx]
    
    def view_image(self, idx):
        plt.imshow(self.images[idx])
        plt.title(self.labels[idx])
        plt.show()
        
    def get_image(self, idx):
        return self.images[idx]
    
    def train_test_split(self, train_size=0.9):
        train_ds, test_ds = random_split(self, [int(train_size*self.len), self.len-int(train_size*self.len)])
        return train_ds, test_ds
    
    def loader(self, batch_size=32):
        train_ds, test_ds = self.train_test_split()
        return DataLoader(train_ds, batch_size=batch_size, shuffle=True), DataLoader(test_ds, batch_size=batch_size, shuffle=False)
    
    
ds=IMAGE_DS('dataset.h5')
train_ds, test_ds = ds.loader()
#print(len(train_ds), len(test_ds), ds[0][0].shape)
# ds.view_image(599)
    