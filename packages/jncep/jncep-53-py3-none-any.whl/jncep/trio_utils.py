from __future__ import annotations

from functools import partial, wraps
import logging
import sys
import warnings

import attr
from exceptiongroup import BaseExceptionGroup
import outcome
import trio
from trio import TrioDeprecationWarning

logger = logging.getLogger(__name__)

warnings.filterwarnings(action="ignore", category=TrioDeprecationWarning)


def handle_PriorityExceptions(exc):
    if (
        isinstance(exc, SystemExit)
        or isinstance(exc, KeyboardInterrupt)
        or isinstance(exc, GeneratorExit)
    ):
        return exc
    if isinstance(exc, BaseExceptionGroup):
        for ex in exc.exceptions:
            base_ex = handle_PriorityExceptions(ex)
            if base_ex:
                return base_ex
    return None


def coro(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return trio.run(partial(f, *args, **kwargs))
        except BaseExceptionGroup as ex:
            # in not debug mode => will only show a single exc ; show complete list
            # of exceptions in debug
            logger.debug(f"Error in wrapper: {ex}", exc_info=sys.exc_info())

            # TODO does this make sense ???
            base_ex = handle_PriorityExceptions(ex)
            if base_ex:
                raise base_ex from ex
            # just the first
            raise ex.exceptions[0] from ex

    return wrapper


def is_in_trio_context():
    try:
        trio.lowlevel.current_task()
        return True
    except RuntimeError:
        return False


# taken from trio-future: incompatible with trio > 0.19 so done here
@attr.s
class Future:
    result_chan: trio.abc.ReceiveChannel = attr.ib()

    async def get(self):
        future_outcome = await self.outcome()
        return future_outcome.unwrap()

    async def outcome(self) -> outcome.Outcome:
        try:
            async with self.result_chan:
                return await self.result_chan.receive()
        except trio.ClosedResourceError as ex:
            raise RuntimeError(
                "Trio resource closed (did you try to call outcome twice on this "
                "future?"
            ) from ex


async def bag(async_fns):
    # background and gather
    async with trio.open_nursery() as n:
        f_tasks = []
        for async_fn in async_fns:
            f_task = background(n, async_fn)
            f_tasks.append(f_task)

        results = await gather(n, f_tasks).get()
        return results


def background(nursery: trio.Nursery, async_fn) -> Future:
    send_chan, recv_chan = trio.open_memory_channel(1)

    async def producer():
        return_val = await outcome.acapture(async_fn)
        # Shield sending the result from parent cancellation.
        with trio.CancelScope(shield=True):
            async with send_chan:
                await send_chan.send(return_val)

    nursery.start_soon(producer)
    return Future(recv_chan)


def gather(nursery: trio.Nursery, futures: list[Future]) -> Future:
    result_list = [None] * len(futures)
    parent_send_chan, parent_recv_chan = trio.open_memory_channel(0)
    child_send_chan, child_recv_chan = trio.open_memory_channel(0)

    async def producer():
        async with child_send_chan:
            for i in range(len(futures)):
                nursery.start_soon(child_producer, i, child_send_chan.clone())

    async def child_producer(i: int, out_chan):
        async with futures[i].result_chan:
            return_val = await futures[i].result_chan.receive()
            result_list[i] = return_val
            async with out_chan:
                await out_chan.send(i)

    async def receiver():
        async with child_recv_chan:
            async for _ in child_recv_chan:
                # Just consume all results from the channel until exhausted
                pass
        # And then wrap up the result and push it to the parent channel
        errors = [e.error for e in result_list if isinstance(e, outcome.Error)]
        if len(errors) > 0:
            result = outcome.Error(BaseExceptionGroup("receiver", errors))
        else:
            result = outcome.Value([o.unwrap() for o in result_list])
        async with parent_send_chan:
            await parent_send_chan.send(result)

    # Start parent producer, which will in turn start all children
    # (doing this inside the nursery because it needs to act async)
    nursery.start_soon(producer)
    nursery.start_soon(receiver)
    return Future(parent_recv_chan)
