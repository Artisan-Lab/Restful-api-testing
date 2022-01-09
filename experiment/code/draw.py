import csv
import matplotlib
import matplotlib.dates as mdate
from matplotlib.dates import HourLocator
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.pyplot import MultipleLocator
from datetime import datetime




y_major_locator=MultipleLocator(600)
forest_file = open('../data/gitlab-project/foREST_gitlab_projects.csv')  # 打开csv文件
forestReader = csv.reader(forest_file)  # 读取csv文件
forestData = list(forestReader)  # csv数据转换为列表
forest_length = len(forestData)  # 得到数据行数

evomaster_file = open('../data/gitlab-project/evomaster_gitlab_projects.csv')
evomaster_reader = csv.reader(evomaster_file)
evomaster_data = list(evomaster_reader)
evomaster_length = len(evomaster_data)

restler_file = open('../data/gitlab-project/reslter.csv')
restler_reader = csv.reader(restler_file)
restler_data = list(restler_reader)
restler_length = len(restler_data)
# for i in range(1,length_zu):
#     print(exampleData[i])

x1 = list()
y1 = list()

x2 = list()
y2 = list()

x3 = list()
y3 = list()
for i in range(0, forest_length):  # 从第二行开始读取
    date1 = datetime.strptime(forestData[i][0], '%H:%M:%S.%f')
    x1.append(date1)  # 将第一列数据从第二行读取到最后一行赋给列表x
    y1.append(int(forestData[i][2]))

for _ in range(0, evomaster_length):
    date2 = datetime.strptime(evomaster_data[_][0], '%H:%M:%S.%f')
    x2.append(date2)
    y2.append(int(evomaster_data[_][2]))

for _ in range(0, restler_length):
    date3 = datetime.strptime(restler_data[_][0], '%H:%M:%S.%f')
    x3.append(date3)
    y3.append(int(restler_data[_][2]))

fig, ax = plt.subplots()

# Plot the date using plot_date rather than plot
ax.plot(x1, y1, 'r-', label='foREST', linewidth=3)
ax.plot(x2, y2, 'b--', label='EvoMaster', linewidth=3)
ax.plot(x3, y3, color='violet', linestyle='-.', label='RESTler', linewidth=3)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
plt.ylabel('Code coverage')
plt.xlabel('time/s')

ax.xaxis.set_major_formatter(mdate.DateFormatter('%H:%M:%S'))
# Choose your xtick format string
# date_fmt = '%m-%d %H:%M:%S'
# Use a DateFormatter to set the data to the correct format.

ax.yaxis.set_major_locator(y_major_locator)
# Sets the tick labels diagonal so they fit easier.
# plt.ylim((10000, 30000))
plt.title('GitLab-project')
plt.legend(bbox_to_anchor=(1, 0.11), loc='upper right', borderaxespad=0, fontsize=8)
fig.savefig('gitlab_projects.svg', format='svg', dpi=300)

plt.show()




