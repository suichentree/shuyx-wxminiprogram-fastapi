import time
import base64
import os
import json
import hashlib
import xml.etree.ElementTree as ET
from typing import Optional, Dict
from config.log_config import logger

# 微信支付V2配置
WECHAT_PAY_CONFIG = {
    # appid公众账号ID。是微信开放平台(移动应用)或微信公众平台(小程序、公众号)为开发者的应用程序提供的唯一标识。
    # 可以填写这三种类型中的任意一种APPID，但请确保该appid与mchid有绑定关系。
    'appid': 'wxf8a159d29ef63e5a',
    # 商户号。是微信支付系统生成并分配给每个商户的唯一标识符。
    'mch_id': '1422735102',
    'api_key': 'a6996e73902564cf314c8362cf9f4412',  # API密钥 v2和v3版本是同一个
    # 商户接收支付成功回调通知的地址
    'notify_url': 'https://wxtest.xiedajia.com/api/wechat/h5pay/v2/notify',
    # 退款通知URL
    'refund_notify_url': 'https://wxtest.xiedajia.com/api/wechat/h5pay/v2/refund-notify',
}


class WechatPayV2Util:
    """微信支付V2工具类"""

    @staticmethod
    def get_appid() -> str:
        """获取appid"""
        return WECHAT_PAY_CONFIG['appid']

    @staticmethod
    def get_mch_id() -> str:
        """获取商户号"""
        return WECHAT_PAY_CONFIG['mch_id']

    @staticmethod
    def get_api_key() -> str:
        """获取API密钥"""
        return WECHAT_PAY_CONFIG['api_key']

    @staticmethod
    def get_notify_url() -> str:
        """获取支付回调通知URL"""
        return WECHAT_PAY_CONFIG['notify_url']

    @staticmethod
    def get_refund_notify_url() -> str:
        """获取退款通知URL"""
        return WECHAT_PAY_CONFIG['refund_notify_url']

    @staticmethod
    def generate_nonce_str() -> str:
        """生成随机字符串 - 微信V2版本要求32位随机字符串"""
        # 从os.urandom获取16字节（128位）的随机数据
        random_bytes = os.urandom(16)
        # 将16字节转换为4个32位整数，然后格式化为8位十六进制大写字母
        hex_str = ''.join([
            f'{int.from_bytes(random_bytes[i:i + 4], byteorder="big"):08X}'
            for i in range(0, 16, 4)
        ])
        return hex_str

    @staticmethod
    def generate_timestamp() -> str:
        """生成时间戳"""
        return str(int(time.time()))

    @staticmethod
    def dict_to_xml(data_dict: Dict) -> str:
        """将字典转换为XML格式 - V2版本使用XML格式"""
        xml_str = '<xml>'
        for key, value in data_dict.items():
            if value is not None:
                xml_str += f'<{key}><![CDATA[{value}]]></{key}>'
        xml_str += '</xml>'
        return xml_str

    @staticmethod
    def xml_to_dict(xml_str: str) -> Dict:
        """将XML字符串转换为字典"""
        try:
            root = ET.fromstring(xml_str)
            result = {}
            for child in root:
                result[child.tag] = child.text
            return result
        except Exception as e:
            logger.error(f"XML解析失败: {str(e)}")
            return {}

    @staticmethod
    def generate_sign_v2(params: Dict) -> str:
        """
        生成V2版本签名 - 使用MD5签名算法
        签名规则：
        1. 将所有参数按参数名ASCII码从小到大排序
        2. 使用URL键值对的格式拼接成字符串
        3. 在字符串最后加上key=API_KEY
        4. 对字符串进行MD5加密并转为大写
        """
        # 过滤空值参数
        filtered_params = {k: v for k, v in params.items() if v is not None and v != ''}

        # 按参数名ASCII码从小到大排序
        sorted_params = sorted(filtered_params.items(), key=lambda x: x[0])

        # 拼接字符串
        sign_str = '&'.join([f"{k}={v}" for k, v in sorted_params])

        # 加上API密钥
        sign_str += f"&key={WechatPayV2Util.get_api_key()}"

        # MD5加密并转为大写
        md5_hash = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        return md5_hash.upper()

    @staticmethod
    def verify_sign_v2(params: Dict, sign: str) -> bool:
        """验证V2版本签名"""
        generated_sign = WechatPayV2Util.generate_sign_v2(params)
        return generated_sign == sign

    @staticmethod
    def build_h5_unifiedorder_body(
            order_no: str,
            amount: int,
            description: str,
            client_ip: str = "127.0.0.1",
            time_expire: str = None,
            attach: str = None
    ) -> Dict:
        """
        构建H5支付统一下单请求体 - V2版本
        """
        # 基础参数
        params = {
            'appid': WechatPayV2Util.get_appid(),
            'mch_id': WechatPayV2Util.get_mch_id(),
            'nonce_str': WechatPayV2Util.generate_nonce_str(),
            'body': description,  # 商品描述
            'out_trade_no': order_no,  # 商户订单号
            'fee_type': 'CNY',  # 货币类型，默认人民币
            'total_fee': str(amount),  # 金额，单位为分
            'spbill_create_ip': client_ip,  # 终端IP,必须传正确的用户端IP,支持ipv4、ipv6格式
            'notify_url': WechatPayV2Util.get_notify_url(),  # 接收微信支付异步通知回调地址，通知url必须为直接可访问的url，不能携带参数。
            'trade_type': 'MWEB',  # H5支付类型
            'scene_info': json.dumps({   # 支付的场景信息
                'h5_info': {
                    'type': 'Wap',  # H5支付场景类型，默认Wap
                    'wap_url': 'https://www.xiedajia.com',  # WAP站点URL
                    'wap_name': '谢大家网'   # WAP站点名称，限制127字符
                }
            })
        }

        # 可选参数
        if time_expire:
            params['time_expire'] = time_expire
        if attach:
            params['attach'] = attach

        # 生成签名
        params['sign'] = WechatPayV2Util.generate_sign_v2(params)

        return params

    @staticmethod
    def build_order_query_body(
            order_no: str = None,
            transaction_id: str = None
    ) -> Dict:
        """
        构建订单查询请求体 - V2版本
        """
        params = {
            'appid': WechatPayV2Util.get_appid(),
            'mch_id': WechatPayV2Util.get_mch_id(),
            'nonce_str': WechatPayV2Util.generate_nonce_str()
        }

        if transaction_id:
            params['transaction_id'] = transaction_id
        elif order_no:
            params['out_trade_no'] = order_no
        else:
            raise ValueError("商户订单号和微信订单号不能同时为空")

        # 生成签名
        params['sign'] = WechatPayV2Util.generate_sign_v2(params)

        return params

    @staticmethod
    def build_close_order_body(order_no: str) -> Dict:
        """
        构建关闭订单请求体 - V2版本
        """
        params = {
            'appid': WechatPayV2Util.get_appid(),
            'mch_id': WechatPayV2Util.get_mch_id(),
            'out_trade_no': order_no,
            'nonce_str': WechatPayV2Util.generate_nonce_str()
        }

        # 生成签名
        params['sign'] = WechatPayV2Util.generate_sign_v2(params)

        return params


