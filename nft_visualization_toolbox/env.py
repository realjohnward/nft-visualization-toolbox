import jinja2 
import web3
from web3 import Web3
import pandas as pd 
from datetime import datetime 
from PIL import Image 
import urllib.request 
import requests 
import logging 
from base64 import b64encode 

def fmt_pctc(pctc):
    if not pctc:
        return "--" 
    else:
        pctc = round(pctc, 2)
    if pctc < 0:
        return f'<span style="color:red;">{pctc}</span>'
    else:
        return f'<span style="color:green;">{pctc}</span>'

def fmt_addr(addr):
    return f'<a href="https://etherscan.io/address/{addr}">{addr}</a>'

def fmt_txn_hash(txn_hash):
    return f'<a href="https://etherscan.io/tx/{txn_hash}">{txn_hash}</a>'

def fmt_block(block):
    return f'<a href="https://etherscan.io/block/{block}">{block}</a>'


class Contract:
    def __init__(self, cfg, w3=None,ids=""):
        self.address = Web3.toChecksumAddress(cfg['address'])
        self.contract = w3.eth.contract(address=self.address, abi=cfg['abi'])
        self.tokens = ids.split(",")
        self.id_key = cfg['id_key']
        self.nfts = [NFT(self.contract, self.id_key, id_value, w3, address=cfg['address']) for id_value in self.tokens]


class NFT:
    def __init__(self, contract, id_key, id_value, w3, img_path=None, address=None):
        self.contract = contract 
        self.img_path = img_path 
        self.w3 = w3 
        self.argument_filters = {id_key: int(id_value)}
        self.address = address 
        self.id_value = id_value 

    def events(self, event_name, fromBlock=0, toBlock='latest'):
        event_filter = getattr(self.contract.events, event_name).createFilter(fromBlock=fromBlock, 
                                                                toBlock=toBlock, 
                                                                argument_filters=self.argument_filters)

        records = []
        for event in event_filter.get_all_entries():
            receipt = self.w3.eth.waitForTransactionReceipt(event['transactionHash'])
            result = getattr(self.contract.events, event_name)().processReceipt(receipt)[0]
            txnhash = result['transactionHash'].hex()
            block = result['blockNumber']
            ts = self.w3.eth.get_block(block).timestamp
            dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            record = {"Block": block, "Txn": txnhash, "Value (Eth)": self.w3.fromWei(result['args']['value'], 'ether'), "Date": dt}
            records.append(record)

        return pd.DataFrame.from_records(records)

def nft_img(nft, classes='', w=100, h=100):
    req = requests.get(f'https://api.opensea.io/api/v1/asset/{nft.address}/{nft.id_value}/', headers={'User-Agent': 'Mozilla/5.0'})
    data = req.json()
    img_path = data['image_url']
    logging.error(f"IMAGE PATH: {img_path}")
    if img_path.startswith("http"):
        req = urllib.request.Request(img_path, headers={'User-Agent': 'Mozilla/5.0'})
        img_bytes = urllib.request.urlopen(req).read()
    else:
        img_bytes = Image.open(img_path)
    img_html = f'<img class="{classes}" width={w} height={h} src=\"data:image/png;base64,{b64encode(img_bytes).decode()}\" />'
    return img_html   

def row(nfts):
    html = f'<div class="row">'
    for nft in nfts:
        html += f'<div class="column">{nft.img_html}</div>'
    html += '</div>'
    return html 

def rows(nft_lists):
    return "".join([row(nft_list) for nft_list in nft_lists])

formatters = {"% Change": fmt_pctc, "Txn": fmt_txn_hash,"From": fmt_addr, "To": fmt_addr, "Block": fmt_block}

def table(df):
    try:
        return df.to_html(columns=['Block','Txn','Value (Eth)'],classes='Table',index=False, border=2, justify='left', escape=False, formatters=formatters)
    except KeyError:
        print("Empty table.")
        return "--"

def contract(cfg, w3=None, ids=""):
    return Contract(cfg, w3=w3, ids=ids)

ENV = jinja2.Environment(extensions=['jinja2.ext.loopcontrols'])
ENV.filters = {
    'row': row,
    'table': table,
    'contract': contract,
    'nft_img': nft_img,
}
