
#header.payload.signature

#header-type,algorithm
#payload=username,expiry
from fastapi import FastAPI,HTTPException
from datetime import datetime,timedelta
from jose import JWTError,jwt


#configuration setup

ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
SECRET_KEY="mysecretkey_123"


app=FastAPI()
def create_token(username:str):
    expiry=datetime.utcnow()+timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    payload={"username":username,"exp":expiry}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    
def verify_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username=payload.get("username")
        return username
    except JWTError:
        raise HTTPException(status_code=401,detail="Invalid Token")
#login endpoint
@app.post("/login")
def login(username:str,password:str):
    if username=="admin" and password=="1234":
        #we need to create JWT token for login
        token=create_token(username)
        return {"access_token":token,} #to access the secret end point the user needs token
    return HTTPException(status_code=401,detail="Invalid Credentials")# if the username or pass is wrong

#secret data endpoint
@app.get("/secret-data")#user data
def secret_data(token:str):#it gets the token generated above
    
        username=verify_token(token) # it verifies the token
        return {"message":f"Hello {username},This is very secret data. Don't share it with anyone!"}
    

