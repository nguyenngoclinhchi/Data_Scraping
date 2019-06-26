from tabulate import tabulate

def main():
    print(tabulate([['Alice', 24], ['Bob', 19]], headers = ['Name', 'Age'], tablefmt = 'Github'))

if __name__ == '__main__':
    main()