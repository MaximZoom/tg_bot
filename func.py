import requests
def get_translation(text,lang):
    URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    KEY = 'trnsl.1.1.20180506T080634Z.8624b3fee218b5e7.94d888f82f100ef6723009f1d8497a964fb5fe8f'
    TEXT = text
    LANG = lang
    r = requests.post(URL,{'key': KEY,'text':TEXT,'lang':LANG})
    return eval(r.text)



