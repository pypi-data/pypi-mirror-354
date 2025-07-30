from typing import TYPE_CHECKING, List, Optional, Union

from loguru import logger

from dspawpy.io.utils import reader

if TYPE_CHECKING:
    from pymatgen.core.structure import Structure


def build_Structures_from_datafile(
    datafile: Union[str, List[str]],
    si=None,
    ele=None,
    ai=None,
    fmt=None,
    task="scf",
):
    """Deprecated alias to read"""
    logger.warning(
        "build_Structures_from_datafile is deprecated; use read instead",
        DeprecationWarning,
    )
    return read(datafile, si=si, ele=ele, ai=ai, fmt=fmt, task=task)


def _get_structure_list(
    df: str,
    si=None,
    ele=None,
    ai=None,
    fmt: Optional[str] = None,
    task: Optional[str] = "scf",
    verbose: bool = True,
):
    """Get pymatgen structures from single datafile.

    Parameters
    ----------
    df:
        Path to the data file or the folder containing the data file

    Returns
    -------
    List[Structure] : list of pymatgen structures

    """
    if task is None:
        task = "scf"

    import os

    if os.path.isdir(df) or df.endswith(".h5") or df.endswith(".json"):
        from dspawpy.io.utils import get_absfile

        absfile = get_absfile(df, task=task, verbose=verbose)
    else:  # for other type of datafile, such as .as, .hzw, POSCAR
        absfile = os.path.abspath(df)

    if fmt is None:
        fmt = absfile.split(".")[-1]
    else:
        assert isinstance(fmt, str)

    if fmt == "as":
        strs = [_from_dspaw_as(absfile)]
    elif fmt == "hzw":
        logger.warning("build from .hzw may lack mag & fix info!", category=UserWarning)
        strs = [_from_hzw(absfile)]
    elif fmt == "xyz":
        strs = [_from_xyz(absfile)]
    elif fmt == "pdb":
        strs = _from_pdb(absfile)
    elif fmt == "h5":
        from dspawpy.io.read import get_sinfo

        Nstep, elements, positions, lattices, D_mag_fix = get_sinfo(
            datafile=absfile,
            si=si,
            ele=ele,
            ai=ai,
        )  # returned positions, not scaled-positions
        # remove _ from elements
        import re

        elements = [re.sub(r"_", "", e) for e in elements]

        strs = []
        from pymatgen.core import Structure

        for i in range(Nstep):
            if D_mag_fix:
                strs.append(
                    Structure(
                        lattices[i],
                        elements,
                        positions[i],
                        coords_are_cartesian=True,
                        site_properties={k: v[i] for k, v in D_mag_fix.items()},
                    ),
                )
            else:
                strs.append(
                    Structure(
                        lattices[i],
                        elements,
                        positions[i],
                        coords_are_cartesian=True,
                    ),
                )

    elif fmt == "json":
        try:
            from dspawpy.io.read import get_sinfo

            Nstep, elements, positions, lattices, D_mag_fix = get_sinfo(
                datafile=absfile,
                si=si,
                ele=ele,
                ai=ai,
            )  # returned positions, not scaled-positions
            # remove _ from elements

            import re

            elements = [re.sub(r"_", "", e) for e in elements]

            strs = []
            from pymatgen.core import Structure

            for i in range(Nstep):
                if D_mag_fix:
                    strs.append(
                        Structure(
                            lattices[i],
                            elements,
                            positions[i],
                            coords_are_cartesian=True,
                            site_properties={k: v[i] for k, v in D_mag_fix.items()},
                        ),
                    )
                else:
                    strs.append(
                        Structure(
                            lattices[i],
                            elements,
                            positions[i],
                            coords_are_cartesian=True,
                        ),
                    )
        except Exception:  # try parse json with pymatgen
            from pymatgen.core import Structure

            strs = [Structure.from_file(absfile)]

    else:
        from pymatgen.core import Structure

        strs = [Structure.from_file(absfile)]

    return strs


