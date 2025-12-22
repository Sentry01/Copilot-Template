# Global Self-Reflection System

A cross-project learning system that captures debugging sessions and builds institutional knowledge.

## Overview

This global reflection system persists learnings across ALL projects. When you solve a difficult problem in one project, the learning is available for future sessions in any project.

## File Structure

```
~/.copilot/Reflection/
├── README.md           # This file
├── reflections.md      # Chronological debug log (all projects)
├── memory.json         # Indexed learnings database
└── auto_reflect.py     # Automatic reflection script
```

## Usage

### 1. Check Memory Before Debugging

```bash
# Search for keywords
grep -i "bash arithmetic" ~/.copilot/Reflection/memory.json

# View recent sessions
tail -50 ~/.copilot/Reflection/reflections.md
```

### 2. Log Debugging Sessions

Add to reflections.md after resolving significant issues.

### 3. Update Memory Database

Extract learnings to memory.json for future reference.

## Quick Commands

Ask Copilot to:
- "Check your reflection memory for similar issues"
- "Log this debugging session to reflections"
- "What have you learned about [topic]?"

## Integration

**Global vs Local:**
- **Global** (`~/.copilot/Reflection/`): Cross-project learnings, general patterns
- **Local** (`.github/Reflection/`): Project-specific patterns, team knowledge

---

