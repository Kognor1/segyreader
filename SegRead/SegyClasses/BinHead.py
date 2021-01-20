class BinHead:
    """
    Class for storage bin head
    """

    def __init__(self, list_header_bin, order):
        self.JobId = int.from_bytes(list_header_bin[0:4:], order, signed=True)
        self.LineNumber = int.from_bytes(list_header_bin[4:8:], order, signed=True)
        self.ReelNumber = int.from_bytes(list_header_bin[8:12:], order, signed=True)
        self.Traces = int.from_bytes(list_header_bin[12:14:], order, signed=True)
        self.AuxTraces = int.from_bytes(list_header_bin[14:16:], order, signed=True)
        self.Interval = int.from_bytes(list_header_bin[16:18:], order, signed=True)
        self.IntervalOriginal = int.from_bytes(list_header_bin[18:20:], order, signed=True)
        self.Samples = int.from_bytes(list_header_bin[20:22:], order)
        self.SamplesOriginal = int.from_bytes(list_header_bin[22:24:], order, signed=True)
        self.Format = int.from_bytes(list_header_bin[24:26:], order, signed=True)
        self.EnsembleFold = int.from_bytes(list_header_bin[26:28:], order, signed=True)  # ?
        self.SortingCode = int.from_bytes(list_header_bin[28:30:], order, signed=True)
        self.VerticalSum = int.from_bytes(list_header_bin[30:32:], order, signed=True)
        self.SweepFrequencyStart = int.from_bytes(list_header_bin[32:34:], order, signed=True)
        self.SweepFrequencyEnd = int.from_bytes(list_header_bin[34:36:], order, signed=True)
        self.SweepLength = int.from_bytes(list_header_bin[36:38:], order, signed=True)
        self.Sweep = int.from_bytes(list_header_bin[38:40:], order, signed=True)
        self.SweepChannel = int.from_bytes(list_header_bin[40:42:], order, signed=True)
        self.SweepTaperStart = int.from_bytes(list_header_bin[42:44:], order, signed=True)
        self.SweepTaperEnd = int.from_bytes(list_header_bin[44:46:], order, signed=True)
        self.Taper = int.from_bytes(list_header_bin[46:48:], order, signed=True)
        self.CorrelatedTraces = int.from_bytes(list_header_bin[48:50:], order, signed=True)
        self.BinaryGainRecovery = int.from_bytes(list_header_bin[50:52:], order, signed=True)
        self.AmplitudeRecovery = int.from_bytes(list_header_bin[52:54:], order, signed=True)
        self.MeasurementSystem = int.from_bytes(list_header_bin[54:56:], order, signed=True)
        self.ImpulseSignalPolarity = int.from_bytes(list_header_bin[56:58:], order, signed=True)
        self.VibratoryPolarity = int.from_bytes(list_header_bin[58:60:], order, signed=True)
        self.order = int.from_bytes(list_header_bin[96:100:], "big", signed=True)
        self.Spare = int.from_bytes(list_header_bin[60:401:], order, signed=True)
