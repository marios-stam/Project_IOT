from multiprocessing import Process, Queue


def foo(q, t):
    q.put("Hello" + t)


if __name__ == '__main__':
    q = Queue()
    p = Process(target=foo, args=(q, " Tom"))
    p.start()
    print(q.get())
