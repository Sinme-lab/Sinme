import torch
from typing import List, Dict
import asyncio

class FederatedTrainer:
    def __init__(self):
        self.current_model = None
        self.participants = set()
        
    async def aggregate_models(self, model_updates: List[Dict[str, torch.Tensor]]) -> Dict[str, torch.Tensor]:
        """Aggregate model updates from multiple participants"""
        aggregated_model = {}
        for param_name in model_updates[0].keys():
            stacked_params = torch.stack([update[param_name] for update in model_updates])
            aggregated_model[param_name] = torch.mean(stacked_params, dim=0)
        return aggregated_model
    
    async def start_training_round(self, model_id: str, round_number: int):
        """Initiate a new training round"""
        pass 
    
    async def calculate_rewards(self, 
                              participant_contributions: Dict[str, float]) -> Dict[str, float]:
        total_contribution = sum(participant_contributions.values())
        rewards = {}
        for participant, contribution in participant_contributions.items():
            reward = (contribution / total_contribution) * settings.REWARD_PER_ROUND
            rewards[participant] = reward
        return rewards
    
    async def get_training_status(self, model_id: str) -> Dict:
        return {
            "model_id": model_id,
            "current_round": self.current_round,
            "participants_count": len(self.participants),
            "status": "active" if self.current_model else "inactive"
        }