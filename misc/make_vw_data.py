ids = ''
fout = open("data.tsv", 'w+')
line_id = 0
for line in open("data_inclmissing.tsv"):
    line_id += 1
    if ids=='':
        ids = line.strip('\n').split('\t')
        continue
    tok = line.strip('\n').split('\t')
    id = int(tok[0].strip("\""))
    idx = 1
    if len(ids) != len(tok):
        print line_id
        print len(ids), len(tok)
    for t in tok[2:]:
        idx += 1
        if t == 'NA':
            continue
        t = t.strip("\"")
        if '-' in t:
            continue
        #if float(t.strip("\"")) < 0:
        #    continue
        fout.write("%d\t%s\t%s\n" % (id, ids[idx].strip("\""), t))
fout.close()

fout_gpa = open("vw_gpa.dat", 'w+')
fout_grit = open("vw_grit.dat", 'w+')
fout_attc = open("vw_attachment.dat", 'w+')
fout_evic = open("vw_evicted.dat", 'w+')
fout_colp = open("vw_collegeplans.dat", 'w+')

ids = ''
cur = None
cur_str = ''
outcomes = {}
for line in open("train_outcomes.csv"):
    if ids == '':
        ids = line.strip().split(',')
        continue
    tok = line.strip().split(',')
    idx = int(tok[0].strip("\""))
    outcomes[idx] = (float(tok[1]), float(tok[2]), float(tok[3]), \
        1 if int(tok[4]) == 1 else -1, \
        1 if int(tok[5]) == 1 else -1)

def write_out(idx, features):
    if idx not in outcomes:
        return
    f = "|MetricFeatures%s" % features[0]
    if len(features) > 1:
        for i in range(1,len(features)):
            f += ' ' + features[i]
    f += '\n'

    fout_gpa.write("%f %s" % (outcomes[idx][0], f))
    fout_grit.write("%f %s" % (outcomes[idx][1], f))
    fout_attc.write("%f %s" % (outcomes[idx][2], f))
    fout_evic.write("%d %s" % (outcomes[idx][3], f))
    fout_colp.write("%d %s" % (outcomes[idx][4], f))
    
    
ids = ''
cur = None
cur_str = ['']
lc = 0
for line in open("data.tsv"):
    lc +=1
    #if lc > 10000:
    #    break
    if ids == '':
        ids = line.strip().split(',')
        continue
    
    tok = line.strip('\n').split('\t')
    idx = int(tok[0])

    if idx != cur:
        if cur_str != ['']:
            print cur
            write_out(cur, cur_str)
        cur = idx
        cur_str = ['']

    try:
        val = float(tok[2])
        cur_str[0] += ' ' + tok[1] + ":" + tok[2]
    except:
        if tok[2] != '':
            cur_str.append('|%s %s' % (tok[1], tok[2]))

write_out(cur, cur_str)
