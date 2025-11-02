# X402 Mint Tools

## 🚀 Navigation
- [中文文档 (Chinese)](README.md)
- [English Documentation](README_EN.md)

## ⚠️ Important Notice
**Submit code to AI for security review before use! Test with new wallets first!**

## 🛠 Tools Overview

### 1. `x402_mint.py` - Main Tool
Automated X402 protocol mint operations with multi-wallet batch processing

### 2. `generate_tmp_private_key.py` - Wallet Generator
Generate test wallet private keys and addresses

### 3. `x402_monitor.py` - Monitor Tool ✅
Monitor new services on x402scan.com and send notifications when new services come online

## 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install web3 eth-account requests loguru mnemonic json-repair
```

## 🚀 Quick Start

### 1. Generate Test Wallets
```bash
python generate_tmp_private_key.py
```

### 2. Configure Parameters (edit x402_mint.py)
```python
TRY_TO_MINT_NUM = 100                                      # mint attempts
SINGLE_MINT_AMOUNT = 1                                     # amount per mint (USDC)
TO_ADDRESS = "Target Wallet Address"   # recipient address
MINT_ENDPOINT = "https://api.ping.observer/mint-v3"        # API endpoint
PRIVATE_KEY_LIST = ["your_private_key"]                    # private key list
```

### 3. Run Mint Tool
```bash
python x402_mint.py
```

### 4. Run Monitor Tool
```bash
python x402_monitor.py
```

**Monitor Tool Usage:**
- First run automatically caches existing service list
- Checks for new services every 30 seconds
- Displays detailed information when new services detected
- **User must implement notification functionality**: Edit `send_notification` method in `x402_monitor.py` to integrate your notification service (WeChat, DingTalk, Telegram, etc.)

## 📊 Monitor Configuration

The monitor tool supports the following notification methods (user implementation required):
1. **WeChat Enterprise Webhook** - Recommended for enterprise users
2. **DingTalk Bot** - Supports group message push
3. **Telegram Bot API** - Recommended for international users
4. **Email Notification** - Traditional method
5. **Other IM Tools** - Based on API integration

Modify the `send_notification` method in `x402_monitor.py:send_notification` to implement your preferred notification method.

## 📅 Availability Period

**x402scan updates frequently, this tool is tested valid until November 2, 2025**
If API changes occur, please update the code promptly or submit an issue

## 🔧 Advanced Configuration

### Monitor Interval Adjustment
Edit the end of `x402_monitor.py` file:
```python
loop_time_interval = 30  # Change to your desired interval (seconds)
```

### Cache File Location
Default cache file: `x402_services_cache.json`
You can specify a different path during initialization:
```python
monitor = X402Monitor("custom_cache_path.json")
```

## 🔧 Configuration Details

### Required Parameters
- `TRY_TO_MINT_NUM`: Number of mint attempts per wallet
- `SINGLE_MINT_AMOUNT`: USDC amount per mint operation
- `TO_ADDRESS`: Target recipient address (get from x402scan)
- `MINT_ENDPOINT`: API endpoint URL (get from x402scan)
- `PRIVATE_KEY_LIST`: List of private keys for your wallets

### Security Best Practices
1. **Never expose private keys** in public repositories
2. **Use test wallets first** before production use
3. **Start with small amounts** to verify functionality
4. **Review all code** with AI before execution
5. **Monitor transaction logs** for any issues
