import bpy
import math
import bmesh


# 体积计算函数
def calculate_object_volume(obj, context):
    depsgraph = context.evaluated_depsgraph_get()  # 获取依赖图
    eval_obj = obj.evaluated_get(depsgraph)
    
    mesh = bpy.data.meshes.new_from_object(eval_obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    volume = bm.calc_volume(signed=False)
    bm.free()
    
    bpy.data.meshes.remove(mesh)  # 清理临时创建的网格数据

    bpy.data.objects["volume_empty"].location.z = volume
    
    return volume


def delete_uv_mesh():
    # 指定要删除的mesh对象名称
    mesh_name = 'decals_gn.001'
    if mesh_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[mesh_name], do_unlink=True)


def hex_to_rgb(hex_color):
    """
    将十六进制颜色字符串转换为RGB元组。
    """
    hex_color = hex_color.lstrip('#')
    hlen = len(hex_color)
    return tuple(int(hex_color[i:i+hlen//3], 16) / 255 for i in range(0, hlen, hlen//3))


# 更新函数，用于同步属性值到相应的空物体
def update_value(self, context):
    rim_dimension = bpy.data.objects["rim_dimension"]
    rim_dimension.location.z = self.height / 100
    rim_dimension.location.x = self.rim / 100

    bottom_ratio = bpy.data.objects["bottom_ratio"]
    bottom_ratio.location.x = self.bottom_ratio

    waist_ratio = bpy.data.objects["waist_ratio"]
    waist_ratio.location.z = self.waist_ratio_h
    waist_ratio.location.x = self.waist_ratio_w

    smooth_shape = bpy.data.objects["smooth_shape"]
    smooth_shape.location.x = self.smooth_shape

    # 有无把手
    is_handle_x = bpy.data.objects["is_handle"]
    is_handle_x.location.x = self.is_handle_x 

    # 调整body_mat
    body_mat_obj = bpy.data.objects["body_mat"]
    body_mat_obj.location.x = self.body_mat_x

    # 调整handle_mat
    handle_mat_obj = bpy.data.objects["handle_mat"]
    handle_mat_obj.location.x = self.handle_mat_x

    bpy.data.objects["color_1"].location = (self.color_1_r, self.color_1_g, self.color_1_b)
    bpy.data.objects["color_2"].location = (self.color_2_r, self.color_2_g, self.color_2_b)
    bpy.data.objects["lip_color"].location = (self.lip_color_r, self.lip_color_g, self.lip_color_b)

    # 删除旧的UV mesh
    delete_uv_mesh()

    # 当属性更新时，强制显示"Go Gen"而不是计算错误率
    context.scene.my_tool["error_message"] = "Go Gen"


# 自定义设置
class MySettings(bpy.types.PropertyGroup):
    height: bpy.props.IntProperty(
        name="Rim Height",
        description="Height of the cup",
        default=100,
        min=math.ceil(bpy.data.objects["rim_dimension"].constraints["Limit Location"].min_z * 100),
        max=math.floor(bpy.data.objects["rim_dimension"].constraints["Limit Location"].max_z * 100),
        update=update_value
    )
    rim: bpy.props.FloatProperty(
        name="Rim Radius",
        description="Radius of the cup rim",
        default=35.0,
        min=math.ceil(bpy.data.objects["rim_dimension"].constraints["Limit Location"].min_x * 100),
        max=math.floor(bpy.data.objects["rim_dimension"].constraints["Limit Location"].max_x * 100),
        precision=1,
        update=update_value
    )
    bottom_ratio: bpy.props.FloatProperty(
        name="Bottom Ratio",
        description="Bottom ratio",
        default=1.0,
        min=bpy.data.objects["bottom_ratio"].constraints["Limit Location"].min_x,
        max=bpy.data.objects["bottom_ratio"].constraints["Limit Location"].max_x,
        update=update_value
    )
    waist_ratio_h: bpy.props.FloatProperty(
        name="Waist H_Ratio",
        description="Waist ratio height",
        default=0.2,
        min=bpy.data.objects["waist_ratio"].constraints["Limit Location"].min_z,
        max=bpy.data.objects["waist_ratio"].constraints["Limit Location"].max_z,
        update=update_value
    )
    waist_ratio_w: bpy.props.FloatProperty(
        name="Waist W_Ratio",
        description="Waist ration width",
        default=1.0,
        min=bpy.data.objects["waist_ratio"].constraints["Limit Location"].min_x,
        max=bpy.data.objects["waist_ratio"].constraints["Limit Location"].max_x,
        update=update_value
    )
    total_volume: bpy.props.FloatProperty(
        name="Total Volume",
        description="Total volume of the object",
        default=0.0
    )
    cup_volume: bpy.props.IntProperty(
        name="Cup Volume",
        description="Target volume for the cup",
        default=350,  # 默认目标体积
        min=70,
        update=update_value
    )
    smooth_shape: bpy.props.FloatProperty(
        name="Smooth Shape",
        description="Smooth waistline",
        default=1.0,
        min=bpy.data.objects["smooth_shape"].constraints["Limit Location"].min_x,
        max=bpy.data.objects["smooth_shape"].constraints["Limit Location"].max_x,
        update=update_value
    )
    is_handle_x: bpy.props.IntProperty(
        name="Handle",
        description="Handle",
        default=0,
        min=0,
        max=1,
        update=update_value
    )
    body_mat_x: bpy.props.IntProperty(
        name="Body Material",
        description="Select Body Material",
        default=0,
        min=0,
        max=2,
        update=update_value
    )
    handle_mat_x: bpy.props.IntProperty(
        name="Handle Material",
        description="Select Handle Material",
        default=0,
        min=0,
        max=2,
        update=update_value
    )

    color_1_r: bpy.props.FloatProperty(
        name="R", description="Red component of Color 1", default=1.0, min=0.0, max=1.0, update=update_value)
    color_1_g: bpy.props.FloatProperty(
        name="G", description="Green component of Color 1", default=1.0, min=0.0, max=1.0, update=update_value)
    color_1_b: bpy.props.FloatProperty(
        name="B", description="Blue component of Color 1", default=1.0, min=0.0, max=1.0, update=update_value)
    
    color_2_r: bpy.props.FloatProperty(
        name="R", description="Red component of Color 2", default=1.0, min=0.0, max=1.0, update=update_value)
    color_2_g: bpy.props.FloatProperty(
        name="G", description="Green component of Color 2", default=1.0, min=0.0, max=1.0, update=update_value)
    color_2_b: bpy.props.FloatProperty(
        name="B", description="Blue component of Color 2", default=1.0, min=0.0, max=1.0, update=update_value)
    
    lip_color_r: bpy.props.FloatProperty(
        name="R", description="Red component of Lip Color", default=1.0, min=0.0, max=1.0, update=update_value)
    lip_color_g: bpy.props.FloatProperty(
        name="G", description="Green component of Lip Color", default=1.0, min=0.0, max=1.0, update=update_value)
    lip_color_b: bpy.props.FloatProperty(
        name="B", description="Blue component of Lip Color", default=1.0, min=0.0, max=1.0, update=update_value)
   
    # 设置错误信息为"Go Gen"
    error_message: bpy.props.StringProperty(
        name="Error Message",
        default="Go Gen"
    )


class ApproachTargetVolume(bpy.types.Operator):
    bl_idname = "object.approach_target_volume"
    bl_label = "Approach Target Volume"

    def execute(self, context):
        scene = context.scene
        my_tool = scene.my_tool
        target_volume = my_tool.cup_volume
        iteration_threshold = 0.06  # 定义体积差异的阈值

        obj = bpy.data.objects.get('cupmesh-volume')
        if not obj:
            self.report({'ERROR'}, "Object 'cupmesh-volume' not found.")
            return {'CANCELLED'}

        # 首次计算当前体积
        current_volume = calculate_object_volume(obj, context) * 1000
        volume_difference = abs(current_volume - target_volume)

        # 调整高度前检查当前高度是否在限制范围内
        height_adjustment_factor = (target_volume / current_volume) ** (1/3)
        new_height = my_tool.height * height_adjustment_factor
        height_min = math.ceil(bpy.data.objects["rim_dimension"].constraints["Limit Location"].min_z * 100)
        height_max = math.floor(bpy.data.objects["rim_dimension"].constraints["Limit Location"].max_z * 100)

        if new_height < height_max and new_height > height_min:
            # 调整高度
            my_tool.height = round(new_height)
        else:
            # 当前高度已达到极限，调整rim值
            rim_adjustment = (volume_difference / 1000) ** (1/3)  # 动态计算rim调整量
            if current_volume < target_volume:
                my_tool.rim += rim_adjustment * 5
            else:
                my_tool.rim -= rim_adjustment * 5

        # 调整高度或rim后重新计算体积
        current_volume = calculate_object_volume(obj, context) * 1000
        volume_difference = abs(current_volume - target_volume)

        # 根据调整后的误差设置错误信息
        if volume_difference <= iteration_threshold * target_volume:
            my_tool["error_message"] = "OK"
        else:
            my_tool["error_message"] = "Go Gen"

        my_tool.total_volume = current_volume

        return {'FINISHED'}
    

# 平展UV    
class GenerateUVOperator(bpy.types.Operator):
    bl_idname = "object.generate_uv"
    bl_label = "Generate UV"

    def execute(self, context):
        obj = bpy.data.objects.get('decals_gn')
        if obj:
            # 复制物体
            obj_copy = obj.copy()
            obj_copy.data = obj.data.copy()
            bpy.context.collection.objects.link(obj_copy)

            # 确保只选择复制的物体
            bpy.ops.object.select_all(action='DESELECT')  # 取消选择所有物体
            obj_copy.select_set(True)
            bpy.context.view_layer.objects.active = obj_copy

            obj_copy.location.x = 0

            # 应用 GeometryNodes 修改器
            bpy.ops.object.modifier_apply(modifier="GeometryNodes")

            # 添加shrinkwrap
            bpy.ops.object.modifier_add(type='SHRINKWRAP')
            bpy.context.object.modifiers["Shrinkwrap"].target = bpy.data.objects["cupmesh"]
            bpy.context.object.modifiers["Shrinkwrap"].offset = 0.0002

            # 进入编辑模式
            bpy.ops.object.mode_set(mode='EDIT')

            # 全选顶点
            bpy.ops.mesh.select_all(action='SELECT')

            # 执行UV操作
            bpy.ops.uv.select_all(action='DESELECT')
            bpy.ops.uv.zenuv_unified_mark(convert='SEAM_BY_UV_BORDER')
            bpy.ops.uv.zenuv_unified_transform(orient_island=False, pp_pos='tl', orient_direction='AUTO', rotate_direction='CCW', fit_keep_proportion=True, desc="Rotate Islands counterclockwise")
            bpy.ops.uv.zenuv_quadrify()
            bpy.ops.uv.muv_pack_uv(allowable_center_deviation=(0.001, 0.001), allowable_size_deviation=(0.001, 0.001), accurate_island_copy=True, stride=(0, 0), apply_pack_uv=True)

            # 确保在对象模式下工作
            bpy.ops.object.mode_set(mode='OBJECT')

            # 获取UV图层
            uv_layer = obj_copy.data.uv_layers.active.data
            
            # 初始化最大Y值变量
            max_y = -float('inf')

            # 遍历所有的UV顶点，找到最大的Y值
            for poly in obj_copy.data.polygons:
                for loop_index in poly.loop_indices:
                    uv_coord = uv_layer[loop_index].uv
                    max_y = max(max_y, uv_coord.y)
            
            # 输出最大Y值，保留三位小数
            print(f"Max UV Y: {max_y:.3f}")

            # 保存最大Y值到txt文件，保留三位小数
            file_path = bpy.path.abspath('//max_uv_y.txt')
            with open(file_path, 'w') as file:
                file.write(f"{max_y:.3f}")


        return {'FINISHED'}


# Get Para
class ImportParametersOperator(bpy.types.Operator):
    """Operator to import parameters from a text file"""
    bl_idname = "object.import_parameters"
    bl_label = "Get Para"

    def execute(self, context):
        filepath = bpy.path.abspath('//para_result.txt')
        try:
            with open(filepath, 'r') as file:
                for line in file:
                    parts = line.strip().split(': ', 1)  # Split only once
                    if len(parts) == 2:
                        key, value = parts
                        if key == 'volume':
                            context.scene.my_tool.cup_volume = int(value)
                            print(f"{key}: {value}")  # 打印键值对
                        elif key == 'is_handle':
                            context.scene.my_tool.is_handle_x = int(value)
                            print(f"{key}: {value}")
                        elif key == 'rim_radius':
                            context.scene.my_tool.rim = float(value)
                            print(f"{key}: {value}")
                        elif key == 'bottom_ratio':
                            context.scene.my_tool.bottom_ratio = float(value)
                            print(f"{key}: {value}")
                        elif key == 'waist_w_ratio':
                            context.scene.my_tool.waist_ratio_w = float(value)
                            print(f"{key}: {value}")
                        elif key == 'shape_smooth':
                            context.scene.my_tool.smooth_shape = float(value)
                            print(f"{key}: {value}")
                        elif key == 'body_mat':
                            context.scene.my_tool.body_mat_x = int(value)
                        elif key == 'handle_mat':
                            context.scene.my_tool.handle_mat_x = int(value)
                            print(f"{key}: {value}")
                        elif key in ['color_1', 'color_2', 'lip_color']:
                            # 将十六进制颜色值转换为RGB
                            r, g, b = hex_to_rgb(value)
                            if key == 'color_1':
                                context.scene.my_tool.color_1_r = r
                                context.scene.my_tool.color_1_g = g
                                context.scene.my_tool.color_1_b = b
                            elif key == 'color_2':
                                context.scene.my_tool.color_2_r = r
                                context.scene.my_tool.color_2_g = g
                                context.scene.my_tool.color_2_b = b
                            elif key == 'lip_color':
                                context.scene.my_tool.lip_color_r = r
                                context.scene.my_tool.lip_color_g = g
                                context.scene.my_tool.lip_color_b = b
                            # print(f"{key}: {r}, {g}, {b}")
        except Exception as e:
            self.report({'ERROR'}, str(e))
        
        bpy.ops.object.approach_target_volume()

        return {'FINISHED'}


# 自定义面板
class CustomPanel(bpy.types.Panel):
    bl_label = "Custom Panel"
    bl_idname = "NODE_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        my_tool = context.scene.my_tool

        # Import Para
        col = layout.column(align=True)
        col.operator("object.import_parameters", text="Get Para")

        # 添加生成按钮
        col = layout.column(align=True)
        col.operator("object.approach_target_volume", text="Gen Cup")

        # 显示体积
        col = layout.column(align=True)
        row = layout.row()
        row.label(text=f"Volume: {int(my_tool.total_volume)}")
        row.label(text="" + my_tool["error_message"])

        # 添加生成 UV 按钮
        col = layout.column(align=True)
        col.operator("object.generate_uv", text="Gen Decals")

        # Handle
        col = layout.column(align=True)
        col.prop(my_tool, "is_handle_x", text="Handle")

        # Mat Select and Color
        col = layout.column(align=True)
        col.prop(my_tool, "body_mat_x", text="Body Mat")
        col.prop(my_tool, "handle_mat_x", text="Handle Mat")
    
        # 添加RGB颜色输入
        col = layout.column(align=True)
        col.label(text="Color 1 (RGB):")
        row = col.row(align=True)
        row.prop(my_tool, "color_1_r", text="R")
        row.prop(my_tool, "color_1_g", text="G")
        row.prop(my_tool, "color_1_b", text="B")
        
        col.label(text="Color 2 (RGB):")
        row = col.row(align=True)
        row.prop(my_tool, "color_2_r", text="R")
        row.prop(my_tool, "color_2_g", text="G")
        row.prop(my_tool, "color_2_b", text="B")

        col.label(text="Lip Color (RGB):")
        row = col.row(align=True)
        row.prop(my_tool, "lip_color_r", text="R")
        row.prop(my_tool, "lip_color_g", text="G")
        row.prop(my_tool, "lip_color_b", text="B")

        # 界面元素排列
        col = layout.column(align=True)
        col.label(text="Dimensions:")
        col.prop(my_tool, "height")
        col.prop(my_tool, "rim")

        col = layout.column(align=True)
        col.prop(my_tool, "bottom_ratio")
        col.prop(my_tool, "waist_ratio_h")
        col.prop(my_tool, "waist_ratio_w")

        # smooth_shape 的控制输入
        col = layout.column(align=True)
        col.prop(my_tool, "smooth_shape", text="Shape Smooth")
        
        # 添加目标体积输入
        col = layout.column(align=True)
        col.prop(my_tool, "cup_volume") 
        

# 注册类
def register():
    bpy.utils.register_class(MySettings)
    bpy.utils.register_class(CustomPanel)
    bpy.utils.register_class(ApproachTargetVolume)
    bpy.utils.register_class(GenerateUVOperator)
    bpy.utils.register_class(ImportParametersOperator)
    bpy.types.Scene.my_tool = bpy.props.PointerProperty(type=MySettings)

# 注销类
def unregister():
    bpy.utils.unregister_class(MySettings)
    bpy.utils.unregister_class(CustomPanel)
    bpy.utils.unregister_class(ApproachTargetVolume)
    bpy.utils.unregister_class(GenerateUVOperator)
    bpy.utils.unregister_class(ImportParametersOperator)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()
