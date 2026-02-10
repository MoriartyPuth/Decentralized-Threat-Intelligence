# Topic: A Blockchain-Integrated Framework with Byzantine-Robust Aggregation and Differential Privacy

## 📖 Project Overview
This project addresses the critical security gaps in Industrial Internet of Things (IIoT) networks. Traditional centralized AI models expose sensitive industrial data to leakage and are vulnerable to single points of failure.

Our solution implements a Decentralized Security Operations Center (SOC) that uses Federated Learning to train malware detection models locally on edge devices. To ensure the system is "Trustless," we integrate Blockchain-based Reputation and Multi-Krum Consensus to automatically detect and "slash" malicious actors attempting model poisoning attacks.

## 🚀 Key Features
- Decentralized Training: Local data never leaves the IIoT device.
- Differential Privacy: Gaussian noise injection ensures $(\epsilon, \delta)$-privacy.
- Byzantine Resilience: Krum Aggregation filters out malicious "Poisoned" updates.
- Blockchain Ledger: A simulated Ethereum-backed trust system with automated slashing logic.
- Live SOC Dashboard: Real-time visualization of network health, node reputation, and security alerts.

## 🏗️ Mathematical Framework

1. Differential Privacy (DP)

To prevent data re-identification, we apply the Gaussian Mechanism to local gradients $\Delta w$:


$$\Delta \tilde{w} = \Delta w + \mathcal{N}(0, \sigma^2)$$


Where $\sigma$ is the noise multiplier adjusted via the dashboard to balance the Privacy-Utility Trade-off.

2. Byzantine-Robust Consensus (Multi-Krum)

Standard averaging (FedAvg) is vulnerable to malicious outliers. We implement Krum Aggregation, which selects updates based on Euclidean distance ($L_2$ norm):

$$Score(i) = \sum_{j \in \text{neighbors}} ||w_i - w_j||^2$$

The aggregator selects the update $i$ with the minimum score, effectively isolating attackers (like Node 3) whose updates are mathematically distant from the honest majority.

3. Reputation & Slashing Logic

Network trust is managed via a dynamic reputation function $R$:

- Honest Participation: $R_{t+1} = R_t + 5$
- Malicious Detection: $R_{t+1} = R_t - 35$

### 🔄 Logical Data Flow
```mermaid
sequenceDiagram
    participant Device as IIoT Edge Device
    participant AI as Local Model (PyTorch)
    participant Sec as Security Controller (Krum)
    participant BC as Blockchain (Web3)

    Note over Device, BC: Start Federated Round
    Device->>AI: Train on Local Data
    AI->>AI: Apply Differential Privacy (Add Noise)
    AI->>Sec: Submit Model Update
    
    alt Update is Honest
        Sec->>BC: Validate & Aggregate Update
        BC->>Device: Reward Reputation (+5)
    else Update is Malicious (Outlier)
        Sec->>Sec: Detect via Euclidean Distance
        Sec->>BC: Flag Byzantine Activity
        BC->>Device: Slash Reputation (-35)
    end
    
    BC->>AI: Broadcast New Global Model
```
### 🗺️ System Topology
```mermaid
graph TD
    subgraph "IIoT Edge Layer"
        N1[IIoT Node 1 - Honest]
        N2[IIoT Node 2 - Honest]
        N3[IIoT Node 3 - Malicious]
    end

    subgraph "Security Layer (Consensus)"
        DP{Differential Privacy Filter}
        Krum[Multi-Krum Aggregator]
    end

    subgraph "Blockchain Layer"
        BC[(Immutable Ledger)]
        Rep[Reputation System]
    end

    N1 & N2 & N3 --> DP
    DP --> Krum
    Krum --> BC
    BC --> Rep
    Rep -.->|Update Trust Score| N1 & N2 & N3
```

## 📊 Scientific Evaluation

The Analytics Tab in the dashboard provides a simulated evaluation of the model performance. It demonstrates that while increasing Privacy Noise ($\sigma$) protects data, it leads to a non-linear decay in accuracy, following the curve:

$$Accuracy \approx 0.5 + (Base - 0.5) \cdot e^{-\sigma \cdot 0.45}$$

This allows researchers to find the "Sweet Spot" for IIoT security deployments.

## 🛠️ Installation & Setup

Clone the Repository:
- git clone https://github.com/MoriartyPuth/Decentralized-Threat-Intelligence

Install Dependencies:
- pip install -r requirements.txt

Run the Dashboard:
- python -m streamlit run app.py

## 🖥️ Dashboard Preview

<img width="1912" height="938" alt="Screenshot 2026-02-04 002150" src="https://github.com/user-attachments/assets/3947bec1-036b-4c50-b557-b4fa5f608c71" />
<img width="1529" height="759" alt="image" src="https://github.com/user-attachments/assets/8101590a-11c3-4a98-859f-3caa28ad418a" />


## ⚖️ Disclaimer

This project is intended for defensive and educational purposes only. It does not provide offensive tooling or exploit code.

