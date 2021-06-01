import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from efficientnet_pytorch import EfficientNet
from PIL import Image
import requests

class CustomLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2):
        super(CustomLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma

    def forward(self, predictions, targets):
        criterion = nn.BCEWithLogitsLoss()
        logits = criterion(predictions, targets.view(-1, 1).type_as(predictions))
        pt = torch.exp(-logits)
        focal_loss = self.alpha * (1 - pt) ** self.gamma * logits
        return torch.mean(focal_loss)



class MelanomaDataset(torch.utils.data.Dataset):
    def __init__(self, image_paths, targets, resize, augmentations=None):
        self.image_paths = image_paths
        self.targets = targets
        self.resize = resize
        self.augmentations = augmentations

    def __getitem__(self, index):
        image_path = self.image_paths[index]
        target = self.targets[index]
        # print(image_path)
        image = Image.open(requests.get(image_path, stream=True).raw)
        if self.resize is not None:
            image = image.resize(
                (self.resize[1], self.resize[0]), resample=Image.BILINEAR
            )
        image = np.array(image)
        if self.augmentations is not None:
            augmented = self.augmentations(image=image)
            image = augmented['image']
        image = np.transpose(image, (2, 0, 1)).astype(np.float32)
        return {
            'image': torch.tensor(image),
            'target': torch.tensor(target)
        }

    def __len__(self):
        return len(self.image_paths)


class Net_Efficientnet(nn.Module):
    def __init__(self,):
        super(Net_Efficientnet, self).__init__()
        # self.base_model = EfficientNet.from_pretrained('efficientnet-b7')
        self.base_model = EfficientNet.from_pretrained('static/efficientNet//efficientnet-b7-dcc49843.pth')
        # self.base_model = self.base_model.load_state_dict(torch.load('static/efficientNet//efficientnet-b7-dcc49843.pth'))
        self.fc = nn.Linear(self.base_model._fc.in_features, 1)

    def forward(self, image, target):
        batch_size, _, _, _ = image.shape
        out = self.base_model.extract_features(image)
        out = F.adaptive_avg_pool2d(out, 1).view(batch_size, -1)
        out = self.fc(out)
        # loss = nn.BCEWithLogitsLoss()(out, target.view(-1, 1).type_as(out))
        loss = CustomLoss()(out, target.view(-1, 1).type_as(out))
        return out, loss
