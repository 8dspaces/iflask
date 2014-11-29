import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():

    SECRET_KEY = '\xf0\xe4},\x8f\x10\xe3.\x13?\x9eP\xcd!\xb1\x17\xa2%\xbbU'
    DEBUG = True 
    
    @staticmethod
    def init_app(app):
        pass 
        
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.dev.db')
    
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.uat.db')
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'data.db')
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
