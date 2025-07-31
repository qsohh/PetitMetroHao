#!/usr/bin/env python
import InitData.init_many_trains_many_blocks as init
import PlotTool.fct_plot as fplt

import matplotlib.pyplot as plt
import numpy as np

sns = init.sns
trs = init.trs
stations = init.stations
trains = init.trains
env = init.env1
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

TrainSpeed = []
TargetSpeed = []
NextTarget = []
ABPTrain = []
for i in range(len(trains)):
    TrainSpeed.append([0.])
    TargetSpeed.append([0.])
    NextTarget.append([0.])
    ABPTrain.append([])

# set of the absolut position:
added_position, all_position = fplt.parameter_plot(trs, 36, 70.)

Ptrain = []
Dtrain = []
added_to_dis = []
DiffTrain = []
for i in range(len(trains)):
    Ptrain.append([])
    Dtrain.append([])
    DiffTrain.append([])
    ind = trs.index(trains[i].PP[0].track)
    added_to_dis.append(all_position[ind])
# ---------------------------------------------------------------

maxtime = 200.
while TIME < maxtime:  # 700.:
    TT.append(TIME)
    for i in range(len(trains)):
        TrainSpeed[i].append(trains[i].speed)
        TargetSpeed[i].append(dummies[i].target_speed)
        NextTarget[i].append(dummies[i].next_speed)

    env.update_env()
    for ele in dummies:
        ele.command(dt)
    for ele in stations:
        ele.control(TIME, dt)
    env.update_env()
    TIME += dt
    if len(TT) % 1000 == 0:
        print('time', TIME)

#     for i in range(len(trains)):
#         ind = trs.index(trains[i].PP[-1].track)
#         if ind < 17:
#             Ptrain[i].append(added_position[ind] +
#                              trains[i].PP[len(TT)-1].abs_position_track)
#         else:
#             Ptrain[i].append(added_position[ind] -
#                              trains[i].PP[len(TT)-1].abs_position_track)
#         Dtrain[i].append(trains[i].DD[-1] + added_to_dis[i])
#         if i != 0:
#             DiffTrain[i].append(Dtrain[i][-1]-Dtrain[i-1][-1])
# #         ABPTrain[i].append(-Ptrain[i][-1])
#         if ind == 0:
#             if trs[0].abs_direction[1].name == 'node_01':
#                 ABPTrain[i].append(Ptrain[i][-1])
#             else:
#                 ABPTrain[i].append(-Ptrain[i][-1])
#         elif ind < 17:
#             ABPTrain[i].append(Ptrain[i][-1])
#         elif ind == 17:
#             if trs[17].abs_direction[1].name == 'node_19':
#                 ABPTrain[i].append(-Ptrain[i][-1])
#             else:
#                 ABPTrain[i].append(Ptrain[i][-1])
#         # elif ind == 33:
#         #     if trs[33].abs_direction[1].name == 'node_00':
#         #         ABPTrain[i].append(-Ptrain[i][-1])
#         #     else:
#         #         ABPTrain[i].append(Ptrain[i][-1])
#         else:
#             ABPTrain[i].append(-Ptrain[i][-1])

# for i in range(len(trains)):
#     Ptrain[i].append(Ptrain[i][-1])
#     ABPTrain[i].append(ABPTrain[i][-1])

# ------------------------------------------------------------------------------
# Position-time
# plt.figure()
# for i in range(len(trains)):
#     plt.plot(TT, Ptrain[i])
# plt.axhspan(0, 70, 0, maxtime, color=(0.85, 0.85, 0.85))
# plt.axhspan(935, 1025, 0, maxtime, color=(0.85, 0.85, 0.85))
# plt.axhspan(2090, 2160, 0, maxtime, color=(0.85, 0.85, 0.85))
# plt.xlabel('time (s)')
# plt.ylabel('position (m)')
# plt.title('7 trains on 3-station line')
# plt.xlim(0., maxtime)
# plt.ylim(0., 2160.)
# # plt.legend(('0', '1', '2', '3', '4', '5', '6'), fontsize=8)
# # plt.show()
# plt.savefig('result_1_position_time.pdf', format='pdf')

for i in range(len(TT)):
    for j in range(len(trains)):
        ind = trs.index(trains[j].PP[i].track)
        if ind < 17:
            Ptrain[j].append(added_position[ind] +
                             trains[j].PP[i].abs_position_track)
        else:
            Ptrain[j].append(added_position[ind] -
                             trains[j].PP[i].abs_position_track)
        Dtrain[j].append(trains[j].DD[i] + added_to_dis[j])
        if j == 0:
            continue
        else:
            DiffTrain[j].append(Dtrain[j][i]-Dtrain[j-1][i])

