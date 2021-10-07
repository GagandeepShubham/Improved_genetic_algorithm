import re
import random
import copy
import plotly.figure_factory as ff
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go


def print_jobs(jobs):
  cnt = 1
  for job in jobs:
    print("job", cnt, " = ", job)
    cnt +=1

def print_machines(machines):
  cnt = 1
  for mc in machines:
    print("machine", cnt, " = ", mc)
    cnt += 1

def update_jobs(machines, jobs):
  print("Perform Update jobs ---")
  print_machines(machines)
  print("BF = ")
  print_jobs(jobs)
  for mc in range(len(machines)):
    for op in range(len(machines[mc])):
      jobs[machines[mc][op][0]-1][machines[mc][op][1]-1][2] = machines[mc][op][3]
  print("After = ")
  print_jobs(jobs)
  print("End perform update jobs")
  return jobs

def check_machines(machines):
  for mc in range(len(machines)):
    for i in range(len(machines[mc])-1):
      for j in range(i+1, len(machines[mc])):
        if machines[mc][i][0] == machines[mc][j][0] and machines[mc][j][1] < machines[mc][i][1]:
          print("NOT valid")
          return False
  print("Valid")
  return True


def check(machines, jobs, crossover_prob, mutation_prob):
  new_machines = []
  for _ in range(len(machines)):
    mc = [ int(0) for i in range(10000) ]
    new_machines.append(mc)
  
  #print("MC = ", new_machines)
  queue = [i for i in range(len(jobs))]
  random.shuffle(queue)
  #print("Q = ", queue)
  for job_no in queue:
    for job_op in range(len(jobs[job_no])):
      a = jobs[job_no][job_op][0]-1 #machine
      b = jobs[job_no][job_op][1] #time
      if job_op == 0:
        c = jobs[job_no][job_op][2] #start
      else:
        c = jobs[job_no][job_op-1][1]+jobs[job_no][job_op-1][2]
      #print("Job = ", jobs[job_no][job_op])
      #print("range = ", c, 50-b-1)
      #print("MC = ", new_machines[a])
      flag = True
      for mc in range(c, 10000-b-1):
        if flag:
          #print("mc = ", mc, "end =", mc+b)
          #print("MR = ", [new_machines[a][x] for x in range(mc, mc+b)])
          if sum([new_machines[a][x] for x in range(mc, mc+b)]) == 0:
            for j in range(mc, mc+b):
              new_machines[a][j] = job_no+1
            jobs[job_no][job_op][2] = mc
            for g in range(len(machines[a])):
              if machines[a][g][0] == job_no+1 and machines[a][g][1] == job_op+1:
                machines[a][g][3] = mc
            flag = False
        else:
          break
      #print("UMC = ", new_machines[a])
  #print_machines(machines)
  #jobs = update_jobs(machines, jobs)
  #print_jobs(jobs)
  mksp = 0
  for job in jobs:
    if job[len(job)-1][1]+job[len(job)-1][2] > mksp:
      mksp = job[len(job)-1][2]+job[len(job)-1][1]
  #print("MKSP = ", mksp)
  #print("----------------END CHECK---------------------\n\n")
  return machines, jobs, mksp


  '''for mc in range(len(machines)):
    start = 0
    for op in range(len(machines[mc])):
      jobs[machines[mc][op][0]-1][machines[mc][op][1]-1][2] = start
      machines[mc][op][3] = start
      start += machines[mc][op][2]
  print("-------------START CHECK------------------------")
  print_machines(machines)
  print_jobs(jobs)

  for job in range(len(jobs)):
    for op in range(len(jobs[job])-1):
      if jobs[job][op+1][2] < jobs[job][op][1]+jobs[job][op][2]:
        start = jobs[job][op][1]+jobs[job][op][2]
        mc_num = jobs[job][op+1][0]
        print("U = ", job+1, op+2, start, mc_num)
        flag = False
        for mcop in range(len(machines[mc_num-1])):
          if flag == False:
            if machines[mc_num-1][mcop][0] == job+1 and machines[mc_num-1][mcop][1] == op+2:
              flag = True
          if flag == True:
            machines[mc_num-1][mcop][3] = start
            start += machines[mc_num-1][mcop][2]
  jobs = update_jobs(machines, jobs)
  print("--------")
  print_machines(machines)
  print_jobs(jobs)
  mksp = 0
  for job in jobs:
    if job[len(job)-1][2] > mksp:
      mksp = job[len(job)-1][2]+job[len(job)-1][1]
  print("MKSP = ", mksp)
  print("----------------END CHECK---------------------\n")
  return machines, jobs, mksp'''

