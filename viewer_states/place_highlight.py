"""
State:          Place Highlight
State type:     place_highlight
Description:    place highlight on an object!
Author:         sreeves
Date Created:   November 06, 2020 - 18:31:27
"""

import hou
import viewerstate.utils as su
import stateutils


class BeePlaceHighlightState(object):
    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.scene_viewer = scene_viewer
        self.light_dist = 1.5
        
        # init geo
        self._geometry = None
        
        # create geo for guide
        guide_line_verb = hou.sopNodeTypeCategory().nodeVerb('line')
        guide_line_verb.setParms({
            'dist': self.light_dist,
            'dir': (0,0,1)
            })

        # Get a fresh geometry to write to
        guide_line_geo = hou.Geometry()
        
        # execute the guide_line_verb
        guide_line_verb.execute(guide_line_geo, [])

        # create the guide
        self._guide = hou.SimpleDrawable(
            scene_viewer,
            guide_line_geo,
            state_name + "_guide"
        )

        self._guide.enable(True)
        self._guide.show(False)


    def onGenerate(self, kwargs):
        self.scene_viewer.beginStateUndo('Place highlight')
        
    def onExit(self, kwargs):
        self.scene_viewer.endStateUndo()
                
    def onSelection(self, kwargs):
        """get the light object from the selection"""
        
        if len(kwargs["selection"]) != 1:
            return False
        
        self.light = kwargs["selection"][0]
        return True
    
    def onMouseEvent(self, kwargs):
        """
        Process mouse events
        """

        self.scene_viewer.setPromptMessage('Left-click to place highlight')

        ui_event = kwargs["ui_event"]
        dev = ui_event.device()
        
        # only continue while left clicking
        if not dev.isLeftButton():
            return False

        # get current viewport
        viewport = self.scene_viewer.curViewport()
        
        # get the object under mouse position
        ray_obj = viewport.queryNodeAtPixel(int(dev.mouseX()), int(dev.mouseY()))
        
        # if nothing was hit return
        if not ray_obj:
            return
        
        # if the light was hit return
        if ray_obj == self.light:
            return
        
        # get geo from ray hit object
        self._geometry = ray_obj.displayNode().geometry()

        # return at this point if no geo
        if not self._geometry:
            return False
    
        # get world xform from  the ray_obj's ancestor
        parent = stateutils.ancestorObject(ray_obj)
        parent_xform = parent.worldTransform()

        # get the viewport ray event
        ray_origin, ray_dir = ui_event.ray()

        # invert view ray transform based on inverse of the hit object's world transform        
        ray_origin_obj = ray_origin * parent_xform.inverted()

        # from docs why no work... but alternative does!
        # ray_dir_obj = ray_dir  * parent_xform.inverted().extractRotates() 
        ray_dir_obj = ray_dir.multiplyAsDir(parent_xform.inverted())
        
        # get geo intersection - return is in local space
        hit, hit_pos, norm, uvw = su.sopGeometryIntersection(
            self._geometry, ray_origin_obj, ray_dir_obj
        )
        
        # as that was local space multiply with world transform
        world_pos = hit_pos * parent_xform
        world_norm = norm.multiplyAsDir(parent_xform)
  
        # work out the reflection direction
        refl = ray_dir - 2 * (ray_dir.dot(world_norm)) * world_norm

        # set the guide position
        guide_m = hou.hmath.buildRotateZToAxis(refl)
        guide_m *= hou.hmath.buildTranslate(world_pos)

        self._guide.setTransform(guide_m)
        self._guide.show(True)
        
        # set the light position
        light_pos = (world_pos) + (refl.normalized() * self.light_dist)
        
        # construct matrix from reflection direction and light position
        light_m = hou.hmath.buildRotateZToAxis(refl)
        light_m *= hou.hmath.buildTranslate(light_pos)

        # set transform on light        
        self.light.setWorldTransform(light_m)

        return True


def createViewerStateTemplate():
    """
    Mandatory entry point to create and return the viewer state 
    template to register.
    """

    state_typename = "place_highlight"
    state_label = "Place Highlight"
    state_cat = hou.objNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(BeePlaceHighlightState)
    template.bindIcon("MISC_python")

    return template
