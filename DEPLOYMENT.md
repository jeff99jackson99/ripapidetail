# 🚀 Deployment Guide for Jeff's API Ripper

## 🌐 Streamlit Cloud Deployment

### Prerequisites
- GitHub repository with your code (✅ Already done!)
- Streamlit Cloud account

### Step 1: Sign up for Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"

### Step 2: Configure Your App
1. **Repository**: Select `jeff99jackson99/ripapidetail`
2. **Branch**: Select `main`
3. **Main file path**: Enter `src/app/main.py`
4. **App URL**: Choose your preferred subdomain

### Step 3: Set Environment Variables (Optional)
If you want to use GitHub integration, add these secrets:
- `GITHUB_TOKEN`: Your GitHub Personal Access Token
- `MAX_DEPTH`: Maximum crawl depth (default: 3)
- `TIMEOUT`: Request timeout in seconds (default: 30)

### Step 4: Deploy
Click "Deploy!" and wait for the build to complete.

## 🐳 Docker Deployment

### Local Docker
```bash
# Build the image
docker build -t jeffs-api-ripper .

# Run the container
docker run -p 8501:8501 jeffs-api-ripper
```

### Docker Compose
```bash
docker-compose up -d
```

### Cloud Docker Deployment
- **Google Cloud Run**
- **AWS ECS/Fargate**
- **Azure Container Instances**
- **Heroku Container Registry**

## ☁️ Other Cloud Platforms

### Heroku
```bash
# Create Procfile
echo "web: streamlit run src/app/main.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

### Railway
1. Connect your GitHub repository
2. Set build command: `pip install -r requirements-streamlit.txt`
3. Set start command: `streamlit run src/app/main.py --server.port=$PORT --server.address=0.0.0.0`

### Render
1. Create a new Web Service
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements-streamlit.txt`
4. Set start command: `streamlit run src/app/main.py --server.port=$PORT --server.address=0.0.0.0`

## 🔧 Environment Configuration

### Required Environment Variables
```bash
# For GitHub integration
GITHUB_TOKEN=your_github_token_here

# For extraction settings
MAX_DEPTH=3
TIMEOUT=30
LOG_LEVEL=INFO
```

### Optional Environment Variables
```bash
# For advanced features
SELENIUM_ENABLED=false
CHROME_DRIVER_PATH=/path/to/chromedriver
```

## 📱 Mobile Optimization

The app is already optimized for mobile devices with:
- Responsive design
- Touch-friendly interface
- Mobile-optimized layouts

## 🔒 Security Considerations

### For Production Deployment
1. **HTTPS**: Always use HTTPS in production
2. **Authentication**: Consider adding user authentication
3. **Rate Limiting**: Implement rate limiting for API calls
4. **Input Validation**: All inputs are validated
5. **CORS**: Configure CORS appropriately for your domain

### Environment Variables
- Never commit sensitive data to version control
- Use environment variables for configuration
- Rotate API keys regularly

## 📊 Monitoring and Logging

### Built-in Logging
- Application logs are automatically generated
- Log levels can be configured via environment variables
- Logs include extraction results and errors

### Health Checks
- Built-in health check endpoint: `/_stcore/health`
- Docker health checks configured
- Streamlit Cloud automatic health monitoring

## 🚀 Performance Optimization

### For High Traffic
1. **Caching**: Implement Redis caching for extraction results
2. **Async Processing**: Use background tasks for long extractions
3. **Load Balancing**: Deploy multiple instances behind a load balancer
4. **CDN**: Use CDN for static assets

### Memory Management
- Automatic cleanup of extraction sessions
- Configurable timeout limits
- Memory-efficient HTML parsing

## 🔄 Continuous Deployment

### GitHub Actions Integration
- Automatic testing on every push
- Docker image building and testing
- Release automation with version tags

### Streamlit Cloud Auto-Deploy
- Automatic deployment on main branch pushes
- Preview deployments for pull requests
- Easy rollback to previous versions

## 📞 Support and Troubleshooting

### Common Issues
1. **Build Failures**: Check requirements.txt and dependencies
2. **Runtime Errors**: Check environment variables and configuration
3. **Performance Issues**: Monitor memory usage and timeouts

### Getting Help
- Check the [GitHub Issues](https://github.com/jeff99jackson99/ripapidetail/issues)
- Review the [README.md](README.md)
- Contact: jeff99jackson99@gmail.com

---

**Happy Deploying! 🎉**
