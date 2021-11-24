from bitcoinutils.utils import to_satoshis
from bitcoinutils.setup import setup
from bitcoinutils.transactions import Transaction, TxInput, TxOutput
from bitcoinutils.keys import P2pkhAddress, P2shAddress, PrivateKey
from bitcoinutils.script import Script
setup('testnet')
#create bitcoin key for CA
ca_private_key = PrivateKey('cQkxgWYwE16rWDEC1FZmrAX3jzzaCfp8Fx8VpqxevoKUD3f1zgfE')
ca_public_key = ca_private_key.get_public_key()

#create bitcoin key for server
server_private_key = PrivateKey('cNHzh3a2Rsry9EEmtVg29WgehYKpApoxtjrYCeVKWjJmV4fJKxVJ')
server_public_key = server_private_key.get_public_key()

#generate bitcoin address for CA
ca_address = ca_public_key.get_address()
print("CA's address:\n" + ca_address.to_string())

#generate server's bitcoin address, this will append in certificate as UID
redeem_script = Script([1, ca_public_key.to_hex(), server_public_key.to_hex(),2, 'OP_CHECKMULTISIG'])

#CA revoke a certificate(Spend an output)
message_script = Script(['OP_RETURN', '54455354'])#test
txin = TxInput('ee663fdeccd8ec608c56268933084811f1d1597477cc74cb53e565b1ac39276f', 0)
txout = TxOutput(to_satoshis(0), message_script)
change_txout = TxOutput(to_satoshis(0.0095), ca_address.to_script_pub_key())
tx = Transaction([txin], [change_txout,txout])
sig = ca_private_key.sign_input(tx, 0, redeem_script)
txin.script_sig = Script(['OP_0',sig, redeem_script.to_hex()])#OP_0 due to stack reason
signed_tx = tx.serialize()
print("\nRaw signed transaction(ready to be broadcasted):\n" + signed_tx)
print("\nTxId:", tx.get_txid())
#send(signed_tx)