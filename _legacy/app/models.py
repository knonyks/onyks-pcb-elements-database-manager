import uuid
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

def get_element_model(db, tablename):

    class Element(db.Model):
        __tablename__ = tablename

        uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
        
        part_name = db.Column(db.String, index=True, unique=False, nullable=False)
        manufacturer = db.Column(db.String, index=True, unique=False, nullable=True)
        manufacturer_part_name = db.Column(db.String, index=True, unique=False, nullable=True)

        datasheet = db.Column(db.Boolean, index=True, unique=False, nullable=True)
        description = db.Column(db.String, nullable=True)

        value = db.Column(db.String, index=True, unique=False, nullable=True)
        availability = db.Column(db.String, index=True, unique=False, nullable=True)

        library_ref = db.Column(db.String, index=True, unique=False, nullable=True)
        library_path = db.Column(db.String, index=True, unique=False, nullable=True)
        
        footprint_ref_1 = db.Column(db.String, index=True, unique=False, nullable=True)
        footprint_path_1 = db.Column(db.String, index=True, unique=False, nullable=True)
        
        footprint_ref_2 = db.Column(db.String, index=True, unique=False, nullable=True)
        footprint_path_2 = db.Column(db.String, index=True, unique=False, nullable=True)
        
        footprint_ref_3 = db.Column(db.String, index=True, unique=False, nullable=True)
        footprint_path_3 = db.Column(db.String, index=True, unique=False, nullable=True)

        created_at = db.Column(db.DateTime, server_default=db.func.now())

        def __repr__(self):
            return f'<{self.part_name}>'

        def get_parameters_dict(self):
            return {
                "uuid": self.uuid,
                "part_name": self.part_name,
                "manufacturer": self.manufacturer,
                "manufacturer_part_name": self.manufacturer_part_name,
                "datasheet": self.datasheet,
                "description": self.description,
                "value": self.value,
                "availability": self.availability,
                "library_ref": self.library_ref,
                "library_path": self.library_path,
                "footprint_ref_1": self.footprint_ref_1,
                "footprint_path_1": self.footprint_path_1,
                "footprint_ref_2": self.footprint_ref_2,
                "footprint_path_2": self.footprint_path_2,
                "footprint_ref_3": self.footprint_ref_3,
                "footprint_path_3": self.footprint_path_3,
                "created_at": self.created_at
            }

        def get_parameters_list(self):
            def get_parameters_list(self):
                return [
                    self.uuid,
                    self.part_name,
                    self.manufacturer,
                    self.manufacturer_part_name,
                    self.datasheet,
                    self.description,
                    self.value,
                    self.availability,
                    self.library_ref,
                    self.library_path,
                    self.footprint_ref_1,
                    self.footprint_path_1,
                    self.footprint_ref_2,
                    self.footprint_path_2,
                    self.footprint_ref_3,
                    self.footprint_path_3,
                    self.created_at
                ]

        def get_parameter_names():
            return [
                ["uuid", "UUID"],
                ["part_name", "Part Name"],
                ["manufacturer", "Manufacturer"],
                ["manufacturer_part_name", "Manufacturer Part Name"],
                ["datasheet", "Datasheet"],
                ["description", "Description"],
                ["value", "Value"],
                ["availability", "Availability"],
                ["library_ref", "Library Reference"],
                ["library_path", "Library Path"],
                ["footprint_ref_1", "Footprint Reference 1"],
                ["footprint_path_1", "Footprint Path 1"],
                ["footprint_ref_2", "Footprint Reference 2"],
                ["footprint_path_2", "Footprint Path 2"],
                ["footprint_ref_3", "Footprint Reference 3"],
                ["footprint_path_3", "Footprint Path 3"],
                ["created_at", "Created At"]
            ]
        
    return Element

def get_user_model(db, bind, tablename):
   
    class User(UserMixin, db.Model):
        __bind_key__ = bind
        __tablename__ = tablename

        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(80), nullable=True)
        family_name = db.Column(db.String(80), nullable=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password = db.Column(db.String(200), nullable=False)
        is_admin = db.Column(db.Boolean, default=False, nullable=False)

        def full_name(self):
            parts = [p for p in (self.first_name, self.last_name) if p]
            return " ".join(parts) if parts else self.username
        
    return User