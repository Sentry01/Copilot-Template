"""
Automatic Reflection Generator
==============================

Generates reflection entries when session metrics indicate learning opportunities.
This provides automatic documentation of difficult sessions without manual intervention.

Triggers:
- high_errors: ≥5 total errors in session
- recovery_mode: Recovery mode was entered
- blocked_features: Any features couldn't be completed  
- low_completion: <50% feature success rate
"""

import json
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SessionMetrics:
    """Metrics collected during an agent session."""

    session_id: str
    start_time: datetime
    end_time: datetime
    total_errors: int
    consecutive_error_max: int
    recovery_mode_entered: bool
    features_attempted: int
    features_completed: int
    blocked_features: list[str] = field(default_factory=list)
    error_patterns: list[str] = field(default_factory=list)


# Reflection trigger conditions
REFLECTION_TRIGGERS = {
    "high_errors": lambda m: m.total_errors >= 5,
    "recovery_mode": lambda m: m.recovery_mode_entered,
    "blocked_features": lambda m: len(m.blocked_features) > 0,
    "low_completion": lambda m: (
        m.features_attempted > 0
        and m.features_completed / m.features_attempted < 0.5
    ),
}


def should_reflect(metrics: SessionMetrics) -> tuple[bool, list[str]]:
    """
    Determine if automatic reflection should trigger.

    Args:
        metrics: Session metrics to evaluate

    Returns:
        (should_trigger, list_of_triggered_conditions)
    """
    triggered = []
    for name, condition in REFLECTION_TRIGGERS.items():
        try:
            if condition(metrics):
                triggered.append(name)
        except (ZeroDivisionError, AttributeError, TypeError):
            # Skip conditions that can't be evaluated
            pass
    return len(triggered) > 0, triggered


def _get_next_session_id(reflections_path: Path) -> str:
    """Get the next session ID (R001, R002, etc.)."""
    if not reflections_path.exists():
        return "R001"

    existing = reflections_path.read_text()
    # Count existing sessions
    import re

    matches = re.findall(r"## Session R(\d+)", existing)
    if not matches:
        return "R001"

    max_id = max(int(m) for m in matches)
    return f"R{max_id + 1:03d}"


def generate_reflection_entry(metrics: SessionMetrics, triggers: list[str]) -> str:
    """
    Generate a reflection entry in markdown format.

    Args:
        metrics: Session metrics
        triggers: List of triggered conditions

    Returns:
        Markdown-formatted reflection entry
    """
    reflections_path = Path(".github/Reflection/reflections.md")
    session_id = _get_next_session_id(reflections_path)

    duration_mins = (metrics.end_time - metrics.start_time).seconds // 60

    # Build blocked features list
    blocked_list = (
        "\n".join(f"- {f}" for f in metrics.blocked_features)
        if metrics.blocked_features
        else "None"
    )

    # Build error patterns list (limit to 5)
    error_list = (
        "\n".join(f"- `{e}`" for e in metrics.error_patterns[:5])
        if metrics.error_patterns
        else "None"
    )

    entry = f"""

## Session {session_id}: Auto-Generated Reflection

**Date:** {metrics.end_time.strftime("%Y-%m-%d %H:%M")}
**Type:** Automatic (triggers: {", ".join(triggers)})
**Duration:** {duration_mins} minutes

### Session Metrics

| Metric | Value |
|--------|-------|
| Total Errors | {metrics.total_errors} |
| Max Consecutive Errors | {metrics.consecutive_error_max} |
| Recovery Mode Entered | {"Yes" if metrics.recovery_mode_entered else "No"} |
| Features Completed | {metrics.features_completed}/{metrics.features_attempted} |

### Blocked Features

{blocked_list}

### Error Patterns Observed

{error_list}

### Notes

*This is an auto-generated reflection. Run `/reflect` for deeper analysis.*

---
"""
    return entry


