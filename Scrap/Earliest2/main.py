


MAX_END_TIME = 9999999999999999999999999999




class Time:
	def __init__(self, jobNum, taskLen):
		self.jobNum = jobNum
		self.taskLen = taskLen
		self.slack = 0

	def getSlack(self):
		return self.slack

	def getJobNum(self):
		return self.jobNum

	def getTaskLen(self):
		return self.taskLen

	def setSlack(self,slack):
		self.slack = slack
	

#input: the job endtime, job number and capacity schedule
# takes any jobs with same job number ans job end time and readjusts based on new job end time
def changeSlackTimes(jobEndTime, jobNumber, CapacitySchedule):
	
	for i in range(len(CapacitySchedule)):

		if (CapacitySchedule[i].jobNum == jobNumber):
			currentTaskEndTime = CapacitySchedule[i].taskLen + i 
			slack = jobEndTime - currentTaskEndTime

			CapacitySchedule[i].setSlack(slack)


#potentially need to add the EndTimes vector to this as well
#(call getJobCurrentEndTime(1,CapacitySchedule) to initialize)
def addInitialJob(jobs, CapacitySchedule, jobEndTimes):
	
	for i in range(len(jobs[0])):

		time = Time(1, jobs[0][i])

		if (i == 0):
			jobEndTimes.append(jobs[0][i])

			time.setSlack(0)
			CapacitySchedule.append(time)
			continue

		#slack times of all other tasks in this job must change
		if (i + jobs[0][i] > jobEndTimes[0]):
			jobEndTimes[0] = i + jobs[0][i]
			time.setSlack(0)
			CapacitySchedule.append(time)
			changeSlackTimes(jobEndTimes[0], 1, CapacitySchedule)

		#slack times of all other tasks in this job don't change
		else:

			time.setSlack(jobEndTimes[0] - i - jobs[0][i])
			CapacitySchedule.append(time)

	curJobEnd = getJobCurrentEndTime(1, CapacitySchedule)
	


#when adding a task, slack values to the right get moved down by one
#if slack goes below 0 (ie -1), then the job's finish time changes by 1
#thus, all other tasks in the job's slack values must also increase by 1
def increaseSlackForJob(jobNum, CapacitySchedule):
	#print("not yet implemented yet")

	for i in range(len(CapacitySchedule)):
		if (CapacitySchedule[i].getJobNum() == jobNum):

			currentSlack = CapacitySchedule[i].getSlack()
			CapacitySchedule[i].setSlack(currentSlack + 1)



#this function will be used to add a task to the specified potential spot
#this will be used by a function that iterates through the positions in the capacity schedule
#(to determine the optimal placement for the task currently being assessed)
#if certain slack values go below 0, increase job finish time by 1 and also all slack values by 1 (making -1 slack values equal 0)
def addTask(index, CapacitySchedule, jobNum, taskLen, EndTimes):

	time = Time(jobNum, taskLen)
	
	if (jobNum > len(EndTimes)):
		EndTimes.append(index + taskLen)

	#make a slack assessment for this job
	CapacitySchedule.insert(index, time)
	
	#make a slack assessment for the jobs that come after it
	for i in range(len(CapacitySchedule)):
		if (i < index):
			continue

		currentSlack = CapacitySchedule[i].getSlack()
		CapacitySchedule[i].setSlack(currentSlack - 1)

	#adjust any values of slack that went below 0
	for i in range(len(CapacitySchedule)):
		if (i < index):
			continue

		if (CapacitySchedule[i].getSlack() < 0):
			currentJob = CapacitySchedule[i].getJobNum()

			EndTimes[currentJob-1] = EndTimes[currentJob-1] + 1

			#changeSlackTimes()
			#def changeSlackTimes(jobEndTime, jobNumber, CapacitySchedule):
			
			changeSlackTimes(EndTimes[currentJob-1], currentJob, CapacitySchedule)


	#this is just insurance (likely unnecessary)
	for i in range(len(EndTimes)):

		changeSlackTimes(EndTimes[i], i+1, CapacitySchedule)

	#need to alter EndTimes and make sure slack values are at appropriate levels




