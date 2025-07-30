from typing import TYPE_CHECKING, Optional, Sequence

from loguru import logger

if TYPE_CHECKING:
    from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine


def get_band_data(
    band_dir: str,
    syst_dir: Optional[str] = None,
    efermi: Optional[float] = None,
    zero_to_efermi: bool = False,
    verbose: bool = False,
) -> "BandStructureSymmLine":
    """Reads band structure data from an h5 or json file and constructs a BandStructureSymmLine object.

    Parameters
    ----------
    band_dir
        - Path to the band structure file, band.h5 / band.json, or a directory containing band.h5 / band.json
        - Note that wannier.h5 can also be read using this function, but band_dir does not support folder types
    syst_dir
        Path to system.json, prepared only for auxiliary processing of Wannier data (structure and Fermi level are read from it)
    efermi
        Fermi level, if the Fermi level in the h5 file is incorrect, it can be specified using this parameter
    zero_to_efermi
        Whether to shift the Fermi level to 0

    Returns
    -------
    BandStructureSymmLine

    Examples
    --------
    >>> from dspawpy.io.read import get_band_data
    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.3/band.h5')
    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.4/band.h5')
    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.4/band.json')

    If you want to process Wannier band structures by specifying wannier.json, you need to additionally specify the syst_dir parameter.

    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.30/wannier.h5')
    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.30/wannier.json', syst_dir='dspawpy_proj/dspawpy_tests/inputs/2.30/system.json')

    """
    if efermi is not None and zero_to_efermi:
        raise ValueError(
            "efermi and zero_to_efermi should not be set at the same time!",
        )

    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(
        band_dir,
        task="band",
        verbose=verbose,
    )  # give wannier.h5 also work, verbose=verboses
    if absfile.endswith(".h5"):
        band = load_h5(absfile)
        from h5py import File

        raw = File(absfile, "r").keys()
        if "/WannBandInfo/NumberOfBand" in raw:
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = _get_band_data_h5(band, iwan=True, zero_to_efermi=zero_to_efermi)
        elif "/BandInfo/NumberOfBand" in raw:
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = _get_band_data_h5(band, iwan=False, zero_to_efermi=zero_to_efermi)
        else:
            raise KeyError("BandInfo or WannBandInfo key not found in h5file!")
    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            band = load(fin)
        if "WannBandInfo" in band.keys():
            assert syst_dir is not None, (
                "system.json is required for processing wannier band info!"
            )
            with open(syst_dir) as system_json:
                from json import load

                syst = load(system_json)
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = _get_band_data_json(
                band,
                syst,
                iwan=True,
                zero_to_efermi=zero_to_efermi,
            )
        elif "BandInfo" in band.keys():
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = _get_band_data_json(band, iwan=False, zero_to_efermi=zero_to_efermi)
        else:
            raise ValueError(
                f"BandInfo or WannBandInfo key not found in {absfile} file!",
            )
    else:
        raise TypeError(f"{absfile} must be h5 or json file!")

    if efermi:  # Fermi level read directly from h5 might be incorrect, user needs to specify manually
        rEf = efermi  # This is just a temporary solution

    from pymatgen.core.lattice import Lattice

    lattice_new = Lattice(structure.lattice.reciprocal_lattice.matrix)

    from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine

    return BandStructureSymmLine(
        kpoints=kpoints,
        eigenvals=eigenvals,
        lattice=lattice_new,
        efermi=rEf,
        labels_dict=labels_dict,
        structure=structure,
        projections=projections,
    )


def get_dos_data(
    dos_dir: str,
    return_dos: bool = False,
    verbose: bool = False,
):
    """Read density of states (DOS) data from an h5 or json file, and construct a CompleteDos or DOS object

    Parameters
    ----------
    dos_dir:
        Path to the density of states file, dos.h5 / dos.json, or a folder containing dos.h5 / dos.json
    return_dos : bool, optional
        Whether to return the DOS object. If False, a CompleteDos object is returned uniformly (regardless of whether projection was enabled during calculation)

    Returns
    -------
    CompleteDos or Dos

    Examples
    --------
    >>> from dspawpy.io.read import get_dos_data
    >>> dos = get_dos_data(dos_dir='dspawpy_proj/dspawpy_tests/inputs/2.5/dos.h5')
    >>> dos = get_dos_data(dos_dir='dspawpy_proj/dspawpy_tests/inputs/2.5/dos.h5', return_dos=True)

    """
    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(dos_dir, task="dos", verbose=verbose)
    if absfile.endswith(".h5"):
        dos = load_h5(absfile)
        if return_dos and not dos["/DosInfo/Project"][0]:
            return _get_total_dos(dos)
        else:
            return _get_complete_dos(dos)

    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            dos = load(fin)
        if return_dos and not dos["DosInfo"]["Project"]:
            return _get_total_dos_json(dos)
        else:
            return _get_complete_dos_json(dos)

    else:
        raise TypeError(f"{absfile} must be h5 or json file!")


def get_ele_from_h5(hpath: str = "aimd.h5") -> list:
    """Read the list of elements from the h5 file;
    Multiple ion steps do not save element information in each ion step's Structure; only the element information of the initial structure can be read.

    Parameters
    ----------
    hpath:
        h5 file path

    Returns
    -------
    ele:
        element list, Natom x 1

    Examples
    --------
    >>> from dspawpy.io.read import get_ele_from_h5
    >>> ele = get_ele_from_h5(hpath='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5')
    >>> ele
    ['H', 'H_1', 'O']

    """
    import os

    absh5 = os.path.abspath(hpath)
    from h5py import File

    data = File(absh5)
    import numpy as np

    Elements_bytes = np.asarray(data.get("/AtomInfo/Elements"))
    tempdata = np.asarray([i.decode() for i in Elements_bytes])
    ele = "".join(tempdata).split(";")

    return ele


