############################################################
#
# Script for moving character to the world zero (Y-Axis ONLY)
# Compatible with MotionBuilder 2015
#
############################################################

from pyfbsdk import *

def move_character_to_zero_y():
    currChar = FBApplication().CurrentCharacter
    
    if not currChar:
        print("Warning: No current character selected.")
        return

    # Get the Hips and Reference nodes
    hipsModel = currChar.GetCtrlRigModel(FBBodyNodeId.kFBHipsNodeId)
    refModel = currChar.GetCtrlRigModel(FBBodyNodeId.kFBReferenceNodeId)
    
    if hipsModel and refModel:
        # Evaluate the scene to ensure matrix coordinates are up to date
        FBSystem().Scene.Evaluate()
        
        v_hips = FBVector3d()
        v_ref = FBVector3d()
        
        # Get Global Translation (True = Global space)
        hipsModel.GetVector(v_hips, FBModelTransformationType.kModelTranslation, True)
        refModel.GetVector(v_ref, FBModelTransformationType.kModelTranslation, True)
        
        # Calculate the offset ONLY for the Y axis
        # We leave v_ref[0] (X) and v_ref[2] (Z) completely untouched
        v_ref[1] = v_ref[1] - v_hips[1]  # Y-axis offset
        
        # Set the Reference node's new position in Global space
        refModel.SetVector(v_ref, FBModelTransformationType.kModelTranslation, True)
        
        # Re-evaluate the scene so the viewport updates immediately
        FBSystem().Scene.Evaluate()
        
        print("Success: Character's Hips moved to world zero on the Y-Axis ONLY.")
    else:
        print("Error: Could not find Hips or Reference node. Does the character have a Control Rig?")

# Run the function
move_character_to_zero_y()
