"""Utility helpers for HTTP requests with automatic infinite retries.

Основная функция `request_with_retries` выполняет HTTP-запрос с помощью
`aiohttp` и при любой сетевой ошибке или «плохом» HTTP-статусе
(не входящем в `expected_statuses`) делает паузу `retry_delay` секунд и
повторяет попытку до успеха.
"""
from __future__ import annotations

import asyncio
from typing import Any, Iterable, Sequence

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError

__all__ = [
    "request_with_retries",
]


async def request_with_retries(
    method: str,
    url: str,
    *,
    retry_delay: int = 5,
    expected_statuses: Sequence[int] | int = (200,),
    return_json: bool = True,
    **request_kwargs: Any,
):
    """Выполняет HTTP-запрос с бесконечными ретраями.

    Parameters
    ----------
    method: str
        HTTP-метод (``"get"``, ``"post"`` и т.д.).
    url: str
        Полный URL запроса.
    retry_delay: int, optional
        Пауза (сек) между повторными попытками.  По умолчанию 5.
    expected_statuses: int | Sequence[int], optional
        Какой статус (или статусы) считается успешным.  По умолчанию ``200``.
    return_json: bool, optional
        Если *True* (по умолчанию) — после успешного ответа парсит и
        возвращает ``await resp.json()``.  Если *False* — просто возвращает
        объект ``aiohttp.ClientResponse`` (уже закрытый контекстом).
    **request_kwargs: Any
        Дополнительные аргументы для ``session.request`` (``headers``, ``json``
        и т.д.).
    """
    if isinstance(expected_statuses, int):
        expected_statuses = (expected_statuses,)

    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(method.upper(), url, **request_kwargs) as resp:
                    if resp.status in expected_statuses:
                        if return_json:
                            return await resp.json()
                        # Читаем тело, чтобы connection pool не ругался
                        await resp.read()
                        return resp
                    # Не тот статус — логируем и ретраим
                    body_preview = await resp.text()[:200]
                    print(
                        f"[HTTP RETRY] {method.upper()} {url} → {resp.status}. "
                        f"Body: {body_preview}. Повтор через {retry_delay}c…"
                    )
        except ClientConnectorError as e:
            print(f"[HTTP RETRY] Не удалось подключиться к {url}: {e}. Повтор через {retry_delay}c…")
        except Exception as e:
            print(f"[HTTP RETRY] Ошибка при запросе {url}: {e}. Повтор через {retry_delay}c…")

        await asyncio.sleep(retry_delay) 