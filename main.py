from fastapi import FastAPI, UploadFile, Form, Response, Depends #Form 데이터는 "python-multipart"가 필요하기 때문에 설치해줘야 함
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException #유효하지 않은 계정 정보에 대한 에러처리를 할 수있도록 하는 문법
from typing import Annotated
import sqlite3

con=sqlite3.connect('market.db',check_same_thread=False)
cur=con.cursor()

# 배포를 하게 되면 배포된 백엔드 서버에서 테이블을 생성해줘야 함 -> 테이블 없으면 데이터 넣을 곳이 없기 때문
# 백엔드 코드에서 자동으로 데이터베이스 테이블을 생성할 수 있도록 sql문 작성
# 배포됐는데 서버가 잠깐 내려갔다가 올라올 수 있는데 그 때마다 테이블을 생성하게 되면 오류 발생
# 그래서 오류 방지하기 위해 테이블이 없을 때만 생성할 수 있도록 해야 함
# IF NOT EXISTS를 추가해줘서 테이블이 없을 때만 생성되는 SQL문
cur.execute(f"""
             CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                image BLOB,
                price INTEGER NOT NULL,
                description TEXT,
                place TEXT NOT NULL,
                insertAt INTEGER NOT NULL
                ); 
                """
            )

app=FastAPI()

#SECRET 정보는 우리가 액세스 토큰을 어떻게 인코딩할 지 정하는 것
# 이게 노출되면 디코딩이 될 수 있음
SECRET="super-coding"
#토큰이 login페이지에서만 발급되도록
#우리가 만든 secret과 login path에서 적당한 access 토큰을 만들어주는 라이브러리
manager=LoginManager(SECRET, '/login')

#LoginManger가 키를 같이 조회하기 위해 user_loader() 호출
@manager.user_loader()
def query_user(data): #data 형식으로 들어감
    WHERE_STATEMENTS=f'id="{data}"'
    #객체 형태로 넘어오게 되면 
    if type(data)==dict:
        WHERE_STATEMENTS=f'''id="{data['id']}"''' #안에 있는 id 빼서 써야하기 때문에 where_statements값이 id="{data['id']}이렇게 될 것
        
    #컬럼명도 같이 가져옴, 특정 컬럼만 조회하기위해 
    con.row_factory=sqlite3.Row
    cur=con.cursor() #커서를 현재위치로 업데이트
    #해당 유저가 db에 존재하는지 확인
    user=cur.execute(f"""
                    SELECT * FROM users WHERE {WHERE_STATEMENTS}                     
                     """).fetchone()
    return user

@app.post('/login')
def login(id:Annotated[str, Form()], password:Annotated[str, Form()]):
    user=query_user(id) #query_user를 통해서 id 받아옴
    
    #user가 존재하는지 판단
    if not user:
        #user 없으면 raise를 통해 에러메시지 보냄
        raise InvalidCredentialsException #-> 401 자동으로 생성해서 내려줌
    elif password != user['password']: #입력한 password랑 user 정보를 조회해서 얻은 패스워드가 불일치 했을 경우
       raise InvalidCredentialsException
    
    access_token=manager.create_access_token(data={
        'sub':{ 
         'id':user['id'],
        'name': user['name'],
        'email':user['email']   
        }
    })
    return {'access_token':access_token}
    
#회원가입 요청이기 때문에 post
@app.post('/signup')
def signup(id:Annotated[str, Form()], password:Annotated[str, Form()], name:Annotated[str, Form()], email:Annotated[str, Form()]):
    #받은 정보를 db에 저장
    cur.execute(f"""
                INSERT INTO users(id, name, email, password)
                VALUES ('{id}','{name}','{email}','{password}')
                """)
    con.commit()
    return '200'
# 이미 가입되어 있는 유저임에도 회원가입이 될 수 있다는 문제점 존재 => 판단하는 로직 한 번 작성해보기!


@app.post('/items')
# image는 UploadFile 형식, title은 form 데이터 형식으로 문자열로 받을 거라는 의미
async def create_item(image:UploadFile, 
                title:Annotated[str, Form()], 
                price:Annotated[int, Form()], 
                description:Annotated[str, Form()], 
                place:Annotated[str, Form()],
                insertAt:Annotated[int, Form()],
                user=Depends(manager)):
    image_bytes = await image.read() #이미지를 읽는 시간
    cur.execute(f"""
                INSERT INTO 
                items (title, image, price, description, place, insertAt) 
                VALUES ('{title}', '{image_bytes.hex()}', {price}, '{description}', '{place}', {insertAt})
                """) #읽힌 정보를 데베에 insert
    con.commit()
    
    return '200' #위의 코드들이 완료가 되면 200이라는 상태코드를 리턴

# items라는 get요청이 들어왔을 때
#ARRAY 형식[1, '식칼팝니다', '잘 설려요']으로 오는 데이터를 {id:1, title:'식칼팝니다', description:'잘 설려요'} 객체(object)로 만들어서 fe에 넘겨주기 위한 코드
@app.get('/items')
#items를 가져올 때, user=Depends(manager)를 넣어서 user가 인증된 상태에서만 응답을 보낼 수 있도록 함
async def get_items(user=Depends(manager)):
    #컬럼명도 같이 가져옴
    con.row_factory=sqlite3.Row 
    
    #db를 가져오면서 connection의 현재위치를 업데이트
    cur=con.cursor() 
    rows = cur.execute(f"""
                       SELECT * FROM items;
                       """).fetchall() #가져오는 문법이기 때문에 fetchall 작성
    #rows =[['id',1], ['title':'식칼팝니다'], ['description':'잘 설려요']]
    #rows들 중에 각각의 array를 돌면서 그 array를 dictonary 형태, 즉 객체 형태로 만들어주는 문법
    #dict(row) for row in rows
        
    
    return JSONResponse(jsonable_encoder(
        dict(row) for row in rows
        )) # dictonary 형태로 자바스크립트 쪽으로 보냄, dict(row) for row in rows를 json형식으로 바꿔주기 위해 jsonable_encoder로 감싸줌

#image 응답하는 get 함수, item_id에 맞는 이미지를 보내줌
@app.get('/images/{item_id}')
async def get_image(item_id):    
    cur=con.cursor()
    #item_id와 똑같은 이미지를 가져오는 sql문, image_bytes는 16진법
    image_bytes=cur.execute(f"""
                            SELECT image from items WHERE id={item_id}
                            """).fetchone()[0] #하나의 column만 가져올거라 fetchone 사용, 튜플이라는 데이터타입으로 내려오기 때문에 껍데기 하나 벗기기 위해 [0]사용
    return Response(content=bytes.fromhex(image_bytes)) # 16진법으로 된 거를 이진법으로 바꿔서 응답

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")