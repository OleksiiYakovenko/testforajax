import asyncio
from PIL import Image
import io


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(host="localhost", port=8888)

    data = {}
    bytesFromServer = bytearray()

    while True:
        print(f'Send: {message!r}')
        writer.write(message.encode())
        await writer.drain()
        chunk = await reader.read(2048)
        if len(chunk) != 0:
            data.setdefault(chunk[0], chunk[1:])
        else:
            break

    print('Close the connection')
    writer.close()
    await writer.wait_closed()

    for i in sorted(data.keys()):
        bytesFromServer += data[i]

    test = Image.open(io.BytesIO(bytesFromServer))
    test.save('testovoe.png')


asyncio.run(tcp_echo_client('next'))