# Nowledge Mem for Pi

Cross-tool memory for Pi. Your decisions, preferences, and procedures persist across sessions and across every AI tool you use.

## What You Get

Pi gains a native extension plus five skills:

- Completed Pi conversations sync into Nowledge Mem as searchable threads
- Context Bundle and Working Memory stay **lazy by default** instead of being injected into every Pi request
- Search, thread lookup, Working Memory, and distillation are available on demand through skills and the `nmem` CLI
- Remote Mem works through `~/.nowledge-mem/config.json` or `NMEM_API_URL` / `NMEM_API_KEY`

| Skill | What it does |
|-------|-------------|
| `read-working-memory` | Loads Context Bundle or the lighter Working Memory briefing when prior context is relevant |
| `search-memory` | Searches past decisions, procedures, and preferences when context would help |
| `distill-memory` | Saves decisions, insights, and procedures as durable memories |
| `save-thread` | Creates a curated handoff summary when you explicitly want one |
| `status` | Checks Nowledge Mem server connectivity |

## Lazy Context by Default

The Pi extension does not read or append Nowledge Context Bundle / Working Memory merely because a session starts. This keeps normal Pi prompts small and lets the agent retrieve memory only when the task actually depends on prior context.

The automatic conversation-to-thread sync remains enabled.

If you explicitly prefer the previous eager behavior, start Pi with:

```bash
NMEM_PLUGIN_AUTO_CONTEXT=1 pi
```

That opt-in restores the existing startup Context Bundle read, `before_agent_start` system-prompt injection, and post-compaction refresh. The shared extension runtime keeps the historical default for non-Pi consumers such as OMP unless `NMEM_PLUGIN_AUTO_CONTEXT` is set explicitly.

## Prerequisites

1. **Nowledge Mem** desktop app running, or a remote server.
2. **`nmem` CLI** in your PATH:

```bash
pip install nmem-cli    # or: pipx install nmem-cli
# Arch Linux: yay -S nmem-cli  # or: paru -S nmem-cli
nmem status             # verify connection
```

On Windows/Linux with the Nowledge Mem desktop app, `nmem` is already bundled.

## Install

**Via Pi package manager:**

```bash
pi install npm:nowledge-mem-pi
```

**Manual install:**

Copy the `skills/` directory and extension into your Pi config:

```bash
# Global skills
cp -r skills/* ~/.pi/agent/skills/
mkdir -p ~/.pi/agent/extensions
cp extensions/nowledge-mem.ts ~/.pi/agent/extensions/

# Or project-local skills
cp -r skills/* .pi/skills/
mkdir -p .pi/extensions
cp extensions/nowledge-mem.ts .pi/extensions/
```

## Verify

Start a Pi session and check connectivity:

```
> check my Nowledge Mem status
```

Pi should run `nmem --json status` and report the server connection.

Then have a short Pi exchange and check recent threads:

```bash
nmem t list --source pi -n 5
```

For a task that needs prior context, ask Pi to load your Nowledge context or use the `read-working-memory` skill. Pi should call `nmem --json context --source-app pi` (or the lighter `nmem --json wm read`) only at that point.

To verify the eager opt-in separately, start a fresh process with `NMEM_PLUGIN_AUTO_CONTEXT=1` and ask what Nowledge Mem context was provided. Pi should then reference the injected Context Bundle or Working Memory without needing another read.

## Import Older Pi Sessions

The extension keeps new Pi conversations synced automatically. To backfill sessions that happened before you installed the package, run the history sync command.

Preview first. This scans Pi session files and makes no changes:

```bash
nmem t sync --from pi --limit 20
```

Import after the preview looks right:

```bash
nmem t sync --from pi --apply
```

The command uses the same local or remote Mem configuration as the extension: `~/.nowledge-mem/config.json`, `NMEM_API_URL`, `NMEM_API_KEY`, and optional `NMEM_SPACE`. It is safe to rerun: thread IDs come from Pi session IDs, and messages use stable Pi entry IDs with backend deduplication.

Useful options:

```bash
nmem t sync --from pi --session-dir ~/.pi/agent/sessions --limit 20
nmem t sync --from pi --space work --apply
nmem t sync --from pi --space-id sp_work_ab12cd34 --apply
```

When you pass `--session-dir`, only that directory is scanned. Without it, the command uses Pi's standard session locations.

If your installed `nmem` does not have `t sync` yet, use the package fallback:

```bash
npx -p nowledge-mem-pi nowledge-mem-pi-sync --apply
```

## Update

```bash
pi update
```

## Project Guidance

For behavioral guidance that shapes how Pi uses these skills (when to search, when to save, retrieval routing), see [AGENTS.md](AGENTS.md). Place it alongside your project configuration so Pi follows it automatically.

The bundled guidance follows the same lazy-context rule: isolated tasks skip memory reads; continuation and prior-decision tasks retrieve only the context they need.

## Customize without editing the package

Use your project's own `AGENTS.md` as the override layer for Pi.

- Keep the package skills as shipped defaults
- Copy or merge the package `AGENTS.md` into your project config area
- Do not patch installed package files under the Pi package cache

That keeps your custom behavior durable across package updates.

## Troubleshooting

**nmem not found:** Install with `pip install nmem-cli`, `pipx install nmem-cli`, or on Arch Linux `yay -S nmem-cli` / `paru -S nmem-cli`.

**Server not running:** Start the Nowledge Mem desktop app, or run `nmem serve` on your server.

**Remote setup:** Create `~/.nowledge-mem/config.json` with `{"apiUrl": "...", "apiKey": "..."}`, or set `NMEM_API_URL` and `NMEM_API_KEY` environment variables. The extension uses the same config for automatic thread sync.

**Context is not loaded at startup:** This is the default Pi behavior. Ask Pi to read context when needed, or set `NMEM_PLUGIN_AUTO_CONTEXT=1` before starting Pi to opt into eager startup injection.

**Check status:** Ask Pi to run the `status` skill, or run `nmem status` directly.

**Extension diagnostics:** Automatic sync failures retry on a later lifecycle event without writing raw diagnostics into Pi's interactive editor. Set `NMEM_PLUGIN_DEBUG=1` before starting Pi when troubleshooting the extension itself.

## Links

- [Documentation](https://mem.nowledge.co/docs/integrations/pi)
- [All Connectors](https://mem.nowledge.co/docs/integrations)
- [GitHub](https://github.com/nowledge-co/community)

---

Made with care by [Nowledge Labs](https://nowledge-labs.ai)
