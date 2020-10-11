from time import time

import numpy as np
from math import pow
import decimal

import pandas
from pandas import DataFrame

from SegRead.SegyClasses.BinHead import BinHead
from SegRead.SegyClasses.Consts import four_bytes, trace_head_names
from SegRead.SegyClasses.TraceBinHead import TraceBinHead


class WriteSegy():
    def __init__(self, filename, data,
        trace_headers = pandas.DataFrame(), bin_head = None,
        text_head = None, order = "big", dt = 1000,
        sample_format = 3):
        """

        :param filename - filename for write:
        :param data - main data:
        :param trace_headers - trace Headers:
        :param bin_head - bin head:
        :param text_head - text head:
        :param order - "big/little":
        :param dt:
        :param sample_format:
        """
        self.filename = filename
        self.data = data
        self.trace_headers = trace_headers
        self.bin_head = bin_head
        self.text_head = text_head
        self.order = order
        self.dt = dt
        self.sample_format = sample_format
        self.write()

    def __check_trace_head(self):
        if (isinstance(self.trace_headers, dict)):
            self.trace_headers = self.__create_head_traces(self.trace_headers)
        elif (isinstance(self.trace_headers, pandas.DataFrame)):
            pass
        else:
            raise Exception("Not definde type")
        return True

    def __check_bin_head(self):
        if (self.bin_head == None):
            self.bin_head = BinHead(bytearray(400), self.order)

        else:
            self.bin_head = self.bin_head
        self.bin_head.Interval = self.dt
        self.bin_head.Samples = len(self.data[0])
        self.bin_head.Format = self.sample_format
        return True

    def __validate_all_data(self):
        print("TraceHeader is valid: " + str(self.__check_trace_head()))
        print("BinHead is valid: " + str(self.__check_bin_head()))

    def __prepare_trace_head(self):
        if (self.trace_headers.empty):
            self.trace_headers = self.__get_null_trace()
        else:
            self.trace_headers = self.trace_headers
        self.trace_headers.TRACE_SAMPLE_COUNT = len(self.data[0])

    def __create_head_traces(self, dict):
        """
                create dataframe from dict with head trace
            inner:
                dict - dict with data
            return:
                new dataFrame
            """
        heads = DataFrame(dict, columns=trace_head_names)
        heads = heads.fillna(0)
        return heads

    def __prepare_all_data(self):
        self.__prepare_trace_head()

    def __get_null_trace(self):
        """
                inner function
            """
        ar = TraceBinHead()
        for i, k in ar.__dict__.items():
            ar.__dict__[i] = 0
        return ar

    def __ret_coef(self):
        """
               inner function don`t call
           """
        if (self.sample_format == 3):
            coef = 2
        elif (self.sample_format == 6 or self.sample_format == 8):
            coef = 1
        elif (self.sample_format == 5):
            coef = 4
            type_float = "IEEE"
        elif (self.sample_format == 1):
            coef = 4
            type_float = "IBM"
        else:
            coef = 4
        return coef

    def write(self):

        """
              write segy file
          input:
              filename - name new file
              Data - segy data for write
              SegyTraceHeaders - trace heads for write
              SegyHeader - bin head for write
              text_head - text header
              order - byte order "little" or "big"
              dt - delta time
              SampleFormat - sample format for write
          return :
                  None
                  create new file in directory
          """
        file = open(self.filename, "wb")
        self.__validate_all_data()
        self.__prepare_all_data()
        self.__write_text_header(file)

        self.__write_bin_head(file, self.bin_head, self.order)
        coef=self.__ret_coef()

        start = time()
        self.__write_trace_head_and_data(file,coef)
        print("Write time: "+ str(time()-start))
        # df_dict = segyTraceHeaders.to_dict(orient='index')

    def __write_trace_head_and_data(self,file,coef):
        all_c = bytearray()
        for i in range(0, len(self.data)):
            if (i != 0 and i % 1000000 == 0):
                file.write(all_c)
                all_c = bytearray()
            if (self.trace_headers.empty):
                b = self.__write_trace_head_empty(file, self.trace_headers, self.order)
            else:
                b = self.__write_one_trace_head(file, self.trace_headers.iloc[i], self.order)
            a = self.__write_data(file, self.data[i], coef, self.order)
            try:
                all_c += b + a
            except Exception as e:
                print(e)
        file.write(all_c)



    def __write_bin_head(self, filename, bin_head, order):
        """
             inner function to write binHead, don`t call
         """
        bytes = 0
        for i, k in bin_head.__dict__.items():
            if (i == "order"):
                continue
            if (i == "Spare"):
                filename.write(k.to_bytes(340, order))
                bytes += 340
                continue
            if (i in four_bytes):
                filename.write(k.to_bytes(4, order))
                bytes += 4
            else:
                filename.write(k.to_bytes(2, order))
                bytes += 2

    def __write_trace_head_empty(self, file, trace_headers, order):
        """
               inner function to write TraceHeadEmpty, don`t call
           """
        a = bytearray(240)
        for i, k in trace_headers.__dict__.items():

            if (i == "spare"):
                a.extend(int(k).to_bytes(60, order, signed=True))
                continue
            if (i in four_bytes):
                a.extend(int(k).to_bytes(4, order, signed=True))
            else:
                a.extend(int(k).to_bytes(2, order, signed=True))

        return a

    def __write_data(self, file,Data,coef,order):
        """
               inner function  write  data in new segy file
            """
        res = None
        if ("int" in str(type(Data[0]))):
            return (Data.astype(int).tobytes())
        elif ("float" in str(type(Data[0]))):
            if (order == "big"):
                res = Data.astype(">f").tobytes()
            else:
                res = Data.astype("<f").tobytes()
        return res

    def _parse_difficult_value(self,num,order):
        if num != "0":
            if (num.find("e") == -1):
                mantisa = int(float(num)).to_bytes(4, order, signed=True)
                power = int(float(0)).to_bytes(2, order, signed=True)
            else:
                mantisa = int(float(num[0:num.find("e")])).to_bytes(4, order, signed=True)
                power = int(float(num[num.find("e") + 2:])).to_bytes(2, order, signed=True)
        else:
            mantisa = int(0).to_bytes(4, order, signed=True)
            power = int(0).to_bytes(2, order, signed=True)
        return mantisa,power

    def __write_one_trace_head(self, file, Headers, order):
        """
                inner function to write TraceHead, don`t call
            """
        order_ = ">"
        a = bytes()
        if order == "big":
            order_ = ">"
        else:
            order_ = "<"

        data = list(Headers.values)
        first_part = np.array(data[0:7], dtype=order_ + "i4").tobytes()
        second_part = np.array(data[7:11], dtype=">i2").tobytes()
        third_part = np.array(data[11:19], dtype=order_ + "i4").tobytes()

        fouth_part = np.array(data[19:21], dtype=order_ + "i2").tobytes()
        fifth_part = np.array(data[21:25], dtype=order_ + "i4").tobytes()

        six_part = np.array(data[25:71], dtype=order_ + "i2").tobytes()
        seven_part = np.array(data[71:76], dtype=order_ + "i4").tobytes()
        eight_part = np.array(data[76:78], dtype=order_ + "i2").tobytes()

        num = format(decimal.Decimal(int(data[78])))
        mantisa,power = self._parse_difficult_value(num,order)
        nine_part = mantisa + power

        ten_part = np.array(data[79:83], dtype=order_ + "i2").tobytes()
        elev_part = np.array(data[83:86], dtype=order_ + "i2").tobytes()

        num = format(decimal.Decimal(int(data[86])))
        mantisa, power = self._parse_difficult_value(num, order)
        twelve_part = mantisa + power

        thirteen_part = np.array(data[87], dtype=order_ + "i2").tobytes()
        fourteen_part = np.array(data[88:], dtype=order_ + "i4").tobytes()
        a = first_part + second_part + third_part + fouth_part + fifth_part + six_part
        a += seven_part + eight_part + nine_part + ten_part + elev_part + twelve_part + thirteen_part + fourteen_part
        return a

    def __write_text_header(self, file):
        if (self.text_head != None):
            file.write(self.text_head)
        else:
            file.write(bytearray(3200))

