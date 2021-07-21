from tkinter import *
import sqlite3
from tkinter import messagebox, Menu
import requests # helps us to get the data
import json # helps us to pass the data
from plyer import notification

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap('favicon.ico')

con = sqlite3.connect('coin.db')
cObj = con.cursor()
cObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT,amount INTEGER,price REAL)")
con.commit()
'''cObj.execute("INSERT INTO coin VALUES(1,'BTC',2,3200)")
con.commit()
cObj.execute("INSERT INTO coin VALUES(2,'ETH',10,5600)")
con.commit()
cObj.execute("INSERT INTO coin VALUES(3,'USDT',125,1550)")
con.commit()
cObj.execute("INSERT INTO coin VALUES(4,'EOS',100,2.05)")
con.commit()
cObj.execute("INSERT INTO coin VALUES(5,'XRP',20,100)")
con.commit()'''


def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()

    app_navig()
    app_header()
    my_portfolio()

def app_navig():
    def clear_all():
        cObj.execute("DELETE from coin")
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Portfolio Deleted-Add new coins!!!")
        reset()
    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label='Clear Portfolio', command=clear_all)
    file_item.add_command(label='Close App',command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pycrypto.config(menu=menu)



def my_portfolio():
    api_requests = requests.get(
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=300&convert=USD&CMC_PRO_API_KEY=e428c45e-383e-4db2-a75a-2c6edd7a97b4")
    api = json.loads(api_requests.content)

    cObj.execute("SELECT * FROM coin")
    coins = cObj.fetchall()

    def font_color(amount):
        if amount >= 0:
            return "green"
        else:
            return "red"

    def insert_coin():
        cObj.execute("INSERT INTO coin(symbol, price, amount) VALUES(?, ?, ?)",
                     (symbol_txt.get(), price_txt.get(), amount_txt.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin added to Portfolio successfully!!!")
        reset()

    def update_coin():
        cObj.execute("UPDATE coin SET symbol=?,price=?,amount=? where id=?",
                     (symbol_update.get(), price_update.get(), amount_update.get(), id_update.get()))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin information updated to Portfolio successfully!!!")
        reset()

    def delete_coin():
        cObj.execute("DELETE from coin where id=?", (id_delete.get(),))
        con.commit()
        messagebox.showinfo("Portfolio Notification", "Coin deleted from Portfolio successfully!!!")
        reset()

    '''for i in range(5):
        print(api['data'][i]['symbol'])
        print("{0:.2f}".format(api['data'][i]['quote']['USD']['price']))
        print("--------------------")'''
    c = 1
    total_amount_paid = 0
    net_pl_amount = 0
    total_curr = 0

    for i in range(300):
        for coin in coins:
            if api['data'][i]['symbol'] == coin[1]:
                total_paid = coin[2] * coin[3]
                current_price = coin[2] * api['data'][i]['quote']['USD']['price']
                pl_per_coin = api['data'][i]['quote']['USD']['price'] - coin[3]
                pl_amount = pl_per_coin * coin[2]

                net_pl_amount += pl_amount
                total_curr += current_price
                total_amount_paid += total_paid

                '''print(api['data'][i]['name'] + "-" + api['data'][i]['symbol'])
                print("Price - {0:.2f}".format(api['data'][i]['quote']['USD']['price']))
                print("Total number of coins: ", coin["no_of_coins"])
                print("Total amount invested: ", "{0:0.2f}".format(total_paid))
                print("Current value: ", "{0:0.2f}".format(current_price))'''

                portfolio_id = Label(pycrypto, text=coin[0], bg="light grey", fg="black",
                             font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
                portfolio_id.grid(row=c, column=0, sticky=N + S + E + W)

                name = Label(pycrypto, text=api['data'][i]['name'] + " " + api['data'][i]['symbol'] , bg="light grey", fg="black", font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
                name.grid(row=c, column=1, sticky=N+S+E+W)

                price = Label(pycrypto, text="{0:.2f}".format(api['data'][i]['quote']['USD']['price']), bg="light grey", fg="black", font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
                price.grid(row=c, column=2, sticky=N+S+E+W)

                no_of_coins = Label(pycrypto, text=coin[2], bg="light grey", fg="black", font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
                no_of_coins.grid(row=c, column=3, sticky=N+S+E+W)

                amount_paid = Label(pycrypto, text="${0:0.2f}".format(total_paid), bg="light grey", fg="black", font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
                amount_paid.grid(row=c, column=4, sticky=N+S+E+W)

                curr_val = Label(pycrypto, text="${0:0.2f}".format(current_price), bg="light grey", fg="black", font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
                curr_val.grid(row=c, column=5, sticky=N+S+E+W)

                pl_coin = Label(pycrypto, text="${0:0.2f}".format(pl_per_coin), bg="light grey", fg=font_color(float("{0:0.2f}".format(pl_per_coin))), font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
                pl_coin.grid(row=c, column=6, sticky=N+S+E+W)

                pl_amount = Label(pycrypto, text="${0:0.2f}".format(pl_amount), bg="light grey", fg=font_color(float("{0:0.2f}".format(pl_amount))), font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
                pl_amount.grid(row=c, column=7, sticky=N+S+E+W)

                c += 1

    # INSERT DATA
    symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove", name='symbol')
    symbol_txt.grid(row=c+1, column=1)

    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=c + 1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=c + 1, column=3)

    add_coin = Button(pycrypto, text="Add Coin", bg="#142E54", fg="white", command=insert_coin, font="Lato 12",
                              borderwidth=2, relief="groove", padx="5", pady="5")
    add_coin.grid(row=c + 1, column=4, sticky=N + S + E + W)

    # UPDATE DATA
    id_update = Entry(pycrypto, borderwidth=2, relief="groove")
    id_update.grid(row=c + 2, column=0)

    symbol_update = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_update.grid(row=c + 2, column=1)

    price_update = Entry(pycrypto, borderwidth=2, relief="groove")
    price_update.grid(row=c + 2, column=2)

    amount_update = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_update.grid(row=c + 2, column=3)

    update_coin_txt = Button(pycrypto, text="Update Coin", bg="#142E54", fg="white", command=update_coin, font="Lato 12", borderwidth=2, relief="groove", padx="5", pady="5")
    update_coin_txt.grid(row=c + 2, column=4, sticky=N + S + E + W)

    # DELETE DATA
    id_delete = Entry(pycrypto, borderwidth=2, relief="groove")
    id_delete.grid(row=c + 3, column=3)

    delete_coin_txt = Button(pycrypto, text="Delete Coin", bg="#142E54", fg="white", command=delete_coin,
                             font="Lato 12", borderwidth=2, relief="groove", padx="5", pady="5")
    delete_coin_txt.grid(row=c + 3, column=4, sticky=N + S + E + W)

    # --------------------------------------------#
    amount_invest = total_amount_paid
    total_amount_paid = Label(pycrypto, text=int(total_amount_paid), bg="white", fg="blue", font=("Arial Bold", 10),
                              padx="5",
                              pady="5", borderwidth=2, relief="groove")
    total_amount_paid.grid(row=c, column=4, sticky=N + S + E + W)

    total_curr = Label(pycrypto, text=int(total_curr), bg="white", fg="blue", font=("Arial Bold", 10), padx="5", pady="5",
                       borderwidth=2, relief="groove")
    total_curr.grid(row=c, column=5, sticky=N + S + E + W)

    curr_amount = net_pl_amount
    net_pl_amount = Label(pycrypto, text=int(net_pl_amount), bg="white", fg=font_color(float("{0:0.2f}".format(net_pl_amount))), font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
    net_pl_amount.grid(row=c, column=7, sticky=N + S + E + W)

    api = ""

    refresh = Button(pycrypto, text="REFRESH", bg="yellow", fg="blue", command=reset, font=("Arial Bold", 10), borderwidth=2, relief="groove")
    refresh.grid(row=c+1, column=7, sticky=N + S + E + W)

    print("And hence the net amount for portfolio is ", net_pl_amount)
    if curr_amount < (0.9*amount_invest):
        notification.notify(
            title="welcome to CoinMarketCap portfolio",
            message="Hey, Your shares went down !! Do you wanna sell your shares? ",
            app_icon=None,
            timeout=100,
        )
    elif curr_amount > (1.1*amount_invest):
        notification.notify(
            title="welcome to CoinMarketCap portfolio",
            message="Hurray,Your shares are growing. Congratulations!! Keep going",
            app_icon=None,
            timeout=100,
    )


def app_header():
    portfolio_id = Label(pycrypto, text="Serial No.", bg="dark blue", fg="white",
                         font=("Arial Bold", 10), padx="5", pady="5", borderwidth=2, relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N + S + E + W)

    name = Label(pycrypto, text="Coin Name", bg="dark blue", fg="white", font=("Arial Bold", 10), padx="5", pady="5",
                 borderwidth=2, relief="groove")
    name.grid(row=0, column=1, sticky=N + S + E + W)

    price = Label(pycrypto, text="Price", bg="dark blue", fg="white", font=("Arial Bold", 10), padx="5", pady="5",
                  borderwidth=2, relief="groove")
    price.grid(row=0, column=2, sticky=N + S + E + W)

    no_of_coins = Label(pycrypto, text="coins owned", bg="dark blue", fg="white", font=("Arial Bold", 10), padx="5",
                        pady="5", borderwidth=2, relief="groove")
    no_of_coins.grid(row=0, column=3, sticky=N + S + E + W)

    amount_paid = Label(pycrypto, text="Total amount paid", bg="dark blue", fg="white", font=("Arial Bold", 10),
                        padx="5", pady="5", borderwidth=2, relief="groove")
    amount_paid.grid(row=0, column=4, sticky=N + S + E + W)

    curr_val = Label(pycrypto, text="Current Value", bg="dark blue", fg="white", font=("Arial Bold", 10), padx="5",
                     pady="5", borderwidth=2, relief="groove")
    curr_val.grid(row=0, column=5, sticky=N + S + E + W)

    pl_coin = Label(pycrypto, text="P/L per coin", bg="dark blue", fg="white", font=("Arial Bold", 10), padx="5",
                    pady="5", borderwidth=2, relief="groove")
    pl_coin.grid(row=0, column=6, sticky=N + S + E + W)

    total_pl = Label(pycrypto, text="Total P/L with coin", bg="dark blue", fg="white", font=("Arial Bold", 10),
                     padx="5", pady="5", borderwidth=2, relief="groove")
    total_pl.grid(row=0, column=7, sticky=N + S + E + W)

app_navig()
app_header()


my_portfolio()

pycrypto.mainloop()

cObj.close()
con.close()

print("program completed")
