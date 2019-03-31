def prob_enough_fbd(fbd_min):
	if fbd_min <= 0.5:
		return 0.99
	elif fbd_min <= 1:
		return 0.95
	elif fbd_min <= 2:
		return 0.85
	elif fbd_min <= 4:
		return 0.7
	elif fbd_min <= 6:
		return 0.5
	elif fbd_min <= 8:
		return 0.25
	else:
		return 0.01


fbd = 0.5

print(prob_enough_fbd(0.5))
