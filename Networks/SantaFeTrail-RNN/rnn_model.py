import torch
import torch.nn as nn
import torch.nn.functional as F

class SantaFeLSTM(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SantaFeLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size=input_size[0], hidden_size=hidden_size, batch_first=True)
        self.fc_value = nn.Linear(hidden_size, 128)
        self.fc_advantage = nn.Linear(hidden_size, 128)
        self.value = nn.Linear(128, 1)
        self.advantage = nn.Linear(128, output_size)

    def forward(self, x):
        x, _ = self.lstm(x)
        # If x is 3D (batch, seq, hidden), take last time step; if 2D, use as is
        if x.dim() == 3:
            x = x[:, -1, :]
        elif x.dim() == 2:
            pass  # already (batch, hidden)
        else:
            raise ValueError(f"Unexpected LSTM output shape: {x.shape}")
        value = F.relu(self.fc_value(x))
        advantage = F.relu(self.fc_advantage(x))
        value = self.value(value)
        advantage = self.advantage(advantage)
        q_values = value + (advantage - advantage.mean(dim=1, keepdim=True))
        return q_values
