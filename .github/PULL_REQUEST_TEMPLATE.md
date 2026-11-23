## Pull Request Checklist

### Description
Explain the changes made in this pull request and link relevant issue numbers.

### Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Documentation update
- [ ] Performance improvement / Refactor
- [ ] Security fix

### AI & RAG Evaluation Checklist
- [ ] Groundedness verified: Responses are supported solely by retrieved university chunks.
- [ ] Citations verified: Every factual claim links to document title and verified page number.
- [ ] Abstention validated: Out-of-scope or unverified inquiries trigger standard abstention template.
- [ ] Guardrails verified: Prompt injection protections tested.

### Code & Testing
- [ ] Backend tests passing (`pytest` / test runner).
- [ ] Frontend builds without TypeScript or bundling errors (`npm run build`).
- [ ] No hardcoded secrets or API keys introduced.