def get_lines_without_comment(filename: str, comment: str = "#") -> list:
    """Read the content of an as file, remove comments, and return a list of lines

    Examples
    --------
    >>> from dspawpy.io.read import get_lines_without_comment
    >>> lines = get_lines_without_comment(filename='dspawpy_proj/dspawpy_tests/inputs/2.15/01/structure01.as', comment='#')
    >>> lines
    ['Total number of atoms', '13', 'Lattice', '5.60580000 0.00000000 0.00000000', '0.00000000 5.60580000 0.00000000', '0.00000000 0.00000000 16.81740000', 'Cartesian', 'H 2.48700709 3.85367720 6.93461994', 'Pt 1.40145000 1.40145000 1.98192999', 'Pt 4.20434996 1.40145000 1.98192999', 'Pt 1.40145000 4.20434996 1.98192999', 'Pt 4.20434996 4.20434996 1.98192999', 'Pt 0.00843706 0.00042409 3.91500875', 'Pt 0.00881029 2.80247953 3.91551673', 'Pt 2.81216310 -0.00105882 3.91807627', 'Pt 2.81156629 2.80392163 3.91572506', 'Pt 1.41398585 1.39603492 5.85554462', 'Pt 4.22886663 1.39820574 5.84677553', 'Pt 1.40485707 4.20963461 5.89521929', 'Pt 4.23788559 4.20753128 5.88625580']

    """
    lines = []
    import os

    absfile = os.path.abspath(filename)
    import re

    with open(absfile) as file:
        while True:
            line = file.readline()
            if line:
                line = re.sub(comment + r".*$", "", line)  # remove comment
                line = line.strip()
                if line:
                    lines.append(line)
            else:
                break

    return lines


def get_phonon_band_data(
    phonon_band_dir: str,
    verbose: bool = False,
):
    """Reads phonon band data from an h5 or json file and constructs a PhononBandStructureSymmLine object

    Parameters
    ----------
    phonon_band_dir:
        Path to the band structure file, phonon.h5 / phonon.json, or a folder containing these files

    Returns
    -------
    PhononBandStructureSymmLine

    Examples
    --------
    >>> from dspawpy.io.read import get_phonon_band_data
    >>> band_data = get_phonon_band_data("dspawpy_proj/dspawpy_tests/inputs/2.16/phonon.h5") # Read phonon band data
    >>> band_data = get_phonon_band_data("dspawpy_proj/dspawpy_tests/inputs/2.16/phonon.json") # Read phonon band data

    """
    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(phonon_band_dir, task="phonon", verbose=verbose)

    if absfile.endswith(".h5"):
        band = load_h5(absfile)
        (
            symmmetry_kpoints,
            symmetry_kPoints_index,
            qpoints,
            structure,
            frequencies,
        ) = _get_phonon_band_data_h5(band)
    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            band = load(fin)
        (
            symmmetry_kpoints,
            symmetry_kPoints_index,
            qpoints,
            structure,
            frequencies,
        ) = _get_phonon_band_data_json(band)
    else:
        raise TypeError(f"{absfile} must be h5 or json file")

    labels_dict = {}
    for i, s in enumerate(symmmetry_kpoints):
        labels_dict[s] = qpoints[symmetry_kPoints_index[i] - 1]
    from pymatgen.core.lattice import Lattice

    lattice_new = Lattice(structure.lattice.reciprocal_lattice.matrix)

    from pymatgen.phonon.bandstructure import PhononBandStructureSymmLine

    return PhononBandStructureSymmLine(
        qpoints=qpoints,  # type: ignore
        frequencies=frequencies,
        lattice=lattice_new,
        has_nac=False,
        labels_dict=labels_dict,
        structure=structure,
    )


def get_phonon_dos_data(
    phonon_dos_dir: str,
    verbose: bool = False,
):
    """Reads phonon density of states data from an h5 or json file, constructs a PhononDos object

    Parameters
    ----------
    phonon_dos_dir:
        Path to the phonon DOS file, phonon_dos.h5 / phonon_dos.json, or a folder containing these files

    Returns
    -------
    PhononDos

    Examples
    --------
    >>> from dspawpy.io.read import get_phonon_dos_data
    >>> phdos = get_phonon_dos_data(phonon_dos_dir='dspawpy_proj/dspawpy_tests/inputs/2.16.1/phonon.json')
    >>> phdos = get_phonon_dos_data(phonon_dos_dir='dspawpy_proj/dspawpy_tests/inputs/2.16.1/phonon.h5')
    >>> phdos.frequencies
    array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ,
            1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2. ,  2.1,
            2.2,  2.3,  2.4,  2.5,  2.6,  2.7,  2.8,  2.9,  3. ,  3.1,  3.2,
            3.3,  3.4,  3.5,  3.6,  3.7,  3.8,  3.9,  4. ,  4.1,  4.2,  4.3,
            4.4,  4.5,  4.6,  4.7,  4.8,  4.9,  5. ,  5.1,  5.2,  5.3,  5.4,
            5.5,  5.6,  5.7,  5.8,  5.9,  6. ,  6.1,  6.2,  6.3,  6.4,  6.5,
            6.6,  6.7,  6.8,  6.9,  7. ,  7.1,  7.2,  7.3,  7.4,  7.5,  7.6,
            7.7,  7.8,  7.9,  8. ,  8.1,  8.2,  8.3,  8.4,  8.5,  8.6,  8.7,
            8.8,  8.9,  9. ,  9.1,  9.2,  9.3,  9.4,  9.5,  9.6,  9.7,  9.8,
            9.9, 10. , 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9,
           11. , 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 12. ,
           12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 13. , 13.1,
           13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14. , 14.1, 14.2,
           14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 15. , 15.1, 15.2, 15.3,
           15.4, 15.5, 15.6, 15.7, 15.8, 15.9, 16. , 16.1, 16.2, 16.3, 16.4,
           16.5, 16.6, 16.7, 16.8, 16.9, 17. , 17.1, 17.2, 17.3, 17.4, 17.5,
           17.6, 17.7, 17.8, 17.9, 18. , 18.1, 18.2, 18.3, 18.4, 18.5, 18.6,
           18.7, 18.8, 18.9, 19. , 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7,
           19.8, 19.9, 20. ])

    """
    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(phonon_dos_dir, task="phonon_dos", verbose=verbose)
    if absfile.endswith(".h5"):
        dos = load_h5(absfile)
        frequencies = dos["/DosInfo/DosEnergy"]
        densities = dos["/DosInfo/Spin1/Dos"]
    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            dos = load(fin)
        frequencies = dos["DosInfo"]["DosEnergy"]
        densities = dos["DosInfo"]["Spin1"]["Dos"]
    else:
        raise TypeError(f"{absfile} must be h5 or json file")

    from pymatgen.phonon.dos import PhononDos

    return PhononDos(frequencies, densities)


