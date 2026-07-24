# Contributing to The Great GSAPI

First, thank you for your interest in contributing! The Great GSAPI is an open-source project and we welcome contributions from the community.

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/0/code_of_conduct/). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating a bug report, please check the [issue list](https://github.com/qv4rk/TheGreatGSAPI/issues) — your bug may have already been reported.

**To report a bug:**

1. Use a clear, descriptive title
2. Describe the exact steps which reproduce the problem
3. Provide specific examples to demonstrate those steps
4. Explain the behavior you observed and why it's a problem
5. Include screenshots if applicable
6. Specify your environment (OS, Python version, etc.)

### Suggesting Features & Enhancements

Feature suggestions are tracked as GitHub issues. When creating a feature request:

1. Use a clear, descriptive title (e.g., "Add support for EEZ boundary layer")
2. Describe the suggested enhancement step-by-step
3. Explain why this enhancement would be useful
4. Reference any relevant data sources or academic papers

### Pull Requests

**For code contributions:**

1. **Fork the repository** and create your branch from `main`
   ```bash
   git checkout -b feature/my-feature-name
   ```

2. **Set up development environment**
   ```bash
   docker-compose up -d
   cd backend && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation if needed

4. **Test your changes**
   ```bash
   # Backend tests
   cd backend
   pytest

   # Frontend tests
   cd ../frontend
   npm test
   ```

5. **Commit with clear messages**
   ```bash
   git commit -m "Add: description of changes"
   ```
   Use prefixes:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Refactor:` for code improvements
   - `Docs:` for documentation updates
   - `Test:` for test additions

6. **Push to your fork**
   ```bash
   git push origin feature/my-feature-name
   ```

7. **Create a Pull Request** with a clear description

## Development Workflow

### Project Structure

```
TheGreatGSAPI/
├── backend/           # FastAPI application
│   ├── app/          # Application code
│   ├── etl/          # Data pipeline scripts
│   ├── migrations/   # Database migrations
│   ├── tests/        # Pytest suite
│   └── requirements.txt
├── frontend/         # React application
│   ├── src/          # React components
│   ├── tests/        # Jest tests
│   └── package.json
└── data/             # Local data storage (git-ignored)
```

### Backend Development

**Stack:** FastAPI, PostGIS, GeoPandas, SQLAlchemy

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

**Stack:** React, Deck.gl, D3.js, MapLibre GL

```bash
cd frontend
npm install
npm run dev
```

### Adding a New Data Source

1. Create ETL script in `backend/etl/sources/`
2. Define schema in `backend/app/models/`
3. Add API endpoint in `backend/app/routes/`
4. Update [DATA_SOURCES.md](DATA_SOURCES.md) with attribution
5. Test with `pytest`

## Code Style Guidelines

### Python (Backend)

- Follow [PEP 8](https://pep8.org/)
- Use type hints
- Maximum line length: 100 characters
- Use `black` for formatting

```bash
# Format code
black backend/

# Check style
flake8 backend/
```

### JavaScript/React (Frontend)

- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use `eslint` and `prettier`
- Components use functional components with hooks

```bash
# Format code
npm run format

# Check style
npm run lint
```

## Documentation

- Update README.md for user-facing changes
- Add docstrings to Python functions (Google-style)
- Add JSDoc comments to complex React components
- Update [DATA_SOURCES.md](DATA_SOURCES.md) when adding data sources

## Testing Requirements

- **Backend:** Minimum 80% code coverage with pytest
- **Frontend:** Tests for new components with Jest/React Testing Library
- **ETL:** Data validation tests for new sources

```bash
# Run tests
cd backend && pytest --cov=app
cd ../frontend && npm test -- --coverage
```

## Review Process

1. PR review by maintainers (typically within 1 week)
2. Automated tests must pass (CI/CD pipeline)
3. Code review feedback addressed
4. At least one approval required before merge
5. Merge to `main` branch

## Attribution & Licensing

By contributing to The Great GSAPI, you agree that your contributions will be licensed under the MIT License. See [LICENSE](LICENSE) for details.

When using data sources:
- Always respect original licenses
- Provide proper attribution
- Update [DATA_SOURCES.md](DATA_SOURCES.md) accordingly

## Questions?

- **GitHub Issues** — For bugs and feature requests
- **Discussions** — For questions and ideas
- **Email** — Contact maintainers for sensitive issues

## Additional Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [How to Write a Git Commit Message](https://chris.beams.io/posts/git-commit/)
- [Contributor Covenant](https://www.contributor-covenant.org/)

---

**Thank you for making The Great GSAPI better!** 🙏
