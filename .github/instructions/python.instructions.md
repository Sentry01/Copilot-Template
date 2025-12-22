---
description: 'Python-specific code review and development guidelines'
applyTo: '**/*.py'
---

# Python Development Standards

Guidelines for Python code in this project.

## Naming Conventions

- Use `snake_case` for functions and variables
- Use `PascalCase` for class names
- Use `SCREAMING_SNAKE_CASE` for constants
- Prefix private variables with `_`

## Code Style

- Follow PEP 8 style guide
- Prefer f-strings over `.format()` or `%` formatting
- Use type hints for function signatures
- Limit lines to 88 characters (Black formatter default)
- Use list comprehensions for simple transformations

### Examples

```python
# ❌ BAD: Poor naming and style
def calc(x):
    r = []
    for i in x:
        r.append(i * 2)
    return r

# ✅ GOOD: Clear naming and Pythonic style
def double_values(items: list[int]) -> list[int]:
    return [item * 2 for item in items]
```

## Error Handling

- Catch specific exceptions, not bare `except:`
- Add context to error messages when raising
- Use custom exception classes for domain errors
- Never silently ignore exceptions

### Examples

```python
# ❌ BAD: Bare except, silent failure
try:
    process_command(cmd)
except:
    pass

# ✅ GOOD: Specific exception with context
try:
    process_command(cmd)
except ValidationError as e:
    logger.warning(f"Command validation failed for '{cmd}': {e}")
    raise CommandBlockedError(f"Blocked: {e}") from e
```

## Security (Critical)

- Use `shlex.split()` for parsing shell commands
- Never use `os.system()` or `subprocess.shell=True` with user input
- Validate all inputs against allowlists
- Don't log sensitive data (tokens, passwords, API keys)

### Security Examples

```python
# ❌ BAD: Command injection vulnerability
os.system(f"grep {user_pattern} file.txt")

# ✅ GOOD: Safe subprocess with argument list
subprocess.run(["grep", user_pattern, "file.txt"], check=True)

# ✅ BETTER: Validate against allowlist first (as in security.py)
if cmd not in ALLOWED_COMMANDS:
    return {"decision": "block", "reason": f"Command '{cmd}' not allowed"}
```

## Async Patterns

- Use `async`/`await` for I/O-bound operations
- Avoid mixing sync and async code
- Handle promise rejections with `try/except`
- Use `asyncio.gather()` for concurrent operations

## Testing

- Name test files as `test_*.py`
- Use pytest for testing
- Use descriptive test function names: `test_should_block_invalid_command`
- Follow Arrange-Act-Assert pattern

### Test Examples

```python
# ❌ BAD: Vague test name
def test1():
    assert validate("ls") == True

# ✅ GOOD: Descriptive name and structure
def test_should_allow_ls_command_in_allowlist():
    # Arrange
    command = "ls -la"
    
    # Act
    result = validate_command(command)
    
    # Assert
    assert result["allowed"] is True
```

## Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Document parameters, return values, and exceptions
- Explain the "why" not just the "what"

### Docstring Example

```python
def validate_command(command: str) -> dict[str, Any]:
    """
    Validate a shell command against the security allowlist.
    
    Uses shlex parsing to extract command names and validates
    each against ALLOWED_COMMANDS. Some commands require
    additional validation (pkill, chmod).
    
    Args:
        command: The full shell command string to validate.
        
    Returns:
        Empty dict if allowed, or {"decision": "block", "reason": "..."}.
        
    Raises:
        ValueError: If command cannot be parsed.
    """
```

## Project-Specific Patterns

### Security Hook Pattern
```python
async def security_hook(input_data, tool_use_id=None, context=None):
    """Return empty dict to allow, or block dict to deny."""
    if not relevant_tool(input_data):
        return {}  # Allow
    
    if not validate(input_data):
        return {"decision": "block", "reason": "..."}
    
    return {}  # Allow
```

### Command Extraction Pattern
```python
def extract_commands(command_string: str) -> list[str]:
    """Extract base command names using shlex, handling pipes and chains."""
    try:
        tokens = shlex.split(command_string)
    except ValueError:
        return []  # Fail safe - block unparseable commands
    # ... validation logic
```
