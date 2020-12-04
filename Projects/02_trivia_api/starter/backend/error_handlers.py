from flask import jsonify

def setUpErrorHandlers(app):
    @app.errorhandler(500)
    def server_error(error):
        print("server error : ", error);
        return jsonify({
            "success":False,
            "status_code":500,
            "message":"server error please try again later"
        });

    @app.errorhandler(400)
    def bad_request(error):
        print("bad request : ", error);
        return jsonify({
            "success":False,
            "status_code":400,
            "message":"bad request: the request format is not supported please review the documentation"
        });

    @app.errorhandler(404)
    def bad_request(error):
        print("bad request : ", error);
        return jsonify({
            "success":False,
            "status_code":404,
            "message":"there is no resource for this URL"
        });

    @app.errorhandler(422)
    def bad_request(error):
        print("bad request : ", error);
        return jsonify({
            "success":False,
            "status_code":422,
            "message":"Unprocessable Entity: please call the Support"
        });