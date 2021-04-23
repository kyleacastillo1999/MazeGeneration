from random_maze import RandomMaze as Rm


def main():
    test = Rm(11, 11, 0, 0, 10, 9)
    test.generate_maze()
    test.print_maze()

    print("\nSolving breadth first")
    path1 = test.solve_breadth_first()
    while path1:
        point = path1.pop()
        print("Point(%s,%s)" % (point.get_x(), point.get_y()))

    print("\nSolving Depth First")
    path2 = test.solve_depth_first()
    while path2:
        point = path2.pop()
        print("Point(%s,%s)" % (point.get_x(), point.get_y()))


if __name__ == "__main__":
    main()
