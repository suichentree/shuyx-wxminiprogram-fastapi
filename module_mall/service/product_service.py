from module_mall.dao.product_dao import ProductDao
from module_mall.model.product_model import ProductModel
from base.base_service import BaseService

# 继承Service类，专注于业务操作, 可添加自定义方法
class ProductService(BaseService[ProductModel]):
    def __init__(self):
        """
        初始化服务实例
        创建DAO实例并传递给基类
        """
        self.dao_instance = ProductDao()
        super().__init__(dao=self.dao_instance)

    # 可以根据业务需求添加自定义方法
