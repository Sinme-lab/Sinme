import torch
from cryptography.fernet import Fernet
from typing import Dict
import hashlib

class PrivacyManager:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)
        
    def encrypt_model_weights(self, weights: Dict[str, torch.Tensor]) -> Dict[str, bytes]:
        encrypted_weights = {}
        for name, param in weights.items():
            data = param.numpy().tobytes()
            encrypted_data = self.cipher_suite.encrypt(data)
            encrypted_weights[name] = encrypted_data
        return encrypted_weights
    
    def decrypt_model_weights(self, encrypted_weights: Dict[str, bytes]) -> Dict[str, torch.Tensor]:
        decrypted_weights = {}
        for name, encrypted_data in encrypted_weights.items():
            data = self.cipher_suite.decrypt(encrypted_data)
            tensor = torch.from_numpy(np.frombuffer(data).reshape(original_shape))
            decrypted_weights[name] = tensor
        return decrypted_weights
    
    @staticmethod
    def compute_model_hash(weights: Dict[str, torch.Tensor]) -> str:
        hasher = hashlib.sha256()
        for name, param in sorted(weights.items()):
            hasher.update(param.numpy().tobytes())
        return hasher.hexdigest()