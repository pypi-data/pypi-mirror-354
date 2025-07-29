"""
Surface mesh VTK reader from hdf5 file
"""

import logging
from pathlib import Path

import h5py
from vtkmodules.util.vtkAlgorithm import VTKPythonAlgorithmBase
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPartitionedDataSet,
    vtkPolyData,
)

from parsli.utils import earth

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)


class VtkMeshReader(VTKPythonAlgorithmBase):
    """
    VTK Surface Mesh hdf5 reader
    """

    def __init__(self):
        VTKPythonAlgorithmBase.__init__(
            self,
            nInputPorts=0,
            nOutputPorts=1,
            outputType="vtkPartitionedDataSet",
        )
        self._file_name = None
        self._proj_spherical = True
        self._longitude_bnd = [0, 360]
        self._latitude_bnd = [-90, 90]
        self._time_index = 0
        self._n_times = -1
        self._vertical_scale = 1
        self._max_depth = 0

    @property
    def file_name(self):
        """
        This property captures the file path to read.
        If set using an invalid path, a ValueError is raised.
        """
        return self._file_name

    @file_name.setter
    def file_name(self, path):
        self._file_name = Path(path)
        if not self._file_name.exists():
            msg = f"Invalid file path: {self._file_name.resolve()}"
            raise ValueError(msg)

        self._n_times = -1
        self._time_index = 0
        self.Modified()

    @property
    def spherical(self):
        """
        This property captures the projection system which can either be spherical or euclidean.
        When set to True (the default), the spherical projection will be used.
        """
        return self._proj_spherical

    @spherical.setter
    def spherical(self, value):
        if self._proj_spherical != value:
            self._proj_spherical = value
            self.Modified()

    @property
    def vertical_scale(self):
        """
        This property captures the vertical scale. The default value is 1.0.
        """
        return self._vertical_scale

    @vertical_scale.setter
    def vertical_scale(self, value):
        if self._vertical_scale != value:
            self._vertical_scale = value
            self.Modified()

    @property
    def maximum_depth(self):
        """
        This property captures the maximum depth based on the mesh read.
        To be accurate, the filter needs to first execute.
        """
        return self._max_depth

    @property
    def available_fields(self):
        """
        This property captures the available fields based on the mesh file.
        Evaluating that property trigger a read on the file.
        """
        if self._file_name is None or not self._file_name.exists():
            return []

        result = set()
        with h5py.File(self._file_name, "r") as hdf:
            meshes = hdf["meshes"]
            for mesh in meshes:
                for name in meshes[mesh]:
                    if isinstance(meshes[mesh][name], h5py.Group):
                        result.add(name)

        return list(result)

    @property
    def longitude_bounds(self):
        """
        This property captures the longitude bounds based on the mesh file.
        """
        return self._longitude_bnd

    @property
    def latitude_bounds(self):
        """
        This property captures the latitude bounds based on the mesh file.
        """
        return self._latitude_bnd

    @property
    def time_index(self):
        """
        This property captures the current time_index.
        The value can only be within [0, number_of_timesteps] range.
        Setting outside values will be ignored.
        """
        return self._time_index

    @time_index.setter
    def time_index(self, v):
        if v == self._time_index:
            return

        if v == 0 or v < self.number_of_timesteps:
            self._time_index = v
            self.Modified()

    @property
    def number_of_timesteps(self):
        """
        This property captures the number of timesteps available in the current file.
        """
        if self._n_times < 0:
            with h5py.File(self._file_name, "r") as hdf:
                meshes = hdf["meshes"]
                for mesh in meshes:
                    n_times = meshes[mesh]["n_time_steps"][()]
                    if n_times > self._n_times:
                        self._n_times = int(n_times)

        return self._n_times

    def _expand_bounds(self, longitude, latitude, depth):
        """Helper to expand longitude and latitude bounds"""
        self._longitude_bnd[0] = min(longitude, self._longitude_bnd[0])
        self._longitude_bnd[1] = max(longitude, self._longitude_bnd[1])

        self._latitude_bnd[0] = min(latitude, self._latitude_bnd[0])
        self._latitude_bnd[1] = max(latitude, self._latitude_bnd[1])

        self._max_depth = max(depth, self._max_depth)

    def RequestData(self, _request, _inInfo, outInfo):
        """VTK Method executed when filter is modified (time_index, file_name, spherical)"""
        if self._file_name is None or not self._file_name.exists():
            return 1

        # Reset bounds
        self._longitude_bnd = [360, 0]
        self._latitude_bnd = [90, -90]
        self._max_depth = 0

        # Read file and generate mesh
        output = self.GetOutputData(outInfo, 0)
        all_meshes = vtkPartitionedDataSet()

        # Projection selection
        insert_pt = earth.insert_spherical if self.spherical else earth.insert_euclidian

        with h5py.File(self._file_name, "r") as hdf:
            meshes = hdf["meshes"]
            n_meshes = len(meshes)
            logger.debug("n_meshes=%s", n_meshes)
            all_meshes.SetNumberOfPartitions(n_meshes)
            for idx, mesh in enumerate(meshes):
                vtk_mesh = vtkPolyData()
                all_meshes.SetPartition(idx, vtk_mesh)

                # Process known names first
                # - coordinates
                vtk_points = vtkPoints()
                vtk_points.SetDataTypeToDouble()
                vtk_mesh.points = vtk_points

                hdf_ds = meshes[mesh]["coordinates"]
                n_points = hdf_ds.shape[0]
                vtk_points.Allocate(n_points)

                for xyz in hdf_ds:
                    self._expand_bounds(xyz[0], xyz[1], -xyz[2] * self._vertical_scale)
                    insert_pt(
                        vtk_points, xyz[0], xyz[1], -xyz[2] * self._vertical_scale
                    )

                # - verts
                vtk_polys = vtkCellArray()
                vtk_mesh.polys = vtk_polys

                hdf_ds = meshes[mesh]["verts"]
                n_cells = hdf_ds.shape[0]
                vtk_polys.Allocate(4 * n_cells)
                assert hdf_ds.shape[1] == 3, "only triangles"

                logger.debug(" %s. mesh %s cells", idx, n_cells)

                for cell in hdf_ds:
                    vtk_polys.InsertNextCell(3)
                    vtk_polys.InsertCellPoint(cell[0])
                    vtk_polys.InsertCellPoint(cell[1])
                    vtk_polys.InsertCellPoint(cell[2])

                time_field_key = f"{self._time_index:012}"
                for name in meshes[mesh]:
                    if isinstance(meshes[mesh][name], h5py.Group):
                        logger.debug(
                            "Field %s: %s",
                            name,
                            meshes[mesh][name][time_field_key].shape,
                        )
                        np_array = meshes[mesh][name][time_field_key][:].ravel()
                        vtk_mesh.cell_data[name] = np_array

        output.ShallowCopy(all_meshes)
        return 1
