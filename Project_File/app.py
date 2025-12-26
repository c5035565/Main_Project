from flask import Flask
from datetime import datetime


from blueprints.main.routes import main as main_blueprint 


def create_app():
   
    app = Flask(__name__) 

    
    app.secret_key = 'cantor_college_is_the_best' 

    app.register_blueprint(main_blueprint, url_prefix='/')

    
    @app.context_processor
    def inject_globals():
       
        return {'current_year': datetime.now().year}
    
    return app 


if __name__ == '__main__': 
   
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)