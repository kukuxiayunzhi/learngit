import ctypes

#-------------------------------------------------------------------------------------------------------------
# TOptions is the struct specifying the options for The Unscrambler engine.
#  TOptions是The Unscrambler引擎指定选项的结构。

class TOptions(ctypes.Structure):
    _fields_ = [
        ("VersionID", ctypes.c_long),
        ("ResultLevel", ctypes.c_int),
        ("OutlierDetection", ctypes.c_int),
        ("DoPretreatments", ctypes.c_int),
        ("ClassifierType", ctypes.c_int),
        ("DigitalSigned", ctypes.c_int),
        ("ApplyBiasandSlopeCorrection", ctypes.c_int),
        ("_Reserved", ctypes.c_int * 15)]

# The TMatrix is the standard matrix data structure
# Used for providing data to the engine as well as the data retrieved from the engine.
# The fields describe the dimensions of the matrix.
# The aData field points to an address in memory where the actual floating point data lives.
			   
class TMatrix(ctypes.Structure):
    _fields_ = [
        ("NumColumns", ctypes.c_long),
        ("NumRows", ctypes.c_long),
        ("NumPlanes", ctypes.c_long),
        ("aData", ctypes.POINTER(ctypes.c_float))]			   

    # to_string() method will convert the TMatrix to a printable string.
    def to_string(self, include_data = True):
        ret = "Columns : %s Rows : %s Planes : %s\n" % (self.NumColumns, self.NumRows, self.NumPlanes)
        if include_data:
            for p in range(0, self.NumPlanes):
                ret += "[ PLANE : %s]\n" % (p)
                for r  in range(0, self.NumRows):
                    for c in range(0, self.NumColumns):
                        f = self.get(c,r,p)
                        ret += " "+"{:10.4f}".format(self.get(c,r,p))+" "
                    ret += "\n"
        return ret

    # get() method returns the value of one cell in the matrix
    def get(self, x, y, z):
        return self.aData[z + self.NumPlanes * x + (self.NumPlanes * self.NumColumns) * y]
		
#-------------------------------------------------------------------------------------------------------------

class TModelInfo(ctypes.Structure):
    _fields_ = [
        ("VersionID", ctypes.c_long),
        ("CalMethod", ctypes.c_long),
        ("CompsUsed", ctypes.c_long),
        ("CompsOpt", ctypes.c_long),
        ("NumComps", ctypes.c_long),
        ("NumXVars", ctypes.c_long),           # Excluding interaction & square effects
        ("NumYVars", ctypes.c_long),
        ("NumXMappedVars", ctypes.c_long),     # Actual X variables used during model building 
        ("NumXOriginalVars", ctypes.c_long),   # The real range of X variables for model building 
        ("ModelSize", ctypes.c_long),          # shortprediction(6), fullwithoutinliers(5), fullwithinliers(4), Micro(3),mini(2),compact(1) or full(0)
        ("DigitalSigned", ctypes.c_long),      # 0 - Normal file... 1 - Signed file 
        ("NumCalSamp", ctypes.c_long),         # Number of calibration samples
        ("NumValSamp", ctypes.c_long),         # Number of validation samples
        ("_Reserved", ctypes.c_int * 12)]

#-------------------------------------------------------------------------------------------------------------

model_size = {
   0: "Full",
   1: "Compact",
   2: "Mini",
   3: "Micro",
   4: "Full with inliers",
   5: "Full without inliers",
   6: "Short prediction",
   -1: "N/A"
}

#-------------------------------------------------------------------------------------------------------------

errors = {
   0: "OK",							# No error
   1: "ERR_INTERNAL",				# Internal error (bug?)
   2: "ERR_OUTOFHANDLES",			# Cannot create object handle
   3: "ERR_OUTOFMEMORY",			# Not enough memory available
   10:"ERR_BADHANDLE",				# Bad/unknown handle specified
   11:"ERR_NULL_POINTER",			# A required pointer param. was NULL
   12:"ERR_INVALID_VALUE",			# Parameter value not valid
   13:"ERR_RESLEVEL_RANGE",			# Result level value too high or low
   14:"ERR_PRETREAT_PARAM",			# Pretreatment parameter missing/wrong
   15:"ERR_SUBMODEL_ERROR",			# Error in MSC/EMSC/OSC files
   16:"ERR_NO_PRETREAT",			# Unsupported pretreatment
   17:"ERR_PRETREAT_DATAERR",		# Insufficient data for pretreatment.
   18:"ERR_NO_OUTLIERS",			# No outliers are found
   30:"ERR_FILE_TYPE",				# Bad file type specified
   31: "ERR_FILE",					# Error during file I/O
   32: "ERR_TEMP_ERROR",			# Unable to create/access temp. location
   33: "ERR_VARNAME",				# required variable name not found
   34: "ERR_INVALID_MODEL",			# Invalid model
   35: "ERR_NO_MODEL",				# No model has been selected
   36: "ERR_PASSWORD",				# Project file failed to open due to wrong password
   37: "ERR_LOAD_FAIL",				# Project file failed to open
   38: "ERR_TRUNCATED",				# Variable name truncated due to in sufficient buffer length
   39: "ERR_NO_INITMODEL",			# Init of model failed
   40: "ERR_COMPATIBLE",			# Compatiblity issue
   41: "ERR_MISSING_MODEL",			# Model not found in the project
   49: "ERR_INPUT_MISSING",			# Input data has missing values/NaN, pretreatment cannot be done
   50: "ERR_PREDICT_FAIL",			# Prediction failed
   51: "ERR_INPUT_ERR",				# Some error in data used for prediction (mostly less no of columns)
   52: "ERR_MODEL_MATRIX_MISSING",	# required model matrix not found
   53: "ERR_MATRIX_NA",				# Required matrix is not available
   54: "ERR_MATRIX_MISSING",		# required result matrix not found
   55: "ERR_HASH_CODE",				# hash code doesnot matches
   56: "ERR_DIGITAL_SIGN",			# Not a signed file
   -1: "ERR_LIC_EXPIRED",			# License expired
   -2: "ERR_LIC_INVALID",			# Invalid license file(key)
   -3: "ERR_LIC_MISSING",			# License file missing/write error
   -4: "ERR_LIC_DATE",				# System date change detected
   999: "ERR_NOT_SUPPORTED"			# Feature not supported  
}

def rc_to_string(rc):
    if rc in errors:
        return errors[rc]
    return("Unknown error code")

calibration_methods = ["PCA", "PCR", "PLS", "MLR", "LDA", "SVM", "SVMR", "BATCH"]


