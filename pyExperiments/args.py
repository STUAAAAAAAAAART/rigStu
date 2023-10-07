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

#