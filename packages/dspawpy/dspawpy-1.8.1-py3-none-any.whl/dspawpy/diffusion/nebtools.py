from typing import Optional

from loguru import logger


def _zip_folder(folder_path: str, output_path: str):
    import os

    absdir1 = os.path.abspath(folder_path)
    absdir2 = os.path.abspath(output_path)
    import zipfile

    with zipfile.ZipFile(absdir2, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(absdir1):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, absdir1))


def get_distance(spo1, spo2, lat1, lat2):
    """Calculate the distance between two structures based on their fractional coordinates and cell parameters

    Parameters
    ----------
    spo1 : np.ndarray
        Scores coordinate list 1
    spo2 : np.ndarray
        Fractional coordinate list 2
    lat1 : np.ndarray
        Cell 1
    lat2 : np.ndarray
        Cell 2

    Returns
    -------
    float
        Distance

    Examples
    --------
    First, read the structure information

    >>> from dspawpy.io.structure import read
    >>> s1 = read('dspawpy_proj/dspawpy_tests/inputs/2.15/01/structure01.as')[0]
    >>> s2 = read('dspawpy_proj/dspawpy_tests/inputs/2.15/02/structure02.as')[0]

    Calculate the distance between two configurations

    >>> from dspawpy.diffusion.nebtools import get_distance
    >>> dist = get_distance(s1.frac_coords, s2.frac_coords, s1.lattice.matrix, s2.lattice.matrix)
    >>> print('The distance between the two configurations is:', dist, 'Angstrom')
    The distance between the two configurations is: 0.476972808803491 Angstrom

    """
    import numpy as np

    diff_spo = spo1 - spo2  # Fractional coordinate difference
    avglatv = 0.5 * (lat1 + lat2)  # Average lattice vector
    pbc_diff_spo = set_pbc(diff_spo)  # Cartesian coordinate difference
    # Dot product of fractional coordinates with average lattice, converted back to Cartesian coordinates
    pbc_diff_pos = np.dot(pbc_diff_spo, avglatv)  # Cartesian coordinate difference
    distance = np.sqrt(np.sum(pbc_diff_pos**2))

    return distance


def get_neb_subfolders(directory: str = ".", return_abs: bool = False):
    r"""List the subfolder names under the directory path and sort them by numerical size

    ```

        Only retain NEB subfolder paths that are of the form 00, 01 numeric types

        Parameters
        ----------
        subfolders:
            List of subfolder names
        return_abs : bool, optional
            Whether to return absolute paths, default is False

        Returns
        -------
        subfolders:
            Sorted list of subfolder names

        Examples
        --------
        >>> from dspawpy.diffusion.nebtools import get_neb_subfolders
        >>> directory = 'dspawpy_proj/dspawpy_tests/inputs/2.15'
        >>> get_neb_subfolders(directory)
        ['00', '01', '02', '03', '04']

    """
    import os

    absdir = os.path.abspath(directory)
    raw_subfolders = next(os.walk(absdir))[1]
    subfolders = []
    for subfolder in raw_subfolders:
        try:
            assert 0 <= int(subfolder) < 100
            subfolders.append(subfolder)
        except Exception:
            pass
    subfolders.sort()  # Sort in ascending order
    if return_abs:
        subfolders = [
            os.path.abspath(os.path.join(absdir, subfolder)) for subfolder in subfolders
        ]
    return subfolders


def plot_barrier(
    datafile: str = "neb.h5",
    directory: Optional[str] = None,
    ri: Optional[float] = None,
    rf: Optional[float] = None,
    ei: Optional[float] = None,
    ef: Optional[float] = None,
    method: str = "PchipInterpolator",
    figname: Optional[str] = "neb_barrier.png",
    show: bool = True,
    raw: bool = False,
    verbose: bool = False,
    **kwargs,
):
    r"""Call the scipy.interpolate interpolation algorithm to fit the NEB barrier and plot

    Parameters
    ----------
    datafile:
        Path to neb.h5 or neb.json file
    directory:
        NEB calculation path
    ri:
        Initial reaction coordinate
    rf:
        Final state reaction coordinate
    ei:
        Initial state self-consistent energy
    ef:
        Final state self-consistent energy
    method : str, optional
        Interpolation algorithm, default 'PchipInterpolator'
    figname : str, optional
        Barrier image name, default 'neb_barrier.png'
    show : bool, optional
        Whether to display the interactive interface, default True
    raw : bool, optional
        Whether to return plotting data to CSV

    Raises
    ------
    ImportError
        The specified interpolation algorithm does not exist in scipy.interpolate
    ValueError
        The parameters passed to the interpolation algorithm do not meet the requirements of the algorithm

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import plot_barrier
    >>> import matplotlib.pyplot as plt

    Comparing different interpolation algorithms

    >>> plot_barrier(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', method='interp1d', kind=2, figname=None, show=False)
    >>> plot_barrier(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', method='interp1d', kind=3, figname=None, show=False)
    >>> plot_barrier(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', method='CubicSpline', figname=None, show=False)
    >>> plot_barrier(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', method='pchip', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/barrier_comparison.png', show=False) # doctest: +ELLIPSIS
    ==> ...barrier_comparison.png...

    Attempt to read neb.h5 file or neb.json file

    >>> plot_barrier(datafile='dspawpy_proj/dspawpy_tests/inputs/2.15/neb.h5', method='pchip', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/barrier_h5.png', show=False) # doctest: +ELLIPSIS
    ==> ...barrier_h5.png
    >>> plot_barrier(datafile='dspawpy_proj/dspawpy_tests/inputs/2.15/neb.json', method='pchip', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/barrier_json.png', show=False) # doctest: +ELLIPSIS
    ==> ...barrier_json.png...

    """
    import os

    import numpy as np

    if directory is not None:
        # read data
        subfolders, resort_mfs, rcs, ens, dEs = _getef(os.path.abspath(directory))

    elif datafile:
        from dspawpy.io.utils import get_absfile

        absfile = get_absfile(
            datafile,
            task="neb",
            verbose=verbose,
        )  # -> return either .h5 or .json
        if absfile.endswith(".h5"):
            from dspawpy.io.read import load_h5

            neb = load_h5(absfile)
            if "/BarrierInfo/ReactionCoordinate" in neb.keys():
                reaction_coordinate = neb["/BarrierInfo/ReactionCoordinate"]
                energy = neb["/BarrierInfo/TotalEnergy"]
            else:  # old version
                reaction_coordinate = neb["/Distance/ReactionCoordinate"]
                energy = neb["/Energy/TotalEnergy"]
        elif absfile.endswith(".json"):
            with open(absfile) as fin:
                from json import load

                neb = load(fin)
            if "BarrierInfo" in neb.keys():
                reaction_coordinate = neb["BarrierInfo"]["ReactionCoordinate"]
                energy = neb["BarrierInfo"]["TotalEnergy"]
            else:  # old version
                reaction_coordinate = neb["Distance"]["ReactionCoordinate"]
                energy = neb["Energy"]["TotalEnergy"]
        else:
            raise ValueError("only h5 and json file are supported")

        x = reaction_coordinate  # No need to sum when reading from neb.h5/json

        y = [x - energy[0] for x in energy]
        # initial and final info
        if ri is not None:  # add initial reaction coordinate
            x.insert(0, ri)
        if rf is not None:  # add final reaction coordinate
            x.append(rf)

        if ei is not None:  # add initial energy
            y.insert(0, ei)
        if ef is not None:  # add final energy
            y.append(ef)

        rcs = np.asarray(x)
        dEs = np.asarray(y)

    else:
        raise ValueError("Please specify directory or datafile!")

    # import scipy interpolater
    try:
        interpolate_method = getattr(
            __import__("scipy.interpolate", fromlist=[method]),
            method,
        )
    except Exception:
        raise ImportError(f"No scipy.interpolate.{method} method！")
    # call the interpolater to interpolate with given kwargs
    try:
        inter_f = interpolate_method(rcs, dEs, **kwargs)
    except Exception:
        raise ValueError(f"Please check whether {kwargs} is valid for {method}！")

    xnew = np.linspace(rcs[0], rcs[-1], 100)
    ynew = inter_f(xnew)

    if raw:
        import polars as pl

        pl.DataFrame({"x_raw": rcs, "y_raw": dEs}).write_csv(
            "raw_xy.csv",
        )
        pl.DataFrame({"x_interpolated": xnew, "y_interpolated": ynew}).write_csv(
            "raw_interpolated_xy.csv",
        )

    # plot
    import matplotlib.pyplot as plt

    if kwargs:
        plt.plot(xnew, ynew, label=method + str(kwargs))
    else:
        plt.plot(xnew, ynew, label=method)
    plt.scatter(rcs, dEs, c="r")
    plt.xlabel("Reaction Coordinate (Å)")
    plt.ylabel("Energy (eV)")
    plt.legend()

    plt.tight_layout()
    # save and show
    if figname:
        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        print(f"==> {absfig}")
    if show:
        plt.show()


