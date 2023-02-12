from flask import jsonify
from flask import Flask
from flask import request
from eth_account import Account
import secrets
from web3 import Web3, HTTPProvider
from web3.gas_strategies.rpc import rpc_gas_price_strategy
from flaskext.mysql import MySQL
import requests
import pymysql
import datetime
from pytz import timezone

application = Flask(__name__)

mysql = MySQL()
application.config['MYSQL_DATABASE_USER'] = 'memorics'
application.config['MYSQL_DATABASE_PASSWORD'] = 'qwer12#$'
application.config['MYSQL_DATABASE_DB'] = 'wallet'
application.config['MYSQL_DATABASE_HOST'] = 'wallet-final-rds-prod.ceoqqcpbjmec.ap-northeast-2.rds.amazonaws.com'
application.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(application)

token_address = "0xADfafBf05d3D74aF537bDEC348Ce4e536d99fb95"
token_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"releaseTime","type":"uint256"}],"name":"Lock","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Unlock","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"}],"name":"autoUnlock","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"}],"name":"balanceOfTotal","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"locked","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"lockInfo","outputs":[{"internalType":"uint256","name":"releaseTime","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"}],"name":"releaseLock","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"locked","type":"address"}],"name":"totalLocked","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"releaseTime","type":"uint256"}],"name":"transferWithLock","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256","name":"idx","type":"uint256"}],"name":"unlock","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'

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

@application.route('/getPrice', methods=['POST'])
async def getPrice():

    try:
        _json = request.json   
        _count = _json['count']
        _type = _json['type']
        url_won = "https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD"
        response_2 = requests.get(url_won,params={})
        won = response_2.json()[0]["basePrice"]
        if _type == "eth":
            
            datas = {}
            eth_num = _count
            url_eth = "https://api.lbkex.com//v2/supplement/ticker/price.do?symbol=eth_usdt"
            response = requests.get(url_eth,params=datas)
            eth_price = float(response.json()["data"][0]["price"])
            usdt = round(eth_num * eth_price, 4)
            krw = round(won*usdt)
            massage = {
                'count':eth_num,
                'krw':format(krw,","),
                'usdt':format(usdt,","),
            }
            respone = jsonify(massage)
            respone.status_code = 200
        elif _type == "xml":

            datas = {}
            xml_num = _count
            url_xml = "https://api.lbkex.com//v2/supplement/ticker/price.do?symbol=xml_usdt"
            response = requests.get(url_xml,params=datas)
            xml_price = float(response.json()["data"][0]["price"])
            usdt = round(xml_num * xml_price)
            krw = round(won*usdt)
            massage = {
                'count':xml_num,
                'krw':format(krw,","),
                'usdt':format(usdt,","),
            }
            respone = jsonify(massage)
            respone.status_code = 200
        else:
            massage = {
                'count':None,
                'krw':None,
                'usdt':None,
            }
            respone = jsonify(massage)
            respone.status_code = 400
        
    except Exception as e:
        massage = {
                'count':None,
                'krw':None,
                'usdt':None,
            }
        respone = jsonify(massage)
        respone.status_code = 500
        #conn.rollback()
        print(e)
    finally:
        
        #cursor.close() 
        #conn.close()  
        return respone

