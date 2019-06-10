import ctypes
import camo

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Uses the PLS_McDo.unsb project file referenced in "PLS quick start tutorial" and "Prediction quick start" in The Unscrambler X 10.5 help files.
#
# Update the path to the project file below according to your installation.
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Do a simple prediction
	
def do_predict():
    predictor = ctypes.c_long(0)

    # Open the Unscrambler Engine

    try:
        engine = ctypes.CDLL('camoengine.dll')
    except:
        print("Could not load Unscrambler Engine (camoengine.dll)")
        return

    # Get a handle to the predictor
   #byfer 将predictor转成
    camo_rc = engine.olpOpenPredictor(ctypes.byref(predictor))
    if camo_rc != 0:
        print("Error opening predictor: ", camo.rc_to_string(camo_rc))
        return

    # Set some options in the predictor

    topts = camo.TOptions()
    #预处理
    topts.DoPretreatments = 1
    #分类等级
    topts.ResultLevel = 2


    camo_rc = engine.olpSetOptions(predictor, ctypes.byref(topts))

    if camo_rc != 0:
        print("Error setting options for predictor: ", camo.rc_to_string(camo_rc))
        return

    # Open the Unscrambler X project file containing the prediction model we want to use

    camo_rc = engine.olpSelectProjectFileUTF8(predictor, ctypes.c_char_p("C:/Program Files/The Unscrambler X 10.5/Data/PLS_McDo.unsb".encode('utf-8')), ctypes.c_char_p("PLS".encode('utf-8')), "")
    if camo_rc != 0:
        print("Error selecting project file: ", camo.rc_to_string(camo_rc))
        return

    # Show some information about the model
		
    tmodelinfo = camo.TModelInfo()
    camo_rc = engine.olpGetModelInfo(predictor, ctypes.byref(tmodelinfo))
    if camo_rc != 0:
        print("Error getting model info: ", camo.rc_to_string(camo_rc))
        return

    print("Calibration method = ", camo.calibration_methods[tmodelinfo.CalMethod - 1])
    print("Components used = ", tmodelinfo.CompsUsed)
    print("Components opt = ", tmodelinfo.CompsOpt)
    print("Components num = ", tmodelinfo.NumComps)
    print("X vars = ", tmodelinfo.NumXVars)
    print("Y vars = ", tmodelinfo.NumYVars)
    print("X mapped vars: ", tmodelinfo.NumXMappedVars)
    print("Model size = ", camo.model_size[tmodelinfo.ModelSize])

	# This is the sample from which we want to predict Energy (kJ/g)
    #              Protein (%), Carbohydrates (%), Fat (%), Saturated Fat (%) 
    food_sample = [ 12.48,         19.62,          11.0,       4.02]
	
    tm = camo.TMatrix()
    tm.NumColumns = len(food_sample)
    tm.NumRows = 1
    tm.NumPlanes = 1

    # Prepare the sample to be predicted (convert the Python array to a TMatrix struct)
	
    data = []
    tm.aData = (ctypes.c_float * (tm.NumColumns * 1 * 1))(*data)
    for x in range(0, tm.NumColumns):
        tm.aData[x] = food_sample[x]

    # Call the Unscrambler Engine to make the prediction
		
    camo_rc = engine.olpPredict(predictor, ctypes.byref(tm))
    if camo_rc != 0:
        print("Error doing predict: ", camo.rc_to_string(camo_rc))
        return

    # Get the result of the prediction
		
    ypredicted = camo.TMatrix()
    camo_rc = engine.olpGetResultMatrix(predictor, ctypes.c_int(6), ctypes.byref(ypredicted))	# 6 = YPREDICTED (see camoengine.h)
    if camo_rc != 0:
        print("Failed to get the YPREDICTED result matrix: ", camo.rc_to_string(camo_rc))
        return

    print("Predicted values: \r\n", ypredicted.to_string())

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
		
do_predict()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
