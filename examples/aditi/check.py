from os import environ
environ.setdefault('NAVYCUT_SETTINGS_MODULE', 'aditi.settings')

import navycut; navycut.setup()
import typing as t

def main():
    from aniket.models import Author
    a:t.List[t.Type["Author"]] = Author.query.all()
    for i in a:
        print (i.name)
    na = Author(name="aniket gb4", picture="piccth")
    na.save()
    print ("done")

if __name__ == "__main__":
    main()