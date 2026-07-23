# Contributing to Monarch Art Vault

Thank you for your interest in contributing! 🦋

## How to Contribute

### Bug Reports

1. Check existing [issues](https://github.com/diamitani/monarch-art-vault/issues)
2. Open a new issue with:
   - Clear title
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (Python version, OS)

### Feature Requests

Open an issue with:
- Use case description
- Proposed solution (if any)
- Whether you'd like to implement it

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `python -m pytest tests/`
5. Run validation: `python scripts/validate_package.py`
6. Commit with clear message: `git commit -m 'Add feature X'`
7. Push: `git push origin feature/my-feature`
8. Open a Pull Request

### Code Style

- Python: Follow PEP 8
- Use type hints where practical
- Add docstrings to public functions
- Keep functions focused and testable

### Testing

- Add tests for new features
- Ensure existing tests pass
- Test with both minimal and full dependencies

### Documentation

- Update README for user-facing changes
- Update SKILL.md for agent behavior changes
- Add examples for new features

## Development Setup

```bash
git clone https://github.com/diamitani/monarch-art-vault.git
cd monarch-art-vault
pip install -r scripts/requirements-optional.txt
python -m pytest tests/
```

## Questions?

Open a [Discussion](https://github.com/diamitani/monarch-art-vault/discussions) or reach out to [@diamitani](https://github.com/diamitani).

---

By contributing, you agree that your contributions will be licensed under the MIT License.