def plot_neb_converge(
    neb_dir: str,
    image_key: str = "01",
    show: bool = True,
    figname: str = "neb_conv.png",
    raw=False,
    verbose: bool = False,
):
    """Specify the NEB calculation path, plot the NEB convergence process graph

    Parameters
    ----------
    neb_dir:
        Path to the neb.h5 / neb.json file or the folder containing the neb.h5 / neb.json file
    image_key:
        The index of the configuration, default "01"
    show:
        Interactive plotting
    image_name:
        NEB convergence plot name, default "neb_conv.png"
    raw:
        Whether to output plot data to a CSV file

    Returns
    -------
    ax1, ax2 : matplotlib.axes.Axes
        Two Axes objects for the subplots

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import plot_neb_converge
    >>> result = plot_neb_converge(neb_dir='dspawpy_proj/dspawpy_tests/inputs/2.15', image_key='01', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge1.png',show=False) # doctest: +ELLIPSIS
    ==> ...neb_converge1.png...
    >>> result = plot_neb_converge(neb_dir='dspawpy_proj/dspawpy_tests/inputs/2.15/neb.h5', image_key='02', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge2.png',show=False) # doctest: +ELLIPSIS
    ==> ...neb_converge2.png...
    >>> result = plot_neb_converge(neb_dir='dspawpy_proj/dspawpy_tests/inputs/2.15/neb.json', image_key='03', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_converge3.png',show=False, raw=True) # doctest: +ELLIPSIS
    ==> ...neb_converge3.png...

    """
    import os

    import numpy as np

    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(neb_dir, "neb", verbose=verbose)
    if absfile.endswith("h5"):
        import h5py

        neb_total = h5py.File(absfile)
        # new output (>=2022B)
        if "/LoopInfo/01/MaxForce" in neb_total.keys():
            maxforce = np.asarray(neb_total.get("/LoopInfo/" + image_key + "/MaxForce"))
        else:  # old output
            maxforce = np.asarray(
                neb_total.get("/Iteration/" + image_key + "/MaxForce")
            )

        if "/LoopInfo/01/TotalEnergy" in neb_total.keys():  # new output (>=2022B)
            total_energy = np.asarray(
                neb_total.get("/LoopInfo/" + image_key + "/TotalEnergy"),
            )
        else:  # old output
            total_energy = np.asarray(
                neb_total.get("/Iteration/" + image_key + "/TotalEnergy"),
            )

    elif absfile.endswith("json"):
        with open(absfile) as fin:
            from json import load

            neb_total = load(fin)
        if "LoopInfo" in neb_total.keys():
            neb = neb_total["LoopInfo"][image_key]
        else:
            neb = neb_total["Iteration"][image_key]
        maxforce = []
        total_energy = []
        for n in neb:
            maxforce.append(n["MaxForce"])
            total_energy.append(n["TotalEnergy"])

        maxforce = np.asarray(maxforce)
        total_energy = np.asarray(total_energy)

    else:
        raise ValueError("Only h5 and json file are supported")

    x = np.arange(len(maxforce))

    force = maxforce
    energy = total_energy

    if raw:
        import polars as pl

        pl.DataFrame({"x": x, "force": force, "energy": energy}).write_csv(
            "neb_conv.csv",
        )

    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(x, force, label="Max Force", c="black")
    ax1.set_xlabel("Number of ionic step")
    ax1.set_ylabel("Force (eV/Å)")
    ax2 = ax1.twinx()
    ax2.plot(x, energy, label="Energy", c="r")  # type: ignore
    ax2.set_xlabel("Number of ionic step")
    ax2.set_ylabel("Energy (eV)")
    ax2.ticklabel_format(
        useOffset=False
    )  # Display absolute values on the y-axis instead of relative values
    fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

    plt.tight_layout()
    # save and show
    if figname:
        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        print(f"==> {absfig}")
    if show:
        plt.show()

    return ax1, ax2


def printef(directory: str):
    """Print the energies and forces of each configuration during NEB calculations

    Parameters
    ----------
    directory:
        Directory for NEB calculations, defaulting to the current directory

    Returns
    -------
    Prints the energy and forces for each configuration

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import printef
    >>> printef(directory='dspawpy_proj/dspawpy_tests/inputs/2.15')
    shape: (5, 5)
    ┌────────────┬─────────────┬──────────┬───────────────┬──────────┐
    │ FolderName ┆ Force(eV/Å) ┆ RC(Å)    ┆ Energy(eV)    ┆ E-E0(eV) │
    ╞════════════╪═════════════╪══════════╪═══════════════╪══════════╡
    │ 00         ┆ 0.180272    ┆ 0.0      ┆ -39637.097656 ┆ 0.0      │
    │ 01         ┆ 0.014094    ┆ 0.542789 ┆ -39637.019531 ┆ 0.079814 │
    │ 02         ┆ 0.026337    ┆ 1.0868   ┆ -39636.878906 ┆ 0.218265 │
    │ 03         ┆ 0.024798    ┆ 1.588367 ┆ -39637.0      ┆ 0.100043 │
    │ 04         ┆ 0.234429    ┆ 2.089212 ┆ -39637.089844 ┆ 0.008414 │
    └────────────┴─────────────┴──────────┴───────────────┴──────────┘
    """
    import numpy as np

    from dspawpy.diffusion.nebtools import _getef

    arr = np.asarray(_getef(directory))
    data = {
        "FolderName": arr[0],
        "Force(eV/Å)": arr[1],
        "RC(Å)": arr[2],
        "Energy(eV)": arr[3],
        "E-E0(eV)": arr[4],
    }
    import polars as pl

    _df = pl.DataFrame(data)
    col_names = [col_name for col_name in _df.columns if col_name != "FolderName"]
    df = _df.with_columns(pl.col(col_names).cast(pl.Float32, strict=False))
    print(df)


