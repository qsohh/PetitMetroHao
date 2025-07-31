#!/usr/bin/env python
import InitData.init_many_trains_many_blocks as init
import PlotTool.fct_plot as fplt


def simulate(dummies, stations, time, dt):
    for ele in dummies:
        ele.command(dt)
    for ele in stations:
        ele.control(time, dt)


sns = init.sns
trs = init.trs
stations = init.stations
trains = init.trains
env1 = init.env1
dummies = init.dummies
TIME = init.TIME
dt = init.dt

TT = []
TT.append(TIME)
simulate(dummies, stations, TIME, dt)
TIME += dt

maxtime = 5000.
while TIME < maxtime:  # 700.:
    TT.append(TIME)
    env1.update_env()
    simulate(dummies, stations, TIME, dt)
    env1.update_env()
    TIME += dt

    if len(TT) % 1000 == 0:
        print('time', TIME)

# set of the absolut position:
added_position, all_position = fplt.parameter_plot(trs, 36, 70.)

fplt.plot_position_time(TT, trains, trs, added_position, 'many trains')

fplt.plot_distance_time(TT, trains, trs, all_position, 'many trains')

fplt.plot_speed_time(TT, trains, 'many trains')

# Ptrain = []
# Dtrain = []
# added_to_dis = []
# DiffTrain = []
# for i in range(len(trains)):
#     Ptrain.append([])
#     Dtrain.append([])
#     DiffTrain.append([])
#     ind = trs.index(trains[i].PP[0].track)
#     added_to_dis.append(all_position[ind])

# for i in range(len(TT)):
#     for j in range(len(trains)):
#         ind = trs.index(trains[j].PP[i].track)
#         if ind < 17:
#             Ptrain[j].append(added_position[ind] +
#                              trains[j].PP[i].abs_position_track)
#         else:
#             Ptrain[j].append(added_position[ind] -
#                              trains[j].PP[i].abs_position_track)
#         Dtrain[j].append(trains[j].DD[i] + added_to_dis[j])
#         if j == 0:
#             continue
#         else:
#             DiffTrain[j].append(Dtrain[j][i]-Dtrain[j-1][i])

# plt.figure()
# # for i in range(len(trains)):
# for i in range(7):
#     plt.plot(TT, Ptrain[i])
# plt.axhspan(10, 60, 0, maxtime, fc='gray')
# plt.axhspan(945, 1015, 0, maxtime, fc='gray')
# plt.axhspan(2100, 2150, 0, maxtime, fc='gray')
# plt.xlabel('time (s)')
# plt.ylabel('position (m)')
# plt.title('two terminus')
# plt.legend(('0', '1', '2', '3', '4', '5', '6'), fontsize=8)
# # plt.savefig('2_terminus.png')

# plt.figure()
# # for i in range(len(trains)):
# for i in range(7):
#     plt.plot(TT, Dtrain[i])
# plt.xlabel('time (s)')
# plt.ylabel('distance (m)')
# plt.title('two terminus')
# plt.legend(('0', '1', '2', '3', '4', '5', '6'), fontsize=8)
# # plt.savefig('2_terminus.png')

# plt.figure()
# for i in range(len(trains) - 1):
#     plt.plot(TT, DiffTrain[i+1])
# plt.xlabel('time (s)')
# plt.ylabel('distance (m)')
# plt.title('two terminus distane between two trains')

# plt.show()
