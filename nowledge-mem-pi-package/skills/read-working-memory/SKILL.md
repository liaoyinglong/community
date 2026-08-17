---
name: read-working-memory
description: "Load Nowledge Context Bundle or Working Memory when prior context is relevant to the current task."
---

# Read Working Memory

Use this skill on demand. Pi should not load Nowledge Mem context merely because a new session started.

Prefer Context Bundle when owner identity, AI Identity, active scope, rules, or Working Memory could materially affect the task. Use Working Memory alone for the lighter daily briefing.

## When to Use

- User asks "what am I working on?", "what's my context?", or asks about recent priorities.
- User references earlier work, previous decisions, established preferences, or a prior session.
- The current task clearly resumes a named project, feature, bug, refactor, incident, or workflow.
- Historical context would materially reduce ambiguity or prevent repeating prior work.

## Skip When

- The task is isolated and context-independent.
- The question is generic and can be answered without user history.
- Context Bundle or Working Memory was already loaded for the current task.
- The user explicitly wants a fresh perspective without prior context.

## Usage

For full context:

```bash
nmem --json context --source-app pi
```

If the runtime already knows the current project or agent lane, add `--space "<space name>"`. Multi-agent orchestrators can set `NMEM_AGENT_ID="<agent-slug>"` before launching the child agent. Add `NMEM_SPACE` only when that whole run should override the identity's default space. Use `NMEM_HOST_AGENT_ID` only for advanced external aliases.

For only Working Memory:

```bash
nmem --json wm read
```

### What You'll Find

- **Active Focus Areas**: Topics you're currently engaged with, ranked by recent activity
- **Priorities**: Items flagged as important or needing attention
- **Unresolved Flags**: Contradictions, stale information, or items needing verification
- **Recent Activity**: What changed in your knowledge base since the last briefing
- **Deep Links**: References to specific memories for further exploration

### How to Use This Context

1. Read the smallest context surface that answers the task.
2. If Context Bundle includes Working Memory, do not read Working Memory again.
3. For continuation, review, regression, release, or prior-decision questions, follow with one targeted `search-memory` call when the briefing is not enough.
4. Reference context naturally only when it connects to the current task.
5. Share only the relevant parts.
6. Do not re-read unless the user asks or the session context changes materially.

The Pi extension itself uses the same lazy default. Set `NMEM_PLUGIN_AUTO_CONTEXT=1` before starting Pi only if eager startup Context Bundle injection is explicitly desired.

If the response includes `exists: false`, mention there's no briefing yet and continue.

## Links

- [Documentation](https://mem.nowledge.co/docs/integrations/pi)
- [Troubleshooting](https://mem.nowledge.co/docs/troubleshooting)
