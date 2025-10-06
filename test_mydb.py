from mydb import MyDB
import os
def describe_test_my_db():
    def describe_constructor():
        def it_creates_a_new_file_when_file_does_not_exist():
            a_db = MyDB("test.db")

            assert os.path.isfile("test.db")
            
            os.remove("test.db")
        def it_saves_an_empty_array_to_a_new_file():
            a_db = MyDB("test.db")

            assert a_db.loadStrings() == []
            
            os.remove("test.db")
        def it_assigns_fname_attribute_on_init():
            a_db = MyDB("test.db")

            assert a_db.fname == "test.db"
            
            os.remove("test.db")
    def describe_load_strings_functionality():
        def load_strings_works_when_there_is_no_file_to_start():
            if os.path.isfile("test.db"):
                os.remove("test.db")
            a_db = MyDB("test.db")
            a_list = ["some", "very", "gummy", "worms"]

            a_db.saveStrings(a_list)

            b_list = a_db.loadStrings()

            assert a_list == b_list

            os.remove("test.db")
        def load_strings_works_when_there_is_a_file_to_start():
            dummy = MyDB("init.db")
            a_db = MyDB("init.db")
            a_list = ["some", "very", "gummy", "worms"]

            a_db.saveStrings(a_list)

            b_list = a_db.loadStrings()

            assert a_list == b_list
            os.remove("init.db")
        def load_strings_works_when_two_db_instances_handle_same_db():
            a_db = MyDB("test.db")
            b_db = MyDB("test.db")
            a_list = ["some", "very", "gummy", "worms"]

            a_db.saveStrings(a_list)

            a_res_list = a_db.loadStrings()

            b_res_list = b_db.loadStrings()

            assert a_res_list == a_list and a_res_list == b_res_list

            os.remove("test.db")
        def load_strings_works_when_large_string_arrays_are_passed_in():
            a_db = MyDB("test.db")

            a_list = [
                "apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew",
                "kiwi", "lemon", "mango", "nectarine", "orange", "papaya", "quince", "raspberry",
                "strawberry", "tangerine", "ugli", "vanilla", "watermelon", "xigua", "yam", "zucchini",
                "apricot", "blackberry", "blueberry", "cranberry", "dragonfruit", "eggplant",
                "feijoa", "guava", "hackberry", "imbe", "jackfruit", "kumquat", "lime", "mulberry",
                "navel_orange", "olive", "peach", "pear", "pineapple", "plum", "pomegranate", "pumpkin",
                "rhubarb", "soursop", "tomato", "ugni", "voavanga", "wolfberry", "xylocarp", "yuzu",
                "ziziphus", "almond", "brazilnut", "cashew", "chestnut", "coconut", "hazelnut",
                "macadamia", "pecan", "pistachio", "walnut", "acorn", "beechnut", "candlenut", "ginkgo",
                "hickory", "kapok", "monkey_puzzle", "pine_nut", "sheanut", "tiger_nut", "water_chestnut",
                "breadfruit", "cantaloupe", "durian", "entawak", "figberry", "genip", "huckleberry",
                "ilang", "jaboticaba", "langsat", "longan", "mamey", "nance", "okra", "persimmon",
                "quenepa", "rambutan", "safou", "tamarind", "ume", "voavanga_fruit", "wax_apple",
                "ximenia", "yellow_passionfruit", "zebra_tomato", "angelica", "basil", "cinnamon",
                "dill", "eucalyptus", "fennel", "garlic", "horseradish", "ivy_gourd", "jalapeno",
                "kelp", "lavender", "mint", "nutmeg", "oregano", "parsley", "rosemary", "sage",
                "thyme", "tarragon", "vanilla_bean", "wasabi", "yarrow", "zatar"
            ]

            a_db.saveStrings(a_list)

            a_res_list = a_db.loadStrings()

            assert a_res_list == a_list


            os.remove("test.db")
        def load_strings_works_with_empty_strings():

            a_db = MyDB("test.db")

            a_list = [""]

            a_db.saveStrings(a_list)

            a_res_list = a_db.loadStrings()

            assert a_res_list == a_list


            os.remove("test.db")

        
