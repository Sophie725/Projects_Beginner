def inverted_pyramid(n:int):
    for stars in range(n, 0, -1):
        for star in range(stars):
            print("*", end="")
        print()
    print("Before ending")

print(inverted_pyramid(5))
print("After function")