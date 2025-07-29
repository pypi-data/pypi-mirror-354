import os
import json
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import matplotlib.pyplot as plt
import random


# Tokenizer for text
class SimpleTokenizer:
    def __init__(self):
        self.word2idx = {"<PAD>": 0}
        self.idx2word = {0: "<PAD>"}
        self.idx = 1

    def encode(self, text):
        tokens = text.lower().split()
        indices = []
        for token in tokens:
            if token not in self.word2idx:
                self.word2idx[token] = self.idx
                self.idx2word[self.idx] = token
                self.idx += 1
            indices.append(self.word2idx[token])
        return torch.tensor(indices, dtype=torch.long)

    def vocab_size(self):
        return len(self.word2idx)


# Custom Dataset Loader from structured folders and JSON prompts
class TextImageDataset(Dataset):
    def __init__(self, data_dir, json_file, tokenizer, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.tokenizer = tokenizer
        with open(json_file, "r") as f:
            self.annotations = json.load(f)
        self.samples = list(self.annotations.items())

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        image_file, prompt = self.samples[idx]
        image_path = os.path.join(self.data_dir, image_file)
        image = Image.open(image_path).convert("RGB")
        if self.transform:
            image = self.transform(image)
        text = self.tokenizer.encode(prompt)
        return text, image


# Text Encoder
class TextEncoder(nn.Module):
    def __init__(self, vocab_size, embed_dim=256):
        super(TextEncoder, self).__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.rnn = nn.GRU(embed_dim, embed_dim, batch_first=True)

    def forward(self, x):
        embedded = self.embedding(x)
        _, hidden = self.rnn(embedded)
        return hidden.squeeze(0)


# Image Generator
class ImageGenerator(nn.Module):
    def __init__(self, embedding_dim=256):
        super(ImageGenerator, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(embedding_dim, 512 * 4 * 4),
            nn.ReLU(True),
            nn.Unflatten(1, (512, 4, 4)),
            nn.ConvTranspose2d(512, 256, 4, 2, 1),  # 8x8
            nn.ReLU(True),
            nn.ConvTranspose2d(256, 128, 4, 2, 1),  # 16x16
            nn.ReLU(True),
            nn.ConvTranspose2d(128, 64, 4, 2, 1),   # 32x32
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 3, 4, 2, 1),     # 64x64
            nn.Tanh()
        )

    def forward(self, embedding):
        return self.net(embedding)


# Main Class for TTI (Text-To-Image)
class TextToImage:
    def __init__(self, data_dir, json_file):
        self.tokenizer = SimpleTokenizer()
        self.transform = transforms.Compose([
            transforms.Resize((64, 64)),
            transforms.ToTensor()
        ])
        self.dataset = TextImageDataset(data_dir, json_file, self.tokenizer, self.transform)
        self.dataloader = DataLoader(self.dataset, batch_size=4, shuffle=True)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        vocab_size = self.tokenizer.vocab_size()
        self.text_encoder = TextEncoder(vocab_size).to(self.device)
        self.generator = ImageGenerator().to(self.device)

        self.optimizer = torch.optim.Adam(list(self.text_encoder.parameters()) + list(self.generator.parameters()), lr=0.001)
        self.criterion = nn.MSELoss()

    def train(self, epochs=5):
        print("Starting training...")
        for epoch in range(epochs):
            total_loss = 0
            for texts, images in self.dataloader:
                texts = texts.to(self.device)
                images = images.to(self.device)

                text_embeddings = self.text_encoder(texts)
                generated_images = self.generator(text_embeddings)

                loss = self.criterion(generated_images, images)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()

            #print(f"Epoch {epoch+1}/{epochs}, Loss: {total_loss:.4f}")
            #self.save_output(generated_images[0].detach().cpu(), f"output_epoch_{epoch+1}.png")
        print(f'Traning Done!')

    def generate(self, prompt):
        self.text_encoder.eval()
        self.generator.eval()
        with torch.no_grad():
            encoded = self.tokenizer.encode(prompt).unsqueeze(0).to(self.device)
            embedding = self.text_encoder(encoded)
            image = self.generator(embedding)
            return image.squeeze(0).cpu()

    def save_output(self, tensor_img, filename):
        img = transforms.ToPILImage()(tensor_img.clamp(0, 1))
        img.save(filename)
        print(f"[✓] Saved image as {filename}")

    def display_image(self, image_tensor):
        img = transforms.ToPILImage()(image_tensor.clamp(0, 1))
        plt.imshow(img)
        plt.axis("off")
        plt.show()


class TTI:
    def __init__(self, text: str, data_dir: str = 'assert', json_file: str = "dataset.json") -> None:
        self.text = text
        self.tti = TextToImage(data_dir, json_file)
        self.tti.train(epochs=10)
        self.gen_img = self.tti.generate(self.text)

    def display(self) -> None:
        self.tti.display_image(self.gen_img)

    def save(self, folder_name: str = "output.png") -> None:
        self.tti.save_output(self.gen_img, f"{folder_name.split('.')[0]}.png")
