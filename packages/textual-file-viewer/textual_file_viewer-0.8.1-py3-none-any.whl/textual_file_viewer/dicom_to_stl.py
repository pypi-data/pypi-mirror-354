# https://gist.github.com/issakomi/29e48917e77201f2b73bfa5fe7b30451
from dataclasses import dataclass
from itertools import chain
import struct

import pydicom
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import vtkActor, vtkPolyDataMapper, vtkRenderWindow, vtkRenderWindowInteractor, vtkRenderer


# CIELab to RGB
# https://getreuer.info/posts/colorspace/
def lab_inverse(x: float) -> float:
    if x >= 0.206896551724137931:
        return x * x * x

    return (108.0 / 841.0) * (x - (4.0 / 29.0))


def gamma_correction(x: float) -> float:
    if x <= 0.0031306684425005883:
        return float(12.92 * x)

    return float(1.055 * pow(x, 0.416666666666666667) - 0.055)


@dataclass
class LAB:
    l: float  # noqa: E741
    a: float
    b: float


@dataclass
class RGB:
    red: float
    green: float
    blue: float


# D65 white point
def cielab2rgb(lab: LAB) -> RGB:
    l_tmp = (lab.l + 16.0) / 116.0

    x = 0.950456 * lab_inverse(l_tmp + lab.a / 500.0)
    y = 1.000000 * lab_inverse(l_tmp)
    z = 1.088754 * lab_inverse(l_tmp - lab.b / 200.0)

    r_tmp = 3.2406 * x - 1.5372 * y - 0.4986 * z
    g_tmp = -0.9689 * x + 1.8758 * y + 0.0415 * z
    b_tmp = 0.0557 * x - 0.2040 * y + 1.0570 * z

    if r_tmp <= g_tmp:
        m = min(r_tmp, b_tmp)
    else:
        m = min(g_tmp, b_tmp)

    if m < 0:
        r_tmp -= m
        g_tmp -= m
        b_tmp -= m

    return RGB(gamma_correction(r_tmp), gamma_correction(g_tmp), gamma_correction(b_tmp))


def get_points(s: pydicom.Dataset) -> vtkPoints:
    points = vtkPoints()
    coordinates = chain.from_iterable(struct.iter_unpack('f', s.SurfacePointsSequence[0].PointCoordinatesData))

    # iterate over data in chunks of 3 values
    v = iter(coordinates)
    for point in [(i, next(v), next(v)) for i in v]:
        points.InsertNextPoint(point)

    return points


def get_polygons(s: pydicom.Dataset) -> vtkCellArray:
    if "LongTrianglePointIndexList" in s.SurfaceMeshPrimitivesSequence[0]:
        # 'I' == unsigned short i.e. 2 bytes
        triangle_index_list = chain.from_iterable(
            struct.iter_unpack('I', s.SurfaceMeshPrimitivesSequence[0].LongTrianglePointIndexList))
    else:
        # 'H' == unsigned short i.e. 2 bytes
        triangle_index_list = chain.from_iterable(
            struct.iter_unpack('H', s.SurfaceMeshPrimitivesSequence[0].TrianglePointIndexList))

    polys = vtkCellArray()  # type: ignore

    # iterate over data in chunks of 3 values
    # DICOM point indices are 1 based, VTK is 0 based
    v = iter(triangle_index_list)
    for point in [(i - 1, next(v) - 1, next(v) - 1) for i in v]:
        polys.InsertNextCell(3)
        polys.InsertCellPoint(point[0])
        polys.InsertCellPoint(point[1])
        polys.InsertCellPoint(point[2])

    return polys


def load_seg_mesh(ds: pydicom.Dataset) -> None:
    rgb = RGB(0.8, 0.5, 0.2)

    ren = vtkRenderer()

    renwin = vtkRenderWindow()
    renwin.AddRenderer(ren)

    iren = vtkRenderWindowInteractor()
    iren.SetInteractorStyle(vtkInteractorStyleTrackballCamera())  # type: ignore
    iren.SetRenderWindow(renwin)
    ren.SetBackground(0.3254, 0.3490, 0.3764)
    renwin.SetSize(800, 600)
    iren.Initialize()

    for s in ds.SurfaceSequence:
        polydata = vtkPolyData()
        polydata.SetPoints(get_points(s))
        polydata.SetPolys(get_polygons(s))

        # writer = vtk.vtkPolyDataWriter()
        # writer.SetFileName('test.vtk')
        # writer.SetInputData(polydata)
        # writer.Write()

        gen_normals = vtkPolyDataNormals()
        gen_normals.SetInputData(polydata)
        gen_normals.ComputePointNormalsOn()
        gen_normals.ComputeCellNormalsOff()

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(gen_normals.GetOutputPort())  # type: ignore

        if "RecommendedDisplayCIELabValue" in s:
            cielab = s.RecommendedDisplayCIELabValue
            rgb = cielab2rgb(LAB(
                (cielab[0] / 65535.0) * 100.0,
                ((cielab[1] - 32896.0) / 65535.0) * 255.0,
                ((cielab[2] - 32896.0) / 65535.0) * 255.0))

        actor = vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(rgb.red, rgb.green, rgb.blue)

        ren.AddActor(actor)

    ren.ResetCamera()
    ren.ResetCameraClippingRange()
    renwin.Render()
    iren.Start()


if __name__ == "__main__":
    load_seg_mesh(pydicom.dcmread(r'D:\Python\DICOM_Seg_Surface_Segmentation\LASegSample.dcm'))
