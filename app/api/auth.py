from fastapi import APIRouter,HTTPException,Depends,Header
from typing import Optional

router = APIRouter()

VALID_API_KEYS = {
    "admin-key-123": {"role": "admin", "name": "管理员"},
    "user-key-456":  {"role": "user",  "name": "普通用户"},
}

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if not x_api_key:
        raise HTTPException(status_code = 401,detail = '请提供API KEY(Header:X-API-Key)')
    
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(status_code = 403,detail = '无效的API KEY')
    
    return VALID_API_KEYS[x_api_key]

@router.get('/me')
async def get_current_user(user:dict = Depends(verify_api_key)):
    """获取当前用户信息"""
    return user
