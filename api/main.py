from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from ..federated.trainer import FederatedTrainer
from ..blockchain.contract import BlockchainInterface
from ..security.privacy import PrivacyManager
from ..evaluation.metrics import ModelEvaluator
from ..auth.auth import get_current_user, Token, User
from fastapi.security import OAuth2PasswordRequestForm
import torch
from typing import List

app = FastAPI(title="Sinme - Decentralized AI Training Platform")

trainer = FederatedTrainer()
blockchain = BlockchainInterface()
privacy_manager = PrivacyManager()
evaluator = ModelEvaluator()

class ModelSubmission(BaseModel):
    model_hash: str
    creator_address: str

@app.post("/models/register")
async def register_model(submission: ModelSubmission):
    try:
        tx_hash = await blockchain.register_model(
            submission.model_hash,
            submission.creator_address
        )
        return {"status": "success", "transaction_hash": tx_hash}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/training/join/{model_id}")
async def join_training(model_id: str, participant_address: str):
    try:
        trainer.participants.add(participant_address)
        return {"status": "success", "message": "Successfully joined training"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/models/{model_id}/status")
async def get_model_status(model_id: str, current_user: User = Depends(get_current_user)):
    try:
        status = await trainer.get_training_status(model_id)
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/models/{model_id}/evaluate")
async def evaluate_model(
    model_id: str,
    test_data: List[float],
    test_labels: List[int],
    current_user: User = Depends(get_current_user)
):
    try:
        test_tensor = torch.tensor(test_data)
        labels_tensor = torch.tensor(test_labels)
        results = await evaluator.evaluate_model(
            trainer.current_model,
            test_tensor,
            labels_tensor
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/rewards/balance/{address}")
async def get_reward_balance(
    address: str,
    current_user: User = Depends(get_current_user)
):
    try:
        balance = await blockchain.get_token_balance(address)
        return {"address": address, "balance": balance}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))