import json
config = json.load(open("config.json"))

def generate_cassio_conf():
    return {
        "pipeline":{
            "Cache":{},
            "SQLStore":{
                "connection_string":config['database']['connection_string'],
                "package":"cassiopeia_sqlstore.SQLStore",
                "pool_size": config["threads"]
            },        
            "DDragon":{},
            "RiotAPI":{}
        }
    }