MAX_LEN_CAP_SCHEDULE = 1000
INITIAL_MIN_SLACK = 99999

class Task:

	def __init__(self, jobNum, taskLen, slack):
		self.jobNum = jobNum
		self.taskLen = taskLen
		self.slack = slack

	def getSlack(self):
		return self.slack
	def setSlack(self, slack):
		self.slack = slack

	def getJobNum(self):
		return self.jobNum

	def getTaskLen(self):
		return self.taskLen


#object type for the capacity schedule.  Tells whether it is an assigned timeslot
#if it is an assigned time slot, then points to task object
class TimeSlot:
	def __init__(self):
		self.assigned = False
		self.task = 0

	def assign(self, task):
		self.assigned = True
		self.task = task

#assign the first job using the capacity schedule 
def assignInitialJob(CapSched, jobs):

	initialJob = jobs[0]

	initialTaskLen = initialJob[0]

	firstAssignment = Task(1, initialTaskLen, 0)
	CapSched[0].assign(firstAssignment)

	for i in range(len(initialJob)):
		if i == 0:
			continue
		currentTaskLen = initialJob[i]

		assignTask(CapSched, currentTaskLen, 1)

	return CapSched
		
#call assignTask() for jobs 2 to n
def assignRestOfJobs(CapSched, jobs):

	for i in range(len(jobs)):
		curJob = jobs[i]
		if (i == 0):
			continue

		for j in range(len(curJob)):
			curTaskLen = curJob[j]
			CapSched = assignTask(CapSched, curTaskLen, i + 1)

	return CapSched

#Given a capacity schedule, taskLen and jobNum, add to capacity schedule optimally (minimizing sum of end times statically)
def assignTask(CapSched, taskLen, jobNum):

	#might have to make an adjustment to the slack value later on
	assigned = False
	curTask = Task(jobNum, taskLen, 0)

	#check the spot that makes the slack equal to zero (get slack value for it)
	jobEndTime = getJobEndTime(jobNum, CapSched)
	if (jobEndTime > 0):
		timeSlotPlacement = jobEndTime - taskLen
	else:
		timeSlotPlacement = 1

	#set curTask to timeslot if it is not yet assigned
	if (CapSched[timeSlotPlacement].assigned == False):
		CapSched[timeSlotPlacement].assign(curTask)
		return CapSched


	#find another place to put the job
	else:

		#check the spaces before it 
		while(timeSlotPlacement > 0):

			timeSlotPlacement = timeSlotPlacement - 1

			curSlack = curTask.getSlack()
			curTask.setSlack(curSlack + 1)

			if (CapSched[timeSlotPlacement].assigned == False):
				CapSched[timeSlotPlacement].assign(curTask)
				return CapSched
	
		#check the spaces after it
		if (jobEndTime > 0):
			timeSlotPlacement = jobEndTime - taskLen
		else:
			timeSlotPlacement = 1

		curTask.setSlack(0)

		while not (assigned):


			if (CapSched[timeSlotPlacement].assigned == False):
				CapSched[timeSlotPlacement].assign(curTask)
				return CapSched

			timeSlotPlacement = timeSlotPlacement + 1
			increaseSlackForJob(jobNum, CapSched)
	
	return CapSched


############################################################################################################################
##		Start helper functions 
############################################################################################################################

def increaseSlackForJob(jobNum, CapacitySchedule):
	#print("not yet implemented yet")

	for i in range(len(CapacitySchedule)):
		if (CapacitySchedule[i].assigned == False):
			continue
		if (CapacitySchedule[i].task.getJobNum() == jobNum):

			currentSlack = CapacitySchedule[i].task.getSlack()
			CapacitySchedule[i].task.setSlack(currentSlack + 1)


#if there's gaps in the capacity schedule, shift back the jobs on the end
def shiftBack(CapSched):

	for i in range(len(CapSched)):

		if (i == 0):
			continue

		#check if empty gap before an assigned job
		if (CapSched[i].assigned == True and CapSched[i-1].assigned == False):
			addedSlack = 0
			j = i

			#go back for as long as there are empty slots
			while (j > 0 and CapSched[j-1].assigned == False):
				addedSlack = addedSlack + 1
				j = j - 1
			
			#create new task with new slack value
			newTask = Task(CapSched[i].task.getJobNum(), CapSched[i].task.getTaskLen(), CapSched[i].task.getSlack() + addedSlack)
			#assign new task
			CapSched[j].assign(newTask)
			#delete old task by replacing with an empty time slot
			CapSched[i] = TimeSlot()


