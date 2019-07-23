# import asyncio
# import random
#
#
# class Potato:
#     @classmethod
#     def make(cls, num, *args, **kws):
#         potatos = []
#         for i in range(num):
#             potatos.append(cls.__new__(cls, *args, **kws))
#             print('potatos:', potatos)
#         return potatos
#
#
# all_potatos = Potato.make(5)
#
#
# async def ask_for_potato():
#     await asyncio.sleep(random.random())
#     all_potatos.extend(Potato.make(random.randint(1, 10)))
#
#
# async def take_potatos(num):
#     count = 0
#     while True:
#         if len(all_potatos) == 0:
#             await ask_for_potato()
#         potato = all_potatos.pop()
#         yield potato
#         count += 1
#         if count == num:
#             break
#
#
# async def buy_potatos():
#     bucket = []
#     async for p in take_potatos(50):
#         bucket.append(p)
#         print(f'Got potato {id(p)}...')
#
#
# class tomato:
#     @classmethod
#     def make(cls, num, *args, **kws):
#         tomatos = []
#         for i in range(num):
#             tomatos.append(cls.__new__(cls, *args, **kws))
#             print('potatos:', tomatos)
#         return tomatos
#
#
# all_tomatos = tomato.make(5)
#
#
# async def ask_for_tomatos():
#     await asyncio.sleep(random.random())
#     all_tomatos.extend(Potato.make(random.randint(1, 10)))
#
#
# async def take_tomatos(num):
#     count = 0
#     while True:
#         if len(all_tomatos) == 0:
#             await ask_for_tomatos()
#         tomatos = all_tomatos.pop()
#         yield tomatos
#         count += 1
#         if count == num:
#             break
#
#
# async def buy_tomatos():
#     bucket = []
#     async for p in take_tomatos(50):
#         bucket.append(p)
#         print(f'Got tomatos {id(p)}...')
#     print('bucket:', bucket)
#     print(len(bucket))
#
#
# def main():
#     import asyncio
#     loop = asyncio.get_event_loop()
#     res = loop.run_until_complete(asyncio.wait([buy_potatos(), buy_tomatos()]))
#     loop.close()
#
#
# main()
