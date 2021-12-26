bl_info = {
	"name": "Create Temp Window",
	"author": "Kenetics",
	"version": (0, 1),
	"blender": (2, 80, 0),
	"location": "View3D > Right Click Context Menu",
	"description": "Creates a new window from 3D View",
	"warning": "",
	"wiki_url": "",
	"category": "System"
}

import bpy
from bpy.props import EnumProperty, IntProperty, FloatVectorProperty, BoolProperty, FloatProperty, StringProperty
from bpy.types import PropertyGroup, UIList, Operator, Panel, AddonPreferences

## Helper Functions


## Operators

class CTW_OT_create_temp_window(Operator):
	"""Creates a new window"""
	bl_idname = "object.ctw_ot_create_temp_window"
	bl_label = "Create Temp Window"
	bl_options = {'REGISTER','UNDO'}
	
	# Properties
	window_type : EnumProperty(
		items=[
			("VIEW_3D","3D View","","VIEW3D",0),
			("GRAPH_EDITOR","Graph Editor","","GRAPH",1),
			("DOPESHEET_EDITOR","Dopesheet","","GRAPH",2),
			("NLA_EDITOR","NLA Editor","","NLA",3),
			("IMAGE_EDITOR","Image Editor","","FILE_IMAGE",4),
			("TEXT_EDITOR","Text Editor","","FILE_TEXT",5),
			("NODE_EDITOR","Node Editor","","NODE_MATERIAL",6),
			("PROPERTIES","Properties","","PROPERTIES",7),
			("OUTLINER","Outliner","","OUTLINER",8),
			("USER_PREFERENCES","Preferences","","PREFERENCES",9),
			("FILE_BROWSER","File Browser","","FILE_FOLDER",10),
			("CONSOLE","Console","","CONSOLE",11),
			("ADDONS","Addons","","PREFERENCES",12),
			("BLENDER_FILE","Blender File","","FILE_FOLDER",13),
			("ASSETS","Assets","","FILE_FOLDER",14)
		],
		name="Window Type",
		description="Type of window to create",
		default="USER_PREFERENCES"
	)

	@classmethod
	def poll(cls, context):
		return True

	def execute(self, context):
		# Call user prefs window
		bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
		
		if self.window_type == "ADDONS":
			context.preferences.active_section = "ADDONS"
			
		elif self.window_type != "USER_PREFERENCES":
			area = context.window_manager.windows[-1].screen.areas[0]
			
			# Catch Custom window type
			if self.window_type == "BLENDER_FILE":
				area.type = "OUTLINER"
				area.spaces[0].display_mode = "LIBRARIES"
			elif self.window_type == "ASSETS":
				area.type = "FILE_BROWSER"
				area.spaces[0].browse_mode = "ASSETS"
			else:
				# Change area type
				area.type = self.window_type
		return {'FINISHED'}

## Append to UI Functions

def create_temp_window_button(self, context):
	self.layout.operator_menu_enum(CTW_OT_create_temp_window.bl_idname, "window_type", icon="WINDOW")

## Register

def register():
	bpy.utils.register_class(CTW_OT_create_temp_window)
	bpy.types.VIEW3D_MT_object_context_menu.append(create_temp_window_button)
	bpy.types.NODE_MT_context_menu.append(create_temp_window_button)
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(create_temp_window_button)

def unregister():
	bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(create_temp_window_button)
	bpy.types.NODE_MT_context_menu.remove(create_temp_window_button)
	bpy.types.VIEW3D_MT_object_context_menu.remove(create_temp_window_button)
	bpy.utils.unregister_class(CTW_OT_create_temp_window)

if __name__ == "__main__":
	register()

## Notes

"""
GRAPH_EDITOR Graph Editor, Edit drivers and keyframe interpolation.
DOPESHEET_EDITOR Dope Sheet, Adjust timing of keyframes.
NLA_EDITOR NLA Editor, Combine and layer Actions.
IMAGE_EDITOR UV/Image Editor, View and edit images and UV Maps.
SEQUENCE_EDITOR Video Sequence Editor, Video editing tools.
CLIP_EDITOR Movie Clip Editor, Motion tracking tools.
TEXT_EDITOR Text Editor, Edit scripts and in-file documentation.
NODE_EDITOR Node Editor, Editor for node-based shading and compositing tools.
LOGIC_EDITOR Logic Editor, Game logic editing.
PROPERTIES Properties, Edit properties of active object and related datablocks.
OUTLINER Outliner, Overview of scene graph and all available datablocks.
USER_PREFERENCES User Preferences, Edit persistent configuration settings.
INFO Info, Main menu bar and list of error messages (drag down to expand and display).
FILE_BROWSER File Browser, Browse for files and assets.
CONSOLE
"""