def get_sinfo(
    datafile: str,
    scaled: bool = False,
    si=None,
    ele=None,
    ai=None,
    verbose: bool = False,
):
    r"""Reads structural information from datafile

    Parameters
    ----------
    datafile:
        Path to h5 / json file
    scaled : bool, optional
        Whether to return score coordinates, default is False
    si : int or list or str, optional
        Step in the movement trajectory, counting from 1!
        If slicing is required, use string notation: '1, 10'
        Default is None, returns all steps
    ele : list, optional
        Element list, Natom x 1
        Default to None, read from h5 file
    ai : int or list or str, optional
        The ion step number within the multi-ion steps, counting from 1
        For slicing, use string notation: '1, 10'
        Default is None, returns all ion steps

    Returns
    -------
    Nstep:
        Total number of ionic steps (number of configurations)
    ele:
        Element list, Natom x 1
    pos : np.ndarray
        Coordinate component array, Nstep x Natom x 3
    latv : np.ndarray
        Lattice vector array, Nstep x 3 x 3
    D_mag_fix:
        Information related to magnetic moments and degrees of freedom

    Examples
    --------
    >>> from dspawpy.io.read import get_sinfo
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=False, si=None, ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si=[1,10], ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si=2, ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si='1:', ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si=None, ele=['H', 'O'], ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si=None, ele='H', ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=False, si=None, ele=None, ai=[1,2])
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=False, si=None, ele=None, ai=1)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=False, si=None, ele=None, ai='1:')
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.2/rho.h5', scaled=False)

    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=False, si=None, ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si=[1,10], ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si=2, ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si='1:', ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si=None, ele=['H', 'O'], ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si=None, ele='H', ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=False, si=None, ele=None, ai=[1,2])
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=False, si=None, ele=None, ai=1)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=False, si=None, ele=None, ai='1:')
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.2/rho.json', scaled=False)

    This information can be used to further construct a Structure object.
    Specifically, refer to the `dspawpy.io.structure.build_Structures_from_datafile` function

    """
    assert ele is None or ai is None, (
        "Cannot select element and atomic number at the same time"
    )

    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(datafile, task="free", verbose=verbose)
    import numpy as np

    D_mag_fix = {}
    if absfile.endswith(".h5"):
        from h5py import File

        hf = File(absfile)  # Load the h5 file

        # decide task type by check the internal key
        if "/Structures" in hf.keys():  # multi-steps
            Total_step = np.asarray(hf.get("/Structures/FinalStep"))[
                0
            ]  # Total number of steps
            if f"/Structures/Step-{Total_step}" not in hf.keys():
                Total_step -= 1  # The final step may not have been saved yet

            if si is not None:  # Step number
                if isinstance(si, int):  # 1
                    indices = [si]

                elif isinstance(si, list) or isinstance(ai, np.ndarray):  # [1,2,3]
                    indices = si

                elif isinstance(si, str):  # ':', '1:'
                    indices = __parse_indices(si, Total_step)

                else:
                    raise ValueError("si=%s is invalid" % si)

                Nstep = len(indices)
            else:
                Nstep = Total_step
                indices = list(range(1, Nstep + 1))

            # Read the element list, which does not change with the step number and does not "merge similar items"
            Elements = np.asarray(get_ele_from_h5(absfile), dtype=object)

            # Start reading unit cells and atomic positions
            lattices = np.empty((Nstep, 3, 3))  # Nstep x 3 x 3
            location = []
            if ele is not None:  # If the user specifies an element
                if isinstance(ele, str):  # Single element symbol, e.g., 'Fe'
                    ele_list = np.asarray(ele, dtype=object)
                    location = np.where(Elements == ele_list)[0]
                # List of multiple element symbols, such as ['Fe', 'O']
                elif isinstance(ele, (list, np.ndarray)):
                    for e in ele:
                        loc = np.where(Elements == e)[0]
                        location.append(loc)
                    location = np.concatenate(location)
                else:
                    raise TypeError("ele=%s is invalid" % ele)
                elements = Elements[location]

            elif ai is not None:  # If the user specifies the atomic number
                if isinstance(ai, int):  # 1
                    ais = [ai]
                elif isinstance(ai, (list, np.ndarray)):  # [1,2,3]
                    ais = ai
                elif isinstance(ai, str):  # ':', '1:'
                    ais = __parse_indices(ai, len(Elements))
                else:
                    raise ValueError("ai=%s is invalid" % ai)
                ais = [
                    i - 1 for i in ais
                ]  # Python uses 0-based indexing, but users count from 1
                elements = Elements[ais]
                location = ais

            else:  # If none are specified
                elements = Elements
                location = list(range(len(Elements)))

            elements = elements.tolist()  # for pretty output
            Natom = len(elements)
            poses = np.empty(shape=(len(indices), Natom, 3))
            wrapped_poses = np.empty(shape=(len(indices), Natom, 3))
            for i, ind in enumerate(indices):  # Step number
                lats = np.asarray(hf.get("/Structures/Step-" + str(ind) + "/Lattice"))
                lattices[i] = lats
                # [x1,y1,z1,x2,y2,z2,x3,y3,z3], ...
                # During structure optimization, fractional coordinates are always output, regardless of what CoordinateType is specified!
                rawpos = np.asarray(
                    hf.get("/Structures/Step-" + str(ind) + "/Position"),
                )  # (3, Natom)
                pos = rawpos[:, location]
                wrapped_pos = pos - np.floor(pos)  # wrap into [0,1)
                wrapped_pos = wrapped_pos.flatten().reshape(-1, 3)
                wrapped_poses[i] = wrapped_pos

            if "/AtomInfo/Fix" in hf.keys():  # fix atom
                atomFixs_raw = np.asarray(hf.get("/AtomInfo/Fix"))
                atomfix = np.asarray(
                    ["True" if _v else "False" for _v in atomFixs_raw],
                ).reshape(-1, 3)
            else:
                atomfix = np.full(shape=(Natom, 3), fill_value="False")

            try:  # fix lattice
                latticeFixs = (
                    np.asarray(hf.get("/AtomInfo/FixLattice")).astype(bool).flatten()
                )
                assert latticeFixs.shape == (9,)
                latticeFixs = latticeFixs.reshape(
                    9,
                )  # (9,)
            except Exception as e:
                if str(e):  # ignore empty AssertionError()
                    print(e)
                latticeFixs = np.full(shape=(9,), fill_value="False")

            # iNoncollinear = False
            try:  # Spin calculation
                if "/MagInfo/TotalMagOnAtom" in hf.keys():  # collinear
                    mag = np.asarray(hf.get("/MagInfo/TotalMagOnAtom"))  # Natom x 1
                    mags = np.repeat(mag[np.newaxis, :], Nstep, axis=0).tolist()
                    D_mag_fix = {
                        "Mag": mags,
                    }
                elif "/MagInfo/TotalMagOnAtomX" in hf.keys():  # noncollinear
                    magx = np.asarray(hf.get("/MagInfo/TotalMagOnAtomX"))  # Natom x 1
                    magy = np.asarray(hf.get("/MagInfo/TotalMagOnAtomY"))  # Natom x 1
                    magz = np.asarray(hf.get("/MagInfo/TotalMagOnAtomZ"))  # Natom x 1
                    # iNoncollinear = True
                    D_mag_fix = {
                        "Mag_x": np.repeat(magx[np.newaxis, :], Nstep, axis=0).tolist(),
                        "Mag_y": np.repeat(magy[np.newaxis, :], Nstep, axis=0).tolist(),
                        "Mag_z": np.repeat(magz[np.newaxis, :], Nstep, axis=0).tolist(),
                    }
                else:
                    mag = np.zeros(shape=(Natom, 1))
                    mags = np.repeat(mag[np.newaxis, :], Nstep, axis=0).tolist()
                    D_mag_fix = {
                        "Mag": mags,
                    }

            except Exception as e:
                if str(e):  # ignore empty AssertionError()
                    print(e)
                mag = np.zeros(shape=(Natom, 1))

            # repeat atomFixs of shape Natom x 3 to Nstep x Natom x 3
            Atomfixs = np.repeat(atomfix[np.newaxis, :], Nstep, axis=0).reshape(
                Nstep,
                Natom,
                3,
            )
            D_mag_fix.update({"Fix_x": Atomfixs[:, :, 0].tolist()})
            D_mag_fix.update({"Fix_y": Atomfixs[:, :, 1].tolist()})
            D_mag_fix.update({"Fix_z": Atomfixs[:, :, 2].tolist()})

            # repeat latticeFixs of shape 9 x 1 to Nstep x Natom x 9
            latticeFixs = (
                np.repeat(latticeFixs[np.newaxis, :], Nstep * Natom, axis=0)
                .reshape(Nstep, Natom, 9)
                .tolist()
            )
            D_mag_fix.update({"FixLattice": latticeFixs})

            if scaled:  # Fractional coordinates
                for k, ind in enumerate(indices):  # Step count
                    poses[k] = wrapped_poses[k]
            else:  # Cartesian coordinates
                for k, ind in enumerate(indices):  # Steps
                    poses[k] = wrapped_poses[k] @ lattices[k]

        elif "/RelaxedStructure" in hf.keys():  # Latest NEB chain
            raise NotImplementedError("neb.h5 is not supported yet")
        elif "/UnitAtomInfo" in hf.keys():  # phonon only reads unit cell information
            raise NotImplementedError("phonon.h5 is not supported yet")

        else:  # rho, potential, elf, pcharge
            hfDict = load_h5(absfile)
            s = _get_structure(hfDict, "/AtomInfo")
            elements = np.asarray(get_ele_from_h5(absfile), dtype=object)
            poses = [s.cart_coords]
            lattices = [s.lattice.matrix]
            Nstep = 1
            D_mag_fix = None

            logger.warning(
                "--> rho/potential/elf/pcharge.h5 has no mag or fix info,\n  you should manually set it if you are going to start new calculations..",
            )

    elif absfile.endswith(".json"):
        logger.warning(
            "float number in json has precision of 4 digits by default, which may cause inconsistency with h5/log file, you may use io.jsonPrec to adjust the precision",
            category=UserWarning,
        )
        with open(absfile) as f:
            from json import load

            data = load(f)  # Load JSON file
        # decide the task type by checking the internal keys
        if "AtomInfo" in data:  # single-step task
            s = _get_structure_json(data["AtomInfo"])
            elements = [str(i) for i in s.species]
            poses = [s.cart_coords]
            lattices = [s.lattice.matrix]
            Nstep = 1
            D_mag_fix = None

        elif "UnitAtomInfo" in data:  # phonon task
            raise NotImplementedError("Read from phonon.json is not supported yet.")
        elif "IniFin" in data:  # neb.json
            raise NotImplementedError("Read from neb.json is not supported yet.")
        elif "WannierInfo" in data:
            raise NotImplementedError("wannier.json has no structure info!")

        else:  # multi-steps task
            if "Structures" in data:
                Total_step = len(data["Structures"])  # aimd.json
            else:
                Total_step = len(data)  # relax.json, neb01.json

            if ele is not None and ai is not None:
                raise ValueError("Cannot specify both ele and ai")
            # Number of steps
            if si is not None:
                if isinstance(si, int):  # 1
                    indices = [si]

                elif isinstance(si, list) or isinstance(ai, np.ndarray):  # [1,2,3]
                    indices = si

                elif isinstance(si, str):  # ':', '-3:'
                    indices = __parse_indices(si, Total_step)

                else:
                    raise ValueError("si=%s is invalid" % si)

                Nstep = len(indices)
            else:
                Nstep = Total_step
                indices = list(range(1, Nstep + 1))  # [1,Nstep+1)

            # Pre-read the total list of all elements, which will not change with the number of steps and will not "combine like terms"
            if "Structures" in data:
                Nele = len(data["Structures"][0]["Atoms"])  # relax.json
                total_elements = np.empty(
                    shape=(Nele), dtype=object
                )  # Unmerged elements list
                for i in range(Nele):
                    element = data["Structures"][0]["Atoms"][i]["Element"]
                    total_elements[i] = element
            else:
                if "Atoms" not in data[0]:
                    raise NotImplementedError("nebXX.json has no structure info!")
                Nele = len(data[0]["Atoms"])
                total_elements = np.empty(
                    shape=(Nele),
                    dtype=object,
                )  # Unmerged elements list
                for i in range(Nele):
                    element = data[0]["Atoms"][i]["Element"]
                    total_elements[i] = element

            Natom = len(total_elements)

            # Starting to read the unit cell and atomic positions
            # Select the structure based on the element's index in data['Structures']['%d' % index]['Atoms']
            if ele is not None:  # User specifies certain elements
                location = []
                if isinstance(ele, str):  # Single element symbol, e.g., 'Fe'
                    ele_list = list(ele)
                # List of multiple element symbols, such as ['Fe', 'O']
                elif isinstance(ele, (list, np.ndarray)):
                    ele_list = ele
                else:
                    raise TypeError("ele=%s is invalid" % ele)
                for e in ele_list:
                    location.append(np.where(total_elements == e)[0])
                location = np.concatenate(location)

            elif (
                ai is not None
            ):  # If the user specifies an atomic number, the element list should also be filtered accordingly
                if isinstance(ai, int):  # 1
                    ais = [ai]
                elif isinstance(ai, (list, np.ndarray)):  # [1,2,3]
                    ais = ai
                elif isinstance(ai, str):  # ':', '-3:'
                    ais = __parse_indices(ai, Natom)
                else:
                    raise ValueError("ai=%s is invalid" % ai)
                ais = [
                    i - 1 for i in ais
                ]  # Python counts from 0, but users count from 1
                location = ais
                # read lattices and poses

            else:  # If none are specified
                location = list(range(Natom))

            # Elements list that meets user requirements
            elements = total_elements[location]

            # Nstep x Natom x 3, positions are all fractional
            poses = np.empty(shape=(len(indices), len(elements), 3))
            lattices = np.empty(shape=(Nstep, 3, 3))  # Nstep x 3 x 3
            mags = []  # Nstep x Natom x ?
            Atomfixs = []  # Nstep x Natom x 1
            LatFixs = []  # Nstep x Natom x 9

            if "Structures" in data:  # aimd
                for i, ind in enumerate(indices):  # for every ionic step
                    lat = data["Structures"][ind - 1]["Lattice"]
                    lattices[i] = np.asarray(lat).reshape(3, 3)
                    mag_for_each_step = []
                    fix_for_each_step = []
                    if "FixLattice" in data["Structures"][ind - 1]:
                        fixlat_raw = data["Structures"][ind - 1]["FixLattice"]
                    else:
                        fixlat_raw = []
                    if fixlat_raw == []:
                        fixlat_raw = np.full((9, 1), fill_value=False).tolist()
                    fixlat_str = [
                        "True" if _v is True else "False" for _v in fixlat_raw
                    ]
                    fixlat_arr = np.asarray(fixlat_str).reshape(9, 1)
                    # repeat fixlat for each atom
                    fixlat = np.repeat(fixlat_arr, Natom, axis=1).T.tolist()
                    LatFixs.append(fixlat)
                    for j, sli in enumerate(location):
                        ati = data["Structures"][ind - 1]["Atoms"][sli]
                        poses[i, j, :] = ati["Position"][:]

                        mag_for_each_atom = ati["Mag"][:]
                        if mag_for_each_atom == []:
                            mag_for_each_atom = [0.0]
                        mag_for_each_step.append(mag_for_each_atom)

                        fix_for_each_atom = ati["Fix"][:]
                        if fix_for_each_atom == []:
                            fix_for_each_atom = ["False"]
                        fix_for_each_step.append(fix_for_each_atom)

                    mags.append(mag_for_each_step)
                    Atomfixs.append(fix_for_each_step)
                    if not scaled:
                        poses[i] = np.dot(poses[i], lattices[i])

            else:  # relax, neb01
                logger.warning(
                    "mag and fix info are not available for relax.json and nebXX.json yet, trying read info...",
                    category=UserWarning,
                )

                for i, ind in enumerate(indices):  # for every ionic step
                    lat = data[ind - 1]["Lattice"]
                    lattices[i] = np.asarray(lat).reshape(3, 3)
                    mag_for_each_step = []
                    fix_for_each_step = []
                    if "FixLattice" in data[ind - 1]:
                        fixlat_raw = data[ind - 1]["FixLattice"]
                        if fixlat_raw is None:
                            fixlat_raw = np.full((9, 1), fill_value=False).tolist()
                        fixlat_str = [
                            "True" if _v is True else "False" for _v in fixlat_raw
                        ]
                        fixlat_arr = np.asarray(fixlat_str).reshape(9, 1)
                        # repeat fixlat for each atom
                        fixlat = np.repeat(fixlat_arr, Natom, axis=1).T.tolist()
                    else:
                        fixlat = np.full((Natom, 9), fill_value=False).tolist()

                    LatFixs.append(fixlat)
                    for j, sli in enumerate(location):
                        ati = data[ind - 1]["Atoms"][sli]
                        poses[i, j, :] = ati["Position"][:]

                        mag_for_each_atom = ati["Mag"][:]
                        if mag_for_each_atom == []:
                            mag_for_each_atom = [0.0]
                        mag_for_each_step.append(mag_for_each_atom)

                        fix_for_each_atom = ati["Fix"][:]
                        if fix_for_each_atom == []:
                            fix_for_each_atom = ["False"]
                        fix_for_each_step.append(fix_for_each_atom)

                    mags.append(mag_for_each_step)
                    Atomfixs.append(fix_for_each_step)
                    if not scaled:
                        poses[i] = np.dot(poses[i], lattices[i])

            elements = elements.tolist()
            Mags = np.asarray(mags).tolist()  # (Nstep, Natom, ?) or (Nstep, 0,)

            D_mag_fix = {"Mag": Mags, "Fix": Atomfixs, "LatticeFixs": LatFixs}

    else:
        raise ValueError(
            "get_sinfo function only accept datafile of .h5 / .json format!",
        )

    return Nstep, elements, poses, lattices, D_mag_fix


