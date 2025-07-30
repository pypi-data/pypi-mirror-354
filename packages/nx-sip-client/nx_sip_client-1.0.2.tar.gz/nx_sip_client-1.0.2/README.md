# <div align="center"> SIP Client Library </div>

Python SIP 客戶端庫，提供兩種不同的實現方式：基於 PJSUA2 的高階實現和基於原生 UDP Socket 的底層實現。

## <div align="center"> 概述 </div>

這個庫包含兩個獨立的 SIP 客戶端實現：

### 🚀 PJSUA2 版本 (`sip_client.pj`)
- **適用場景**: 生產環境、快速開發、穩定性要求高
- **特點**: 成熟穩定、功能完整、API 簡潔
- **依賴**: PJSUA2 庫

### 🛠️ UDP 手刻版本 (`sip_client.udp`)
- **適用場景**: 學習研究、深度客製化、嵌入式系統
- **特點**: 完全控制、教育價值、輕量級
- **依賴**: 僅 Python 標準庫

## <div align="center"> 安裝方式 </div>

### PyPI 安裝

```bash
pip install nx-sip-client
```

> ⚠️ **注意**: 若欲使用本庫中的pj.sip_client，需要系統中已安裝 PJSUA2 庫。若無，建議使用下面的 Docker 環境。

### 🐳 使用 Docker 環境（推薦）

```bash
# 克隆項目（獲取 Docker 配置）
git clone <repository-url>
cd sip-client

# 構建含 PJSUA2 的 Docker 映像
cd docker
docker build -t sip-client .
docker run -it --network host sip-client /bin/bash

# 使用 Docker Compose 啟動環境
# 內有 volume 本庫做快速測試
cd docker
docker-compose up -d
```

### 🔧 自行安裝環境

如果需要開發或客製化：

```bash
# 克隆項目
git clone <repository-url>
cd sip-client

# PJSUA2 安裝及編譯（複雜，建議使用 Docker）
# 詳細步驟請參考 docker/Dockerfile

# 安裝測試依賴
pip install -r requirements.txt
```

## <div align="center"> 基本使用 </div>

#### 使用測試程式

```bash
# 進入容器
docker exec -it sip-client /bin/bash

# 在容器中運行測試
cd /home/user
python3 test_pjsua2.py  # 測試 PJSUA2 版本
python3 test_udp.py     # 測試 UDP 版本
```

#### PJSUA2 版本（需要 Docker 環境）

```python
from sip_client.pj import SipClient
import logging

# 設定日誌
logging.basicConfig(level=logging.DEBUG)

# 建立客戶端
sc = SipClient(
    domain="sip.provider.com",
    port=5060,
    username="your_username",
    password="your_password",
    transport_ip="192.168.1.100",
    transport_port=5060,
    sip_log_level=3
)

# 初始化並註冊
sc.init()

# 等待註冊成功
while not sc.account.getInfo().regIsActive:
    sc.ENDPOINT.libHandleEvents(10)

print("SIP 註冊成功")

# 撥打電話
sc.make_call("target_user")

# 主事件循環
while True:
    sc.ENDPOINT.libHandleEvents(10)
    # 其他邏輯...
```

#### UDP 手刻版本

```python
from sip_client.udp import SipClient, CallState
import time

# 建立客戶端
sc = SipClient(
    domain="sip.provider.com",
    port=5060,
    username="your_username",
    password="your_password",
    transport_ip="192.168.1.100",
    transport_port=5060,
    rtp_port=5004,
    rtcp_port=5005
)

# 註冊 SIP 帳號
success = sc.register()
if success:
    print("註冊成功")
    
    # 撥打電話
    sc.make_call("target_user")
    
    # 檢查通話狀態
    while sc.state != CallState.CONFIRMED:
        time.sleep(0.1)
    
    print("通話已建立")
```

## <div align="center"> 功能比較 </div>

