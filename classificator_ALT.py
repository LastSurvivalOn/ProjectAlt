from torch import nn

class ALT_CLASSIFICATOR(nn.Module):
    def __init__(self, in_channels=3, out_channels=32, kernel_size=(3,3)):
        super().__init__()
        self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=kernel_size, stride=1, padding=1)
        self.relu=nn.ReLU()
        
        self.dropout1 = nn.Dropout(0.3)

        self.conv2 = nn.Conv2d(in_channels=out_channels, out_channels=32, kernel_size=(3,3), stride=1, padding=1)
        self.relu2 = nn.ReLU()
        
        self.pool = nn.MaxPool2d(kernel_size=(2,2))
        self.flat=nn.Flatten()
        
        #self.linear1 = nn.Linear(16384, 10)
        self.linear1 = nn.Linear(32 * 128 * 128, 10)
        
        self.relu3=nn.ReLU()
        
        self.dropout2 = nn.Dropout(0.5)
        
        self.linear2 = nn.Linear(10, 2)
        
    def forward(self, x):
        x = self.conv1(x)
        x = self.relu(x)
        x=self.dropout1(x)
        
        x = self.conv2(x)
        x = self.relu2(x)
        
        x = self.pool(x)
        
        print(x.shape)
        x = self.flat(x)
        print(x.shape)
        
        x=self.linear1(x)
        x = self.relu3(x)
        
        x = self.dropout2(x)
        
        x = self.linear2(x)
        
        return x
    
        
        