def restart(directory: str = ".", output: str = "bakfile"):
    """Archive and compress old NEB tasks, and prepare for continuation at the original path

    Parameters
    ----------
    directory:
        Old NEB task path, default current path
    output:
        Backup folder path, default is to create a bakfile folder in the current path for backup;
        Alternatively, you can specify any path, but it cannot be the same as the current path

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import restart
    >>> from shutil import copytree
    >>> copytree('dspawpy_proj/dspawpy_tests/inputs/2.15', 'dspawpy_proj/dspawpy_tests/outputs/doctest/neb4bk2', dirs_exist_ok=True)
    'dspawpy_proj/dspawpy_tests/outputs/doctest/neb4bk2'
    >>> restart(directory='dspawpy_proj/dspawpy_tests/outputs/doctest/neb4bk2', output='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_backup') # doctest: +ELLIPSIS
    ==> ...neb_backup...

    The preparation for the continuation calculation may take a long time to complete, please be patient

    """
    import os
    import shutil

    from dspawpy.io.write import handle_duplicated_output

    absdir = os.path.abspath(directory)
    absolute_output = handle_duplicated_output(os.path.abspath(output))

    subfolders = get_neb_subfolders(absdir, return_abs=True)  # Get subfolder paths
    os.makedirs(absolute_output, exist_ok=True)  # Create the bakfile folder
    # First process subfolders 00, 01...
    for subfolder_old in subfolders:
        folder_index = subfolder_old.split("/")[-1]  # 00，01...
        subfolder_back = os.path.join(
            absolute_output, folder_index
        )  # Backup subfolders to this location
        shutil.move(subfolder_old, subfolder_back)
        os.makedirs(subfolder_old, exist_ok=True)  # Original folder cleared

        latestStructureFile = f"{subfolder_back}/latestStructure{folder_index}.as"
        structureFile = f"{subfolder_back}/structure{folder_index}.as"

        # Copy the structure file to the original path for continuation calculation; use the latest structure file (latestStructureFile) if it exists, otherwise use s_in_old (s), and raise an error if neither exists
        s_in_old = f"{subfolder_old}/structure{folder_index}.as"
        if os.path.isfile(latestStructureFile):
            shutil.copy(latestStructureFile, s_in_old)
        elif os.path.isfile(structureFile):
            shutil.copy(structureFile, s_in_old)
        else:
            raise FileNotFoundError(
                f"{latestStructureFile} and {structureFile} do not exist!"
            )

        # Temporarily placed in the backup main path; if neither exists, an error has already been raised earlier
        ls_bk = os.path.join(absdir, f"latestStructure{folder_index}.as")
        s_bk = os.path.join(absdir, f"structure{folder_index}.as")
        if os.path.isfile(latestStructureFile):
            shutil.copy(latestStructureFile, ls_bk)
        if os.path.isfile(structureFile):
            shutil.copy(structureFile, s_bk)

        # Handle subfolders in the backup path
        zf = f"{absolute_output}/{folder_index}.zip"
        _zip_folder(subfolder_back, zf)  # Compress subfolder
        # Empty the backup subfolder
        for f in os.listdir(subfolder_back):
            fpath = os.path.join(subfolder_back, f)
            if os.path.isfile(fpath):
                os.remove(fpath)
            else:
                shutil.rmtree(fpath)

        # Move the archive and structure files in
        shutil.move(zf, f"{subfolder_back}/{folder_index}.zip")
        if os.path.isfile(ls_bk) and os.path.isfile(s_bk):
            shutil.move(ls_bk, f"{subfolder_back}/latestStructure{folder_index}.as")
            shutil.move(s_bk, f"{subfolder_back}/structure{folder_index}.as")
        elif os.path.isfile(ls_bk):
            shutil.move(ls_bk, f"{subfolder_back}/latestStructure{folder_index}.as")
        elif os.path.isfile(s_bk):
            shutil.move(s_bk, f"{subfolder_back}/structure{folder_index}.as")
        else:
            raise FileNotFoundError(f"Both {ls_bk} and {s_bk} not found")

    # Process individual files in the main directory of the old NEB folder
    # Backup neb.h5, neb.json, and DS-PAW.log
    tmp_dir = os.path.join(absolute_output, "tmp")
    os.makedirs(tmp_dir, exist_ok=True)
    if os.path.isfile(f"{absdir}/neb.h5"):
        shutil.move(f"{absdir}/neb.h5", f"{tmp_dir}/neb.h5")

    if os.path.isfile(f"{absdir}/neb.json"):
        shutil.move(f"{absdir}/neb.json", f"{tmp_dir}/neb.json")

    if len(os.listdir(tmp_dir)) > 0:  # If there are data files
        _zip_folder(tmp_dir, f"{absolute_output}/neb_data.zip")
        for f in os.listdir(tmp_dir):
            os.remove(os.path.join(tmp_dir, f))
        os.removedirs(tmp_dir)

    if os.path.isfile(f"{absdir}/DS-PAW.log"):
        shutil.move(f"{absdir}/DS-PAW.log", f"{absolute_output}/DS-PAW.log")

    print(f"==> {absolute_output}")


def set_pbc(spo):
    """Shift fractional coordinate components into the [-0.5, 0.5) interval according to periodic boundary conditions.

    Parameters
    ----------
    spo : np.ndarray or list
        A list of fractional coordinates

    Returns
    -------
    pbc_spo : np.ndarray
        A list of fractional coordinates satisfying periodic boundary conditions

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import set_pbc
    >>> set_pbc([-0.6, 1.2, 2.3])
    array([0.4, 0.2, 0.3])

    """
    # wrap into [-0.5, 0.5)
    import numpy as np

    pbc_spo = np.mod(np.asarray(spo) + 0.5, 1.0) - 0.5

    return pbc_spo