def draw_plot(machines, jobs):
  df = []
  cnt = 1
  for mc in machines:
    for op in mc:
      x = {}
      x["Task"] = "Machine-"+str(cnt)
      x["Job"] = "Job-"+str(op[0])
      x["Start"] = int(op[3])
      x["Finish"] = int(op[2] + op[3])
      df.append(x)
    cnt += 1
  #print(type(df))
  #print(df)
  '''
  #colors = ['#%06X' % random.randint(0, 256 ** 3 - 1) for _ in range(len(jobs))]
  fig = ff.create_gantt(df)
  fig.show()'''
  #df = [dict(Task="Job-1", Start='2017-01-01', Finish='2017-02-02', Resource='Complete'), dict(Task="Job-1", Start='2017-02-15', Finish='2017-03-15', Resource='Incomplete')]
  #print(type(df))
  #print(df)
  """colors = {'Job-1': 'rgb(220, 0, 0)',
          'Job-2': (1, 0.9, 0.16),
          'Job-3': 'rgb(0, 255, 100)'}"""
          
  job_count = len(jobs)
  temp = 1
  colors = {} #to store the colors corresponding to each job.

  # Define random colors for jobs
  clr = ['#%06X' % random.randint(0, 256 ** 3 - 1) for _ in range(len(jobs))]

  for _ in range(job_count):
    colors.update({f'Job-{temp}':clr[temp - 1]})
    temp += 1

  df = pd.DataFrame(df) #added
  fig = ff.create_gantt(df, colors=colors, index_col='Job', show_colorbar=True, group_tasks=True)
  fig.layout.xaxis.type = 'linear'
  fig.layout.xaxis.tickformat = 'j'
  go.FigureWidget(fig)
  fig.show()


'''def check_machine(machine, num_jobs):
  for i in range(1, len(machine)):
    if job[machine[i][0]-1] == False:
      for j in range'''













#--------------------------------------------------------
#-------------------MAIN CODE----------------------------
#--------------------------------------------------------

filename = input ("Enter file name: ")
file1 = open(filename, 'r')
#file1 = open('test.fjs', 'r')
Lines = file1.readlines()

num_machines = 0
num_jobs = 0
num_op_eachjob = []

jobs = []
machines = []

count = 0
# Strips the newline character
for line in Lines:
  count += 1
  line = re.findall('\S+', line)
  if count == 1:
    num_machines = int(line[0])
    num_jobs = int(line[1])
    for i in range(num_machines):
      machines.append([])
    continue;
  job = []
  start = 2
  #print(line)
  #print(line[0])
  num_op_eachjob.append(int(line[0]))
  for i in range(int(line[0])):
    op = []
    op.append(int(line[start]))
    start += 1
    op.append(int(line[start]))
    machines[op[0]-1].append([count-1, i+1, op[1], int(0)])
    op.append(int(0))
    job.append(op)
    start += 2
  jobs.append(job)
  

print("Job operations")
print("[machine, processing time, start time]")
print_jobs(jobs)

print("Machine operations:")
print("[job no, operation no, processing time, start time]")
print_machines(machines)

num_gen = int(input("Enter the population size: "))
crossover_prob = float(input("Enter the crossover probability: "))
mutation_prob = float(input("Enter the mutation probability: "))

#machines = check_machines(machines)
#new_machines, new_jobs, mksp = check(machines, jobs)
#check(machines, jobs)
mksp = 999999
optimal_machines = []
optimal_jobs = []
flag_t = 0
for _ in range(num_gen):
  '''x = random.randint(0, len(machines)-1)
  if len(machines[x]) == 1:
    continue
  random.shuffle(machines[x])
  if check_machines(machines) == False:
    continue'''
  new_machines, new_jobs, new_mksp = check(machines, jobs, crossover_prob, mutation_prob)
  #print("New mksp = ", new_mksp)
  if new_mksp < mksp:
    mksp = new_mksp
    optimal_machines = copy.copy(new_machines)
    optimal_jobs = copy.copy(new_jobs)
    flag_t = 1 #added
    #print("\n\nNew mksp = ", mksp)
    #print("New machines")
    #print_machines(optimal_machines)
    #print("New jobs")
    #print_jobs(optimal_jobs)
#draw_plot(machines, jobs)

print("Final makespan = ", mksp)

#Drawing the gantt chart
print("Gantt Chart")
if flag_t == 1:
  draw_plot(optimal_machines, optimal_jobs)
else:
  draw_plot(machines, jobs)
'''while True:
  print("Menu:")
  print("1. Print job details")
  print("2. Print machine details")
  print("3. Draw gantt chart")
  print("4. Print final makespan")
  print("5. Exit")
  while True:
    value = int(input("Enter:"))
    if value == 1:
        print("Job operations")
        print("[machine, processing time, start time]")
        print_jobs(optimal_jobs)
    elif value == 2:
        print("Machine operations:")
        print("[job no, operation no, processing time, start time]")
        print_machines(optimal_machines)
    elif value == 3:
        print("Gantt chart")
        draw_plot(optimal_machines, optimal_jobs)
    elif value == 4:
        print("Final makespan value = ", mksp)
    elif value == 5:
        exit()
    else:
      input("Wrong option selection. Enter any key to try again...")'''
    

