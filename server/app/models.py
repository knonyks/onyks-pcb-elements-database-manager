from app import db
import uuid

class Components(db.Model):
    __tablename__ = 'Components'
    uuid = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    part_name = db.Column(db.String, index=True, unique=False, nullable=False)
    manufacturer = db.Column(db.String, index=True, unique=False, nullable=False)
    description = db.Column(db.String, nullable=True)
    library_ref = db.Column(db.String, index=True, unique=False, nullable=False)
    library_path = db.Column(db.String, index=True, unique=False, nullable=False)
    footprint_ref_1 = db.Column(db.String, index=True, unique=False, nullable=False)
    footprint_path_1 = db.Column(db.String, index=True, unique=False, nullable=False)
    footprint_ref_2 = db.Column(db.String, index=True, unique=False, nullable=False)
    footprint_path_2 = db.Column(db.String, index=True, unique=False, nullable=False)
    footprint_ref_3 = db.Column(db.String, index=True, unique=False, nullable=False)
    footprint_path_3 = db.Column(db.String, index=True, unique=False, nullable=False)

    
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    last_edited_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    # category = db.Column(db.String, index=True, nullable=False)
    # value = db.Column(db.String, nullable=False)

    # available = db.Column(db.String, default=True)
    # atributes = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f'<{self.part_name}>'