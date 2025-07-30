import femtotemplate.names as names


def test_no_numbers_in_names():
    number_chars = [str(i) for i in range(10)]
    for name in names.names:
        for c in name:
            if c in number_chars:
                print("name {} HAD A NUMBER!!".format(name))
                assert False
        print("name {} had no numbers".format(name))


if __name__ == "__main__":
    test_no_numbers_in_names()
