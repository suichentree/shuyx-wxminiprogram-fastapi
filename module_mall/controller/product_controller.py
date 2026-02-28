from datetime import datetime

from fastapi import APIRouter, Body, Depends,Request
from sqlalchemy.orm import Session

from config.database_config import get_db_session
from config.log_config import logger
from module_exam.model.mp_user_model import MpUserModel
from module_exam.service.mp_user_service import MpUserService
from utils.response_util import ResponseUtil
from utils.jwt_util import JWTUtil

# 创建路由实例
router = APIRouter(prefix='',tags=['login相关接口'])

# 创建服务实例
MpUserService_instance = MpUserService()

# 密码登录接口
@router.post("/login")
def passwordLogin(username:str = Body(...),password:str = Body(...),db_session: Session = Depends(get_db_session)):
    logger.info(f'/login, username = {username} password = {password}')
    # 调用服务层方法，查询用户
    result = MpUserService_instance.get_one_by_filters(db_session,
            filters=MpUserModel(name=username,password=password).to_dict())
    if result is None:
        return ResponseUtil.error(data={"message": "登录失败,用户名或密码错误"})
    else:
        # 获取user id
        userId = result.id
        # 创建token,传入openId,userId生成token
        token = JWTUtil.create_token({"username": username, "userId": userId})
        # 返回响应数据
        return ResponseUtil.success(data={"token": token,"userName": username, "userId": userId})


