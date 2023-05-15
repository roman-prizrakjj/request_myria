import http.client
from web3 import Web3
from eth_account.messages import encode_defunct
import requests
import http.client
import json
from resource_req.headers import *
import logging
from loguru import logger
from time import sleep
from config import delay, claim_delay, delay_after_claim, user_agent



def claim(id_on_site, private_key, ethAddress):
    try:
        # ПОЛУЧАЕМ ВРЕМЯ С СЕРВЕРА
        sleep(delay)
        headers = headers1
        r = requests.get('https://myriaverse-api.myria.com/v1/time', headers=headers)
        time = json.loads(r.text)
        time = time['data']['time']

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

            try:
                # "GET", f"/v1/users/{ethAddress}"
                sleep(delay)
                conn = http.client.HTTPSConnection("myriacore-api.myria.com")
                headers = headers5
                conn.request("GET", f"/v1/users/{ethAddress}", headers=headers)
                res = conn.getresponse()
                data = res.read()

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
                    sleep(delay)
                    conn.request("GET", "/v1/accounts/users", headers=headers)
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
                        # code = id_data['data']['campaign']['missionProgress'][0]['code']
                        # status_email = id_data['data']['campaign']['missionProgress'][0]['status']
                        # email = id_data['data']['user']['email']
                        # verified_at = id_data['data']['user']['verifiedAt']
                        alliance_id = id_data['data']['user']['allianceId']


                        if available_points < 500:
                            for i in range(0, 500, 100):
                                if available_points == i:
                                    return False, i/100, None


                        try:
                            if alliance_id == 1:
                                id_1, id_2, id_3, id_4, id_5, id_6 = 13, 14, 15, 16, 17, 18
                            if alliance_id == 2:
                                id_1, id_2, id_3, id_4, id_5, id_6 = 1, 2, 3, 4, 5, 6
                            if alliance_id == 3:
                                id_1, id_2, id_3, id_4, id_5, id_6 = 7, 8, 9, 10, 11, 12



                            sleep(claim_delay)
                            conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                            payload = "{\"rewardId\":" + str(id_1) + ",\"userId\":" + str(id_on_site) + "}"

                            headers = headers11
                            conn.request("POST", "/v1/rewards/user-claim", payload, headers)
                            res = conn.getresponse()


                            sleep(claim_delay)
                            conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                            payload = "{\"rewardId\":" + str(id_2) + ",\"userId\":" + str(id_on_site) + "}"

                            headers = headers11
                            conn.request("POST", "/v1/rewards/user-claim", payload, headers)
                            res = conn.getresponse()


                            sleep(claim_delay)
                            conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                            payload = "{\"rewardId\":" + str(id_3) + ",\"userId\":" + str(id_on_site) + "}"
                            headers = headers11
                            conn.request("POST", "/v1/rewards/user-claim", payload, headers)
                            res = conn.getresponse()


                            sleep(claim_delay)
                            conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                            payload = "{\"rewardId\":" + str(id_4) + ",\"userId\":" + str(id_on_site) + "}"
                            headers = headers11
                            conn.request("POST", "/v1/rewards/user-claim", payload, headers)
                            res = conn.getresponse()


                            sleep(claim_delay)
                            conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                            payload = "{\"rewardId\":" + str(id_5) + ",\"userId\":" + str(id_on_site) + "}"
                            headers = headers11
                            conn.request("POST", "/v1/rewards/user-claim", payload, headers)
                            res = conn.getresponse()


                            sleep(claim_delay)
                            conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                            payload = "{\"rewardId\":" + str(id_6) + ",\"userId\":" + str(id_on_site) + "}"
                            headers = headers11
                            conn.request("POST", "/v1/rewards/user-claim", payload, headers)
                            res = conn.getresponse()


                            try:
                                # ПРОВЕРКА ПОИНТОВ
                                sleep(delay_after_claim)
                                conn = http.client.HTTPSConnection("myriacore-campaign-api.myria.com")
                                headers = headers9
                                conn.request("GET", f"/v1/users/{id_on_site}/campaign-id/1", headers=headers)
                                res = conn.getresponse()
                                data = res.read()
                                id_data = json.loads(data.decode())

                                status1 = id_data['data']['rewards'][0]['rewardStatus']
                                status2 = id_data['data']['rewards'][1]['rewardStatus']
                                status3 = id_data['data']['rewards'][2]['rewardStatus']
                                status4 = id_data['data']['rewards'][3]['rewardStatus']
                                status5 = id_data['data']['rewards'][4]['rewardStatus']
                                status6 = id_data['data']['rewards'][5]['rewardStatus']

                                if status1 != 'CLAIMED' or status2 != 'CLAIMED' or status3 != 'CLAIMED' or status4 != 'CLAIMED' or status5 != 'CLAIMED' or status6 != 'CLAIMED':
                                    return False, 5, None

                                answer = f"{id_data['data']['rewards'][0]['description']}: {id_data['data']['rewards'][0]['rewardStatus']}\n" \
                                         f"{id_data['data']['rewards'][1]['description']}: {id_data['data']['rewards'][1]['rewardStatus']}\n" \
                                         f"{id_data['data']['rewards'][2]['description']}: {id_data['data']['rewards'][2]['rewardStatus']}\n" \
                                         f"{id_data['data']['rewards'][3]['description']}: {id_data['data']['rewards'][3]['rewardStatus']}\n" \
                                         f"{id_data['data']['rewards'][4]['description']}: {id_data['data']['rewards'][4]['rewardStatus']}\n" \
                                         f"{id_data['data']['rewards'][5]['description']}: {id_data['data']['rewards'][5]['rewardStatus']}\n"
                                #
                                # print(answer)

                                if status1 == status2 == status3 == status4 == status5 == status6 == 'CLAIMED':
                                    return True, 5, answer




                            except Exception as e:
                                logging.error(f"Не смог проверить поинты: {e}", exc_info=True)
                                logger.error(f"Не смог проверить поинты")

                        except Exception as e:
                            logging.error(f"Не смог заклеймить: {e}", exc_info=True)
                            logger.error(f"Не смог заклеймить")

                    except Exception as e:
                        logging.error(f"Не смог получить инфо об акке: {e}", exc_info=True)
                        logger.error(f"Не смог получить инфо об акке")

                except Exception as e:
                    logging.error(f"Ошибка в GET, /v1/accounts/users: {e}", exc_info=True)
                    logger.error(f"Ошибка в GET, /v1/accounts/users")

            except Exception as e:
                logging.error(f"Ошибка в GET, /v1/users/ethAddress: {e}", exc_info=True)
                logger.error(f"Ошибка в GET, /v1/users/ethAddress")

        except Exception as e:
            logging.error(f"Ошибка в /v1/accounts/login/wallet: {e}", exc_info=True)
            logger.error(f"Ошибка в /v1/accounts/login/wallet")

    except Exception as e:
        logging.error(f"Не смог получить время {e}", exc_info=True)
        logger.error(f"Не смог получить время")


