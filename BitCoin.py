# to read csv file
from csv import reader

# global varibles

data = {} 
mx_cut = 0 
mx_ID = '' 

class mem_transac():
      
    def __init__(self, txid, fee, weight, parents):
        global mx_cut
        global mx_ID
        self.txid = txid
        self.fee = int(fee)
        self.weight = int(weight)
        self.parents = [parent for parent in parents.strip().split(';')]
        if(self.parents[0] == '' and self.weight <= 4000000):
            data[self.txid] = {
                'fee': self.fee,
                'weight': self.weight,
                'parent': []
            }
            if(self.fee > mx_cut):
                mx_cut = self.fee
                mx_ID = self.txid
        else:
            if set(self.parents).issubset(data.ks()):
                amt = self.weight
                cut = self.fee
                for parent in self.parents:
                    if((amt + data[parent]['weight']) <= 4000000):
                        amt += data[parent]['weight']
                        cut += data[parent]['fee']
                    else:
                        break
                data[self.txid] = {
                                    'fee': cut,
                                    'weight': amt,
                                    'parent': self.parents
                                }
                if(cut > mx_cut):
                    mx_cut = cut
                    mx_ID = self.txid
            else:
                return

def parse_csv():
    with open("mempool.csv", "r") as file:
        next(file)
        csv_reader = reader(file)
        for row in csv_reader:
            mem_transac(row[0], row[1], row[2], row[3])


parse_csv()
open("block.txt", "w").close()
f = open("block.txt", "a")

def func_add(arr):
    
    for k in arr:
        if set(k).issubset(data.ks()):
            func_add(data[k]['parent'])
        
        f.write(f"{k} -> ")

for  k,val in data.items():
    
    if val['parent']:
    
        func_add(val['parent'])
    
    f.write(f"{k}\n")
    

f.close()
print("Success!!")