import datetime
import os
JWT_KEY=os.environ.get('JWT_KEY')

JWT_ACCESS_TOKEN_EXPIRES=datetime.timedelta(hours=1)
JWT_REFRESH_TOKEN_EXPIRES=datetime.timedelta(days=14)