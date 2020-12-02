from flask import jsonify

def setUpErrorHandlers(app):
    @app.errorhandler(400)
    def notFound(error):
        print(error);
        return jsonify({
            "success":False,
            "error_code": 400,
            "message": "this json format is not valid"
        });

    @app.errorhandler(404)
    def notFound(error):
        print(error);
        return jsonify({
            "success":False,
            "error_code": 404,
            "message": "there is no resources for this url"
        });

    @app.errorhandler(405)
    def notFound(error):
        """
            this error is thrown by the flask it self.
        """
        print(error);
        return jsonify({
            "success":False,
            "error_code": 405,
            "message": "this method is not allowed on this route"
        });

    @app.errorhandler(500)
    def notFound(error):
        print(error);
        return jsonify({
            "success":False,
            "error_code": 500,
            "message": "sever failure: your request has failed due to server failure, please try again"
        });

