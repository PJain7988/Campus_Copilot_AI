# Contributing to CampusCopilot AI

Thank you for contributing to **CampusCopilot AI**, the enterprise university information assistant.

## Development Workflow
1. Fork and clone the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Follow the modular structure:
   - Python code adheres to PEP 8 standards with full type annotations.
   - Frontend components use React 18 + TypeScript + Tailwind CSS.
4. Ensure zero hallucination rules: Any AI agent prompt update must enforce verified citations and deterministic abstention.
5. Run tests before submitting a PR:
   - Backend: `tests/test_rag_and_agents.py`
   - Frontend: `npm run build`
6. Commit using conventional commit format: `feat:`, `fix:`, `docs:`, `refactor:`, `test:`.
