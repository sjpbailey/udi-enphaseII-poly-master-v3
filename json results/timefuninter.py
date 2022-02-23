import datetime
#from datetime import datetime

import time

#now = datetime.now()

#current_time = now.strftime("%H%M%S")
#print("Current Time =", current_time)
t0 = time.time()
print(t0)

    
while True:
    t0 = time.time()
if (time.strftime("%H:%M",time.localtime(t0))) > (today_sr.strftime('%H:%M')) and (time.strftime("%H:%M",time.localtime(t0))) < (today_ss.strftime('%H:%M')):
    print (random.randint(0,20))
else:
    print ("nighttime...")
    time.sleep(10)
    

