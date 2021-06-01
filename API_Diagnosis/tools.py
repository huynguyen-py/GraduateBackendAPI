import pickle

import matplotlib.pyplot as plt
import torch
from PIL import Image


def load_checkpoint(model, filepath):
    # checkpoint = torch.load(filepath, map_location='cpu')
    checkpoint=pickle.load(open(filepath,'rb'))
    # model = checkpoint['model']
    model.load_state_dict(checkpoint)
    for parameter in model.parameters():
        parameter.requires_grad = False
    model.eval()
    return model


def plot_images(data, target, nrows=3, ncols=3):
    data = data[data['target'] == target].sample(nrows * ncols)['image_path']
    plt.figure(figsize=(nrows * 2, ncols * 2))
    for idx, image_path in enumerate(data):
        image = Image.open(image_path)
        plt.subplot(nrows, ncols, idx + 1)
        plt.imshow(image)
        plt.axis('off')
    plt.show();
