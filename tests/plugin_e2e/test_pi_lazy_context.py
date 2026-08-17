from pathlib import Path


COMMUNITY_ROOT = Path(__file__).resolve().parents[2]
PI_EXTENSION = COMMUNITY_ROOT / "nowledge-mem-pi-package" / "extensions" / "nowledge-mem.ts"


def _hook_block(source: str, hook: str, next_hook: str) -> str:
    return source.split(f'pi.on("{hook}"', 1)[1].split(f'pi.on("{next_hook}"', 1)[0]


def test_pi_startup_context_is_lazy_by_default():
    source = PI_EXTENSION.read_text(encoding="utf-8")

    assert "NMEM_PLUGIN_AUTO_CONTEXT" in source
    assert 'return sourceApp() !== "pi";' in source

    session_start = _hook_block(source, "session_start", "before_agent_start")
    before_agent_start = _hook_block(source, "before_agent_start", "agent_end")
    session_compact = _hook_block(source, "session_compact", "session_before_switch")

    assert "if (!automaticStartupContextEnabled()) return;" in session_start
    assert "if (!automaticStartupContextEnabled()) return;" in before_agent_start
    assert "if (!automaticStartupContextEnabled()) return;" in session_compact


def test_pi_thread_sync_stays_automatic_when_context_is_lazy():
    source = PI_EXTENSION.read_text(encoding="utf-8")

    agent_end = _hook_block(source, "agent_end", "session_before_compact")
    before_compact = _hook_block(source, "session_before_compact", "session_compact")

    assert "automaticStartupContextEnabled" not in agent_end
    assert 'scheduleFlush(ctx, "agent_end")' in agent_end
    assert "automaticStartupContextEnabled" not in before_compact
    assert 'await flush(ctx, "session_before_compact")' in before_compact
