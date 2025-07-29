# WxPal CLI

**WxPal CLI** is a command-line tool for accessing weather and fire risk data provided by Paladin Industries. It allows users to list and download CSV files hosted on a remote API, making it easy to integrate Paladin data into their workflows.

---

## 📦 Installation

Install directly from source (for dev/test use):

```bash
git clone https://github.com/YOUR_USERNAME/WxPal_CLI.git
cd WxPal_CLI
pip install -e .
```
Or install from PyPI (once published):

```bash
pip install wxpal-cli
```

🚀 Usage
Once installed, use the wxpal CLI tool:
```
🔍 List available files:

```bash
wxpal list
```

📥 Download a file:

```bash
wxpal download <filename.csv>
```
Example:

```bash
wxpal download wind_forecast_2025-04-20.csv
```
🔧 Configuration
The CLI pulls from a predefined API endpoint configured in the source. Future versions will support user-defined endpoints via config files or environment variables.

📄 License
MIT License

🛠️ Developed by
Paladin Industries — know wildfires