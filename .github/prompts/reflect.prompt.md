---
agent: agent
---
# Self-Reflection Loop

Execute the self-improvement reflection loop for this coding session.

## Instructions

1. **Analyze the current session** - Review what was accomplished, any errors encountered, and how they were resolved

2. **Check existing memory** - Read `.github/Reflection/memory.json` and `.github/Reflection/reflections.md` to understand current learnings and avoid duplicates

3. **Create a new session entry** in `.github/Reflection/reflections.md` following the template:
   - Use the next sequential session ID (R001, R002, etc.)
   - Document the issue/task clearly
   - Log debug steps taken
   - Note the resolution and root cause
   - Extract key learnings (L001, L002, etc.)

4. **Update `.github/Reflection/memory.json`**:
   - Add new learnings to the `learnings` array
   - Update `stats.totalLearnings` and `stats.sessionsLogged`
   - Update `lastUpdated` timestamp
   - Add keywords to `searchIndex`
   - If a learning reinforces an existing rule, update that rule's `learningSources`

5. **Evaluate for high-impact rules** - If a learning is:
   - Likely to recur frequently
   - Caused significant debugging time
   - Applies broadly to the project
   
   Then add/update a rule in `.github/copilot-instructions.md`

## Output Format

Use emojis to indicate:
- 📝 New session logged
- 💡 New learning added (L00X)
- 🔄 Existing rule reinforced
- ⚡ New high-impact rule added (RULEXX)
- 📊 Stats updated

## Files to Update

| File | Action |
|------|--------|
| `.github/Reflection/reflections.md` | Add new session entry |
| `.github/Reflection/memory.json` | Add learnings, update stats and index |
| `.github/copilot-instructions.md` | Add rules (if high-impact) |

## Example Output

```
📝 Session R004 logged: "Dead Code Cleanup & Fast Mode Removal"

💡 L007: After deleting files, grep for references to the filename
   - Category: workflow, refactoring
   - Reinforces RULE002

💡 L008: Consolidate redundant tools into single well-designed one
   - Category: tooling, maintenance

📊 Stats: 8 learnings, 4 rules, 4 sessions logged
```
