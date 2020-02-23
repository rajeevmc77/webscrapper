#!/usr/bin/env python
# coding: utf-8

# import classes.MGuruProcesor as mp
#
# if __name__ == "__main__":
#     p = mp.MGuruProcessor()
#     p.process()

loop = None
import asyncio
import classes.MGuruProcessorAsync as mp

def handle_exception(loop, context):
    msg = context.get("exception", context["message"])
    print(msg)

async def main():
    global loop
    p = mp.MGuruProcessorAsync(loop)
    await p.process()

loop = asyncio.get_event_loop()
loop.set_exception_handler(handle_exception)
loop.run_until_complete(main())


