#!/bin/bash
# Quick Start Script - AI Hiring Assistant
# Supports: Local, Docker, and Cloud deployments

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║     🤖 AI Hiring Assistant - Quick Start               ║"
    echo "║     CrewAI Multi-Agent System v0.1                     ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

# Check dependencies
check_dependencies() {
    print_info "Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed!"
        exit 1
    fi
    
    if ! command -v git &> /dev/null; then
        print_error "Git is not installed!"
        exit 1
    fi
    
    print_success "Dependencies found!"
}

# Setup environment
setup_env() {
    print_info "Setting up environment..."
    
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            print_success "Created .env from template"
            print_warning "⚠️  Remember to update OPENAI_API_KEY in .env"
        fi
    else
        print_success ".env already exists"
    fi
    
    # Check if OPENAI_API_KEY is set
    if ! grep -q "OPENAI_API_KEY=sk-" .env; then
        print_warning "⚠️  OPENAI_API_KEY not properly configured in .env"
        echo "Get your key from: https://platform.openai.com/api-keys"
    fi
}

# Deploy locally
deploy_local() {
    print_info "Deploying locally..."
    
    # Create virtual environment
    if [ ! -d venv ]; then
        print_info "Creating virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi
    
    # Activate venv
    source venv/bin/activate || . venv/Scripts/activate 2>/dev/null || true
    
    # Install dependencies
    print_info "Installing dependencies..."
    pip install -q -r requirements.txt
    print_success "Dependencies installed"
    
    # Export variables from .env
    export $(cat .env | grep -v '#' | xargs)
    
    print_success "✅ Ready to start!"
    echo ""
    echo -e "${BLUE}📝 To start the API server, run:${NC}"
    echo "   cd $(pwd)"
    echo "   source venv/bin/activate"
    echo "   python -m src.api.main"
    echo ""
    echo -e "${BLUE}📊 To start Streamlit UI (in another terminal), run:${NC}"
    echo "   cd $(pwd)"
    echo "   source venv/bin/activate"
    echo "   streamlit run src/ui/streamlit_app.py"
    echo ""
    echo -e "${BLUE}🌐 Access URLs:${NC}"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
    echo "   UI: http://localhost:8501"
}

# Deploy with Docker
deploy_docker() {
    print_info "Deploying with Docker..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed!"
        print_info "Install Docker from: https://www.docker.com/products/docker-desktop"
        exit 1
    fi
    
    # Build images
    print_info "Building Docker images..."
    docker-compose build -q
    print_success "Docker images built"
    
    # Start services
    print_info "Starting services..."
    docker-compose up -d
    print_success "Services started"
    
    # Wait for services to be ready
    print_info "Waiting for services to be ready..."
    sleep 3
    
    # Check health
    if curl -s http://localhost:8000/health > /dev/null; then
        print_success "API is healthy!"
    else
        print_warning "API health check failed, check logs with: docker-compose logs api"
    fi
    
    print_success "✅ Docker deployment complete!"
    echo ""
    echo -e "${BLUE}📊 Access URLs:${NC}"
    echo "   API: http://localhost:8000"
    echo "   Docs: http://localhost:8000/docs"
    echo "   UI: http://localhost:8501"
    echo ""
    echo -e "${BLUE}📝 Useful commands:${NC}"
    echo "   View logs: docker-compose logs -f api"
    echo "   Stop services: docker-compose down"
    echo "   Remove volumes: docker-compose down -v"
}

# Main menu
show_menu() {
    echo ""
    echo -e "${BLUE}Choose deployment method:${NC}"
    echo "1) Local (Python + venv)"
    echo "2) Docker (Recommended)"
    echo "3) Cloud (See DEPLOYMENT.md)"
    echo "4) Test API (Quick verification)"
    echo "5) Exit"
    echo ""
    read -p "Enter choice [1-5]: " choice
}

# Test API
test_api() {
    print_info "Testing API..."
    
    if ! curl -s http://localhost:8000/health > /dev/null; then
        print_error "API is not running!"
        print_info "Start API first: python -m src.api.main"
        return 1
    fi
    
    print_success "API is healthy!"
    
    # Test job analysis
    print_info "Testing job analysis..."
    response=$(curl -s -X POST http://localhost:8000/api/v1/jobs/analyze \
      -H "Content-Type: application/json" \
      -d '{
        "job_id": "TEST-001",
        "job_title": "Senior Python Developer",
        "job_text": "We need a Python developer with 5+ years experience in Django, FastAPI, and AWS"
      }')
    
    if echo "$response" | grep -q "required_skills"; then
        print_success "Job analysis working!"
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    else
        print_error "Job analysis failed"
        echo "$response"
    fi
}

# Main script
main() {
    print_banner
    check_dependencies
    setup_env
    
    while true; do
        show_menu
        case $choice in
            1)
                deploy_local
                break
                ;;
            2)
                deploy_docker
                break
                ;;
            3)
                print_info "See DEPLOYMENT.md for cloud options:"
                echo "   - Heroku"
                echo "   - Railway"
                echo "   - Render"
                echo "   - AWS EC2"
                echo "   - DigitalOcean"
                echo "   - Google Cloud Run"
                ;;
            4)
                test_api
                ;;
            5)
                print_info "Goodbye! 👋"
                exit 0
                ;;
            *)
                print_error "Invalid choice!"
                ;;
        esac
    done
    
    echo ""
    print_success "🚀 Deployment complete!"
}

# Run main
main "$@"
