# NFT Visualization Toolbox

This repository contains tools for data visualizing non-fungible tokens on Ethereum.

## Requirements
Python 3.6 <=

## Setup 
        pip install -r requirements.txt
        python config.py default_args #(I used my infura project's mainnet endpoint)

## How to use
        python show.py <template filename> <contract filename> <list of token ids (separated by comma)>

## Examples 
        python show.py sales cryptopunks 4152,4153

   ![alt text](/nft_visualization_toolbox/imgs/example1.png)

        python show.py nft_w_qr cryptopunks 4152

   ![alt text](/nft_visualization_toolbox/imgs/example3.png)

