from flask import Flask, render_template, request, jsonify, session
import cfscrape
from bs4 import BeautifulSoup
import time
import json
import os
from auth import auth, login_required, token_required
import cloudscraper

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Register blueprint
app.register_blueprint(auth)

def Seturl(url, retry=False):
    client = cfscrape.create_scraper(delay=10)
    DOMAIN = "https://set.seturl.in/"
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://loan.techzed.in/"
    h_get = {"referer": ref}
    h_post = {"x-requested-with": "XMLHttpRequest", "referer": final_url, "content-type": "application/x-www-form-urlencoded"}

    try:
        resp = client.get(final_url, headers=h_get)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs if input.get("name")}

        if not data:
            return "No form data found. The page structure might have changed."

        time.sleep(7)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h_post)
        return str(r.json()["url"])
    except BaseException as e:
        if not retry:
            print(f"Error occurred: {e}. Retrying...")
            return Seturl(url, retry=True)
        else:
            return "Something went wrong, Please Wait For Few Seconds and try again..."
        
def runurl(url, retry=False):
    client = cfscrape.create_scraper(delay=10)
    DOMAIN = "https://get.runurl.in/"
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://techzed.in/"
    h_get = {"referer": ref}
    h_post = {"x-requested-with": "XMLHttpRequest", "referer": final_url, "content-type": "application/x-www-form-urlencoded"}

    try:
        resp = client.get(final_url, headers=h_get)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        data = {input.get("name"): input.get("value") for input in inputs if input.get("name")}

        if not data:
            return "No form data found. The page structure might have changed."

        time.sleep(7)
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h_post)
        return str(r.json()["url"])
    except BaseException as e:
        if not retry:
            print(f"Error occurred: {e}. Retrying...")
            return Seturl(url, retry=True)
        else:
            return "Something went wrong, Please Wait For Few Seconds and try again..."

def Runurl_in(url, retry=False):
    client = cfscrape.create_scraper(delay=10)
    DOMAIN = "https://get.runurl.in/"  # Domain for scraping
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://loan.newsaddapro.in/"  # Referrer URL
    h_get = {"referer": ref}

    try:
        # Initial GET request to fetch the page content
        resp = client.get(final_url, headers=h_get)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        
        # Collecting form data
        data = {input.get("name"): input.get("value") for input in inputs if input.get("name")}

        if not data:
            #return "No form data found. The page structure might have changed."
            return Runurl_in1(url, delay=7)

        time.sleep(8)  # Wait time for better reliability
        h_post = {"x-requested-with": "XMLHttpRequest"}  # Headers for POST request
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h_post)
        
        # Attempt to retrieve the final URL
        try:
            return str(r.json()["url"])
        except KeyError:
            #return "Final URL not found in response."
            return Runurl_in1(url, delay=7)
    except BaseException as e:
        if not retry:
            print(f"Error occurred: {e}. Retrying...")
            #return Seturl(url, retry=True)
            return Runurl_in1(url, delay=7)
        else:
            #return "Something went wrong, Please Wait For Few Seconds and try again..."
            return Runurl_in1(url, delay=7)

def Runurl_in1(url, delay=0):
    """
    Fetches the final URL from a runurl.in shortlink after a specified delay.

    Args:
        url (str): The runurl.in shortlink.
        delay (int, optional): The number of seconds to wait before execution. Defaults to 0.

    Returns:
        str: The final URL if successful, otherwise "Something went wrong :(".
    """
    print(f"[+] Waiting for {delay} seconds before processing...")
    time.sleep(delay)  # Wait for the specified delay
    time.sleep(5)


    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://get.runurl.in"
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://loan.newsaddapro.in/"
    ref = referurl
    h = {"referer": ref}
    resp = client.get(final_url, headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = {input.get("name"): input.get("value") for input in inputs}
    h = {"x-requested-with": "XMLHttpRequest"}
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return str(r.json()["url"])
    except BaseException:
        return "Something went wrong :("

def Seturl_in(url, retry=False):
    client = cfscrape.create_scraper(delay=10)
    DOMAIN = "https://set.seturl.in/"  # Domain for scraping
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://loan.techzed.in/"  # Referrer URL
    h_get = {"referer": ref}

    try:
        # Initial GET request to fetch the page content
        resp = client.get(final_url, headers=h_get)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        
        # Collecting form data
        data = {input.get("name"): input.get("value") for input in inputs if input.get("name")}

        if not data:
            #return "No form data found. The page structure might have changed."
            return Seturl_in1(url, delay=7)

        time.sleep(8)  # Wait time for better reliability
        h_post = {"x-requested-with": "XMLHttpRequest"}  # Headers for POST request
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h_post)
        
        # Attempt to retrieve the final URL
        try:
            return str(r.json()["url"])
        except KeyError:
            #return "Final URL not found in response."
            return Seturl_in1(url, delay=7)
    except BaseException as e:
        if not retry:
            print(f"Error occurred: {e}. Retrying...")
            #return Seturl(url, retry=True)
            return Seturl_in1(url, delay=7)
        else:
            #return "Something went wrong, Please Wait For Few Seconds and try again..."
            return Seturl_in1(url, delay=7)

