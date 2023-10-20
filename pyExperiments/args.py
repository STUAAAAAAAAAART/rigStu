# cursed argument passthrough in python

def fn1(a,b):
	print("a=",a)
	print("b=",b)

def fn2arg(*args):
	fn1(*args)

fn2arg(99,44)


def fn2kw(**kwargs):
	fn1(**kwargs)

fn2kw(b=99,a=44)


def fn2(*args,**kwargs):
	fn1(*args,**kwargs)

fn2(99,44)
fn2(b=99,a=44)

# cursed function dictionary
	# goal: make a file parser to then read and execute commands
def fnA():
	print("HELLO FN A!")
fnA() # >> "HELLO FN A!"

fnB = fnA
fnB() # >> "HELLO FN A!"

fnDict = {
	"fnKey": fnA
}

fnDict["fnKey"]()  # >> "HELLO FN A!"

# unpacking lists to arguments
# https://stackoverflow.com/questions/3480184/pass-a-list-to-a-function-to-act-as-multiple-arguments
# https://note.nkmk.me/en/python-argument-expand/#with-variable-length-arguments-kwargs

inList = [5,6,7,8]
def fnUnpack(*args):
	print(args)

fnUnpack(inList) #, vs
fnUnpack(*inList)