| 功能 | PJSUA2 版本 | UDP 手刻版本 |
|------|-------------|--------------|
| 基本通話 | ✅ | ✅ |
| 來電處理 | ✅ | ✅ |
| 主動轉接 | ✅ | ✅ |
| 被動轉接（接收 REFER） | ⚠️ | ⚠️ |
| 通話保留 | ✅ | ✅ |
| Digest 認證 | ✅ | ✅ |
| RTP 音頻 | ✅ | ✅ |
| 183 智能處理 | ✅ | ❌ |
| Hold-then-REFER | ✅ | ❌ |
| 線程安全 | ✅ | ⚠️ |
| 多編解碼器 | ✅ | ⚠️ |
| 開發難度 | 低 | 中 |
| 資源使用 | 高 | 低 |
| 客製化程度 | 中 | 高 |

## <div align="center"> 詳細文檔 </div>

### PJSUA2 版本
詳細說明請參考：[sip_client/pj/README.md](sip_client/pj/README.md)

**主要特色：**
- 基於成熟的 PJSIP 庫
- 完整的線程安全支援
- 自動通話處理（183 Session Progress）
- 標準的 Hold-then-REFER 轉接機制
- 多編解碼器支援

### UDP 手刻版本
詳細說明請參考：[sip_client/udp/README.md](sip_client/udp/README.md)

**主要特色：**
- 完全手工實現 SIP 協議
- 基於 RFC 3261 的完整狀態機
- 詳細的識別符管理說明
- 適合學習和深度客製化
- 輕量級，無外部依賴

## <div align="center"> 音頻處理範例 </div>

兩個版本都支援音頻處理，以下是通用的音頻處理範例：

```python
import librosa
import numpy as np

def convert_to_audio_bytes(audio, sr, norm=True):
    """將音頻轉換為 8kHz 16bit PCM 格式"""
    if sr != 8000:
        audio = librosa.resample(audio, orig_sr=sr, target_sr=8000, res_type='kaiser_fast')

    if norm:  
        # 正規化避免高頻雜音
        audio = audio * (32767 / max(0.01, np.max(np.abs(audio))))
        audio = audio.astype(np.int16)
    else:
        audio = (audio * 32767).astype(np.int16)

    return audio.tobytes()

# 播放音頻到通話中
def play_audio_to_call(sip_client, audio_file):
    audio, sr = librosa.load(audio_file, sr=None)
    audio_bytes = convert_to_audio_bytes(audio, sr)
    
    # PJSUA2 版本
    if hasattr(sip_client, 'current_call') and sip_client.current_call:
        sip_client.current_call.putFrame(audio_bytes)
    
    # UDP 版本  
    if hasattr(sip_client, 'current_call') and sip_client.current_call:
        sip_client.current_call.send_audio(audio_bytes)
```

## <div align="center"> 測試範例 </div>

項目包含完整的測試範例：

- **test_pjsua2.py**: PJSUA2 版本的完整測試
- **test_udp.py**: UDP 版本的完整測試
- **test_audio.py**: 音頻處理測試

```bash
# 測試 PJSUA2 版本
python test_pjsua2.py

# 測試 UDP 版本
python test_udp.py

# 測試音頻處理
python test_audio.py
```

## <div align="center"> 已知限制與 TODO </div>

### 當前限制
- **被動轉接功能不完整**: 當對方（第三方）嘗試將通話轉接到本 SIP 客戶端時，可能會出現問題
- **REFER 請求處理**: 接收和處理來自外部的 REFER 請求尚未完全實現

### TODO 清單
1. **完善被動轉接機制**
   - 實現接收 REFER 請求的完整處理流程
   - 支援被動轉接時的狀態機轉換
   - 處理轉接過程中的錯誤情況

2. **UDP 版本改進**
   - RTP socket 的保護機制
   - Socket 發送失敗時的 FSM 調整
   - 增強線程安全性

3. **功能擴展**
   - 支援更多音頻編解碼器
   - 改進錯誤處理和恢復機制
   - 添加更完整的 SIP 特性支援

## <div align="center"> 注意事項 </div>

1. **推薦使用 Docker**: 由於 PJSUA2 編譯複雜，強烈建議使用提供的 Docker 環境
2. **網路配置**: 使用 `--network host` 模式確保 SIP 和 RTP 端口正常通信
3. **音頻格式**: 預設使用 PCMA/8000 編解碼器
4. **線程安全**: UDP 版本在多線程環境需要額外注意
5. **手動編譯**: 如需手動編譯 PJSUA2，請參考 `docker/Dockerfile` 中的詳細步驟