def Seturl_in1(url, delay=0):
    """
    Fetches the final URL from a runurl.in shortlink after a specified delay.

    Args:
        url (str): The runurl.in shortlink.
        delay (int, optional): The number of seconds to wait before execution. Defaults to 0.

    Returns:
        str: The final URL if successful, otherwise "Something went wrong :(".
    """
    print(f"[+] Waiting for {delay} seconds before processing...")
    time.sleep(delay)  # Wait for the specified delay
    time.sleep(5)


    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://set.seturl.in/"
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://loan.techzed.in/"
    ref = referurl
    h = {"referer": ref}
    resp = client.get(final_url, headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = {input.get("name"): input.get("value") for input in inputs}
    h = {"x-requested-with": "XMLHttpRequest"}
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return str(r.json()["url"])
    except BaseException:
        return "Something went wrong :("

def Modijiurl_in(url, retry=False):
    client = cfscrape.create_scraper(delay=10)
    DOMAIN = "https://modijiurl.com/"  # Domain for scraping
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://mazakisan.com/"  # Referrer URL
    h_get = {"referer": ref}

    try:
        # Initial GET request to fetch the page content
        resp = client.get(final_url, headers=h_get)
        soup = BeautifulSoup(resp.content, "html.parser")
        inputs = soup.find_all("input")
        
        # Collecting form data
        data = {input.get("name"): input.get("value") for input in inputs if input.get("name")}

        if not data:
            #return "No form data found. The page structure might have changed."
            return Modijiurl_in1(url, delay=7)

        time.sleep(8)  # Wait time for better reliability
        h_post = {"x-requested-with": "XMLHttpRequest"}  # Headers for POST request
        r = client.post(f"{DOMAIN}/links/go", data=data, headers=h_post)
        
        # Attempt to retrieve the final URL
        try:
            return str(r.json()["url"])
        except KeyError:
            #return "Final URL not found in response."
            return Modijiurl_in1(url, delay=7)
    except BaseException as e:
        if not retry:
            print(f"Error occurred: {e}. Retrying...")
            #return Seturl(url, retry=True)
            return Modijiurl_in1(url, delay=7)
        else:
            #return "Something went wrong, Please Wait For Few Seconds and try again..."
            return Modijiurl_in1(url, delay=7)

def Modijiurl_in1(url, delay=0):
    """
    Fetches the final URL from a runurl.in shortlink after a specified delay.

    Args:
        url (str): The runurl.in shortlink.
        delay (int, optional): The number of seconds to wait before execution. Defaults to 0.

    Returns:
        str: The final URL if successful, otherwise "Something went wrong :(".
    """
    print(f"[+] Waiting for {delay} seconds before processing...")
    time.sleep(delay)  # Wait for the specified delay
    time.sleep(5)


    client = cloudscraper.create_scraper(allow_brotli=False)
    DOMAIN = "https://modijiurl.com/"
    url = url[:-1] if url[-1] == "/" else url
    code = url.split("/")[-1]
    final_url = f"{DOMAIN}/{code}"
    ref = "https://mazakisan.com/"
    h = {"referer": ref}
    resp = client.get(final_url, headers=h)
    soup = BeautifulSoup(resp.content, "html.parser")
    inputs = soup.find_all("input")
    data = {input.get("name"): input.get("value") for input in inputs}
    h = {"x-requested-with": "XMLHttpRequest"}
    time.sleep(8)
    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)
    try:
        return str(r.json()["url"])
    except BaseException:
        return "Something went wrong :("

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/check_url', methods=['POST'])
@login_required
@token_required
def check_url():
    url = request.json.get('url', '')
    if 'runurl.in' in url:
        result = Runurl_in(url)
    elif 'seturl.in' in url:
        result = Seturl_in(url)
    elif 'modijiurl.com' in url:
        result = Modijiurl_in(url)
    else:
        result = "URL not supported. Please provide a valid runurl.in or seturl.in or modiji.in URL."
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True) 
