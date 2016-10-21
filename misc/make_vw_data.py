print "reading in training outcomes"
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
        1 if int(tok[4]) == 1 else 0, \
        1 if int(tok[5]) == 1 else 0)


print "setting up vw files"
fout_gpa = open("vw_gpa.dat", 'w+')
fout_grit = open("vw_grit.dat", 'w+')
fout_attc = open("vw_attachment.dat", 'w+')
fout_evic = open("vw_evicted.dat", 'w+')
fout_colp = open("vw_collegeplans.dat", 'w+')
fout2_gpa = open("vw_gpa_test.dat", 'w+')
fout2_grit = open("vw_grit_test.dat", 'w+')
fout2_attc = open("vw_attachment_test.dat", 'w+')
fout2_evic = open("vw_evicted_test.dat", 'w+')
fout2_colp = open("vw_collegeplans_test.dat", 'w+')
def write_out(idx, features):
    f = "|MetricFeatures%s" % features[0]
    #f = "|m%s" % features[0]
    if len(features) > 1:
        for i in range(1,len(features)):
            f += ' ' + features[i]
    f += '\n'
    
    if idx not in outcomes:
        fout2_gpa.write("0 %s" % f)
        fout2_grit.write("0 %s" % f)
        fout2_attc.write("0 %s" % f)
        fout2_evic.write("0 %s" % f)
        fout2_colp.write("0 %s" % f)

    else:
        fout_gpa.write("%f %s" % (outcomes[idx][0], f))
        fout_grit.write("%f %s" % (outcomes[idx][1], f))
        fout_attc.write("%f %s" % (outcomes[idx][2], f))
        fout_evic.write("%d %s" % (outcomes[idx][3], f))
        fout_colp.write("%d %s" % (outcomes[idx][4], f))
        

print "processing training data"
ids = ''
for line in open("data_inclmissing.tsv"):
    if ids=='':
        ids = line.strip('\n').split('\t')
        continue
    tok = line.strip('\n').split('\t')
    id = int(tok[0].strip("\""))
    print "child", id
    idx = 1
    cur_str = ['']
    for t in tok[2:]:
        idx += 1

        # remove na and negative-valued covariates
        if t == 'NA':
            continue
        t = t.strip("\"")
        if '-' in t:
            continue
        
        # add the covariat in
        try:
            val = float(t)
            cur_str[0] += ' ' + ids[idx].strip("\"") + ":" + t
        except:
            if t != '':
                t = t.replace(':', ' ')
                cur_str.append('|%s %s' % (ids[idx].strip("\""), t))

    write_out(id, cur_str)
