from PIL import Image

import torch
import torch.nn as nn
from PIL.Image import Resampling
from torchvision.transforms import Compose, ToTensor


class CNN(nn.Module):
    def __init__(self, out_channels) -> None:
        super(CNN, self).__init__()

        # Level 1: (0 + 24) / 2 = 12
        # Level 2: (25 + 49) / 2 = 37
        # Level 3: (50 + 74) / 2 = 62
        # Level 4: (75 + 100) / 2 = 87
        self.brightness_levels = 4
        self.out_channels = out_channels

        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=self.out_channels, kernel_size=3, padding=1)
        self.batch_norm1 = nn.BatchNorm2d(self.out_channels)

        self.out_channels *= 2

        self.conv2 = nn.Conv2d(in_channels=self.out_channels // 2, out_channels=self.out_channels, kernel_size=3,
                               padding=1)
        self.batch_norm2 = nn.BatchNorm2d(self.out_channels)

        self.out_channels *= 2

        self.conv3 = nn.Conv2d(in_channels=self.out_channels // 2, out_channels=self.out_channels, kernel_size=3,
                               padding=1)
        self.batch_norm3 = nn.BatchNorm2d(self.out_channels)

        # A size of 640x480 picture is reduced by a factor of 2 three times in three pooling layers -> 80x60.
        self.fc = nn.Linear(self.out_channels * 80 * 60, self.brightness_levels)

    def forward(self, x):
        x = self.batch_norm1(self.pool(torch.relu(self.conv1(x))))
        x = self.batch_norm2(self.pool(torch.relu(self.conv2(x))))
        x = self.batch_norm3(self.pool(torch.relu(self.conv3(x))))

        # Resize the input from 4D to 3D wrt to the batch size in order to fit the input size of FC layer
        x = x.view(-1, self.out_channels * 80 * 60)

        return torch.softmax(self.fc(x), dim=1)


def preprocess_image(image_path):
    # Load the image
    image = Image.open(image_path)

    # # Resize the image
    # image = image.resize((640, 480), resample=Resampling.LANCZOS)

    # Apply the required transformations
    transform = Compose([
        ToTensor()
    ])
    image = transform(image)

    # Add a batch dimension
    image = image.unsqueeze(0)

    return image


def predict_image(image_path):
    # Preprocess the image
    image = preprocess_image(image_path)

    # Set the model to evaluation mode
    model = CNN(out_channels=2)
    model.eval()

    # Get the model's prediction
    output = model(image)

    # Get the index of the highest probability
    _, pred = output.max(1)

    result = pred.item()

    if result == 0:
        return 12
    elif result == 1:
        return 37
    elif result == 2:
        return 62
    return 87
