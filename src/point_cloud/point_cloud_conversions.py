from typing import NoReturn

import vtk

from .type import ColorList


# 颜色列表到 vtkPolyData
def color_list_to_vtk_polydata(color_list: ColorList) -> vtk.vtkPolyData:
    """
    将自定义颜色列表转换为 vtkPolyData 对象
    :param color_list: list of tuples (x, y, z, r, g, b)
    :return: vtkPolyData 对象
    """
    points = vtk.vtkPoints()
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("Colors")

    # 添加点和颜色
    for point, color in color_list:
        points.InsertNextPoint(*point)
        colors.InsertNextTuple3(*color)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.GetPointData().SetScalars(colors)
    return polydata


# vtkPolyData 到颜色列表
def vtk_polydata_to_color_list(polydata: vtk.vtkPolyData) -> ColorList:
    """
    将 vtkPolyData 对象转换为自定义颜色列表
    :param polydata: vtkPolyData 对象
    :return: list of tuples (x, y, z, r, g, b)
    """
    points = polydata.GetPoints()
    colors = polydata.GetPointData().GetScalars()
    color_list = []

    for i in range(points.GetNumberOfPoints()):
        x, y, z = points.GetPoint(i)
        r, g, b = colors.GetTuple3(i)
        color_list.append(((x, y, z), (r, g, b)))

    return color_list


# vtkPolyData 到文件
def vtk_polydata_to_file(polydata: vtk.vtkPolyData, file_path: str) -> NoReturn:
    """
    将 vtkPolyData 对象保存到文件
    :param polydata: vtkPolyData 对象
    :param file_path: 保存文件的路径，支持 .ply 或 .vtk 格式
    """
    writer = vtk.vtkPLYWriter() if file_path.endswith('.ply') else vtk.vtkPolyDataWriter()
    writer.SetFileName(file_path)
    writer.SetInputData(polydata)
    writer.Write()


# 文件到 vtkPolyData
def file_to_vtk_polydata(file_path: str) -> vtk.vtkPolyData:
    """
    从文件读取数据并转换为 vtkPolyData 对象
    :param file_path: 文件路径，支持 .ply 或 .vtk 格式
    :return: vtkPolyData 对象
    """
    reader = vtk.vtkPLYReader() if file_path.endswith('.ply') else vtk.vtkPolyDataReader()
    reader.SetFileName(file_path)
    reader.Update()
    return reader.GetOutput()
