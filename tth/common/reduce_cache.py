from collections.abc import Callable, Coroutine, Hashable, MutableMapping
from functools import wraps
from typing import Any, Concatenate, ParamSpec, TypeVar, overload

from async_reduce import AsyncReducer

THashable = TypeVar("THashable", bound=Hashable)
KeyType = tuple[THashable, ...]


class ReduceCacheMixin:
    _reducer: AsyncReducer
    _cache: MutableMapping[KeyType[Hashable], Any]

    def __init__(self) -> None:
        self._reducer = AsyncReducer()
        self._cache = dict()

    def _clear_cache(self) -> None:
        self._cache = dict()


TClass = TypeVar("TClass", bound=ReduceCacheMixin)
TParams = ParamSpec("TParams")
TResult = TypeVar("TResult")

WrappedFunctionType = Callable[
    Concatenate[TClass, TParams],
    Coroutine[Any, Any, TResult],
]
KeyFunctionType = Callable[TParams, KeyType[THashable]]
DecoratorFunctionType = Callable[
    [WrappedFunctionType[TClass, TParams, TResult]],
    WrappedFunctionType[TClass, TParams, TResult],
]


def _dump_key_func(*args: TParams.args, **kwargs: TParams.kwargs) -> KeyType[Hashable]:
    return (
        *args,
        *sorted(kwargs.items()),
    )


@overload
def reduce_cache(
    _func: None = None,
    *,
    key_func: KeyFunctionType[TParams, Hashable] = _dump_key_func,
) -> DecoratorFunctionType[TClass, TParams, TResult]: ...


@overload
def reduce_cache(
    _func: WrappedFunctionType[TClass, TParams, TResult],
    *,
    key_func: KeyFunctionType[TParams, Hashable] = _dump_key_func,
) -> WrappedFunctionType[TClass, TParams, TResult]: ...


def reduce_cache(
    _func: WrappedFunctionType[TClass, TParams, TResult] | None = None,
    *,
    key_func: KeyFunctionType[TParams, Hashable] = _dump_key_func,
) -> (
    WrappedFunctionType[TClass, TParams, TResult]
    | DecoratorFunctionType[TClass, TParams, TResult]
):
    def decorate(
        func: WrappedFunctionType[TClass, TParams, TResult],
    ) -> WrappedFunctionType[TClass, TParams, TResult]:
        @wraps(func)
        async def wrapper(
            self: TClass, /, *args: TParams.args, **kwargs: TParams.kwargs
        ) -> TResult:
            _key = (func.__name__, *key_func(*args, **kwargs))

            if _key in self._cache:
                return self._cache[_key]

            cache = self._cache
            value = await self._reducer(
                func(self, *args, **kwargs),
                ident=_key_hash_to_str(_key),
            )
            # check cache not dropped
            if self._cache is cache:
                # save value into cache
                cache[_key] = value
            return value

        return wrapper

    if _func:
        return decorate(_func)
    else:
        return decorate


def _key_hash_to_str(key: KeyType[Hashable]) -> str:
    return "#".join(str(hash(item)) for item in key)
