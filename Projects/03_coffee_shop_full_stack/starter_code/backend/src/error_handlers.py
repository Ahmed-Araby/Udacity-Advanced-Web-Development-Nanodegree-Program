"""
we are able to handle exceptions using app.errorhandler()
- raise Exception could be handled by this decorator
- abort(httpCode) also could be handled
- we can decorate with http code or exception class/sub class.
"""

from flask import jsonify, Flask, abort
from .auth.auth import AuthError


def setup_errorHandlers(app):

    @app.errorhandler(422)
    def unprocessable(error):
        print("unprocessable error ", error)

        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422  # status code of the response, this will override the one in the header.

    @app.errorhandler(404)
    def notFound(error):
        print("not found error ", error)

        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(500)
    def serverError(error):
        print("server error", error)

        return jsonify({
            "success": False,
            "error": 500,
            "message": str(error)
        }), 500

    @app.errorhandler(409)
    def serverError(error):
        print("server error", error)

        return jsonify({
            "success": False,
            "error": 409,
            "message": str(error)
        }), 409

    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''

    @app.errorhandler(AuthError)
    def authError_expiredToekn(error):
        """
            error is the authError object
        """
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code