def summary(
    directory: str = ".",
    raw=False,
    show_converge=False,
    outdir: Optional[str] = None,
    **kwargs,
):
    r"""Summary of NEB task completion, execute the following steps in order:

    - 1. Print the forces, reaction coordinates, energy, and energy differences from the initial configuration for each structure
    - 2. Plot the energy barrier diagram
    - 3. Plot and save the convergence processes of energy and forces during the structure optimization

    Parameters
    ----------
    directory:
        NEB path, default to the current path
    raw:
        Whether to save the plot data to a CSV file
    show_converge:
        Whether to display energy and force convergence plots of the structural optimization process, default is not displayed
    outdir:
        Path to save the convergence process figure, default to directory
    **kwargs : dict
        Parameters passed to plot_barrier

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import summary
    >>> directory = 'dspawpy_proj/dspawpy_tests/inputs/2.15' # Path for NEB calculation, default to current path
    >>> summary(directory, show=False, figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_barrier.png') # doctest: +ELLIPSIS
    shape: (5, 5)
    ┌────────────┬─────────────┬──────────┬───────────────┬──────────┐
    │ FolderName ┆ Force(eV/Å) ┆ RC(Å)    ┆ Energy(eV)    ┆ E-E0(eV) │
    ╞════════════╪═════════════╪══════════╪═══════════════╪══════════╡
    │ 00         ┆ 0.180272    ┆ 0.0      ┆ -39637.097656 ┆ 0.0      │
    │ 01         ┆ 0.014094    ┆ 0.542789 ┆ -39637.019531 ┆ 0.079814 │
    │ 02         ┆ 0.026337    ┆ 1.0868   ┆ -39636.878906 ┆ 0.218265 │
    │ 03         ┆ 0.024798    ┆ 1.588367 ┆ -39637.0      ┆ 0.100043 │
    │ 04         ┆ 0.234429    ┆ 2.089212 ┆ -39637.089844 ┆ 0.008414 │
    └────────────┴─────────────┴──────────┴───────────────┴──────────┘
    ==> ...neb_barrier.png...
    ==> ...converge.png...
    ==> ...converge.png...
    ==> ...converge.png...

    >>> summary(directory, show=False, figname='dspawpy_proj/dspawpy_tests/outputs/doctest/neb_barrier.png', outdir="dspawpy_proj/dspawpy_tests/outputs/doctest/neb_summary") # doctest: +ELLIPSIS
    shape: (5, 5)
    ┌────────────┬─────────────┬──────────┬───────────────┬──────────┐
    │ FolderName ┆ Force(eV/Å) ┆ RC(Å)    ┆ Energy(eV)    ┆ E-E0(eV) │
    ╞════════════╪═════════════╪══════════╪═══════════════╪══════════╡
    │ 00         ┆ 0.180272    ┆ 0.0      ┆ -39637.097656 ┆ 0.0      │
    │ 01         ┆ 0.014094    ┆ 0.542789 ┆ -39637.019531 ┆ 0.079814 │
    │ 02         ┆ 0.026337    ┆ 1.0868   ┆ -39636.878906 ┆ 0.218265 │
    │ 03         ┆ 0.024798    ┆ 1.588367 ┆ -39637.0      ┆ 0.100043 │
    │ 04         ┆ 0.234429    ┆ 2.089212 ┆ -39637.089844 ┆ 0.008414 │
    └────────────┴─────────────┴──────────┴───────────────┴──────────┘
    ==> ...neb_barrier.png...
    ==> ...converge.png...
    ==> ...converge.png...
    ==> ...converge.png...

    If inifin=False, the user must place a converged scf.h5 or system.json in the initial and final state subfolders.

    """
    import os

    # 1. Plot the energy barrier curve
    absdir = os.path.abspath(directory)
    printef(absdir)

    # 2. Print the forces, reaction coordinates, energy, and energy difference from the initial configuration for each structure
    import matplotlib.pyplot as plt

    plt.clf()  # Clear the canvas before plotting
    plot_barrier(directory=absdir, raw=raw, **kwargs)

    # 3. Plot and save the convergence processes of energy and forces during the structure optimization to each configuration folder
    subfolders = get_neb_subfolders(absdir)
    for subfolder in subfolders[1 : len(subfolders) - 1]:
        if outdir:
            absolute_output = os.path.abspath(outdir)
            os.makedirs(os.path.join(absolute_output, subfolder), exist_ok=True)
            pngfile = f"{absolute_output}/{subfolder}/converge.png"
        else:
            pngfile = (
                f"dspawpy_proj/dspawpy_tests/outputs/doctest/{subfolder}/converge.png"
            )

        plot_neb_converge(
            neb_dir=absdir,
            image_key=subfolder,
            figname=pngfile,
            raw=raw,
            show=show_converge,
        )
    plt.clf()


def write_movie_json(
    preview: bool = False,
    directory: str = ".",
    step: int = -1,
    dst: Optional[str] = None,
):
    DeprecationWarning("Please use write_json_chain() instead")
    write_json_chain(preview=preview, directory=directory, step=step, dst=dst)


def write_json_chain(
    preview: bool = False,
    directory: str = ".",
    step: int = -1,
    dst: Optional[str] = None,
    ignorels=False,
):
    r"""Read information after NEB calculation or initial interpolation, and save it as neb_chain*.json files

    View the structure and other information by opening the file with Device Studio.

    Parameters
    ----------
    preview:
        Whether to enable preview mode, default is no
    directory:
        Directory where the computation results are located. Default to the current path
    step:
        - Ion step number. Default is -1, which reads the entire NEB calculation process information; at this time, the priority is latestStructure.as > h5 > json
        - 0 indicates the initial insertion structure (uncompleted ionic step);
        - 1 represents the first ionic step, and so on
    dst:
        Save path, default to directory
    ignorels:
        Whether to ignore the latestStructure.as file when step=-1, default is no

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import write_json_chain

    To observe the entire trajectory change process after NEB computation, simply specify the NEB computation path.

    >>> write_json_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    structure info collected from latestStructure.as
    ==> ...neb_chain_last.json...

    To observe the structure of the nth ion step after NEB computation, set step to n, noting that step is counted starting from 1.

    >>> write_json_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=1, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> ...neb_chain_1.json...

    If the specified step number exceeds the actual ion steps completed by NEB, it will be automatically adjusted to the final step.

    >>> write_json_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=10, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> ...neb_chain_10.json...
    >>> write_json_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=100, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> ...neb_chain_last.json...

    Additionally, to preview the initial insertion structure, set preview to True and specify the directory as the main path of the NEB calculation

    >>> write_json_chain(preview=True, directory='dspawpy_proj/dspawpy_tests/inputs/2.15', dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> ...neb_chain_init.json...

    """
    import os

    absdir = os.path.abspath(directory)
    if preview or step == 0:  # preview mode
        raw = get_raw_from_structure(absdir)
    elif step == -1:  # priority latestStructure.as > h5 > json
        if ignorels:
            raw = _from_h5(absdir, step)
        else:
            try:  # read ls.as
                raw = _from_structures(absdir, ls=True)
                print("structure info collected from latestStructure.as")
            except FileNotFoundError:
                raw = _from_h5(absdir, step)
    else:
        raw = _from_h5(absdir, step)

    new = []
    assert raw is not None
    if dst is not None:
        abs_dst = os.path.abspath(dst)
        os.makedirs(abs_dst, exist_ok=True)
        new.append(f"{abs_dst}/{raw[0]}")
        for i in range(1, len(raw)):
            new.append(raw[i])
        _dump_neb_chain_json(new)
    else:
        _dump_neb_chain_json(raw)


def write_xyz(
    preview: bool = False,
    directory: str = ".",
    step: int = -1,
    dst: Optional[str] = None,
):
    DeprecationWarning("Please use write_xyz_chain() instead")
    write_xyz_chain(preview=preview, directory=directory, step=step, dst=dst)


def get_raw_from_structure(dire: str):
    try:
        raw = _from_structures(dire)
        return raw
    except FileNotFoundError:
        print("No structure file")
    except Exception as e:
        print(e)


