import asyncio

from mock_ai import get_mock_hazard
from protocol import encode_hazard
from ble_sender import BLESender


async def main():
    sender = BLESender()

    hazard = get_mock_hazard()
    packet = encode_hazard(hazard)

    print("Mock AI:", hazard)
    print("Packet:", packet)

    await sender.connect_with_retry()
    await sender.send(packet)
    await sender.disconnect()


if __name__ == "__main__":
    asyncio.run(main())