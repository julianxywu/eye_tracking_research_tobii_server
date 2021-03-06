#!/usr/bin/env python

import asyncio
import websockets
import time

def follow(thefile):
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line

async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    # data file details
    data_fpath = './data.txt'
    data_fh = open(data_fpath,'a')
    data_fh.write('writing data on {}\n'.format(time.asctime(time.localtime(time.time()))))
    ###

    file_path = "/Users/AhsanAzim/.talon/talon.log"
    logfile = open(file_path,"r")
    loglines = follow(logfile)
    for line in loglines:
        splitted_line = line.split(" ")
        if (len(splitted_line) >= 8) and (splitted_line[7] == "1"):          # filter log properly
            x, y = splitted_line[8], splitted_line[9]
            y = y.strip("\n")                                   # get rid of newline
            x, y = float(x) * 1000, float(y) * 1000         # convert

            # write data to file
            data_fh.write('* {} {}\n'.format(x,y))
            ##

            # further format data string and send
            data_str = "during|{}|{}".format(x, y)
            # print(x, y)
            # print("SENDING {}".format(data_str))
            await websocket.send(data_str)
            line_time_info = await websocket.recv()
            print("{}\n".format(line_time_info))        # write to data file
            data_fh.write(line_time_info)

    # greeting = f"Hello {name}!"

    # await websocket.send(greeting)
    # print(f"> {greeting}")

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()



# https://stackoverflow.com/questions/5419888/reading-from-a-frequently-updated-file