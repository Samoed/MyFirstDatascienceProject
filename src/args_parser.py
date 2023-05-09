from argparse import ArgumentParser


def get_device() -> int:
    parser = ArgumentParser(description="PyTorch MNIST Example")
    parser.add_argument(
        "--device", "-d",
        type=int,
        default=0,
        help="Webcam device number",
    )
    args = parser.parse_args()
    return args.device
