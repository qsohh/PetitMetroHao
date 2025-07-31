#!/usr/bin/env python
import InitData.init_many_trains_many_blocks as init
# import InitData.init_random_line as init
import PlotTool.fct_plot as fplt

sns = init.sns
trs = init.trs
stations = init.stations
trains = init.trains
env1 = init.env1
dummies = init.dummies
TIME = init.TIME
dt = init.dt

for ele in dummies:
    ele.command(dt)
for ele in stations:
    ele.control(TIME, dt)

TT = []
TT.append(TIME)
TIME += dt

# ---------------------------------------------------------------

maxtime = 200.
while TIME < maxtime:  # 700.:
    TT.append(TIME)
    env1.update_env()
    for ele in dummies:
        ele.command(dt)
    for ele in stations:
        ele.control(TIME, dt)
    env1.update_env()
    TIME += dt
    if len(TT) % 1000 == 0:
        print('time', TIME)

# XX, YY = env1.lines[0].show_limit_speed_info()
# XX2, YY2 = env1.lines[1].show_limit_speed_info()
# for i in range(len(XX2)):
#     XX2[i] += env1.lines[0].tracklength_line  # 435.

# plt.figure()
# plt.plot(TT, train93341.VV)
# plt.xlabel('TIME (s)')
# plt.ylabel('speed (m/s)')
# plt.title('current speed of a simple scenario of traffic simulation')

# plt.figure()
# plt.plot(DD1, train93341.VV, 'b')
# # plt.plot(XX+XX2, YY+YY2, 'r')
# plt.plot(DD1, dummies[0].NVC, 'g--')
# plt.plot(DD1, train93341.TV, 'y--')
# # plt.axvline(x=275.)
# # plt.axvline(x=430.)
# # plt.axvline(x=165. + 505.)
# plt.xlabel('distance on the route (m)')
# plt.ylabel('speed (m/s)')
# plt.legend(('current speed',  # 'limit speed',
#            'next limit speed inf', 'current target speed'),
#            loc=(0.13, 0.05), fontsize=8)
# plt.title('a simple scenario of traffic simulation')
# # plt.savefig('2stations_v_d.png')


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
