#!/usr/bin/python
# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials
 
def wrspr(a,b,t,w,p):
    #変更してください
    key_name = '*****************.json'
    sheet_name = 'test'
     
    #APIにログイン
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(key_name, scope)
    gc = gspread.authorize(credentials)
     
    #セル'A1'に'TEST'と入力
    #num = 3
    #cell_number = 'A' + str(num)
    #input_value = 'TEST'
    test_value = [str(a), str(b), str(t), str(w), str(p)]
    wks = gc.open(sheet_name).sheet1
    #wks.update_acell(cell_number, input_value)
    wks.append_row(test_value)
