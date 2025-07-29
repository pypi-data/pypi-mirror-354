def number_guess_game():
    import random
    randnumber = random.randint(0,12)
    trys=3
    for _ in range(trys):
        guess_number=int(input("enter your guess "))
        if guess_number == randnumber:
            return f"correct the number was {randnumber}"
        
        else:
            if guess_number > randnumber:
                print("number guessed is bigger then genrated number")
            
            else:
                print("number guessed is smaller then genrated number")
            
            trys=trys-1

            if trys == 0:
                return f"sorry you failed the number was {randnumber}"
            