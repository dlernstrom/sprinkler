"""This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org>
"""
import asyncio
import datetime
import os
import sys
import time


def reboot_system():
    """wait 10 minutes to restart in case there is a problem we need to investigate and abort the reboot
    this also allows plenty of opportunity to update the code in case this occured on fire-up
    """
    time.sleep(120)
    os.system('sudo reboot')
    sys.exit()


def secs_until_hour(hour_requested):
    now = datetime.datetime.now()
    target = now.replace(hour=hour_requested, minute=0, second=0, microsecond=0)
    if target < now:
        target += datetime.timedelta(days=1)
    return int((target - now).total_seconds())


def spin(total_duration):
    yield
    for x in range(total_duration):
        time.sleep(1)
        yield


async def arange(count):
    """Range as an async object"""
    for i in range(count):
        yield i


async def async_spin(total_duration):
    yield
    async for x in arange(total_duration):
        await asyncio.sleep(1)
        yield
