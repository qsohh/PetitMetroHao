import matplotlib.pyplot as plt


def parameter_plot(trs, number_nodes, platform_length=70.):
    added_position = []
    all_position = []
    length = 0.
    length_tot = 0.
    ind = int(number_nodes/2)
    for ele in trs[0:ind]:
        added_position.append(length)
        all_position.append(length_tot)
        length += ele.tracklength
        length_tot += ele.tracklength
    length -= platform_length
    for ele in trs[ind:]:
        added_position.append(length)
        all_position.append(length_tot)
        length -= ele.tracklength
        length_tot += ele.tracklength
    added_position[ind-1] += platform_length
    return added_position, all_position


def plot_position_time(TT, trains, trs, added_position, title, save_im=False):
    Ptrain = []
    for i in range(len(trains)):
        Ptrain.append([])
    for i in range(len(TT)):
        for j in range(len(trains)):
            ind = trs.index(trains[j].PP[i].track)
            if ind < 17:
                Ptrain[j].append(added_position[ind] +
                                 trains[j].PP[i].abs_position_track)
            else:
                Ptrain[j].append(added_position[ind] -
                                 trains[j].PP[i].abs_position_track)
    plt.figure()
    # for i in range(len(trains)):
    for i in range(len(trains)):
        plt.plot(TT, Ptrain[i])
    # plt.axhspan(10, 60, 0, maxtime, fc='gray')
    # plt.axhspan(945, 1015, 0, maxtime, fc='gray')
    # plt.axhspan(2100, 2150, 0, maxtime, fc='gray')
    plt.xlabel('time (s)')
    plt.ylabel('position (m)')
    plt.title(title)
    # plt.legend(('0', '1', '2', '3', '4', '5', '6'), fontsize=8)
    # plt.show()
    plt.savefig(fname='%sposition_time.pdf' % title, format="pdf")


def plot_distance_time(TT, trains, trs, all_position, title, save_im=False):
    Dtrain = []
    added_to_dis = []
    DiffTrain = []
    for i in range(len(trains)):
        Dtrain.append([])
        DiffTrain.append([])
        ind = trs.index(trains[i].PP[0].track)
        added_to_dis.append(all_position[ind])

    for i in range(len(TT)):
        for j in range(len(trains)):
            ind = trs.index(trains[j].PP[i].track)
            Dtrain[j].append(trains[j].DD[i] + added_to_dis[j])
            if j == 0:
                continue
            else:
                DiffTrain[j].append(Dtrain[j][i]-Dtrain[j-1][i])

    plt.figure()
    # for i in range(len(trains)):
    for i in range(len(trains)):
        plt.plot(TT, Dtrain[i])
    # plt.axhspan(10, 60, 0, maxtime, fc='gray')
    # plt.axhspan(945, 1015, 0, maxtime, fc='gray')
    # plt.axhspan(2100, 2150, 0, maxtime, fc='gray')
    plt.xlabel('time (s)')
    plt.ylabel('distance (m)')
    plt.title(title + ' distance-time')
    # plt.legend(('0', '1', '2', '3', '4', '5', '6'), fontsize=8)

    plt.figure()
    for i in range(len(trains) - 1):
        plt.plot(TT, DiffTrain[i+1])
    plt.xlabel('time (s)')
    plt.ylabel('distance (m)')
    plt.title(title + ' distance between two trains')
    plt.savefig(fname='%sdistance_time.pdf' % title, format="pdf")
    # plt.show()


def plot_speed_time(TT, trains, title, save_im=False):
    plt.figure()
    for i in range(len(trains)):
        plt.plot(TT, trains[i].VV)
    plt.xlabel('times (s)')
    plt.ylabel('speed (m/s)')
    plt.title(title)

    plt.savefig(fname='%sspeed_time.pdf' % title, format="pdf")
    # plt.show()


# def plot_speed_distance(trains, Dtrain, title, save_im=False):
