import numpy as np
import vtk
from scipy.spatial import KDTree


def extract_points_colors(cloud: vtk.vtkPolyData):
    """从vtkPolyData中提取点和颜色信息"""
    points = np.array([cloud.GetPoint(i) for i in range(cloud.GetNumberOfPoints())])
    colors = cloud.GetPointData().GetScalars()
    return points, colors


def insert_point_with_color(overlapping_points, overlapping_colors, point, colors, color_idx):
    """将点和颜色插入到结果中"""
    overlapping_points.InsertNextPoint(point)
    color = colors.GetTuple3(color_idx)
    overlapping_colors.InsertNextTuple3(int(color[0]), int(color[1]), int(color[2]))


def find_overlapped_cloud_kdtree(cloud1: vtk.vtkPolyData, cloud2: vtk.vtkPolyData, threshold=0.1) -> vtk.vtkPolyData:
    """使用KDTree查找重叠点云并包含颜色信息"""

    # 提取点和颜色信息
    points1, colors1 = extract_points_colors(cloud1)
    points2, colors2 = extract_points_colors(cloud2)

    # 创建 KDTree 加速最近邻查找
    kdtree = KDTree(points1)

    overlapping_points = vtk.vtkPoints()
    overlapping_colors = vtk.vtkUnsignedCharArray()
    overlapping_colors.SetName("Colors")
    overlapping_colors.SetNumberOfComponents(3)

    # 遍历第二个点云中的点
    for i, point in enumerate(points2):
        distance, nearest_point_id = kdtree.query(point)

        if distance < threshold:
            insert_point_with_color(overlapping_points, overlapping_colors, point, colors2, i)

    # 返回包含重叠点和颜色的vtkPolyData
    return create_result_polydata(overlapping_points, overlapping_colors)


def find_overlapped_cloud_octree(cloud1: vtk.vtkPolyData, cloud2: vtk.vtkPolyData, threshold=0.1) -> vtk.vtkPolyData:
    """使用Octree查找重叠点云并包含颜色信息"""

    # 提取点和颜色信息
    points1, colors1 = extract_points_colors(cloud1)
    points2, colors2 = extract_points_colors(cloud2)

    # 创建 Octree
    octree = vtk.vtkOctreePointLocator()
    octree.SetDataSet(cloud1)
    octree.BuildLocator()

    overlapping_points = vtk.vtkPoints()
    overlapping_colors = vtk.vtkUnsignedCharArray()
    overlapping_colors.SetName("Colors")
    overlapping_colors.SetNumberOfComponents(3)

    # 遍历第二个点云中的点
    for i, point in enumerate(points2):
        nearest_point_id = octree.FindClosestPoint(point)

        if nearest_point_id != -1:
            nearest_point = points1[nearest_point_id]
            distance = np.linalg.norm(nearest_point - point)

            if distance < threshold:
                insert_point_with_color(overlapping_points, overlapping_colors, point, colors2, i)

    # 返回包含重叠点和颜色的vtkPolyData
    return create_result_polydata(overlapping_points, overlapping_colors)


def create_result_polydata(overlapping_points, overlapping_colors) -> vtk.vtkPolyData:
    """创建结果 vtkPolyData 对象"""
    result_polydata = vtk.vtkPolyData()
    result_polydata.SetPoints(overlapping_points)
    result_polydata.GetPointData().SetScalars(overlapping_colors)
    return result_polydata


# 使用Octree方法作为默认实现
find_overlapped_cloud = find_overlapped_cloud_octree
