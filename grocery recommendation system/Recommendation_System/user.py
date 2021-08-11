import random
import dataset

def get_user(search_item):
    filename = "C:\Disk E\grocery recommendation system\dataset\grocery_data.csv"
    fil = "C:\\Disk E\\grocery recommendation system\\dataset\\grocery_ratings_data.csv"
    search = search_item
    # writing to csv file
    try:
        with open(filename, newline='') as csv1, open(fil, newline='') as csv2:
            li = []
            for i in csv1:
                val = i.split(",")
                if search in val[1].lower():
                    # print(val)
                    # print(val[0])
                    li.append(val[0])
                    # print("----------")
            # print(li)
            val = random.randint(0, len(li) - 1)
            product = li[val]
            user1 = 0
            for i in csv2:
                spli = i.split(",")
                # print(spli)
                if spli[1] == str(product):
                    # print(spli)
                    # print(spli[0])
                    user1 = spli[0]

            user2 = random.randint(1, 65)
            return (int(user1),user2)
    except Exception as e:
        user1 = random.randint(1, 65)
        user2 = random.randint(1, 65)
        return (user1,user2)

def return_users(search):
    count=0
    while True:
        if count<3:
            val=get_user(search)
            if val[0] !=0:
                return val
        else:
            user1 = random.randint(1, 65)
            user2 = random.randint(1, 65)
            return (user1,user2)
#
# if __name__ == '__main__':
#     print(return_users("coco cola"))
