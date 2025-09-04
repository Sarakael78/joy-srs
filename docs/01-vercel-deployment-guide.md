# Vercel Deployment Guide for Legal Strategy Infographics Platform

## Overview

This guide explains how to deploy the Legal Strategy Infographics Platform on Vercel using GitHub integration, with the security framework from the boilerplate.

## Prerequisites

- GitHub account
- Vercel account
- Python 3.11+ knowledge
- Basic understanding of FastAPI

## Step 1: Prepare Your Repository

### 1.1 Repository Structure

Ensure your repository has the following structure:

```
joy-srs/
├── legal_infographics/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── infographics.py
│   │   ├── cases.py
│   │   ├── users.py
│   │   └── audit.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── rate_limit.py
│   │   ├── audit.py
│   │   └── security.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── case.py
│   │   └── infographic.py
│   └── utils/
│       ├── __init__.py
│       ├── security.py
│       └── logging.py
├── public/
│   └── infographic.html
├── requirements.txt
├── vercel.json
├── pyproject.toml
└── README.md
```

### 1.2 Environment Variables

Create a `.env` file with the following variables:

```env
# Application Settings
APP_NAME="Legal Strategy Infographics"
DEBUG=false
HOST="0.0.0.0"
PORT=8000

# Security Configuration
SECRET_KEY="your-super-secret-key-here-make-it-at-least-32-characters-long"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS Settings
CORS_ORIGINS=["https://joy-srs.vercel.app"]
CORS_ALLOW_CREDENTIALS=true

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=900

# Monitoring
LOG_LEVEL="INFO"
```

## Step 2: GitHub Repository Setup

### 2.1 Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: Legal Strategy Infographics Platform"

# Add remote origin (replace with your GitHub repo URL)
git remote add origin https://github.com/Sarakael78/joy-srs.git

# Push to GitHub
git push -u origin main
```

### 2.2 Repository Settings

1. Go to your GitHub repository settings
2. Enable GitHub Actions (if needed)
3. Set up branch protection rules (recommended)

## Step 3: Vercel Deployment

### 3.1 Connect to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign in with your GitHub account
3. Click "New Project"
4. Import your GitHub repository: https://github.com/Sarakael78/joy-srs

### 3.2 Configure Project Settings

#### Build Settings:

- **Framework Preset**: Other
- **Build Command**: `pip install -r requirements.txt`
- **Output Directory**: (leave empty - Vercel will auto-detect from vercel.json)
- **Install Command**: `pip install -r requirements.txt`

**Note**: The `vercel.json` file already contains the correct configuration for FastAPI deployment.

#### Environment Variables:

Add the following environment variables in Vercel:

```
APP_NAME=Legal Strategy Infographics
DEBUG=false
SECRET_KEY=your-super-secret-key-here-make-it-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=["https://your-vercel-domain.vercel.app"]
CORS_ALLOW_CREDENTIALS=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=900
LOG_LEVEL=INFO
```

### 3.3 Deploy

1. Click "Deploy"
2. Wait for the build to complete
3. Your application will be available at `https://joy-srs.vercel.app`

## Step 4: Security Framework Integration

### 4.1 Authentication Endpoints

The platform includes the following secure endpoints:

- `POST /auth/login` - User authentication
- `GET /auth/me` - Get current user
- `GET /infographics/` - Protected infographic access
- `GET /infographics/public` - Public infographic access

### 4.2 Security Features

The deployed application includes:

- **Rate Limiting**: 100 requests per 15 minutes per IP
- **CORS Protection**: Configured for your Vercel domain
- **Security Headers**: XSS protection, content type options, etc.
- **Audit Logging**: All requests are logged
- **JWT Authentication**: Secure token-based auth

### 4.3 Accessing the Infographic

#### Public Access:

```
https://joy-srs.vercel.app/infographics/public
```

#### Protected Access (requires authentication):

```
https://joy-srs.vercel.app/infographics/
```

#### Root Access:

```
https://joy-srs.vercel.app/
```

## Step 5: Testing the Deployment

### 5.1 Health Check

Test the health endpoint:

```bash
curl https://joy-srs.vercel.app/health
```

Expected response:

```json
{
  "status": "healthy",
  "version": "0.1.0",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### 5.2 Infographic Access

1. Open your browser
2. Navigate to `https://your-project-name.vercel.app/infographics/public`
3. Verify the infographic loads correctly

### 5.3 API Documentation

Access the API documentation at:

```
https://joy-srs.vercel.app/docs
```

## Step 6: Monitoring and Maintenance

### 6.1 Vercel Dashboard

- Monitor deployment status
- View function logs
- Check performance metrics
- Set up custom domains

### 6.2 Environment Variables

Update environment variables through the Vercel dashboard:

1. Go to your project settings
2. Navigate to "Environment Variables"
3. Add or modify variables as needed

### 6.3 Automatic Deployments

- Every push to the main branch triggers a new deployment
- Preview deployments are created for pull requests
- Rollback to previous deployments if needed

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check `requirements.txt` for missing dependencies
   - Verify Python version compatibility
   - Check build logs in Vercel dashboard

2. **Runtime Errors**:
   - Check function logs in Vercel dashboard
   - Verify environment variables are set correctly
   - Test locally before deploying

3. **CORS Issues**:
   - Update `CORS_ORIGINS` to include your domain
   - Check browser console for CORS errors

4. **File Not Found**:
   - Ensure `public/infographic.html` exists
   - Check file permissions
   - Verify file path in code

### Support

- Vercel Documentation: [vercel.com/docs](https://vercel.com/docs)
- FastAPI Documentation: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- GitHub Issues: Create issues in your repository

## Security Best Practices

1. **Environment Variables**: Never commit sensitive data to Git
2. **Secret Management**: Use Vercel's environment variables for secrets
3. **HTTPS**: Vercel provides automatic HTTPS
4. **Rate Limiting**: Configure appropriate rate limits
5. **Monitoring**: Set up alerts for unusual activity
6. **Updates**: Keep dependencies updated regularly

## Next Steps

1. Set up custom domain (optional)
2. Configure monitoring and alerts
3. Set up CI/CD pipeline
4. Implement additional security features
5. Add database integration (if needed)
6. Set up backup and recovery procedures
