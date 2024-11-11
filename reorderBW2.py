import xml.etree.ElementTree as ET

type_order = [
    "cTequilaEffectResource",
    "cNodeHierarchyResource",
    "cGameScriptResource",
    "sSampleResource",
    "cTextureResource",
    "cSoundBase",
    "cGUINumberNumber",
    "cGUINumberFromFunction",
    "cGUINumberFromLabel",
    "cGUIScriptFunction",
    "cGUIVectorFromLabel",
    "cGUIVectorFromFunction",
    "cGUIScaleFromFunction",
    "cGUIColourFromLabel",
    "cGUIColourFromFunction",
    "cGUIBoolFromFunction",
    "cGUIBoolBool",
    "cGUIButtonSpriteSet",
    "cGUIColourColour",
    "cGUIColourNumber",
    "cGUIStringFromLabel",
    "cGUIStringFromFunction",
    "cCameraBase",
    "cGUIMatrixFromLabel",
    "cGUIStringString",
    "cGUIScaleVector",
    "cGUIBoolFromLabel",
    "cGUIVectorVector",
    "cGUIScaleFromLabel",
    "cSprite",
    "cGUIEvent",
    "cGUISpriteWidget",
    "sSpriteBasetype",
    "cWaypoint",
    "cScriptedSound",
    "cGUISoundWidget",
    "cGUIButtonWidget",
    "cGUISliderWidget",
    "cGUITextureWidget",
    "cGUITextBoxWidget",
    "cGUICustomWidget",
    "cGUIDialogBox3Widget",
    "cGUIDialogBox2Widget",
    "cGUIDialogBox1Widget",
    "cGUIDialogBox0Widget",
    "cGUI3DModelData",
    "cGUI3DObjectWidget",
    "cRenderParams",
    "cGlobalScriptEntity",
    "cInitialisationScriptEntity",
    "cGUIPage",
    "cGUIRectWidget",
    "cGUIVertexColouredRectWidget",
    "cGUIControllerBlip",
    "cScriptSprite",
    "cSKUSpecificData",
    "cGUITequilaData",
    "cGUIListBoxWidget",
    "cGUIEventHandler",
    "cGUITequilaWidget",
    "cScriptedEffectBase",
    "cCamera",
    "cAnimationResource",
    "cSimpleTequilaTaggedEffectBase",
    "cCoverPointBase",
    "sDestroyBase",
    "sSceneryClusterBase",
    "cAnimationTriggeredEffectChainItemGroundImpact",
    "cAdvancedWeaponBase",
    "cImpactTableTaggedEffectBase",
    "cProjectileSoundBase",
    "sProjectileBase",
    "sWeaponBase",
    "sAirVehicleBase",
    "cTroopAnimationSet",
    "cTroopVoiceManagerBase",
    "sTroopBase",
    "cReflectedPhysicsParams",
    "cGroundVehiclePhysicsBase",
    "cGroundVehicleSoundBase",
    "cSeatBase",
    "cGroundVehicleBase",
    "cAnimationTriggeredEffectManager",
    "cSoundCurve",
    "cAirVehicleEngineSoundBase",
    "cBuildingImpBase",
    "cWeaponSoundBase",
    "cArmyAllegiance",
    "cPanelSprites",
    "cObjectiveMarkerBase",
    "cAirVehicleSoundBase",
    "sExplodeBase",
    "cImpactBase",
    "cImpactTableBase",
    "cIncidentalBase",
    "cTerrainParticleGeneratorBase",
    "cCapturePointBase",
    "cAnimationTriggeredEffectChainItemSound",
    "cAnimationTriggeredEffectChainItemTequilaEffect",
    "cReticuleState",
    "cAnimationTriggeredEffect",
    "cTroopVoiceMessageBase",
    "cHUDSoundBlock",
    "sPickupBase",
    "cAirVehiclePhysicsBase",
    "cGroundVehicleEngineSoundBase",
    "cRevConScrollRegionBase",
    "cContextSensitiveIdle",
    "cContextSensitiveIdleList",
    "cPlayerSettings",
    "cHUDVariables",
    "cHUD",
    "cHUDTutorial",
    "cAttackSustainReleaseEnvelope",
    "cFlightData",
    "cMapZone",
    "cPhase",
    "cObjective",
    "cMorphingBuilding",
    "cStrategicInstallation",
    "cActionParameterData",
    "cMeleeHitReactionData",
    "cAmbientAreaPointSoundSphere",
    "cActionParameters",
    "cDestroyableObject",
    "cSceneryCluster",
    "cTroop",
    "cGroundVehicle",
    "cAirVehicle",
    "cBuilding",
    "cCapturePoint",
    "cObjectiveMarker",
    "cWaterVehiclePhysicsBase",
    "cWaterVehicleSoundBase",
    "cWaterVehicleBase",
    "cCoastZone",
    "cReflectedUnitGroup",
    "cWaterVehicle",
    "cPickupReflected",
    "cDamageZone",
    "cNogoHintZone"
]

type_order_set = set(type_order)

def reorder_xml(filepath):

    tree = ET.parse(filepath)
    root = tree.getroot()

    ordered_objects = []
    unordered_objects = []

    for obj in root.findall(".//Object"):
        obj_type = obj.get("type")
        if obj_type in type_order_set:
            ordered_objects.append((type_order.index(obj_type), obj))
        else:
            unordered_objects.append(obj)

    ordered_objects.sort(key=lambda x: x[0])

    instances = root.find(".//Instances")
    if instances is not None:
        root.remove(instances)
    for obj in root.findall(".//Object"):
        root.remove(obj)

    for _, obj in ordered_objects:
        root.append(obj)
    for obj in unordered_objects:
        root.append(obj)
        print(f"Unordered type placed at bottom: {obj.get('type')}")

    output_path = filepath.replace(".xml", "_reordered.xml")
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Reordered XML saved to {output_path}")

# Your XML file here
reorder_xml("D:\\Battalion wars modding laptop\\desktop imports\\Modding Stream\\files\\Data\\CompoundFiles\\MP11_Level.xml")
