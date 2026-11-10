"""In-process event bus: how modules integrate without importing each other (weeks 9-10).

The published event catalogue lives in docs/integration-contracts.md. Publish only events listed there.
"""

from collections import defaultdict
from collections.abc import Callable

_subscribers: dict[str, list[Callable[[dict], None]]] = defaultdict(list)


def subscribe(event: str, handler: Callable[[dict], None]) -> None:
    _subscribers[event].append(handler)


def publish(event: str, payload: dict) -> int:
    """Call every handler for the event; return how many ran. A failing handler does not stop the others."""
    ran = 0
    for handler in list(_subscribers.get(event, [])):
        try:
            handler(dict(payload))
            ran += 1
        except Exception as exc:  # noqa: BLE001 - one module must not break another
            print(f"[events] handler {getattr(handler, '__name__', handler)} failed on {event}: {exc}")
    return ran


def clear() -> None:
    _subscribers.clear()
