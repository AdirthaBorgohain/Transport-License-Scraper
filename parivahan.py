import requests
import json
from lxml import html

# flag = 0
session_requests = requests.session()

link = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
# get page data from server
response = session_requests.get(link)
# get string of source code from response
sourceCode = response.content
# make HTML element object
htmlElem = html.document_fromstring(sourceCode)
test = htmlElem.xpath(
    '//*[@id="j_id1:javax.faces.ViewState:0"]')[0].attrib['value']                                      # get value of unique token for each session
# print(test)
# while(flag==0){}
# try{}
captcha = htmlElem.xpath('//*[@id="form_rcdl:j_idt33:j_idt39"]')[0].get('src')
captcha_url = 'https://parivahan.gov.in' + captcha
image_response = session_requests.get(captcha_url, stream=True)
with open("captcha_image.png", 'wb') as f:
    f.write(image_response.content)

captcha_manual = input("Enter Captcha (captcha_image.png): ")

payload = {
    "javax.faces.partial.ajax": "true",
    "javax.faces.source: form_rcdl": "j_idt44",
    "javax.faces.partial.execute": "@all",
    "javax.faces.partial.render": "form_rcdl:pnl_show form_rcdl:pg_show form_rcdl:rcdl_pnl",
    "form_rcdl:j_idt44": "form_rcdl:j_idt44",
    "form_rcdl": "form_rcdl",
    "form_rcdl:tf_dlNO": "DL-0420110149646",
    "form_rcdl:tf_dob_input": "09-02-1976",
    "form_rcdl:j_idt33:CaptchaID": captcha_manual,
    "javax.faces.ViewState": test
}

final = session_requests.post(
    'https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml', data=payload)


final_source_code = final.content

final_htmlElem = html.document_fromstring(final_source_code)

current_status = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[1]/tr[1]/td[2]')[0].text_content()

name = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[1]/tr[2]/td[2]')[0].text_content()

date_of_issue = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[1]/tr[3]/td[2]')[0].text_content()

last_trans_loc = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[1]/tr[4]/td[2]')[0].text_content()

nontrans_valid_from = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[2]/tr[1]/td[2]/text()')[0]

nontrans_valid_to = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[2]/tr[1]/td[3]/text()')[0]

trans_valid_from = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[2]/tr[2]/td[2]/text()')[0]

trans_valid_to = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[2]/tr[2]/td[3]/text()')[0]

hazard_valid_till = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[3]/tr/td[2]')[0].text_content()

hill_valid_till = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt122"]/table[3]/tr/td[4]')[0].text_content()

cov_category = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt165_data"]/tr/td[1]')[0].text_content()

class_of_vehicle = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt165_data"]/tr/td[2]')[0].text_content()

cov_date_of_issue = final_htmlElem.xpath(
    '//*[@id="form_rcdl:j_idt165_data"]/tr/td[3]')[0].text_content()

print(current_status)
print(name)
print(date_of_issue)
print(last_trans_loc)
print(nontrans_valid_from)
print(nontrans_valid_to)
print(trans_valid_from)
print(trans_valid_to)
print(hazard_valid_till)
print(hill_valid_till)
print(cov_category)
print(class_of_vehicle)
print(cov_date_of_issue)

# saveDict = {
#     "Holder's Name": name,
#     "lastTransac": lastTransac
# }

# with open("adi.json", "w") as fp:
#     json.dump(saveDict, fp)
