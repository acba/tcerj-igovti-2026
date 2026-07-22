"""Locacao exclusiva de chaves de API com limites individuais de RPM e TPM."""
from __future__ import annotations

import collections
import threading
import time
from dataclasses import dataclass, field
from typing import Callable


MAX_KEY_COOLDOWN_SECONDS = 180.0
DEFAULT_KEY_COOLDOWN_SECONDS = 60.0


def normalizar_chaves(raw_keys: str) -> list[str]:
    """Separa a lista do ambiente, removendo vazios e duplicatas sem reordenar."""
    return list(dict.fromkeys(key.strip() for key in raw_keys.split(",") if key.strip()))


def rotulo_chave(key: str, index: int) -> str:
    if len(key) > 12:
        return f"{key[:6]}...{key[-4:]}"
    return f"chave-{index + 1}"


@dataclass
class _KeyState:
    key: str
    label: str
    in_use: bool = False
    cooldown_until: float = 0.0
    last_started_at: float | None = None
    token_reservations: collections.deque[tuple[float, int]] = field(
        default_factory=collections.deque
    )


class ApiKeyLease:
    """Locacao que deve ser liberada exatamente uma vez."""

    def __init__(self, pool: "ExclusiveApiKeyPool", state: _KeyState):
        self._pool = pool
        self._state = state
        self._released = False

    @property
    def key(self) -> str:
        return self._state.key

    @property
    def label(self) -> str:
        return self._state.label

    def release(self, *, cooldown_seconds: float = 0.0) -> None:
        if self._released:
            return
        self._released = True
        self._pool._release(self._state, cooldown_seconds=cooldown_seconds)


class ExclusiveApiKeyPool:
    """Entrega apenas chaves livres, respeitando limites por chave.

    ``rpm`` preserva a semantica historica do projeto: intervalo minimo entre
    inicios de chamadas logicas. ``tpm`` usa uma janela movel de 60 segundos
    sobre a estimativa de tokens de entrada reservada no inicio da chamada.
    """

    def __init__(
        self,
        raw_keys: str,
        *,
        rpm: int = 0,
        tpm: int = 0,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        if rpm < 0:
            raise ValueError("rpm por chave deve ser maior ou igual a zero")
        if tpm < 0:
            raise ValueError("tpm por chave deve ser maior ou igual a zero")
        keys = normalizar_chaves(raw_keys)
        if not keys:
            raise ValueError("GEMINI_API_KEY não contém chaves válidas")
        self.rpm = rpm
        self.tpm = tpm
        self._clock = clock
        self._states = [
            _KeyState(key=key, label=rotulo_chave(key, index))
            for index, key in enumerate(keys)
        ]
        self._condition = threading.Condition()
        self._cursor = 0

    @property
    def key_count(self) -> int:
        return len(self._states)

    def _prune_tokens(self, state: _KeyState, now: float) -> None:
        cutoff = now - 60.0
        while state.token_reservations and state.token_reservations[0][0] <= cutoff:
            state.token_reservations.popleft()

    def _tokens_ready_at(self, state: _KeyState, tokens: int, now: float) -> float:
        if self.tpm <= 0 or tokens <= 0:
            return now
        self._prune_tokens(state, now)
        total = sum(amount for _, amount in state.token_reservations)
        if total + tokens <= self.tpm:
            return now
        for timestamp, amount in state.token_reservations:
            total -= amount
            if total + tokens <= self.tpm:
                return timestamp + 60.0
        return now + 60.0

    def _ready_at(self, state: _KeyState, tokens: int, now: float) -> float:
        ready_at = max(now, state.cooldown_until)
        if self.rpm > 0 and state.last_started_at is not None:
            ready_at = max(ready_at, state.last_started_at + (60.0 / self.rpm))
        return max(ready_at, self._tokens_ready_at(state, tokens, now))

    def acquire(
        self,
        *,
        tokens: int = 0,
        on_wait: Callable[[dict[str, object]], None] | None = None,
    ) -> ApiKeyLease:
        if tokens < 0:
            raise ValueError("a reserva de tokens não pode ser negativa")
        if self.tpm > 0 and tokens > self.tpm:
            raise ValueError(
                f"payload estimado excede o TPM por chave: {tokens:,} > {self.tpm:,}"
            )

        with self._condition:
            while True:
                now = self._clock()
                ready: list[tuple[int, _KeyState, float]] = []
                for offset in range(len(self._states)):
                    index = (self._cursor + offset) % len(self._states)
                    state = self._states[index]
                    if not state.in_use:
                        ready.append((index, state, self._ready_at(state, tokens, now)))

                available = next((item for item in ready if item[2] <= now), None)
                if available is not None:
                    index, state, _ = available
                    state.in_use = True
                    state.last_started_at = now
                    if self.tpm > 0 and tokens > 0:
                        state.token_reservations.append((now, tokens))
                    self._cursor = (index + 1) % len(self._states)
                    return ApiKeyLease(self, state)

                constrained_ready = [ready_at for _, _, ready_at in ready]
                timeout = max(0.01, min(constrained_ready) - now) if constrained_ready else None
                if on_wait is not None:
                    on_wait(
                        {
                            "wait_seconds": round(timeout, 3) if timeout is not None else None,
                            "keys_in_use": sum(state.in_use for state in self._states),
                            "keys_total": len(self._states),
                        }
                    )
                self._condition.wait(timeout=timeout)

    def _release(self, state: _KeyState, *, cooldown_seconds: float) -> None:
        cooldown = min(
            MAX_KEY_COOLDOWN_SECONDS,
            max(0.0, float(cooldown_seconds)),
        )
        with self._condition:
            state.in_use = False
            if cooldown > 0:
                state.cooldown_until = max(state.cooldown_until, self._clock() + cooldown)
            self._condition.notify_all()


def cooldown_429(result: dict[str, object]) -> float:
    value = result.get("retry_after_seconds", DEFAULT_KEY_COOLDOWN_SECONDS)
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        seconds = DEFAULT_KEY_COOLDOWN_SECONDS
    return min(MAX_KEY_COOLDOWN_SECONDS, max(1.0, seconds))


def resultado_429(result: object) -> bool:
    return isinstance(result, dict) and result.get("http_status") == 429
