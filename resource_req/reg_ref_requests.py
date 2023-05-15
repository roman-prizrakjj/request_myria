import http.client
from web3 import Web3
from eth_account.messages import encode_defunct
import requests
import http.client
import random
import subprocess
import json
import re
from resource_req.headers import *
import logging, sys
from loguru import logger
from time import sleep
from secrets import token_bytes
from coincurve import PublicKey
from sha3 import keccak_256
from config import delay, user_agent


def reg_ref_requests(referrer_id):
    try:
        # ПОЛУЧАЕМ ВРЕМЯ С СЕРВЕРА
        sleep(delay)
        headers = headers1
        r = requests.get('https://myriaverse-api.myria.com/v1/time', headers=headers)
        time = json.loads(r.text)
        time = time['data']['time']


        # Получаем приватник
        private_key = keccak_256(token_bytes(32)).digest()
        public_key = PublicKey.from_valid_secret(private_key).format(compressed=False)[1:]
        addr = keccak_256(public_key).digest()[-20:]
        private_key = private_key.hex()
        ethAddress = f"0x{addr.hex()}"


        # ПОЛУЧАЕМ СИГНАТУРУ 1
        private_key_hex = private_key
        private_key_bytes = bytes.fromhex(private_key_hex)
        w3 = Web3()
        msg = "Welcome to Myria!\n\nSelect 'Sign' to create and sign in to your Myria account.\n\nThis request will not trigger a blockchain transaction or cost any gas fees.\n\n{\"created_on\":\"" + str(
            time) + "\"}"
        message = encode_defunct(text=msg)
        signed_message = w3.eth.account.sign_message(message, private_key=private_key_bytes)
        signature = signed_message.signature.hex()

        try:
            conn = http.client.HTTPSConnection("myria.com")
            headers = {
                'authority': "myria.com",
                'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,tr;q=0.6",
                'cache-control': "no-cache",
                'pragma': "no-cache",
                'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                'sec-ch-ua-mobile': "?0",
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': "document",
                'sec-fetch-mode': "navigate",
                'sec-fetch-site': "none",
                'sec-fetch-user': "?1",
                'upgrade-insecure-requests': "1",
                'user-agent': f'{user_agent}'
            }

            conn.request("GET", f"/airdrop/?referCode={referrer_id}", headers=headers)
            res = conn.getresponse()
            data = res.read()

            try:

                # "POST", "/v1/accounts/login/wallet"
                sleep(delay)
                conn = http.client.HTTPSConnection("myriaverse-api.myria.com")
                payload = "{\"wallet_id\":\"" + str(ethAddress) + "\",\"signature\":\"" + str(
                    signature) + "\",\"message\":\"Welcome to Myria!\\n\\nSelect 'Sign' to create and sign in to your Myria account.\\n\\nThis request will not trigger a blockchain transaction or cost any gas fees.\\n\\n{\\\"created_on\\\":\\\"" + str(
                    time) + "\\\"}\"}"
                headers = headers2
                conn.request("POST", "/v1/accounts/login/wallet", payload, headers)
                res = conn.getresponse()
                data = res.read()
                acc_data_eth = json.loads(data.decode())
                user_account_id = acc_data_eth['data']['user_id']
                access_token = acc_data_eth['data']['access_token']
                refresh_token = acc_data_eth['data']['refresh_token']
                session_id = acc_data_eth['data']['session_id']


                # ПОЛУЧАЕМ СИГНАТУРУ 2
                private_key_hex = private_key
                private_key_bytes = bytes.fromhex(private_key_hex)
                w3 = Web3()
                msg = "Sign-in to your Myria L2 Wallet"
                message = encode_defunct(text=msg)
                signed_message = w3.eth.account.sign_message(message, private_key=private_key_bytes)
                signature2 = signed_message.signature.hex()

                try:
                    # Вызов скрипта script.js с передачей аргументов
                    process = subprocess.Popen(['node', 'sign.js', signature2, ethAddress], stdout=subprocess.PIPE)
                    output, error = process.communicate()
                    # Проверка наличия данных
                    result = json.loads(output.decode())
                    stark_key = result['starkkey']
                    r_value = result['r']
                    s_value = result['s']

                    try:
                        # "POST", "/v1/users"
                        sleep(delay)
                        conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                        payload = "{\"starkKey\":\"" + str(stark_key) + "\",\"walletAddress\":\"" + str(
                            ethAddress) + "\",\"accountId\":\"" + str(user_account_id) + "\",\"referrerId\":" + str(
                            referrer_id) + ",\"signature\":{\"r\":\"" + str(
                            r_value) + "\",\"s\":\"" + str(s_value) + "\"}}"
                        headers = headers3
                        conn.request("POST", "/v1/users", payload, headers)
                        res = conn.getresponse()
                        data = res.read()
                        id_data = json.loads(data.decode())
                        id_on_site = id_data['data']['id']

                        try:
                            # "GET", "/v1/accounts/users"
                            sleep(delay)
                            conn = http.client.HTTPSConnection("myriaverse-api.myria.com")
                            headers = {
                                'cookie': "session=" + str(session_id) + "; access_token=" + str(
                                    access_token) + "; refresh_token=" + str(refresh_token) + "",
                                'authority': "myriaverse-api.myria.com",
                                'accept': "application/json, text/plain, */*",
                                'accept-language': "en-US",
                                'cache-control': "no-cache",
                                'origin': "https://myria.com",
                                'pragma': "no-cache",
                                'referer': "https://myria.com/",
                                'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                                'sec-ch-ua-mobile': "?0",
                                'sec-ch-ua-platform': '"Windows"',
                                'sec-fetch-dest': "empty",
                                'sec-fetch-mode': "cors",
                                'sec-fetch-site': "same-site",
                                'user-agent': f'{user_agent}'
                            }

                            conn.request("GET", "/v1/accounts/users", headers=headers)
                            res = conn.getresponse()
                            data = res.read()

                            try:
                                # "GET", f"/v1/users/{ethAddress}"
                                sleep(delay)
                                conn = http.client.HTTPSConnection("myriacore-api.myria.com")
                                headers = headers5
                                conn.request("GET", f"/v1/users/{ethAddress}", headers=headers)
                                res = conn.getresponse()
                                data = res.read()

                                try:
                                    # "POST", "/v1/users/register-campaign"
                                    sleep(delay)
                                    conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                                    payload = "{\"userId\":" + str(id_on_site) + ",\"campaignId\":1}"
                                    headers = headers6
                                    conn.request("POST", "/v1/users/register-campaign", payload, headers)
                                    res = conn.getresponse()
                                    data = res.read()

                                    try:
                                        # "GET", f"/v1/users/wallet-address/{ethAddress}?campaignId=1"
                                        sleep(delay)
                                        conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                                        headers = headers7
                                        conn.request("GET", f"/v1/users/wallet-address/{ethAddress}?campaignId=1",
                                                     headers=headers)
                                        res = conn.getresponse()
                                        data = res.read()
                                        acc_data = json.loads(data.decode())
                                        account_id = acc_data['data']['accountId']

                                        try:
                                            # "PATCH", f"/v1/users/{id_on_site}/alliances"
                                            sleep(delay)
                                            conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                                            rand_alliance_id = random.randint(1, 3)
                                            payload = "{\"allianceId\":" + str(rand_alliance_id) + "}"  # рандомный альянс
                                            headers = headers8
                                            conn.request("PATCH", f"/v1/users/{id_on_site}/alliances", payload, headers)
                                            res = conn.getresponse()
                                            data = res.read()

                                            try:
                                                # Генерация временной почты
                                                email = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]

                                                try:
                                                    # ВЕРИФИКАЦИЯ ПОЧТЫ "POST", "/v1/accounts/email"
                                                    sleep(delay)
                                                    conn = http.client.HTTPSConnection("myriaverse-api.myria.com")
                                                    payload = "{\"email\":\"" + str(email) + "\",\"redirect\":5}"
                                                    headers = {
                                                        'cookie': "session=" + str(session_id) + "; access_token=" + str(
                                                            access_token) + "; refresh_token=" + str(refresh_token) + "",
                                                        'authority': "myriaverse-api.myria.com",
                                                        'accept': "application/json",
                                                        'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,tr;q=0.6",
                                                        'content-type': "application/json",
                                                        'origin': "https://myria.com",
                                                        'referer': "https://myria.com/",
                                                        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                                                        'sec-ch-ua-mobile': "?0",
                                                        'sec-ch-ua-platform': '"Windows"',
                                                        'sec-fetch-dest': "empty",
                                                        'sec-fetch-mode': "cors",
                                                        'sec-fetch-site': "same-site",
                                                        'user-agent': f'{user_agent}'
                                                    }
                                                    sleep(delay)
                                                    conn.request("POST", "/v1/accounts/email", payload, headers)
                                                    res = conn.getresponse()
                                                    data = res.read()

                                                    try:
                                                        # Ожидание нового письма
                                                        while True:
                                                            sleep(1)
                                                            getmsg_endp = f"https://www.1secmail.com/api/v1/?action=getMessages&login={email[:email.find('@')]}&domain={email[email.find('@') + 1:]}"
                                                            response = requests.get(getmsg_endp).json()
                                                            if response:
                                                                # Получение первого письма из списка
                                                                message = response[0]
                                                                # Извлечение id письма
                                                                id_ = message["id"]
                                                                # Формирование ссылки для получения сообщения
                                                                link = f"https://www.1secmail.com/mailbox/?action=readMessageFull&id={id_}&login={email[:email.find('@')]}&domain={email[email.find('@') + 1:]}"
                                                                break

                                                        try:
                                                            # Получаем текст письма
                                                            sleep(delay)
                                                            r = requests.get(link)
                                                            html = r.text
                                                            reg = r"https?://\S+?(?=<\/a>)"
                                                            match = re.search(reg, html)
                                                            if match != None:
                                                                link = match.group(0)

                                                            try:
                                                                # Переход по ссылке
                                                                sleep(delay)
                                                                headers = {
                                                                    'cookie': "session=" + str(
                                                                        session_id) + "; access_token=" + str(
                                                                        access_token) + "; refresh_token=" + str(
                                                                        refresh_token) + "",
                                                                    'authority': "myriaverse-api.myria.com",
                                                                    'accept': "application/json",
                                                                    'accept-language': "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,tr;q=0.6",
                                                                    'content-type': "application/json",
                                                                    'origin': "https://myria.com",
                                                                    'referer': "https://myria.com/",
                                                                    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
                                                                    'sec-ch-ua-mobile': "?0",
                                                                    'sec-ch-ua-platform': '"Windows"',
                                                                    'sec-fetch-dest': "empty",
                                                                    'sec-fetch-mode': "cors",
                                                                    'sec-fetch-site': "same-site",
                                                                    'user-agent': f'{user_agent}'
                                                                }
                                                                r = requests.get(link, headers=headers)

                                                                try:
                                                                    sleep(delay)
                                                                    conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                                                                    payload = "{\"missionCode\":\"VERIFY_EMAIL\"}"
                                                                    headers = headers11
                                                                    conn.request("PATCH", f"/v1/users/{id_on_site}/verify-email", payload, headers)
                                                                    res = conn.getresponse()
                                                                    data = res.read()


                                                                    try:
                                                                        # ПРОВЕРКА ПОИНТОВ
                                                                        sleep(delay)
                                                                        conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                                                                        headers = headers9
                                                                        conn.request("GET", f"/v1/users/{id_on_site}/campaign-id/1", headers=headers)
                                                                        res = conn.getresponse()
                                                                        data = res.read()
                                                                        id_data = json.loads(data.decode())
                                                                        available_points = id_data['data']['availablePoints']
                                                                        code = id_data['data']['campaign']['missionProgress'][0]['code']
                                                                        status_email = id_data['data']['campaign']['missionProgress'][0]['status']
                                                                        email = id_data['data']['user']['email']
                                                                        verified_at = id_data['data']['user']['verifiedAt']
                                                                        alliance_id = id_data['data']['user']['allianceId']

                                                                        ref_link = f'https://myria.com/airdrop/?referCode={id_on_site}'

                                                                        return status_email, id_on_site, private_key

                                                                    except Exception as e:
                                                                        logging.error(f"Не смог получить инфо об акке: {e}", exc_info=True)
                                                                        logger.error(f"Не смог получить инфо об акке")

                                                                except Exception as e:
                                                                    logging.error(f"Не смог подтвердить вериф. на сервере: {e}",exc_info=True)
                                                                    logger.error(f"Не смог подтвердить вериф. на сервере")

                                                            except Exception as e:
                                                                logging.error(f"Не смог перейти по ссылки из письма: {e}", exc_info=True)
                                                                logger.error(f"Не смог перейти по ссылки из письма")

                                                        except Exception as e:
                                                            logging.error(f"Не смог получить ссылку на письмо: {e}", exc_info=True)
                                                            logger.error(f"Не смог получить ссылку на письмо")

                                                    except Exception as e:
                                                            logging.error(f"Ошибка полученя письма: {e}", exc_info=True)
                                                            logger.error(f"Ошибка полученя письма")

                                                except Exception as e:
                                                    logging.error(f"Ошибка в POST, /v1/accounts/email: {e}", exc_info=True)
                                                    logger.error(f"Ошибка в POST, /v1/accounts/email")

                                            except Exception as e:
                                                logging.error(f"Ошибка создания почты: {e}", exc_info=True)
                                                logger.error(f"Ошибка создания почты")

                                        except Exception as e:
                                            logging.error(f"Ошибка в PATCH, /v1/users/id_on_site/alliances: {e}", exc_info=True)
                                            logger.error(f"Ошибка в GET, /v1/users/id_on_site/alliances")

                                    except Exception as e:
                                        logging.error(f"Ошибка в GET, /v1/users/wallet-address/ethAddress?campaignId=1: {e}", exc_info=True)
                                        logger.error(f"Ошибка в GET, /v1/users/wallet-address/ethAddress?campaignId=1")

                                except Exception as e:
                                    logging.error(f"Ошибка в POST, /v1/users/register-campaign: {e}", exc_info=True)
                                    logger.error(f"Ошибка в POST, /v1/users/register-campaign")

                            except Exception as e:
                                logging.error(f"Ошибка в GET, /v1/users/ethAddress: {e}", exc_info=True)
                                logger.error(f"Ошибка в GET, /v1/users/ethAddress")

                        except Exception as e:
                            logging.error(f"Ошибка в GET, /v1/accounts/users: {e}", exc_info=True)
                            logger.error(f"Ошибка в GET, /v1/accounts/users")

                    except Exception as e:
                        logging.error(f"Ошибка в POST, /v1/users: {e}", exc_info=True)
                        logger.error(f"Ошибка в POST, /v1/users")

                except Exception as e:
                    logging.error(f"Не смог получить starkkey: {e}", exc_info=True)
                    logger.error(f"Не смог получить starkkey")

            except Exception as e:
                logging.error(f"Ошибка в /v1/accounts/login/wallet: {e}", exc_info=True)
                logger.error(f"Ошибка в /v1/accounts/login/wallet")

        except Exception as e:
            logging.error(f"Ошибка в /airdrop/?referCode=referrer_id: {e}", exc_info=True)
            logger.error(f"Ошибка в /airdrop/?referCode=referrer_id")

    except Exception as e:
        logging.error(f"Не смог получить время {e}", exc_info=True)
        logger.error(f"Не смог получить время")


