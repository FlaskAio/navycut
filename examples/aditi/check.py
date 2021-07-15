from os import environ
environ.setdefault('NAVYCUT_SETTINGS_MODULE', 'aditi.settings')

import navycut; navycut.setup()


def main():
    from aniket.models import Author
    na = Author(name="aniket gb4", picture="piccth")
    na.save()
    print ("done")

if __name__ == "__main__":
    main()