def _from_dspaw_as(as_file: str = "structure.as") -> "Structure":
    """Read structure information from a DSPAW as structure file.

    Parameters
    ----------
    as_file:
        DSPAW's as structure file, default 'structure.as'

    Returns
    -------
    Structure
        a pymatgen Structure object

    """
    import os

    absfile = os.path.abspath(as_file)
    from dspawpy.io.read import get_lines_without_comment

    lines = get_lines_without_comment(absfile, "#")
    N = int(lines[1])  # number of atoms

    # parse lattice info
    lattice = []  # lattice matrix
    for line in lines[3:6]:
        vector = line.split()
        lattice.extend([float(vector[0]), float(vector[1]), float(vector[2])])
    import numpy as np

    lattice = np.asarray(lattice).reshape(3, 3)

    lat_fixs = []
    if lines[2].strip() != "Lattice":  # fix lattice
        lattice_fix_info = lines[2].strip().split()[1:]
        if lattice_fix_info == ["Fix_x", "Fix_y", "Fix_z"]:
            # ONLY support xyz fix in sequence, yzx will cause error
            for line in lines[3:6]:
                lfs = line.strip().split()[3:6]
                for lf in lfs:
                    if lf.startswith("T"):
                        lat_fixs.append("True")
                    elif lf.startswith("F"):
                        lat_fixs.append("False")
        elif lattice_fix_info == ["Fix"]:
            for line in lines[3:6]:
                lf = line.strip().split()[3]
                if lf.startswith("T"):
                    lat_fixs.append("True")
                elif lf.startswith("F"):
                    lat_fixs.append("False")
        else:
            raise ValueError("Lattice fix info error!")

    elements = []
    positions = []
    for i in range(N):
        atom = lines[i + 7].strip().split()
        elements.append(atom[0])
        positions.extend([float(atom[1]), float(atom[2]), float(atom[3])])

    mf_info = None
    l6 = lines[6].strip()  # str, 'Cartesian/Direct Mag Fix_x ...'
    if l6.split()[0] == "Direct":
        is_direct = True
    elif l6.split()[0] == "Cartesian":
        is_direct = False
    else:
        raise ValueError("Structure file format error!")

    mf_info = l6.split()[1:]  # ['Mag', 'Fix_x', 'Fix_y', 'Fix_z']
    for item in mf_info:
        assert item in [
            "Mag",
            "Mag_x",
            "Mag_y",
            "Mag_z",
            "Fix",
            "Fix_x",
            "Fix_y",
            "Fix_z",
        ], (
            f"{item} is not a valid flag! Expecting ['Mag', 'Mag_x', 'Mag_y', 'Mag_z', 'Fix', 'Fix_x', 'Fix_y', 'Fix_z']"
        )

    mag_fix_dict = {}
    if mf_info is not None:
        after_Fix = False
        for mf_index, item in enumerate(mf_info):
            values = []
            for i in range(N):
                atom = lines[i + 7].strip().split()
                mf = atom[4:]
                if item == "Fix":  # Fix == Fix_x, Fix_y, Fix_z
                    values.append([mf[mf_index], mf[mf_index + 1], mf[mf_index + 2]])
                elif item.startswith("Fix_"):
                    values.append(mf[mf_index])
                else:  # mag
                    if after_Fix:
                        values.append(float(mf[mf_index + 2]))
                    else:
                        values.append(float(mf[mf_index]))
            # set after_Fix flag, to shift index with 2
            if item == "Fix":
                after_Fix = True
            else:
                after_Fix = False

            if item.startswith("Fix"):  # F -> False, T -> True
                for value in values:
                    if isinstance(value, str):
                        if value.startswith("T"):
                            values[values.index(value)] = "True"
                        elif value.startswith("F"):
                            values[values.index(value)] = "False"
                    elif isinstance(value, list):
                        for v in value:
                            if v.startswith("T"):
                                value[value.index(v)] = "True"
                            elif v.startswith("F"):
                                value[value.index(v)] = "False"
            mag_fix_dict[item] = values
    if lat_fixs != []:
        # replicate lat_fixs to N atoms
        mag_fix_dict["LatticeFixs"] = [lat_fixs for _ in range(N)]

    coords = np.asarray(positions).reshape(-1, 3)
    # remove _ from elements
    import re

    elements = [re.sub(r"_", "", e) for e in elements]

    from pymatgen.core import Structure

    if mag_fix_dict == {}:
        return Structure(
            lattice,
            elements,
            coords,
            coords_are_cartesian=(not is_direct),
        )
    else:
        return Structure(
            lattice,
            elements,
            coords,
            coords_are_cartesian=(not is_direct),
            site_properties=mag_fix_dict,
        )


