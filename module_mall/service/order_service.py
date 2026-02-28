from module_mall.dao.order_dao import OrderDao
from module_mall.model.order_model import OrderModel
from base.base_service import BaseService

# 继承Service类，专注于业务操作, 可添加自定义方法
class OrderService(BaseService[OrderModel]):
    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        self.dao_instance = OrderDao()
        super().__init__(dao=self.dao_instance)

    # 可以根据业务需求添加自定义方法
