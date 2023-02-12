
from flask import jsonify
from flask import Flask
from flask import request

from flask_cors import CORS, cross_origin
import requests
import json
from eth_account import Account
import secrets
from web3 import Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy

application = Flask(__name__)



@application.route('/', methods=['POST','GET'])
async def root():
    try:        
        
        respone = jsonify('hey!')
        respone.status_code = 200
        
        
    except Exception as e:
        respone = jsonify('there is an error')
        return respone
    finally:
        return respone  



@application.route('/getWallet_eth', methods=['POST'])
async def getWallet_eth():

    try:
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        print ("SAVE BUT DO NOT SHARE THIS:", private_key)
        acct = Account.from_key(private_key)
        print("Address:", acct.address)
        _wallet_pubkey = acct.address
        _wallet_seckey = private_key
       
    
        massage = {
                'status' : 200,
                'result_code' : 230,
                'pubkey' : str(_wallet_pubkey),
                'seckey' : str(_wallet_seckey)
                }
        respone = jsonify(massage)
        respone.status_code = 200
        return respone
    except Exception as e:
        massage = {
                'status' : 500,
                'result_code' : 231,
                'pubkey' : None,
                'seckey' : None
            }
        respone = jsonify(massage)
        respone.status_code = 200
        #conn.rollback()
        print(e)
    finally:
        
        #cursor.close() 
        #conn.close()  
        return respone


@application.route('/trans_eth', methods=['POST'])
async def trans_eth():
    print("start")
    try:
        print("test0")
        web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/03140aaea4f94153992f71b4c4214d4b'))
        _json = request.json   
        _from_private_key = _json['from_private_key']
        _from_pub_key = _json['from_pub_key']
        _to_pub_key = _json['to_pub_key']
        _eth_num = _json['eth_num']
        print("test1")
        
        address_to = _to_pub_key
        print("test2")
        # 4. Set the gas price strategy
        web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)

        # 5. Sign tx with PK
        tx_create = web3.eth.account.sign_transaction(
            {
                "nonce": web3.eth.get_transaction_count(_from_pub_key),
                "gasPrice": web3.eth.generate_gas_price(),
                "gas": 21000,
                "to": address_to,
                "value": web3.toWei(_eth_num, "ether")
            },
            _from_private_key,
        )
        print("test")
        # 6. Send tx and wait for receipt
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        print(f"Transaction successful with hash: { tx_receipt.transactionHash.hex() }")
        
        massage = {
                'status' : 200,
                'result_code' : 230,
                'tx_hash' : str(tx_hash),
                'tx_receipt' : str(tx_receipt),
                'msg' : "successfully transfer"
                }
        respone = jsonify(massage)
        respone.status_code = 200
        return respone

    except Exception as e:
        massage = {
                'status' : 500,
                'result_code' : 231,
                'pubkey' : None,
                'seckey' : None
            }
        respone = jsonify(massage)
        respone.status_code = 200
      
        print(e)
    finally:
        
        return respone

@application.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone
        
if __name__ == "__main__":
    application.run()