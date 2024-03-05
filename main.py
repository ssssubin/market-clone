from fastapi import FastAPI, UploadFile, Form, Response #Form 데이터는 "python-multipart"가 필요하기 때문에 설치해줘야 함
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
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

@app.post('/items')
# image는 UploadFile 형식, title은 form 데이터 형식으로 문자열로 받을 거라는 의미
async def create_item(image:UploadFile, 
                title:Annotated[str, Form()], 
                price:Annotated[int, Form()], 
                description:Annotated[str, Form()], 
                place:Annotated[str, Form()],
                insertAt:Annotated[int, Form()]):
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
async def get_items():
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

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")