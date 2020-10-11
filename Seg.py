#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mmap import mmap
import ibm2ieee
import numpy as np

from pandas import DataFrame

from SegRead import WriteSegy
import os

import pandas
import struct
from time import time

from SegRead.SegyClasses.BinHead import BinHead
from SegRead.SegyClasses.Consts import trace_head_names
from SegRead.SegyClasses.TraceBinHead import TraceBinHead


class SegReader():


    def __init__(self):
        self.f =None
        self.path=""
        self.bin_head=None
        self.line_header = None
        self.trace_bin_head=None
        self.count_trace = 0
        self.order = "big"
        self.sample_format=4
        self.type_float = None
    def get_lineHeader(self):
        """ return sliceViewer """
        return self.line_header
    def get_bin_head(self):
        """ return bin_head """
        return self.bin_head

    def __check_order(self, b_h):
        format = struct.unpack(b'>h', b_h[24:26:])[0]
        if format in [1, 2, 3, 4, 5, 8]:
            return "big"
        elif struct.unpack(b'<h', b_h[24:26:])[0] in [1, 2, 3, 4, 5, 8]:
            return "little"
        else:
            msg = 'Unable to determine the endianness of the file. ' + \
                  'Please specify it.'
            raise Exception(msg)

    def open(self,path ):
        """ open file
        path = path for file
        """
        self.path=path
        self.f = open(self.path, "rb")
        self.f.seek(0, 0)
        self.line_header = self.f.read(3200)
        b_h = self.f.read(400)
        self.order = self.__check_order(b_h)
        self.bin_head = BinHead(b_h, self.order)
        size_file = os.path.getsize(self.path)
        coef = self.check_coef()
        self.count_trace = (size_file - 3600) / (self.bin_head.Samples * coef + 240)
        self.count_trace = int(self.count_trace)
    def read_all(self):
        """ 
        read and return all data from sgy
        input
            - 
        return:    
            data - sgy trace data
            bin_head - binary head 
            trace_head - dataFrame with trace head for data
        """
        data , trace_head=self.get_data_and_trace_heads()
        self.f.close()
        return data, self.bin_head.__dict__,trace_head
    def get_step_count(self):
        """ 
        return sample count
        input
            - 
        return:
            step count - Trace Sample Count
        """
        self.f.seek(3600, 0)
        trace_head =TraceBinHead()
        b = trace_head.get_all_trace(self.f.read(240), self.order)
        step_count = b["TRACE_SAMPLE_COUNT"]
        self.f.seek(3600, 0)
        return step_count
    def __get_step_count(self):
        """
        inner function don't call
        """
        trace_head = TraceBinHead()
        b = trace_head.get_all_trace(self.f.read(240), self.order)
        step_count = b["TRACE_SAMPLE_COUNT"]
        return step_count
        
    def get_data(self,start=0,end=None):
        """ 
        return only data
        input
            start - start number line
            end - end number line
        return:
            data - np.array with data
        """    
        self.f.seek(3600, 0)
        step_count = self.__get_step_count()
        coef = self.check_coef()
        offset =coef* step_count
        data = []
        if end == None : end =self.count_trace
        new_end=end-start
        self.f.seek(-240, 1)
        if(start!=0):
            self.f.seek((offset+240) * start,1)
            start =0
        if end ==None :
            end = self.count_trace
        if( end>self.count_trace):
            raise Exception
        for i in range(start, new_end):
            step_count=self.__get_step_count()
            print(coef,step_count)
            datas = (self.f.read(int(coef*step_count)))
            sample=self.__get_sample(coef,datas)
            data.append(sample)
        return (np.array(data))
        
    def get_data_and_trace_heads(self):
        """ 
        return data and trace heads without bin head
        input
          -
        return:
            data - np.array with data
            trace head - dataFrame with trace heads
        """    
        if( self.f == None):
            raise Exception("File not open. Use open('path')")
        self.f.seek(3600,0)
        coef = self.check_coef()
        self.trace_bin_headers=None
        offset =self.bin_head.Samples*coef
        #print(offset)
        # all={}#pandas.DataFrame(index=np.arange(0,len(Heads.TraceBinHead().__dict__.keys())),columns=Heads.TraceBinHead().__dict__.keys())
        all= np.zeros((self.count_trace, len(TraceBinHead().__dict__.keys())), dtype=np.int32)
        data = np.zeros((self.count_trace, self.bin_head.Samples), dtype=np.float32)
        trace_head = TraceBinHead()
        start_tp=time()
        for i in range(0,self.count_trace):
            # start=time()

            b=trace_head.get_all_trace(self.f.read(240), self.order)
            step_count = b["TRACE_SAMPLE_COUNT"]
            all[i]=list(b.values())
            step_count=self.bin_head.Samples
            datas = (self.f.read(coef*step_count))
            sample= self.__get_sample(coef,datas)
            data[i]=sample
            # print(time()-start)
        self.data=data
        strat = time()
        self.trace_bin_headers = pandas.DataFrame(data=all,columns=TraceBinHead().__dict__.keys())#,orient='index')

       
        return self.data ,self.trace_bin_headers
    
    def create_data_frame(self,series):
         """
            create dataFrame with input series, where columns is Trace  Heads
         input
            series with data for Trace Head
         return
            res = dataFrame 
         """
         res = pandas.DataFrame.from_dict(data=series,columns=TraceBinHead().__dict__.keys(),orient='index')
         return res
    def check_coef(self):
        """
            inner function dont call
        """
        if (self.bin_head.Format == 3):
            coef = 2
        elif (self.bin_head.Format == 6 or self.bin_head.Format == 8):
            coef = 1
        elif (self.bin_head.Format == 5):
            coef = 4
            self.type_float="IEEE"
        elif (self.bin_head.Format == 1):
            coef = 4
            self.type_float = "IBM"
        else:
            coef = 4
        return coef
    
    def delete_rows_cols(self,df):
        """
        delete none and zeros columns with dataFrame
        input:
            df - DataFrame
        return:
            df - new DataFrame
        """
    
        a = df.values
        mask = a!= 0
        m0 = mask.any(0)
        m1 = mask.any(1)
        return pandas.DataFrame(a[np.ix_(m1,m0)], df.index[m1], df.columns[m0])
    
    
    def get_line_header(self):
        """
        return line header
        input:
             -
        return:
           line_header if exist,else None
        """
        try:
              if self.line_header.decode("cp500")[0]=="C":
                  return self.line_header.decode("cp500"),1
              else:
                  return self.line_header.decode("cp1251"),0
        except Exception as e:
              return None
    def print_line_header(self):
        """
        print line header
        input:
             -
        return:
             -
        """
    
        Line_header_decode,id=self.get_line_header()
        if(id==0):
            print(Line_header_decode)
            return
        res = "1"
        for num in range(0, len(Line_header_decode)):

            if res[len(res) - 1] == " " and Line_header_decode[num] == " ":
                continue
            if (Line_header_decode[num] == "C" and Line_header_decode[num + 1].isdigit()):
                res += Line_header_decode[num]
                res += " "
                continue
            if (num == 0):
                res += " "
            res += Line_header_decode[num]
        res = res[1::]
        list_C = res.split(" C ")
        list_C.remove("")
        for i in (list_C):
            print("C" + i)
    def read_bin_trace_specefic(self, param):
        self.f.seek(3600, 0)
        all=[]
        trace_head = TraceBinHead()
        for i in range(0, self.count_trace):
              cur  = self.f.tell()
              all.append(trace_head.get_specific_trace(self.f,self.order,cur,param))
              self.f.seek(cur+240,0)
              step_count = self.bin_head.Samples
              self.f.seek(step_count*self.check_coef(),1)
        return  pandas.DataFrame(all)
    def load_all_file(self,path):
        """
            inner function dont use
        """
        with open(path ,"r+b") as f:
            self.f = mmap(f.fileno(), 0)
            self.f.seek(0, 0)
            self.line_header = self.f.read(3200)
            b_h = self.f.read(400)
            if (int.from_bytes(b_h[24:26:], "big") > 255):
                self.order = "little"
            else:
                self.order = "big"
            self.bin_head =BinHead(b_h, self.order)
            print(self.bin_head.__sizeof__())
            size_file = os.path.getsize(path)
            coef = self.check_coef()
            self.count_trace = (size_file - 3600) / (self.bin_head.Samples * coef + 240)
            self.count_trace = int(self.count_trace)
           # self.f.close()
    def __get_sample(self,coef,datas):
        """
            inner function don`t call
        """
        sample=[]
        if (coef == 2):
            sample = np.frombuffer(datas, dtype=np.int16)
        elif (coef == 4):
            if (self.order == "big"):
                if (self.type_float == "IBM"):
                    dt = np.dtype(np.uint32)
                    dt = dt.newbyteorder(">")
                    sample = np.frombuffer(datas, dtype=dt)
                    sample = ibm2ieee.ibm2float32(sample)
                else:
                    dt = np.dtype(np.float32)
                    dt = dt.newbyteorder(">")
                    sample = np.frombuffer(datas, dtype=dt)
            else:

                if (self.type_float == "IBM"):
                    dt = np.dtype(np.uint32)
                    dt = dt.newbyteorder("<")
                    sample = np.frombuffer(datas, dtype=dt)
                    sample = ibm2ieee.ibm2float32(sample)
                else:
                    dt = np.dtype(np.float32)
                    dt = dt.newbyteorder("<")
                    sample = np.frombuffer(datas, dtype=dt)
        elif (coef == 1):
            sample = np.frombuffer(datas, dtype=np.int8)
        return sample
    def get_dt(self):
        return self.bin_head.Interval