def _from_hzw(hzw_file) -> "Structure":
    """Read structure information from an hzw structure file

    Parameters
    ----------
    hzw_file:
        hzw structure file, with a .hzw extension

    Returns
    -------
    Structure
        pymatgen's Structure object

    Examples
    --------
    >>> from dspawpy.io.structure import _from_hzw
    >>> print(_from_hzw('dspawpy_proj/dspawpy_tests/inputs/supplement/Si2.hzw'))
    Full Formula (Si2)
    Reduced Formula: Si
    abc   :   0.678839   0.678839   0.678839
    angles:  90.000000  90.000000  90.000000
    pbc   :       True       True       True
    Sites (2)
      #  SP           a         b         c
    ---  ----  --------  --------  --------
      0  Si    0.999999  0.999999  0.999999
      1  Si    3         3         3

    """
    import os

    from pymatgen.core import Structure

    from dspawpy.io.read import get_lines_without_comment

    absfile = os.path.abspath(hzw_file)

    lines = get_lines_without_comment(absfile, "%")
    number_of_probes = int(lines[0])
    elements = []
    positions = []
    if number_of_probes == 0:  # with lattice
        N = int(lines[4])
        for i in range(N):
            atom = lines[i + 5].strip().split()
            elements.append(atom[0])
            positions.append([float(atom[1]), float(atom[2]), float(atom[3])])

        lattice = []
        for line in lines[1:4]:
            vector = line.split()
            lattice.append([float(vector[0]), float(vector[1]), float(vector[2])])

    elif number_of_probes == -1:  # crystal
        N = int(lines[1])
        for i in range(N):
            atom = lines[i + 2].strip().split()
            elements.append(atom[0])
            positions.append([float(atom[1]), float(atom[2]), float(atom[3])])

        max_a = max(positions[:][0]) + 1e-6
        max_b = max(positions[:][0]) + 1e-6
        max_c = max(positions[:][0]) + 1e-6
        lattice = [max_a, 0, 0, 0, max_b, 0, 0, 0, max_c]

    else:
        raise NotImplementedError("number of probes must be 0 or 1")

    return Structure(lattice, elements, positions, coords_are_cartesian=True)


def _from_xyz(xyzfile: str) -> "Structure":
    """From molecule xyz file, build pmg.structure

    Examples
    --------
    >>> from dspawpy.io.structure import _from_xyz
    >>> print(_from_xyz('dspawpy_proj/dspawpy_tests/inputs/supplement/Si2.xyz'))
    Full Formula (Si2)
    Reduced Formula: Si
    abc   :   4.811495   4.826272   4.826271
    angles:  90.000000  90.000000  90.000000
    pbc   :       True       True       True
    Sites (2)
      #  SP           a         b         c
    ---  ----  --------  --------  --------
      0  Si    0.928452  0.927353  0.927353
      1  Si    0.071548  0.072647  0.072647

    """
    from pymatgen.core.structure import Molecule

    mol = Molecule.from_file(xyzfile)
    assert mol is not None

    a = max(mol.cart_coords[:, 0]) + 1e-6
    b = max(mol.cart_coords[:, 1]) + 1e-6
    c = max(mol.cart_coords[:, 2]) + 1e-6

    return mol.get_boxed_structure(a, b, c, no_cross=True)


def _read_atom_line(line_full):
    """Read atomic name, xyz coordinates, and element symbol from a PDB file
    The format of the ATOM section in a PDB file is as follows (excluding magnetic moment and coordinate information):
    HETATM    1  H14 ORTE    0       6.301   0.693   1.919  1.00  0.00        H
    Fixed label Atom number Atom name Residue name Residue number x y z Occupancy Temperature factor Element symbol

    Exclude redundant information, retain only
        - Atom name
        - xyz coordinates
        - Element symbol
    """
    line = line_full.rstrip("\n")
    type_atm = line[0:6]
    if type_atm == "ATOM  " or type_atm == "HETATM":
        name = line[12:16].strip()  # Atom name
        # atomic coordinates
        import numpy as np

        try:  # 5.3f indicates 5 digits for the integer part and 3 digits for the decimal part, unit is Angstrom
            coord = np.asarray(
                [float(line[30:38]), float(line[38:46]), float(line[46:54])],
                dtype=np.float64,
            )
        except ValueError:
            raise ValueError("Invalid or missing coordinate(s)")
        symbol = line[76:78].strip().upper()  # Element symbol

    else:
        raise ValueError("Only ATOM and HETATM supported")

    return name, coord, symbol


