# config_manager.py
import os


class ConfigManager:
    """Manages configuration and API keys."""

    def __init__(self, file_path="binance_secrets.txt"):
        self.file_path = file_path
        self.secrets = self._load_secrets()

    def _load_secrets(self):
        """Load API keys and secrets from a file."""
        if not os.path.exists(self.file_path):
            raise FileNotFoundError(f"Secret file not found: {self.file_path}")
        secrets = {}
        with open(self.file_path, "r") as file:
            for line in file:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    secrets[key] = value
        return secrets

    def get_config(self, env):
        """Return configuration based on the environment."""
        try:
            if env == "testnet":
                return {
                    "base_url": "https://testnet.binance.vision/api",
                    "ws_url": "wss://testnet.binance.vision/ws",
                    "api_key": self.secrets["TESTNET_API_KEY"],
                    "api_secret": self.secrets["TESTNET_API_SECRET"],
                }
            elif env == "real":
                return {
                    "base_url": "https://api.binance.com/api",
                    "ws_url": "wss://stream.binance.com:9443/ws",
                    "api_key": self.secrets["REAL_API_KEY"],
                    "api_secret": self.secrets["REAL_API_SECRET"],
                }
            else:
                raise ValueError("Invalid environment. Use 'testnet' or 'real'.")
        except KeyError as e:
            raise ValueError(f"Missing key in secrets file: {e}")
