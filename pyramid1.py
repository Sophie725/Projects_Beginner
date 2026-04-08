def make_stars(n:int) -> None:
    for stars in range(n):
        for star in range(stars):
            print("*", end="")
        print()

print(make_stars(6))

print(make_stars(5))