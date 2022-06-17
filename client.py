from datetime import datetime
import logging
import sys
from signalrcore.hub_connection_builder import HubConnectionBuilder
import os
import signal
import time
import threading
from tabulate import tabulate

address = os.getenv('ADDRESS', 'wss://feed.beter.co')
channel = os.getenv('CHANNEL', 'incident')
apiKey = os.getenv('API_KEY', "374cbc97-3126-441c-9bfa-6df8426380ff")
snapshotBatchSize = os.getenv('BATCH_SIZE', '1')

url = f"{address}/{channel}?ApiKey={apiKey}&snapshotBatchSize={snapshotBatchSize}"

start = datetime.utcnow()
disconnected = start
maxDis = start - start
maxR = start - start
maxR_HU = start - start
maxH = start - start
maxH_HU = start - start
maxHU = start - start
maxR_TIME = start
maxH_TIME = start
maxHU_TIME = start
maxDis_TIME = start

plus = False
last = datetime.utcnow()
lastData = datetime.utcnow()


def onUpdate(data):
    global plus
    global lastData
    global maxHU
    global maxHU_TIME
    now = datetime.utcnow()
    l = len(data[0])
    if l > 1:
        if plus:
            print("")
            plus = False
        print(f"OnUpdate - {l}")
    else:
        print("+", end='', flush=True)
        plus = True
    hu = now-lastData
    if hu > maxHU:
        maxHU = hu
        maxHU_TIME = now
    lastData = now


heartbeatInterval = 5


def onHeartbeat(data):
    global plus
    global last
    global lastData
    global maxR
    global maxR_HU
    global maxR_TIME
    global maxH
    global maxH_HU
    global maxH_TIME
    global maxHU
    global maxHU_TIME
    now = datetime.utcnow()
    if plus:
        print("")
        plus = False
    h = now-last
    hu = now-lastData
    suf = ""
    if h.total_seconds() > heartbeatInterval + 1:
        suf = " (long)"
        if hu.total_seconds() < heartbeatInterval + 1:
            suf = " (long heartbeat only)"
    else:
        if h.total_seconds() < heartbeatInterval - 1:
            suf = " (short)"

    ts = data[0]
    hb = datetime.utcfromtimestamp(ts/1000)
    r = now-hb
    if r.total_seconds() < 0:
        r = hb-hb
    if r > maxR:
        maxR = r
        maxR_HU = hu
        maxR_TIME = now
    if h > maxH:
        maxH = h
        maxH_HU = hu
        maxH_TIME = now
    if hu > maxHU:
        maxHU = hu
        maxHU_TIME = now

    table = [["OnHeartbeat", now, r, "", h, "", hu, "", suf],
             ["max", now-start, maxR, maxR_TIME, maxH, maxH_TIME, maxHU, maxHU_TIME, ""]]
    print(tabulate(table, headers=[
          "", "Time/Duration", "Real time", "R_TIME", "Hartbeat", "H_TIME", "Hartbeat OR Update", "HU_TIME", ""]))
    last = now
    lastData = now


def makeConnection():
    return HubConnectionBuilder()\
        .with_url(url, {
            "skip_negotiation": url.startswith("ws")
        })\
        .configure_logging(logging.ERROR, socket_trace=True)\
        .with_automatic_reconnect({
            "type": "raw",
            "keep_alive_interval": 10,
            "reconnect_interval": 1,
            "max_attempts": None
        }).build()


def startClient():
    hub_connection.on_open(onOpen)
    hub_connection.on_close(onClose)
    hub_connection.on_error(lambda data: print(
        f"An exception was thrown closed {data.error}"))
    hub_connection.on("OnUpdate", onUpdate)
    hub_connection.on("OnHeartbeat", onHeartbeat)
    while True:
        try:
            hub_connection.start()
            break
        except Exception as e:
            print(e)
            time.sleep(1)


def onOpen():
    global last
    global lastData
    global maxDis
    global maxDis_TIME
    global connected
    if connected:
        print("already connected")
        return
    connected = True
    print("connection opened and handshake received")
    now = datetime.utcnow()
    last = now
    lastData = now
    dis = now - disconnected
    if dis > maxDis:
        maxDis = dis
        maxDis_TIME = now
    table = [[now, dis, disconnected, maxDis, maxDis_TIME]]
    print(tabulate(table, headers=[
          "Connected", "DisDuration", "DisTime", "MaxDisDuration", "MaxDisTime"]))


connected = False


def reconnect():
    global hub_connection
    if needRestart != True:
        return
    if connected != True:
        print("reconnecting...")
        try:
            hub_connection.start()
        except Exception as e:
            print(e)


timer = None


def onClose():
    global hub_connection
    global disconnected
    global connected
    global timer
    if connected != True:
        print("already not connected")
        if timer != None:
            print("reconnect timer reset")
            timer.cancel()
            timer = None
        if needRestart:
            timer = threading.Timer(5, reconnect)
            timer.start()
    else:
        print("connection closed")
        disconnected = datetime.utcnow()
        connected = False


hub_connection = makeConnection()

startClient()

needRestart = True


def checkData():
    if needRestart != True:
        return
    delay = 1
    try:
        delta = datetime.utcnow() - lastData
        if delta.total_seconds() > 15:
            delay = 5
            print(f"Last data was {delta} ago. Restarting...")
            hub_connection.stop()
            hub_connection.start()
    finally:
        threading.Timer(delay, checkData).start()


checkData()


def signal_handler(_sig, _frame):
    global needRestart
    needRestart = False
    print("closing...")
    hub_connection.stop()
    threading.Timer(1, lambda: sys.exit(0)).start()


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.pause()
