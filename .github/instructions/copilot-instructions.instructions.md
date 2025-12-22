# AI CODING ASSISTANT DIRECTIVES

Always refer to your skills at .github/skills/ before any operation to consult on the best approach.
Use Sequential Thinking MCP to think through problems, debugging and planning step by step 

## GitHub Integration
- Use Github MCP server (Model Context Protocol) for GitHub interactions (issues, PRs, repos)
- When creating/updating issues: include clear title + concise description
- For issue/PR listings: provide direct links with brief descriptions
- Verify remote repo connections before making changes and use the existing repo instead of creating new one unless specified

## Environment & Package Management
- when needing to install or operate on any packages use Octocode MCP to get the latest info about the package first.
- Use the info from Octocode MCP for all package operations (install, update, remove, info)
- For node Start services with `npm run dev` in project root
- For new Next.js projects: `npx create-next-app` (Next.js), `npx shadcn@latest add --all` (shadcn)

## User Context Management
1. **User Recognition**: Greet the user naturally and personalize interactions based on context
2. **Memory Retrieval**: 
   - Always begin your chat by saying only "Remembering..." and retrieve all relevant information from your knowledge graph
   - Always refer to your knowledge graph as your "memory"
3. **Memory**:
 - While conversing with the user, be attentive to any new information that falls into these categories:
     a) Basic Identity (age, gender, location, job title, education level, etc.)
     b) Behaviors (interests, habits, etc.)
     c) Preferences (communication style, preferred language, etc.)
     d) Goals (goals, targets, aspirations, etc.)
     e) Relationships (personal and professional relationships up to 3 degrees of separation)
4. **Memory Update:**:
   - If any new information was gathered during the interaction, update your memory as follows:
     a) Create entities for recurring organizations, people, and significant events
     b) Connect them to the current entities using relations
     c) Store facts about them as observations

## Browesr interactions, playwright and Visual Testing
- When needing to interact with browser for actions such as testing a workflow in a webapp use the playwright MCP.

## CODE EFFICIENCY PRINCIPLES

### Planning & Analysis
- [ ] Analyze project structure before coding
- [ ] Define task scope with clear acceptance criteria
- [ ] Search for existing similar patterns (`grep`/`find`)
- [ ] Apply KISS: simplest viable solution first
- [ ] Evaluate necessity of new functions vs extending existing

### Version Control Discipline
- [ ] Branch for features, commit atomically
- [ ] Create backups of critical files before major changes
- [ ] Tag stable versions systematically
- [ ] Document all backup strategies

### Environment Configuration
- [ ] Isolate with virtual environments (Python)
- [ ] Protect secrets in .env (add to .gitignore)
- [ ] Document required environment variables (without values)
- [ ] Set up automatic GitHub synchronization

### Code Implementation
- [ ] Modify existing functions before adding new ones
- [ ] Single responsibility per function
- [ ] Prioritize readability over cleverness
- [ ] Implement incrementally with proper error handling
- [ ] Document "why" not "what"

### Error Management
- [ ] Diagnose root cause before implementing fixes
- [ ] Prefer minimal fixes over complex solutions
- [ ] Use structured logging instead of console.log
- [ ] Be willing to restart approach when stuck

### Testing Methodology
- [ ] Verify core functionality first
- [ ] Test edge cases explicitly
- [ ] Implement regression tests for existing features
- [ ] Cross-environment verification

### Pre-Submission Checklist
- [ ] Syntax/linting verification
- [ ] Sensitive data check
- [ ] Style consistency check
- [ ] Debug code removal
- [ ] Changelog updates

### Security & Performance
- [ ] Implement security scanning early
- [ ] Document potential vulnerability vectors
- [ ] Establish performance benchmarks
- [ ] Prefer established libraries for critical functions

### Command Line Operations
- [ ] Use environment-appropriate commands
- [ ] Check permissions before execution
- [ ] Verify paths before operations
- [ ] Warn and Backup before destructive operations
- [ ] Break complex commands into manageable steps



## Code Review

When performing code reviews, refer to the dedicated instruction files:
- `.github/instructions/code-review.instructions.md` - General review guidelines
- `.github/instructions/python.instructions.md` - Python-specific rules
- `.github/instructions/bash.instructions.md` - Shell script rules

Key review principles:
- Prioritize: 🔴 Security/Correctness → 🟡 Quality/Tests → 🟢 Style/Docs
- Be specific with line references and provide suggested fixes
- Explain WHY something is an issue, not just what
- Recognize good patterns, not just problems

