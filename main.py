from routes import app
import uvicorn
from log import logging
from settings import settings

if __name__ == "__main__":
    uvicornlog=logging.getLogger('uvicorn')
    uvicornlog.setLevel(logging.INFO)
    logging.config.fileConfig("logging.conf")
    uvicorn.run(app,
                host=settings.BASE_URL, 
                port=settings.PORT, 
                logger = uvicornlog)