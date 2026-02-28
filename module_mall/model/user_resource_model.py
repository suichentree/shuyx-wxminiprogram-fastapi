# 导入sqlalchemy框架中的相关字段
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, DateTime, func, Index, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, MappedColumn

# 导入公共基类
from base.base_model import myBaseModel

# 用户资源表
class UserResourceModel(myBaseModel):
    """
    用户资源表 t_user_resources
    存储用户资源信息
    """
    __tablename__ = 't_user_resources'

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True, comment='订单id')
    user_id: Mapped[int] = MappedColumn(Integer, nullable=False, comment='用户id')
    # 资源信息
    resource_id: Mapped[int] = MappedColumn(Integer, nullable=False, comment='资源id')
    resource_type_name: Mapped[str] = MappedColumn(String(50), nullable=False, comment='资源类型,如测试资源，课程资源等')
    resource_type_code: Mapped[str] = MappedColumn(String(50), nullable=False, comment='资源类型编码,如EXAM, COURSE, VIP等')
    resource_status: Mapped[str] = MappedColumn(String(20), default='ACTIVE', comment='资源状态 ACTIVE-有效，INACTIVE-无效')
    resource_expire_time: Mapped[datetime] = MappedColumn(DateTime, nullable=False, comment='资源过期时间。只有当资源有效时，该字段才有用。例如：会员资源的过期时间')

    create_time: Mapped[datetime] = MappedColumn(DateTime, comment='创建时间', default=func.now())
    update_time: Mapped[datetime] = MappedColumn(DateTime, comment='更新时间', default=func.now(), onupdate=func.now())

    # 添加索引
    __table_args__ = (
        Index('index_id', 'id'),
        Index('index_order_no', 'order_no'),
        Index('index_user_id', 'user_id'),
        Index('index_status', 'status'),
    )