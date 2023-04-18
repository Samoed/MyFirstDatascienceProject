import argparse

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import f1_score
from sklearn.model_selection import train_test_split
from torch import nn, optim
from torch.utils.data import DataLoader, Dataset
from tqdm.auto import tqdm
import mlflow.pytorch

BATCH_SIZE = 8


class HandLandmarksDataset(Dataset):
    def __init__(self, imgs: np.ndarray):
        self.imgs = imgs

    def __len__(self):
        return len(self.imgs)

    def __getitem__(self, idx):
        arr = self.imgs[idx]
        return torch.tensor(arr[:-1], dtype=torch.float32), torch.tensor(arr[-1], dtype=torch.int64)


class GestureClassifier(nn.Module):
    def __init__(self, num_classes: int = 14):
        super(GestureClassifier, self).__init__()

        # Fully connected layers
        self.fc1 = nn.Linear(42, 128)  # 21 * 2
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, num_classes)  # 14 classes for the gestures

    def forward(self, x):
        # x = x.view(-1, 21 * 2)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def train(
        model, train_loader, test_loader, criterion, optimizer, num_epochs=10, batch_size=32, device=torch.device("cpu")
):
    # Train the model
    train_predicted = []
    train_labels = []
    for epoch in tqdm(range(num_epochs), desc="Epochs"):
        # Set the model to training mode
        model.train()

        # Initialize running loss and accuracy
        running_loss = 0.0
        running_accuracy = 0.0

        # Train on the batches in the training set
        pbar = tqdm(train_loader, desc=f"Train Epoch {epoch + 1}/{num_epochs}")
        for i, (inputs, labels) in enumerate(pbar):
            # Send the inputs and labels to the device
            inputs = inputs.to(device)
            labels = labels.to(device)

            # Zero the gradients
            optimizer.zero_grad()

            # Forward pass and backward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # Update the running loss and accuracy
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs.data, 1)
            running_accuracy += torch.sum(predicted == labels).item()
            mlflow.log_metric("loss", running_loss)

            train_predicted.extend(predicted.tolist())
            train_labels.extend(labels.tolist())

        # Compute the average loss and accuracy for the epoch
        epoch_loss = running_loss / len(train_loader)
        epoch_accuracy = running_accuracy / len(train_loader)
        epoch_f1 = f1_score(train_labels, train_predicted, average="macro")

        mlflow.log_metric("epoch_loss", epoch_loss, epoch)
        mlflow.log_metric("epoch_accuracy", epoch_accuracy, epoch)
        mlflow.log_metric("epoch_f1", epoch_f1, epoch)

        # Print the training loss and accuracy for the epoch
        print(f"Train Epoch {epoch + 1}: Loss={epoch_loss:.4f}, Accuracy={epoch_accuracy:.4f}, F1={epoch_f1:.4f}")

        # Set the model to evaluation mode
        model.eval()

        # Initialize test loss and accuracy
        test_loss = 0.0
        test_accuracy = 0.0

        # Evaluate on the batches in the test set
        with torch.no_grad():
            pbar = tqdm(test_loader, desc=f"Test Epoch {epoch + 1}/{num_epochs}")

            test_predicted = []
            test_labels = []
            for i, (inputs, labels) in enumerate(pbar):
                # Send the inputs and labels to the device
                inputs = inputs.to(device)
                labels = labels.to(device)

                # Forward pass
                outputs = model(inputs)

                # Compute the loss and accuracy
                loss = criterion(outputs, labels)
                test_loss += loss.item() * inputs.size(0)
                _, predicted = torch.max(outputs.data, 1)
                test_accuracy += torch.sum(predicted == labels).item()

                test_predicted.extend(predicted.tolist())
                test_labels.extend(labels.tolist())

        # Compute the average test loss and accuracy for the epoch
        test_loss /= len(train_loader)
        test_accuracy /= len(train_loader)
        test_f1 = f1_score(test_labels, test_predicted, average="macro")

        mlflow.log_metric("test_accuracy", test_accuracy, epoch)
        mlflow.log_metric("test_f1", test_f1, epoch)

        # Print the test loss and accuracy for the epoch
        print(f"Test Epoch {epoch + 1}: Loss={test_loss:.4f}, Accuracy={test_accuracy:.4f}, F1={test_f1:.4f}")


def main():
    parser = argparse.ArgumentParser(description="PyTorch MNIST Example")
    parser.add_argument(
        "--epochs",
        type=int,
        default=7,
        metavar="N",
        help="number of epochs to train (default: 14)",
    )
    parser.add_argument(
        "--lr",
        type=float,
        default=0.001,
        metavar="LR",
        help="learning rate (default: 0.001)",
    )
    args = parser.parse_args()

    data = np.load("../../data/processed.npy")

    train_data, test_data = train_test_split(data, test_size=0.1)
    train_dataset = HandLandmarksDataset(train_data)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

    test_dataset = HandLandmarksDataset(test_data)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=True)

    model = GestureClassifier()
    scripted_model = torch.jit.script(model)  # scripting the model
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    train(scripted_model, train_loader, test_loader, criterion, optimizer, num_epochs=args.epochs)

    mlflow.pytorch.log_model(scripted_model, "model")  # logging scripted model


if __name__ == "__main__":
    main()
