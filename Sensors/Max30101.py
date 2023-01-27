





class HeartRate(object):
    """
    HeartRate
    
        :return: The Heart Beat device object.
        :rtype: Object
    """
    def __init__(self):
        
        self.IR_AC_Max = 20
        self.IR_AC_Min = -20

        self.IR_AC_Signal_Current = 0
        self.IR_AC_Signal_Previous = 0
        self.IR_AC_Signal_min = 0
        self.IR_AC_Signal_max = 0
        self.IR_Average_Estimated = 0

        self.positiveEdge = 0
        self.negativeEdge = 0
        self.ir_avg_reg = 0

        self.cbuff = list(range(32))
        self.offset = 0

        self.FIRCoeffs = [172, 321, 579, 927, 1360, 1858, 2390, 2916, 3391, 3768, 4012, 4096]

    # Average DC Estimator
    def averageDCEstimator(self,p, x):
        self.ir_avg_reg = p
        self.ir_avg_reg += ( ( (x << 15) - self.ir_avg_reg) >> 4)
        return (self.ir_avg_reg >> 15)

    # Integer multiplier
    def mul16(self,x, y):
        return (x * y)
        
    # Low Pass FIR Filter
    def lowPassFIRFilter(self,din):
        
        self.cbuff[self.offset] = din

        z = self.mul16(self.FIRCoeffs[11], self.cbuff[(self.offset - 11) & 0x1F])
      
        for i in range(0,11):
            z += self.mul16(self.FIRCoeffs[i], self.cbuff[(self.offset - i) & 0x1F] + self.cbuff[(self.offset - 22 + i) & 0x1F])

        self.offset += 1
        self.offset %= 32 #Wrap condition

        return (z >> 15)

    def getDCE(self):
        return self.IR_Average_Estimated

    #  Heart Rate Monitor functions takes a sample value
    #  Returns True if a beat is detected
    #  A running average of four samples is recommended for display on the screen.
    def checkForBeat(self, sample):
        beatDetected = False
        
        #  Save current state
        self.IR_AC_Signal_Previous = self.IR_AC_Signal_Current
      
        #This is good to view for debugging
        #Serial.print("Signal_Current: ")
        #Serial.println(self.IR_AC_Signal_Current)

        # Process next data sample
        self.IR_Average_Estimated = self.averageDCEstimator(self.ir_avg_reg, sample)
        self.IR_AC_Signal_Current = self.lowPassFIRFilter(sample - self.IR_Average_Estimated)

        # Detect positive zero crossing (rising edge)
        if ((self.IR_AC_Signal_Previous < 0) & (self.IR_AC_Signal_Current >= 0)):
            self.IR_AC_Max = self.IR_AC_Signal_max #Adjust our AC max and min
            self.IR_AC_Min = self.IR_AC_Signal_min

            self.positiveEdge = 1
            self.negativeEdge = 0
            self.IR_AC_Signal_max = 0

            #if ((self.IR_AC_Max - self.IR_AC_Min) > 100 & (self.IR_AC_Max - self.IR_AC_Min) < 1000)
            if ((self.IR_AC_Max - self.IR_AC_Min) > 20 & (self.IR_AC_Max - self.IR_AC_Min) < 1000):
                #Heart beat!!!
                beatDetected = True

        # Detect negative zero crossing (falling edge)
        if ((self.IR_AC_Signal_Previous > 0) & (self.IR_AC_Signal_Current <= 0)):
            self.positiveEdge = 0
            self.negativeEdge = 1
            self.IR_AC_Signal_min = 0

        # Find Maximum value in positive cycle
        if (self.positiveEdge & (self.IR_AC_Signal_Current > self.IR_AC_Signal_Previous)):
            self.IR_AC_Signal_max = self.IR_AC_Signal_Current

        # Find Minimum value in negative cycle
        if (self.negativeEdge & (self.IR_AC_Signal_Current < self.IR_AC_Signal_Previous)):
            self.IR_AC_Signal_min = self.IR_AC_Signal_Current
      
        return beatDetected