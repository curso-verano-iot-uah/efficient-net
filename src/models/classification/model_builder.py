import torchvision.models as models
import torch.nn as nn
import torch
import logging
import os


class ModelBuilder:
    def __init__(self, name, pretrained=True, fine_tune=True, num_classes=10, model_name='efficientnet_b0',
                 weights=None, device='cuda' if torch.cuda.is_available() else 'cpu'):

        self.model_name = name
        self.pretrained = pretrained
        self.fine_tune = fine_tune
        self.num_classes = num_classes
        self.model_name = model_name
        self.weights = weights
        self.device = device
        self.model = self.build_model()

    def build_model(self):
        """
        Builds and configures the model.

        Args:
        - pretrained: Boolean, indicating whether to use pretrained weights.
        - fine_tune: Boolean, indicating whether to fine-tune all layers.
        - num_classes: Number of output classes.
        - model_name: Name of the model to build.

        Returns:
        - model: The constructed and configured model.
        """

        if self.pretrained:
            logging.info('Loading pre-trained weights')
        else:
            logging.info('Not loading pre-trained weights')

        if self.model_name == 'efficientnet_b0':

            logging.info('Loading EfficientNet-B0')
            self.model = models.efficientnet_b0(pretrained=self.pretrained)
            logging.info('EfficientNet-B0 loaded.')

            self.model.classifier[1] = nn.Linear(in_features=1280, out_features=self.num_classes)
            logging.info('EfficientNet-B0 loaded.')

        elif self.model_name == 'resnet18':
            self.model = torch.hub.load('pytorch/vision:v0.10.0', 'resnet18', pretrained=self.pretrained)
            self.model.fc = nn.Linear(in_features=512, out_features=self.num_classes)
            logging.info('ResNet-18 loaded.')
        else:
            logging.info(f'Model {self.model_name} not implemented.')
            raise NotImplementedError(f'Model {self.model_name} not implemented.')

        # Freeze or fine-tune layers.
        self._set_requires_grad()

        if not self.pretrained and self.weights is not None:
            logging.info(f'Loading weights from {self.weights}')
            checkpoint = torch.load(self.weights, map_location=self.device)
            self.model.load_state_dict(checkpoint['model_state_dict'])
            logging.info('Weights loaded successfully.')

        return self.model

    def _set_requires_grad(self):
        """
        Helper function to set requires_grad attribute for model parameters.

        Args:
        - fine_tune: Boolean, indicating whether to fine-tune all layers.
        """
        if self.fine_tune:
            logging.info('Fine-tuning all layers...')
            for params in self.model.parameters():
                params.requires_grad = True
        else:
            logging.info('Freezing hidden layers...')
            for params in self.model.parameters():
                params.requires_grad = False

    def __dict__(self):
        # Return a dictionary with attribute names as keys and their values
        return {
            'model_name': self.model_name,
            'pretrained': self.pretrained,
            'fine_tune': self.fine_tune,
            'num_classes': self.num_classes,
            'weights': self.weights,
            'device': self.device
        }