@reader
def _from_pdb(fileobj):
    """Read PDB files. Modified from ASE"""
    images = []  # Conformation list
    import numpy as np

    orig = np.identity(3)  # Origin
    trans = np.zeros(3)  # Offset
    symbols = []  # Elements
    positions = []  # Coordinates
    cell = None  # Unit cell

    from pymatgen.core.lattice import Lattice

    for line in fileobj.readlines():
        if line.startswith("CRYST1"):
            cellpar = [
                float(line[6:15]),  # a
                float(line[15:24]),  # b
                float(line[24:33]),  # c
                float(line[33:40]),  # alpha
                float(line[40:47]),  # beta
                float(line[47:54]),
            ]  # gamma
            cell = Lattice.from_parameters(
                a=cellpar[0],
                b=cellpar[1],
                c=cellpar[2],
                alpha=cellpar[3],
                beta=cellpar[4],
                gamma=cellpar[5],
            )

        for c in range(3):
            if line.startswith("ORIGX" + "123"[c]):
                orig[c] = [float(line[10:20]), float(line[20:30]), float(line[30:40])]
                trans[c] = float(line[45:55])

        if line.startswith("ATOM") or line.startswith("HETATM"):
            # line_info = name, coord, symbol
            line_info = _read_atom_line(line)

            from dspawpy.io.utils import label_to_symbol

            try:  # Attempt to convert from element symbol, use atomic name if failure occurs
                symbol = label_to_symbol(line_info[2])
            except (KeyError, IndexError):
                symbol = label_to_symbol(line_info[0])
            symbols.append(symbol)

            position = np.dot(orig, line_info[1]) + trans
            positions.append(position)

        if line.startswith("END"):
            atoms = _build_atoms(cell, symbols, positions)
            images.append(atoms)
            symbols = []
            positions = []
            cell = None

    if len(images) == 0:
        atoms = _build_atoms(cell, symbols, positions)
        images.append(atoms)

    return images


def _build_atoms(cell, symbols, positions):
    if cell is None:
        logger.warning(
            "No lattice info in PDB file! The lattice defaults to [[2xmax, 0, 0]; [0, 2ymax, 0]; [0, 0, 2zmax]])",
            category=UserWarning,
        )
        # cell = np.zeros(shape=(3, 3))
        import numpy as np

        max_xyz = np.max(positions, axis=0)
        cell = np.diag(max_xyz * 2)

    from pymatgen.core import Structure

    atoms = Structure(
        lattice=cell,
        species=symbols,
        coords=positions,
        coords_are_cartesian=True,
    )

    return atoms


def read(
    datafile: Union[str, list],
    si=None,
    ele=None,
    ai=None,
    fmt: Optional[str] = None,
    task: Optional[str] = "scf",
):
    r"""Read one or more h5/json files and return a list of pymatgen Structures.

    Parameters
    ----------
    datafile:
        - file paths for h5/json/as/hzw/cif/poscar/cssr/xsf/mcsqs/prismatic/yaml/fleur-inpgen files;
        - If a directory path is given, it can be combined with the task parameter to read the {task}.h5/json files inside
        - If a list of strings is given, it will sequentially read the data and merge them into a list of Structures
    si: int, list or str
        - Configuration number, starting from 1

            - si=1, reads the first configuration
            - si=[1,2], reads the first and second configurations
            - si=':', reads all configurations
            - si='-3:', reads the last three configurations
        - If empty, it reads all configurations for multi-configuration files and the latest configuration for single-configuration files
        - This parameter is only valid for h5/json files
    ele:
        - Element symbol, format reference: 'H' or ['H','O']
        - If empty, it will read atomic information for all elements
        - This parameter is only valid for h5/json files
    ai:
        - Atom index, starting from 1
        - Same as si
        - If empty, it will read all atom information
        - This parameter is only valid for h5/json files
    fmt:
        - File format, including 'as', 'hzw', 'xyz', 'pdb', 'h5', 'json' 6 types, other values will be ignored.
        - If empty, the file type will be determined based on file name conventions.
    task:
        - Used when datafile is a directory path to find the internal {task}.h5/json file.
        - Determine the task type, including 'scf', 'relax', 'neb', 'aimd' four types, other values will be ignored.

    Returns
    -------
    pymatgen_Structures:
        Structure list

    Examples
    --------
    >>> from dspawpy.io.structure import read

    Reads a single file to generate a list of Structures

    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/supplement/PtH.as')
    >>> len(pymatgen_Structures)
    1
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/supplement/PtH.hzw')
    >>> len(pymatgen_Structures)
    1
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/supplement/Si2.xyz')
    >>> len(pymatgen_Structures)
    1
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/supplement/aimd.pdb')
    >>> len(pymatgen_Structures)
    1000
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/2.1/relax.h5') # doctest: +ELLIPSIS
    >>> len(pymatgen_Structures)
    3
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/2.1/relax.json') # doctest: +ELLIPSIS
    >>> len(pymatgen_Structures)
    3

    Note that pymatgen_Structures is a list composed of multiple Structure objects, each corresponding to a structure. If there is only one structure, it will also return a list. Please use pymatgen_Structures[0] to obtain the Structure object.

    When datafile is a list, it reads multiple files sequentially and merges them into a Structures list

    >>> pymatgen_Structures = read(datafile=['dspawpy_proj/dspawpy_tests/inputs/supplement/aimd1.h5','dspawpy_proj/dspawpy_tests/inputs/supplement/aimd2.h5']) # doctest: +ELLIPSIS

    """
    dfs = []
    if isinstance(datafile, list):  # Continuation mode, multiple files are provided
        dfs = datafile
    else:  # Single calculation mode, processing a single file
        dfs.append(datafile)

    # Read structure data
    pymatgen_Structures = []
    for df in dfs:
        structure_list = _get_structure_list(df, si, ele, ai, fmt, task)
        pymatgen_Structures.extend(structure_list)

    return pymatgen_Structures


