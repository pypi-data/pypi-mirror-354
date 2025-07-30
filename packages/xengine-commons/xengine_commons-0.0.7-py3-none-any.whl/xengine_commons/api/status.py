from enum import IntEnum


class APIStatus(IntEnum):
    """应用状态码枚举类（IntEnum 版本，格式：NAME = (code, "description")）"""

    OK = (0, "成功")

    # 用户及登录相关 (1000-1099)
    LOGIN_FAILED = (1000, "登录失效/登录失败")
    USER_NOT_FOUND = (1001, "用户不存在")
    INVALID_CREDENTIALS = (1002, "用户名或密码错误")
    USER_ALREADY_EXISTS = (1003, "用户已存在")
    INVALID_USER_INPUT = (1004, "用户名或密码不符合要求")
    PERMISSION_DENIED = (1005, "用户无权限")

    # 接口及参数相关 (1100-1199)
    INVALID_REQUEST_FORMAT = (1100, "请求参数格式错误")
    INVALID_REQUEST_PARAMS = (1101, "请求参数不符合要求")
    API_NOT_FOUND = (1102, "接口不存在")
    API_RATE_LIMIT = (1103, "接口使用超限")

    # 数据或业务逻辑相关 (1200-1299)
    DATA_ERROR = (1200, "数据错误")
    DATA_NOT_FOUND = (1201, "数据不存在")
    BUSINESS_LOGIC_ERROR = (1202, "业务逻辑错误")

    # 第三方服务相关 (1300-1399)
    THIRD_PARTY_ERROR = (1300, "第三方服务异常")
    PAYMENT_FAILED = (1301, "第三方支付失败")
    SMS_SEND_FAILED = (1302, "短信发送失败")
    WECHAT_SEND_FAILED = (1303, "微信发送失败")
    EMAIL_SEND_FAILED = (1304, "邮件发送失败")
    FAX_SEND_FAILED = (1305, "传真发送失败")
    PHONE_CALL_FAILED = (1306, "电话外呼失败")

    # 页面服务相关 (1400-1499)
    PAGE_SERVICE_ERROR = (1400, "页面服务异常")
    PAGE_REDIRECT_FAILED = (1401, "页面跳转或打开失败")
    POPUP_FAILED = (1402, "页面弹窗提示失败")
    PAGE_CLOSE_FAILED = (1403, "页面关闭失败")
    INVALID_PAGE_ACTION = (1404, "无效的页面操作")
    PAGE_TIMEOUT = (1405, "页面响应超时")

    # 服务相关 (1500-1599)
    INTERNAL_SERVER_ERROR = (1500, "服务器内部错误")
    SERVER_OVERLOAD = (1501, "服务器使用超限")
    SERVER_TIMEOUT = (1502, "服务器响应超时")
    INVALID_RESPONSE_FORMAT = (1503, "服务器返回格式异常")

    def __new__(cls, value, description):
        """自定义构造方法，支持值和描述"""
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj._description_ = description
        return obj

    @property
    def description(self):
        """The description property."""
        return self._description_

    @classmethod
    def get_by_code(cls, code):
        """通过状态码获取枚举成员"""
        for member in cls:
            if member.value == code:
                return member
        raise ValueError(f"无效的状态码: {code}")

