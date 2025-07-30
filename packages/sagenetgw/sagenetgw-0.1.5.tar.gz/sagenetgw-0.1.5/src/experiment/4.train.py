import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from numpy import log10

import json


def load_json_data(file_path):
    """从JSON文件加载数据"""
    with open(file_path, 'r') as f:
        data = json.load(f)
    # 验证数据格式
    assert all(k in data[0] for k in ['r', 'n_t', 'kappa10', 'T_re', 'DN_re',
                                      'Omega_bh2', 'Omega_ch2', 'H0', 'A_s',
                                      'f_interp_85', 'log10OmegaGW_interp_85']), "数据格式不正确"
    assert len(data[0]['f_interp_85']) == 256, "f_interp长度应为256"
    assert len(data[0]['log10OmegaGW_interp_85']) == 256, "log10OmegaGW长度应为256"
    return data


class GWDataset(Dataset):
    def __init__(self, data, x_scaler=None, y_scaler=None, param_scaler=None, fit_scalers=True):
        self.data = data

        params = np.array([[log10(item['r']), item['n_t'], log10(item['kappa10']),
                            log10(item['T_re']), item['DN_re'],
                            item['Omega_bh2'], item['Omega_ch2'], item['H0'], item['A_s']] for item in data])
        curves = np.array([np.column_stack((item['f_interp_85'],
                                            item['log10OmegaGW_interp_85']))
                           for item in data])

        # 分割x和y
        curves_x = curves[:, :, 0]
        curves_y = curves[:, :, 1]

        if fit_scalers or x_scaler or y_scaler or param_scaler is None:
            self.param_scaler = StandardScaler()
            self.param_scaler.fit(params)
            self.x_scaler = StandardScaler()
            self.x_scaler.fit(curves_x.reshape(-1, 1))
            self.y_scaler = StandardScaler()
            self.y_scaler.fit(curves_y.reshape(-1, 1))
        else:
            self.param_scaler = param_scaler
            self.x_scaler = x_scaler
            self.y_scaler = y_scaler

        self.params = self.param_scaler.transform(params)
        curves_x_scaled = self.x_scaler.transform(curves_x.reshape(-1, 1)).reshape(curves_x.shape)
        curves_y_scaled = self.y_scaler.transform(curves_y.reshape(-1, 1)).reshape(curves_y.shape)
        self.curves = np.stack([curves_x_scaled, curves_y_scaled], axis=2)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        params = torch.tensor(self.params[idx], dtype=torch.float32)
        curve = torch.tensor(self.curves[idx], dtype=torch.float32)
        return params, curve


def collate_fn(batch):
    params, curves = zip(*batch)
    return torch.stack(params), torch.stack(curves)


class ResidualBlock(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.block = nn.Sequential(
            nn.Linear(dim, dim),
            nn.GELU(),
            nn.LayerNorm(dim)
        )

    def forward(self, x):
        return x + self.block(x)


class CurvePredictor(nn.Module):
    def __init__(self, num_points=256):
        super().__init__()
        self.num_points = num_points

        self.param_encoder = nn.Sequential(
            nn.Linear(9, 128),
            nn.GELU(),
            nn.LayerNorm(128),
            nn.Linear(128, 256),
            nn.GELU(),
            nn.LayerNorm(256)
        )

        self.position_embed = nn.Embedding(num_points, 256)

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=256,
            nhead=8,
            dim_feedforward=512,
            dropout=0.1,
            activation="gelu",
            batch_first=True,
            norm_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=3)

        self.decoder = nn.Sequential(
            nn.Linear(256, 128),
            nn.GELU(),
            nn.Linear(128, 2)
        )

    def forward(self, x):
        batch_size = x.size(0)
        encoded_params = self.param_encoder(x)
        seq = encoded_params.unsqueeze(1).repeat(1, self.num_points, 1)
        positions = torch.arange(self.num_points, device=x.device).unsqueeze(0)  # [1, N]
        pos_embed = self.position_embed(positions)
        seq += pos_embed
        transformed = self.transformer(seq)
        outputs = self.decoder(transformed)
        return outputs
        # return outputs.permute(0, 2, 1)


