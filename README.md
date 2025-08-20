# 🔍 Jeff's API Ripper

Extract API details from dealer menus and other web sources.

## Features

- 🔍 **Smart URL Analysis** - Detects password protection and authentication requirements
- 🔐 **Gated API Support** - Extract from protected APIs using browser automation
- 🌐 **Public Site Extraction** - Extract from publicly accessible websites
- 🤖 **Automatic GitHub Integration** - No need to manually enter tokens
- 🎨 **Beautiful Modern UI** - Clean, responsive interface
- 📊 **Comprehensive Analysis** - Detailed API endpoint and form analysis
- 💾 **Multiple Export Formats** - JSON, CSV, and API documentation

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jeff99jackson99/ripapidetail.git
   cd ripapidetail
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run src/app/main.py
   ```

## Usage

1. Enter the URL of the dealer menu or API documentation
2. Choose extraction method (Public URL or Gated API)
3. View extracted API details and analysis
4. Export results in your preferred format

## Deployment

### Streamlit Cloud
- Push to GitHub
- Connect repository to Streamlit Cloud
- Deploy automatically

### Local Docker
```bash
make docker/build
make docker/run
```

## License

MIT License - Copyright (c) 2025 Jeff Jackson
