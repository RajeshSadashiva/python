import datetime
import pandas as pd
print("Welcome to super market\n")
print("Usage:\n")
print("Billing activities: To create an order use create_order() function\n")
print("Inventory activities:\n")
print("To list existing inventory use list_inventory() function\n")
print("To add new item to inventory use add_new_item(item,quantity,price,discount) function\n")
print("To update quantity of any item use update_quantity(item,quantity) function\n")
print("To update price of any item use update_price(item,price) function\n")
print("To update discount of any item use update_discount(item,discount) function\n")

def list_inventory():
    inventory=pd.read_csv("./inventory.csv")
    print(inventory)
    
def update_quantity(iName,iQuantity):
    inventory=pd.read_csv("./inventory.csv")
    inventory.at[inventory.index[inventory.Name==iName][0],'Quantity']=iQuantity
    inventory.to_csv("./inventory.csv", header=["Name","Quantity","Price","Discount"], index=False)
    
def update_price(iName,iPrice):
    inventory=pd.read_csv("./inventory.csv")
    inventory.at[inventory.index[inventory.Name==iName][0],'Price']=iPrice
    inventory.to_csv("./inventory.csv", header=["Name","Quantity","Price","Discount"], index=False)
    
def update_discount(iName,iDiscount):
    inventory=pd.read_csv("./inventory.csv")
    inventory.at[inventory.index[inventory.Name==iName][0],'Discount']=iDiscount
    inventory.to_csv("./inventory.csv", header=["Name","Quantity","Price","Discount"], index=False)
    
def add_new_item(iName,iQuantity,iPrice,iDiscount):
    inventory=pd.read_csv("./inventory.csv")
    inventory.loc[len(inventory.index)] = [iName,iQuantity,iPrice,iDiscount] 
    inventory.to_csv("./inventory.csv", header=["Name","Quantity","Price","Discount"], index=False)

def create_order():
    x1 = datetime.datetime.now().strftime("%d_%m_%Y_%H%M%S")
    cName = input('Name of the customer: ')
    x="./orders/"+x1+"_"+cName+".txt"
    f = open(x, "w")
    f.write("***************************************\n")
    f.write("Welcome to the Super Market\n")
    f.write("This bill is For :"+cName+" dated :"+x1+"\n")
    f.write("***************************************\n")
    inventory=pd.read_csv("./inventory.csv")
    order = pd.DataFrame(columns = ["Name","Quantity","Price","Discount"])
    response=input("Would you like to add an item to the basket if yes input y, else input N\n")
    while response=="y":
        oName = input('Which item would you like add to basket: ')
        oQuantity = input('Quantity Please: ')
        oQuantity=int(oQuantity)
        iQuantity=inventory.at[inventory.index[inventory.Name==oName][0],'Quantity']
        iQuantity=int(iQuantity)
        if iQuantity >= oQuantity:
            order=order.append(inventory[inventory["Name"]==oName],ignore_index=True)
            order.at[order.index[order.Name==oName][0],'Quantity']=oQuantity
        else:
            print("Not enough Quantity, item not added\n")
        response=input("Would you like to add any other item to the basket if yes input y, else input N\n")
    
    response=input("Remove any item\n")
    while response=="y":
        oName = input('Which item would you like remove from basket: ')
        order.at[order.index[order.Name==oName][0],'Quantity']=0
        response=input("Remove any other item\n")
    print("Now printing order\n")
    finalprice=0
    for ind in order.index:
        oName=order['Name'][ind]
        oQuantity=order['Quantity'][ind]
        oPrice=order['Price'][ind]
        oDiscount=order['Discount'][ind]
        iQuantity=inventory.at[inventory.index[inventory.Name==oName][0],'Quantity']
        inventory.at[inventory.index[inventory.Name==oName][0],'Quantity']=iQuantity-oQuantity
        finalprice=finalprice+(oQuantity*oPrice*(1-oDiscount*0.01))
    inventory.to_csv("./inventory.csv", header=["Name","Quantity","Price","Discount"], index=False)
    order = order.to_string(index=False)
    f.write(order)
    f.write("\n***************************************\n")
    f.write("\nFinal Price is: "+str(finalprice))
    f = open(x, "r")
    print(f.read())
