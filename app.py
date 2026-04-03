from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

# ----------- FREE API (OpenStreetMap) -----------

def get_coordinates(place):
    url = f"https://nominatim.openstreetmap.org/search?q={place}&format=json"
    headers = {"User-Agent": "food-delivery-app"}
    response = requests.get(url, headers=headers).json()
    
    if len(response) == 0:
        return None, None
    
    lat = response[0]['lat']
    lon = response[0]['lon']
    
    return lat, lon


def get_distance(origin, destination):
    lat1, lon1 = get_coordinates(origin)
    lat2, lon2 = get_coordinates(destination)

    if lat1 is None or lat2 is None:
        return 5

    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    response = requests.get(url).json()

    try:
        distance = response['routes'][0]['distance']
        return distance / 1000
    except:
        return 5

# ------------------------------------------------

#  Landing page (first open hoga)
@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/about")
def about():
    return render_template("about.html")

#  Prediction page
@app.route("/predict_page")
def home():
    return render_template("index.html")



@app.route("/predict", methods=["POST"])
def predict():
    origin = request.form["origin"]
    destination = request.form["destination"]

    
    prep_time = int(request.form["prep_time"])
    traffic = int(request.form["traffic"])

    distance = get_distance(origin, destination)


    prediction = model.predict([[distance, prep_time, traffic]])

    return render_template(
        "index.html",
        prediction_text=f"Estimated Delivery Time: {round(prediction[0],2)} minutes",
        distance=round(distance, 2)
    )


if __name__ == "__main__":
    app.run(debug=True)