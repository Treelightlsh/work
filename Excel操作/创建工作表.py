import xlsxwriter

header = '2019年南沙区初中毕业班学业考试                  英语听说考试考生登记表'
workbook = xlsxwriter.Workbook('test.xlsx')
worksheet = workbook.add_worksheet()
worksheet.merge_range('A1:H1', '')
f = workbook.add_format(({
    'align': 'center',
    'valign': 'top',
    'font_size': 20,
    'text_wrap': 1,
}))
worksheet.write('A1', header, f)
worksheet.set_row(0, 70)
worksheet.set_column('A:A',  5)
worksheet.set_column('B:B',  12)
worksheet.set_column('C:C',  10)
worksheet.set_column('D:D',  12.5)
worksheet.set_column('E:E',  5)
worksheet.set_column('F:F',  12)
worksheet.set_column('G:G',  10)
worksheet.set_column('H:H',  12.5)
workbook.close()
