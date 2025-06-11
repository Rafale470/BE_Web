from myApp.config import DEBUG, WEB_SERVER
from myApp.views import app
from myApp.model.cellar import get_details_work_by_eurovoc_uri 
if __name__ == '__main__':
    print(get_details_work_by_eurovoc_uri(["http://eurovoc.europa.eu/4505", "http://eurovoc.europa.eu/4506"]))
    app.run(
    host = WEB_SERVER['host'],
    port= WEB_SERVER['port'],
    debug=DEBUG
    )