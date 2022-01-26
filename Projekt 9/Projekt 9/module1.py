import asyncio

#korutyna
async def hello_async():
	await asyncio.sleep(5)
	print('hello Async World!')

	
async def hello_async2():
	print('hello Async World!')
	await asyncio.sleep(5)
	return 'ROTFL'

async def main():
	#1
	#tasks = [asyncio.create_task(hello_async()) for _ in range(4)]
	#for task in tasks:
	#	await task

	#2
	#tasks = [asyncio.create_task(hello_async()) for _ in range(4)]
	#await asyncio.gather(*tasks)

	#3
	#await asyncio.gather(*[hello_async() for _ in range(4)])

	#4
	#x = await hello_async2()
	print(await asyncio.gather(*[hello_async2() for _ in range(4)]))


asyncio.run(main())