#this adjusts slack levels based on the potentail changes made by readjustmentTest()
def changeSlack(CapSched, jobNum):
	#find when the job ends
	endTime = 0
	for i in range(len(CapSched)):
		if (CapSched[i].assigned == False):
			continue

		if (CapSched[i].task.getJobNum() == jobNum):

			if (i + CapSched[i].task.getTaskLen() > endTime):
				endTime = i + CapSched[i].task.getTaskLen()


	#resets the slack values for tasks in that job
	for i in range(len(CapSched)):
		if (CapSched[i].assigned == False):
			continue
		
		if (CapSched[i].task.getJobNum() == jobNum):

			CapSched[i].task.setSlack(endTime - CapSched[i].task.getTaskLen() - i)

	return CapSched



def getSumOfEndTimes(numberOfJobs, CapSched):
	
	sum = 0
	for i in range(numberOfJobs):
		curJob = 0
		curJob = getJobEndTime(i+1, CapSched)
		sum = sum + curJob

	return sum

def getJobEndTime(jobNum, CapacitySchedule):

	maximum = 0
	for i in range(len(CapacitySchedule)):

		if (CapacitySchedule[i].assigned == False):
			continue

		if (CapacitySchedule[i].task.getJobNum() == jobNum):

			if (CapacitySchedule[i].task.getTaskLen() + i > maximum):
				maximum = CapacitySchedule[i].task.getTaskLen() + i
				

	return maximum

############################################################################################################################
##		End helper functions 
############################################################################################################################


############################################################################################################################
##		Start functions that handle the readjustment after initial scheduling 
############################################################################################################################

#objective of this function:
#create a list of dictionaries (index of list corresponds to job number)
#keys - slack value
#values - number of times it occurs
def createSlackDictionary(CapSched, numJobs):
	dictionaryList = []
	for i in range(numJobs):
		jobDictionary = {}
		for j in range(len(CapSched)):
			if (CapSched[j].assigned == False):
				continue
			else:
				if (i+1 == CapSched[j].task.getJobNum()):

					curSlack = CapSched[j].task.getSlack()

					if curSlack in jobDictionary:
						jobDictionary[curSlack] = jobDictionary[curSlack] + 1
					else:
						#print("got here")
						jobDictionary[curSlack] = 1


		#create a sorted dictionary for future processing 
		sortedDict = {}
		for key in sorted(jobDictionary.keys()):
			sortedDict[key] = jobDictionary[key]

		#append current dictionary to the list of dictionaries
		dictionaryList.append(sortedDict)

	return dictionaryList


#input taskToShift (the initial index of the task that needs to be shifted),
#shift amount (how far to move it back), the CapSched and numJobs

#push back the slack 0 task i spaces (readjusting capacity schedule)

#output: the new capacity schedule from making that shift
def moveBackTask(taskToShift, shiftAmt, CapSched, numJobs):

	newCapSched = []

	shiftForwardOneList = []

	if (taskToShift - shiftAmt <= 0):
		return CapSched

	#add the tasks before the shifted task
	for i in range(0, taskToShift - shiftAmt):
		if (CapSched[i].assigned == False):
			continue
		curTaskLen = CapSched[i].task.getTaskLen()
		curJobNum = CapSched[i].task.getJobNum()
		curTask = Task(curJobNum, curTaskLen, 0)
		timeSlot = TimeSlot()
		timeSlot.assign(curTask)
		newCapSched.append(timeSlot)


	#write task to shift to the next index
	#add all tasks to be shifted forward one to a list (to be added to the new Cap Sched later)
	for i in range(taskToShift - shiftAmt, taskToShift):
		if (CapSched[i].assigned == False):
			continue
		shiftForwardOneList.append(CapSched[i])


	#add the task that's shifted
	curJobNum = CapSched[taskToShift].task.getJobNum()
	curTaskLen = CapSched[taskToShift].task.getTaskLen()
	curTask = Task(curJobNum, curTaskLen, 0)
	timeSlot = TimeSlot()
	timeSlot.assign(curTask)
	newCapSched.append(timeSlot)


	#add all the tasks that are shifted by one
	for i in range(len(shiftForwardOneList)):
		curJobNum = shiftForwardOneList[i].task.getJobNum()
		curTaskLen = shiftForwardOneList[i].task.getTaskLen()
		curTask = Task(curJobNum, curTaskLen, 0)
		timeSlot = TimeSlot()
		timeSlot.assign(curTask)
		newCapSched.append(timeSlot)

	#add all the unmodified tasks after the change
	for i in range(taskToShift + 1, len(CapSched)):
		if (CapSched[i].assigned == False):
			continue

		curTaskLen = CapSched[i].task.getTaskLen()
		curJobNum = CapSched[i].task.getJobNum()
		curTask = Task(curJobNum, curTaskLen, 0)
		timeSlot = TimeSlot()
		timeSlot.assign(curTask)
		newCapSched.append(timeSlot)

	#recalculate all slack values (call changeSlack(newCapSched, jobNum) with for loop for each job)
	for i in range(numJobs):
		changeSlack(newCapSched, i+1)
	return newCapSched


