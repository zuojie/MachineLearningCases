slots = []
for i in range(10): slots += [i]
print slots
for i in range(10):
	print slots[0]
	del slots[0]
print slots
