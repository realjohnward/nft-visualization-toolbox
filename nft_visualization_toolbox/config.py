import sys 
import json 


cfg_type = sys.argv[1]
print(cfg_type)

if cfg_type == "default_args":
    new_default_args = {}
    default_args = {"mainnet_url": None}
    for k,v in default_args.items():
        print(k + "?")
        answer = input("> ")
        new_default_args[k] = answer 

    json.dump(new_default_args, open("./config/default_args.json", "w"))
    print("Done")
