import bottle
from bottle import route, request, post
from bottle.ext.sqlalchemy import SQLAlchemyPlugin
from accesslogschema import engine, Base, Dailypageviews, DailypageviewsPerCountry
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.sql.expression import and_, func
from datetime import datetime
        
@post('/pageviewspercountry')
def test(db):
    
    startdatestring = request.json['startdate']
    enddatestring = request.json['enddate']
    dateformat = '%d-%m-%Y'
    
    startdate = datetime.strptime(startdatestring, dateformat)
    enddate = datetime.strptime(enddatestring, dateformat)
    
    selectedDailypageviewsPerCountry = db.query(DailypageviewsPerCountry, func.count(DailypageviewsPerCountry.pageviews)).filter(
        and_(DailypageviewsPerCountry.startdate >= startdate,
        DailypageviewsPerCountry.enddate <= enddate)).group_by(DailypageviewsPerCountry.countrycode)
    
    returnDict = {'postdata' : request.json, 'returndata' : []}

    for dailyPageviewsPerCountry in selectedDailypageviewsPerCountry:
        
        tempDict = {'pageviews' : dailyPageviewsPerCountry[1],
                'countrycode' : dailyPageviewsPerCountry[0].countrycode}

        returnDict['returndata'].append(tempDict)

    return returnDict

if __name__ == '__main__':
    bottle.install(SQLAlchemyPlugin(engine, Base.metadata, create=True))
    bottle.run(host='localhost', port=8080, debug=True, reloader=True)