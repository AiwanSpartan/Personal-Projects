import requests 

def pokemon_info(name):
    url = f"https://pokeapi.co/api/v2/pokemon/{name}"
    info = requests.get(url)

    if(info.status_code == 200):
        data = info.json()
        print(data["name"])

        for type in data["types"]:
            print(type["type"]["name"])
        print(data["id"])
    
    else:
        print(f"unable to get data for {name}")

pokemon_info("jirachi")