import maya.cmds as cmds
import maya.mel as mel


def Overlapper():
    # 创建工作集
    work_set = cmds.sets(name="OverlapperWorkSet")

    # 初始化
    if not cmds.objExists("OverlapperWorkSet"):
        cmds.delete(work_set)

    # 清理
    debug_mode = 0
    if not debug_mode:
        cmds.delete("overlapResultLocatorOut*", "*overlapOffsetIKLocator*")

    # 更新当前时间
    current_time = cmds.currentTime(query=True)
    cmds.currentTime(current_time, edit=True)

    # 选择控制点集合
    selected_controls = cmds.ls(selection=True)
    cmds.select(selected_controls)
    cmds.cycleCheck(state=True)

    # 结束进度窗口
    cmds.progressWindow(endProgress=True)

    # 选择重叠控制点集合
    if cmds.objExists("OverlapperSet"):
        cmds.select("OverlapperSet")


def OverlapperStarter():
    if cmds.objExists("OverlapperWorkSet"):
        cmds.delete("OverlapperWorkSet")

    # 时间范围
    playback_slider = cmds.playbackOptions(query=True, animationStartTime=True)
    time_start, time_end = cmds.timeControl(playback_slider, query=True, rangeArray=True)
    time_range = time_end - time_start

    if time_range == 1:
        time_start_global = cmds.playbackOptions(query=True, minTime=True)
        time_end_global = cmds.playbackOptions(query=True, maxTime=True)
    else:
        time_start_global = time_start
        time_end_global = time_end

    # 控制点数量
    selected_controls = cmds.ls(selection=True)

    # 多个控制点
    if len(selected_controls) > 1:
        # 带层次结构
        if cmds.checkBox("HierarchyCheckBox", query=True, value=True):
            for ctrl in selected_controls:
                cmds.select(ctrl)
                WithHierarchy()
                CycleFinal()
        # 不带层次结构
        else:
            Overlapper()
            CycleFinal()
    # 单个控制点
    else:
        # 带层次结构
        if cmds.checkBox("HierarchyCheckBox", query=True, value=True):
            CycleFinal()
        # 不带层次结构
        else:
            cmds.confirmDialog(title="Oooops..",
                               message="For correct work you should select more than one control\nor switch on Hierarchy mode in Options\n\nIf you want overlap one control:\n1. select two neighboring controls\n2. check `Don't use first control` in Options",
                               button=["Ok"])


def OverlapperStarterParent():
    selected_items = cmds.ls(selection=True)
    for item in selected_items:
        nurbs_curves = cmds.listRelatives(item, type="nurbsCurve", allDescendents=True, fullPath=True)
        parents = cmds.listRelatives(nurbs_curves, parent=True)
        cmds.select(parents)
        OverlapperStarter()
    cmds.select(selected_items)


def DeleteSelectedKeys():
    selected_items = cmds.ls(selection=True)
    for item in selected_items:
        nurbs_curves = cmds.listRelatives(item, type="nurbsCurve", allDescendents=True, fullPath=True)
        parents = cmds.listRelatives(nurbs_curves, parent=True)
        cmds.cutKey(parents)
    cmds.select(selected_items)


def OverlapperWithHierarchy():
    all_scene_nurbs = cmds.ls(type="nurbsCurve")
    current_controls = cmds.ls(selection=True)
    current_shape_type = cmds.objectType(cmds.pickWalk(direction="down")[0])

    if any(cmds.objExists(obj) for obj in
           ["*Root_M", "*:Root_M", "*DeformationSystem", "*:DeformationSystem", "*MotionSystem", "*:MotionSystem",
            "*FitSkeleton", "*:FitSkeleton"]):
        current_shape_type = "nurbsCurve"

    stuff = list(set(all_scene_nurbs) - set(current_controls))
    ctrl_by_hierarchy = list(set(stuff) - set(current_controls))
    cmds.select(ctrl_by_hierarchy)

    amount_of_all_ctrls = len(ctrl_by_hierarchy)
    last_ctrl_in_hierarchy = ctrl_by_hierarchy[-1]

    chain = []
    for i in range(amount_of_all_ctrls):
        cmds.select(ctrl_by_hierarchy[i])
        cmds.select(hi=True)
        current_controls = cmds.ls(selection=True)
        stuff = list(set(all_scene_nurbs) - set(current_controls))
        current_ctrl_by_hierarchy = list(set(stuff) - set(current_controls))

        if ctrl_by_hierarchy[i + 1] == current_ctrl_by_hierarchy[1] and current_ctrl_by_hierarchy[
            0] != last_ctrl_in_hierarchy:
            chain.append(current_ctrl_by_hierarchy[0])
            cmds.select(current_ctrl_by_hierarchy[0])
        else:
            chain.append(current_ctrl_by_hierarchy[0])
            cmds.select(chain)
            Overlapper()
            ctrl_by_hierarchy = list(set(chain) - set(ctrl_by_hierarchy))
            chain.clear()




def CycleFinal():
    selected_controls_clear_namespaces = [cmds.stripNamespace(ctrl) for ctrl in cmds.ls(selection=True)]
    euler_filter_curves = []

    overlapper_work_set = cmds.sets(name="OverlapperWorkSet")
    euler_arrays = cmds.ls(overlapper_work_set)

    for obj in euler_arrays:
        anim_attrs = cmds.listAttr(obj, keyable=True)
        for attr in anim_attrs:
            anim_curve = cmds.listConnections(obj + "." + attr, type="animCurve")
            if anim_curve:
                euler_filter_curves.extend(anim_curve)

    cmds.filterCurve(euler_filter_curves)
    cmds.delete("OverlapperWorkSet")


# 调用函数
OverlapperRelease()
