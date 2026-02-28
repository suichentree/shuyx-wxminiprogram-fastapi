# 导入sqlalchemy框架中的相关字段
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, DateTime, func, Index, DECIMAL
from sqlalchemy.orm import Mapped, MappedColumn

# 导入公共基类
from base.base_model import myBaseModel

class ProductModel(myBaseModel):
    """
    商品表 t_product
    存储所有商品信息，支持多种商品类型（如考试商品、课程商品、会员商品，优惠卷商品等）
    """
    __tablename__ = 't_product'

    id: Mapped[int] = MappedColumn(Integer, primary_key=True, autoincrement=True, comment='商品id')
    product_no: Mapped[str] = MappedColumn(String(64), unique=True, nullable=False, comment='商品编号')
    product_name: Mapped[str] = MappedColumn(String(64), nullable=False, comment='商品名称')

    # 其他商品信息
    description: Mapped[str] = MappedColumn(String(1000), nullable=True, comment='商品描述')
    cover_image: Mapped[str] = MappedColumn(String(500), nullable=True, comment='商品封面图')
    current_price: Mapped[Decimal] = MappedColumn(DECIMAL(10, 2), nullable=False, comment='商品现价')
    original_price: Mapped[Decimal] = MappedColumn(DECIMAL(10, 2), nullable=True, comment='商品原价')
    status: Mapped[int] = MappedColumn(Integer, default=1, comment='商品状态 1上架 0下架')

    # 商品对应的资源信息
    resource_id: Mapped[int] = MappedColumn(Integer, nullable=True, comment='关联的资源id。一个商品需要关联一个资源，如考试商品关联考试资源、课程商品关联课程资源等')
    resource_type_name: Mapped[str] = MappedColumn(String(100), nullable=False, comment='商品类型名称,如：考试商品、课程商品、会员商品等')
    resource_type_code: Mapped[str] = MappedColumn(String(50), nullable=False, comment='商品类型编码，如：EXAM, COURSE, VIP')

    create_time: Mapped[datetime] = MappedColumn(DateTime, comment='创建时间', default=func.now())

    # 添加索引
    __table_args__ = (
        Index('index_id', 'id'),
        Index('index_product_name', 'product_name'),
        Index('index_resource_type_name', 'resource_type_name'),
        Index('index_resource_type_code', 'resource_type_code'),
        Index('index_status', 'status'),
    )

    @property
    def is_free(self):
        """通过现价判断是否免费"""
        return self.current_price == 0

