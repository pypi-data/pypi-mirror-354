from flask import (
    Flask,
    request,
    render_template,
    Response,
    jsonify,
)

from .tc720.controller import TC720Controller

#from tc720.mock_controller import MockTC720Controller
import sys

port = sys.argv[1]
controller = TC720Controller(port)
#controller = MockTC720Controller()

app = Flask(__name__)
# Default values when controller is run
#app.config["com_port"] = "COM3"
app.config["current_temp"] = controller.get_current_temperature()  # Current temp from controller
app.config["set_temp"] = controller.get_current_temperature()  # What the user wants to temp to be
app.config["internal_gain"] = 1.00
app.config["proportional_bw"] = 5.00
app.config["derivative_gain"] = 0.00


# print(TC720Controller.get_current_temperature("TEST"))


# HOME PAGE
@app.route("/")
def index():
    return render_template("index.html")


# CONTACT US
@app.route("/contact")
def contact_html():
    return render_template("contact.html")


@app.route("/api/current_status", methods=["GET"])
def current_status():
    app.config["current_temp"] = controller.get_current_temperature()
    return jsonify(
        {
            #"com_port": app.config["com_port"],
            "current_temp": app.config["current_temp"],
            "set_temp": app.config["set_temp"],
            "internal_gain": app.config["internal_gain"],
            "proportional_bw": app.config["proportional_bw"],
            "derivative_gain": app.config["derivative_gain"],
        }
    )


@app.route("/api/submit_values", methods=["POST"])
def submit_values():
    data = request.get_json()
    print("Received:", data)

    #app.config["com_port"] = data.get("com_port")
    app.config["set_temp"] = data.get("set_temp")
    app.config["internal_gain"] = data.get("internal_gain")
    app.config["proportional_bw"] = data.get("proportional_bw")
    app.config["derivative_gain"] = data.get("derivative_gain")

    controller.set_pid_gains(p=app.config["proportional_bw"], i=app.config["internal_gain"], d=app.config["derivative_gain"])
    controller.set_temperature(app.config["set_temp"])

    print(app.config["internal_gain"])
    return jsonify({"status": "success"})


@app.route("/api/reset_values", methods=["POST"])
def reset_values():
    # TODO - Insert default hardcoded values
    #app.config["com_port"] = "COM3"
    app.config["set_temp"] = 38.2
    app.config["internal_gain"] = 1.00
    app.config["proportional_bw"] = 5.00
    app.config["derivative_gain"] = 0.00

    controller.set_pid_gains(p=5.0, i=1.0, d=0.0)
    controller.set_temperature(38.2)

    return jsonify({"status": "success"})


if __name__ == "__main__":
    app.run(debug=False)
