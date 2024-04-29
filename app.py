from inventory_system import app,db,routes




if __name__ == '__main__': # this is used to run the app
    db.create_all()
    app.run(debug=True)


# this is used to show the error page when the user enter a wrong url
# @app.errorhandler(404)
# def error_404(error):
#     return render_template('/errors/404.html'), 404

# @app.errorhandler(403)
# def error_403(error):
#     return render_template('/errors/403.html'), 403

# @app.errorhandler(500)
# def error_500(error):
#     return render_template('/errors/500.html'), 500




























# from flask import Flask
# app=Flask(__name__)


# # loccalhost:5000/
# @app.route("/")
# def hello():
#     return "Hello World!"


# if __name__=="__main__":
#     app.run()
    
#     # app/run(port=3000) #specify port number
    
#     # app.run(debug=True) # activate debug mode 
#     # (development environment)