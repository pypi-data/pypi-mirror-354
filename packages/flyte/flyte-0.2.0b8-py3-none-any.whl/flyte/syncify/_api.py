from __future__ import annotations

import asyncio
import atexit
import concurrent.futures
import inspect
import threading
from typing import (
    Any,
    AsyncIterator,
    Awaitable,
    Callable,
    Coroutine,
    Iterator,
    ParamSpec,
    Protocol,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)

P = ParamSpec("P")
R_co = TypeVar("R_co", covariant=True)
T = TypeVar("T")


class SyncFunction(Protocol[P, R_co]):
    """
    A protocol that defines the interface for synchronous functions or methods that can be converted from asynchronous
     ones.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> R_co: ...

    def aio(self, *args: Any, **kwargs: Any) -> Awaitable[R_co]: ...


class SyncGenFunction(Protocol[P, R_co]):
    """
    A protocol that defines the interface for synchronous functions or methods that can be converted from asynchronous
     ones.
    """

    def __call__(self, *args: Any, **kwargs: Any) -> Iterator[R_co]: ...

    def aio(self, *args: Any, **kwargs: Any) -> AsyncIterator[R_co]: ...


class _BackgroundLoop:
    """
    A background event loop that runs in a separate thread and used the the Syncify decorator to run asynchronous
    functions or methods synchronously.
    """

    def __init__(self, name: str):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(name=name, target=self._run, daemon=True)
        self.thread.start()
        atexit.register(self.stop)

    def _run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop(self):
        # stop the loop and wait briefly for thread to exit
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.thread.join(timeout=1)

    def is_in_loop(self) -> bool:
        """
        Check if the current thread is the background loop thread.
        """
        # If the current thread is not the background loop thread, return False
        if threading.current_thread() != self.thread:
            return False

        if not self.thread.is_alive():
            # If the thread is not alive, we cannot be in the loop
            return False

        # Lets get the current event loop and check if it matches the background loop
        loop = None
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            pass

        return loop == self.loop

    def iterate_in_loop_sync(self, async_gen: AsyncIterator[R_co]) -> Iterator[R_co]:
        # Create an iterator that pulls items from the async generator
        assert self.thread.name != threading.current_thread().name, "Cannot run coroutine in the same thread"
        while True:
            try:
                # use __anext__() and cast to Coroutine so mypy is happy
                future: concurrent.futures.Future[R_co] = asyncio.run_coroutine_threadsafe(
                    cast(Coroutine[Any, Any, R_co], async_gen.__anext__()),
                    self.loop,
                )
                yield future.result()
            except (StopAsyncIteration, StopIteration):
                break

    def call_in_loop_sync(self, coro: Coroutine[Any, Any, R_co]) -> R_co:
        """
        Run the given coroutine in the background loop and return its result.
        """
        future: concurrent.futures.Future[R_co] = asyncio.run_coroutine_threadsafe(coro, self.loop)
        return future.result()

    async def iterate_in_loop(self, async_gen: AsyncIterator[R_co]) -> AsyncIterator[R_co]:
        """
        Run the given async iterator in the background loop and yield its results.
        """
        if self.is_in_loop():
            # If we are already in the background loop, just return the async iterator
            async for r in async_gen:
                yield r
            return

        while True:
            try:
                # same replacement here for the async path
                future: concurrent.futures.Future[R_co] = asyncio.run_coroutine_threadsafe(
                    cast(Coroutine[Any, Any, R_co], async_gen.__anext__()),
                    self.loop,
                )
                # Wrap the future in an asyncio Future to yield it in an async context
                aio_future: asyncio.Future[R_co] = asyncio.wrap_future(future)
                # await for the future to complete and yield its result
                yield await aio_future
            except StopAsyncIteration:
                break

    async def aio(self, coro: Coroutine[Any, Any, R_co]) -> R_co:
        """
        Run the given coroutine in the background loop and return its result.
        """
        if self.is_in_loop():
            # If we are already in the background loop, just run the coroutine
            return await coro
        # Otherwise, run it in the background loop and wait for the result
        future: concurrent.futures.Future[R_co] = asyncio.run_coroutine_threadsafe(coro, self.loop)
        # Wrap the future in an asyncio Future to await it in an async context
        aio_future: asyncio.Future[R_co] = asyncio.wrap_future(future)
        # await for the future to complete and return its result
        return await aio_future


class _SyncWrapper:
    """
    A wrapper class that the Syncify decorator uses to convert asynchronous functions or methods into synchronous ones.
    """

    def __init__(
        self,
        fn: Any,
        bg_loop: _BackgroundLoop,
        instance: Any = None,
        owner: Type | None = None,
        underlying_obj: Any = None,
    ):
        self.fn = fn
        self._bg_loop = bg_loop
        self._underlying_obj = underlying_obj

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        # bind method if needed
        coro_fn = self.fn

        if inspect.isasyncgenfunction(coro_fn):
            # Handle async iterator by converting to sync iterator
            async_gen = coro_fn(*args, **kwargs)
            return self._bg_loop.iterate_in_loop_sync(async_gen)
        else:
            return self._bg_loop.call_in_loop_sync(coro_fn(*args, **kwargs))

    def __get__(self, instance: Any, owner: Any) -> Any:
        """
        This method is called when the wrapper is accessed as a method of a class instance.
        :param instance:
        :param owner:
        :return:
        """
        fn: Any = self.fn
        if instance is not None:
            # If we have an instance, we need to bind the method to the instance (for instance methods)
            fn = self.fn.__get__(instance, owner)

        if instance is None and owner is not None and self._underlying_obj is not None:
            # If we have an owner, we need to bind the method to the owner (for classmethods or staticmethods)
            fn = self._underlying_obj.__get__(None, owner)

        return _SyncWrapper(fn, bg_loop=self._bg_loop, underlying_obj=self._underlying_obj)

    def aio(self, *args: Any, **kwargs: Any) -> Any:
        fn = self.fn

        if inspect.isasyncgenfunction(fn):
            # If the function is an async generator, we need to handle it differently
            async_iter = fn(*args, **kwargs)
            return self._bg_loop.iterate_in_loop(async_iter)
        else:
            # If we are already in the background loop, just return the coroutine
            coro = fn(*args, **kwargs)
            if hasattr(coro, "__aiter__"):
                # If the coroutine is an async iterator, we need to handle it differently
                return self._bg_loop.iterate_in_loop(coro)
            return self._bg_loop.aio(coro)


class Syncify:
    """
    A decorator to convert asynchronous functions or methods into synchronous ones.

    This is useful for integrating async code into synchronous contexts.

    Example::

    ```python
    syncer = Syncify()

    @syncer
    async def async_function(x: str) -> str:
        return f"Hello, Async World {x}!"


    # now you can call it synchronously
    result = async_function("Async World")
    print(result)
    # Output: Hello, Async World Async World!

    # or call it asynchronously
    async def main():
        result = await async_function.aio("World")
        print(result)
    ```

    """

    def __init__(self, name: str = "flyte_syncify"):
        self._bg_loop = _BackgroundLoop(name=name)

    @overload
    def __call__(self, func: Callable[P, Awaitable[R_co]]) -> Any: ...

    # def __call__(self, func: Callable[P, Awaitable[R_co]]) -> SyncFunction[P, R_co]: ...

    @overload
    def __call__(self, func: Callable[P, Iterator[R_co] | AsyncIterator[R_co]]) -> SyncGenFunction[P, R_co]: ...

    # def __call__(self, func: Callable[[Type[T], *P.args, *P.kwargs], Awaitable[R_co]])
    # -> SyncFunction[[Type[T], *P.args, *P.kwargs], R_co]: ...
    @overload
    def __call__(self, func: classmethod) -> Union[SyncFunction[P, R_co], SyncGenFunction[P, R_co]]: ...

    @overload
    def __call__(self, func: staticmethod) -> staticmethod: ...

    def __call__(self, obj):
        if isinstance(obj, classmethod):
            return _SyncWrapper(obj.__func__, bg_loop=self._bg_loop, underlying_obj=obj)
        if isinstance(obj, staticmethod):
            return staticmethod(cast(Any, _SyncWrapper(obj.__func__, bg_loop=self._bg_loop)))
        if inspect.isasyncgenfunction(obj):
            # If the function is an async generator, we need to handle it differently
            return cast(Callable[P, Iterator[R_co]], _SyncWrapper(obj, bg_loop=self._bg_loop))
        if inspect.iscoroutinefunction(obj):
            # If the function is a coroutine, we can wrap it directly
            return _SyncWrapper(obj, bg_loop=self._bg_loop)
        raise TypeError(
            "Syncify can only be applied to async functions, async generators, async classmethods or staticmethods."
        )