def readjustCapacitySchedule(CapSched, dictList):

	numberOfJobs = len(dictList)
	curSumEndTimes = getSumOfEndTimes(numberOfJobs, CapSched)

	#record old capacity schedule
	oldSchedule = CapSched.copy()
	newSched = []
	changedSchedule = False
	for i in range(numberOfJobs):
		#CapSched = oldSchedule.copy()
		#current dictList item
		curDict = dictList[i]

		#check dictionary to see if it has a key value pair of 0, 1 (1 task with slack 0)
		if (curDict[0] > 0):

			#if so, iterate through rest of dictionary and find the minimum of slacks (just check the next value because it should be sorted)\
			if (len(curDict) > 1):
				minSlack = INITIAL_MIN_SLACK
				for j in curDict.keys():

					if (j == 0):
						continue
					elif (j < minSlack):
						minSlack = j


				for j in range(minSlack):
					#CapSched = oldSchedule.copy()
					curTaskToShift = 0
					
					#iterate through capacity schedule and find the task with slack 0 and current job (i+1)
					for k in range(len(CapSched)):

						if (CapSched[k].task.getJobNum() == i + 1 and CapSched[k].task.getSlack() == 0):
							curTaskToShift = k
							break

					newCapSched = moveBackTask(curTaskToShift, j + 1, CapSched, numberOfJobs)
					newSumOfEndtimes = getSumOfEndTimes(numberOfJobs, newCapSched)
					if (newSumOfEndtimes < curSumEndTimes):
						newSched = newCapSched
						changedSchedule = True
						CapSched = newSched.copy()

					CapSched = oldSchedule.copy()

	if(changedSchedule):
		return newSched

	else:
		return oldSchedule


############################################################################################################################
##		End functions that handle the readjustment after initial scheduling 
############################################################################################################################


############################################################################################################################
##		Start functions to help with debugging/getting info about assignments
############################################################################################################################


#display the information regarding the created capacity schedule
def printSlackValues(CapacitySchedule):
	print()
	for i in range(len(CapacitySchedule)):
		if (CapacitySchedule[i].assigned == False):
			continue
		print("t=" + str(i) + ": job num: " + str(CapacitySchedule[i].task.getJobNum()) + ", task len: " + str(CapacitySchedule[i].task.getTaskLen()) +  ", slack: " + str(CapacitySchedule[i].task.getSlack()))

#Iterate through the EndTimes vector and print out values with the job numbers
def printEndTimes(numberOfJobs, CapacitySchedule):

	sumOfEndTimes = 0
	print("End Times:")
	for i in range(numberOfJobs):
		curEndTime = getJobEndTime(i+1, CapacitySchedule)
		print("Job " + str(i+1) +": " + str(curEndTime))
		sumOfEndTimes = sumOfEndTimes + curEndTime
	print("Sum of End Times: " + str(sumOfEndTimes))


#Print out all key-value pairs
#Key = slack value
#Value = number of tasks with this slack value 
def printDictList(dictList):
	for i in range(len(dictList)):
		print("Job num: " + str(i+1))

		for key, value in dictList[i].items():
			#print("here")
			print("Key: " + str(key) + ", Value: " + str(value))
	

############################################################################################################################
##		End functions to help with debugging/getting info about assignments
############################################################################################################################