from tqdm import tqdm


def train_gw_model(json_path, epochs=200, batch_size=32):
    raw_data = load_json_data(json_path)
    full_dataset = GWDataset(raw_data)
    print(f'data num:{len(raw_data)}')

    train_idx, val_idx = train_test_split(
        np.arange(len(full_dataset)),
        test_size=0.2,
        random_state=42
    )
    train_data = torch.utils.data.Subset(full_dataset, train_idx)
    val_data = torch.utils.data.Subset(full_dataset, val_idx)

    train_loader = DataLoader(
        train_data,
        batch_size=batch_size,
        shuffle=True,
        collate_fn=collate_fn
    )
    val_loader = DataLoader(
        val_data,
        batch_size=batch_size,
        collate_fn=collate_fn
    )

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = CurvePredictor().to(device)

    optimizer = optim.AdamW(model.parameters(), lr=1e-4, weight_decay=1e-5)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode='min',
        factor=0.5,
        patience=5
    )
    criterion = nn.MSELoss()
    print('start training')

    best_loss = float('inf')
    for epoch in tqdm(range(epochs)):
        model.train()
        train_loss = 0.0

        for params, curves in train_loader:
            params = params.to(device)
            curves = curves.to(device)

            optimizer.zero_grad()
            outputs = model(params)
            loss = criterion(outputs, curves)
            # loss_last = criterion(outputs[:,-1, :], curves[:,-1,:]) * 5.0  # 权重设为5
            # loss_rest = criterion(outputs[:, :, :], curves[:, :, :])
            # loss = loss_last + loss_rest
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

            train_loss += loss.item() * params.size(0)

        # 验证阶段
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for params, curves in val_loader:
                params = params.to(device)
                curves = curves.to(device)
                outputs = model(params)
                val_loss += criterion(outputs, curves).item() * params.size(0)

        train_loss /= len(train_loader.dataset)
        val_loss /= len(val_loader.dataset)
        scheduler.step(val_loss)

        print(f"Epoch {epoch + 1}/{epochs}")
        print(f"Train Loss: {train_loss:.4e} | Val Loss: {val_loss:.4e}")

        if val_loss < best_loss:
            best_loss = val_loss
            torch.save({
                'model_state': model.state_dict(),
                'x_scaler': full_dataset.x_scaler,
                'y_scaler': full_dataset.y_scaler,
                'param_scaler': full_dataset.param_scaler
            }, 'best_gw_model.pth')

    return model


class GWPredictor:
    def __init__(self, model_path='best_gw_model.pth'):
        checkpoint = torch.load(model_path, map_location='cpu')

        self.model = CurvePredictor()
        self.model.load_state_dict(checkpoint['model_state'])
        self.model.eval()

        self.x_scaler = checkpoint['x_scaler']
        self.y_scaler = checkpoint['y_scaler']
        self.param_scaler = checkpoint['param_scaler']

    def predict(self, params_dict):
        params = np.array([
            log10(params_dict['r']),
            params_dict['n_t'],
            log10(params_dict['kappa10']),
            log10(params_dict['T_re']),
            params_dict['DN_re']
        ]).reshape(1, -1)

        scaled_params = self.param_scaler.transform(params)

        with torch.no_grad():
            inputs = torch.tensor(scaled_params, dtype=torch.float32)
            outputs = self.model(inputs).numpy()

        # denorm = self.y_scaler.inverse_transform(
        #     outputs.reshape(-1, 2)).reshape(outputs.shape)
        denorm_x = self.x_scaler.inverse_transform(outputs[..., 0].reshape(-1, 1)).reshape(outputs.shape[0], -1)
        denorm_y = self.y_scaler.inverse_transform(outputs[..., 1].reshape(-1, 1)).reshape(outputs.shape[0], -1)

        return {
            'f': denorm_x[0].tolist(),
            'log10OmegaGW': denorm_y[0].tolist()
        }


trained_model = train_gw_model("solve_plus.data.json", epochs=200)