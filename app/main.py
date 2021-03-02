import datetime,uuid,os
import model as mdUser
from pg_db import database,users
from fastapi import FastAPI,File,UploadFile
from fastapi.staticfiles import StaticFiles
from typing import List
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

app = FastAPI(
    docs_url="/api/v2/docs",
    redoc_url="/api/v2/redocs",
    title="小程序核心接口",
    description="小程序用户接口、支付接口等",
    openapi_url="/api/v2/openapi.json",
)

app.mount("/Upload", StaticFiles(directory="Upload"), name="Upload")

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/",tags=["默认页"])
async def index():
    return 'Hello World!'

@app.get("/users",response_model=List[mdUser.UserList],tags=["用户接口"])
async def find_all_users():
    query = users.select()
    return await database.fetch_all(query)

@app.post("/users",response_model=mdUser.UserList,tags=["用户接口"])
async def register_user(user:mdUser.UserEntry):
    gID = str(uuid.uuid1())
    gDate = str(datetime.datetime.now())
    query = users.insert().values(
        id = gID,
        username = user.username,
        password = pwd_context.hash(user.password),
        first_name = user.first_name,
        last_name = user.last_name,
        gender = user.gender,
        create_at = gDate,
        status = "1"
    )

    await database.execute(query)
    return {
        "id":gID,
        **user.dict(),
        "create_at":gDate,
        "status":"1"
    }
@app.get("/users/{userId}",response_model=mdUser.UserList,tags=["用户接口"])
async def find_user_by_id(userId:str):
    query = users.select().where(users.c.id==userId)
    return await database.fetch_one(query)

@app.put("/users",response_model=mdUser.UserList,tags=["用户接口"])
async def update_user(user:mdUser.UserUpdate):
    gDate = str(datetime.datetime.now())
    query = users.update().\
        where(users.c.id == user.id).\
        values(
            first_name = user.first_name,
            last_name = user.last_name,
            gender = user.gender,
            status = user.status,
            create_at=gDate,
        )
    await database.execute(query)
    return await find_user_by_id(user.id)

@app.delete("/users/{userId}",tags=["用户接口"])
async def delete_user(user:mdUser.UserDelete):
    query  = users.delete().where(users.c.id==user.id)
    await database.execute(query)

    return{
        "status":True,
        "message":"This user has been deleted successfully."
    }


@app.get("/pays",tags=["支付接口"])
def find_all_pays():
    return "list all pays.  "


@app.post("/uploadfile/",tags=["文件上传"])
async def create_upload_file(file: UploadFile = File(...)):
    toDay = datetime.datetime.now().strftime("%Y%m%d")
    save_dir = "Upload"
    UploadFile_dir = os.path.join(save_dir,toDay)
    if not os.path.exists(UploadFile_dir):
        os.makedirs(UploadFile_dir,0o777)
    try:
        res = await file.read()
        testlist = file.filename.split('.')
        extension = testlist[1]
        filename = datetime.datetime.now().strftime("%H-%M-%S-")+str(uuid.uuid1())+'.'+extension
        with open(UploadFile_dir+'/'+filename, "wb") as f:
            f.write(res)
        f.close()    
        return {"message": "success", 'filename': UploadFile_dir+'/'+filename}
    except Exception as e:
        return {"message": str(e), 'filename': file.filename}