# import xlsxwriter module
import xlsxwriter
import json

def getExcelData():

    workbook = xlsxwriter.Workbook('paymentReceipt.xlsx')

    # By default worksheet names in the spreadsheet will be
    # Sheet1, Sheet2 etc., but we can also specify a name.
    worksheet = workbook.add_worksheet("My payment bot sheet")
    # Some data we want to write to the worksheet.
    with open('partyData.json', 'r') as f:
        memberArray = json.loads(f.read())
    # Start from the first cell.
    # Rows and columns are zero indexed.
    row = 0
    col = 0
    header_data = ['Player ID', 'Player Name', 'Player Level', 'Player Damage', 'Player Payment']

    header_format = workbook.add_format({'bold': True,
                                        'bottom': 2,
                                        'bg_color': '#F9DA04'})

    for col_num, data in enumerate(header_data):
        worksheet.write(0, col_num, data, header_format)

    worksheet.set_column(0,0, 40)
    worksheet.set_column(0,1, 40)
    worksheet.set_column(0,2, 20)
    worksheet.set_column(0,3, 40)
    worksheet.set_column(0,4, 40)

    # Iterate over the data and write it out row by row.
    for PlayerID, PlayerName, PlayerLevel, PlayerDamage, PlayerPayment in memberArray:
    # print("##########################")
        #print(memberArray[row]["PlayerName"])
        worksheet.write(row+1, col, memberArray[row]["PlayerID"])
        worksheet.write(row+1, col + 1, memberArray[row]["PlayerName"])
        worksheet.write(row+1, col + 2, memberArray[row]["PlayerLevel"])
        worksheet.write(row+1, col + 3, memberArray[row]["PlayerDamage"])
        worksheet.write(row+1, col + 4, memberArray[row]["PlayerPayment"])
        row += 1

    workbook.close()
