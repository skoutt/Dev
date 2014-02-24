import sys
import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.OpenMayaRender as OpenMayaRender
import maya.OpenMayaUI as OpenMayaUI
import maya.OpenMayaAnim as OMAnim



nodeTypeName = "timeLord"
nodeTypeId   = OpenMaya.MTypeId(0x87093)

glRender     = OpenMayaRender.MHardwareRenderer.theRenderer()
glFT         = glRender.glFunctionTable()

#defaults
defaultShape = 'line'
defaultLineW = 'small'

shapeDir     = {'line':([0.0, -0.5 ,0.0], [0.0,  0.5 ,0.0]),
                'face':([-0.5, 0.0 ,-0.5],[0.5, 0.0 ,-0.5],[0.5, 0.0 ,0.5],[-0.5, 0.0 ,0.5])
               }
lineWDir     = {'small':1.0,
                'medium':2.0,
                'large':4.0
               }

def rtFrame():
    frame = OMAnim.MAnimControl.currentTime()
    frame = frame.value()
    return frame

#retime off Frame
def rtFrameMath(pivit,timeScale,anchor,frame,getSwitch,animTime):
    if (getSwitch == 0):
        getOff    = -((pivit * timeScale) - anchor)
        finalTime = (frame * timeScale) + getOff
        return finalTime
    if (getSwitch == 1):
        getOff    = -((pivit * timeScale) - anchor)
        finalTime = (animTime * timeScale) + getOff
        return finalTime
    if (getSwitch == 2):
        finalTime = frame
        return finalTime

def printSelectionList(selection):
    '''Prints a comma separated list of the object names in the selectionList.
    Useful for debugging'''
    selectionNames = []
    for x in range(selection.length()):
        oSelected = OpenMaya.MDagPath()
        selection.getDagPath(x, oSelected)
        fnSelected = OpenMaya.MFnDagNode(oSelected)
        selectionNames.append(fnSelected.name())
    print ', '.join(selectionNames)
    


class myNode(OpenMayaMPx.MPxLocatorNode):
    #variables
    inTime    = OpenMaya.MObject()
    animTime  = OpenMaya.MObject()
    timeScale = OpenMaya.MObject()
    finalTime = OpenMaya.MObject()
    pivit     = OpenMaya.MObject()
    anchor    = OpenMaya.MObject()
    switch    = OpenMaya.MObject()
    
    
    def __init__(self):
        OpenMayaMPx.MPxLocatorNode.__init__(self)
        
    def draw(self, view, path, style, status):
        view.beginGL()
        glFT.glEnable(OpenMayaRender.MGL_BLEND)
        
        glFT.glBegin(OpenMayaRender.MGL_LINES)
        glFT.glVertex3f(0.0, -0.5 ,0.0)
        glFT.glVertex3f(0.0,  0.5 ,0.0)
        glFT.glEnd()
        
        glFT.glDisable(OpenMayaRender.MGL_BLEND)
        
        view.endGL()
        
    def compute (self, plug, dataBlock):
        if (plug == myNode.finalTime):
            dataHandle = dataBlock.inputValue(myNode.pivit)
            pivit      = dataHandle.asFloat()
            dataHandle = dataBlock.inputValue(myNode.timeScale)
            timeScale      = dataHandle.asFloat()
            dataHandle = dataBlock.inputValue(myNode.anchor)
            anchor      = dataHandle.asFloat()
            dataHandle = dataBlock.inputValue(myNode.inTime)
            frame      = dataHandle.asFloat()
            
            dataHandle = dataBlock.inputValue(myNode.animTime)
            animTime      = dataHandle.asFloat()
            
            dataHandle = dataBlock.inputValue(myNode.switch)
            getSwitch      = dataHandle.asInt()
            
            getFrame = rtFrameMath(pivit,timeScale,anchor,frame,getSwitch,animTime)
            
            dataHandle = dataBlock.outputValue(myNode.finalTime)
            dataHandle.setFloat(getFrame)
            dataBlock.setClean(plug)
            
    def postConstructor(self):
        print "post smpxconstructor"
        test = self.name()
        obj = self.thisMObject()
        print self.typeId()
        print obj.isNull()
        node = OpenMaya.MFnDependencyNode(obj)
        print node.name()
        print test
        

def nodeCreator():
    return OpenMayaMPx.asMPxPtr(myNode())

    
def nodeInitializer():
    numAttr = OpenMaya.MFnNumericAttribute()
    getFrame = rtFrame()
    print getFrame
    myNode.finalTime = numAttr.create("finalTime","ftime",OpenMaya.MFnNumericData.kFloat,getFrame)
    numAttr.setStorable(1)
    
    numAttr = OpenMaya.MFnNumericAttribute()
    getFrame = rtFrame()
    print getFrame
    myNode.inTime = numAttr.create("inTime","inTime",OpenMaya.MFnNumericData.kFloat,getFrame)
    numAttr.setStorable(1)
    
    numAttr = OpenMaya.MFnNumericAttribute()
    myNode.animTime = numAttr.create("animTime","aTime",OpenMaya.MFnNumericData.kFloat,0.0)
    numAttr.setStorable(1)
    
    numAttr = OpenMaya.MFnNumericAttribute()
    myNode.pivit = numAttr.create("pivit","piv",OpenMaya.MFnNumericData.kFloat,0.0)
    numAttr.setStorable(1)
    
    numAttr = OpenMaya.MFnNumericAttribute()
    myNode.anchor = numAttr.create("anchor","anc",OpenMaya.MFnNumericData.kFloat,0.0)
    numAttr.setStorable(1)
    
    numAttr = OpenMaya.MFnNumericAttribute()
    myNode.timeScale = numAttr.create("timeScale","ts",OpenMaya.MFnNumericData.kFloat,1.0)
    numAttr.setStorable(1)
    
    enumAttr = OpenMaya.MFnEnumAttribute()
    myNode.switch = enumAttr.create("switch","sw")
    enumAttr.addField("frame",0)
    enumAttr.addField("animTime",1)
    enumAttr.addField("onRetime",2)
    enumAttr.setHidden(False)
    enumAttr.setKeyable(True)
    enumAttr.setDefault(0)
    enumAttr.setStorable(1)
    
    myNode.addAttribute(myNode.inTime)
    myNode.addAttribute(myNode.animTime)
    myNode.addAttribute(myNode.timeScale)
    myNode.addAttribute(myNode.pivit)
    myNode.addAttribute(myNode.anchor)
    myNode.addAttribute(myNode.finalTime)
    myNode.addAttribute(myNode.switch)
    myNode.attributeAffects(myNode.inTime, myNode.finalTime)
    myNode.attributeAffects(myNode.animTime, myNode.finalTime)
    myNode.attributeAffects(myNode.timeScale, myNode.finalTime)
    myNode.attributeAffects(myNode.pivit, myNode.finalTime)
    myNode.attributeAffects(myNode.anchor, myNode.finalTime)
    myNode.attributeAffects(myNode.switch, myNode.finalTime)
    
    return
    #return OpenMaya.MStatus.kSuccess


def initializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.registerNode(nodeTypeName, nodeTypeId, nodeCreator, nodeInitializer, OpenMayaMPx.MPxNode.kLocatorNode)
    except:
        sys.stderr.write("Failed to register node: %s" % nodeTypeName)
    
def uninitializePlugin(obj):
    plugin = OpenMayaMPx.MFnPlugin(obj)
    try:
        plugin.deregisterNode(nodeTypeId)
    except:
        sys.stderr.write("Failed to deregister node: %s" % nodeTypeName)