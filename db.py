import time
import datetime
import os

class Database:


    def __init__(self, path):
        self.path = path
        self.items = {}
        self.load()
        self.key = self.items.keys()
        self.value = self.items.values()

    def load(self):
        self.items = {}
        with open(self.path + "/catalog.txt", "r", encoding="utf=8")as cat:
            for list in cat:
                exp = list.strip().split()
                if len(exp) == 2:
                    self.items[exp[0]] = exp[1]

    
    def save_item(self, curr_num, curr_name):
        self.curr_num = curr_num
        self.curr_name = curr_name
        f = open("data/catalog.txt", "a", encoding="utf-8")
        f.write(curr_num + "\t" + curr_name + "\n")
        f.close()

    def save_place(self, curr_num, place):
        self.place = place
        f = open("data/"+curr_num+".txt", "a", encoding="utf-8")
        f.write(place + "\t" + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + "\n")
        f.close()

    def find_item(self, message):
        a = 0
        inv_d = {value: key for key, value in self.items.items()}
        have_find = []
        if (message in self.key) or (message in self.value):
            if message in self.key:
                ort = message
            elif message in self.value:
                ort = inv_d.get(message, )
            with open(self.path + "/" + ort + ".txt", "r", encoding="utf=8") as _place:
                for _places in _place:
                    end = _places.strip().split()
                    have_find.append(end[0])
                    return have_find
        else:
            return a
    def del_file(self,name):
        self.inv_d = {value: key for key, value in self.items.items()}
        if (name in self.key) or (name in self.inv_d.keys):
            with open('data/catalog.txt', "w", encoding="utf=8") as myfile:
                del self.items[f"{name}"] 
                myfile.write(self.items)
                myfile.close()
            
       
            

            
        

        