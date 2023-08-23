
def data_collection():

    from bs4 import BeautifulSoup
    import requests
    import json
    import math
    import pandas as pd
    from nested_lookup import nested_lookup
    from tqdm import tqdm
    from requests_ip_rotator import ApiGateway

    def parseNextCache(url, session):
        page = session.get(url)
        soup = BeautifulSoup(page.text, 'html') 
        script = soup.find('script', {'id': '__NEXT_DATA__'})
        data = json.loads(script.text)
        return data
    
    def parseIndexPages(url):

        # # Create gateway object and initialize in AWS
        gateway = ApiGateway(url)
        gateway.start()

        # Assign gateway to session
        session = requests.Session()
        session.mount(url, gateway)

        data = parseNextCache(url, session)
        
        _first_page_results = nested_lookup("results", data)[0]
        _paging_info = _first_page_results["pageInfo"]
        total_pages = _paging_info["pageCount"] or math.ceil(_paging_info["total"] / _paging_info["limit"])
        product_previews = [edge["node"] for edge in _first_page_results["edges"]]
        product_sales = [salesInfo['lastSale'] for salesInfo in nested_lookup("salesInformation", data)]

        for i in tqdm(range(125)): # total_pages-2
            current_url = f"{url}&page={i+2}"
            data = parseNextCache(current_url, session)
            _page_results = nested_lookup("results", data)[0]
            product_previews.extend([edge["node"] for edge in _page_results["edges"]])
            product_sales.extend([salesInfo['lastSale'] for salesInfo in nested_lookup("salesInformation", data)])
        
        gateway.shutdown()
        return product_previews, product_sales
    

    url = "https://stockx.com/search?s=sneakers"
    preview, sales = parseIndexPages(url)
    df  = pd.DataFrame(preview)
    df['last sale'] = sales

    df.to_csv(path_or_buf="/Users/FranklinZhao/TensorFlowProjects/ImageBasedSneakerPrediction/data/raw/" + "5000_output.csv", sep='\t')

    

    