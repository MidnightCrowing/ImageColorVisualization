import vtk


# TODO: 重新实现 find_overlapped_cloud 函数，该函数目前无法满足需求
def find_overlapped_cloud(cloud1: vtk.vtkPolyData, cloud2: vtk.vtkPolyData) -> vtk.vtkPolyData:
    """查找重叠点云并包含颜色信息"""
    overlapped_points = vtk.vtkPoints()
    overlapped_colors = vtk.vtkUnsignedCharArray()  # 创建用于存储颜色的数组
    overlapped_colors.SetNumberOfComponents(3)  # 设置颜色分量为3（RGB）
    overlapped_colors.SetName("Colors")  # 设置数组名称

    octree = vtk.vtkOctreePointLocator()
    octree.SetDataSet(cloud1)
    octree.BuildLocator()

    bounds = cloud1.GetBounds()  # 获取点云1的边界
    min_pt = [bounds[0], bounds[2], bounds[4]]
    max_pt = [bounds[1], bounds[3], bounds[5]]

    # 获取 cloud2 中的点和颜色
    num_points = cloud2.GetNumberOfPoints()
    points = [cloud2.GetPoint(i) for i in range(num_points)]
    colors = cloud2.GetPointData().GetScalars()  # 获取点云2的颜色数组

    # 使用列表推导式加速检查并存储重叠点和颜色
    for i, point in enumerate(points):
        if (min_pt[0] <= point[0] <= max_pt[0] and
                min_pt[1] <= point[1] <= max_pt[1] and
                min_pt[2] <= point[2] <= max_pt[2]):
            closest_point_id = octree.FindClosestPoint(point)
            if closest_point_id != -1:  # 找到重叠点
                overlapped_points.InsertNextPoint(point)
                if colors:  # 如果 cloud2 包含颜色数据，则添加相应的颜色
                    color = colors.GetTuple(i)
                    overlapped_colors.InsertNextTuple3(int(color[0]), int(color[1]), int(color[2]))

    # 创建新的点云包含重叠点和颜色
    overlapped_cloud = vtk.vtkPolyData()
    overlapped_cloud.SetPoints(overlapped_points)
    overlapped_cloud.GetPointData().SetScalars(overlapped_colors)  # 将颜色数据设置到点云上

    return overlapped_cloud
