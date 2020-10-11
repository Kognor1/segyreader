import numpy as np
class TraceBinHead():
    """
    Class for storage Trace head
    """
    def __init__(self):
            self.TRACE_SEQUENCE_LINE =[0,4]
            self.TRACE_SEQUENCE_FILE=[4,4]
            self.FieldRecord=[8,4]
            self.TraceNumber=[12,4]
            self.EnergySourcePoint=[16,4]
            self.CDP=[20,4]
            self.CDP_TRACE=[24,4]

            self.TraceIdentificationCode=[28,2]
            self.NSummedTraces=[30,2]
            self.NStackedTraces=[32,2]
            self.DataUse=[34,2]

            self.offset=[36,4]
            self.ReceiverGroupElevation=[40,4]
            self.SourceSurfaceElevation=[44,4]
            self.SourceDepth=[48,4]
            self.ReceiverDatumElevation=[52,4]
            self.SourceDatumElevation =[56,4]
            self.SourceWaterDepth=[60,4]
            self.GroupWaterDepth=[64,4]

            self.ElevationScalar =[68,2]
            self.SourceGroupScalar=[70,2]
            self.SourceX=[72,4]
            self.SourceY=[76,4]
            self.GroupX=[80,4]
            self.GroupY=[84,4]

            self.CoordinateUnits=[88,2]
            self.WeatheringVelocity=[90,2]
            self.SubWeatheringVelocity=[92,2]
            self.SourceUpholeTime=[94,2]
            self.GroupUpholeTime=[96,2]
            self.SourceStaticCorrection=[98,2]

            self.GroupStaticCorrection=[100,2]
            self.TotalStaticApplied=[102,2]
            self.LagTimeA =[104,2]
            self.LagTimeB =[106,2]
            self.DelayRecordingTime=[108,2]
            self.MuteTimeStart=[110,2]

            self.MuteTimeEND=[112,2]
            self.TRACE_SAMPLE_COUNT=[114,2]
            self.TRACE_SAMPLE_INTERVAL=[116,2]
            self.GainType=[118,2]
            self.InstrumentGainConstant=[120,2]
            self.InstrumentInitialGain=[122,2]

            self.Correlated=[124,2]
            self.SweepFrequencyStart=[126,2]
            self.SweepFrequencyEnd=[128,2]
            self.SweepLength=[130,2]
            self.SweepType=[132,2]
            self.SweepTraceTaperLengthStart=[134,2]

            self.SweepTraceTaperLengthEnd =[136,2]
            self.TaperType=[138,2]
            self.AliasFilterFrequency=[140,2]
            self.AliasFilterSlope=[142,2]
            self.NotchFilterFrequency =[144,2]
            self.NotchFilterSlope =[146,2]

            self.LowCutFrequency =[148,2]
            self.HighCutFrequency =[150,2]
            self.LowCutSlope =[152,2]
            self.HighCutSlope =[154,2]
            self.YearDataRecorded =[156,2]
            self.DayOfYear =[158,2]

            self.HourOfDay=[160,2]
            self.MinuteOfHour=[162,2]
            self.SecondOfMinute =[164,2]
            self.TimeBaseCode=[166,2]
            self.TraceWeightingFactor=[168,2]
            self.GeophoneGroupNumberRoll1=[170,2]

            self.GeophoneGroupNumberFirstTraceOrigField=[172,2]
            self.GeophoneGroupNumberLastTraceOrigField=[174,2]
            self.GapSize=[176,2]
            self.OverTravel=[178,2]
            self.CDP_X=[180,4]
            self.CDP_Y=[184,4]

            self.ILINE_NO=[188,4]
            self.XLINE_NO=[192,4]
            self.ShortpointNumber=[196,4]
            self.ScalarValueForShortpointNumber=[200,2]
            self.TraceValueMeasurementUnit=[202,2]
            self.TransductionConstant=[204,6]

            self.TransductionUnits=[210,2]
            self.DeviceIdentifier=[212,2]
            self.ScalarToTimes=[214,2]
            self.SourceType=[216,2]
            self.SourceEnergyDirectionVerticalOrientation=[218,2]
            self.SourceEnergyDirectionCrossLineOrientation = [220, 2]
            self.SourceEnergyDirectionInLineOrientation = [222, 2]
            self.SourceMeasurement=[224,6]

            self.SourceMeasurementUnit=[230,2]
            self.ex1=[232,4]
            self.ex2=[236,4]


    def get_all_trace(self,list_trace_head_bin,order):
        """
            inner function to parse data from trace header
        """
        if order == "big":
            order_ = ">"
        else:
            order_ = "<"
        keys = self.__dict__.keys()
        first_part = np.frombuffer(list_trace_head_bin,dtype=order_ + "i4",count=7,offset=0)
        second_part = np.frombuffer(list_trace_head_bin,dtype=">i2",count=4,offset=28)
        third_part = np.frombuffer(list_trace_head_bin,count=8,offset=36,dtype=order_ + "i4")
        fouth_part = np.frombuffer(list_trace_head_bin,count=2,offset=68,dtype=order_ + "i2")
        fifth_part = np.frombuffer(list_trace_head_bin,count=4,offset=72,dtype=order_ + "i4")
        six_part =   np.frombuffer(list_trace_head_bin,count=46,offset=88,dtype=order_ + "i2")
        seven_part = np.frombuffer(list_trace_head_bin,count =5,offset=180,dtype=order_ + "i4")
        eight_part = np.frombuffer(list_trace_head_bin,count =2,offset=200,dtype=order_ + "i2")
        mantisa=int.from_bytes(list_trace_head_bin[204:208],byteorder=order,signed=True)
        exponent = int.from_bytes(list_trace_head_bin[208:210],byteorder=order,signed=True)
        nine_part= [mantisa * pow(10,exponent)]

        ten_part =   np.frombuffer(list_trace_head_bin,count=4,offset=210,dtype=order_ + "i2")

        elev_part=  np.frombuffer(list_trace_head_bin,count =3,offset=218,dtype=order_ + "i2")


        twelve_part=[int.from_bytes(list_trace_head_bin[224:228],byteorder=order,signed=True)*
                    pow(10,int.from_bytes(list_trace_head_bin[228:230],byteorder=order,signed=True))]

        thirteen_part=  np.frombuffer(list_trace_head_bin,count =1,offset=230,dtype=order_ + "i2")
        fourteen_part =   np.frombuffer(list_trace_head_bin,count =2,offset=232,dtype=order_ + "i4")
        data=np.concatenate((first_part, second_part, third_part, fouth_part,
                             fifth_part, six_part, seven_part, eight_part,
                             nine_part, ten_part, elev_part, twelve_part,
                             thirteen_part, fourteen_part))
        trace=dict(zip(keys,data))
        iter=0
        return trace
    def get_specific_trace(self,f,order,cur,a:list=None):
        data={}
        fields = self.__dict__
        if(a==None or (len(a)<=0)):
            return
        else:
            for i in a:
                f.seek(cur+fields[i][0],0)
                data[i]=int.from_bytes(f.read(fields[i][1]),order,signed=True)
        return data

