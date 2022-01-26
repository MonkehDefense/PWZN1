import asyncio

async def callback(reader: asyncio.StreamReader,writer: asyncio.StreamWriter):
	#Visual Studio jest tępe
	while((message := await reader.read(100)) != b''):
		print(message)
		writer.write(message)
		await writer.drain()

async def main():
	server = await asyncio.start_server(callback, '', 8080)
	await server.serve_forever()

asyncio.run(main())
