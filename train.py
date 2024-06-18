from dataset_job import train_ds
import classificator_ALT
from torch import nn
from torch import optim
import torch


model = classificator_ALT.ALT_CLASSIFICATOR()
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)


num_epochs = 10

for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    
    for images, labels in train_ds:
        optimizer.zero_grad()
        outputs = model(images)
        labels = labels.view(-1)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item()
    
    print(f'Epoch {epoch+1}, Loss: {running_loss / len(train_ds)}')

PATH = './trained_data.pth'
torch.save(model.state_dict(), PATH)