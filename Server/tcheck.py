import requests

'''
文本审核接口
'''
AK=''
SK=''

def IsToxic(text):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(AK,SK)
    response = requests.get(host)
    if response:
        access_token =response.json()['access_token']


    request_url = "https://aip.baidubce.com/rest/2.0/solution/v1/text_censor/v2/user_defined"

    params = {"text":text}

    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.post(request_url, data=params, headers=headers)
    conclusion=''
    print(conclusion)
    if response:
        conclusion=response.json()['conclusion']
    conclusion= True if conclusion=='不合规' else False
    return conclusion
