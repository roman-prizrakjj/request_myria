def clean_files():
    # Запись 0 в файл ref_counter
    with open("ref_counters.txt", "w") as file:
        file.write(str(0))
    # Удаляю все из "accounts.txt"
    with open("accounts.txt", "w") as file:
        file.write(str(''))