from app import db


class People(db.Model):
    wdentity = db.Column(db.String, primary_key=True)
    bdate = db.Column(db.String, primary_key=True)
    name = db.Column(db.Integer)
    descrs = db.Column(db.String)
    links = db.Column(db.String)
    photo = db.Column(db.String)
    qrank = db.Column(db.Integer)


class Occupations(db.Model):
    occu_entity = db.Column(db.String, primary_key=True)
    occu_group = db.Column(db.String)
    emoji = db.Column(db.String)
    descr_cache = db.Column(db.String)


class Tags(db.Model):
    people_entity = db.Column(db.String, primary_key=True)
    occupation_entity = db.Column(db.String, primary_key=True)


class Countries(db.Model):
    people_entity = db.Column(db.String, primary_key=True)
    country_entity = db.Column(db.String, primary_key=True)


class Flags(db.Model):
    country_entity = db.Column(db.String, primary_key=True)
    country_name = db.Column(db.String)
    emoji_flag = db.Column(db.String)
    svg_flag = db.Column(db.String)


class Presorted(db.Model):
    flyid = db.Column(db.Integer, primary_key=True)
    bday = db.Column(db.String)
    enwde = db.Column(db.String)
    ruwde = db.Column(db.String)
    bewde = db.Column(db.String)
    ukwde = db.Column(db.String)
    kkwde = db.Column(db.String)
    dewde = db.Column(db.String)
    frwde = db.Column(db.String)
    eswde = db.Column(db.String)
    itwde = db.Column(db.String)
    zhwde = db.Column(db.String)
    kowde = db.Column(db.String)
    jawde = db.Column(db.String)
    enrank = db.Column(db.String)
    rurank = db.Column(db.String)
    berank = db.Column(db.String)
    ukrank = db.Column(db.String)
    kkrank = db.Column(db.String)
    derank = db.Column(db.String)
    frrank = db.Column(db.String)
    esrank = db.Column(db.String)
    itrank = db.Column(db.String)
    zhrank = db.Column(db.String)
    korank = db.Column(db.String)
    jarank = db.Column(db.String)
