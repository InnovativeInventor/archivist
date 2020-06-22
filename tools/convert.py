with open("socialbot.txt", "r") as f:
    for each_line in f:
        if each_line.rstrip():
            print(" ".join(each_line.rstrip().split()[1:]))
