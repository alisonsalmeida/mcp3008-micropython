from machine import Pin, SPI
from MCP3008 import MCP3008

import uasyncio as asyncio


async def main():
    spi = SPI(1, 100000, bits=8, firstbit=SPI.MSB)
    cs = Pin(27, mode=Pin.OUT, value=1)
    mcp = MCP3008(0, spi, cs)

    while True:
        value = await mcp.read(MCP3008.SINGLE)
        voltage = mcp.voltage

        print(f'value read: {value}')
        print(f'voltage: {voltage}')

        await asyncio.sleep(1)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
