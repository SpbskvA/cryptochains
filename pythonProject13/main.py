from bit import Key
from multiprocessing import Process, Value

PATTERN = 'pusev'
N_PROCESSES = 16


# предикат проверки адреса на наше желание
def predicate(addr: str):
    return addr[1:].startswith(PATTERN)


# рабочая функция
def worker(predicate: callable, stop: Value, counter: Value):
    # пока нам не посигналили о завершении из другого процесса
    while not stop.value:
        # новый ключ
        k = Key()

        # проверяем
        if predicate(k.address):
            print('done!')
            print(f'{k.address} with WIF private key {k.to_wif()}')

            # сигналим другим и выходим
            stop.value = True
            break

        counter.value += 1
        if counter.value % 10_000 == 0:
            print('.', end='')


if __name__ == '__main__':
    # эти переменные необычные - они позволяют обмениваться инфой между процессами
    stop = Value('b', False)
    counter = Value('i', 0)
    procs = []
    for worker_id in range(N_PROCESSES):
        # создадим процесс, передав рабочего и аргументы
        proc = Process(target=worker, args=(predicate, stop, counter))
        proc.start()
        procs.append(proc)
    # будем ждать пока все процессы не завершаться
    for proc in procs:
        proc.join()  # ждет процесс