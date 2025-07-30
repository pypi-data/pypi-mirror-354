import decimal
import os
import sys
import time

from apexomni.helpers.util import round_size

from apexomni.http_private_sign import HttpPrivateSign
import os
import sys
import time

from apexomni.http_private_sign import HttpPrivateSign

root_path = os.path.abspath(__file__)
root_path = '/'.join(root_path.split('/')[:-2])
sys.path.append(root_path)

from apexomni.constants import NETWORKID_TEST, APEX_OMNI_HTTP_TEST, APEX_OMNI_HTTP_MAIN, NETWORKID_OMNI_MAIN_ARB

print("Hello, Apex omni")

key = 'fbfd1d5d-7b7f-cd3b-d543-cc967358b4ed'
secret = 'SBWzi6gquvTlE7bh5aKWRNZh8XPI1lekCVz7RN7x'
passphrase = 'eIseQZzgyjwac5_Xmk7z'
#seeds = 'b3548ef2c22182bbc9e9a546583a49a176a95b0fa664ad0ce2711a6b9367a4523ab483df26844a7163dbc3701507e9c39e39ec714bf04a8eb710785c24c29f251b'
#l2Key = '0x711df5ffc57b033b22c65e38e4b3d8b1947eaee7403aaa4ff5847d31ca0b0700'
seeds = 'be6e8018468dfb458946f6b0b69927cfe9410c9af3a2851df969f246391c39034fd596fcb85be0112d49c3354b067ac69007a70bb20805322e71cd16a7931de31c'
l2Key = '0xe4c45d7a576f4eaef99c8a25eec9342f6f013baf31554151bda845bebfa030a6'

client = HttpPrivateSign(APEX_OMNI_HTTP_MAIN, network_id=NETWORKID_OMNI_MAIN_ARB,
                         zk_seeds=seeds,zk_l2Key=l2Key,
                         api_key_credentials={'key': key, 'secret': secret, 'passphrase': passphrase})
configs = client.configs_v3()
accountData = client.get_account_v3()


currentTime = time.time()
createOrderRes = client.create_order_v3(symbol="BTC-USDT", side="SELL",
                                        type="MARKET", size="0.01", timestampSeconds= currentTime,
                                        price="113222.2")
print(createOrderRes)

# sample6
# Create a  TP/SL order
# first, Set a slippage to get an acceptable slPrice or tpPrice
#slippage is recommended to be greater than 0.1
# when buying, the price = price*(1 + slippage). when selling, the price = price*(1 - slippage)
slippage = decimal.Decimal("-0.1")
slPrice =  decimal.Decimal("58000") * (decimal.Decimal("1") + slippage)
tpPrice =  decimal.Decimal("79000") * (decimal.Decimal("1") - slippage)

createOrderRes = client.create_order_v3(symbol="BTC-USDT", side="BUY",
                                     type="LIMIT", size="0.01",
                                     price="65000",
                                     isOpenTpslOrder=True,
                                     isSetOpenSl=True,
                                     slPrice=slPrice,
                                     slSide="SELL",
                                     slSize="0.01",
                                     slTriggerPrice="58000",
                                     isSetOpenTp=True,
                                     tpPrice=tpPrice,
                                     tpSide="SELL",
                                     tpSize="0.01",
                                     tpTriggerPrice="79000",
                                     )
print(createOrderRes)


print("end, Apex Omni")


