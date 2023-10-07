import pprint
import binascii
import mnemonic
import bip32utils


def bip39(mnemonic_words):
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)
    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)
    return(bip32_child_key_obj.Address())


if __name__ == '__main__':
    while True:
        mnemonic_words = mnemonic.Mnemonic("english").generate()
        ad = bip39(mnemonic_words)
        if '777' in ad[1:3]:
            print(mnemonic_words)
            print(ad)
            break
