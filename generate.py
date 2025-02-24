def generator():
    def generate_password(length, use_symbols):
        characters = string.ascii_letters + string.digits
        if use_symbols:
            characters += string.punctuation

        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def password_generator():
        num_passwords = int(
            input(Fore.BLUE + Style.BRIGHT + "Enter the number of passwords: " + Fore.RESET + Style.RESET_ALL))
        length = int(
            input(Fore.BLUE + Style.BRIGHT + "Enter the length of each password: " + Fore.RESET + Style.RESET_ALL))
        use_symbols = input(
            Fore.BLUE + Style.BRIGHT + "Use other symbols? (Yes/No): " + Fore.RESET + Style.RESET_ALL).lower() == "yes"

        passwords = set()
        while len(passwords) < num_passwords:
            password = generate_password(length, use_symbols)
            passwords.add(password)
            update_msg(f"{password + (' ' * int(len(password) + 1))}")

        with open("passwords.txt", "w") as file:
            for password in passwords:
                file.write(password + "\n")

        update_msg(Fore.LIGHTGREEN_EX + Style.BRIGHT + f'Successful generated {len(passwords)} passwords {" " * 15}')
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\nPasswords saved in the 'passwords.txt' file.")

    password_generator()
