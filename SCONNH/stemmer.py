import re


def stemword(word):
		x = re.findall(r'^((.*?)(लाई|ले|लागि|बाट|देखि|को|की|का|मा|माथि|कै|हरु|हरू|मै|न्ने|सँग|वटा))$', word)
		if x:
			y = re.findall(r'^((.*?)(लाई|ले|लागि|बाट|देखि|को|की|का|मा|माथि|कै|हरु|हरू|मै|न्ने|सँग|वटा))$', x[0][1])
			if y:
				return y[0][1]
			else:
				return x[0][1]
		elif word.replace("'","").replace(" ",'').strip():
			return word.replace("'","").replace(" ",'').strip()
		else:
			return None