def write(
    structure,
    filename: str,
    fmt: Optional[str] = None,
    coords_are_cartesian: bool = True,
):
    r"""Write information to the structure file

    Parameters
    ----------
    structure:
        `A pymatgen Structure object`
    filename:
        Structure filename
    fmt:
        - Structure file type, natively supports 'json', 'as', 'hzw', 'pdb', 'xyz', 'dump' six types
    coords_are_cartesian:
        - Whether to write in Cartesian coordinates, default is True; otherwise write in fractional coordinate format
        - This option is currently only effective for 'as' and 'json' formats

    Examples
    --------
    First, read the structure information:

    >>> from dspawpy.io.structure import read
    >>> s = read('dspawpy_proj/dspawpy_tests/inputs/2.15/01/neb01.h5') # doctest: +ELLIPSIS
    >>> len(s)
    17

    Writing structure information to a file:

    >>> from dspawpy.io.structure import write
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.json', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.json...
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.as', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.as...
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.hzw', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.hzw...

    PDB, XYZ, and DUMP file types can write multiple conformations to form a "trajectory." The generated XYZ trajectory files can be opened and visualized using visualization software like OVITO.

    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.pdb', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.pdb...
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.xyz', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.xyz...
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.dump', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.dump...

    The recommended format for storing single structure information is as format. If the Structure contains magnetic moment or degree of freedom information, it will be written in the most complete format, such as Fix_x, Fix_y, Fix_z, Mag_x, Mag_y, Mag_z. The default value for degree of freedom information is F, and the default value for magnetic moment is 0.0. You can manually delete this default information from the generated as file as needed. Writing to other types of structure files will ignore magnetic moment and degree of freedom information.

    """
    from pymatgen.core import Structure

    if isinstance(structure, Structure):
        structure = [structure]

    import os

    absfilename = os.path.abspath(filename)
    if fmt is None:
        fmt = absfilename.split(".")[-1]

    if fmt == "pdb":  # Can be multiple conformations
        from .write import _to_pdb

        _to_pdb(structure, absfilename)
    elif fmt == "xyz":  # Can be multiple configurations
        from .write import _write_xyz_traj

        _write_xyz_traj(structure, absfilename)
    elif fmt == "dump":  # Can be multiple configurations
        from .write import _write_dump_traj

        _write_dump_traj(structure, absfilename)

    elif fmt == "json":  # Single configuration
        from .write import _to_dspaw_json

        _to_dspaw_json(structure[-1], absfilename, coords_are_cartesian)
    elif fmt == "as":
        from .write import _to_dspaw_as

        _to_dspaw_as(structure[-1], absfilename, coords_are_cartesian)
    elif fmt == "hzw":
        from .write import _to_hzw

        _to_hzw(structure[-1], absfilename)

    elif fmt in [
        "cif",
        "mcif",
        "poscar",
        "cssr",
        "xsf",
        "mcsqs",
        "yaml",
        "fleur-inpgen",
        "prismatic",
        "res",
    ]:
        structure[-1].to(filename=absfilename, fmt=fmt)  # type: ignore

    else:
        try:
            structure[-1].to(filename=absfilename)
        except Exception as e:
            raise NotImplementedError(
                f"formats other than [pdb, xyz, dump, json, as, hzw] are handled by pymatgen, while it returns: {e}",
            )


