import torch
from torch import nn

from yms_class.kan_convolutional.KANConv import KAN_Convolutional_Layer


class KKAN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()
        self.features = nn.Sequential(
            KAN_Convolutional_Layer(in_channels=3, out_channels=4, kernel_size=(3, 3), padding=(1, 1),
                                    grid_size=5),
            KAN_Convolutional_Layer(in_channels=4, out_channels=8, kernel_size=(3, 3), padding=(1, 1),
                                    grid_size=5),
            nn.MaxPool2d(2),
            KAN_Convolutional_Layer(in_channels=8, out_channels=16, kernel_size=(3, 3), padding=(1, 1),
                                    grid_size=5),
            KAN_Convolutional_Layer(in_channels=16, out_channels=32, kernel_size=(3, 3), padding=(1, 1),
                                    grid_size=5),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Linear(32 * 8 * 8, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x

if __name__ == '__main__':
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = KKAN().to(device)
    y = torch.randn(1, 3, 32, 32).to(device)
    z = model(y)
    print(z)
