#TimeTest0
import time

time.time()
#1970年1月1日0:00开始到当前时间
#1588995726.000384

time.ctime()
#获得当前时间
#'Sat May  9 11:42:24 2020'

t = time.gmtime()
#其他程序可用的时间
#time.struct_time(tm_year=2020, tm_mon=5, tm_mday=9, tm_hour=3, tm_min=46, tm_sec=33, tm_wday=5, tm_yday=130, tm_isdst=0)

time.strftime("%Y-%m-%d %H:%M:%S",t)
#时间格式化
#'2020-05-09 03:50:48'

timeStr = '2020-05-09 03:50:48'
time.strptime(timeStr,"%Y-%m-%d %H:%M:%S")
#time.struct_time(tm_year=2020, tm_mon=5, tm_mday=9, tm_hour=3, tm_min=50, tm_sec=48, tm_wday=5, tm_yday=130, tm_isdst=-1)

start = time.perf_counter()
end = time.perf_counter()
end - start
#程序计时
#13.489014700000098

def wait():
	time.sleep(5)
wait()
#程序休眠5s
