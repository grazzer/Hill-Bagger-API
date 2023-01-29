from flask import Flask
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import mapper, sessionmaker
import pandas as pd


dbLoc = "sqlite:///DoBIH.db"

# SQLAlchemy Automap method of accsesing exisiting db
# Base = automap_base()
# engine = create_engine(dbLoc)
# Base.prepare(engine, reflect=True)
# Hills = Base.classes.hills
# session = Session(engine)

# SQLAlchemy reflection method of accsesing exisiting db
engine = create_engine(dbLoc)
metadata = MetaData(engine)
Hills = Table('hills', metadata, autoload=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()



app = Flask(__name__)

@app.route("/")
def hello_world():
    return "The Database of British and Irish Hills API"

@app.route('/hills')
def getHills():
    result = session.query(Hills)
    if result:
        df = pd.read_sql(result.statement, result.session.bind)
        jsonResult = df.to_json(orient = 'records')
        return jsonResult
    else:
        return {'msg':'Resource not found'}, 404

@app.route('/hills/<string:name>')
def getHillByName(name):
    result = session.query(Hills).filter(Hills.columns.Name == name)
    if result:
        df = pd.read_sql(result.statement, result.session.bind)
        jsonResult = df.to_json(orient = 'records')
        return jsonResult [1:-1]
    else:
        return {'msg':'Resource not found'}, 404

@app.route('/hills/<int:number>')
def getHillByNumber(number):
    result = session.query(Hills).filter(Hills.columns.Number == number)
    if result:
        df = pd.read_sql(result.statement, result.session.bind)
        jsonResult = df.to_json(orient = 'records')
        return jsonResult [1:-1]
    else:
        return {'msg':'Resource not found'}, 404

@app.route('/munros')
def getMunros():
    result = session.query(Hills).filter(Hills.columns.M == 1)
    if result:
        df = pd.read_sql(result.statement, result.session.bind)
        jsonResult = df.to_json(orient = 'records')
        return jsonResult
    else:
        return {'msg':'Resource not found'}, 404

app.run()