def write_xyz_chain(
    preview: bool = False,
    directory: str = ".",
    step: int = -1,
    dst: Optional[str] = None,
    ignorels=False,
):
    r"""Write the NEB structure chains to an xyz trajectory file for visualization

    Parameters
    ----------
    preview:
        Whether to enable preview mode, default is no
    directory:
        Directory where the calculation results are located. Default to the current path
    step:
        - Ion step number. Default is -1, which reads the entire NEB calculation process information; at this time, the priority is latestStructure.as > h5 > json
        - 0 indicates the initial inserted structure (not completed ion step);
        - 1 represents the first ionic step, and so on
    dst:
        Save path, default to directory
    ignorels:
        Whether to ignore the latestStructure.as file when step=-1, default is no

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import write_xyz_chain

    To observe the entire process of trajectory changes after NEB calculation, simply specify the NEB calculation path.

    >>> write_xyz_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    structure info collected from latestStructure.as
    ==> ...neb_chain_last.xyz...

    To observe the structure of the nth ion step after NEB calculation, set step to n, note that step is counted starting from 1

    >>> write_xyz_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=1, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> ...neb_chain_1.xyz...

    If the specified step number exceeds the actual ion steps completed by NEB, it will be automatically adjusted to the final step.

    >>> write_xyz_chain(directory='dspawpy_proj/dspawpy_tests/inputs/2.15', step=10, dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> ...neb_chain_10.xyz...

    Additionally, to preview the initial insertion structure, set preview to True and specify the directory as the main path of the NEB calculation

    >>> write_xyz_chain(preview=True, directory='dspawpy_proj/dspawpy_tests/inputs/2.15', dst='dspawpy_proj/dspawpy_tests/outputs/doctest') # doctest: +ELLIPSIS
    ==> ...neb_chain_init.xyz...

    """
    import os

    absdir = os.path.abspath(directory)
    if preview or step == 0:  # preview mode, write neb_chain_init.xyz from structure.as
        raw = get_raw_from_structure(absdir)
    elif step == -1:  # Priority: latestStructure.as > h5 > json
        if ignorels:
            raw = _from_h5(absdir, step)
        else:
            try:  # read ls.as
                raw = _from_structures(absdir, ls=True)
                print("structure info collected from latestStructure.as")
            except FileNotFoundError:
                raw = _from_h5(absdir, step)
    else:
        raw = _from_h5(absdir, step)

    new = []
    assert raw is not None
    if dst is not None:
        abs_dst = os.path.abspath(dst)
        os.makedirs(abs_dst, exist_ok=True)
        new.append(f"{abs_dst}/{raw[0]}")
        for i in range(1, len(raw)):
            new.append(raw[i])
        _dump_neb_xyz(new)
    else:
        _dump_neb_xyz(raw)


def _dump_neb_xyz(raw):
    """Dump the JSON file to the output based on the previously collected data lists"""
    import os

    import numpy as np

    (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,
        Poses,  # Nimage x Natom x 3 , read
        Latvs,  # Nimage x 9
        Elems,  # Nimage x Natom
        Fixs,  # Natom x 3
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    ) = raw

    # Write to file
    xyzfile = output[:-5] + ".xyz"
    absolute_output = os.path.abspath(xyzfile)
    Nstep = len(subfolders)  # Select ion step, display configuration chain
    with open(absolute_output, "w") as f:
        # Nstep
        for n in range(Nstep):
            elements = Elems[n]  # For each configuration
            # Number of atoms remains constant, this is the total number of elements without merging
            f.write("%d\n" % len(elements))
            # lattice
            f.write(
                'Lattice="%f %f %f %f %f %f %f %f %f" Properties=species:S:1:pos:R:3 pbc="T T T"\n'
                % (
                    Latvs[n, 0],
                    Latvs[n, 1],
                    Latvs[n, 2],
                    Latvs[n, 3],
                    Latvs[n, 4],
                    Latvs[n, 5],
                    Latvs[n, 6],
                    Latvs[n, 7],
                    Latvs[n, 8],
                ),
            )
            lat = Latvs[n].reshape(3, 3)
            if iDirects[n]:
                Poses[n] = np.dot(Poses[n], lat)

            # position and element
            for i in range(len(elements)):
                f.write(
                    "%s %f %f %f\n"
                    % (elements[i], Poses[n, i, 0], Poses[n, i, 1], Poses[n, i, 2]),
                )

    print(f"==> {absolute_output}")


def _from_structures(directory: str, ls: bool = False):
    """Read structure information from structure00.as, structure01.as, ..., etc.,
    Write to neb_chain_init so that it can be observed with DeviceStudio

    Parameters
    ----------
    directory:
        NEB calculation path, default to the current path
    ls:
        Whether it is the latest configuration

    Returns
    -------
    Arrays for JSON files

    """
    import os

    absdir = os.path.abspath(directory)
    if ls:
        output = "neb_chain_last.json"
    else:
        output = "neb_chain_init.json"
    step = 1

    subfolders = get_neb_subfolders(absdir)
    nimage = len(subfolders)
    import numpy as np

    reactionCoordinates = np.zeros(shape=nimage)  # optional
    totalEnergies = np.zeros(shape=nimage)  # optional
    maxForces = np.zeros(shape=nimage)  # optional
    tangents = np.zeros(shape=nimage)  # optional
    MaxForces = np.zeros(shape=(nimage, step + 1))  # optional
    TotalEnergies = np.zeros(shape=(nimage, step + 1))  # optional

    Poses = []  # nimage x Natom x 3 , read
    Elems = []  # nimage x Natom, read
    Latvs = []  # nimage x 9, read

    iDirects = []  # read coordinate type
    from dspawpy.io.structure import read

    for i, folder in enumerate(subfolders):
        if ls and i != 0 and i != len(subfolders) - 1:
            structure_path = os.path.join(absdir, folder, f"latestStructure{folder}.as")
        else:
            structure_path = os.path.join(absdir, folder, f"structure{folder}.as")
        if not os.path.isfile(structure_path):
            raise FileNotFoundError(f"No {structure_path}！")
        structure = read(structure_path, task="free")[0]
        ele = [str(i) for i in structure.species]
        lat = structure.lattice.matrix
        Elems.append(ele)
        Latvs.append(lat)
        with open(structure_path) as f:
            lines = f.readlines()
            coordinateType = lines[6].split()[0]
            if coordinateType == "Direct":
                iDirect = True
                Poses.append(structure.frac_coords)
            elif coordinateType == "Cartesian":
                iDirect = False
                Poses.append(structure.cart_coords)
            else:
                raise ValueError(
                    f"coordinateType in {structure_path} is neither Direct nor Cartesian!",
                )
            iDirects.append(iDirect)
    Natom = len(Elems[0])

    # reshape data
    Poses = np.asarray(Poses).reshape((nimage, Natom, 3))
    Elems = np.asarray(Elems).reshape((nimage, Natom))
    Latvs = np.asarray(Latvs).reshape((nimage, 9))
    Fixs = np.zeros(shape=(Natom, 3))  # optional

    return (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,
        Poses,
        Latvs,
        Elems,
        Fixs,
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    )


