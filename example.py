import SegRead as s
from time import time

start = time()
ss = s.Seg.SegReader()
ss.open("test.sgy")
data,head,trace_head =ss.read_all()
print(data)
print(trace_head)
print(head)
print(time()-start)


#Data = numpy ndarray
#SegyTraceHeaders = это хедеры трасс. Должен быть либо словарём вида {"Имя поля": numpy.array} размерность, либо dataframe где имя колонок - результат функции get_names()
# из этой библиотеки, а значение - ndarray
#SegyHeader= Хедер всего файла словарь вида {"Поле":value}
#order= big-endian или little-endian
#SampleFormat=тип данных (int,float, вид записи, посмотреть файл с описанием формата, и выбрать нужный). По умолчанию float. Это нужно толлько для хедера.
#данные записываются в том формате в котором они. Если они np.float32, то и будут 32битными, даже если sample format поставить int
#Dt - Шаг дискретизации
#Очень долго создаётся dataframe из данных если передавать словарь, это уже зависит от pandas, никак не ускорю
s.Seg.write("new.sgy",Data=data,SegyTraceHeaders=({"TRACE_SEQUENCE_LINE":trace_head["TRACE_SEQUENCE_LINE"]}),dt=1000)#,SegyHeader=ss.get_bin_head(),order=ss.order,SampleFormat=ss.sample_format,dt=1000)