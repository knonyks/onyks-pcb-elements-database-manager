from app import db

class Components(db.Model):
    __tablename__ = 'Components'
    uuid = db.Column(db.String, primary_key=True)
    part_name = db.Column(db.String, index=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


    def __repr__(self):
        return f'<User {self.part_name}>'