import random
random.seed()
ans=[random.randint(1,6) for item in range(4)]

print("guess a sequence 4 values from 1-6")
print("\u25CB = one element is in the code but in the wrong place")
print("\u25CF = one element is in the code and in the correct place")
turn=0
while True:
	guess=[]
	while len(guess) !=4:
			guess=list(input("/nguess a sequence 4 values from 1-6:"))
			guess = [x for x in guess if int(x) in range(1,7)]
	
	print("result:", end="")

	#guess_list=list(map(int,str(guess)))
	result=[]
	ans_temp=ans[:]
	guess_list_temp=guess[:]
	turn+=1
	for i in range(4):
		if ans_temp[i]==guess_list_temp[i]:
			ans_temp[i]="a"
			guess_list_temp[i]="b"
			result.append("\u25CF")
	for i in range(4):
		for j in range(4):
			if ans_temp[i]==guess_list_temp[j] and i!=j:
				guess_list_temp[j]="b"
				result.append("\u25CB")
				break
	print("Guess %d of 12: %d" % (turn, guess))
	print(result)
	if guess==ans:
		print("Correct - you win!")
		break
	if turn>=12:
		print("sorry the code was %d"%(ans))
		break