@application.route('/getPriceAll', methods=['POST'])
async def getPriceAll():

    try:
        _json = request.json   
        _count_xml = _json['xml']
        _count_eth = _json['eth']
        url_won = "https://quotation-api-cdn.dunamu.com/v1/forex/recent?codes=FRX.KRWUSD"
        response_2 = requests.get(url_won,params={})
        won = response_2.json()[0]["basePrice"]
        if _count_xml and _count_eth:
            
            datas = {}
            eth_num = float(_count_eth)
            xml_num = float(_count_xml)
            url_eth = "https://api.lbkex.com//v2/supplement/ticker/price.do?symbol=eth_usdt"
            url_xml = "https://api.lbkex.com//v2/supplement/ticker/price.do?symbol=xml_usdt"
            response_eth = requests.get(url_eth,params=datas)
            response_xml = requests.get(url_xml,data={})
            eth_price = float(response_eth.json()["data"][0]["price"])
            xml_price = float(response_xml.json()["data"][0]["price"])
            eth_usdt = round(eth_num * eth_price, 4)
            eth_krw = round(won*eth_usdt)

            xml_usdt = round(xml_num * xml_price, 4)
            xml_krw = round(won*xml_usdt)

            massage = {
                'eth_count':eth_num,
                'eth_krw':format(eth_krw,","),
                'eth_usdt':format(eth_usdt,","),
                'xml_count':xml_num,
                'xml_krw':format(xml_krw,","),
                'xml_usdt':format(xml_usdt,","),
                'total_krw':format(eth_krw+xml_krw,","),
                'total_usdt':format(eth_usdt+xml_usdt,","),
            }
            respone = jsonify(massage)
            respone.status_code = 200
       
        else:
            massage = {
                'eth_count':eth_num,
                'eth_krw':None,
                'eth_usdt':None,
                'xml_count':xml_num,
                'xml_krw':None,
                'xml_usdt':None,
            }
            respone = jsonify(massage)
            respone.status_code = 400
        
    except Exception as e:
        massage = {
                'count':None,
                'krw':None,
                'usdt':None,
            }
        respone = jsonify(massage)
        respone.status_code = 500
        #conn.rollback()
        print(e)
    finally:
        
        #cursor.close() 
        #conn.close()  
        return respone

