from pyfbsdk import *
from pyfbsdk_additions import *

# Declare UI globals
is_Tpose = None
is_DOF = None

def getGlobalRotate(lModel):
    globalRotation = FBVector3d()
    lModel.GetVector(globalRotation, FBModelTransformationType.kModelRotation, True)
    return globalRotation

def tPoseAngleMatch(in_vector):
    '''
    This function is helping rig to Tpose-ish. Select joints and execute it.
    '''
    # Create a new vector to return, avoiding modifying the object in place incorrectly
    out_vector = FBVector3d()
    
    for i in range(3): # Loop through X, Y, Z (0, 1, 2)
        angle = in_vector[i]
        negative = False
        
        if angle < 0:
            angle = abs(angle)
            negative = True
            
        if 0 <= angle < 45:
            angle = 0
        elif 45 <= angle < 135:
            angle = 90
        elif 135 <= angle < 225:
            angle = 180
        elif 225 <= angle < 315:
            angle = 270
        elif 315 <= angle:
            angle = 360
            
        if negative:
            angle = -angle
            
        out_vector[i] = angle
        
    return out_vector

def reurn_HIK_link_model(lCharacter, idName):
    nameId = 'kFB' + idName + 'NodeId'
    
    # getattr is the safest way to get enum values by string in MoBu 2015
    if hasattr(FBBodyNodeId, nameId):
        node_id = getattr(FBBodyNodeId, nameId)
        model = lCharacter.GetModel(node_id)
        if model:
            return model 

def DOF(lModel, values):
    attrs = ['RotationActive', 'RotationMaxX', 'RotationMaxY',
             'RotationMaxZ', 'RotationMinX', 'RotationMinY', 'RotationMinZ']
    
    for at, v in zip(attrs, values):
        # Convert 1/0 to True/False for RotationActive
        if at == 'RotationActive':
            v = bool(v)
            
        # Use setattr instead of exec(). It is safer, faster, and works in Python 2.7
        setattr(lModel, at, v)

def DOF_Character(lCharacter, Nodes, RotationActive=1, RotationMaxX=1, RotationMaxY=1, RotationMaxZ=0, RotationMinX=1, RotationMinY=1, RotationMinZ=0):
    for name in Nodes:
        for side in ['Left', 'Right']:
            values = [RotationActive, RotationMaxX, RotationMaxY,
                      RotationMaxZ, RotationMinX, RotationMinY, RotationMinZ]
            idName = side + name
            model = reurn_HIK_link_model(lCharacter, idName)
            if model:
                DOF(model, values)

def T_Pose(lCharacter, is_Finger):
    body = ['Hip', 'Knee', 'Ankle', 'Foot', 'Shoulder', 'Elbow', 'Wrist']
    if is_Finger:
        lThumb = [finger + id for finger in ['Thumb'] for id in ['B', 'C', 'D']]
        fingers = [finger + id for finger in ['Index', 'Middle', 'Ring', 'Pinky'] for id in ['A', 'B', 'C', 'D']]
        body = body + lThumb + fingers
        
    for name in body:
        for side in ['Left', 'Right']:
            node = reurn_HIK_link_model(lCharacter, side + name)
            if node:
                FBSystem().Scene.Evaluate()
                tPoseAngle = tPoseAngleMatch(getGlobalRotate(node))
                node.SetVector(tPoseAngle, FBModelTransformationType.kModelRotation)
    FBSystem().Scene.Evaluate()

def get_select_models():
    lModelList = FBModelList()
    FBGetSelectedModels(lModelList)
    if len(lModelList) > 0:
        return lModelList

def btn_execute_selection(control, event):
    '''select joints and execute this function'''
    lModelList = get_select_models()
    if lModelList:
        for lModel in lModelList:
            if is_Tpose.State:
                tPoseAngle = tPoseAngleMatch(getGlobalRotate(lModel))
                lModel.SetVector(tPoseAngle, FBModelTransformationType.kModelRotation)
            if is_DOF.State:
                DOF(lModel, [1, 1, 1, 0, 1, 1, 0])

def main():
    global is_Tpose, is_DOF
    
    # Tool creation will serve as the hub for all other controls
    t = FBCreateUniqueTool('Quick T-pose Tool')
    t.StartSizeX = 200
    t.StartSizeY = 160

    # Create a button that is left justify
    x = FBAddRegionParam(10, FBAttachType.kFBAttachLeft, "")
    y = FBAddRegionParam(10, FBAttachType.kFBAttachTop, "")
    w = FBAddRegionParam(-10, FBAttachType.kFBAttachRight, "")
    h = FBAddRegionParam(-10, FBAttachType.kFBAttachBottom, "")
    t.AddRegion("top", "top", x, y, w, h)
    
    box = FBVBoxLayout(FBAttachType.kFBAttachTop)

    hStrip = FBHBoxLayout(FBAttachType.kFBAttachLeft)
    vStrip = FBVBoxLayout(FBAttachType.kFBAttachTop)
    hStrip.Add(vStrip, 20)
    vStrip = FBVBoxLayout(FBAttachType.kFBAttachTop)
    
    is_Tpose = FBButton()
    is_Tpose.Caption = 'T-Pose'
    is_Tpose.Style = FBButtonStyle.kFBCheckbox
    is_Tpose.State = True
    vStrip.Add(is_Tpose, 20)

    is_DOF = FBButton()
    is_DOF.Caption = 'DOF'
    is_DOF.Style = FBButtonStyle.kFBCheckbox
    is_DOF.State = False
    vStrip.Add(is_DOF, 20)

    hStrip.AddRelative(vStrip, 0.5)
    box.Add(hStrip, 60)

    bnt03 = FBButton()
    bnt03.Caption = "Execute Selected"
    bnt03.Justify = FBTextJustify.kFBTextJustifyCenter
    # Fixed typo: 'wight=30' to nothing (MoBu 2015 doesn't accept kwarg here)
    box.Add(bnt03, 30) 
    bnt03.OnClick.Add(btn_execute_selection)

    t.SetControl("top", box)
    ShowTool(t)

# MoBu 2015 uses '__builtin__'. MoBu 2022+ uses 'builtins'
if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
