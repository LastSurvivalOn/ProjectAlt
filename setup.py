import classificator_ALT
import torch
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from PIL import Image

img = Image.open("foto.jpg")
size=(256, 256)
img1 = img.resize(size)

transform = transforms.Compose([transforms.ToTensor()])
img2 = transform(img1).unsqueeze(0)

PATH = './trained_data.pth'
net = classificator_ALT.ALT_CLASSIFICATOR()
net.load_state_dict(torch.load(PATH))

classes = ['(NOT ALT)', '(ALT)'] 


output = net(img2)
_, predicted = torch.max(output, 1)

plt.imshow(img)
plt.title(f"Predicted - {classes[predicted.item()]}")
plt.show()