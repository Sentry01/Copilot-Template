---
description: 'Generic code review instructions'
applyTo: '**'
excludeAgent: ["coding-agent"]
---

# Code Review Instructions

When performing a code review, follow these guidelines.

## Review Priorities

When performing a code review, prioritize issues in this order:

### 🔴 CRITICAL (Block merge)
- Security vulnerabilities, exposed secrets, authentication issues
- Logic errors, data corruption risks, race conditions
- Command injection or shell escape issues (critical for this project)

### 🟡 IMPORTANT (Requires discussion)
- Code quality violations (SOLID principles, excessive duplication)
- Missing tests for critical paths
- Performance bottlenecks (N+1 queries, memory leaks)

### 🟢 SUGGESTION (Non-blocking)
- Readability improvements, naming, simplification
- Minor best practice deviations
- Documentation gaps

## General Review Principles

When performing a code review:

1. Be specific - Reference exact lines and provide concrete examples
2. Explain WHY something is an issue and the potential impact
3. Suggest solutions with corrected code when applicable
4. Recognize good practices - Acknowledge well-written code
5. Be pragmatic - Not every suggestion needs immediate fix

## Security Review (Critical for this project)

When performing a code review, check for security issues:

- No passwords, API keys, tokens, or PII in code or logs
- All user inputs are validated and sanitized
- Shell commands use allowlist validation (see `security.py`)
- No command injection vulnerabilities
- Proper error handling that doesn't leak sensitive info

### Security Examples

```python
# ❌ BAD: Direct shell execution without validation
os.system(f"ls {user_input}")

# ✅ GOOD: Use allowlist and shlex parsing
if cmd in ALLOWED_COMMANDS:
    tokens = shlex.split(command)
    # validate tokens
```

## Code Quality Standards

When performing a code review, check for:

- Descriptive names for variables, functions, and classes
- Single Responsibility Principle - each function does one thing
- No code duplication (DRY)
- Functions should be focused (ideally < 30 lines)
- Avoid deeply nested code (max 3-4 levels)
- Use constants instead of magic numbers/strings

## Error Handling

When performing a code review, verify error handling:

- Proper error handling at appropriate levels
- Meaningful error messages
- No silent failures or ignored exceptions
- Fail fast - validate inputs early
- Use appropriate exception types

### Error Handling Examples

```python
# ❌ BAD: Silent failure
try:
    process_command(cmd)
except:
    pass

# ✅ GOOD: Specific exception handling with logging
try:
    process_command(cmd)
except ValidationError as e:
    logger.warning(f"Command validation failed: {e}")
    return {"decision": "block", "reason": str(e)}
```

## Testing Standards

When performing a code review, verify test quality:

- Critical paths and new functionality must have tests
- Test names describe what is being tested
- Clear Arrange-Act-Assert pattern
- Tests should not depend on each other
- Test edge cases and boundary conditions

## Documentation Standards

When performing a code review, check documentation:

- Public APIs must be documented (purpose, parameters, returns)
- Complex logic should have explanatory comments
- Update README when adding features or changing setup
- Document the "why" not just the "what"

## Comment Format

When performing a code review, use this format:

```markdown
**[PRIORITY] Category: Brief title**

Description of the issue.

**Why this matters:**
Impact explanation.

**Suggested fix:**
[code example]
```

## Project-Specific Rules

Add your project-specific code review rules here. Examples:

- Entry points and core architecture
- Security-critical files and patterns
- Technology-specific guidelines
- Common pitfalls in your codebase
