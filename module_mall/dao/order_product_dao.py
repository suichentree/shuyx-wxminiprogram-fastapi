from module_mall.model.order_product_model import OrderProductModel
from base.base_dao import BaseDao

# 继承BaseDao类，专注于数据访问操作, 可添加自定义方法
class OrderProductDao(BaseDao[OrderProductModel]):
    def __init__(self):
        """初始化DAO实例"""
        super().__init__(model = OrderProductModel)

    # 除此之外，可以根据业务需求添加自定义方法


