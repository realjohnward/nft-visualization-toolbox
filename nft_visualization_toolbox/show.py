import argparse 
import json 
import jinja2 
from env import ENV 
from datetime import datetime 
from io import BytesIO 
import pandas as pd 
import pdfkit 
from pdfkit.configuration import Configuration
from PyPDF2 import PdfFileMerger
from web3 import Web3
import os 
import webbrowser

default_args = json.load(open("./config/default_args.json"))

parser = argparse.ArgumentParser()

parser.add_argument('--mainnet_url', type=str, help='URL to mainnet ethereum node')
parser.add_argument('template', type=str, help='path to template txt file')
parser.add_argument('contract', type=str, help='path to contract json file')
parser.add_argument('ids', type=str, help='list of token ids (separate by comma)')

args = parser.parse_args()

contract_filename = args.contract 
if not contract_filename:
    contract_path = os.path.join("./config/contracts", default_args['contract'] + ".json")
else:
    contract_path = os.path.join("./config/contracts", contract_filename + ".json")

config = json.load(open(contract_path))

template_filename = args.template 
if not template_filename:
    template_path = os.path.join("./config/templates", default_args['template'] + ".txt")
else:
    template_path = os.path.join("./config/templates", template_filename + ".txt")


with open(template_path, 'r') as f:
    t = ENV.from_string(f.read())
    f.close()

with open('./config/stylesheet.css') as f:
    template_styles = f.read()
    f.close()

mainnet_url = args.mainnet_url 
if not mainnet_url:
    mainnet_url = default_args['mainnet_url']

# wkhtmltopdf_path = "../../vr_nfts/wkhtmltopdf"
# pdf_config = Configuration(wkhtmltopdf=wkhtmltopdf_path)

w3 = Web3(Web3.HTTPProvider(mainnet_url))

template_html = f'<html><head><meta name="viewport" content="width=1024"><style>{template_styles}</style></head><body>{t.render(cfg=config, w3=w3, ids=args.ids)}</body></html>'

f = open('view.html', 'w')
f.write(template_html)
f.close()

webbrowser.open_new_tab('view.html')






