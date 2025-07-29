def listndsort():
    LISTS = []
    try:
        make_list_range = int(input("Enter list range: "))
        if make_list_range <= 0:
            print("Please enter a positive integer for the list range.")
            return ""
    except ValueError:
        print("Wrong input {try entering numbers}")
        return ""

    for _ in range(make_list_range):
        try:
            number = int(input("Enter a number to be sorted by this function: "))
            LISTS.append(number)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
            return ""

    regorev = input("Reversed or regular? (press 1 for reversed, 2 for regular): ")
    if regorev == '1':
        return sorted(LISTS, reverse=True)
    elif regorev == '2':
        return sorted(LISTS)
    else:
        print("Wrong input {try entering 1 or 2}")
        return ""


