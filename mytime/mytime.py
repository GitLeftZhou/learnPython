# -*- coding:utf-8 -*-
import datetime,time

print("clock1="+ str(time.clock()))
bgn = time.time()
dt = datetime.datetime.now()
print(dt.year)
print(dt.strftime("%Y/%m/%d %H:%M:%S"))
time.sleep(2)
end = time.time()
time.sleep(1)
print("exec last " + str(end-bgn))
time.sleep(1)
print("clock2="+str(time.clock()))
time.sleep(1)
print("clock3="+str(time.clock()))