from tkinter import Tk,Label,Frame,Entry,Button,messagebox,Toplevel,simpledialog,filedialog
from tkinter.ttk import Style,Treeview,Scrollbar
from tkinter.ttk import Combobox
import time
from PIL import Image,ImageTk   #pip insatll pillow from cmd 
import random
# import
import Generator
import sqlite3
import mailing
from tkcalendar import Calendar
from datetime import date
import os,shutil,re


Generator.generate_tables()

list_logos=['logo.jpg','logo1.jpg','logo2.png','logo3.jpg',
            'logo4.jpg','logo5.png']



#createing root window
root=Tk()
root.title("Vanguard Banking Association(VBA).Com")
# making window fullscreen
root.state('zoomed')
root.resizable(width=False,height=False)
root.configure(bg='lightblue')

# to update time after each 1 sec
def update_time():
    dt=time.strftime('%A,%d-%b-%Y ⏰%r')
    lbl_dt.config(text=dt)
    root.after(1000,update_time)

# to change logo after each sec
def update_logo():
    logo=random.choice(list_logos) 
    img=Image.open(logo).resize((300,150))
    img_pil=ImageTk.PhotoImage(img,master=root)
    lbl_logo.configure(image=img_pil)
    lbl_logo.image=img_pil
    root.after(1000,update_logo)

def fp_frame():
    def call_main_frame():
        frm.destroy
        main_frame()

    def reset():
        e_acn.delete(0,'end')
        e_email.delete(0,'end')
        e_adhar.delete(0,'end')
        e_acn.focus()

    def send_otp():
            uacn=e_acn.get()
            uemail=e_email.get()
            uadhar=e_adhar.get()

            if len(uacn)==0 or len(uemail)==0 or len(uadhar)==0:
                messagebox.showerror('forgot','empty field are not allowed')
                return
            
            if  not uacn.isdigit():
                messagebox.showerror("Login","Account Number Should Be In Digit")
                return 

            if not re.fullmatch(r'[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-zA-Z]+',uemail):
                messagebox.showerror("Forgot Password","Incorrect format of email")
                return
            
            if not uadhar.isdigit() and len(uadhar) == 12:
                messagebox.showerror("Login", "Enter a valid 12-digit Aadhaar number!")
                return

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select name,email,password from account where acno=? and email=? and adhar=?'
            curobj.execute(query,(uacn,uemail,uadhar))
            row=curobj.fetchone()
            if row==None:
                messagebox.showerror("Password Recovery","Record not found")
                return
            else:
                otp=Generator.generate_otp()
                utext=f'''Dear {row[0]},
            Kindly use otp {otp} to recover password of your account {uacn} in our bank.
            
            Thanks,
            VBA Bank,Noida
            '''
                conobj.close()
            try:
                mailing.send_close_otp(row[1],"otp to recover password",utext)
                messagebox.showinfo("Account","otp has been sent to your mail")
                attmpt=1
                while attmpt<=3:
                    uotp=simpledialog.askstring("OTP","Enter OTP")
                    if str(otp)==uotp:
                        messagebox.showinfo("Password Recovery",row[2])
                        break
                    else:
                        messagebox.showerror("Password Recovery","invalid otp")
                        attmpt+=1
                        if attmpt==4:
                            messagebox.showerror("Password Recovery","max attamptes completed ,you need to resend otp")
            except:
                msg='''Something went wrong
                Kindly check internet connectivity or mail id'''
                messagebox.showerror("Account",msg)


    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.75)  

    btn_back=Button(frm,text='🔙',bg='light blue',width=2,command=call_main_frame,
                       font=('arial',15,'bold'),bd=5)
    btn_back.place(relx=0,rely=0) 

    lbl_acn=Label(frm,text='ACN NO.      :',
                   font=('arial',15,"bold"),bg='white')
    lbl_acn.place(relx=.3,rely=.2)

    e_acn=Entry(frm,font=('arial',15),bd=5,)
    e_acn.place(relx=.4,rely=.2)
    e_acn.focus()

    lbl_email=Label(frm,text='E-MAIL        :',
                   font=('arial',15,"bold"),bg='white')
    lbl_email.place(relx=.3,rely=.3)

    e_email=Entry(frm,font=('arial',15),bd=5,)
    e_email.place(relx=.4,rely=.3)

    lbl_adhar=Label(frm,text= 'ADHAR NO. :',
                   font=('arial',15,"bold"),bg='white')
    lbl_adhar.place(relx=.3,rely=.4)

    e_adhar=Entry(frm,font=('arial',15),bd=5)
    e_adhar.place(relx=.4,rely=.4)

    btn_otp=Button(frm,text='SEND OTP',bg='light blue',command=send_otp,
                       font=('arial',13,'bold'),bd=5)
    btn_otp.place(relx=.4,rely=.5)

    btn_reset=Button(frm,text='Reset',bg='powder blue',command=reset,
                       font=('arial',13,'bold'),bd=5)
    btn_reset.place(relx=.5,rely=.497)