@application.route('/trans_eth', methods=['POST'])
async def trans_eth():
    print("start")
    sqlQuery_0 = """UPDATE tb_point_history
                        SET transaction_hash = %s,
                            commission = %s,
                            approve_dt = %s,
                            status = %s
                        WHERE idx = %s"""
    try:
        print("test0")
        web3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/03140aaea4f94153992f71b4c4214d4b'))
        _json = request.json   
        _from_private_key = _json['from_private_key']
        _from_pub_key = _json['from_pub_key']
        _to_pub_key = _json['to_pub_key']
        _eth_num = float(_json['eth_num'])
        _history_key = _json['history_key']
        print("test1")
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        now_dt = datetime.datetime.now(timezone("Asia/Seoul"))
        now_uttm = int(round(datetime.datetime.now(timezone("Asia/Seoul")).timestamp()))	
        address_to = _to_pub_key

        

        ###############선언부################
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
                "value": Web3.to_wei(_eth_num, "ether")
            },
            _from_private_key,
        )
        print("test")
        # 6. Send tx and wait for receipt
        tx_hash = web3.eth.send_raw_transaction(tx_create.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        gas_price = tx_receipt.effectiveGasPrice
        gas_used = tx_receipt.gasUsed

        transection_fee = Web3.from_wei(gas_price*gas_used ,"ether")
        print(f"Transaction successful with hash: { tx_receipt.transactionHash.hex() }")

        bindData_0 = (tx_hash.hex(),transection_fee,now_dt,"success",_history_key)
        cursor.execute(sqlQuery_0,bindData_0)
        massage = {
                'status' : 200,
                'result_code' : 230,
                'tx_hash' : tx_hash.hex(),
                'tx_receipt' : {
                    "blockHash" : str(tx_receipt.blockHash.hex()),
                    "effectiveGasPrice": str(tx_receipt.effectiveGasPrice),
                    "transection_fee" : transection_fee,
                    "from" : str(tx_receipt.get("from")),
                    "to" : str(tx_receipt.get("to")),
                   
                },
                'msg' : "successfully transfer"
                }
        respone = jsonify(massage)
        respone.status_code = 200



    except Exception as e:
        print("exception")
        conn.rollback()
        bindData_0 = (None,None,now_dt,"fail",_history_key)
        cursor.execute(sqlQuery_0,bindData_0)
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
        conn.commit()
        cursor.close() 
        conn.close()  
        return respone

@application.route('/trans_xml', methods=['POST'])
async def trans_xml():
    print("start")
    token_address = "0xADfafBf05d3D74aF537bDEC348Ce4e536d99fb95"
    token_abi = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"releaseTime","type":"uint256"}],"name":"Lock","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":false,"internalType":"uint256","name":"amount","type":"uint256"}],"name":"Unlock","type":"event"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"}],"name":"autoUnlock","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"holder","type":"address"}],"name":"balanceOfTotal","outputs":[{"internalType":"uint256","name":"balance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"burnFrom","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"locked","type":"address"},{"internalType":"uint256","name":"index","type":"uint256"}],"name":"lockInfo","outputs":[{"internalType":"uint256","name":"releaseTime","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"}],"name":"releaseLock","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"locked","type":"address"}],"name":"totalLocked","outputs":[{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"length","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"releaseTime","type":"uint256"}],"name":"transferWithLock","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"uint256","name":"idx","type":"uint256"}],"name":"unlock","outputs":[{"internalType":"bool","name":"success","type":"bool"}],"stateMutability":"nonpayable","type":"function"}]'

    sqlQuery_0 = """UPDATE tb_point_history
                        SET transaction_hash = %s,
                            commission = %s,
                            approve_dt = %s,
                            status = %s
                        WHERE idx = %s"""
    try:
        print("test0")
        web3 = Web3(HTTPProvider('https://mainnet.infura.io/v3/03140aaea4f94153992f71b4c4214d4b'))
        _json = request.json   
        _from_private_key = _json['from_private_key']
        _from_pub_key = _json['from_pub_key']
        _to_pub_key = _json['to_pub_key']
        _xml_num = float(_json['xml_num'])
        _history_key = _json['history_key']
        token_contract = web3.eth.contract(token_address, abi=token_abi)
        #token balance
        token_balance = web3.from_wei(token_contract.functions.balanceOf(_from_pub_key).call(),"ether")
        print("tokenbalance : ", token_balance)
        #transfer



        print("test1")
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        now_dt = datetime.datetime.now(timezone("Asia/Seoul"))
        now_uttm = int(round(datetime.datetime.now(timezone("Asia/Seoul")).timestamp()))	
        address_to = _to_pub_key


        # Set the gas price strategy
        web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)


        nonce = web3.eth.get_transaction_count(_from_pub_key)
        print("test2")
        transaction = token_contract.functions.transfer(address_to, Web3.to_wei(_xml_num, "ether")).build_transaction({
            "nonce":nonce,
            "gas":200000,
            "gasPrice":web3.eth.gas_price,
        })
        # Send tx and wait for receipt
        sign_transaction = web3.eth.account.sign_transaction(transaction,_from_private_key)
        tx_hash = web3.eth.send_raw_transaction(sign_transaction.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

        gas_price = tx_receipt.effectiveGasPrice
        gas_used = tx_receipt.gasUsed
     

        ###############선언부################
        print("test2")
        
        transection_fee = Web3.from_wei(gas_price*gas_used ,"ether")
        print(f"Transaction successful with hash: { tx_receipt.transactionHash.hex() }")

        bindData_0 = (tx_hash.hex(),transection_fee,now_dt,"success",_history_key)
        cursor.execute(sqlQuery_0,bindData_0)
        massage = {
                'status' : 200,
                'result_code' : 230,
                'tx_hash' : tx_hash.hex(),
                'tx_receipt' : {
                    "blockHash" : str(tx_receipt.blockHash.hex()),
                    "effectiveGasPrice": str(tx_receipt.effectiveGasPrice),
                    "transection_fee" : transection_fee,
                    "from" : str(tx_receipt.get("from")),
                    "to" : str(tx_receipt.get("to")),
                   
                },
                'msg' : "successfully transfer"
                }
        respone = jsonify(massage)
        respone.status_code = 200



    except Exception as e:
        print("exception")
        conn.rollback()
        bindData_0 = (None,None,now_dt,"fail",_history_key)
        cursor.execute(sqlQuery_0,bindData_0)
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
        conn.commit()
        cursor.close() 
        conn.close()  
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