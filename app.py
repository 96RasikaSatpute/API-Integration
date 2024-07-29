import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# Loaded API keys from environment variables
yelpAPIKey = 'nNF-wLi4ecF2w2QRpIQEoopptw4NwZNujhBXc1VNK0qDV2gC0HlqJ_XVIshNuhisfeD3dmcLcbm_ji0Xhl_l-v_jFXUZ623kiTx5bwpKgIPHu11kPURuPLGg9BFrZnYx'
GooglemapsApiKey = 'AIzaSyA52VJEnX8ec4zOmEDR-MpdxeGPzKs7s-E'

# API endpoints are defined for fetching data
YelpApiEndpoint = 'https://api.yelp.com/v3/businesses/search'
GooglemapsEndpoint = 'https://maps.googleapis.com/maps/api/geocode/json'


# Function for handling the root URL '/' route
# GET and POST requests are handled
@app.route('/', methods=['GET', 'POST'])
def fetching_data():
    # Receiving the form values 
    if request.method == 'POST':
        location = request.form['location']

        # Geocode location parameters using Google Maps API
        geocode_parameters = {
            'address': location,
            'key': GooglemapsApiKey
        }
        geocode_responses = requests.get(GooglemapsEndpoint, params=geocode_parameters)
        geocode_data = geocode_responses.json()
        try:
            if geocode_data['status'] == 'OK':
                # Getting coordinates from geocoding responses
                coordinates = geocode_data['results'][0]['geometry']['location']
                lat = coordinates['lat']
                lng = coordinates['lng']

                # Making request to Yelp using google coordinates and search cuisine
                headers = {
                    'Authorization': f'Bearer {yelpAPIKey}'
                }

                # Setting parameters for yelp api with search limit 10 for result
                yelp_parameters = {
                    'latitude': lat,
                    'longitude': lng,
                    'location': location,
                    'limit': 10
                }
                yelp_responses = requests.get(YelpApiEndpoint, headers=headers, params=yelp_parameters)
                yelp_data = yelp_responses.json()

                # Extracting list of restaurants from yelp responses
                list_of_restaurants = yelp_data.get('businesses', [])

                return render_template('restaurants.html', restaurants=list_of_restaurants)
            else:
                # Handling errors if geocoding fails
                error_messages = "Geocoding failed. Please try again."
                return render_template('index.html', error=error_messages)
        except requests.exceptions.RequestException:
            # Handling errors if there is an issue while making API requests
            error_messages = "Error occurred while making API requests. Please try again."
            return render_template('index.html', error=error_messages)
    return render_template('index.html')

# Start of the code
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
