from myApp.config import DEBUG, WEB_SERVER
from myApp.views import app
from myApp.model.cellar import get_work_by_uri 
if __name__ == '__main__':
    print(get_work_by_uri("http://publications.europa.eu/resource/cellar/0fda6403-6e09-4dc7-8b26-241c59773d5f"))
    app.run(
    host = WEB_SERVER['host'],
    port= WEB_SERVER['port'],
    debug=DEBUG
    )