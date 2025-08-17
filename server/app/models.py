from app import db

class Components(db.Model):
    __tablename__ = 'Components'
    uuid = db.Column(db.String, primary_key=True)
    part_name = db.Column(db.String, index=True, unique=True, nullable=False)
    category = db.Column(db.String, index=True, nullable=False)
    value = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    available = db.Column(db.String, default=True)
    atributes = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


    def __repr__(self):
        return f'<User {self.part_name}>'