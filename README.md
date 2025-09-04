# Legal Strategy Infographics Platform

A secure, enterprise-grade platform for displaying legal strategy infographics to lawyers and clients with essential security features and compliance measures.

## 🔒 Security Features

- **Multi-Factor Authentication (MFA)**: TOTP-based authentication
- **Role-Based Access Control (RBAC)**: Granular permissions for lawyers, clients, and admins
- **Data Encryption**: AES-256 encryption for sensitive data at rest and in transit
- **Audit Logging**: Comprehensive activity tracking and compliance reporting
- **Session Management**: Secure session handling with automatic timeout
- **Input Validation**: Robust sanitization and validation of all inputs
- **Rate Limiting**: Protection against brute force and DDoS attacks
- **CORS Protection**: Configured cross-origin resource sharing policies
- **HTTPS Enforcement**: TLS 1.3 encryption for all communications

## 🏗️ Architecture

- **Backend**: FastAPI with async/await support
- **Database**: PostgreSQL with connection pooling
- **Cache**: Redis for session storage and caching
- **Task Queue**: Celery for background processing
- **Authentication**: JWT tokens with refresh mechanism
- **Frontend**: Modern React with TypeScript
- **Deployment**: Docker containers with Kubernetes support

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Poetry (dependency management)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/Sarakael78/joy-srs.git
   cd joy-srs
   ```

2. **Install dependencies**

   ```bash
   poetry install
   ```

3. **Set up environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Initialize database**

   ```bash
   poetry run alembic upgrade head
   ```

5. **Start the application**
   ```bash
   poetry run uvicorn legal_infographics.main:app --reload
   ```

## 📋 Environment Variables

Create a `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/legal_infographics
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-super-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# File Storage
STORAGE_BACKEND=s3  # or local
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_BUCKET_NAME=legal-infographics-bucket

# Monitoring
SENTRY_DSN=your-sentry-dsn
LOG_LEVEL=INFO
```

## 🔐 Authentication & Authorization

### User Roles

1. **Admin**: Full system access, user management, system configuration
2. **Lawyer**: Create, edit, and manage infographics, client access control
3. **Client**: View assigned infographics, limited access to case materials
4. **Viewer**: Read-only access to public infographics

### API Endpoints

- `POST /auth/login` - User authentication
- `POST /auth/refresh` - Token refresh
- `POST /auth/logout` - User logout
- `GET /auth/me` - Current user profile
- `POST /auth/mfa/enable` - Enable MFA
- `POST /auth/mfa/verify` - Verify MFA code

## 📊 Infographics Management

### Features

- **Interactive Charts**: D3.js powered visualizations
- **Real-time Updates**: WebSocket connections for live data
- **Export Options**: PDF, PNG, SVG formats
- **Version Control**: Track changes and revisions
- **Collaboration**: Multi-user editing with conflict resolution
- **Templates**: Pre-built legal strategy templates

### API Endpoints

- `GET /infographics` - List infographics
- `POST /infographics` - Create new infographic
- `GET /infographics/{id}` - Get infographic details
- `PUT /infographics/{id}` - Update infographic
- `DELETE /infographics/{id}` - Delete infographic
- `POST /infographics/{id}/export` - Export infographic

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=legal_infographics

# Run specific test categories
poetry run pytest -m unit
poetry run pytest -m integration
poetry run pytest -m e2e
```

## 🔧 Development

### Code Quality

```bash
# Format code
poetry run black .
poetry run isort .

# Lint code
poetry run flake8
poetry run mypy legal_infographics
```

### Database Migrations

```bash
# Create new migration
poetry run alembic revision --autogenerate -m "Description"

# Apply migrations
poetry run alembic upgrade head

# Rollback migration
poetry run alembic downgrade -1
```

## 🚀 Deployment Options

### Vercel Deployment (Recommended)

Deploy your infographic to Vercel with the security framework:

```bash
# Run the deployment script
./deploy.sh
```

This will:

- Check all required files
- Set up Git repository
- Push to GitHub
- Guide you through Vercel configuration

For detailed instructions, see [docs/01-vercel-deployment-guide.md](docs/01-vercel-deployment-guide.md)

### Docker Deployment

#### Build and run with Docker Compose

```bash
docker-compose up -d
```

#### Production deployment

```bash
# Build production image
docker build -t legal-infographics:latest .

# Run with proper environment
docker run -d \
  --name legal-infographics \
  -p 8000:8000 \
  --env-file .env \
  legal-infographics:latest
```

## 📈 Monitoring & Logging

- **Application Metrics**: Prometheus metrics endpoint
- **Health Checks**: `/health` endpoint for load balancers
- **Structured Logging**: JSON format with correlation IDs
- **Error Tracking**: Sentry integration for error monitoring
- **Performance Monitoring**: APM integration

## 🔒 Compliance

- **GDPR Compliance**: Data protection and privacy controls
- **SOC 2 Type II**: Security and availability controls
- **HIPAA**: Healthcare data protection (if applicable)
- **ISO 27001**: Information security management
- **Audit Trails**: Complete activity logging for compliance

## 📚 Documentation

- **API Documentation**: Auto-generated with OpenAPI/Swagger
- **User Guides**: Comprehensive documentation for all user roles
- **Developer Docs**: Architecture and development guidelines
- **Security Docs**: Security policies and procedures

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:

- Email: support@legal-infographics.com
- Documentation: https://docs.legal-infographics.com
- Issues: GitHub Issues page
