
# Binance Trading Web Application

This repository contains a real-time trading order book application for Binance, with a front-end and back-end integration. The application displays live order book data from Binance for both **testnet** and **real market** environments.

## Features

- Real-time order book data display.
- WebSocket-based live data updates for both testnet and real environments.
- Modern, professional front-end built with React and Material-UI.
- Robust back-end implemented using Python and WebSockets.

---

## Requirements

### Back-End
- Python 3.8 or higher
- A Binance account with API key and secret key set up
- WebSocket and asyncio libraries

### Front-End
- Node.js and npm (for React)

---

## Installation

### Clone the Repository
```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

### Back-End Setup

#### 1. Create a Virtual Environment
```bash
cd web/backend
python3 -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scriptsctivate     # For Windows
```

#### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 3. Configure API Keys
Create a file named `binance_secrets.txt` in `web/backend`. Add your Binance API keys in the following format:
```plaintext
TESTNET_API_KEY=your_testnet_api_key
TESTNET_API_SECRET=your_testnet_api_secret
REAL_API_KEY=your_real_api_key
REAL_API_SECRET=your_real_api_secret
```

---

### 5. Run Scripts

#### Order Book
To display the order book in real time:
```bash
python terminal_view.py --env testnet --pair DOGEUSDT # For testnet DOGEUSDT
python terminal_view.py --env real --pair DOGEUSDT # For real market DOGEUSDT
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
but it really depends on how you have your SSL configured.

---

### 6. Start the Back-End

#### Navigate to the Back-End Directory
```bash
cd web/backend
```

#### Start the Development Server
For the **testnet** environment:
```bash
python backend.py --env testnet --pair DOGEUSDT --ws-port 8765
```

For the **real** environment:
```bash
python backend.py --env real --pair DOGEUSDT --ws-port 8766
```

---

### 7. Front-End Setup

#### 1. Navigate to the Front-End Directory
```bash
cd web/frontend
```

#### 2. Install Dependencies
```bash
npm install
```

#### 3. Start the Development Server
```bash
npm start
```

This will launch the front-end application in your default browser at `http://localhost:3000`.

---

### Configure .gitignore
Make sure sensitive files are excluded from version control by using the provided `.gitignore` file.

#### .gitignore
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

---

## Application Usage

### Navigation
The application has two pages:
1. **Testnet Page**: Displays the testnet order book (connected to port 8765).
2. **Real Page**: Displays the real market order book (connected to port 8766).

You can switch between these pages using the navigation bar.

### Order Book Display
- **Top of Book**: Displays the best bid and ask prices along with quantities.
- **Order Book Depth**: Displays bid and ask data in a table format.
- **Spread**: Shows the price difference between the best bid and ask prices.

---

## File Structure

### Back-End
- `backend.py`: Main back-end server script.
- `streamers.py`: Handles WebSocket connections to Binance.
- `data_manager.py`: Manages shared data and updates listeners.
- `config_manager.py`: Handles configuration and API keys.

### Front-End
- `src/`: React source files.
  - `pages/`: Components for testnet and real pages.
  - `components/`: Reusable UI components (tables, navigation bar).
  - `App.js`: Main application entry point.
  - `index.js`: ReactDOM entry point.

---

## Notes

1. **Testing**: Always test on the testnet environment before switching to the real market.
2. **Security**: Never expose your `binance_secrets.txt` file to the public.
3. **Performance**: The application uses WebSockets for low-latency updates.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

Enjoy trading responsibly! 🚀
