from flask import Flask, render_template, request, redirect, url_for, session
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session

# Load models and encoders
encoders = joblib.load("model/encoders.pkl")
rf_model = joblib.load("model/rf_model.pkl")
usage_model = joblib.load("model/usage_type_model.pkl")
duration_model = joblib.load("model/duration_model.pkl")
fuel_model = joblib.load("model/fuel_type_model.pkl")

@app.route("/", methods=["GET", "POST"])
def index():
    # Dropdown values from label encoders
    vehicle_classes = encoders["vehicleClass"].classes_
    model_descs = encoders["modelDesc"].classes_
    offices = encoders["OfficeCd"].classes_

    if request.method == "POST":
        try:
            # Get form inputs
            vehicle_class = request.form["vehicle_class"]
            model_desc = request.form["model_desc"]
            office = request.form["office"]
            month = int(request.form["month"])

            # Encode inputs
            vc_encoded = encoders["vehicleClass"].transform([vehicle_class])[0]
            md_encoded = encoders["modelDesc"].transform([model_desc])[0]
            of_encoded = encoders["OfficeCd"].transform([office])[0]

            input_data = np.array([[vc_encoded, md_encoded, of_encoded, month]])

            # Predictions
            reg_count = int(rf_model.predict(input_data)[0])
            usage_type_encoded = usage_model.predict(input_data)[0]
            usage_type = encoders["usage_type"].inverse_transform([usage_type_encoded])[0]

            duration = int(duration_model.predict(input_data)[0])
            duration_str = f"{duration} year" if duration == 1 else f"{duration} years"

            fuel_encoded = fuel_model.predict(input_data)[0]
            fuel_group = encoders["fuel"].inverse_transform([fuel_encoded])[0]

            # Store prediction in session
            session['prediction'] = {
                "reg_count": reg_count,
                "usage_type": usage_type,
                "duration": duration_str,
                "fuel_group": fuel_group
            }

        except Exception as e:
            session['prediction'] = {
                "error": f"Error: {str(e)}. Please check your inputs."
            }

        return redirect(url_for('result'))

    return render_template("index.html",
                           vehicle_classes=vehicle_classes,
                           model_descs=model_descs,
                           offices=offices)

@app.route("/result")
def result():
    prediction = session.get("prediction")
    return render_template("result.html", prediction=prediction)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)
