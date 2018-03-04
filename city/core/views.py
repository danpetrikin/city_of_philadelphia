from django.shortcuts import render
from django.http import JsonResponse
import urllib
import re

def home(request):
    account_number = request.GET.get('account', '161113200')
    
    try:
        url = "http://www.phila.gov/revenue/realestatetax/?txtBRTNo=%s" % account_number
        with urllib.request.urlopen(url) as response:
            str = response.read().decode('utf-8')
        #print (str)
        p = re.compile(r'\"ctl00_BodyContentPlaceHolder_GetTaxInfoControl_frm_lblPropertyAddress\">(.*?)</span></div>')
        address = p.findall(str)[0]    
        
        p = re.compile(r'<div><span><b>BRT#:</b></span></span><span id="ctl00_BodyContentPlaceHolder_GetTaxInfoControl_frm_lblPropertyTaxAccountNo">(.*?)</span></div>')
        account_number = p.findall(str)[0]
        
        p = re.compile(r'<div><span><b>Owner Name:</b></span></span><span id="ctl00_BodyContentPlaceHolder_GetTaxInfoControl_frm_lblOwnerName">(.*?)</span></div>')
        owner = p.findall(str)[0]
        
        p = re.compile(r'<table class="grdRecords".*?>(.*?)</table>', re.DOTALL)
        table_info = p.findall(str)
        
        row = re.compile(r'<tr class="grdAlternatingRow">(.*?)</tr>', re.DOTALL)
        
        rows = row.findall(table_info[0])
        
        balance_list = []
        for r in rows:
            count = 0
            td = re.compile(r'<td.*?><font color="Black">(.*?)</font></td>', re.DOTALL)
            td_list = td.findall(r)
            for t in td_list:
                count += 1
                if count == 6:
                    t = t.replace('$','')
                    t = float(t)
                    
                    balance_list.append(t)
    
        total = 0
        for balance in balance_list:
            total += balance
        
        return JsonResponse({
            'address':address,
            'account number': account_number,
            'owner':owner,
            'balance_list':balance_list,
            'total_balance': total,
        })
    except:
        return JsonResponse({'account unknown':True})