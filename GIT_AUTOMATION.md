# 🔄 Git Automation & Continuous Deployment Guide

This guide explains how to use the automated commit and deployment workflows set up for your AI Hiring Assistant project.

## 📋 Quick Start

### Option 1: Use the Batch Script (Windows)
```bash
# Simple auto-commit
commit.bat

# Auto-commit with custom message
commit.bat "feat: Add new feature"

# Auto-commit and push to GitHub
commit.bat "feat: Add new feature" --push
```

### Option 2: Use the Python Script
```bash
# Simple auto-commit
python git_auto_commit.py

# Auto-commit with custom message
python git_auto_commit.py --message "feat: Add new feature"

# Auto-commit and push to GitHub
python git_auto_commit.py --message "feat: Add new feature" --push

# Push to specific branch
python git_auto_commit.py --message "feat: Add new feature" --push --branch develop
```

### Option 3: Use GitHub Actions (Automatic)
Once you push to the `main` branch, GitHub Actions will automatically:
1. ✅ Run tests on Python 3.10 and 3.11
2. ✅ Lint your code with flake8
3. ✅ Build Docker images
4. ✅ Push Docker images to GitHub Container Registry (GHCR)

## 🔧 Configuration

### Enable GitHub Actions
1. Go to your repository: https://github.com/Annaa74/Crew-Ai-Multi-agent-system
2. Click on **Settings** → **Actions** → **General**
3. Enable "Allow all actions and reusable workflows"

### Docker Deployment (Optional)
If you want to push Docker images to GHCR:
1. Docker images will be automatically built and pushed to:
   - `ghcr.io/Annaa74/Crew-Ai-Multi-agent-system-api:latest`
   - `ghcr.io/Annaa74/Crew-Ai-Multi-agent-system-ui:latest`

## 📊 Workflow Summary

### 1. **Auto-Commit Workflow** (`.github/workflows/auto-commit.yml`)
- **Triggers**: Pushes to `main` with changes in `src/`, docs, Docker files
- **Actions**: 
  - Stages and commits changes
  - Pushes to remote repository
  - Logs commit details

### 2. **Tests & Build Workflow** (`.github/workflows/tests.yml`)
- **Triggers**: Push or Pull Request to `main`
- **Actions**:
  - Tests on Python 3.10 and 3.11
  - Code quality checks with flake8
  - Verifies all imports work correctly
  - Creates test status badges

### 3. **Docker Build & Push Workflow** (`.github/workflows/docker.yml`)
- **Triggers**: Push to `main` with code changes
- **Actions**:
  - Builds API Docker image
  - Builds Streamlit UI Docker image
  - Pushes to GitHub Container Registry (GHCR)
  - Caches layers for faster builds

## 📝 Commit Message Conventions

The system uses conventional commits for better readability:

```
feat:   Add new feature
fix:    Fix a bug
docs:   Documentation changes
style:  Code style changes (formatting)
refactor: Refactor code without changing functionality
perf:   Performance improvements
test:   Add or modify tests
ci:     CI/CD configuration changes
chore:  Build, dependency updates, other maintenance
```

### Examples:
```bash
commit.bat "feat: Add email notification system" --push
commit.bat "fix: Correct skill matching algorithm" --push
commit.bat "docs: Update API documentation" --push
commit.bat "perf: Optimize vector database queries" --push
```

## 🚀 Deployment Pipeline

### Local Development Workflow
1. Make code changes in `src/`
2. Run tests locally: `pytest tests/ -v`
3. Commit: `commit.bat "description" --push`
4. GitHub Actions will automatically:
   - Run CI/CD tests
   - Build Docker images
   - Push to container registry

### Production Deployment
```bash
# Direct push to main triggers automatic deployment
git push origin main

# Docker images available at:
# ghcr.io/Annaa74/Crew-Ai-Multi-agent-system-api:latest
# ghcr.io/Annaa74/Crew-Ai-Multi-agent-system-ui:latest
```

## 📊 Monitoring Workflows

### View Workflow Status
1. Go to: https://github.com/Annaa74/Crew-Ai-Multi-agent-system/actions
2. Select a workflow to see:
   - ✅ Passed jobs
   - ❌ Failed jobs
   - ⏳ Running jobs
   - Detailed logs

### Check Test Results
```bash
# Local testing
pytest tests/ -v
pytest tests/ --cov=src

# View in GitHub
Actions → Tests & Build → [Latest Run]
```

## 🔐 Security Best Practices

### Environment Variables
- ✅ Never commit `.env` file
- ✅ Use GitHub Secrets for sensitive data
- ✅ Rotate API keys regularly

### Setting Up GitHub Secrets
1. Go to Repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DOCKER_USERNAME`: Docker Hub username (optional)
   - `DOCKER_PASSWORD`: Docker Hub token (optional)

### Update Workflow to Use Secrets
```yaml
- name: Build Docker image
  env:
    OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  run: docker build -t hiring-api .
```

## 🐛 Troubleshooting

### Workflow Not Triggering
- Check file paths in workflow `paths:` section
- Ensure `.github/workflows/*.yml` files exist
- Go to Actions tab and enable workflows

### Docker Build Fails
```bash
# Test locally first
docker build -t hiring-api -f Dockerfile .
docker build -t hiring-ui -f Dockerfile.streamlit .
```

### Push Fails Due to Authentication
```bash
# Configure git credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Use personal access token if prompted
# Or set up SSH keys for GitHub
```

### Tests Failing
```bash
# Run tests locally
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install pytest
pytest tests/ -v
```

## 📈 Metrics & Monitoring

### Key Performance Indicators
Track these metrics in your GitHub Actions workflows:

```yaml
- Build time: Should be < 2 minutes
- Test coverage: Target 85%+
- Successful build rate: Target 100%
- Deployment frequency: Every commit to main
```

### View Metrics
1. Go to Insights → Actions
2. Monitor:
   - Workflow run duration
   - Success rate
   - Most common failures

## 🎯 Next Steps

1. **Enable Branch Protection**: Require tests to pass before merging
2. **Add Code Review**: Set up pull request reviews before main branch
3. **Keep Dependencies Updated**: Use Dependabot for automatic updates
4. **Monitor Costs**: Check GitHub Actions usage under Settings → Billing

## 📞 Support

For issues with workflows:
1. Check GitHub Actions logs: https://github.com/Annaa74/Crew-Ai-Multi-agent-system/actions
2. Review workflow files in `.github/workflows/`
3. Check commit history for patterns

---

## 🔗 Useful Links

- **Repository**: https://github.com/Annaa74/Crew-Ai-Multi-agent-system
- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Conventional Commits**: https://www.conventionalcommits.org/
- **Docker Best Practices**: https://docs.docker.com/develop/design/dockerfile_best-practices/

Made with ❤️ | Auto-commit v1.0