def load_h5(dir_h5: str) -> dict:
    """Traverse and read data from h5 file, save it in dictionary format

    Use this function with caution, as it will read a lot of unnecessary data and take a long time.

    Parameters
    ----------
    dir_h5:
        Path to the h5 file

    Returns
    -------
    data:
        Data dictionary

    Examples
    --------
    >>> from dspawpy.io.read import load_h5
    >>> data = load_h5(dir_h5='dspawpy_proj/dspawpy_tests/inputs/2.2/scf.h5')
    >>> data.keys()
    dict_keys(['/AtomInfo/CoordinateType', '/AtomInfo/Elements', '/AtomInfo/Grid', '/AtomInfo/Lattice', '/AtomInfo/Position', '/Eigenvalue/CBM/BandIndex', '/Eigenvalue/CBM/Energy', '/Eigenvalue/CBM/Kpoint', '/Eigenvalue/NumberOfBand', '/Eigenvalue/Spin1/BandEnergies', '/Eigenvalue/Spin1/Kpoints/Coordinates', '/Eigenvalue/Spin1/Kpoints/Grid', '/Eigenvalue/Spin1/Kpoints/NumberOfKpoints', '/Eigenvalue/Spin1/Occupation', '/Eigenvalue/VBM/BandIndex', '/Eigenvalue/VBM/Energy', '/Eigenvalue/VBM/Kpoint', '/Electron', '/Energy/EFermi', '/Energy/TotalEnergy', '/Energy/TotalEnergy0', '/Force/ForceOnAtoms', '/Stress/Direction', '/Stress/Pressure', '/Stress/Stress', '/Stress/Total', '/Structures/FinalStep', '/Structures/Step-1/Lattice', '/Structures/Step-1/Position'])

    """

    def get_names(key, h5_object):
        names.append(h5_object.name)

    def is_dataset(name):
        for name_inTheList in names:
            if name_inTheList.find(name + "/") != -1:
                return False
        return True

    import numpy as np

    def get_data(key, h5_object):
        if is_dataset(h5_object.name):
            _data = np.asarray(h5_object)
            if _data.dtype == "|S1":  # Convert to string and split by ";"
                byte2str = [str(bi, "utf-8") for bi in _data]
                string = ""
                for char in byte2str:
                    string += char
                _data = np.asarray([elem for elem in string.strip().split(";")])
            # "/group1/group2/.../groupN/dataset" : value
            data[h5_object.name] = _data.tolist()

    import os

    from h5py import File

    with File(os.path.abspath(dir_h5), "r") as fin:
        names = []
        data = {}
        fin.visititems(get_names)
        fin.visititems(get_data)

        return data