def _from_h5(directory: str, step: int):
    """Read structure and energy information from h5 files under the NEB path, starting from the first step to the specified step number,
    Write to a JSON file for observation with DeviceStudio.

    Supports hot reading structure information (ignoring other information)

    Parameters
    ----------
    directory:
        NEB path, default to current path
    step:
        number of steps, default -1, read the last configuration

    Returns
    -------
    Arrays for JSON files

    """
    import os

    absdir = os.path.abspath(directory)
    # Initial setup
    neb_h5 = os.path.abspath(os.path.join(absdir, "01", "neb01.h5"))
    from dspawpy.io.read import get_ele_from_h5

    ele = get_ele_from_h5(hpath=neb_h5)
    Natom = len(ele)
    import h5py

    data = h5py.File(neb_h5)
    import numpy as np

    try:
        total_steps = np.asarray(data.get("/NebSize"))[0]
    except Exception:
        print("Reading latest info for unfinished NEB task...")
        try:
            total_steps = np.asarray(data.get("/Structures/FinalStep"))[0]
        except Exception:
            raise ValueError(
                f"No finished ionic step detected, please check {neb_h5} file or wait for NEB task to finished at least one ionic step.",
            )

    if step == -1:
        output = "neb_chain_last.json"
        step = total_steps
    elif step > total_steps:
        output = "neb_chain_last.json"
        logger.warning(
            "specified %s > %s, reading last step info..." % (step, total_steps),
        )
        step = total_steps
    else:
        output = f"neb_chain_{step}.json"

    # ^ Prepare the array framework required for the json file before reading
    subfolders = get_neb_subfolders(absdir)
    nimage = len(subfolders)
    reactionCoordinates = np.zeros(shape=nimage)  # optional
    totalEnergies = np.zeros(
        shape=nimage
    )  # optional, final energies for each configuration
    maxForces = np.zeros(shape=nimage - 2)  # optional
    tangents = np.zeros(shape=nimage - 2)  # optional
    MaxForces = np.zeros(shape=(nimage - 2, step))  # optional
    TotalEnergies = np.zeros(
        shape=(nimage - 2, step),
    )  # optional, energy at each ion step for intermediate configurations
    # Sposes = []  # nimage x Natom x 3 , read
    Sposes = np.empty(shape=(nimage, Natom, 3))  # nimage x Natom x 3 , read
    Elems = []  # nimage x Natom, read
    Latvs = []  # nimage x 9, read
    Fixs = []  # Natom x 3, set

    from dspawpy.io.structure import read

    for i, folder in enumerate(subfolders):
        if folder == subfolders[0] or folder == subfolders[-1]:
            h5_path = os.path.join(absdir, folder, "scf.h5")
            spath = os.path.join(absdir, folder, f"structure{folder}.as")
            if os.path.isfile(h5_path):
                data = h5py.File(h5_path)
                # Does not affect visualization, set directly to 0
                if folder == subfolders[0]:
                    reactionCoordinates[i] = 0
                pos = np.asarray(data.get("/Structures/Step-1/Position")).reshape(
                    -1,
                    3,
                )  # scaled
                lat = np.asarray(data.get("/Structures/Step-1/Lattice"))
                ele = get_ele_from_h5(hpath=h5_path)
                totalEnergies[i] = np.asarray(data.get("/Energy/TotalEnergy0")[0])
            else:
                structure = read(spath, task="neb")[0]
                pos = structure.frac_coords
                ele = [str(i) for i in structure.species]
                lat = structure.lattice.matrix
        else:
            h5_path = os.path.join(absdir, folder, f"neb{folder}.h5")
            data = h5py.File(h5_path)
            # reading...
            try:
                reactionCoordinates[i - 1] = np.asarray(data.get("/Distance/Previous"))[
                    -1
                ]
                maxForces[i - 1] = np.asarray(data.get("/MaxForce"))[-1]
                tangents[i - 1] = np.asarray(data.get("/Tangent"))[-1]
                if folder == subfolders[-2]:
                    reactionCoordinates[i + 1] = np.asarray(data.get("/Distance/Next"))[
                        -1
                    ]
                # read MaxForces and TotalEnergies
                nionStep = np.asarray(data.get("/MaxForce")).shape[0]
                assert step <= nionStep, (
                    f"The number of finished ionic steps is {nionStep}"
                )
                for j in range(step):
                    MaxForces[i - 1, j] = np.asarray(data.get("/MaxForce"))[j]
                    TotalEnergies[i - 1, j] = np.asarray(data.get("/TotalEnergy"))[j]
                totalEnergies[i] = np.asarray(data.get("/Energy/TotalEnergy0")[0])
            except Exception:
                pass  # NEB calculation is not yet complete, but it does not affect reading structure information for visualization
            # read the latest structure for visualization
            pos = np.asarray(data.get(f"/Structures/Step-{step}/Position")).reshape(
                Natom,
                3,
            )  # scaled
            lat = np.asarray(data.get(f"/Structures/Step-{step}/Lattice"))
            ele = get_ele_from_h5(hpath=h5_path)

        Elems.append(ele)
        Sposes[i, :, :] = pos
        Latvs.append(lat)

    if os.path.isfile(os.path.join(absdir, "neb.h5")):
        tdata = h5py.File(os.path.join(absdir, "neb.h5"))
        # atom fix, not lattice
        # ignore this trivial message because it is not necessary for the visualization
        if "/UnrelaxStructure/Image00/Fix" in tdata:
            fix_array = np.asarray(tdata.get("/UnrelaxStructure/Image00/Fix"))
            for fix in fix_array:
                if fix == 0.0:
                    F = False
                elif fix == 1.0:
                    F = True
                else:
                    raise ValueError("Fix must be 0/1")
                Fixs.append(F)
        else:
            Fixs = np.full(shape=(Natom, 3), fill_value=False)
    else:
        Fixs = np.full(shape=(Natom, 3), fill_value=False)

    Elems = np.asarray(Elems).reshape((nimage, Natom))
    Latvs = np.asarray(Latvs).reshape((nimage, 9))
    Fixs = np.asarray(Fixs).reshape((Natom, 3))
    iDirects = [True for i in range(Natom)]  # only output direct coordinates

    return (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,  #
        Sposes,
        Latvs,
        Elems,
        Fixs,
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    )


def _dump_neb_chain_json(raw):
    """Dump the JSON file to output based on the previously collected data lists"""
    (
        output,
        subfolders,
        step,
        MaxForces,
        TotalEnergies,
        Poses,
        Latvs,
        Elems,
        Fixs,
        reactionCoordinates,
        totalEnergies,
        maxForces,
        tangents,
        iDirects,
    ) = raw

    IterDict = {}
    for s, sf in enumerate(subfolders):
        if sf == subfolders[0] or sf == subfolders[-1]:
            continue
        else:
            Eflist = []
            for _i in range(step):
                ef = {
                    "MaxForce": MaxForces[s - 1, _i],
                    "TotalEnergy": TotalEnergies[s - 1, _i],
                }
                Eflist.append(ef)
                iterDict = {sf: Eflist}  # construct sub-dict
                IterDict.update(iterDict)  # append sub-dict

    RSList = []
    """
    Traverse configurations and atoms (sub-dictionaries) from outside to inside.
    The key-value pair for an atom is: 'Atoms': atom information list
    The atom information list is a list of dictionaries, where each dictionary corresponds to the information of an atom.
    """
    for s, sf in enumerate(subfolders):
        pos = Poses[s]
        lat = Latvs[s]
        elem = Elems[s]
        atoms = []
        for i in range(len(elem)):
            atom = {
                "Element": elem[i],
                "Fix": Fixs[i].tolist(),
                "Mag": [],  # empty
                "Position": pos[i].tolist(),
                "Pot": "",
            }  # empty
            atoms.append(atom)
        if iDirects[s]:
            rs = {"Atoms": atoms, "CoordinateType": "Direct", "Lattice": lat.tolist()}
        else:
            rs = {
                "Atoms": atoms,
                "CoordinateType": "Cartesian",
                "Lattice": lat.tolist(),
            }
        RSList.append(rs)

    URSList = []  # DS does not seem to read this part of the information, it can be left empty

    # data structure refs to inputs/2.15/neb.json
    data = {
        "BarrierInfo": {
            "MaxForce": maxForces.tolist(),
            "ReactionCoordinate": reactionCoordinates.tolist(),
            "Tangent": [],
            "TotalEnergy": totalEnergies.tolist(),
        },
        "Force": {"Tangent": tangents.tolist()},
        "LoopInfo": IterDict,
        "RelaxedStructure": RSList,
        "UnrelaxedStructure": URSList,
    }

    # ^ Write the dictionary to a json file
    import os

    absolute_output = os.path.abspath(output)
    with open(absolute_output, "w") as f:
        from json import dump

        dump(data, f, indent=4)

    print(f"==> {absolute_output}")


