# Contributing to TrashMap

Thank you for your interest in contributing to TrashMap!

## How to Contribute

### Reporting Bugs
1. Check existing issues
2. Create new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details

### Suggesting Features
1. Open a GitHub issue
2. Describe the feature
3. Explain use cases
4. Consider implementation suggestions

### Pull Requests
1. Fork the repository
2. Create a feature branch
3. Make changes
4. Add tests if applicable
5. Submit PR with description

## Development Setup

```bash
git clone https://github.com/moltycollab/trashmap.git
cd trashmap

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest

# Run locally
uvicorn main:app --reload
```

## Code Style
- Follow PEP 8 for Python
- Use type hints
- Add docstrings
- Keep functions small and focused

## Commit Messages
- Use clear, descriptive messages
- Start with type: (feat, fix, docs, etc.)
- Example: `feat: Add nearby incidences endpoint`

## License
By contributing, you agree to license under MIT.
