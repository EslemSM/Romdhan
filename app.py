from flask import Flask
from models.db import db
from flask_jwt_extended import JWTManager

def create_app():
    print("CREATE_APP CALLED") 
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Islem2003*@localhost/ramadhan'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
        'connect_args': {'connect_timeout': 5}
    }

    app.config["JWT_SECRET_KEY"] = "ramadhan-secret-key"  # change later
    jwt = JWTManager(app)
    # Initialize database (with error handling - don't fail app startup if DB unavailable)
    try:
        db.init_app(app)
        print("✓ Database initialized")
    except Exception as e:
        print(f"⚠ Database initialization warning (app will continue): {type(e).__name__}: {e}")
        # Don't fail the app if database isn't available - some endpoints don't need it

    # Import and register blueprints (with error handling)
    try:
        from resources.prayer import prayer_bp
        app.register_blueprint(prayer_bp, url_prefix="/prayer")
        print("✓ Prayer blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register prayer blueprint: {e}")
        import traceback
        traceback.print_exc()

    try:
        from resources.sunnah_prayer import sunnah_bp
        app.register_blueprint(sunnah_bp, url_prefix="/sunnah_prayer")
        print("✓ Sunnah prayer blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register sunnah_prayer blueprint: {e}")

    try:
        from resources.quran_tafsir import tafseer_bp
        app.register_blueprint(tafseer_bp, url_prefix="/quran_tafsir")
        print("✓ Quran tafsir blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register quran_tafsir blueprint: {e}")

    try:
        from resources.adhkar_resource import adhkar_bp
        app.register_blueprint(adhkar_bp, url_prefix='/adhkar')
        print("✓ Adhkar blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register adhkar blueprint: {e}")

    try:
        from resources.ahadith_ramadhania import ahadith_bp
        app.register_blueprint(ahadith_bp, url_prefix='/ahadith')
        print("✓ Ahadith blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register ahadith blueprint: {e}")

    try:
        from resources.doua_resource import doua_bp
        app.register_blueprint(doua_bp, url_prefix='/doua')
        print("✓ Doua blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register doua blueprint: {e}")

    try:
        from resources.user_resources import user_bp
        app.register_blueprint(user_bp, url_prefix="/users")
        print("✓ user blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register doua blueprint: {e}")
    
    try: 
        from resources.khatma_resources import khatma_bp
        app.register_blueprint(khatma_bp, url_prefix="/khatma")
        print("✓ khatma blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register khatma blueprint: {e}")

    try:
        from resources.recipe_resource import recipe_bp
        app.register_blueprint(recipe_bp, url_prefix="/recipes")
        print("✓ recipes blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register recipes blueprint: {e}")


    try:
        from resources.user_adhkar import user_adhkar_bp
        app.register_blueprint(user_adhkar_bp, url_prefix="/user_adhkar")
        print("✓ user_adhkar blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register user_adhkar blueprint: {e}")


    try:
        from resources.user_doua import user_doua_bp
        app.register_blueprint(user_doua_bp, url_prefix="/user_doua")
        print("✓ user_doua blueprint registered")
    except Exception as e:
        print(f"✗ Failed to register user_doua blueprint: {e}")


   




    print(app.url_map)


    @app.route('/')
    def health():
        return {"status": "API OK"}


    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)