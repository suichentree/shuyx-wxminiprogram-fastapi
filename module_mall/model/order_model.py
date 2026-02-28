# 导入sqlalchemy框架中的相关字段
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, DateTime, func, Index, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, MappedColumn

# 导入公共基类
from base.base_model import myBaseModel

# 订单表
class OrderModel(myBaseModel):
    """
    订单表 t_order
    存储用户订单信息
    """
    __tablename__ = 't_order'

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True, comment='订单id')
    user_id: Mapped[int] = MappedColumn(Integer, nullable=False, comment='用户id')
    order_no: Mapped[str] = MappedColumn(String(64), unique=True, nullable=False, comment='订单编号')
    trade_no: Mapped[str] = MappedColumn(String(100), nullable=True, comment='第三方交易编号,如微信交易号，支付宝交易号等')

    # 订单支付信息
    total_amount: Mapped[Decimal] = MappedColumn(DECIMAL(10, 2), nullable=False, comment='订单总金额')
    pay_amount: Mapped[Decimal] = MappedColumn(DECIMAL(10, 2), nullable=False, comment='实际支付金额')
    pay_channel: Mapped[str] = MappedColumn(String(50), nullable=True, comment='支付渠道')
    pay_status: Mapped[str] = MappedColumn(String(20), default='PENDING', comment='订单支付状态 PENDING-待支付，PAID-已支付，CANCELLED-已取消，REFUNDED-已退款')
    pay_time: Mapped[datetime] = MappedColumn(DateTime, nullable=True, comment='支付时间')
    refund_time: Mapped[datetime] = MappedColumn(DateTime, nullable=True, comment='退款时间')

    create_time: Mapped[datetime] = MappedColumn(DateTime, comment='创建时间', default=func.now())
    update_time: Mapped[datetime] = MappedColumn(DateTime, comment='更新时间', default=func.now(), onupdate=func.now())

    # 添加索引
    __table_args__ = (
        Index('index_id', 'id'),
        Index('index_order_no', 'order_no'),
        Index('index_user_id', 'user_id'),
        Index('index_status', 'status'),
    )