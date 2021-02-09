import os
from pathlib import Path

from PIL import Image

import torch
from torchvision import transforms

model_path = os.getcwd() + '/core/densenet121_imagenet.h5'
labels_path = os.getcwd() + '/core/imagenet_classes.txt'

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
    mean = [0.485, 0.456, 0.406],
    std  = [0.229, 0.224, 0.225]
)])

def predict(path):
    """
    Run inference on an image in the provided path using DenseNet121.
    """
    image_path = Path(path)
    img = Image.open(image_path)
    img_t = transform(img)
    batch_t = torch.unsqueeze(img_t, 0)
    
    model = torch.load(model_path)
    model.eval()
    out = model(batch_t)

    with open(labels_path) as f:
        labels = [line.strip() for line in f.readlines()]

    _, index = torch.max(out, 1)
    percentage = torch.nn.functional.softmax(out, dim=1)[0] * 100
    prediction = labels[index[0]].split(' ')[1]
    probability = round(percentage[index[0]].item(), 2)

    return [prediction, probability]
