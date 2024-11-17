# Binance Trading Scripts

This repository contains Python scripts for interacting with the Binance API. These tools include real-time order book monitoring and a position neutralisation utility.

## Files Overview

- **`orderbook.py`**: Connects to the Binance WebSocket to display real-time order book data for a specific trading pair.
- **`neutralise_position.py`**: Neutralises a position in a specified trading pair using Binance API.
- **`binance_secrets.txt`**: Stores the Binance API keys for both testnet and real market environments (not included in the repository for security).

## Requirements

- Python 3.8 or higher
- A Binance account with API key and secret key set up.
- Basic familiarity with Python and Binance API usage.

## Installation

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
# OR
venv\\Scripts\\activate  # For Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create `binance_secrets.txt`

1. Create a [Binance account](https://accounts.binance.com/en/register?registerChannel=&return_to=). To then get API endpoint access, you need one layer of identity verification to be approved (should take like 5/10 mins to do and get approved).

2. Create your [Binance API keys](https://www.binance.com/en/my/settings/api-management) for the **actual exchange**
3. Create your [Binance API keys](https://testnet.binance.vision/) for the **testnet exchange**

Add your Binance API keys in a file named `binance_secrets.txt` at the root of the repository. The format should be:
```plaintext
TESTNET_API_KEY=your_testnet_api_key
TESTNET_API_SECRET=your_testnet_api_secret
REAL_API_KEY=your_real_api_key
REAL_API_SECRET=your_real_api_secret
```

### 5. Run Scripts

#### Order Book
To display the order book in real time:
```bash
python orderbook.py --env testnet  # For testnet
python orderbook.py --env real     # For real market
```

#### Neutralise Position
To neutralise a position in a specified trading pair:
```bash
python neutralise_position.py --pair BTCUSDT --env testnet
python neutralise_position.py --pair BTCUSDT --env real
```

#### SSL Errors
If you get SSL Certificate errors, just use ChatGPT and google to fix it up (its not that hard bro). I found this fixed it for me (on mac):
```bash
export SSL_CERT_FILE=/usr/local/etc/openssl@3/cert.pem
```
but it really depends on how you have your ssl configured.

### 6. Configure `.gitignore`
Make sure sensitive files are excluded from version control by using the provided `.gitignore` file.

## .gitignore
```plaintext
# Virtual environment
venv/

# Python cache files
__pycache__/
*.pyc
*.pyo

# Secrets file
binance_secrets.txt

# IDE configuration
.vscode/
.idea/
*.swp
*.swo
.DS_Store
```

## Notes

1. **Security**: Ensure your `binance_secrets.txt` file is not accidentally committed by keeping it in the `.gitignore`.
2. **Testing**: Use the `testnet` environment for testing before running scripts on the live market.
3. **Dependencies**: Update dependencies if new libraries are required for additional features.

## License
[MIT License](LICENSE)

---

Enjoy trading irresponsibly! 🚀

