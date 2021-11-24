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
redeem_script = Script(['OP_1', ca_public_key.to_hex(), server_public_key.to_hex(),'OP_2', 'OP_CHECKMULTISIG'])
certificate_address = P2shAddress.from_script(redeem_script)
print("\ncertificate's address:\n" + certificate_address.to_string())

#create a multisig transaction and send it
txin = TxInput('8a0e04c45a2d29fe44811c255d70351f9629ada1c3cde0ce181c0b9d23da4467', 1)
txout = TxOutput(to_satoshis(0.01), redeem_script.to_p2sh_script_pub_key() 
change_txout = TxOutput(to_satoshis(0.005), ca_address.to_script_pub_key())
tx = Transaction([txin], [txout, change_txout])
sig = ca_private_key.sign_input(tx, 0, ca_address.to_script_pub_key() )
txin.script_sig = Script([sig, ca_public_key.to_hex()])
signed_tx = tx.serialize()
print("\nRaw signed transaction(ready to be broadcasted):\n" + signed_tx)
print("\nTxId:", tx.get_txid())
#send(signed_tx)