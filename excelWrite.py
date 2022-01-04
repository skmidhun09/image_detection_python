import xlwt
from xlwt import Workbook
  
# Workbook is created
wb = Workbook()
row = 1
sheet1 = wb.add_sheet('PChainData')
sheet1.write(0, 0, 'IMAGE NAME')
i=1
while i <= 10:
    sheet1.write(0, i, 'P-'+str(i))
    i=i+1

def addtoExcel(chains,imgName,totCount):
  global row
  sheet1.write(row,0,imgName)
  for chain in chains.items():
    sheet1.write(row, chain[0],str(chain[1]))  
  if row == totCount:
    wb.save('OUTPUT\pearl_chain_data.xls')
  row = row + 1