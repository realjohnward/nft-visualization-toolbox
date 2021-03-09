# NFT Visualization Toolbox

This repository contains tools for data visualizing non-fungible tokens on Ethereum.

## Requirements
Python 3.6 >=

## Setup 
1) Install required packages
        pip install -r requirements.txt
2) Configure default arguments: mainnet_url is required (I used my infura project's mainnet endpoint)
        python config.py default_args

## How to use
        python show.py <template filename> <contract filename> <list of token ids (separated by comma)>

## Examples 
        python show.py sales cryptopunks 4152,4153

   ![alt text](/nft_visualization_toolbox/imgs/example1.png)

        python show.py bids cryptopunks 4152,4153

   ![alt text](/nft_visualization_toolbox/imgs/example2.png)

