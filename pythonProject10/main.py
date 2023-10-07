from eth_account import Account
import multiprocessing
import time

start_time = time.time()
def main():
    while True:
        Account.enable_unaudited_hdwallet_features()
        acct, mnemonic = Account.create_with_mnemonic()
        if 'BEEF' in acct.address[2:6]:
            print(acct.address)
            print(mnemonic)
            print("--- %s seconds ---" % (time.time() - start_time))
            p.terminate()

if __name__ == '__main__':
    for i in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=main)
        p.start()
