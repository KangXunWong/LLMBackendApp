from routes import app
import uvicorn
from settings import settings
import os




if __name__ == "__main__":
    # uvicornlog=logging.getLogger('uvicorn')
    # uvicornlog.setLevel(log.info)
    uvicorn.run(app,
                host=settings.BASE_URL,
                port=settings.PORT,
                log_config=f"{os.getcwd()}/logging.ini",
                # reload=True
                )