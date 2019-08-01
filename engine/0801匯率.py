import twder

def currencySearch(search)
	dollarTupe = twder.now(search)
	reply = '{}\n{} 的即期賣出價: {}'.format(dollarTuple[0],search,dollarTupe[4])
	return reply