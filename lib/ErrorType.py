from enum import unique, Enum


@unique
class ErrorType(Enum):
    """使用枚举定义错误类型
    """
    SHEETERROR = u'Excel中sheet名称或者数量和标准格式不一致'
    NAMEERROR = u'基本信息表中姓名不能为空'
    NAMEALLDIGITERROR = u'基本信息表中姓名不能全部是数字'
    BIRTHDAYERROR = u'基本信息表中出生日期不能为空'
    BRANCHERROR = u'基本信息表中所属支社不能为空'
    FILETYPEERROR = u'文件类型错误,只能导入.xls.xlsx'
    FILEREPEATERROR = u'社员信息重复(姓名+出生日期)'
    DATAFORMATEERROR = u'日期格式错误(正确格式Ex:1980.01.01)'
    DATAFORMATEERROR1 = u'日期格式错误(正确格式Ex:1980-01-01)'
    OTHERERROR = u'其他错误'
