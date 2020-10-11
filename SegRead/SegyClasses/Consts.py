"""
    list four bytes fields
"""
four_bytes={"JobId","LineNumber","ReelNumber","order",
            "TRACE_SEQUENCE_LINE","TRACE_SEQUENCE_FILE","FieldRecord","TraceNumber",
            "EnergySourcePoint","CDP","CDP_TRACE","offset",
            "ReceiverGroupElevation","SourceSurfaceElevation","SourceDepth","ReceiverDatumElevation",
            "SourceDatumElevation","SourceWaterDepth","GroupWaterDepth",
            "SourceX","SourceY","GroupX","GroupY"}
trace_head_names=['TRACE_SEQUENCE_LINE', 'TRACE_SEQUENCE_FILE', 'FieldRecord', 'TraceNumber',
                  'EnergySourcePoint', 'CDP', 'CDP_TRACE', 'TraceIdentificationCode', 'NSummedTraces',
                  'NStackedTraces', 'DataUse', 'offset', 'ReceiverGroupElevation', 'SourceSurfaceElevation',
                  'SourceDepth', 'ReceiverDatumElevation', 'SourceDatumElevation', 'SourceWaterDepth', 'GroupWaterDepth',
                  'ElevationScalar', 'SourceGroupScalar', 'SourceX', 'SourceY', 'GroupX', 'GroupY', 'CoordinateUnits',
                  'WeatheringVelocity', 'SubWeatheringVelocity', 'SourceUpholeTime', 'GroupUpholeTime', 'SourceStaticCorrection',
                  'GroupStaticCorrection', 'TotalStaticApplied', 'LagTimeA', 'LagTimeB', 'DelayRecordingTime', 'MuteTimeStart',
                  'MuteTimeEND', 'TRACE_SAMPLE_COUNT', 'TRACE_SAMPLE_INTERVAL', 'GainType', 'InstrumentGainConstant',
                  'InstrumentInitialGain', 'Correlated', 'SweepFrequencyStart', 'SweepFrequencyEnd', 'SweepLength', 'SweepType',
                  'SweepTraceTaperLengthStart', 'SweepTraceTaperLengthEnd', 'TaperType', 'AliasFilterFrequency',
                  'AliasFilterSlope', 'NotchFilterFrequency', 'NotchFilterSlope', 'LowCutFrequency', 'HighCutFrequency',
                  'LowCutSlope', 'HighCutSlope', 'YearDataRecorded', 'DayOfYear', 'HourOfDay', 'MinuteOfHour',
                  'SecondOfMinute', 'TimeBaseCode', 'TraceWeightingFactor', 'GeophoneGroupNumberRoll1',
                  'GeophoneGroupNumberFirstTraceOrigField', 'GeophoneGroupNumberLastTraceOrigField', 'GapSize',
                  'OverTravel', 'spare']
