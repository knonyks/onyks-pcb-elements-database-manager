import uuid
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

def getElementModel(db, tablename):

    class Element(db.Model):
        __tablename__ = tablename

        uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        
        part_name = db.Column(db.String, index=True, unique=False, nullable=False)
        manufacturer = db.Column(db.String, index=True, unique=False, nullable=True)
        description = db.Column(db.String, nullable=True)
       
        library_ref = db.Column(db.String, index=True, unique=False, nullable=True)
        library_path = db.Column(db.String, index=True, unique=False, nullable=True)
        
        footprint_ref_1 = db.Column(db.String, index=True, unique=False, nullable=True)
        footprint_path_1 = db.Column(db.String, index=True, unique=False, nullable=True)
        
        footprint_ref_2 = db.Column(db.String, index=True, unique=False, nullable=True)
        footprint_path_2 = db.Column(db.String, index=True, unique=False, nullable=True)
        
        footprint_ref_3 = db.Column(db.String, index=True, unique=False, nullable=True)
        footprint_path_3 = db.Column(db.String, index=True, unique=False, nullable=True)

        created_at = db.Column(db.DateTime, server_default=db.func.now())
        last_edited_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

        # value = db.Column(db.String, nullable=False)

        # available = db.Column(db.String, default=True)
        # atributes = db.Column(db.String, nullable=True)

        def __repr__(self):
            return f'<{self.part_name}>'
        
    return Element

def getUserModel(db, tablename):
   
    class User(UserMixin, db.Model):
        __tablename__ = tablename
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=True)
        family_name = db.Column(db.String(80), nullable=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)
        expired_access_time = db.Column(db.DateTime, nullable=True)
        is_admin = db.Column(db.Boolean, default=False, nullable=False)

        def full_name(self):
            parts = [p for p in (self.first_name, self.last_name) if p]
            return " ".join(parts) if parts else self.username
        
    return User