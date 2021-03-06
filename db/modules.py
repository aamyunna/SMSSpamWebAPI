import rethinkdb as r

rcon = None
table = ""

def dbConnect(config):
    global rcon, table
    rcon = r.connect(
        db=config['db'],
        user=config['user'],
        password=config['password']
    )
    table = config['tables'][0]

def msgPusher(msgs, labels):
    for i in range(len(msgs)):
        if msgs[i].strip() == "":
            continue
        hasMsg = r.table(table).filter(r.row['message']==msgs[i]).count().run(rcon)
        if hasMsg == 0:
            r.table(table).insert({
                "message": msgs[i],
                "predicted": labels[i],
                "ham": 0,
                "spam": 0
            }).run(rcon)
    return

def msgListGet():
    res = list(r.table(table).order_by(r.row['spam'] + r.row['ham']).limit(30).run(rcon))
    return res

def classPusher(id, label):
    try:
        hasID = r.table(table).filter(r.row['id']==id).count().run(rcon)
        if hasID > 0:
            r.table(table).get(str(id)).update({
                label: r.row[label] + 1
            }).run(rcon)
    except:
        return False
    return True