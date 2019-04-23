import requests
import json
from lxml import html

# flag = 0


session_requests = requests.session()

link = 'https://parivahan.gov.in/rcdlstatus/?pur_cd=101'
response = session_requests.get(link)                                                                   # get page data from server
sourceCode = response.content                                                                           # get string of source code from response
htmlElem = html.document_fromstring(sourceCode)                                                         # make HTML element object
test = htmlElem.xpath(
    '//*[@id="j_id1:javax.faces.ViewState:0"]')[0].attrib['value']                                      # get value of unique token for each session
# print(test)
# while(flag==0){}
# try{}
captcha = htmlElem.xpath('//*[@id="form_rcdl:j_idt33:j_idt39"]')[0].get('src')
captcha_url = 'https://parivahan.gov.in' + captcha
image_response = session_requests.get(captcha_url, stream=True)
with open("sample.png", 'wb') as f:
    f.write(image_response.content)

captcha_manual = input("Enter Captcha: ")


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

final = session_requests.post('https://parivahan.gov.in/rcdlstatus/vahan/rcDlHome.xhtml', data=payload)



final_source_code = final.content
print(final_source_code)
final_htmlElem = html.document_fromstring(final_source_code)
name = final_htmlElem.xpath('//*[@id="form_rcdl:j_idt122"]/table[1]/tr[2]/td[2]')[0].text_content()
lastTransac = final_htmlElem.xpath('//*[@id="form_rcdl:j_idt122"]/table[1]/tr[4]/td[2]')[0].text_content() 
print(name)
print(lastTransac)

saveDict = {
    "name" : name,
    "lastTransac" : lastTransac
}

with open("adi.json", "w") as fp:
    json.dump(saveDict , fp) 



