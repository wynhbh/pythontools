import os
import sys

def main(argv):
    """
    @param argv:
    @return:
    """
    btmp = get_btmp()
    wtmp = get_wtmp()

    confusion(btmp, wtmp)

    save()

    return

if __name__ == '__main__':
    main(sys.argv[1:])