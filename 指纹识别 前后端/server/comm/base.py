import json
from django.http import HttpResponse

'''
检查指定的参数是否存在
存在返回 True
不存在返回 False
'''
def isExit(param):
    if (param == None) or (param == ''):
        return False
    else:
        return True

'''
转换分页查询信息
'''
def parasePage(pageIndex, pageSize, pageTotal, count, data):
    return {'pageIndex': pageIndex, 'pageSize': pageSize, 'pageTotal': pageTotal, 'count': count, 'data': data}


'''
成功响应信息
'''
def success(msg='处理成功'):
    resl = {'code': 0, 'msg': msg}
    return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')


'''
成功响应信息, 携带数据
'''
def successData(data, msg='处理成功'):
    resl = {'code': 0, 'msg': msg, 'data': data}
    return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')


'''
系统警告信息
'''
def warn(msg='操作异常，请重试'):
    resl = {'code': 1, 'msg': msg}
    return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')


'''
系统异常信息
'''
def error(msg='系统异常'):
    resl = {'code': 2, 'msg': msg}
    return HttpResponse(json.dumps(resl), content_type='application/json; charset=utf-8')