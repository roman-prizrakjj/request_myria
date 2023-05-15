import time
from resource_req.claim import claim
from resource_req.reg_acc_requests import reg_acc_requests
from resource_req.reg_ref_requests import reg_ref_requests
from resource_req.clean import clean_files
import logging, sys
from loguru import logger
from resource_req.send import run_send


logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "format": "<green>{time:YY-MM-DD HH:mm:ss}</green> | {level} | {message}",
            "level": "INFO",
            "colorize": True
        },
        {
            "sink": sys.stdout,
            "format": "<green>{time:YY-MM-DD HH:mm:ss}</green> | <red>{level}</red> | {message}",
            "level": "ERROR",
            "colorize": True
        },
    ]
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename='py_log.log',
    filemode='w'
)



if __name__ == "__main__":
    while 1:
        try:
            try:
                with open("accounts.txt", "r") as file:
                    lines = file.readlines()
                    if lines:
                        try:
                            id_on_site, private_key, ethAddress = lines[0].strip().split("#")
                            # logger.info('Смог распарсить')
                            if id_on_site == '' or id_on_site == 'None' or id_on_site == None:
                                # logger.error('Реф код пустой')
                                clean_files()
                                continue
                        except:
                            # logger.error('Не смог распарсить')
                            clean_files()
                            continue
                    else:
                        # logger.info('accounts.txt пустой')
                        id_on_site = ''
            except Exception as e:
                logging.error(f"Не смог прочитать accounts.txt {e}", exc_info=True)
                logger.error(f"Не смог прочитать accounts.txt")
                break


            try:
                with open("ref_counters.txt", "r") as file:  # Чтение значения ref_counter
                    ref_counters = int(file.readline().strip())
            except Exception as e:
                logging.error(f"Не смог прочитать 'ref_counters.txt' {e}", exc_info=True)
                logger.error(f"Не смог прочитать ref_counters.txt")
                break



            # РЕГАЕМ НОВЫЙ АКК
            if ref_counters == 0 and id_on_site == '': # Если вообще нет рефов, но есть ссылка
                try:
                    logger.info('Создаю новый акк')
                    start = time.time()
                    status_email, id_on_site, private_key, ethAddress = reg_acc_requests()
                    end = time.time()
                    if status_email != 'COMPLETED':
                        logger.info('Перезапускаю бота')
                        clean_files()
                        continue

                    logger.info(f"Приватник от нового ака: {private_key}")
                    logger.info(f"Реф код: {id_on_site}")
                    print('--------------------------------')
                    # Записываем сид нового ака
                    with open('accounts.txt', 'w') as f:
                        f.write(f'{id_on_site}#{private_key}#{ethAddress}\n')
                    continue

                except Exception as e:
                    logger.error(f"Ошибка регистрации нового акка")
                    logging.error(f"Ошибка регистрации нового акка: {e}", exc_info=True)
                    continue



            # РЕГАЕМ РЕФОВ
            if (0 <= ref_counters < 5) and id_on_site != '':  # Если кол-во рефов от 0-4, и есть код то доделываем рефов
                while ref_counters < 5:
                    try:
                        logger.info(f'Использую код: {id_on_site}')
                        logger.info(f'Регаю рефа номер: {ref_counters + 1}')
                        status_email, ref_link, private_key = reg_ref_requests(id_on_site)
                        ref_counters += 1
                        logger.info(status_email)


                        # Запись номер рефа которого зарегали в файл ref_counter
                        with open("ref_counters.txt", "w") as file:
                            file.write(str(ref_counters))

                    except Exception as e:
                        logger.error('Ошибка регистрации рефов')
                        logging.error(f"Ошибка регистрации рефов: {e}", exc_info=True)

                logger.info("Успешно зарегал 5 рефов")
                continue

            # КЛЕЙМ
            if ref_counters == 5 and id_on_site != '': # Если есть 5 рефов, то идем клеймить
                try:
                    print('--------------------------------')
                    logger.info('Набралось 5 рефов, пошел клеймить')
                    logger.info(f'Использую код: {id_on_site}')
                    ready, ref_counters, answer = claim(id_on_site, private_key, ethAddress)

                    if ready == False and ref_counters < 5:
                        logger.info(f'Не достаточно поинтов, обновляю файл, было рефов: {int(ref_counters)}')
                        # Запись новое кол-во в файл ref_counter
                        with open("ref_counters.txt", "w") as file:
                            file.write(str(int(ref_counters)))
                        continue

                    if ready == False and ref_counters == 5:
                        logger.info(f'Не смог заклеймить все ключи, пробую еще раз')
                        continue

                    if ready == True and ref_counters == 5:
                        # Запись готового ака в finish
                        with open("finish.txt", "a") as file:
                            file.write(f"{private_key}\n")
                        clean_files()
                        logger.info('Успешно заклеймил акк')
                        with open("finish.txt", 'r') as f:
                            acc_count = 0
                            for line in f:
                                acc_count += 1
                        logger.info(f'Кол-во аккаунтов в файле: {acc_count}')
                        # Отсылаем в телегу
                        run_send(private_key, answer)
                        print('################################\n')
                        print('################################')
                        continue

                except Exception as e:
                    logger.error('Ошибка клейма')
                    logging.error(f"Ошибка клейма: {e}", exc_info=True)
                    continue


        except Exception as e:
            logger.info('Ошибка в глобальном цикле while')
            logging.error(f"Ошибка в глобальном цикле while: {e}", exc_info=True)
            continue
