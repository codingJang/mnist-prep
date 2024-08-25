import random
import matplotlib.pyplot as plt
from torchvision import datasets, transforms
import os
import argparse

# Function to save random samples to an image file
def save_random_samples_image(dataset, num_samples=20, filename='random_samples.png'):
    # Select random indices
    indices = random.sample(range(len(dataset)), num_samples)
    
    # Set up the plot
    plt.figure(figsize=(10, 10))
    
    for i, idx in enumerate(indices):
        image, label = dataset[idx]
        image = image.squeeze(0)  # Remove the channel dimension
        
        # Plot the image
        plt.subplot(4, 5, i + 1)
        plt.imshow(image, cmap='gray')
        plt.title(f'Label: {label}')
        plt.axis('off')
    
    plt.tight_layout()
    
    # Ensure the directory exists
    os.makedirs('images', exist_ok=True)
    plt.savefig(os.path.join('images', filename))
    print(f"Random samples saved to {'images/'+filename}")

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Load MNIST dataset and save random samples.")
    parser.add_argument('--root', type=str, default='./data', help='Root directory for the dataset')
    parser.add_argument('--is-corrupted', action='store_true', help='Flag to indicate using corrupted dataset')

    args = parser.parse_args()

    # Determine the root directory based on the flag

    # Load the dataset
    train_dataset = datasets.MNIST(root=args.root, train=True, download=False, transform=transforms.ToTensor())
    test_dataset = datasets.MNIST(root=args.root, train=False, download=False, transform=transforms.ToTensor())

    print(f"Loaded {'corrupted' if args.is_corrupted else 'original'} MNIST dataset:")
    print(f"Training set size: {len(train_dataset)}")
    print(f"Test set size: {len(test_dataset)}")

    # Save 20 random images and their labels from the train dataset to an image file
    save_random_samples_image(train_dataset, num_samples=20, filename='random_mnist_samples.png')

if __name__ == '__main__':
    main()
