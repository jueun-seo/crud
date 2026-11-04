from fastapi import FastAPI, Request, Form #request는 하나의 객체인 것. 그걸 사용자한테 넘겨줘야함
from fastapi.templating import Jinja2Templates #이걸 사용하려면 밑에 templates 변수 생성

app = FastAPI()
# direcotry는 어떤 위치에 html 파일을 찾을 위치
templates = Jinja2Templates(directory='templates') # templates 폴더 만들기 


@app.get("/")
def home():
    return {"Hello": "World"}


#사용자에게 정보를 입력받는 페이지 
@app.get("/ping")
def ping(request: Request): #request에 Request 객체 형태가 들어와야한다고 타입으로 선언. 만약 request 안에 숫자 들어오면 타입안맞는다고 함
    return templates.TemplateResponse(
        request=request,
        name='ping.html'
    ) #TemplateResponse: 우리가 재료 주면 html 완성본 제공 (안에 몇 가지 필수 정보 넣어야함)
#ping은 request받아 ping.html 보여줄 수 있게 보여주기만 하면 됨 
#사용자에게 정보를 입력받는 페이지를 리턴 

#받은 정보를 사용하는 페이지
@app.get("/pong")
def pong(count: int):
    return {'result': count**3} #사용자한테 정보받아 3제곱해서 돌려주는

@app.post('/pong')
def pong_post(count: int = Form()): #url에 form 안넣으면 여기서 꺼내와주세요, 1번줄도 추가
    return {'result': count**2}