from myApp.config import DEBUG, WEB_SERVER
from myApp.views import app
from myApp.model.cellar import get_details_work_by_eurovoc_uri 
from myApp.model.bdd import get_eurvoc_uri_from_uid
if __name__ == '__main__':
    print(get_eurvoc_uri_from_uid(1))  # Example user_id
    app.run(
    host = WEB_SERVER['host'],
    port= WEB_SERVER['port'],
    debug=DEBUG
    )