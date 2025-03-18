from pydantic import BaseSettings

class Settings(BaseSettings):
    # Blockchain settings
    BLOCKCHAIN_PROVIDER_URL: str = "http://localhost:8545"
    CONTRACT_ADDRESS: str = ""
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./sinme.db"
    
    # API settings
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Model training settings
    MIN_PARTICIPANTS: int = 3
    ROUNDS_PER_EPOCH: int = 10
    
    # Token rewards
    REWARD_PER_ROUND: float = 1.0
    
settings = Settings() 