def _getef(directory: str = "."):
    """Read the energies and forces of each configuration during NEB calculation, NEB calculation can be non-converged
    But if the initial and final states are converged elsewhere, please manually move them into the 00 folders!

    Parameters
    ----------
    directory:
        Path for NEB calculation, default to current path

    Returns
    -------
    subfolders:
        List of configuration folder names
    resort_mfs:
        List of maximum components of configuration forces
    rcs:
        Reaction coordinate list
    ens:
        List of total electronic energies
    dEs:
        List of energy differences from the initial configuration

    """
    import os

    import numpy as np

    absdir = os.path.abspath(directory)
    subfolders = get_neb_subfolders(absdir)
    Nimage = len(subfolders)

    ens = []
    dEs = np.zeros(Nimage)
    rcs = [0]
    mfs = []

    # read energies
    import h5py

    count = 1
    for i, subfolder in enumerate(subfolders):
        if i == 0 or i == Nimage - 1:
            jsf = os.path.join(absdir, subfolder, f"system{subfolder}.json")
            old_jsf = os.path.join(absdir, subfolder, "system.json")
            hf = os.path.join(absdir, subfolder, "scf.h5")

            if os.path.isfile(hf):  # Prefer reading the content of the h5 file
                data = h5py.File(hf)
                en = np.asarray(data.get("/Energy/TotalEnergy0"))[0]
                if i == 0 or i == Nimage - 1:
                    mf = np.max(np.abs(np.asarray(data.get("/Force/ForceOnAtoms"))))
                    mfs.append(mf)

            elif os.path.isfile(jsf):  # Next, read the content of the JSON file
                with open(jsf) as f:
                    from json import load

                    data = load(f)
                en = data["Energy"]["TotalEnergy0"]
                if i == 0 or i == Nimage - 1:
                    mf = np.max(np.abs(data["Force"]["ForceOnAtoms"]))
                    mfs.append(mf)

            elif os.path.isfile(old_jsf):  # Compatible with old JSON
                with open(old_jsf) as f:
                    from json import load

                    data = load(f)
                en = data["Energy"]["TotalEnergy0"]
                if i == 0 or i == Nimage - 1:
                    mf = np.max(np.abs(data["Force"]["ForceOnAtoms"]))
                    mfs.append(mf)

            else:
                raise FileNotFoundError(f"No {jsf}/{old_jsf}/{hf} for {subfolder}")
            ens.append(en)

        else:
            jsf = os.path.join(absdir, subfolder, f"neb{subfolder}.json")
            sysjsf = os.path.join(absdir, subfolder, f"system{subfolder}.json")
            old_sysjsf = os.path.join(absdir, subfolder, "system.json")
            hf = os.path.join(absdir, subfolder, f"neb{subfolder}.h5")

            if os.path.isfile(hf):  # Prefer reading the content of the h5 file
                data = h5py.File(hf)
                en = np.asarray(data.get("/Energy/TotalEnergy0"))[0]
                mf = np.asarray(data.get("/MaxForce"))[-1]
                # the key may change depends on your DS-PAW version
                if "/Distance/Previous" in data:
                    rc = np.asarray(data.get("/Distance/Previous"))[-1]
                elif "/ReactionCoordinate" in data:
                    rc = np.asarray(data.get("/ReactionCoordinate"))[-2]
                else:
                    raise KeyError(
                        f"Neither /Distance/Previous nor /ReactionCoordinate in {hf}",
                    )
                rcs.append(rc)
                if count == Nimage - 2:  # before final image
                    if "/Distance/Next" in data:
                        rc = np.asarray(data.get("/Distance/Next"))[-1]
                    elif "/ReactionCoordinate" in data:
                        rc = np.asarray(data.get("/ReactionCoordinate"))[-1]
                    else:
                        raise KeyError(
                            f"Neither /Distance/Next nor /ReactionCoordinate in {hf}",
                        )
                    rcs.append(rc)

            elif os.path.isfile(jsf):
                from json import load

                if os.path.isfile(sysjsf):
                    with open(sysjsf) as f:
                        data = load(f)
                    en = data["Energy"]["TotalEnergy0"]
                elif os.path.isfile(old_sysjsf):  # Compatible with old DS-PAW
                    with open(old_sysjsf) as f:
                        data = load(f)
                    en = data["Energy"]["TotalEnergy0"]
                else:
                    raise FileNotFoundError(f"No {sysjsf}/{old_sysjsf}")

                with open(jsf) as f:
                    data = load(f)
                Nion_step = len(data)
                # en = data[Nion_step - 1]["TotalEnergy"] # invalid
                mf = data[Nion_step - 1]["MaxForce"]  # Maximum force at the last step
                rc = data[Nion_step - 1]["ReactionCoordinate"][
                    0
                ]  # Reaction coordinate of the final step
                rcs.append(rc)
                if count == Nimage - 2:  # before final image
                    rc = data[Nion_step - 1]["ReactionCoordinate"][
                        1
                    ]  # Final reaction coordinate
                    rcs.append(rc)

            else:
                raise FileNotFoundError(f"No {hf}/{jsf}")

            ens.append(en)
            mfs.append(mf)

            # get dE
            dE = ens[count] - ens[0]
            dEs[i] = dE
            count += 1
    dEs[-1] = ens[Nimage - 1] - ens[0]

    # The rcs read from nebXX.h5/json need to be converted to cumulative values
    for i in range(1, len(rcs)):
        rcs[i] += rcs[i - 1]

    rcs = np.asarray(rcs)

    return subfolders, mfs, rcs, ens, dEs


