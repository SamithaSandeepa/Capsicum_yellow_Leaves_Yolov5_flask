from flask import Flask, request, jsonify, render_template, send_from_directory
from detect_app import detect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


# Serve output_images directory
@app.route('/output_images/<path:filename>')
def serve_output_image(filename):
    return send_from_directory('output_images', filename)

# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/detect", methods=['POST'])
def detect_image():
    try:
        # Get the image from the request
        image = request.files.getlist("image")[0]
        print(len(request.files.getlist("image")))
        all_results = []
        for i in range(len(request.files.getlist("image"))):
            image = request.files.getlist("image")[i]

            image_name = image.filename

            print(image_name)

            results = detect(image, image_name)
            all_results.append(results)

            # Return the detection results as JSON
        return jsonify(all_results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)



# Save the image to a folder
        # image_path = 'images_to_detect/' + image_name
        # image.save(image_path)
        # print(f"Image saved to {image_path}")
        # Perform object detection