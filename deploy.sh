#!/bin/bash

# Legal Strategy Infographics Platform - Deployment Script
# This script helps automate the deployment process to Vercel via GitHub

set -e

echo "🚀 Legal Strategy Infographics Platform - Deployment Script"
echo "=========================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if required files exist
check_files() {
    print_status "Checking required files..."
    
    local missing_files=()
    
    # Check for required files
    [[ ! -f "public/infographic.html" ]] && missing_files+=("public/infographic.html")
    [[ ! -f "legal_infographics/main.py" ]] && missing_files+=("legal_infographics/main.py")
    [[ ! -f "requirements.txt" ]] && missing_files+=("requirements.txt")
    [[ ! -f "vercel.json" ]] && missing_files+=("vercel.json")
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "Missing required files:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi
    
    print_success "All required files found"
}

# Check if git is initialized
check_git() {
    print_status "Checking Git repository..."
    
    if [[ ! -d ".git" ]]; then
        print_warning "Git repository not initialized. Initializing..."
        git init
        print_success "Git repository initialized"
    else
        print_success "Git repository already exists"
    fi
}

# Check if remote origin is set
check_remote() {
    print_status "Checking Git remote..."
    
    if ! git remote get-url origin >/dev/null 2>&1; then
        print_warning "No remote origin found"
        echo "Adding remote origin: https://github.com/Sarakael78/joy-srs.git"
        git remote add origin "https://github.com/Sarakael78/joy-srs.git"
        print_success "Remote origin added: https://github.com/Sarakael78/joy-srs.git"
    else
        current_remote=$(git remote get-url origin)
        print_success "Remote origin already configured: $current_remote"
    fi
}

# Create .env file if it doesn't exist
create_env() {
    print_status "Checking environment configuration..."
    
    if [[ ! -f ".env" ]]; then
        print_warning "No .env file found. Creating template..."
        
        cat > .env << 'EOF'
# Legal Strategy Infographics Platform - Environment Configuration

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
EOF
        
        print_success ".env file created"
        print_warning "Please update the SECRET_KEY and CORS_ORIGINS in .env file"
    else
        print_success ".env file already exists"
    fi
}

# Add files to git and commit
git_commit() {
    print_status "Adding files to Git..."
    
    # Add all files except .env
    git add .
    
    # Check if there are changes to commit
    if git diff --cached --quiet; then
        print_warning "No changes to commit"
    else
        git commit -m "Deploy: Legal Strategy Infographics Platform to Vercel"
        print_success "Changes committed to Git"
    fi
}

# Push to GitHub
push_to_github() {
    print_status "Pushing to GitHub..."
    
    # Get current branch
    current_branch=$(git branch --show-current)
    
    # Try to push to GitHub
    if git push -u origin "$current_branch"; then
        print_success "Successfully pushed to GitHub"
    else
        print_warning "Failed to push to GitHub - repository may not exist"
        print_status "Attempting to create GitHub repository..."
        
        # Check if GitHub CLI is available
        if ! command -v gh &> /dev/null; then
            print_error "GitHub CLI (gh) not found. Please install it or create the repository manually."
            echo "Install with: sudo apt install gh"
            exit 1
        fi
        
        # Check if user is authenticated
        if ! gh auth status &> /dev/null; then
            print_warning "GitHub CLI not authenticated. Please login first:"
            echo "  gh auth login"
            exit 1
        fi
        
        # Create the repository
        if gh repo create Sarakael78/joy-srs --public --source=. --remote=origin --push; then
            print_success "Successfully created and pushed to GitHub repository"
        else
            print_error "Failed to create GitHub repository"
            echo "Please create the repository manually at: https://github.com/Sarakael78/joy-srs"
            exit 1
        fi
    fi
}

# Display next steps
show_next_steps() {
    echo ""
    echo "🎉 Deployment preparation complete!"
    echo "=================================="
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. Go to https://vercel.com"
    echo "2. Sign in with your GitHub account"
    echo "3. Click 'New Project'"
    echo "4. Import your GitHub repository: https://github.com/Sarakael78/joy-srs"
    echo "5. Configure the following settings:"
    echo "   - Framework Preset: Other"
    echo "   - Build Command: pip install -r requirements.txt"
    echo "   - Output Directory: ."
    echo "   - Install Command: pip install -r requirements.txt"
    echo ""
    echo "6. Add environment variables in Vercel:"
    echo "   - APP_NAME=Legal Strategy Infographics"
    echo "   - DEBUG=false"
    echo "   - SECRET_KEY=your-super-secret-key-here-make-it-at-least-32-characters-long"
    echo "   - ALGORITHM=HS256"
    echo "   - ACCESS_TOKEN_EXPIRE_MINUTES=30"
    echo "   - REFRESH_TOKEN_EXPIRE_DAYS=7"
    echo "   - CORS_ORIGINS=[\"https://joy-srs.vercel.app\"]"
    echo "   - CORS_ALLOW_CREDENTIALS=true"
    echo "   - RATE_LIMIT_REQUESTS=100"
    echo "   - RATE_LIMIT_WINDOW=900"
    echo "   - LOG_LEVEL=INFO"
    echo ""
    echo "7. Click 'Deploy'"
    echo ""
       echo "Your application will be available at:"
   echo "  https://joy-srs.vercel.app"
    echo ""
    echo "For detailed instructions, see: docs/01-vercel-deployment-guide.md"
    echo ""
}

# Main execution
main() {
    echo ""
    print_status "Starting deployment preparation..."
    
    check_files
    check_git
    check_remote
    create_env
    git_commit
    push_to_github
    show_next_steps
}

# Run main function
main "$@"
