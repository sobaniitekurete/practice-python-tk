# -*- coding: utf-8 -*-
from tkinter import *
from bh3 import *
import json
from urllib import parse
from event_manager import *
import threading
import time

flag = False
EVENT_COUNT = 'event_count'
EVENT_RESULT = 'event_result'
eventmanager = EventManager()

threades = []


def start(auth_key, sign, buy_types, buy_price, count, btn, result):
    global flag, threades
    flag = False
    # _start(auth_key,sign,count)

    t = threading.Thread(target=_start, args=(auth_key, sign, buy_types, buy_price, count, result))
    threades.append(t)
    t.setDaemon(True)
    t.start()
    btn['state'] = DISABLED


def _start(auth_key, sign, buy_types, buy_price, count, result):
    global eventmanager
    print('start')
    print('-' * 20)
    types = buy_types.get().split(',')
    price_to_buy = buy_price.get().split(',')
    auth_key = parse.quote(auth_key.get())
    sign = parse.quote(sign.get())
    buyer = Buyer(auth_key, sign)

    event = Event(type_=EVENT_COUNT)
    event.dict['target'] = count

    event2 = Event(type_=EVENT_RESULT)
    event2.dict['target'] = result
    n = 0
    while True:
        time.sleep(0.01)
        if flag:
            break
        pre_data = buyer.get_data()
        data = json.loads(pre_data)
        if data['retcode'] == 0:
            data = data['data']
            for t in types:
                for p in price_to_buy:
                    n += 1
                    event.dict['content'] = n
                    eventmanager.SendEvent(event)
                    if data[t][p] != '0':
                        res = buyer.buy(t, p)
                        res = json.loads(res)
                        if res['retcode'] == 0:
                            event2.dict['content'] = ('购买' + t + '   ' + p + '     1个')
                            eventmanager.SendEvent(event2)
        else:
            event.dict['content'] = str(data)
            eventmanager.SendEvent(event)
            break


def url2dict(url):
    query = parse.urlparse(url).query
    return dict([(k, v[0]) for k, v in parse.parse_qs(query).items()])


def set_keys(url, target1, target2):
    data = url2dict(url.get())
    target1.set(data['auth_key'])
    target2.set(data['sign'])


def stop(btn1, btn2):
    global flag, threades
    flag = True
    btn1['state'] = NORMAL
    for t in threades:
        t.join()


root = Tk()
root.title("Bh_")

l0 = Label(root, text="url：")
l0.pack()

url = StringVar()
url_entry = Entry(root, textvariable=url)
url.set("")
url_entry.pack()

auth_key = StringVar()
bh_sign = StringVar()
b0 = Button(root, text='cs', width=15, height=2, command=lambda: set_keys(url, auth_key, bh_sign))
b0.pack()

l1 = Label(root, text="auth_key：")
l1.pack()
auth_key_entry = Entry(root, textvariable=auth_key)
auth_key.set("")
auth_key_entry.pack()

l2 = Label(root, text="sign：")
l2.pack()

bh_sign_entry = Entry(root, textvariable=bh_sign)
bh_sign.set("")
bh_sign_entry.pack()

count = StringVar()
count_label = Entry(root, textvariable=count)
count.set(0)

l3 = Label(root, text="types：papercut,chipao,firecracker")
l3.pack()
buy_types = StringVar()
buy_types_entry = Entry(root, textvariable=buy_types)
buy_types.set("papercut,firecracker")
buy_types_entry.pack()

l4 = Label(root, text="price：0100")
l4.pack()
buy_price = StringVar()
buy_price_entry = Entry(root, textvariable=buy_price)
buy_price.set("0100,0200,0300,0400")
buy_price_entry.pack()

text = Text(root, height=20)


def set_count(event):
    event.dict['target'].set(event.dict['content'])


def insert_result(event):
    event.dict['target'].insert(END, event.dict['content'] + '\n')


def event_test(key, sign, which):
    exchange(key, sign, which)


eventmanager.AddEventListener(EVENT_COUNT, set_count)
eventmanager.AddEventListener(EVENT_RESULT, insert_result)

b1 = Button(root, text='start', width=15, height=2,
            command=lambda: start(auth_key, bh_sign, buy_types, buy_price, count, b1, text))
b1.pack()
b2 = Button(root, text='stop', width=15, height=2, command=lambda: stop(b1, b2))
b2.pack()
count_label.pack()
text.pack()

eventmanager.Start()

b3 = Button(root, text='sadfasdf', width=15, height=2, command=lambda: event_test(auth_key, bh_sign, 2))
b3.pack()


def close_window():
    global threades, eventmanager
    eventmanager.Stop()
    for t in threades:
        t.join()
    root.destroy()


root.protocol('WM_DELETE_WINDOW', close_window)

root.mainloop()
