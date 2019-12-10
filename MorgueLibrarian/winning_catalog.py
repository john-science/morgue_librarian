from sys import argv


def main():
    """
    1. parse input commandline for winning build/run info
    2. open/read all winning runs in /data/, bzip or not
    3. print lines that match search criteria
      a) exact matches
      b) wildcard match any
      c) match any in a list
      d) range operators from Python syntax: < > <= >= !=
        i) perhaps we can use eval() here, to build lambdas?
    """
    pass


if __name__ == '__main__':
    main()

