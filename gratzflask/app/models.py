from app import db


class People(db.Model):
    bdate = db.Column(db.String, primary_key=True)
    bklinks = db.Column(db.Integer)
    wdentity = db.Column(db.String, primary_key=True)
    photo = db.Column(db.String)
    links = db.Column(db.String)


class Occupations(db.Model):
    occu_entity = db.Column(db.String, primary_key=True)
    occu_group = db.Column(db.String)
    emoji = db.Column(db.String)
    descr_cache = db.Column(db.String)

    def __repr__(self):
        return '<OCCU {}>'.format(self.descr_cache)


class Tags(db.Model):
    people_entity = db.Column(db.String, primary_key=True)
    occupation_entity = db.Column(db.String, primary_key=True)


class Wdentities(db.Model):
    wdentity = db.Column(db.String, primary_key=True)
    descr_cache = db.Column(db.String)