#based on the EndTimesVector, calculates the total number of endTimes in order
#to be assessed with minimzation function specified in "tryTaskSpots()"
def totalEndTimes(EndTimes):
	sum = 0
	for i in range(len(EndTimes)):
		sum = sum + EndTimes[i]

	return sum


#for the given job number, output the current endTime 
def getJobCurrentEndTime(jobNum, CapacitySchedule):

	maximum = 0
	for i in range(len(CapacitySchedule)):

		if (CapacitySchedule[i].jobNum == jobNum):

			if (CapacitySchedule[i].taskLen + i > maximum):
				maximum = CapacitySchedule[i].taskLen + i
				

	return maximum


#take a job number and task length and find best place to put it
def addEndTime(EndTimes, newEndTime):
	print("not implemented yet")


def tryTaskSpots(jobNum, taskLen, CapacitySchedule, EndTimes):

	#save previous value of Capacity Schedule and EndTimes
	oldCap = CapacitySchedule.copy()
	oldEnd = EndTimes.copy()
	curMinEndTimes = MAX_END_TIME

	newCapacitySchedule = []
	newEndTimes = []



	##THIS ASSUMES THAT THE JOB BEING ADDED IS EXACTLY 1 MORE THAN THE LARGEST ALREADY (MIGHT NEED TO CHANGE FOR MORE ROBUSTNESS)
	
	if (jobNum > len(EndTimes)):

		EndTimes.append(taskLen+len(CapacitySchedule)-1)


	for i in reversed(range(len(CapacitySchedule))):
		newEndTimes = []
		addTask(i,CapacitySchedule,jobNum,taskLen,EndTimes)

		#recalculate end times for the job
		for j in range(len(EndTimes)):

			EndTimes[j] = getJobCurrentEndTime(j+1, CapacitySchedule)
			newEndTimes.append(EndTimes[j])

		sumEndTimes = totalEndTimes(EndTimes)


		print("sum end times: " + str(sumEndTimes) + " ,  " + " cur Min end times: " + str(curMinEndTimes))

		#print("New sum End Times: " + str(sumEndTimes) + ", Old: " + str(curMinEndTimes))
		if (sumEndTimes < curMinEndTimes):
			print("Iteration that endtimes changes: " + str(i))
			curMinEndTimes = sumEndTimes
			newCapacitySchedule = CapacitySchedule
			newEndTimes = EndTimes

		EndTimes = oldEnd.copy()
		CapacitySchedule = oldCap.copy()

	return newCapacitySchedule, newEndTimes



#Iterate through the capacity schedule and print out what job number, task length and associated slack value
def printSlackValues(CapacitySchedule):
	print()
	for i in range(len(CapacitySchedule)):

		print("t=" + str(i) + ": job num: " + str(CapacitySchedule[i].jobNum) + ", task len: " + str(CapacitySchedule[i].taskLen) +  ", slack: " + str(CapacitySchedule[i].slack))


#Iterate through the EndTimes vector and print out values with the job numbers
def printEndTimes(EndTimes):

	print("End Times:")
	for i in range(len(EndTimes)):
		print("Job " + str(i+1) +": " + str(EndTimes[i]))

if __name__ == "__main__":
	
	
	job1 = [10,9,7,6,5]
	job2 = [10,8,6,4,2]

	jobs = []

	jobs.append(job1)
	jobs.append(job2)

	CapacitySchedule = []

	EndTimes = []

	#assign the initial jobs and give them slack values
	addInitialJob(jobs,CapacitySchedule, EndTimes)

	#display the job number, task length and slack for each task in capacity schedule

	printSlackValues(CapacitySchedule)
	printEndTimes(EndTimes)


	#def addTask(index, CapacitySchedule, jobNum, taskLen, EndTimes):
	
	newCapacitySchedule = []
	newEndTimes = []
	newCapacitySchedule, newEndTimes = tryTaskSpots(2,10,CapacitySchedule,EndTimes)


	for i in range(len(newEndTimes)):
		newEndTimes[i] = getJobCurrentEndTime(i+1, newCapacitySchedule)

	printSlackValues(CapacitySchedule)
	printEndTimes(newEndTimes)



	"""
	Problem: just noticed the slack calculation is off

	The end time is off

	The placement of the job is off

	"""