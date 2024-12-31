def validate_card(card, length):
    evens = []
    odds = []
    products = []
    sum_products = 0
    sum_odds = 0
    for i in range(0, length):
        if length % 2 == 0:
            if (length - i) % 2 == 0:
                odds.append(card[length - 1 - i])
            else:
                evens.append(card[length - 1 - i])
        else:
            if (length - i) % 2 == 0:
                evens.append(card[length - 1 - i])
            else:
                odds.append(card[length - 1 - i])
    for element in evens:
        products.append(int(element) * 2)
    for element in odds:
        sum_odds += int(element)
    for element in products:
        # print(element)
        if int(element) >= 10:
            sum_products += int(str(element)[0])
            sum_products += int(str(element)[1])
        else:
            sum_products += int(element)

    sum = sum_products + sum_odds
    # print("Evens",evens)
    # print("sum_products",sum_products)
    # print("Odds",odds)
    # print("sum_odds",sum_odds)
    # print("Sum",sum)
    is_zero = sum % 10
    # print("is_zero",is_zero)
    if is_zero == 0:
        # print(card[0],card[1])
        if str(card[0]) == "4" and (length == 13 or length == 16):
            return "VISA"
        elif card[0] == "3":
            if (str(card[1]) == "4" or str(card[1]) == "7") and length == 15:
                return "AMEX"
        elif card[0] == "5":
            if (str(card[1]) == "1" or str(card[1]) == "2" or str(card[1]) == "3" or str(card[1]) == "4" or str(card[1]) == "5") and length == 16:
                return "MASTERCARD"
        return "INVALID"
    else:
        return "INVALID"


card = input("Number: ")
length = len(card)
# print(length)
if (length <= 0 or length < 13 or length > 16):
    # if length < 13:
    # print("Too short, try again")
    # elif length > 16:
    # print("Too long, try again")
    print("INVALID")
else:
    print(validate_card(card, length))
