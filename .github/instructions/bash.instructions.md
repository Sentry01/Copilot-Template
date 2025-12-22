---
description: 'Bash/Shell script code review and development guidelines'
applyTo: '**/*.sh'
---

# Bash/Shell Script Standards

Guidelines for shell scripts in this project.

## Critical Rule: Bash Arithmetic

When performing a code review, verify bash arithmetic safety:

```bash
# ❌ BAD: ((x++)) exits with code 1 when x=0 (breaks set -e)
PASS=0
((PASS++))  # This fails when PASS is 0!

# ✅ GOOD: Always safe arithmetic
PASS=0
PASS=$((PASS + 1))
```

**Why:** `((0++))` evaluates to `((0))` which is falsy, returning exit code 1.

## Script Header

Every script should start with:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Brief description of what this script does
```

- `set -e`: Exit on any command failure
- `set -u`: Exit on undefined variables
- `set -o pipefail`: Exit on pipe failures

## Variable Naming

- Use `SCREAMING_SNAKE_CASE` for constants and environment variables
- Use `snake_case` for local variables
- Always quote variables: `"$VAR"` not `$VAR`

### Examples

```bash
# ❌ BAD: Unquoted variables, poor naming
x=$1
if [ -f $x ]; then
    cat $x
fi

# ✅ GOOD: Quoted variables, clear naming
input_file="$1"
if [[ -f "$input_file" ]]; then
    cat "$input_file"
fi
```

## Conditionals

- Prefer `[[ ]]` over `[ ]` for conditionals
- Use `(( ))` for arithmetic comparisons
- Always quote string variables

```bash
# ❌ BAD: Old-style test
if [ $count -gt 0 ]; then

# ✅ GOOD: Modern bash syntax
if (( count > 0 )); then

# For string comparisons
if [[ "$status" == "success" ]]; then
```

## Error Handling

- Check return codes for critical commands
- Provide meaningful error messages
- Use `trap` for cleanup on exit

```bash
# ❌ BAD: No error handling
rm -rf "$temp_dir"
cd "$work_dir"

# ✅ GOOD: Error handling with cleanup
cleanup() {
    rm -rf "$temp_dir"
}
trap cleanup EXIT

if ! cd "$work_dir"; then
    echo "ERROR: Cannot change to $work_dir" >&2
    exit 1
fi
```

## Command Substitution

- Use `$(command)` not backticks
- Quote command substitutions when assigning to variables

```bash
# ❌ BAD: Backticks
result=`ls -la`

# ✅ GOOD: Modern syntax
result="$(ls -la)"
```

## Security Considerations

When performing a code review, check for:

- No hardcoded secrets or credentials
- Validate user input before use
- Avoid `eval` with user input
- Use absolute paths for critical commands

```bash
# ❌ BAD: Dangerous eval
eval "$user_command"

# ❌ BAD: Path injection
$user_dir/script.sh

# ✅ GOOD: Validate and use absolute paths
if [[ "$user_dir" =~ ^[a-zA-Z0-9_/.-]+$ ]]; then
    /usr/bin/env bash "$validated_path/script.sh"
fi
```

## Functions

- Use `function_name() { }` syntax
- Declare local variables with `local`
- Return meaningful exit codes

```bash
# ❌ BAD: No local variables, implicit return
process_file() {
    result=$(cat "$1")
    echo "$result"
}

# ✅ GOOD: Local variables, explicit return
process_file() {
    local input_file="$1"
    local result
    
    if ! result="$(cat "$input_file" 2>/dev/null)"; then
        return 1
    fi
    
    echo "$result"
    return 0
}
```

## Output and Logging

- Use `>&2` for error messages
- Use colored output sparingly
- Provide progress feedback for long operations

```bash
# ❌ BAD: Errors to stdout
echo "Error: File not found"

# ✅ GOOD: Errors to stderr with prefix
echo "ERROR: File not found: $file" >&2

# Info messages
echo "INFO: Processing $count files..."
```

## Project-Specific Rules

### Allowed Commands
Scripts in this project should only use commands from the security allowlist:
`ls`, `cat`, `head`, `tail`, `wc`, `grep`, `cp`, `mkdir`, `chmod`, `pwd`, `npm`, `node`, `npx`, `git`, `ps`, `lsof`, `sleep`, `pkill`

### Check Prerequisites Pattern
```bash
check_command() {
    if ! command -v "$1" &> /dev/null; then
        echo "ERROR: $1 is required but not installed" >&2
        return 1
    fi
    echo "✓ $1 found"
    return 0
}
```
