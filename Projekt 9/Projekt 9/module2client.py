import asyncio


async def main():
	reader, writer = await asyncio.open_connection('127.0.0.1',8080)

	writer.write(b'Hello!')
	await writer.drain()

	print(await reader.read(100))

asyncio.run(main())
