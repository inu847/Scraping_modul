import json
import requests
import subprocess
import os

def scrap(keywoard):

    try:
        for newest in range(0,10000,50):
            try:
                URL = 'https://mall.shopee.co.id/api/v4/search/search_items?by=relevancy&keyword='+str(keywoard)+'&limit=50&newest='+str(newest)+'&official_mall=1&order=desc&page_type=search&version=2'
                shopeeId = requests.get(URL)
            except:
                print('Activation Tor')
                subprocess.Popen(['tor_proxy/Tor/tor.exe'])
                break

            datas = shopeeId.json()
            arrs = datas['items']
            for arr in arrs:
                itemId = arr['item_basic']['itemid']
                shopid = arr['item_basic']['shopid']
                name = arr['item_basic']['name']
                price = arr['item_basic']['price']

                print('Item ID : '+str(itemId)+'\nShopee Id : '+ str(shopid) +'\nProduct Name : '+ name+'\nPrice : '+ str(price))
                images = arr['item_basic']['images']
                print('Json Images : ')
                for image in images:
                    print('\t'+image)
                    # Download Images
                    try: 
                        os.mkdir('images') 
                    except: 
                        pass
                    response = requests.get("https://cf.shopee.co.id/file/"+image)
                    file = open("images/"+image+'.jpg', "wb")
                    file.write(response.content)
                    file.close()
                try:
                    variations = arr['item_basic']['tier_variations']
                    for variasi in variations:
                        print(variasi['name'])
                        options = variasi['options']
                        for option in options:
                            print('\t'+option)
                except:
                    options = ''
                    print('Not Variations')

                writers = open('grabShopee.txt', 'a+', encoding="utf-8")
                writers.writelines(f"{itemId}|{shopid}|{name}|{price}|{images}|{options}\n")
                writers.close()

            # IDs = open(r"grabShopee.txt", "r", encoding="utf-8")
            # keys = IDs.readlines()
            # for key in keys:
            #     results = key.strip()
            #     result = results.split("|")
            #     itemID = result[0]
            #     shopID = result[1]

            #     detailUrl = "https://mall.shopee.co.id/api/v2/item/get?itemid="+str(itemID)+"&shopid="+str(shopID)
            #     detailProduct = requests.get(detailUrl)
            #     detail = detailProduct.json()
        else:
            print("Finished Scrap")
    except:
        print("Cannot Activated Tor, Please Check IP socks5")

def scrapByKeywoard():
    urls = open(r"ShopeeKeywoard.txt", "r")
    keywoards = urls.readlines()
    # subprocess.Popen(['tor_proxy/Tor/tor.exe'])
    for key in keywoards:
        keywoard = key.replace(' ', '%20')
        keywoard = key.replace('&', '%26')
        keywoard = key.replace('-', '%20')
        scrap(keywoard)

if __name__ == '__main__':
    scrapByKeywoard()