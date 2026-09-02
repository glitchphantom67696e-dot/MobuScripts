############################################################
#
# Script for moving character to the world zero
# Updated for MotionBuilder 2015 compatibility
#
# Original Author: Sergey Solohin (Neill3d)
# Ported/Modernized for MoBu 2015
############################################################

from pyfbsdk import *

def move_character_to_zero():
    currChar = FBApplication().CurrentCharacter
    
    if not currChar:
        print("Warning: No current character selected.")
        return

    # In MoBu 2015, it is safer to get the Hips via the BodyNodeId 
    # rather than EffectorId, as it works in both IK and FK modes.
    hipsModel = currChar.GetCtrlRigModel(FBBodyNodeId.kFBHipsNodeId)
    refModel = currChar.GetCtrlRigModel(FBBodyNodeId.kFBReferenceNodeId)
    
    if hipsModel and refModel:
        # Evaluate the scene to ensure we get the most accurate, up-to-date coordinates
        FBSystem().Scene.Evaluate()
        
        v_hips = FBVector3d()
        v_ref = FBVector3d()
        
        # Get Global Translation (True at the end specifies Global space)
        hipsModel.GetVector(v_hips, FBModelTransformationType.kModelTranslation, True)
        refModel.GetVector(v_ref, FBModelTransformationType.kModelTranslation, True)
        
        # Calculate the offset. 
        # We subtract the hips world position from the reference world position on X and Z.
        # We leave Y alone so the character doesn't get pushed through the floor.
        v_ref[0] = v_ref[0] - v_hips[0]
        v_ref[2] = v_ref[2] - v_hips[2]
        
        # Set the Reference node's new position in Global space
        refModel.SetVector(v_ref, FBModelTransformationType.kModelTranslation, True)
        
        # Re-evaluate the scene so the viewport updates immediately
        FBSystem().Scene.Evaluate()
        
        print("Success: Character moved to world zero.")
    else:
        print("Error: Could not find Hips or Reference node. Does the character have a Control Rig?")

# Run the function
move_character_to_zero()
