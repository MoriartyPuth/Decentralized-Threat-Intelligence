# blockchain_backend.py
import torch
import torch.nn as nn
from web3 import Web3, EthereumTesterProvider
import numpy as np

# 1. AI Model Architecture
class MalwareDetector(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(5, 10), 
            nn.ReLU(), 
            nn.Linear(10, 2)
        )
    def forward(self, x): 
        return self.net(x)

# 2. Security Logic
def apply_differential_privacy(model, sigma=1.0):
    """Gaussian noise injection for data privacy."""
    with torch.no_grad():
        for param in model.parameters():
            noise = torch.randn_like(param.data) * sigma
            param.data.add_(noise)
    return model.state_dict()

def model_poisoning_attack(model):
    """Malicious update logic for Byzantine simulation."""
    with torch.no_grad():
        for param in model.parameters():
            param.data.mul_(-5.0) 
    return model.state_dict()

# 3. Aggregation & Blockchain
def krum_aggregation(updates):
    """Selection of the most consistent update via Euclidean distance."""
    if not updates: return None, 0
    flat_updates = [torch.cat([u[n].view(-1) for n in u.keys()]) for u in updates]
    distances = torch.zeros(len(updates))
    for i in range(len(updates)):
        for j in range(len(updates)):
            if i != j: distances[i] += torch.norm(flat_updates[i] - flat_updates[j])
    best_idx = torch.argmin(distances).item()
    return updates[best_idx], best_idx

def get_blockchain_connection():
    """Initializes local Ethereum tester."""
    return Web3(EthereumTesterProvider())


def calculate_privacy_utility_tradeoff(sigma_range):
    """Simulates the Accuracy vs Privacy curve for evaluation."""
    import numpy as np # Local import to ensure it works even if global fails
    accuracies = []
    base_acc = 0.94
    for s in sigma_range:
        decay = np.exp(-s * 0.45)
        acc = 0.5 + (base_acc - 0.5) * decay
        acc += np.random.normal(0, 0.005)
        accuracies.append(acc * 100)
    return accuracies
