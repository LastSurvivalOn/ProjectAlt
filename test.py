from dataset_job import test_ds
import classificator_ALT
from torch import nn
from torch import optim
import torch
import torchvision
import matplotlib.pyplot as plt

PATH = './trained_data.pth'
net = classificator_ALT.ALT_CLASSIFICATOR()
net.load_state_dict(torch.load(PATH))


classes = ['(NOT ALT)', '(ALT)'] 

# dataiter = iter(test_ds)
# images, labels = dataiter.next()
# # print images
# plt.imshow(torchvision.utils.make_grid(images))
# print('GroundTruth: ', ' '.join(f'{classes[labels[j]]:5s}' for j in range(4)))



# # Perform inference and print predictions
# outputs = net(images)
# _, predicted = torch.max(outputs, 1)

# print('Predicted: ', ' '.join(f'{classes[predicted[j]]:5s}' for j in range(4)))

# correct = 0
# total = 0
# # since we're not training, we don't need to calculate the gradients for our outputs
# with torch.no_grad():
#     for data in test_ds:
#         images, labels = data
#         # calculate outputs by running images through the network
#         outputs = net(images)
#         # the class with the highest energy is what we choose as prediction
#         _, predicted = torch.max(outputs.data, 1)
#         total += labels.size(0)
#         correct += (predicted == labels).sum().item()

# print(f'Accuracy of the network on the 10000 test images: {100 * correct // total} %')

import numpy as np
# Get one batch from the DataLoader
images, labels = next(iter(test_ds))



# Define a function to show the image
def imshow(img):
    img = img / 2 + 0.5  # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))
    plt.show()

for i in range (32):
    
        # Select a single image and its label
    index = i  # Change this index to select a different image
    image, label = images[index], labels[index]
    # Print the selected image and its label
    imshow(image)
    print(f'GroundTruth: {classes[label]}')

    # Perform inference for the selected image
    image = image.unsqueeze(0)  # Add batch dimension since the model expects batches
    output = net(image)
    _, predicted = torch.max(output, 1)

    # Print the predicted label
    print(f'Predicted: {classes[predicted.item()]}')