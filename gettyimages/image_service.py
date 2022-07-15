from flask import Flask, request, jsonify, Blueprint

from . import image_extract as images
import traceback

# import meme_service
# app = meme_service.app
# app = Flask(__name__)

image_api = Blueprint('image', __name__)

NEWS_PREFIX = './image_meme'

@image_api.route(NEWS_PREFIX + '/')
def image_hello():
    return "Hello World!"

@image_api.route(NEWS_PREFIX + '/image-list', methods = ['GET'])
def images_get_image_list():
    try:
        page = request.args.get('page', 1)
        response = images.get_image_list(page)
        message = {'code':'ok', 'data':response}

        return jsonify(message)
    except Exception:
        traceback.print_exc()
        message = {'code' : 'error', 'message' : 'error occured'}

        return jsonify(message)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=6004, debug=True)