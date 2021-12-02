

from flask import Flask, render_template
import requests

app = Flask(__name__) # Create the app app.config['TEMPLATES_AUTO_RELOAD'] = True # This will make sure we don't need to restart the server each time we change something to the layout of the webpage

rypto_data = None # We will reuse this object everytime we render the homepage.
# You can also decide not to reuse it, but we'll have to think about API request limitation 
# and on top of that, having it cached will make it render faster

@app.route("/") # Tell the server to use this function when '/' is the url
def main():
    global crypto_data
    if crypto_data is None: # If crypto_data is not yet defined, make the API request
        crypto_data = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?sort=market_cap&start=1&cryptocurrency_type=tokens&convert=BTC', headers={'X-CMC_PRO_API_KEY': 'YOUR_API_KEY'}) # Replace YOUR_API_KEY with the key in your account
        crypto_data = crypto_data.json() # Transform the received data into JSON so we can use it
    return render_template('index.html', crypto_data=crypto_data) # Render the html

@app.route("/information/<string:crypto>") # crypto will be the name of the variable
def crypto(crypto): # Add the name of the variable so we can use it
    json = requests.get('https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol=' + crypto + '&convert=BTC', headers={'X-CMC_PRO_API_KEY': 'YOUR_API_KEY'})
    json = json.json()
    return render_template('crypto.html', data=json, crypto=crypto) # Pass two variables to the template: data (which is retrieved from the API) and crypto (Which is the symbol from the url)

# Run the app
if __name__ == "__main__":
    app.run(port=5000) # Run the app on port 5000 (localhost:5000)
