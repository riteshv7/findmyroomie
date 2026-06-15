# FindMyRoomie — Agent Instructions

This project uses [agent-skills](https://github.com/addyosmani/agent-skills) for structured engineering workflows.

## Skills

All 24 skills are available under `.agent-skills/`. The agent should automatically apply the right skill based on the current task:

| Task | Skill to apply |
|------|---------------|
| Underspecified ask | `interview-me` |
| Rough idea to explore | `idea-refine` |
| New feature / project | `spec-driven-development` |
| Break work into tasks | `planning-and-task-breakdown` |
| Writing code | `incremental-implementation` |
| Frontend / UI work | `frontend-ui-engineering` |
| API design | `api-and-interface-design` |
| Writing tests | `test-driven-development` |
| Code review | `code-review-and-quality` |
| Simplifying code | `code-simplification` |
| Debugging | `debugging-and-error-recovery` |
| Deploying / shipping | `shipping-and-launch` |
| Security hardening | `security-and-hardening` |
| Performance work | `performance-optimization` |
| CI/CD setup | `ci-cd-and-automation` |
| Documentation | `documentation-and-adrs` |
| Git workflow | `git-workflow-and-versioning` |
| Observability | `observability-and-instrumentation` |
| Migration/deprecation | `deprecation-and-migration` |
| Browser testing | `browser-testing-with-devtools` |
| Context building | `context-engineering` |
| Doc-verified code | `source-driven-development` |
| High-stakes unfamiliar code | `doubt-driven-development` |

## Slash Commands

Use these commands during development:

- `/spec` — Write a structured spec before any code
- `/plan` — Break work into small, verifiable tasks  
- `/build` — Implement the next task incrementally
- `/test` — Run TDD workflow (red → green → refactor)
- `/review` — Five-axis code review
- `/code-simplify` — Reduce complexity without changing behavior
- `/ship` — Pre-launch checklist

## Project Context

- **Stack**: Python (app.py), see readme.md for details
- **Skills directory**: `.agent-skills/`
