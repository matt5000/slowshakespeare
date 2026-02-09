# Slow Shakespeare for Tidbyt

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](../../LICENSE)
[![Platform](https://img.shields.io/badge/platform-Tidbyt-orange.svg)](https://tidbyt.com/)
[![Starlark](https://img.shields.io/badge/language-Starlark-purple.svg)](https://github.com/bazelbuild/starlark)

<p align="center">
  <img src="preview.gif" alt="Slow Shakespeare on Tidbyt" width="256">
</p>

Learn Shakespeare's sonnets through slow, daily repetition — one line per day over 14 days.

## Features

- **10 sonnets available**: 1, 18, 29, 30, 55, 73, 104, 116, 130, 138
- **Review mode**: At the top of each hour, animates through all learned lines
- **Static display**: Rest of the hour shows the newest line
- **Start date picker**: Begin anytime or sync with friends
- **Auto-advance**: Moves to next sonnet after 14 days
- **5 color themes**
- **Optional line numbers**

## Two Versions

This app has two deployment options:

### Tidbyt Community (Recommended)

Submit to the [Tidbyt Community](https://github.com/tidbyt/community) for cloud-hosted deployment. The app runs on Tidbyt's servers and pushes to your device automatically.

### Local Deployment

Run from your own machine using cron jobs. Requires your computer to be on and connected.

## Requirements

- [Tidbyt](https://tidbyt.com/) device
- macOS or Linux
- [Pixlet CLI](https://github.com/tidbyt/pixlet)

## Local Install

### 1. Install Pixlet

```bash
# macOS
brew install tidbyt/tidbyt/pixlet

# Linux: download from https://github.com/tidbyt/pixlet/releases
```

### 2. Set up credentials

Create `~/.tidbyt_credentials` with your device info (from Tidbyt app → Settings → General → Get API Key):

```bash
export TIDBYT_DEVICE_ID="your-device-id"
export TIDBYT_API_TOKEN="your-api-token"
```

Secure it:
```bash
chmod 600 ~/.tidbyt_credentials
```

### 3. Download and run

```bash
git clone https://github.com/matt5000/slowshakespeare.git
cd slowshakespeare/tidbyt

./push.sh
```

### 4. Set up cron jobs

The app needs two cron jobs — one for review mode at :00, one for static display at :01:

```bash
crontab -e
```

Add:
```cron
0 * * * * /path/to/apps/slowshakespeare/push.sh >> /path/to/cron.log 2>&1
1 * * * * /path/to/apps/slowshakespeare/push.sh >> /path/to/cron.log 2>&1
```

## Preview locally

```bash
pixlet serve --watch slow_shakespeare.star
# Open http://localhost:8080
```

## Configuration

The app supports these settings (via Tidbyt schema):

| Setting | Options |
|---------|---------|
| Sonnet | 1, 18, 29, 30, 55, 73, 104, 116, 130, 138 |
| Color | Salad Days, Milk of Kindness, Midsummer Night, All That Glisters, Damask Rose |
| Line numbers | On/Off |
| Started | Any date (to restart or sync with friends) |

## Testing

```bash
python3 test_slow_shakespeare.py
```

## License

Apache 2.0

---

Part of [Slow Shakespeare](https://github.com/matt5000/slowshakespeare) — learn Shakespeare's sonnets one line per day.
