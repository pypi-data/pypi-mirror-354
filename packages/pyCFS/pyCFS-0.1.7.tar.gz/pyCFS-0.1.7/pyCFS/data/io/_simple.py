"""
Top-level functions for reading and writing CFS files.

This module provides simple functions to read and write mesh and result data
in the CFS HDF5 file format.

Examples
--------
>>> from pyCFS.data import io
>>> mesh = io.read_mesh(file="example.cfs")
>>> result = io.read_data(file="example.cfs", multistep=1)
>>> mesh, results = io.read_file(file="example.cfs")
>>> io.write_file(file="output.cfs", mesh=mesh, result=results)
"""

from typing import Dict, Optional, Sequence

from pyCFS.data import v_def
from pyCFS.data.io import CFSReader, CFSMeshData, CFSResultContainer, CFSResultArray, CFSWriter


def read_mesh(file: str, verbosity: int = v_def.release):
    """
    Read a mesh from a CFS file.

    Parameters
    ----------
    file : str
        Path to the CFS file.
    verbosity : int, optional
        Verbosity level for logging (default is v_def.release).

    Returns
    -------
    tuple
        A tuple containing the mesh data and region data.

    Examples
    --------
    >>> from pyCFS.data.io import read_mesh
    >>> mesh = read_mesh(file="file.cfs")
    """
    with CFSReader(file, verbosity=verbosity) as f:
        mesh = f.MeshData

    return mesh


def read_data(file: str, multistep=1, verbosity: int = v_def.release) -> CFSResultContainer:
    """
    Read result data from a CFS file.

    Parameters
    ----------
    file : str
        Path to the CFS file.
    multistep : int, optional
        Multi-step ID to read (default is 1).
    verbosity : int, optional
        Verbosity level for logging (default is v_def.release).

    Returns
    -------
    CFSResultContainer
        Result data for the specified multi-step ID.

    Examples
    --------
    >>> from pyCFS.data.io import read_data
    >>> result = read_data(file="file.cfs", multistep=1)
    """
    with CFSReader(file, verbosity=verbosity) as f:
        res = f.get_multi_step_data(multi_step_id=multistep)

    return res


def read_file(file: str, verbosity: int = v_def.release) -> tuple[CFSMeshData, Dict[int, CFSResultContainer]]:
    """
    Read a CFS file and return the mesh and result data for all multi-steps.

    Parameters
    ----------
    file : str
        Path to the CFS file.
    verbosity : int, optional
        Verbosity level for logging (default is v_def.release).

    Returns
    -------
    tuple[CFSMeshData, dict[int, CFSResultContainer]]
        A tuple containing the mesh data and a dictionary mapping multi-step IDs to result data.

    Examples
    --------
    >>> from pyCFS.data.io import read_file
    >>> mesh, result = read_file(file="file.cfs")
    """

    res_dict = {}
    with CFSReader(file, verbosity=verbosity) as f:
        mesh = f.MeshData
        for mid in f.MultiStepIDs:
            res_dict[mid] = f.get_multi_step_data(multi_step_id=mid)

    return mesh, res_dict


def write_file(
    file: str,
    mesh: Optional[CFSMeshData] = None,
    result: (
        Dict[int, CFSResultContainer]
        | Sequence[CFSResultContainer]
        | CFSResultContainer
        | Sequence[CFSResultArray]
        | None
    ) = None,
    verbosity: int = v_def.release,
):
    """
    Write mesh and result data to a CFS file.

    Parameters
    ----------
    file : str
        Path to the CFS file to write.
    mesh : CFSMeshData, optional
        Mesh data to write to the file. If None, only result data is written (if provided).
    result : dict[int, CFSResultContainer] or Sequence[CFSResultContainer] or CFSResultContainer or Sequence[CFSResultArray], optional
        Result data to write.
        Can be a dictionary mapping multi-step IDs to result containers, a list of result containers,
        a single result container, or a list of result arrays. If None, only mesh data is written (if provided).
    verbosity : int, optional
        Verbosity level for logging (default is v_def.release).

    Examples
    --------
    >>> from pyCFS.data.io import write_file
    >>> write_file(file="file.cfs", mesh=mesh)
    >>> write_file(file="file.cfs", mesh=mesh, result=result)
    >>> write_file(file="file.cfs", mesh=mesh, result={1: result_1, 2: result_2})
    >>> write_file(file="file.cfs", mesh=mesh, result=[result_1, result_2])
    """
    with CFSWriter(file, verbosity=verbosity) as f:
        f.create_file(mesh=mesh)

        if isinstance(result, dict):
            for mid in result:
                res_data = CFSResultContainer.require_container(result=result[mid], verbosity=verbosity)
                res_data.check_result(mesh=mesh)
                f.write_multistep(result=res_data, multi_step_id=mid, perform_check=False)
        elif isinstance(result, Sequence) and all([isinstance(item, CFSResultContainer) for item in result]):
            for midx, item in enumerate(result):
                res_data = CFSResultContainer.require_container(result=item, verbosity=verbosity)  # type: ignore[arg-type]
                res_data.check_result(mesh=mesh)
                f.write_multistep(result=res_data, multi_step_id=midx + 1, perform_check=False)
        elif (
            isinstance(result, CFSResultContainer)
            or isinstance(result, Sequence)
            and all([isinstance(item, CFSResultArray) for item in result])
        ):
            res_data = CFSResultContainer.require_container(result=result, verbosity=verbosity)  # type: ignore[arg-type]
            res_data.check_result(mesh=mesh)
            f.write_multistep(result=res_data, multi_step_id=1, perform_check=False)


def file_info(file: str) -> str:
    """
    Read information from a CFS file and return a summary string.

    Parameters
    ----------
    file : str
        Path to the CFS file.

    Returns
    -------
    str
        A string summarizing the contents of the CFS file, including mesh and result data.

    Examples
    --------
    >>> from pyCFS.data.io import file_info
    >>> file_info(file="example.cfs")
    """
    with CFSReader(file) as f:
        return str(f)
