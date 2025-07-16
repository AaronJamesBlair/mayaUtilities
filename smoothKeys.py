# Same results as the classic "oaSmooth", but more efficient
import maya.cmds as mc

def smoothKeys():
    curves = mc.keyframe(q=True, name=1)
    
    for curve in curves:
        keys = mc.keyframe(curve, q=True, sl=1)
        values = mc.keyframe(curve, q=True, vc=True, sl=True)
            
        for i in range(1, len(keys)-1):
            time = keys[i]
            currentValue = values[i]
            
            previousValue = values[i-1]
            nextValue = values[i+1]
            
            average = (previousValue + currentValue + nextValue) / 3
            mc.keyframe(curve, valueChange=average, absolute=1, time=(time, time))
