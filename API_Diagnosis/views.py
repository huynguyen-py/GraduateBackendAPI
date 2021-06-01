from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from .models import DiagnosisRecord
from .serializers import DiagnosisRecordSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView, get_object_or_404, ListCreateAPIView
from rest_framework import permissions, authentication
from rest_framework.views import APIView
from tqdm import tqdm

from .dataset import *
from .tools import *
import albumentations
import cloudinary


# import os
# from tqdm import tqdm
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from sklearn import model_selection
# from sklearn.model_selection import StratifiedKFold
# from sklearn.metrics import roc_auc_score
# import torch
# import torch.nn as nn
# import torch.nn.functional as F
# import torchvision.transforms as transforms
# import albumentations
# import pretrainedmodels
# from efficientnet_pytorch import EfficientNet
# from PIL import Image


class ListCreateDiagnosisView(ListCreateAPIView):
    model = DiagnosisRecord
    serializer_class = DiagnosisRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return DiagnosisRecord.objects.filter(author=self.request.user).order_by('-create_at')

    def create(self, request, *args, **kwargs):
        serializer = DiagnosisRecordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=self.request.user)

            return JsonResponse({
                'message': 'Create a new Record successful!'
            }, status=status.HTTP_201_CREATED)

        return JsonResponse({
            'message': 'Create a new Record unsuccessful!'
        }, status=status.HTTP_400_BAD_REQUEST)


class DiagnosisDetailView(RetrieveUpdateDestroyAPIView):
    model = DiagnosisRecord
    serializer_class = DiagnosisRecordSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return DiagnosisRecord.objects.filter(author=self.request.user)

    def put(self, request, *args, **kwargs):
        Old_record = get_object_or_404(DiagnosisRecord, id=kwargs.get('pk'))
        serializer = DiagnosisRecordSerializer(Old_record, data=request.data)

        print(request.data)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({
                'message': 'Update Record successful!'
            }, status=status.HTTP_200_OK)

        return JsonResponse({
            'message': 'Failed to update!'
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        diagnosis = get_object_or_404(DiagnosisRecord, id=kwargs.get('pk'))
        # cloudinary.up.destroy('zombie', None)
        diagnosis.delete()
        return JsonResponse({
            'message': 'Delete Record successful!'
        }, status=status.HTTP_200_OK)


# ==================================================


MyModel = Net_Efficientnet()
device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
MyModel = load_checkpoint(MyModel, 'static/efficientNet/MAIN_model_fold_full_1.pth')


def predicted(image_path, model, device):
    test_images = [image_path]
    mean = (0.485, 0.456, 0.406)
    std = (0.229, 0.224, 0.225)

    test_aug = albumentations.Compose([
        albumentations.Normalize(mean, std, max_pixel_value=255.0, always_apply=True),
    ])
    # dataset and dataloader for test images
    test_dataset = MelanomaDataset(
        image_paths=test_images,
        targets=[0],
        resize=[224,224],
        augmentations=test_aug
    )
    test_loader = torch.utils.data.DataLoader(
        test_dataset, batch_size=1, shuffle=False, num_workers=0
    )
    model.to(device)
    model.eval()
    test_predictions = np.zeros((1, 1))
    tk0 = tqdm(test_loader, total=1, position=0, leave=True)
    with torch.no_grad():
        for idx, data in enumerate(tk0):
            for key, value in data.items():
                data[key] = value.to(device)
            batch_preds, _ = model(**data)
            start = idx * 1
            end = start+len(data['image'])
            test_predictions[start:end] = batch_preds.cpu()
    tk0.close()
    return test_predictions.ravel()


'''
    predict view 
'''


class predictView(APIView):
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, format=None):
        return Response("hello")

    def post(self, request):
        record = DiagnosisRecord.objects.get(id=request.data['id'])
        url = record.image_record.url
        # print("url", url)
        serializer = DiagnosisRecordSerializer(record)
        final_predictions = predicted(url, MyModel, device)
        probs = np.round(torch.sigmoid(torch.tensor(final_predictions))).cpu().detach().numpy()
        print(np.round(torch.sigmoid(torch.tensor(final_predictions))).cpu().detach())
        record.predict = probs
        record.save()
        data = {
            'record': probs, 'data': serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)