def customer_frame(cust_tup):

    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='pink')
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.75)

    def logout():
        frm.destroy()
        main_frame()


    def view_details():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.3,relwidth=.6,relheight=.55)
        ifrm.configure(bg='white')

        def Exit():
            ifrm.destroy()
            customer_frame(cust_tup)

        lbl_title=Label(ifrm,text='Details Screen:',
                  font=('arial',18,"bold",'underline'),bg='white')
        lbl_title.place(relx=0,rely=0)

        lbl_title=Label(ifrm,text='Details :',
                  font=('arial',15,"bold"),bg='white')
        lbl_title.place(relx=0,rely=.2)


        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from account where acno=?'
        curobj.execute(query,(cust_tup[0],))
        tup=curobj.fetchone()
        conobj.close()

        details=f'''
{'Account no':45}\n
{'Customer Name':50}\n
{'Customer Email':25}\n
{'Customer Mob':20}\n
{'Available Bal':20}\n
{'Customer Adr':20} \n
{'ACN Open Date':20}                                                
'''
        lbl_details=Label(ifrm,text=details,
                        font=('consolas',15,),bg='white',fg='black',justify='left',anchor='w')
        lbl_details.place(relx=.2,rely=.2)

        details_values=f'''
{tup[0]:>25}\n
{tup[1]:>25}\n
{tup[5]:>25}\n
{tup[6]:>25}\n
{tup[7]:>25}\n
{tup[8]:>25}\n
{tup[10]:>25}
'''
        lbl_details_values=Label(ifrm,text=details_values,
                        font=('arial',15,),bg='white',fg='purple',justify='left',anchor="w")
        lbl_details_values.place(relx=.4,rely=.2)

        btn_exit=Button(ifrm,text='Exit',bg='powder blue',command=Exit,
                        font=('arial',10,'bold'),bd=5)
        btn_exit.place(relx=.955,rely=0)

    def edit():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.3,relwidth=.6,relheight=.55)
        ifrm.configure(bg='white')

        def Exit():
            ifrm.destroy()
            customer_frame(cust_tup)

        lbl_title=Label(ifrm,text='This is Edit Details Screen',
                  font=('arial',15,"bold"),bg='white')
        lbl_title.pack()

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from account where acno=?'
        curobj.execute(query,(cust_tup[0],))
        tup=curobj.fetchone()
        conobj.close()

        def edit_db():
            uname=e_name.get()
            uemail=e_email.get()
            umob=e_mob.get()
            uadr=e_adr.get()
            uadhar=e_adhar.get()
            upan=e_pan.get()
            upass=e_pass.get()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='update account set name=?,password=?,adhar=?,mob=?,email=?,pan=?,adr=? where acno=?'

            curobj.execute(query,(uname,upass,uadhar,umob,uemail,upan,uadr,cust_tup[0]))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Edit Details','Details updated successfully')
            
            

        lbl_name=Label(ifrm,text='Name',font=('arial',15),bg='white')
        lbl_name.place(relx=.1,rely=.1)

        e_name=Entry(ifrm,bd=5,font=('arial',15))
        e_name.focus()
        e_name.place(relx=.1,rely=.15)

        lbl_email=Label(ifrm,text='Email',font=('arial',15),bg='white')
        lbl_email.place(relx=.1,rely=.3)

        e_email=Entry(ifrm,bd=5,font=('arial',15))
        e_email.place(relx=.1,rely=.35)

        lbl_mob=Label(ifrm,text='Mob',font=('arial',15),bg='white')
        lbl_mob.place(relx=.1,rely=.5)

        e_mob=Entry(ifrm,bd=5,font=('arial',15))
        e_mob.place(relx=.1,rely=.55)

        lbl_adr=Label(ifrm,text='Adr',font=('arial',15),bg='white')
        lbl_adr.place(relx=.5,rely=.5)

        e_adr=Entry(ifrm,bd=5,font=('arial',15))
        e_adr.place(relx=.5,rely=.55)

        lbl_adhar=Label(ifrm,text='Adhar',font=('arial',15),bg='white')
        lbl_adhar.place(relx=.5,rely=.1)

        e_adhar=Entry(ifrm,bd=5,font=('arial',15))
        e_adhar.place(relx=.5,rely=.15)

        lbl_pan=Label(ifrm,text='PAN',font=('arial',15),bg='white')
        lbl_pan.place(relx=.5,rely=.3)

        e_pan=Entry(ifrm,bd=5,font=('arial',15))
        e_pan.place(relx=.5,rely=.35)

        lbl_pass=Label(ifrm,text='Pass',font=('arial',15),bg='white')
        lbl_pass.place(relx=.1,rely=.7)

        e_pass=Entry(ifrm,bd=5,font=('arial',15))
        e_pass.place(relx=.1,rely=.75)

        e_name.insert(0,tup[1])
        e_email.insert(0,tup[5])
        e_mob.insert(0,tup[6])
        e_pan.insert(0,tup[4])
        e_adhar.insert(0,tup[3])
        e_adr.insert(0,tup[8])
        e_pass.insert(0,tup[2])
        

        
        btn_update=Button(ifrm,bd=5,font=('arial',15),text='update',
                        bg='powder blue',command=edit_db)
        btn_update.place(relx=.5,rely=.75)

        btn_reset=Button(ifrm,bd=5,font=('arial',15),text='Reset',bg='powder blue')
        btn_reset.place(relx=.6,rely=.75)

        btn_exit=Button(ifrm,text='Exit',bg='powder blue',command=Exit,
                        font=('arial',10,'bold'),bd=5)
        btn_exit.place(relx=.955,rely=0)


    def deposit():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.3,relwidth=.6,relheight=.55)
        ifrm.configure(bg='white')

        def Exit():
            ifrm.destroy()
            customer_frame(cust_tup)

        def deposit_db():
            uamt=float(e_amt.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select bal from account where acno=?'
            curobj.execute(query,(cust_tup[0],))
            ubal=curobj.fetchone()[0]
            conobj.close()

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query1='update account set bal=bal+? where acno=?'
            query2='insert into txn_history values(?,?,?,?,?,?)'

            curobj.execute(query1,(uamt,cust_tup[0]))
            curobj.execute(query2,(None,cust_tup[0],uamt,'CR.',
                           ubal+uamt,time.strftime("%d-%m-%Y %r")))
            conobj.commit()
            conobj.close()
            messagebox.showinfo("Deposit",f"""Amount {uamt} deposited,
                                Updated Bal:{ubal+uamt}""")


        lbl_title=Label(ifrm,text='This is deposit screen',
                        font=('arial',20,'bold'),bg='white',fg='purple')
        lbl_title.pack()

        lbl_amt=Label(ifrm,text='Amount',
                        font=('arial',20,'bold'),bg='white',fg='black')
        lbl_amt.place(relx=.28,rely=.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.2)

        btn_deposit=Button(ifrm,bd=5,font=('arial',15),
                           text='deposit',bg='powder blue',command=deposit_db)
        btn_deposit.place(relx=.4,rely=.35)        

        btn_exit=Button(ifrm,text='Exit',bg='powder blue',command=Exit,
                        font=('arial',10,'bold'),bd=5)
        btn_exit.place(relx=.955,rely=0)

    def withdraw():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.3,relwidth=.6,relheight=.55)
        ifrm.configure(bg='white')

        def Exit():
            ifrm.destroy()
            customer_frame(cust_tup)

        lbl_title=Label(ifrm,text='This is Withdraw Amount Screen',
                  font=('arial',15,"bold"),bg='white')
        lbl_title.pack()

        def withdraw_db():
            uamt=float(e_amt.get())
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select bal from account where acno=?'
            curobj.execute(query,(cust_tup[0],))
            ubal=curobj.fetchone()[0]
            conobj.close()
            if ubal>=uamt:

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1='update account set bal=bal-? where acno=?'
                query2='insert into txn_history values(?,?,?,?,?,?)'

                curobj.execute(query1,(uamt,cust_tup[0]))
                curobj.execute(query2,(None,cust_tup[0],uamt,'DB.',
                            ubal-uamt,time.strftime("%d-%m-%Y %r")))
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Withdraw",f"""Amount {uamt} withdrawn,
                                    Updated Bal:{ubal-uamt}""")
            else:
                messagebox.showerror("Withdraw",f"Insufficient Bal:{ubal}")

        lbl_amt=Label(ifrm,text='Amount',
                        font=('arial',20,'bold'),bg='white',fg='black')
        lbl_amt.place(relx=.28,rely=.2)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.2)

        btn_withdraw=Button(ifrm,bd=5,font=('arial',15),
                           text='withdraw',bg='powder blue',command=withdraw_db)
        btn_withdraw.place(relx=.4,rely=.35)

        btn_exit=Button(ifrm,text='Exit',bg='powder blue',command=Exit,
                        font=('arial',10,'bold'),bd=5)
        btn_exit.place(relx=.955,rely=0)


    def transfer():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.3,relwidth=.6,relheight=.55)
        ifrm.configure(bg='white')

        def Exit():
            ifrm.destroy()
            customer_frame(cust_tup)

        lbl_title=Label(ifrm,text='This is Transfer Amount Screen',
                  font=('arial',15,"bold"),bg='white')
        lbl_title.pack()

        def transfer_db():
            toacn=e_to.get()
            uamt=float(e_amt.get())

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from account where acno=?'
            curobj.execute(query,(toacn,))
            to_details=curobj.fetchone()
            conobj.close()
            if to_details==None:
                messagebox.showerror("Transfer",f"To ACN does not exist:{toacn}")
                return
            
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select bal from account where acno=?'
            curobj.execute(query,(cust_tup[0],))
            ubal=curobj.fetchone()[0]
            conobj.close()
            if ubal>=uamt:

                conobj=sqlite3.connect(database='bank.sqlite')
                curobj=conobj.cursor()
                query1='update account set bal=bal-? where acno=?'
                query2='update account set bal=bal+? where acno=?'
                
                query3='insert into txn_history values(?,?,?,?,?,?)'
                query4='insert into txn_history values(?,?,?,?,?,?)'
                

                curobj.execute(query1,(uamt,cust_tup[0]))
                curobj.execute(query2,(uamt,toacn))
                curobj.execute(query3,(None,cust_tup[0],uamt,'DB.',
                            ubal-uamt,time.strftime("%d-%m-%Y %r")))
                curobj.execute(query4,(None,toacn,uamt,'CR.',
                            ubal+uamt,time.strftime("%d-%m-%Y %r")))
                
                conobj.commit()
                conobj.close()
                messagebox.showinfo("Transfer",f"""Amount {uamt} transfered,
                                    Updated Bal:{ubal-uamt}""")
            else:
                messagebox.showerror("Transfer",f"Insufficient Bal:{ubal}")



        lbl_to=Label(ifrm,text='To ACN',
                        font=('arial',20,'bold'),bg='white',fg='black')
        lbl_to.place(relx=.28,rely=.2)

        e_to=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_to.place(relx=.4,rely=.2)

        lbl_amt=Label(ifrm,text='Amount',
                        font=('arial',20,'bold'),bg='white',fg='black')
        lbl_amt.place(relx=.28,rely=.3)

        e_amt=Entry(ifrm,font=('arial',20,'bold'),bd=5)
        e_amt.place(relx=.4,rely=.3)

        btn_transfer=Button(ifrm,bd=5,font=('arial',15),
                           text='transfer',bg='powder blue',command=transfer_db)
        btn_transfer.place(relx=.4,rely=.45)

        btn_exit=Button(ifrm,text='Exit',bg='powder blue',command=Exit,
                        font=('arial',10,'bold'),bd=5)
        btn_exit.place(relx=.955,rely=0)

    def history():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.3,relwidth=.6,relheight=.55)
        ifrm.configure(bg='white')

        def Exit():
            ifrm.destroy()
            customer_frame(cust_tup)

        def open_calendar():
            top = Toplevel(ifrm)
            top.title("Select Date")
            top.geometry("250x240+700+600")
            top.grab_set()  # Make the calendar modal (blocks other windows)
            
            # Create a Calendar widget
            cal = Calendar(top, selectmode='day', year=date.today().year,
                            month=date.today().month, day=date.today().day,
                            date_pattern='dd-mm-yyyy')
            cal.pack(pady=10)
            
            # Function to get the selected date
            def pick_date():
                selected = cal.get_date()
                # e_dob.delete(0, "end")
                # e_dob.insert(0, selected)
                top.destroy()
            
                Button(top, text="Select", command=pick_date).pack(pady=5)

            btn = Button(ifrm, text="📅", command=open_calendar)
            btn.place(relx=.755,rely=.58)

        def credit():
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from txn_history where acno=? and lower(type)="cr."'
            curobj.execute(query,(cust_tup[0],))
            txn_data=curobj.fetchall()
            conobj.close()

            tv=Treeview(ifrm)
            tv.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)

            style = Style()
            style.configure("Treeview.Heading", font=('Arial',15,'bold'),foreground='black')


            sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
            sb.place(relx=.9,rely=.2,relheight=.7)
            tv.configure(yscrollcommand=sb.set)


            tv['columns']=('txn date','txn amount','txn type','updated bal')
            tv.column('txn date',width=250,anchor='c')
            tv.column('txn amount',width=150,anchor='c')
            tv.column('txn type',width=150,anchor='c')
            tv.column('updated bal',width=150,anchor='c')

            tv.heading('txn date',text='txn date')
            tv.heading('txn amount',text='txn amount')
            tv.heading('txn type',text='txn type')
            tv.heading('updated bal',text='updated bal')   

            tv['show']='headings'

            for row in txn_data:
                tv.insert("","end",values=(row[5],row[2],row[3],row[4]))
                tv.insert("","end",values=('','','',''))

        def debit():
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from txn_history where acno=? and lower(type)="db."'
            curobj.execute(query,(cust_tup[0],))
            txn_data=curobj.fetchall()
            conobj.close()

            tv=Treeview(ifrm)
            tv.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)

            style = Style()
            style.configure("Treeview.Heading", font=('Arial',15,'bold'),foreground='black')


            sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
            sb.place(relx=.9,rely=.2,relheight=.7)
            tv.configure(yscrollcommand=sb.set)


            tv['columns']=('txn date','txn amount','txn type','updated bal')
            tv.column('txn date',width=250,anchor='c')
            tv.column('txn amount',width=150,anchor='c')
            tv.column('txn type',width=150,anchor='c')
            tv.column('updated bal',width=150,anchor='c')

            tv.heading('txn date',text='txn date')
            tv.heading('txn amount',text='txn amount')
            tv.heading('txn type',text='txn type')
            tv.heading('updated bal',text='updated bal')   

            tv['show']='headings'

            for row in txn_data:
                tv.insert("","end",values=(row[5],row[2],row[3],row[4]))
                tv.insert("","end",values=('','','',''))
            
            

        lbl_title=Label(ifrm,text='History Screen :',
                  font=('arial',15,"bold","underline"),bg='white')
        lbl_title.place(relx=0,rely=0)

        conobj=sqlite3.connect(database='bank.sqlite')
        curobj=conobj.cursor()
        query='select * from txn_history where acno=?'
        curobj.execute(query,(cust_tup[0],))
        txn_data=curobj.fetchall()
        conobj.close()
        

        tv=Treeview(ifrm)
        tv.place(relx=.1,rely=.2,relwidth=.8,relheight=.7)


        style = Style()
        style.configure("Treeview.Heading", font=('Arial',15,"italic"),foreground='black')


        sb=Scrollbar(ifrm,orient='vertical',command=tv.yview)
        sb.place(relx=.9,rely=.2,relheight=.7)
        tv.configure(yscrollcommand=sb.set)


        tv['columns']=('txn date','txn amount','txn type','updated bal')
        tv.column('txn date',width=250,anchor='c')
        tv.column('txn amount',width=150,anchor='c')
        tv.column('txn type',width=150,anchor='c')
        tv.column('updated bal',width=150,anchor='c')

        tv.heading('txn date',text='txn date')
        tv.heading('txn amount',text='txn amount')
        tv.heading('txn type',text='txn type')
        tv.heading('updated bal',text='updated bal')   

        tv['show']='headings'

        for row in txn_data:
            tv.insert("","end",values=(row[5],row[2],row[3],row[4]))
            tv.insert("","end",values=('','','',''))
        
        btn_exit=Button(ifrm,text='Exit',bg='powder blue',command=Exit,
                        font=('arial',10,'bold'),bd=5)
        btn_exit.place(relx=.955,rely=0)

        btn_cr=Button(ifrm,text='Credit Bal.',bg='light green',command=credit,
                        font=('arial',8,'bold'),bd=5)
        btn_cr.place(relx=.1,rely=.125)

        btn_db=Button(ifrm,text='Debit Bal.',bg='red',command=debit,
                        font=('arial',8,'bold'),bd=5)
        btn_db.place(relx=.83,rely=.125)

    def update_pic():
        filepath=filedialog.askopenfile()
        shutil.copy(filepath,f'{cust_tup[0]}.jpg')

        img_profile=Image.open(f'{cust_tup[0]}.jpg').resize((170,150))
        img_profilepil=ImageTk.PhotoImage(img_profile,master=root)
        lbl_profilepic=Label(frm,image=img_profilepil)
        lbl_profilepic.image=img_profilepil
        lbl_profilepic.place(relx=0,rely=.1)
            

    lbl_wel=Label(frm,text=f' Welcome,{cust_tup[1]}',
                  font=('arial',20,"bold"),bg='pink',fg='red')
    lbl_wel.place(relx=0,rely=0)

    btn_logout=Button(frm,text='Logout',bg='white',
                       font=('arial',15,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.946,rely=0)

    if os.path.exists(f'{cust_tup[0]}.jpg'):
        img_profile=Image.open(f'{cust_tup[0]}.jpg').resize((170,150))
    else:
        img_profile=Image.open('default.jpg').resize((170,150))
    img_profilepil=ImageTk.PhotoImage(img_profile,master=root)
    lbl_profilepic=Label(frm,image=img_profilepil)
    lbl_profilepic.image=img_profilepil
    lbl_profilepic.place(relx=0,rely=.1)

    btn_update=Button(frm,text='🔄',bg='white',command=update_pic,
                       font=('arial',10,'bold'),bd=5)
    btn_update.place(relx=.12,rely=.29)

    btn_details=Button(frm,text='View Details',bg='white',command=view_details,
                       font=('arial',10,'bold'),bd=5,width=16)
    btn_details.place(relx=0,rely=.4)

    btn_edit=Button(frm,text='Edit Details',bg='white',command=edit,
                       font=('arial',10,'bold'),bd=5,width=16)
    btn_edit.place(relx=0,rely=.5)

    btn_deposit=Button(frm,text='Deposit AMT.',bg='white',command=deposit,
                       font=('arial',10,'bold'),bd=5,width=16)
    btn_deposit.place(relx=0,rely=.6)

    btn_withdraw=Button(frm,text='Withdraw AMT.',bg='white',command=withdraw,
                       font=('arial',10,'bold'),bd=5,width=16)
    btn_withdraw.place(relx=0,rely=.7)

    btn_transfer=Button(frm,text='Transfer AMT.',bg='white',command=transfer,
                       font=('arial',10,'bold'),bd=5,width=16)
    btn_transfer.place(relx=0,rely=.8)

    btn_history=Button(frm,text='View History',bg='white',command=history,
                       font=('arial',10,'bold'),bd=5,width=16)
    btn_history.place(relx=0,rely=.9)

def admin_frame():
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.75)

    def logout():
        frm.destroy()
        main_frame()

    def open():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.35,relwidth=.6,relheight=.55)
        ifrm.configure(bg='light blue')
  
        def save():
            uname=e_name.get()
            uemail=e_email.get()
            umob=e_mob.get()
            uadr=e_adr.get()
            uadhar=e_adhar.get()
            upan=e_pan.get()
            udob=e_dob.get()
            ubal=0
            upass=Generator.generate_passward()
            uopendate=time.strftime("%d-%b-%Y %r")

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='insert into account values(?,?,?,?,?,?,?,?,?,?,?)'
            curobj.execute(query,(None,uname,upass,uadhar,upan,uemail,umob,ubal,uadr,udob,uopendate))
            conobj.commit()
            conobj.close()
            messagebox.showinfo('Account','Account opened successfully')
            e_name.delete(0,"end")
            e_name.focus()
            
            e_email.delete(0,"end")
            e_mob.delete(0,"end")
            e_pan.delete(0,"end")
            e_adhar.delete(0,"end")
            e_adr.delete(0,"end")
            e_dob.delete(0,"end")

            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select max(acno) from account'
            curobj.execute(query)
            uacn=curobj.fetchone()[0]
            usub="Account Opened in VBA Bank"
            utext=f'''Dear {uname},
            We have successfully opened your account in our bank.
            Your ACN={uacn}
            Your Pass={upass}

            Thanks,
            VBA Bank,Noida
            '''
            try:
                mailing.send_acn_cred(uemail,usub,utext)
                messagebox.showinfo("Account","Credential has been sent to your mail")
            except Exception as exp:
                msg='''Something went wrong
                Kindly check internet connectivity or mail id'''
                messagebox.showerror("Account",exp)
            
        lbl_title=Label(ifrm,text='This Open Account Screen',
                  font=('arial',15,"bold"),bg='white')
        lbl_title.pack()

        lbl_name=Label(ifrm,text='Name :',font=('arial',15,'bold'),
                       bg='white')
        lbl_name.place(relx=.1,rely=.1)

        e_name=Entry(ifrm,bd=5,font=('arial',15))
        e_name.place(relx=.1,rely=.17)
        e_name.focus()

        lbl_email=Label(ifrm,text='Email :',font=('arial',15,'bold'),bg='white')
        lbl_email.place(relx=.1,rely=.3)

        e_email=Entry(ifrm,bd=5,font=('arial',15))
        e_email.place(relx=.1,rely=.37)

        lbl_mob=Label(ifrm,text='Mobile :',font=('arial',15,'bold'),bg='white')
        lbl_mob.place(relx=.1,rely=.5)

        e_mob=Entry(ifrm,bd=5,font=('arial',15))
        e_mob.place(relx=.1,rely=.57)

        lbl_adr=Label(ifrm,text='Address :',font=('arial',15,'bold'),bg='white')
        lbl_adr.place(relx=.1,rely=.7)

        e_adr=Entry(ifrm,bd=5,font=('arial',15))
        e_adr.place(relx=.1,rely=.77)

        lbl_adhar=Label(ifrm,text='Adhar NO. :',font=('arial',15,'bold'),bg='white')
        lbl_adhar.place(relx=.5,rely=.1)

        e_adhar=Entry(ifrm,bd=5,font=('arial',15))
        e_adhar.place(relx=.5,rely=.17)

        lbl_pan=Label(ifrm,text='PAN NO. :',font=('arial',15,'bold'),bg='white')
        lbl_pan.place(relx=.5,rely=.3)

        e_pan=Entry(ifrm,bd=5,font=('arial',15))
        e_pan.place(relx=.5,rely=.37)

        lbl_dob=Label(ifrm,text='DOB :',font=('arial',15,'bold'),bg='white')
        lbl_dob.place(relx=.5,rely=.5)

        e_dob=Entry(ifrm,bd=5,font=('arial',15))
        e_dob.place(relx=.5,rely=.57)
        
        def open_calendar():
            top = Toplevel(ifrm)
            top.title("Select Date")
            top.geometry("250x240+700+600")
            top.grab_set()  # Make the calendar modal (blocks other windows)
            
            # Create a Calendar widget
            cal = Calendar(top, selectmode='day', year=date.today().year,
                            month=date.today().month, day=date.today().day,
                            date_pattern='dd-mm-yyyy')
            cal.pack(pady=10)
            
            # Function to get the selected date
            def pick_date():
                selected = cal.get_date()
                e_dob.delete(0, "end")
                e_dob.insert(0, selected)
                top.destroy()
            
            Button(top, text="Select", command=pick_date).pack(pady=5)

        btn = Button(ifrm, text="📅", command=open_calendar)
        btn.place(relx=.755,rely=.58)

        btn_save=Button(ifrm,bd=5,font=('arial',15),text='Save',bg='powder blue',command=save)
        btn_save.place(relx=.5,rely=.7)

        btn_reset=Button(ifrm,bd=5,font=('arial',15),text='Reset',bg='powder blue')
        btn_reset.place(relx=.6,rely=.7)



    def close():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.35,relwidth=.6,relheight=.55)
        ifrm.configure(bg='white')

        def send_otp():
            uacn=e_acn.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select name,email,password from account where acno=?'
            curobj.execute(query,(uacn,))
            row=curobj.fetchone()
            if row==None:
                messagebox.showerror("View","Record not found")
            else:
                otp=Generator.generate_otp()
                utext=f'''Dear {row[0]},
            Kindly share otp {otp} with bank to close your account in our bank.
            
            Thanks,
            VBA Bank,Noida
            '''
                conobj.close()
            try:
                mailing.send_close_otp(row[1],"otp to close account",utext)
                messagebox.showinfo("Account","otp has been sent to customer mail")
                attmpt=1
                while attmpt<=3:
                    uotp=simpledialog.askstring("OTP","Enter OTP")
                    if str(otp)==uotp:
                        conobj=sqlite3.connect(database='bank.sqlite')
                        curobj=conobj.cursor()
                        query="delete from account where acno=?"
                        curobj.execute(query,(uacn,))
                        conobj.commit()
                        conobj.close()
                        messagebox.showinfo("close","Account closed!")
                        break
                    else:
                        messagebox.showerror("close","invalid otp")
                        attmpt+=1
                        if attmpt==4:
                            messagebox.showerror("close","max attamptes completed ,you need to resend otp")
            except:
                msg='''Something went wrong
                Kindly check internet connectivity or mail id'''
                messagebox.showerror("Account",msg)
            


        lbl_title=Label(ifrm,text='This Close Account Screen',
                  font=('arial',15,"bold"),bg='white')
        lbl_title.pack()

        lbl_acn=Label(ifrm,text='ACN :',
                  font=('arial',15,"bold"),bg='white')
        lbl_acn.place(relx=.3,rely=.2)

        e_acn=Entry(ifrm,bd=5,font=('arial',15))
        e_acn.place(relx=.4,rely=.2)

        btn_otp=Button(ifrm,text='Send OTP',bg='light blue',command=send_otp,
                    font=('arial',15,'bold'),bd=5,)
        btn_otp.place(relx=.45,rely=.3)


    def view():
        ifrm=Frame(root,highlightbackground='black',highlightthickness=2)
        ifrm.place(relx=.2,rely=.35,relwidth=.6,relheight=.55)
        ifrm.configure(bg='white')

        def view_customer():
            uacn=e_acn.get()
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from account where acno=?'
            curobj.execute(query,(uacn,))
            row=curobj.fetchone()
            if row==None:
                messagebox.showerror("View","Record not found")
            else:
                msg=f'''
            {'Name':15}{row[1]}
            {'Bal':15}{row[7]}
            {'Mob':15}{row[6]}
            {'Email':15}{row[5]}
            {'Open date':15}{row[10]}
            {'Adhar':15}{row[3]}
                '''
                messagebox.showinfo("View",msg)
            conobj.close()

        lbl_title=Label(ifrm,text='This View Account Screen',
                  font=('arial',15,"bold"),bg='white')
        lbl_title.pack()

        lbl_acn=Label(ifrm,text='ACN :',
                  font=('arial',15,"bold"),bg='white')
        lbl_acn.place(relx=.3,rely=.2)

        e_acn=Entry(ifrm,bd=5,font=('arial',15))
        e_acn.place(relx=.4,rely=.2)

        btn_view=Button(ifrm,text='VIEW',bg='light blue',command=view_customer,
                    font=('arial',10,'bold'),bd=5,)
        btn_view.place(relx=.66,rely=.195)


    lbl_admin=Label(frm,text=' Welcome Admin ',
                  font=('arial',20,"bold"),bg='white')
    lbl_admin.place(relx=0,rely=0)

    btn_logout=Button(frm,text='Logout',bg='white',
                       font=('arial',15,'bold'),bd=5,command=logout)
    btn_logout.place(relx=.946,rely=0)

    btn_open=Button(frm,text='Open Account',bg='white',command=open,
                    font=('arial',15,'bold'),bd=5,fg='black')
    btn_open.place(relx=.25,rely=.1)

    btn_close=Button(frm,text='Close Account',bg='white',command=close,
                    font=('arial',15,'bold'),bd=5,fg='black')
    btn_close.place(relx=.45,rely=.1)

    btn_view=Button(frm,text='View Account',bg='white',command=view,
                    font=('arial',15,'bold'),bd=5,fg='black')
    btn_view.place(relx=.65,rely=.1)


# to make center window work
def main_frame():
    #command of captcha
    def refresh_captcha():
        nonlocal gen_captcha
        gen_captcha=Generator.generate_captcha()
        lbl_captcha.configure(text=gen_captcha)
    
    def call_fp_frame():
        frm.destroy()
        fp_frame()
    
    def reset():
        e_acn.delete(0,'end')
        e_acn.focus()
        e_pass.delete(0,'end')
        e_user_captcha.delete(0,'end')


    def login():
        utype=cb_user.get()
        uacn=e_acn.get().strip()
        upass=e_pass.get().strip()
        ucaptcha=e_user_captcha.get().strip()

        if len(uacn)==0:
            messagebox.showerror("Login","ACN can't be empty")
            return
        
        if len(upass)==0:
            messagebox.showerror("Login","Pass can't be empty")
            return
        
        if ucaptcha!=gen_captcha.replace(' ',''):
            messagebox.showerror("Login","Invalid captcha")
            return 
        
        if  not uacn.isdigit():
            messagebox.showerror("Login","Account Number Should Be In Digit")
            return   
        
        if len(upass)<=8:
            messagebox.showerror('login','Password must be greater than 8 characters!')
            return                                    

        if utype=='Admin' and uacn=='0' and upass=='Admin_pass':
            frm.destroy()
            admin_frame()
        elif utype=='Customer':
            conobj=sqlite3.connect(database='bank.sqlite')
            curobj=conobj.cursor()
            query='select * from account where acno=? and password=?'
            curobj.execute(query,(uacn,upass))
            tup=curobj.fetchone()
            conobj.close()
            if tup==None:
                messagebox.showerror('Login','Invalid ACN/Pass')
            else:
                frm.destroy()
                customer_frame(tup)
        else:
            messagebox.showerror('ERROR','Invalid User Type')
            
    frm=Frame(root,highlightbackground='black',highlightthickness=2)
    frm.configure(bg='white')
    frm.place(relx=0,rely=.18,relwidth=1,relheight=.75)


    lbl_acn=Label(frm,text='ACCOUNT NUMBER  :',
                  font=('arial',15,"bold"),bg='white')
    lbl_acn.place(relx=.25,rely=.1)

    e_acn=Entry(frm,font=('arial',15),bd=5)
    e_acn.place(relx=.4,rely=.1)
    e_acn.focus()

    lbl_pass=Label(frm,text='PASSWORD       :',
                   font=('arial',15,"bold"),bg='white')
    lbl_pass.place(relx=.28,rely=.2)

    e_pass=Entry(frm,font=('arial',15),bd=5,show='*')
    e_pass.place(relx=.4,rely=.2)

    lbl_user=Label(frm,text='USER            : ',
                   font=('arial',15,"bold"),bg='white')
    lbl_user.place(relx=.3,rely=.3)

    #its use for change user help from combobox
    cb_user=Combobox(frm,values=('Customer','Admin'),font=('arial',15))
    cb_user.current(0)
    cb_user.place(relx=.4,rely=.3)

    # genterate captcha code
    gen_captcha=Generator.generate_captcha()
    lbl_captcha=Label(frm,text=gen_captcha,width=15,
                      font=('Times New Roman',15,"bold"),bg='light blue')
    lbl_captcha.place(relx=.4,rely=.4)

    lbl_user_captcha=Label(frm,text='CAPTCHA        : ',  
                   font=('arial',15,"bold"),bg='white')
    lbl_user_captcha.place(relx=.285,rely=.5)

    e_user_captcha=Entry(frm,font=('arial',15),bd=5)
    e_user_captcha.place(relx=.4,rely=.5)

    #button of refresh 
    btn_refresh=Button(frm,text='🔄',bg='white',
                       font=('arial',13,'bold'),command=refresh_captcha)
    btn_refresh.place(relx=.53,rely=.395)

    #button of login,reset,forget
    btn_login=Button(frm,text='Login',bg='light blue',
                       font=('arial',13,'bold'),bd=5,command=login)
    btn_login.place(relx=.41,rely=.6)

    btn_reset=Button(frm,text='Reset',bg='light blue',command=reset,
                       font=('arial',13,'bold'),bd=5)
    btn_reset.place(relx=.50,rely=.6)

    btn_fp=Button(frm,text='Forget Passward',bg='light blue',command=call_fp_frame,
                       font=('arial',13,'bold'),bd=5,width=20)
    btn_fp.place(relx=.405,rely=.7)

#making title
lbl_title=Label(root,text='Banking Automation',
                font=('Comic Sans MS',50,'bold','italic','underline'),bg='light blue')
lbl_title.pack()

lbl_dt=Label(root,text='',
             font=('arial',15,'bold','italic'),bg='light blue',fg='green')
lbl_dt.pack()

#call update time function
update_time()

# set image at corner
img=Image.open('logo.jpg').resize((300,150))
img_pil=ImageTk.PhotoImage(img,master=root)
lbl_logo=Label(root,image=img_pil)
lbl_logo.place(x=0,y=0)

#call update logo function
update_logo()

img1=Image.open('VBA.png').resize((300,150))
img_pil1=ImageTk.PhotoImage(img1,master=root)
lbl_logo1=Label(root,image=img_pil1)
lbl_logo1.place(relx=.8,rely=0)

# make for footer
lbl_footer=Label(root,text='Developed by: VK\nCONTACT📞:95684524XX',
                 font=('arial',15 ,'bold'),bg='light blue')
lbl_footer.pack(side='bottom')

#call main_frame function
main_frame()

#show window
root.mainloop()

