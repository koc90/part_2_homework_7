from model import Base
from seeds import fill_all_tables
from my_selects import my_selects


def main():
    Base.metadata.drop_all()
    Base.metadata.create_all()
    fill_all_tables()
    my_selects()


if __name__ == "__main__":
    main()