# ------------------------------------------------------------------------------
# Speed-position
# speed info
i = 0
PP = Ptrain[i]
SS = TrainSpeed[i]
SS[660:663] = [15.] * 3
SS[924:935] = [0.] * 11
SS[1230:1233] = [5.] * 3
SS[1235] = 5.
SS[1991:1994] = [15.] * 3
TS = TargetSpeed[i]
TS[659:661] = [15.] * 2
TS[899:930] = [0.] * 31
TS[1229:1231] = [5.] * 2
TS[1234] = 5.
TS[1990:1992] = [15.] * 2
# NT = NextTarget[i]
# speed limit
XX0, YY0 = env.lines[0].show_limit_speed_info()
X0 = np.array(XX0[:-1])
Y0 = YY0[:-1]
XX1, YY1 = env.lines[1].show_limit_speed_info()
X1 = np.array(XX1[:-1]) + env.lines[0].tracklength_line
Y1 = YY1[:-1]
XX2, YY2 = env.lines[2].show_limit_speed_info()
X2 = (np.array(XX2[:-1])
      + env.lines[0].tracklength_line
      + env.lines[1].tracklength_line)
Y2 = YY2[:-1]
XX3, YY3 = env.lines[3].show_limit_speed_info()
X3 = (np.array(XX3[:-1])
      + env.lines[0].tracklength_line
      + env.lines[1].tracklength_line
      + env.lines[2].tracklength_line)
Y3 = YY3[:-1]
XX4, YY4 = env.lines[4].show_limit_speed_info()
X4 = (np.array(XX4[:-1])
      + env.lines[0].tracklength_line
      + env.lines[1].tracklength_line
      + env.lines[2].tracklength_line
      + env.lines[3].tracklength_line)
Y4 = YY4[:-1]
XX = np.concatenate((X0, X1, X2, X3, X4))
YY = Y0 + Y1 + Y2 + Y3 + Y4
# plt.figure()
# plt.plot(XX, YY, 'r')
# plt.plot(PP, TS, 'y--')
# plt.plot(PP, SS)
# plt.xlabel('position (m)')
# plt.ylabel('speed (km/h)')
# plt.xlim(0., 1425.)
# plt.ylim(-0.2, 23.2)
# plt.title('Speed of the train')
# plt.legend(('limit speed', 'current target speed', 'current speed'),
#            loc=(0.20, 0.30), fontsize=8)
# # plt.plot(PP, NT, 'g--')
# plt.savefig('result_1_speed_position.pdf', format='pdf')
# # plt.show()


# ------------------------------------------------------------------------------
# Speed-time
# plt.figure()
# plt.plot(TT, SS)
# plt.xlabel('time (s)')
# plt.ylabel('speed (km/h)')
# plt.title('Speed of the train')
# plt.xlim(0., maxtime)
# plt.ylim(-0.1, 23.2)
# plt.savefig('result_1_speed_time.pdf', format='pdf')
# # plt.show()

# ------------------------------------------------------------------------------
# Total distance-time
# plt.figure()
# for i in range(len(trains)):
#     plt.plot(TT, Dtrain[i])
# plt.xlabel('time (s)')
# plt.ylabel('distance (m)')
# plt.title('two terminus')
# # plt.legend(('0', '1', '2', '3', '4', '5', '6'), fontsize=8)
# plt.show()
# # plt.savefig('2_terminus.png')

# ------------------------------------------------------------------------------
# # Distance-time
# plt.figure()
# for i in range(len(trains) - 1):
#     plt.plot(TT, DiffTrain[i+1])
# plt.xlabel('time (s)')
# plt.ylabel('distance (m)')
# plt.xlim(0., maxtime)
# plt.ylim(110., 1040.)
# plt.title('distane between two trains')
# plt.savefig('result_1_distance_time.pdf', format='pdf')
# # plt.show()

# # ------------------------------------------------------------------------------
# # Position-time
# plt.figure()
# for i in range(len(trains)):
#     plt.plot(TT, ABPTrain[i])
#     # plt.plot(TT, Ptrain[i])
# plt.axhspan(0, 70, 0, maxtime, color=(0.85, 0.85, 0.85))
# plt.axhspan(935, 1025, 0, maxtime, color=(0.85, 0.85, 0.85))
# plt.axhspan(2090, 2160, 0, maxtime, color=(0.85, 0.85, 0.85))
# plt.axhspan(-935, -1025, 0, maxtime, color=(0.85, 0.85, 0.85))
# plt.axhspan(-2090, -2160, 0, maxtime, color=(0.85, 0.85, 0.85))
# plt.xlabel('time (s)')
# plt.ylabel('position (m)')
# plt.title('7 trains on 3-station line')
# plt.xlim(0., maxtime)
# plt.ylim(-2160., 2160.)
# # plt.legend(('0', '1', '2', '3', '4', '5', '6'), fontsize=8)
# plt.savefig('result_1_exten_distance_time.pdf', format='pdf')
# # plt.show()
