import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
from time import sleep

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("Test").sheet1
# data = sheet.get_all_records()
# row = sheet.row_values(3)
# col = sheet.col_values(3)
# cell = sheet.cell(6,2).value
# pprint(cell)
# # insertRow = ["hello", 5, "red", "blue"]
# # sheet.add_rows(insertRow, 8)
def loopback():
    main()

def main():
    username = open(r"username.txt", "r")
    reads = username.readlines()
    number = 2
    while(number <= 50):
        for read in reads:
            akun = read.strip()
            username = akun.split("|")[0]
            password = akun.split("|")[1]
            print("update cell 4,"+ str(number) +" "+str(username))
            print()
            sheet.update_cell(number,4, username)
            sleep(2)
            number += 1

loopback()
