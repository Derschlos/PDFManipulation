import openpyxl as op



bearbe = []
wb = op.load_workbook(file)
for ws in wb.worksheets:
    for cells in ws.iter_rows(min_row = 2, max_col= 2):
        if cells[1].value is not None:
            line = cells[1].value
            line = line.replace(' ', '')
            line = line.split(',')
            for be in line:
                bearbe.append(be)

print(set(bearbe))
print(len(set(bearbe)))