def update_memory(metrics: SessionMetrics, triggers: list[str]) -> None:
    """
    Update memory.json with session data for pattern analysis.

    Args:
        metrics: Session metrics
        triggers: List of triggered conditions
    """
    memory_path = Path(".github/Reflection/memory.json")

    if memory_path.exists():
        memory = json.loads(memory_path.read_text())
    else:
        memory = {
            "learnings": [],
            "rules": [],
            "stats": {},
            "searchIndex": {},
        }

    # Update stats
    stats = memory.get("stats", {})
    stats["totalSessions"] = stats.get("totalSessions", 0) + 1
    stats["autoReflections"] = stats.get("autoReflections", 0) + 1
    stats["lastAutoReflection"] = metrics.end_time.isoformat()
    stats["totalErrors"] = stats.get("totalErrors", 0) + metrics.total_errors

    # Track trigger frequency
    trigger_counts = stats.get("triggerCounts", {})
    for trigger in triggers:
        trigger_counts[trigger] = trigger_counts.get(trigger, 0) + 1
    stats["triggerCounts"] = trigger_counts

    memory["stats"] = stats

    # Add error patterns to search index for future matching
    search_index = memory.get("searchIndex", {})
    session_ref = f"session_{metrics.session_id}"
    for pattern in metrics.error_patterns:
        # Extract meaningful keywords (skip common words)
        skip_words = {"error", "failed", "the", "a", "an", "in", "at", "on", "is", "was"}
        keywords = [
            w.lower()
            for w in pattern.split()[:5]
            if len(w) > 2 and w.lower() not in skip_words
        ]
        for kw in keywords:
            if kw not in search_index:
                search_index[kw] = []
            if session_ref not in search_index[kw]:
                search_index[kw].append(session_ref)

    memory["searchIndex"] = search_index

    # Write back
    memory_path.parent.mkdir(parents=True, exist_ok=True)
    memory_path.write_text(json.dumps(memory, indent=2))


def run_auto_reflection(metrics: SessionMetrics) -> Optional[str]:
    """
    Main entry point for automatic reflection.

    Args:
        metrics: Session metrics to evaluate

    Returns:
        The generated reflection entry if triggered, None otherwise
    """
    should, triggers = should_reflect(metrics)

    if not should:
        return None

    # Generate and append reflection entry
    entry = generate_reflection_entry(metrics, triggers)
    reflections_path = Path(".github/Reflection/reflections.md")

    # Ensure directory exists
    reflections_path.parent.mkdir(parents=True, exist_ok=True)

    # Create file with header if it doesn't exist
    if not reflections_path.exists():
        header = """# Reflection Sessions

Chronological log of debug sessions and learnings.

---
"""
        reflections_path.write_text(header)

    # Append the entry
    with open(reflections_path, "a") as f:
        f.write(entry)

    # Update memory with session data
    update_memory(metrics, triggers)

    print(f"\n📝 Auto-reflection triggered ({', '.join(triggers)})")
    print(f"   Entry added to .github/Reflection/reflections.md")

    return entry


