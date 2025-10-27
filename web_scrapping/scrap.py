def search_by_local_image(image_path):
    """Upload and search by local image file"""
    
    url = "https://www.google.com/searchbyimage/upload"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    with open(image_path, 'rb') as img:
        files = {'encoded_image': img}
        response = requests.post(url, files=files, headers=headers, allow_redirects=True)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if href and 'url?q=' in href:
            actual_url = href.split('url?q=')[1].split('&')[0]
            actual_url = urllib.parse.unquote(actual_url)
            
            if any(shop in actual_url.lower() for shop in ['amazon', 'ebay', 'nike', 'adidas', 'flipkart', 'shop']):
                if actual_url not in links:
                    links.append(actual_url)
    
    return links