def monitor_force_energy(directory: str, outdir: str = ".", relative: bool = False):
    """Read forces and energies during NEB calculations from xx/DS-PAW.log and plot curves

    No JSON files are output during the calculation, and only force information is present in nebXX.h5 files, so DS-PAW.log must be read.

    Energy matching mode, should hit -40521.972259

    ------------------------------------------------------------
    LOOP 1:
    ------------------------------------------------------------
    #  iter |      Etot(eV)       dE(eV)         time
    #   1   |  -35958.655378  -3.595866e+04    47.784 s
    #   2   |  -40069.322436  -4.110667e+03    15.146 s
    #   3   |  -40490.281166  -4.209587e+02    15.114 s
    #   4   |  -40521.972259  -3.169109e+01    17.936 s

    Examples
    --------
    >>> from dspawpy.diffusion.nebtools import monitor_force_energy
    >>> monitor_force_energy(
    ...     directory="dspawpy_proj/dspawpy_tests/inputs/supplement/neb_unfinished",
    ...     outdir="imgs"
    ... ) # doctest: +ELLIPSIS
    Max Force shape: (57, 4)
    ┌───────────┬───────────┬───────────┬───────────┐
    │ Folder 01 ┆ Folder 02 ┆ Folder 03 ┆ Folder 04 │
    ╞═══════════╪═══════════╪═══════════╪═══════════╡
    │ 23.775228 ┆ 71.547767 ┆ 72.641234 ┆ 24.147289 │
    │ 22.683711 ┆ 68.595607 ┆ 69.704747 ┆ 23.0549   │
    │ 5.624252  ┆ 20.071221 ┆ 20.049429 ┆ 5.567894  │
    │ 5.354774  ┆ 19.631643 ┆ 19.599093 ┆ 5.425462  │
    │ 3.188546  ┆ 9.840143  ┆ 9.748006  ┆ 2.943709  │
    │ …         ┆ …         ┆ …         ┆ …         │
    │ 0.293867  ┆ 0.812679  ┆ 0.920251  ┆ 0.573649  │
    │ 0.27249   ┆ 0.7475    ┆ 0.921836  ┆ 0.540239  │
    │ 0.299767  ┆ 0.360673  ┆ 1.174016  ┆ 0.416171  │
    │ 0.249903  ┆ 0.288985  ┆ 1.169237  ┆ 0.366117  │
    │ 0.204396  ┆ 0.518356  ┆ 0.913792  ┆ 0.300884  │
    └───────────┴───────────┴───────────┴───────────┘
    Energies shape: (57, 4)
    ┌───────────────┬───────────────┬───────────────┬───────────────┐
    │ Folder 01     ┆ Folder 02     ┆ Folder 03     ┆ Folder 04     │
    ╞═══════════════╪═══════════════╪═══════════════╪═══════════════╡
    │ -40448.281556 ┆ -40436.419243 ┆ -40436.084611 ┆ -40447.527434 │
    │ -40448.491374 ┆ -40437.026948 ┆ -40436.685178 ┆ -40447.73947  │
    │ -40451.391617 ┆ -40446.884408 ┆ -40446.613158 ┆ -40450.686918 │
    │ -40451.448662 ┆ -40447.079933 ┆ -40446.803281 ┆ -40450.743777 │
    │ -40452.126865 ┆ -40450.274376 ┆ -40449.978142 ┆ -40451.405157 │
    │ …             ┆ …             ┆ …             ┆ …             │
    │ -40452.620987 ┆ -40452.538682 ┆ -40452.230568 ┆ -40452.056262 │
    │ -40452.621777 ┆ -40452.544298 ┆ -40452.231776 ┆ -40452.055815 │
    │ -40452.620701 ┆ -40452.565649 ┆ -40452.164604 ┆ -40452.035357 │
    │ -40452.621371 ┆ -40452.569113 ┆ -40452.164784 ┆ -40452.037426 │
    │ -40452.622418 ┆ -40452.577864 ┆ -40452.141919 ┆ -40452.037885 │
    └───────────────┴───────────────┴───────────────┴───────────────┘
    ==> ...MaxForce.png...
    ==> ...Energies.png...

    """
    import os

    absdir = os.path.abspath(directory)
    absoutdir = os.path.abspath(outdir)
    subfolders = get_neb_subfolders(absdir)
    Nimage = len(subfolders)

    import re

    forces_all_images = []
    energies_all_images = []
    folder_names = []
    for i, subfolder in enumerate(subfolders):
        logfile = f"{absdir}/{subfolder}/DS-PAW.log"
        if i == 0 or i == Nimage - 1 or not os.path.isfile(logfile):
            continue

        folder_names.append(subfolder)
        forces = []
        if os.path.isfile(logfile):
            force_lines = []
            with open(logfile) as f:
                lines = f.readlines()
                # find all "LOOP 1:" lines
                inds = []
                for j, line in enumerate(lines):
                    if line.startswith("LOOP 1:"):
                        inds.append(j)
                if len(inds) == 0:
                    raise FileNotFoundError(f"No LOOP 1: in {logfile}")

                pattern = r"-{10,}\nLOOP \d+:\n-{10,}\n(?:.*\n)*?#\s*\d+\s+\|\s+(-\d+\.\d+).*\n\s*\n"
                latest_lines = lines[inds[-1] - 2 :]
                energies = re.findall(pattern, "".join(latest_lines))
                for line in latest_lines:
                    if "Max force:" in line:
                        force_lines.append(line)
                for line in force_lines:
                    forces.append(float(line.split()[2]))
            energies = [float(e) for e in energies]

            forces_all_images.append(forces)
            energies_all_images.append(energies)
        else:
            raise FileNotFoundError(f"No {logfile}")

    import polars as pl

    pl.Config.set_tbl_rows(10)

    # first check the LOOP number for each folder, and use the one all folders have as refs.
    nloops = [len(forces_all_images[i]) for i in range(len(folder_names))]
    if len(nloops) == 0:
        print("No loops found, did you specify the wrong path?")
        exit(1)
    min_loop = min(nloops)
    if min_loop == 0:
        print("please wait until at least the first loop is finished for all folders.")
        exit(1)
    max_loop = max(nloops)

    # set force and energy relative to last value of each folder
    if relative:
        for i in range(len(folder_names)):
            if len(forces_all_images[i]) == 0 or len(energies_all_images[i]) == 0:
                print(f"No forces or energies found in {folder_names[i]}/DS-PAW.log")
                exit(1)
            last_force = forces_all_images[i][min_loop - 1]
            last_energy = energies_all_images[i][min_loop - 1]
            forces_all_images[i] = [f - last_force for f in forces_all_images[i]]
            energies_all_images[i] = [e - last_energy for e in energies_all_images[i]]

    df1 = pl.DataFrame(
        {
            f"Folder {folder_names[i]}": forces_all_images[i]
            if len(forces_all_images[i]) == max_loop
            else forces_all_images[i] + [None] * (max_loop - len(forces_all_images[i]))
            for i in range(len(folder_names))
        },
    )
    print(f"Max Force {df1}")

    df2 = pl.DataFrame(
        {
            f"Folder {folder_names[i]}": energies_all_images[i]
            if len(energies_all_images[i]) == max_loop
            else energies_all_images[i]
            + [None] * (max_loop - len(energies_all_images[i]))
            for i in range(len(folder_names))
        },
    )
    print(f"Energies {df2}")

    import matplotlib.pyplot as plt

    plt.clf()
    for _i in range(len(folder_names)):
        plt.plot(
            range(len(forces_all_images[_i])),
            forces_all_images[_i],
            "-o",
            label=f"Image {folder_names[_i]}",
        )

    os.makedirs(absoutdir, exist_ok=True)
    plt.legend()
    plt.title("Max Force")
    plt.tight_layout()
    plt.savefig(f"{absoutdir}/MaxForce.png")
    print(f"==> {absoutdir}/MaxForce.png")

    plt.clf()
    for _i in range(len(folder_names)):
        plt.plot(
            range(len(energies_all_images[_i])),
            energies_all_images[_i],
            "-o",
            label=f"Image {folder_names[_i]}",
        )

    plt.legend()
    plt.title("Energies")
    plt.tight_layout()
    plt.savefig(f"{absoutdir}/Energies.png")
    print(f"==> {absoutdir}/Energies.png")
