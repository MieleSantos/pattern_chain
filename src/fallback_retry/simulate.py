"""
Failure simulation, to see the pattern working without waiting for a real outage.
"""

from langchain_core.runnables import Runnable, RunnableLambda


class TransientError(Exception):
    """Stands for a rate limit (429), a timeout or a server error (5xx)."""


def failing(model: Runnable, times: int, name: str = "model", log: list[str] | None = None) -> Runnable:
    """
    Wrap a model so that its first `times` calls raise TransientError.

    Every call is appended to `log` as "<name>: falhou" or "<name>: ok".
    """
    state = {"calls": 0}

    def call(value):
        state["calls"] += 1
        if state["calls"] <= times:
            if log is not None:
                log.append(f"{name}: falhou")
            raise TransientError(f"{name} failed (call {state['calls']})")
        result = model.invoke(value)
        if log is not None:
            log.append(f"{name}: ok")
        return result

    return RunnableLambda(call)
