def amount_to_coins(amount: int, coins: list[int]) -> list[int]:
    coins.sort(reverse=True)
    change = []
    for coin in coins:
        while amount >= coin:
            change.append(coin)
            amount -= coin
    return change
