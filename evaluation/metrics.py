import torch
from typing import Dict, List, Callable
import numpy as np

class ModelEvaluator:
    def __init__(self):
        self.metrics = {}
        
    def add_metric(self, name: str, metric_fn: Callable):
        self.metrics[name] = metric_fn
        
    async def evaluate_model(self, model: Dict[str, torch.Tensor], 
                           test_data: torch.Tensor, 
                           test_labels: torch.Tensor) -> Dict[str, float]:
        results = {}
        for name, metric_fn in self.metrics.items():
            results[name] = await metric_fn(model, test_data, test_labels)
        return results
    
    @staticmethod
    async def calculate_accuracy(predictions: torch.Tensor, 
                               labels: torch.Tensor) -> float:
        return (predictions.argmax(dim=1) == labels).float().mean().item() 