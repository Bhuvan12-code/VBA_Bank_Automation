import yagmail

email='bhuvank0412@yagmail.com'
pwd="gryd iuof xekm guzn"

def send_acn_cred(uemail,usub,utext):
    con=yagmail.yagmail(email,pwd)
    msg=yagmail.Message(to=uemail,subject=usub,text=utext)
    con.send(msg)

def send_close_otp(uemail,usub,utext):
    con=yagmail.yagmail(email,pwd)
    msg=yagmail.Message(to=uemail,subject=usub,text=utext)
    con.send(msg)