def __parse_indices(index: str, maxIndex: int) -> list:
    """Parse the atomic or structural index string input by the user

    Input:
        - index: User input atom index/element string, e.g. '1:3,5,7:10'
        - maxIndex: Maximum index, e.g., 10
    Output:
        - indices: List of parsed atomic numbers, e.g., [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    assert ":" in index, (
        "If you don't want to slice the index, please enter an integer or a list"
    )
    blcs = index.split(",")
    indices = []
    for blc in blcs:
        if ":" in blc:  # Slicing
            low = blc.split(":")[0]
            if not low:
                low = 1  # Start from 1
            else:
                low = int(low)
                assert low > 0, "Index start at 1!"
            high = blc.split(":")[1]
            if not high:
                high = maxIndex
            else:
                high = int(high)
                assert high <= maxIndex, "Index too large!"

            for i in range(low, high + 1):
                indices.append(i)
        else:  # Single number
            indices.append(int(blc))
    return indices


def _get_lammps_non_orthogonal_box(lat: Sequence):
    """Calculate the box boundary parameters for input to LAMMPS, used for generating dump structure files

    Parameters
    ----------
    lat : np.ndarray
        Common non-triangular 3x3 matrices

    Returns
    -------
    box_bounds:
        Used for inputting box boundaries into LAMMPS

    """
    # https://docs.lammps.org/Howto_triclinic.html
    A = lat[0]
    B = lat[1]
    C = lat[2]
    import numpy as np

    assert np.cross(A, B).dot(C) > 0, "Lat is not right handed"

    # Convert a general 3x3 matrix to a standard upper triangular matrix
    alpha = np.arccos(np.dot(B, C) / (np.linalg.norm(B) * np.linalg.norm(C)))
    beta = np.arccos(np.dot(A, C) / (np.linalg.norm(A) * np.linalg.norm(C)))
    gamma = np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)))

    ax = np.linalg.norm(A)
    a = np.asarray([ax, 0, 0])

    bx = np.linalg.norm(B) * np.cos(gamma)
    by = np.linalg.norm(B) * np.sin(gamma)
    b = np.asarray([bx, by, 0])

    cx = np.linalg.norm(C) * np.cos(beta)
    cy = (np.linalg.norm(B) * np.linalg.norm(C) - bx * cx) / by
    cz = np.sqrt(abs(np.linalg.norm(C) ** 2 - cx**2 - cy**2))
    c = np.asarray([cx, cy, cz])

    # triangluar matrix in lammmps cell format
    # note that in OVITO, it will be down-triangular one
    # lammps_lattice = np.asarray([a,b,c]).T

    # write lammps box parameters
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=The%20inverse%20relationship%20can%20be%20written%20as%20follows
    lx = np.linalg.norm(a)
    xy = np.linalg.norm(b) * np.cos(gamma)
    xz = np.linalg.norm(c) * np.cos(beta)
    ly = np.sqrt(np.linalg.norm(b) ** 2 - xy**2)
    yz = (np.linalg.norm(b) * np.linalg.norm(c) * np.cos(alpha) - xy * xz) / ly
    lz = np.sqrt(np.linalg.norm(c) ** 2 - xz**2 - yz**2)

    # "The parallelepiped has its “origin” at (xlo,ylo,zlo) and is defined by 3 edge vectors starting from the origin given by a = (xhi-xlo,0,0); b = (xy,yhi-ylo,0); c = (xz,yz,zhi-zlo)."
    # Let the origin be at (0,0,0), then xlo = ylo = zlo = 0
    xlo = ylo = zlo = 0
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=the%20LAMMPS%20box%20sizes%20(lx%2Cly%2Clz)%20%3D%20(xhi%2Dxlo%2Cyhi%2Dylo%2Czhi%2Dzlo)
    xhi = lx + xlo
    yhi = ly + ylo
    zhi = lz + zlo
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=This%20bounding%20box%20is%20convenient%20for%20many%20visualization%20programs%20and%20is%20calculated%20from%20the%209%20triclinic%20box%20parameters%20(xlo%2Cxhi%2Cylo%2Cyhi%2Czlo%2Czhi%2Cxy%2Cxz%2Cyz)%20as%20follows%3A
    xlo_bound = xlo + np.min([0, xy, xz, xy + xz])
    xhi_bound = xhi + np.max([0, xy, xz, xy + xz])
    ylo_bound = ylo + np.min([0, yz])
    yhi_bound = yhi + np.max([0, yz])
    zlo_bound = zlo
    zhi_bound = zhi
    box_bounds = np.asarray(
        [
            [xlo_bound, xhi_bound, xy],
            [ylo_bound, yhi_bound, xz],
            [zlo_bound, zhi_bound, yz],
        ],
    )

    return box_bounds


def _get_total_dos(dos: dict):
    # h5 -> Dos Obj
    import numpy as np

    energies = np.asarray(dos["/DosInfo/DosEnergy"])
    from pymatgen.electronic_structure.core import Spin

    if dos["/DosInfo/SpinType"][0] != "collinear":
        densities = {Spin.up: np.asarray(dos["/DosInfo/Spin1/Dos"])}
    else:
        densities = {
            Spin.up: np.asarray(dos["/DosInfo/Spin1/Dos"]),
            Spin.down: np.asarray(dos["/DosInfo/Spin2/Dos"]),
        }

    efermi = dos["/DosInfo/EFermi"][0]

    from pymatgen.electronic_structure.dos import Dos

    return Dos(efermi, energies, densities)


def _get_total_dos_json(dos: dict):
    # json -> Dos Obj
    import numpy as np

    energies = np.asarray(dos["DosInfo"]["DosEnergy"])
    from pymatgen.electronic_structure.core import Spin

    if dos["DosInfo"]["SpinType"] != "collinear":
        densities = {Spin.up: np.asarray(dos["DosInfo"]["Spin1"]["Dos"])}
    else:
        densities = {
            Spin.up: np.asarray(dos["DosInfo"]["Spin1"]["Dos"]),
            Spin.down: np.asarray(dos["DosInfo"]["Spin2"]["Dos"]),
        }
    efermi = dos["DosInfo"]["EFermi"]
    from pymatgen.electronic_structure.dos import Dos

    return Dos(efermi, energies, densities)


def _get_complete_dos(dos: dict):
    # h5 -> CompleteDos Obj
    total_dos = _get_total_dos(dos)
    structure = _get_structure(dos, "/AtomInfo")
    N = len(structure)
    pdos = [{} for i in range(N)]
    number_of_spin = 2 if dos["/DosInfo/SpinType"][0] == "collinear" else 1

    from pymatgen.electronic_structure.core import Orbital, Spin

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        if dos["/DosInfo/Project"][0]:
            atomindexs = dos["/DosInfo/" + spin_key + "/ProjectDos/AtomIndexs"][0]
            orbitindexs = dos["/DosInfo/" + spin_key + "/ProjectDos/OrbitIndexs"][0]
            for atom_index in range(atomindexs):
                for orbit_index in range(orbitindexs):
                    orbit_name = Orbital(orbit_index)
                    Contribution = dos[
                        "/DosInfo/"
                        + spin_key
                        + "/ProjectDos"
                        + str(atom_index + 1)
                        + "/"
                        + str(orbit_index + 1)
                    ]
                    if orbit_name in pdos[atom_index].keys():
                        pdos[atom_index][orbit_name].update({spin: Contribution})
                    else:
                        pdos[atom_index][orbit_name] = {spin: Contribution}

            pdoss = {structure[i]: pd for i, pd in enumerate(pdos)}
        else:
            pdoss = {}

    from pymatgen.electronic_structure.dos import CompleteDos

    return CompleteDos(structure, total_dos, pdoss)  # type: ignore


def _get_complete_dos_json(dos: dict):
    # json -> CompleteDos Obj
    total_dos = _get_total_dos_json(dos)
    structure = _get_structure_json(dos["AtomInfo"])
    N = len(structure)
    pdos = [{} for i in range(N)]
    number_of_spin = 2 if dos["DosInfo"]["SpinType"] == "collinear" else 1

    from pymatgen.electronic_structure.core import Orbital, Spin

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        if dos["DosInfo"]["Project"]:
            project = dos["DosInfo"][spin_key]["ProjectDos"]
            for p in project:
                atom_index = p["AtomIndex"] - 1
                o = p["OrbitIndex"] - 1
                orbit_name = Orbital(o)
                if orbit_name in pdos[atom_index].keys():
                    pdos[atom_index][orbit_name].update({spin: p["Contribution"]})
                else:
                    pdos[atom_index][orbit_name] = {spin: p["Contribution"]}
            pdoss = {structure[i]: pd for i, pd in enumerate(pdos)}
        else:
            pdoss = {}

    from pymatgen.electronic_structure.dos import CompleteDos

    return CompleteDos(structure, total_dos, pdoss)  # type: ignore


def _get_structure(hdf5: dict, key: str):
    """For single-step task"""
    # load_h5 -> Structure Obj
    import numpy as np

    lattice = np.asarray(hdf5[key + "/Lattice"]).reshape(3, 3)
    elements = hdf5[key + "/Elements"]
    positions = hdf5[key + "/Position"]
    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = hdf5[key + "/CoordinateType"][0] == "Direct"
    import re

    elements = [re.sub(r"_", "", e) for e in elements]

    from pymatgen.core.structure import Structure

    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def _get_structure_json(atominfo: dict):
    """For single-step task"""
    import numpy as np

    lattice = np.asarray(atominfo["Lattice"]).reshape(3, 3)
    elements = []
    positions = []
    for atom in atominfo["Atoms"]:
        elements.append(atom["Element"])
        positions.extend(atom["Position"])

    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = atominfo["CoordinateType"] == "Direct"
    import re

    elements = [re.sub(r"_", "", e) for e in elements]

    from pymatgen.core.structure import Structure

    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def _get_band_data_h5(band: dict, iwan: bool = False, zero_to_efermi: bool = False):
    if iwan:
        bd = "WannBandInfo"
    else:
        bd = "BandInfo"
    number_of_band = band[f"/{bd}/NumberOfBand"][0]
    number_of_kpoints = band[f"/{bd}/NumberOfKpoints"][0]
    if band[f"/{bd}/SpinType"][0] != "collinear":
        number_of_spin = 1
    else:
        number_of_spin = 2

    symmetry_kPoints_index = band[f"/{bd}/SymmetryKPointsIndex"]

    efermi = band[f"/{bd}/EFermi"][0]
    eigenvals = {}
    import numpy as np
    from pymatgen.electronic_structure.core import Spin

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down

        if f"/{bd}/" + spin_key + "/BandEnergies" in band:
            data = band[f"/{bd}/" + spin_key + "/BandEnergies"]
        elif f"/{bd}/" + spin_key + "/Band" in band:
            data = band[f"/{bd}/" + spin_key + "/Band"]
        else:
            raise KeyError("Band key error")
        band_data = np.asarray(data).reshape((number_of_kpoints, number_of_band)).T

        if zero_to_efermi:
            eigenvals[spin] = band_data - efermi
        else:
            eigenvals[spin] = band_data

    kpoints = np.asarray(band[f"/{bd}/CoordinatesOfKPoints"]).reshape(
        number_of_kpoints,
        3,
    )

    structure = _get_structure(band, "/AtomInfo")
    labels_dict = {}

    for i, s in enumerate(band[f"/{bd}/SymmetryKPoints"]):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]

    # read projection data
    projections = None
    if f"/{bd}/IsProject" in band:
        if band[f"/{bd}/IsProject"][0]:
            projections = {}
            number_of_orbit = len(band[f"/{bd}/Orbit"])
            projection = np.zeros(
                (number_of_band, number_of_kpoints, number_of_orbit, len(structure)),
            )

            for i in range(number_of_spin):
                spin_key = "Spin" + str(i + 1)
                spin = Spin.up if i == 0 else Spin.down

                atomindexs = band[f"/{bd}/" + spin_key + "/ProjectBand/AtomIndex"][0]
                orbitindexs = band[f"/{bd}/" + spin_key + "/ProjectBand/OrbitIndexs"][0]
                for atom_index in range(atomindexs):
                    for orbit_index in range(orbitindexs):
                        project_data = band[
                            f"/{bd}/"
                            + spin_key
                            + "/ProjectBand/1/"
                            + str(atom_index + 1)
                            + "/"
                            + str(orbit_index + 1)
                        ]
                        projection[:, :, orbit_index, atom_index] = (
                            np.asarray(project_data)
                            .reshape((number_of_kpoints, number_of_band))
                            .T
                        )
                projections[spin] = projection

    if zero_to_efermi:
        efermi = 0  # set to 0

    return structure, kpoints, eigenvals, efermi, labels_dict, projections


def _get_band_data_json(
    band: dict,
    syst: Optional[dict] = None,
    iwan: bool = False,
    zero_to_efermi: bool = False,
):
    # syst is only required for wannier band structure
    if iwan:
        bd = "WannBandInfo"
        assert syst is not None, "syst is required for wannier band structure"
        efermi = syst["Energy"]["EFermi"]
        structure = _get_structure_json(syst["AtomInfo"])
    else:
        bd = "BandInfo"
        if "EFermi" in band[bd]:
            efermi = band[bd]["EFermi"]
        else:
            logger.warning("EFermi not found in band data, set to 0")
            efermi = 0
        structure = _get_structure_json(band["AtomInfo"])

    number_of_band = band[bd]["NumberOfBand"]
    number_of_kpoints = band[bd]["NumberOfKpoints"]
    # ! wannier.json has no SpinType key
    # if band[bd]["SpinType"][0] != "collinear":
    if "Spin2" not in band[bd]:
        number_of_spin = 1
    else:
        number_of_spin = 2

    symmetry_kPoints_index = band[bd]["SymmetryKPointsIndex"]
    eigenvals = {}
    import numpy as np
    from pymatgen.electronic_structure.core import Spin

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down

        if "BandEnergies" in band[bd][spin_key]:
            data = band[bd][spin_key]["BandEnergies"]
        elif "Band" in band[bd][spin_key]:
            data = band[bd][spin_key]["Band"]
        else:
            raise KeyError("Band key error")

        band_data = np.asarray(data).reshape((number_of_kpoints, number_of_band)).T

        if zero_to_efermi:
            eigenvals[spin] = band_data - efermi

        else:
            eigenvals[spin] = band_data

    kpoints = np.asarray(band[bd]["CoordinatesOfKPoints"]).reshape(number_of_kpoints, 3)

    labels_dict = {}

    for i, s in enumerate(band[bd]["SymmetryKPoints"]):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]

    # read projection data
    projections = None
    if "IsProject" in band[bd].keys():
        if band[bd]["IsProject"]:
            projections = {}
            number_of_orbit = len(band[bd]["Orbit"])
            projection = np.zeros(
                (number_of_band, number_of_kpoints, number_of_orbit, len(structure)),
            )

            for i in range(number_of_spin):
                spin_key = "Spin" + str(i + 1)
                spin = Spin.up if i == 0 else Spin.down

                data = band[bd][spin_key]["ProjectBand"]
                for d in data:
                    orbit_index = d["OrbitIndex"] - 1
                    atom_index = d["AtomIndex"] - 1
                    project_data = d["Contribution"]
                    projection[:, :, orbit_index, atom_index] = (
                        np.asarray(project_data)
                        .reshape((number_of_kpoints, number_of_band))
                        .T
                    )
                projections[spin] = projection

    if zero_to_efermi:
        logger.warning("Setting efemi to 0 because zero_to_efermi is True")
        efermi = 0  # set to 0

    return structure, kpoints, eigenvals, efermi, labels_dict, projections


def _get_phonon_band_data_h5(band: dict):
    import numpy as np

    number_of_band = band["/BandInfo/NumberOfBand"][0]
    number_of_qpoints = band["/BandInfo/NumberOfQPoints"][0]
    symmmetry_qpoints = band["/BandInfo/SymmetryQPoints"]
    symmetry_qPoints_index = band["/BandInfo/SymmetryQPointsIndex"]
    qpoints = np.asarray(band["/BandInfo/CoordinatesOfQPoints"]).reshape(
        number_of_qpoints,
        3,
    )
    if "/SupercellAtomInfo/CoordinateType" in band:
        structure = _get_structure(band, "/SupercellAtomInfo")
    else:
        structure = _get_structure(band, "/AtomInfo")

    spin_key = "Spin1"
    if "/BandInfo/" + spin_key + "/BandEnergies" in band:
        data = band["/BandInfo/" + spin_key + "/BandEnergies"]
    elif "/BandInfo/" + spin_key + "/Band" in band:
        data = band["/BandInfo/" + spin_key + "/Band"]
    else:
        raise KeyError("Band key error")
    frequencies = np.asarray(data).reshape((number_of_qpoints, number_of_band)).T

    return symmmetry_qpoints, symmetry_qPoints_index, qpoints, structure, frequencies


def _get_phonon_band_data_json(band: dict):
    import numpy as np

    number_of_band = band["BandInfo"]["NumberOfBand"]
    number_of_qpoints = band["BandInfo"]["NumberOfQPoints"]

    symmmetry_qpoints = band["BandInfo"]["SymmetryQPoints"]
    symmetry_qPoints_index = band["BandInfo"]["SymmetryQPointsIndex"]
    qpoints = np.asarray(band["BandInfo"]["CoordinatesOfQPoints"]).reshape(
        number_of_qpoints,
        3,
    )
    if "SupercellAtomInfo" in band:
        structure = _get_structure_json(band["SupercellAtomInfo"])
    else:
        structure = _get_structure_json(band["AtomInfo"])

    spin_key = "Spin1"
    if "BandEnergies" in band["BandInfo"][spin_key]:
        data = band["BandInfo"][spin_key]["BandEnergies"]
    elif "Band" in band["BandInfo"][spin_key]:
        data = band["BandInfo"][spin_key]["Band"]
    else:
        raise KeyError("Band key error")
    frequencies = np.asarray(data).reshape((number_of_qpoints, number_of_band)).T

    return symmmetry_qpoints, symmetry_qPoints_index, qpoints, structure, frequencies
