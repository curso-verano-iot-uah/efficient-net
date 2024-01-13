import argparse


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-m', '--model-name', type=str, default='efficientnet_b0',
        dest='model-name', help='Model to use for training: efficientnet_b0, resnet18'
    )
    parser.add_argument(
        '-w', '--weights', type=str, default='../../weights/model_pretrained_True_prueba2.pth',
        dest='weights', help='Model weights to use for testing.'
    )

    parser.add_argument('-i', '--input', type=str, default='../../input/test/esp-camera',
                        dest='input', help='Path to the input folder.'
                        )

    parser.add_argument('-o', '--output', type=str, default='predictions',
                        dest='output', help='Path to the output folder where images predictions are save.'
                        )

    parser.add_argument('-s', '--save', type=bool, default=False,
                        dest='save', help='True for save the labeled images into the output folder, false '
                                          'for not save them but visualize them.'
                        )
    parser.add_argument('-c', '--camera', type=int, default=0,
                        help='Port the camera is connected to (0-99).'
                             'Default is 0. If you only have one camera,'
                             'you should always use 0.')

    parser.add_argument('-v', '--visualize', type=int, default=600,
                        help='Width of the window where we will see the '
                             'stream'
                             'of the camera. (Maintains the relationship of'
                             'aspect with respect to width)')

    parser.add_argument(
        '-e', '--epochs', type=int, default=10, help='Number of epochs to train our network for'
    )

    parser.add_argument(
        '-pt', '--pretrained', action='store_true', default=True, help='Whether to use pretrained weights or not'
    )

    parser.add_argument(
        '-lr', '--learning-rate', type=float, dest='learning_rate', default=0.0001,
        help='Learning rate for training the model'
    )

    parser.add_argument('-n', '--name', type=str, dest='name', help='Name used to store de results'
                        )

    return parser.parse_args()