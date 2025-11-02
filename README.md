# X402 Mint Tools

## 🚀 导航栏 / Navigation
- [中文文档 (Chinese)](README.md)
- [English Documentation](README_EN.md)

## ⚠️ 重要提醒
**使用前请先将代码提交给 AI 审核，确保安全！建议先用新钱包测试！**

## 🛠 工具说明

### 1. `x402_mint.py` - 主要工具
自动化 X402 协议 mint 操作，支持多钱包批量处理

### 2. `generate_tmp_private_key.py` - 钱包生成器
生成测试钱包私钥和地址

### 3. `x402_monitor.py` - 监控工具 ✅
监控 x402scan.com 上新上线的服务，当检测到新服务时自动通知

## 📦 安装依赖
```bash
pip install -r requirements.txt
```

或者手动安装：
```bash
pip install web3 eth-account requests loguru mnemonic json-repair
```

## 🚀 快速开始

### 1. 生成测试钱包
```bash
python generate_tmp_private_key.py
```

### 2. 配置参数 (编辑 x402_mint.py)
```python
TRY_TO_MINT_NUM = 100                                      # mint 次数
SINGLE_MINT_AMOUNT = 1                                     # 每次金额 (USDC)
TO_ADDRESS = "Target Wallet Address"   # 收款地址
MINT_ENDPOINT = "https://api.ping.observer/mint-v3"        # API 接口
PRIVATE_KEY_LIST = ["your_private_key"]                    # 私钥列表
```

### 3. 运行 mint 工具
```bash
python x402_mint.py
```

### 4. 运行监控工具
```bash
python x402_monitor.py
```

**监控工具使用说明：**
- 首次运行会自动缓存现有服务列表
- 之后每30秒检查一次新服务
- 检测到新服务会在控制台显示详细信息
- **需要用户自行实现通知功能**：编辑 `x402_monitor.py` 中的 `send_notification` 方法，接入您的通知服务（微信、钉钉、Telegram等）

## 📊 监控工具配置

监控工具支持以下通知方式（需用户自行实现）：
1. **微信企业号 Webhook** - 推荐企业用户
2. **钉钉机器人** - 支持群消息推送
3. **Telegram Bot API** - 国际用户推荐
4. **邮件通知** - 传统方式
5. **其他即时通讯工具** - 根据API接入

修改 `x402_monitor.py:send_notification` 方法来实现您需要的通知方式。

## 📅 可用期限

**x402scan 更新频繁，截止2025年11月2日本工具测试有效**
如遇接口变化请及时更新代码或提交 issue

## 🔧 高级配置

### 监控间隔调整
编辑 `x402_monitor.py` 文件末尾：
```python
loop_time_interval = 30  # 修改为您需要的间隔时间（秒）
```

### 缓存文件位置
默认缓存文件：`x402_services_cache.json`
可在初始化时指定其他路径：
```python
monitor = X402Monitor("custom_cache_path.json")
```
