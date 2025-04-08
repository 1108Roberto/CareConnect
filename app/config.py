class Config:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:rootpassword@localhost:3306/clinic_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
