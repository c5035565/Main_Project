from flask import Flask
from datetime import datetime

# CRITICAL FIX: Explicitly reference the 'Project_File' folder as the package root
from blueprints.main.routes import main as main_blueprint 


def create_app():
    # --- APPLICATION SETUP ---
    app = Flask(__name__) 

   

    app.register_blueprint(main_blueprint, url_prefix='/')

    # --- GLOBAL CONTEXT ---
    @app.context_processor
    def inject_globals():
        # This makes 'current_year' available to ALL templates automatically
        return {'current_year': datetime.now().year}
    
    return app # Return the configured application instance

# --- EXECUTION ---
if __name__ == '__main__': 
    # When running locally, call the factory and run the app
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)