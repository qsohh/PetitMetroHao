class <Position>: @def_train
    |Attribute|:
        track: # <Track>
        line # <Line>
        abs_position_track # <float>
        abs_position_line # <float>

    |Method|:
        __init__
        coord_line2track
        update_position_line
        __str__

class <Track>: @def_line
    |Attribute|:
        name # <string>
        tracklength # <float>
        line # <Line>
        node_origin # <Node>
        node_end # <Node>
        track_pre # <Track> or None
        track_next # <Track> or None
        limit_speed # <float>
        abs_direction # list <Node>
        list_trains_track 'to be modified' # <Train>
    |Method|:
        __init__

class <Station>: @def_station
    |Attribute|:
        name # <string>
        entry # <Node>
        exit # <Node>
        balise_ap # <Balise>
        balise_en # <Balise>
        balise_nn # <Balise>
        sign_ap 'to be confirmed' # <Signal> or <Node>
        sign_en 'to be confirmed' # <Signal> or <Node>
        sign_lv 'to be confirmed' # <Signal> or <Node>
        state # <string>
        stopping_time # <float>
        passing_train # <Train> or None

    |Method|:
        __init__

class <>: @def_
    |Attribute|:
         # <>

    |Method|:
        __init__