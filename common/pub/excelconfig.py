# coding=utf-8
import xlwt


# 导出数据到excel
def export(fields, results, table_name, outputpath):
    '''
    :param fields:数据库取出的字段值
    :param results: 列表元组或者元组元组
    :param table_name:
    :param outputpath:
    :return:
    '''

    # 搜取所有结果
    # 获取MYSQL里面的数据字段名称
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('table_' + table_name, cell_overwrite_ok=True)

    # 写上字段信息
    for field in range(0, len(fields)):
        sheet.write(0, field, fields[field][0])

    # 获取并写入数据段信息
    row = 1
    col = 0
    for row in range(1, len(results) + 1):
        for col in range(0, len(fields)):
            sheet.write(row, col, u'%s' % results[row - 1][col])

    workbook.save(outputpath)