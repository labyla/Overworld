import tls_client
from random import choice
import ua_generator
from web3 import Web3
from eth_account import Account, messages
import time

class Overworld:
    def __init__(self, address, private_key, twitter_auth_token, proxy):
        self.Address = Web3.to_checksum_address(address)
        self.PrivateKey = private_key
        self.TwitterAuthToken = twitter_auth_token

        self.session = tls_client.Session(client_identifier = choice(['Chrome110', 'chrome111', 'chrome112']))
        self.session.proxies.update({
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        })
        self.UserAgent = self.random_user_agent
    
    def LinkWallet(self):
        headers = {
            'content-type': 'application/json',
            'origin': 'https://whitelist.overworld.games',
            'referer': 'https://whitelist.overworld.games/',
            'user-agent': self.UserAgent
        }
        json_data = {
            'balance': 0,
            'wallet_address': self.Address,
            'network': {
                'name': 'homestead',
                'chainId': 1,
                'ensAddress': '0x00000000000C2E074eC69A0dFb2997BA6C7d2e1e',
            },
        }

        response = self.session.post("https://owapi.ovrwrld.net/applicants", headers=headers, json=json_data)


        self.OverWorld_uuid = response.json()['uuid']
        print(self.OverWorld_uuid)
        MessageForSign = messages.encode_defunct(text=self.OverWorld_uuid)
        SignedMessage = Account.sign_message(MessageForSign, private_key=self.PrivateKey)
        Signature = SignedMessage.signature.hex()
        print(Signature)

        headers = {
            'content-type': 'application/json',
            'origin': 'https://whitelist.overworld.games',
            'referer': 'https://whitelist.overworld.games/',
            'user-agent': self.UserAgent
        }
        json_data = {
            'signed_message': Signature
        }
        response = self.session.post(f'https://owapi.ovrwrld.net/applicants/{self.OverWorld_uuid}/message', headers=headers, json=json_data)
        return response.status_code

    def LinkTwitter(self):
        cookies = {
            'auth_token': self.TwitterAuthToken
        }
        response = self.session.get("https://twitter.com", cookies=cookies)
        print(response.cookies)
        self.Twitter_csrfToken = response.cookies.get_dict()['ct0']
        

        headers = {
            'user-agent': self.UserAgent
        }
        response = self.session.get(f"https://owapi.ovrwrld.net/applicants/{self.OverWorld_uuid}/twitter/start?redirect_url=https://whitelist.overworld.games", headers=headers, allow_redirects=False)
        response = self.session.get(f"https://owapi.ovrwrld.net/applicants/{self.OverWorld_uuid}/twitter/connect?redir=https://whitelist.overworld.games", headers=headers, allow_redirects=False)


        TwitterAuthorizeLink = response.headers['Location']
        TwitterAuthorizeLink = "https://twitter.com/i/api/2/oauth2/authorize?" + TwitterAuthorizeLink[TwitterAuthorizeLink.find('?') + 1:]
        cookies = {
            'auth_token': self.TwitterAuthToken,
            'ct0': self.Twitter_csrfToken
        }
        headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'x-csrf-token': self.Twitter_csrfToken,
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session'
        }
        response = self.session.get(TwitterAuthorizeLink, cookies=cookies, headers=headers, timeout_seconds=15, allow_redirects=False)
        

        code = response.json()['auth_code']
        cookies = {
            'auth_token': self.TwitterAuthToken,
            'ct0': self.Twitter_csrfToken
        }
        headers = {
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/x-www-form-urlencoded',
            'x-csrf-token': self.Twitter_csrfToken,
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session'
        }
        data = {
            'approval': 'true',
            'code': code
        }
        response = self.session.post("https://twitter.com/i/api/2/oauth2/authorize", cookies=cookies, headers=headers, data=data, timeout_seconds=15, allow_redirects=False)
        

        response = self.session.get(response.json()['redirect_uri'], timeout_seconds=15, allow_redirects=True)
        return response.status_code
    
    def TweetTask(self):
        headers = {
            'user-agent': self.UserAgent
        }
        response = self.session.post(f"https://owapi.ovrwrld.net/applicants/{self.OverWorld_uuid}/tweet", headers=headers)
        return response.status_code

    def AnswerQuestions(self):
        headers = {
            'user-agent': self.UserAgent
        }
        json_data = {
            'questions_and_answers': [
                [
                    'What interests you about Overworld?',
                    'ysdfsd',
                ],
                [
                    'How do you plan on supporting the community and project?',
                    'asdasdsa',
                ],
                [
                    'What Web3 communities are you a part of?',
                    'ifgidffdid',
                ],
                [
                    'To receive notifications about future mints and product updates please enter your email address',
                    'dasdaspppdas@gmail.com',
                ],
                [
                    'I consent to receiving email communication from Xterio',
                    False,
                ],
            ],
        }
        response = self.session.post(f"https://owapi.ovrwrld.net/applicants/{self.OverWorld_uuid}/questionnaire", headers=headers, json=json_data)
        return response.status_code

    @property
    def random_user_agent(self) -> str:
        return ua_generator.generate(device="desktop", browser='chrome').text
    
if __name__ == "__main__":
    overworld = Overworld(
        "0x77869093BFe825C83C57Fa58c4B45eED60e2C58F",
        "private-key",
        "twitter-auth-token",
        "mr30046GzwA:MP1kX6i1Rq_country-de@91.239.130.17:44443"
    )
    
    try:
        print(overworld.LinkWallet())
        time.sleep(4)
        print(overworld.LinkTwitter())
        time.sleep(4)
        print(overworld.TweetTask())
        time.sleep(4)
        print(overworld.AnswerQuestions())
    except Exception as e:
        print(e)
    
    
    
    """    Account.enable_unaudited_hdwallet_features()
    account, mnemonic = Account.create_with_mnemonic()
    print(account.address)
    print(account.key.hex())
    print(mnemonic)"""