from fastapi import FastAPI, Request, Form #request는 하나의 객체인 것. 그걸 사용자한테 넘겨줘야함
from fastapi.templating import Jinja2Templates #이걸 사용하려면 밑에 templates 변수 생성
from fastapi.responses import RedirectResponse

app = FastAPI()
# direcotry는 어떤 위치에 html 파일을 찾을 위치
templates = Jinja2Templates(directory='templates') # templates 폴더 만들기 

# 가상 데이터
posts = {
    1: {"id": 1, "title": "hi", "content": "반갑습니다."},
    2: {"id": 2, "title": "배고파요", "content": "뭐먹지"},
}

@app.get("/")
def home():
    return {"Hello": "World"}


#사용자에게 정보를 입력받는 페이지 
@app.get('/ping')
def ping(request: Request): #request에 Request 객체 형태가 들어와야한다고 타입으로 선언. 만약 request 안에 숫자 들어오면 타입안맞는다고 함
    return templates.TemplateResponse(
        request=request,
        name='ping.html'
    ) #TemplateResponse: 우리가 재료 주면 html 완성본 제공 (안에 몇 가지 필수 정보 넣어야함)
#ping은 request받아 ping.html 보여줄 수 있게 보여주기만 하면 됨 
#사용자에게 정보를 입력받는 페이지를 리턴 

#받은 정보를 사용하는 페이지
@app.get('/pong')
def pong(count: int):
    return {'result': count**3} #사용자한테 정보받아 3제곱해서 돌려주는

@app.post('/pong')
def pong_post(count: int = Form()): #url에 form 안넣으면 여기서 꺼내와주세요, 1번줄도 추가
    return {'result': count**2}

@app.get('/posts')
def post_list(request: Request):
    return templates.TemplateResponse(
        request=request, #이거 쓸 때 39번 괄호 안 같이 써야
        name = 'list.html',
        context = {'posts' : list(posts.values())}
    )


#사용자가 데이터 입력할 수 있는 페이지 제공
@app.get('/posts/new')
def post_new(request: Request):
    return templates.TemplateResponse(
        request=request,
        name='new.html'
    )

#사용자가 넘겨준 데이터를 저장 
@app.post('/posts/create')
def post_create(title: str = Form(), content: str = Form()):
    # return {'t':title, 'c': content}
    new_id = max(posts.keys())+1 #전체키목록추출, 여기서 max함수 써서 가장 큰 숫자나옴
    posts[new_id] = {'id': new_id, 'title':title, 'content':content}

    return RedirectionResponse(f'/posts/{new_id}', status_code=303) #어디로갈지정보넣어줘야

#하나의 게시글을 출력
@app.get('/posts/{post_id}')
def post_detail(request: Request, post_id: int): #url에 해당하는 post_id는 숫자가 들어올 예정
    
    post = posts[post_id] #전체 데이터 중에 내가 보고싶은 데이터 하나를 골라 그걸 post라는 단수변수에 저장
    
    return templates.TemplateResponse( #이렇게 가져온 post데이터를 templates에 보내는
        request=request,
        name='detail.html',
        context={'post': post}
    )