# Convenience class for tracking metrics during a session
class SessionTracker:
    """
    Helper class to track session metrics throughout agent execution.

    Usage:
        tracker = SessionTracker()
        # ... during session ...
        tracker.record_error("Some error message")
        tracker.record_feature_attempt("feature_name")
        tracker.record_feature_complete("feature_name")
        # ... at session end ...
        tracker.finalize()  # Triggers auto-reflection if needed
    """

    def __init__(self, session_id: Optional[str] = None):
        self.start_time = datetime.now()
        self.session_id = session_id or f"session_{self.start_time.strftime('%Y%m%d_%H%M')}"
        self.error_count = 0
        self.consecutive_errors = 0
        self.max_consecutive_errors = 0
        self.recovery_mode_entered = False
        self.features_attempted: set[str] = set()
        self.features_completed: set[str] = set()
        self.blocked_features: list[str] = []
        self.error_messages: set[str] = set()

    def record_error(self, error_msg: str) -> None:
        """Record an error occurrence."""
        self.error_count += 1
        self.consecutive_errors += 1
        self.max_consecutive_errors = max(
            self.max_consecutive_errors, self.consecutive_errors
        )
        # Store truncated, deduplicated error messages
        self.error_messages.add(error_msg[:100])

    def record_success(self) -> None:
        """Record a successful operation (resets consecutive error counter)."""
        self.consecutive_errors = 0

    def record_recovery_mode(self) -> None:
        """Record that recovery mode was entered."""
        self.recovery_mode_entered = True

    def record_feature_attempt(self, feature_name: str) -> None:
        """Record that a feature was attempted."""
        self.features_attempted.add(feature_name)

    def record_feature_complete(self, feature_name: str) -> None:
        """Record that a feature was completed successfully."""
        self.features_completed.add(feature_name)

    def record_blocked_feature(self, feature_name: str) -> None:
        """Record that a feature was blocked and couldn't be completed."""
        if feature_name not in self.blocked_features:
            self.blocked_features.append(feature_name)

    def get_metrics(self) -> SessionMetrics:
        """Generate SessionMetrics from tracked data."""
        return SessionMetrics(
            session_id=self.session_id,
            start_time=self.start_time,
            end_time=datetime.now(),
            total_errors=self.error_count,
            consecutive_error_max=self.max_consecutive_errors,
            recovery_mode_entered=self.recovery_mode_entered,
            features_attempted=len(self.features_attempted),
            features_completed=len(self.features_completed),
            blocked_features=self.blocked_features,
            error_patterns=list(self.error_messages),
        )

    def finalize(self) -> Optional[str]:
        """
        Finalize the session and trigger auto-reflection if needed.

        Returns:
            The reflection entry if generated, None otherwise
        """
        metrics = self.get_metrics()
        return run_auto_reflection(metrics)


# =============================================================================
# Integration Example
# =============================================================================
#
# To use automatic reflection in your agent, integrate SessionTracker:
#
# ```python
# from auto_reflect import SessionTracker
#
# async def run_agent():
#     tracker = SessionTracker()
#
#     try:
#         tracker.record_feature_attempt("implement_feature_x")
#
#         # Your agent logic here...
#         result = await do_work()
#
#         if result.success:
#             tracker.record_success()
#             tracker.record_feature_complete("implement_feature_x")
#         else:
#             tracker.record_error(str(result.error))
#
#     except Exception as e:
#         tracker.record_error(str(e))
#         tracker.record_blocked_feature("implement_feature_x")
#         raise
#
#     finally:
#         # Always finalize to trigger reflection if needed
#         tracker.finalize()
# ```
#
# For recovery mode tracking, call tracker.record_recovery_mode() when
# entering error recovery logic in your agent.
# =============================================================================


if __name__ == "__main__":
    # Demo/test mode - simulate a problematic session
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        print("🧪 Running auto-reflection demo...")

        tracker = SessionTracker("demo_session")

        # Simulate a session with problems
        tracker.record_feature_attempt("feature_a")
        tracker.record_feature_attempt("feature_b")
        tracker.record_error("ModuleNotFoundError: No module named 'foo'")
        tracker.record_error("SyntaxError: unexpected indent")
        tracker.record_error("FileNotFoundError: config.yaml not found")
        tracker.record_error("TypeError: expected str, got int")
        tracker.record_error("ConnectionError: timeout after 30s")
        tracker.record_feature_complete("feature_a")
        tracker.record_blocked_feature("feature_b")

        result = tracker.finalize()

        if result:
            print("\n✅ Demo complete - reflection was triggered")
        else:
            print("\n⚠️ Demo complete - no reflection triggered")
    else:
        print("Usage: python auto_reflect.py --demo")
        print("       Runs a demonstration of the auto-reflection system")
