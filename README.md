# 🔍 Jeff's API Ripper - Dealer Menu API Details Extractor

A powerful Streamlit application that extracts API details from dealer menus and other web sources, helping developers understand and integrate with various APIs.

## 🚀 Features

- **Multi-source extraction**: Extract from URLs, file uploads, GitHub repositories, or direct input
- **Intelligent parsing**: Automatically detects API endpoints, forms, JavaScript calls, and network requests
- **Pattern recognition**: Identifies REST APIs, GraphQL, OAuth, and other common API patterns
- **GitHub integration**: Sync configuration and updates from GitHub repositories
- **Export capabilities**: Export extracted data in JSON, CSV, YAML, or Markdown formats
- **Security analysis**: Identifies potential security concerns in API implementations
- **Documentation generation**: Auto-generates API documentation from extracted details

## 🛠️ Installation

### Prerequisites

- Python 3.11 or higher
- Chrome/Chromium browser (for Selenium-based extraction)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/jeff99jackson99/ripapidetail.git
   cd ripapidetail
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**
   ```bash
   streamlit run src/app/main.py
   ```

## 📁 Project Structure

```
ripapidetail/
├── src/
│   └── app/
│       ├── core/
│       │   ├── extractor.py          # Core extraction logic
│       │   ├── github_integration.py # GitHub integration
│       │   └── api_analyzer.py       # API analysis and documentation
│       ├── utils/
│       │   ├── config.py             # Configuration management
│       │   └── logging.py            # Logging utilities
│       └── main.py                   # Main Streamlit application
├── tests/                            # Test suite
├── config/                           # Configuration files
├── requirements.txt                  # Python dependencies
├── pyproject.toml                   # Project configuration
├── Dockerfile                       # Docker configuration
├── docker-compose.yml               # Docker Compose setup
├── Makefile                         # Build and development commands
└── README.md                        # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```bash
# GitHub Integration
GITHUB_TOKEN=your_github_token_here

# Extraction Settings
MAX_DEPTH=3
TIMEOUT=30
SELENIUM_ENABLED=false
CHROME_DRIVER_PATH=/path/to/chromedriver

# Logging
LOG_LEVEL=INFO
```

### GitHub Integration

To enable GitHub integration:

1. Create a GitHub Personal Access Token
2. Add it to your `.env` file
3. Use the GitHub sync feature in the application

## 🎯 Usage

### Basic Extraction

1. **URL Extraction**: Enter a dealer menu URL and click "Extract API Details"
2. **File Upload**: Upload HTML/text files for analysis
3. **Direct Input**: Paste content directly into the application

### Advanced Features

- **Pattern Analysis**: Automatically detect API patterns and generate recommendations
- **Security Scanning**: Identify potential security concerns
- **Documentation Generation**: Create comprehensive API documentation
- **Data Export**: Export results in multiple formats

### Example Workflow

1. Navigate to a dealer website
2. Use the URL extraction feature
3. Review extracted endpoints, forms, and JavaScript
4. Analyze patterns and security concerns
5. Generate API documentation
6. Export data for integration

## 🧪 Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black src/ tests/
ruff check src/ tests/
```

### Available Commands

```bash
make setup          # Setup development environment
make dev           # Run development server
make test          # Run test suite
make lint          # Run linting
make fmt           # Format code
make docker/build  # Build Docker image
make docker/run    # Run Docker container
```

## 🐳 Docker

### Build and Run with Docker

```bash
# Build the image
docker build -t api-ripper .

# Run the container
docker run -p 8501:8501 api-ripper

# Or use Docker Compose
docker-compose up
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_extractor.py
```

## 📊 API Extraction Capabilities

The application can extract:

- **API Endpoints**: REST, GraphQL, and custom API endpoints
- **Form Data**: HTML forms with input fields and submission details
- **JavaScript Calls**: Fetch, Axios, jQuery AJAX, and XMLHttpRequest calls
- **Network Requests**: Data attributes and API-related HTML elements
- **API Keys**: Potential API keys and authentication tokens
- **Metadata**: Page information and response headers

## 🔒 Security Features

- **API Key Detection**: Identifies exposed API keys in client-side code
- **URL Analysis**: Detects sensitive data in URLs
- **Form Security**: Analyzes form submission methods and security
- **Authentication Patterns**: Identifies OAuth and other auth mechanisms

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

Copyright (c) 2025 Jeff Jackson

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Uses [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing
- [Selenium](https://selenium.dev/) for dynamic content extraction
- [PyGithub](https://pygithub.readthedocs.io/) for GitHub integration

## 📞 Support

For support and questions:

- Create an [issue](https://github.com/jeff99jackson99/ripapidetail/issues)
- Contact: jeff99jackson99@gmail.com

---

**Note**: This tool is designed for legitimate API integration purposes. Please ensure you have permission to analyze any websites or APIs you're extracting information from.
