



# 主要暴露 创建邮箱(支持账号密码自定义)  获取邮件  发送邮件 获取一个不被占用的邮箱(动态创建)



# 基于 fastapi 暴露服务
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse

from p2_暴露服务_工具函数 import *

token = "email_2025_06_11_wzq_1213wzwz"
router = APIRouter(prefix=f"/{token}")

domain = 'ifengxiang365.com'
mxdomain = 'email.ifengxiang365.com'
mxdomain_ip = '47.83.16.21'



app = FastAPI(
    title="邮箱服务 API",
    description="提供创建邮箱、发送邮件、获取邮件等功能",
    version="1.0.0"
)


from pydantic import BaseModel
from typing import Optional, Any

class EmailRequestModel(BaseModel):
    email_account: Optional[str] = None
    email_password: Optional[str] = None
    to_email: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None

    def get(self, key: str, default: Any = None) -> Any:
        """支持 .get('key') 的方式访问属性"""
        return getattr(self, key, default)


@app.get("/", summary="首页 - 跳转至 Swagger UI", response_class=HTMLResponse)
async def root():
    html_content = f"""
    <html>
        <head><title>邮箱服务 API</title></head>
        <body style="font-family: Arial; text-align:center; margin-top: 100px;">
            <h1>欢迎使用 邮箱服务 API</h1>
            <p>请前往 <a href="/docs" target="_blank">Swagger UI</a> 查看和调试接口。</p>
            <p>请前往 <a href="https://{mxdomain_ip}" target="_blank">登录邮箱</a> 可视化查看邮件  默认密码为 1213wzwz。</p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


class CreateMailRequestModel(BaseModel):
    email_account: str
    email_password: str
    def get(self, key: str, default: Any = None) -> Any:
        """支持 .get('key') 的方式访问属性"""
        return getattr(self, key, default)

@router.post("/create_mail", summary="创建一个邮箱账户 自定义账号 自定义密码")
async def create_mail(data: CreateMailRequestModel):
    email_account = data.get('email_account')
    email_password = data.get('email_password')

    flag, info = create_email_accout_password( domain, mxdomain, mxdomain_ip, email_account, email_password)
    
    if flag:
        return {"code": 200, "msg": "创建成功", "data": info}
    else:
        return {"code": 500, "msg": "创建失败", "data": info}



@router.post("/get_mail", summary="获取指定邮箱的邮件")
async def router_get_mail(data: CreateMailRequestModel):
    # 实现获取邮件逻辑
    email_account = data.get('email_account')
    email_password = data.get('email_password')
    flag = get_email( mxdomain, mxdomain_ip, email_account, email_password)
    return {"code": 200, "msg": "获取成功", "data": flag}



@router.get("/get_one_unuse_mail", summary="创建一个未被占用的邮箱,默认密码为 1213wzwz ,如果需要修改密码,请使用修改密码接口进行修改")
async def get_unuse_mail():
    # 实现动态创建邮箱逻辑
    res = create_email(domain, mxdomain, mxdomain_ip)
    if res:
        return {"code": 200, "msg": "获取成功", "data": res}
    else:
        return {"code": 500, "msg": "获取失败", "data": res}
    

@router.get("/change_password/", summary="修改指定邮箱的密码")
async def change_password(data: CreateMailRequestModel):
    email_account = data.get('email_account')
    email_password = data.get('email_password')
    flag , info = change_email_password( mxdomain_ip, email_account, email_password)
    if flag:
        return {"code": 200, "msg": "修改成功", "data": info}
    else:
        return {"code": 500, "msg": "修改失败", "data": info}


class SendMailRequestModel(BaseModel):
    email_account: str
    email_password: str
    to_email: str
    title: str
    content: str
    def get(self, key: str, default: Any = None) -> Any:
        """支持 .get('key') 的方式访问属性"""
        return getattr(self, key, default)

@router.post("/send_mail", summary="发送邮件")
async def router_send_mail(data: SendMailRequestModel):
    # 实现发送邮件逻辑
    email_account = data.get('email_account')
    email_password = data.get('email_password')
    to_email = data.get('to_email')
    title = data.get('title')
    content = data.get('content')

    flag, info = send_mail(mxdomain, mxdomain_ip, email_account, email_password, to_email, title, content)
    if flag:
        return {"code": 200, "msg": "发送成功", "data": info}
    else:
        return {"code": 500, "msg": "发送失败", "data": info}

app.include_router(router)



# 启动服务
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=19012)
    """
    nohup python /root/mail_home/p2_暴露服务.py >/dev/null 2>&1 &
    """
    
