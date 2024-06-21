from dataset_job import test_ds
import classificator_ALT
from torch import nn
from torch import optim
import torch
import torchvision
import matplotlib.pyplot as plt
import numpy as np
import torchvision.transforms as transforms

PATH = './trained_data.pth'
net = classificator_ALT.ALT_CLASSIFICATOR()
net.load_state_dict(torch.load(PATH))


classes = ['(NOT ALT)', '(ALT)'] 



def imshow(img, truel, predl):
    npimg = img.numpy()
    # Transpose from (C, H, W) to (H, W, C) for displaying
    npimg = np.transpose(npimg, (1, 2, 0))
    # plt.imshow(npimg)
    # npimg = img.numpy()
    # img=transforms.ToPILImage(npimg)
    plt.imshow(npimg)
    plt.title(f"True label - {classes[truel]}, Predicted - {classes[predl]}")
    plt.show()

true_count=0
false_count=0
stage_count=0

for batch in test_ds:
    images, labels = batch
    if(stage_count>4): break
    for i in range (8):

        index = i 
        image, label = images[index], labels[index]
        
        # print(f'GroundTruth: {classes[label]}')

        image1 = image.unsqueeze(0)
        output = net(image1)
        _, predicted = torch.max(output, 1)
        imshow(image, label, predicted.item())
        if label==predicted.item(): true_count+=1
        else: false_count+=1
        # print(f'Predicted: {classes[predicted.item()]}')
    stage_count+=1
    print(f"EPOCH {stage_count}\n\tAccuracy: {true_count/(true_count+false_count)}")
print(f"Final Accuracy is {true_count/(true_count+false_count)} from {true_count+false_count} images")