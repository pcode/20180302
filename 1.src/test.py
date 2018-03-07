from models.d_room import opt_room

if __name__ == '__main__':

    recs = opt_room.GetRowsByDbWhere()
    for rec in recs:
        print rec