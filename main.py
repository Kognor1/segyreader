import SegRead as s
from time import time
ss = s.Seg.SegReader()
start =time()
for i in range(1,20):
    ss.open("test_segy_data/sofi3d_hti_vy.sgy.shot"+str(i))
    data, head, trace_head = ss.read_all()
    trace_head["TRACE_SEQUENCE_LINE"]=trace_head["TRACE_SEQUENCE_LINE"]
    s.Seg.WriteSegy.WriteSegy("new/new.sgy" + str(i), data, bin_head=ss.get_bin_head(), trace_headers=trace_head, order="little")

print(time()-start)