def convert(
    infile,
    si=None,
    ele=None,
    ai=None,
    infmt: Optional[str] = None,
    task: str = "scf",
    outfile: str = "temp.xyz",
    outfmt: Optional[str] = None,
    coords_are_cartesian: bool = True,
):
    """convert from infile to outfile.

    - multi -> single, only keep last step
    - crystal -> molecule, will lose lattice info
    - molecule -> crystal, will add a box of twice the maximum xyz
    - pdb, dump may suffer decimal precision loss

    Parameters
    ----------
    infile:  
        - h5/json/as/hzw/cif/poscar/cssr/xsf/mcsqs/prismatic/yaml/fleur-inpgen file path  
        - If a folder is given, will read {task}.h5/json files  
        - If structures are given, will read multiple structures.  

    si: int, list, or str  
        - Structure index, starting from 1  

            - si=1, read the 1st  
            - si=[1,2], read the 1st and 2nd  
            - si=':', read all  
            - si='-3:', read the last 3  
        - If empty, for multi-configuration files, all configurations will be read; for single-configuration files, the latest configuration will be read.  
        - This parameter is only valid for h5/json files.  

    ele:  
        - Element symbol, written as 'H' or ['H','O']  
        - If empty, atomic information for all elements will be read.  
        - This parameter is only valid for h5/json files.  

    ai:  
        - Atom index, starting from 1  
        - Usage is the same as si  
        - If empty, atomic information for all atoms will be read.  
        - This parameter is only valid for h5/json files.  

    infmt:  
        - Input structure file type, e.g., 'h5'. If None, the file extension will determine the format.  

    task:  
        - Used when datafile is a folder path to locate the internal {task}.h5/json file.  
        - Calculation task type, including 'scf', 'relax', 'neb', 'aimd'. Other values will be ignored.  

    outfile:  
        - Output filename  

    outfmt:  
        - Output structure file type, e.g., 'xyz'. If None, the file extension will determine the format.  

    coords_are_cartesian:  
        - Whether to write coordinates in Cartesian form (default: True); otherwise, fractional coordinates will be used.  
        - This option is currently only valid for as and json formats.  

    Examples
    --------
    >>> from dspawpy.io.structure import convert
    >>> convert('dspawpy_proj/dspawpy_tests/inputs/supplement/PtH.as', outfile='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.hzw') # doctest: +ELLIPSIS
    ==> ...PtH.hzw...

    batch test

    >>> for readable in ['relax.h5', 'system.json', 'aimd.pdb', 'latestStructure.as', 'CuO.hzw', 'POSCAR']:
    ...     for writable in ['pdb', 'xyz', 'dump', 'as', 'hzw', 'POSCAR']:
    ...         convert('dspawpy_proj/dspawpy_tests/inputs/supplement/stru/'+readable, outfile=f"dspawpy_proj/dspawpy_tests/outputs/doctest/{readable.split('.')[0]}.{writable}") # doctest: +ELLIPSIS
    ==> ...relax.pdb...
    ==> ...relax.xyz...
    ==> ...relax.dump...
    ==> ...relax.as...
    ==> ...relax.hzw...
    ==> ...system.pdb...
    ==> ...system.xyz...
    ==> ...system.dump...
    ==> ...system.as...
    ==> ...system.hzw...
    ==> ...aimd.pdb...
    ==> ...aimd.xyz...
    ==> ...aimd.dump...
    ==> ...aimd.as...
    ==> ...aimd.hzw...
    ==> ...latestStructure.pdb...
    ==> ...latestStructure.xyz...
    ==> ...latestStructure.dump...
    ==> ...latestStructure.as...
    ==> ...latestStructure.hzw...
    ==> ...CuO.pdb...
    ==> ...CuO.xyz...
    ==> ...CuO.dump...
    ==> ...CuO.as...
    ==> ...CuO.hzw...
    ==> ...POSCAR.pdb...
    ==> ...POSCAR.xyz...
    ==> ...POSCAR.dump...
    ==> ...POSCAR.as...
    ==> ...POSCAR.hzw...

    """
    write(read(infile, si, ele, ai, infmt, task), outfile, outfmt, coords_are_cartesian)
