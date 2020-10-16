from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
	'''
	TODO Validate user & password
	'''
    correct_username = secrets.compare_digest(credentials.username, "linka")
    correct_password = secrets.compare_digest(credentials.password, "linka")
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username