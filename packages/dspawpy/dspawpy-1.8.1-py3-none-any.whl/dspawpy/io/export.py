from dspawpy.io.read import load_h5
import os
import numpy as np
import polars as pl
from pathlib import Path
from typing import Union


def read_dos(
    dosfile: Union[str, Path],
    mode: int = 5,
    hide_index: bool = False,
    fmt: str = "8.3f",
) -> pl.DataFrame:
    """Construct a dataframe of dos data from an h5 or json file.

    Parameters
    ----------
    bandfile: str | Path
        band data file location, such as 'band.json'.
    mode: int
        which projection mode, only valid for pband data.
    hide_index: bool
        hide index column in dataframe or not.
    fmt: str
        control display decimal, such as '8.3f'

    Examples
    --------
    >>> from dspawpy.io.export import read_dos
    >>> read_dos(dosfile='dspawpy_proj/dspawpy_tests/inputs/2.5/dos.h5')
    efermi=4.8711625000000005 eV
    shape: (401, 3)
    ┌───────┬──────────┬──────────┐
    │ index ┆ energy   ┆ dos      │
    ╞═══════╪══════════╪══════════╡
    │ 1     ┆   -4.830 ┆    0.690 │
    │ 2     ┆   -4.780 ┆    0.719 │
    │ 3     ┆   -4.730 ┆    0.757 │
    │ 4     ┆   -4.680 ┆    0.809 │
    │ 5     ┆   -4.630 ┆    0.950 │
    │ …     ┆ …        ┆ …        │
    │ 397   ┆   14.970 ┆    0.044 │
    │ 398   ┆   15.020 ┆    0.041 │
    │ 399   ┆   15.070 ┆    0.039 │
    │ 400   ┆   15.120 ┆    0.037 │
    │ 401   ┆   15.170 ┆    0.035 │
    └───────┴──────────┴──────────┘
    """
    absfile = os.path.abspath(dosfile)

    def _read_tdos_h5(dos):
        energies = np.asarray(dos["/DosInfo/DosEnergy"])

        if dos["/DosInfo/SpinType"][0] != "collinear":
            densities = {
                "energy": energies,
                "dos": np.asarray(dos["/DosInfo/Spin1/Dos"]),
            }
        else:
            densities = {
                "energy": energies,
                "up": np.asarray(dos["/DosInfo/Spin1/Dos"]),
                "down": np.asarray(dos["/DosInfo/Spin2/Dos"]),
            }
        return pl.DataFrame(data=densities)

    def _read_tdos_json(dos):
        energies = np.asarray(dos["DosInfo"]["DosEnergy"])

        if dos["DosInfo"]["SpinType"] != "collinear":
            densities = {
                "energy": energies,
                "dos": np.asarray(dos["DosInfo"]["Spin1"]["Dos"]),
            }
        else:
            densities = {
                "energy": energies,
                "up": np.asarray(dos["DosInfo"]["Spin1"]["Dos"]),
                "down": np.asarray(dos["DosInfo"]["Spin2"]["Dos"]),
            }
        return pl.DataFrame(data=densities)

    def _read_pdos_h5(dos, mode):
        energies: list[float] = dos["/DosInfo/DosEnergy"]
        data = {}
        orbitals: list[str] = dos["/DosInfo/Orbit"]

        atom_index: int = dos["/DosInfo/Spin1/ProjectDos/AtomIndexs"][0]  # 2
        orb_index: int = dos["/DosInfo/Spin1/ProjectDos/OrbitIndexs"][0]  # 9
        if dos["/DosInfo/SpinType"] == "collinear":
            for ai in range(atom_index):
                for oi in range(orb_index):
                    data.update(
                        {
                            f"{ai + 1}{orbitals[oi]}-up": dos[
                                f"/DosInfo/Spin1/ProjectDos{ai + 1}/{oi + 1}"
                            ]
                        }
                    )
                    data.update(
                        {
                            f"{ai + 1}{orbitals[oi]}-down": dos[
                                f"/DosInfo/Spin2/ProjectDos{ai + 1}/{oi + 1}"
                            ]
                        }
                    )
        else:
            for ai in range(atom_index):
                for oi in range(orb_index):
                    data.update(
                        {
                            f"{ai + 1}{orbitals[oi]}": dos[
                                f"/DosInfo/Spin1/ProjectDos{ai + 1}/{oi + 1}"
                            ]
                        }
                    )

        _data = _refactor_data(energies, data, mode)

        return pl.DataFrame(_data)

    def _read_pdos_json(dos, mode):
        energies: list[float] = dos["DosInfo"]["DosEnergy"]
        data = {}
        orbitals: list[str] = dos["DosInfo"]["Orbit"]

        if dos["DosInfo"]["SpinType"] == "collinear":
            project = dos["DosInfo"]["Spin1"]["ProjectDos"]
            for p in project:
                atom_index = p["AtomIndex"]
                orb_index = p["OrbitIndex"] - 1
                contrib = p["Contribution"]
                data.update({f"{atom_index}{orbitals[orb_index]}-up": contrib})
            project = dos["DosInfo"]["Spin2"]["ProjectDos"]
            for p in project:
                atom_index = p["AtomIndex"]
                orb_index = p["OrbitIndex"] - 1
                contrib = p["Contribution"]
                data.update({f"{atom_index}{orbitals[orb_index]}-down": contrib})
        else:
            project = dos["DosInfo"]["Spin1"]["ProjectDos"]
            for p in project:
                atom_index = p["AtomIndex"]
                orb_index = p["OrbitIndex"] - 1
                contrib = p["Contribution"]
                data.update({f"{atom_index}{orbitals[orb_index]}": contrib})

        _data = _refactor_data(energies, data, mode)

        return pl.DataFrame(_data)

    def _refactor_data(energies, data, mode):
        if mode == 1:  # spdf
            _data = {"energy": energies}
            for k, v in data.items():
                ao = k.split("-")[0]
                _, o = _split_atomIndex_orbital(ao)
                o_1st = o[0]
                if o_1st in _data:
                    _data[o_1st] += np.asarray(v)
                else:
                    _data[o_1st] = np.asarray(v)
        elif mode == 2:  # spxpy...
            _data = {"energy": energies}
            for k, v in data.items():
                ao = k.split("-")[0]
                _, o = _split_atomIndex_orbital(ao)
                if o in _data:
                    _data[o] += np.asarray(v)
                else:
                    _data[o] = np.asarray(v)
        elif mode == 3:  # element
            elements: list[str] = [atom["Element"] for atom in dos["AtomInfo"]["Atoms"]]
            _data = {"energy": energies}
            for k, v in data.items():
                ao = k.split("-")[0]
                a, _ = _split_atomIndex_orbital(ao)
                e = elements[a - 1]
                if e in _data:
                    _data[e] += np.asarray(v)
                else:
                    _data[e] = np.asarray(v)
        elif mode == 4:  # atom+spdf
            _data = {"energy": energies}
            for k, v in data.items():
                ao = k.split("-")[0]
                a, o = _split_atomIndex_orbital(ao)
                o_1st = o[0]
                if o_1st in _data:
                    _data[f"{a}{o_1st}"] += np.asarray(v)
                else:
                    _data[f"{a}{o_1st}"] = np.asarray(v)
        elif mode == 5:  # atom+spxpy...
            _data = data
        elif mode == 6:  # atom+t2g/eg
            _data = {"energy": energies}
            for k, v in data.items():
                ao = k.split("-")[0]
                a, o = _split_atomIndex_orbital(ao)
                if o in ["dxy", "dxz", "dyz"]:
                    if a in _data:
                        _data[f"{a}t2g"] += np.asarray(v)
                    else:
                        _data[f"{a}t2g"] = np.asarray(v)
                elif o in ["dz2", "dx2y2"]:
                    if a in _data:
                        _data[f"{a}eg"] += np.asarray(v)
                    else:
                        _data[f"{a}eg"] = np.asarray(v)
        else:
            print(f"{mode=} not supported yet")
            exit(1)

        return _data

    if absfile.endswith(".h5"):
        dos = load_h5(absfile)
        efermi = dos["/DosInfo/EFermi"][0]
        print(f"{efermi=} eV")
        if not dos["/DosInfo/Project"][0]:
            df = _read_tdos_h5(dos)

        else:
            df = _read_pdos_h5(dos, mode)

    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            dos = load(fin)
        if not dos["DosInfo"]["Project"]:
            df = _read_tdos_json(dos)
        else:
            df = _read_pdos_json(dos, mode)

    else:
        raise TypeError(f"{absfile} must be h5 or json file!")

    df = _format_float_columns_as_str_mapelements(df, fmt)

    if hide_index:
        return df
    else:
        return df.with_row_index(name="index", offset=1)


def read_band(
    bandfile: Union[str, Path],
    mode: int = 5,
    hide_index: bool = False,
    fmt: str = "8.3f",
):
    """Construct a dataframe of band structure data from an h5 or json file.

    Parameters
    ----------
    bandfile: str | Path
        band data file location, such as 'band.json'.
    mode: int
        which projection mode, only valid for pband data.
    hide_index: bool
        hide index column in dataframe or not.
    fmt: str
        control display decimal, such as '8.3f'

    Examples
    --------
    >>> from dspawpy.io.export import read_band
    >>> read_band(bandfile='dspawpy_proj/dspawpy_tests/inputs/2.3/band.h5')
    efermi=5.1696 eV
    shape: (150, 16)
    ┌───────┬──────────┬──────────┬──────────┬───┬──────────┬──────────┬──────────┬──────────┐
    │ index ┆ kx       ┆ ky       ┆ kz       ┆ … ┆ 9        ┆ 10       ┆ 11       ┆ 12       │
    ╞═══════╪══════════╪══════════╪══════════╪═══╪══════════╪══════════╪══════════╪══════════╡
    │ 1     ┆    0.000 ┆    0.500 ┆    0.246 ┆ … ┆   -4.950 ┆    7.858 ┆   -6.766 ┆    8.395 │
    │ 2     ┆    0.000 ┆    0.172 ┆    0.246 ┆ … ┆   -0.491 ┆    9.558 ┆    3.944 ┆   12.139 │
    │ 3     ┆    0.000 ┆    0.672 ┆    0.491 ┆ … ┆    1.294 ┆   11.707 ┆    4.708 ┆   12.457 │
    │ 4     ┆    0.017 ┆    0.500 ┆    0.233 ┆ … ┆    3.604 ┆   12.532 ┆    4.708 ┆   12.457 │
    │ 5     ┆    0.000 ┆    0.181 ┆    0.233 ┆ … ┆    7.334 ┆   13.710 ┆    7.369 ┆   13.616 │
    │ …     ┆ …        ┆ …        ┆ …        ┆ … ┆ …        ┆ …        ┆ …        ┆ …        │
    │ 146   ┆    0.155 ┆    0.272 ┆    0.483 ┆ … ┆    3.067 ┆    8.304 ┆    0.255 ┆   12.534 │
    │ 147   ┆    0.655 ┆    0.543 ┆    0.483 ┆ … ┆    3.906 ┆   12.505 ┆    3.982 ┆   15.529 │
    │ 148   ┆    0.500 ┆    0.259 ┆    0.500 ┆ … ┆    4.713 ┆   12.505 ┆    3.982 ┆   15.942 │
    │ 149   ┆    0.164 ┆    0.259 ┆    0.500 ┆ … ┆    7.675 ┆   12.908 ┆    6.606 ┆   16.040 │
    │ 150   ┆    0.664 ┆    0.517 ┆    0.500 ┆ … ┆    7.700 ┆   16.401 ┆    8.395 ┆   17.259 │
    └───────┴──────────┴──────────┴──────────┴───┴──────────┴──────────┴──────────┴──────────┘
    """
    absfile = os.path.abspath(bandfile)

    def _read_tband_h5(band):
        kcoord = np.asarray(band["/BandInfo/CoordinatesOfKPoints"])  # 3,nkpt
        kx = kcoord[0, :]
        ky = kcoord[1, :]
        kz = kcoord[2, :]
        data = {
            "kx": kx,
            "ky": ky,
            "kz": kz,
        }
        bands = np.asarray(band["/BandInfo/Spin1/BandEnergies"])  # nband, nkpt

        if not band["/BandInfo/IsProject"][0]:
            for i in range(bands.shape[0]):
                data[f"{i + 1}"] = bands[i, :]
        else:
            for i in range(bands.shape[0]):
                data[f"{i + 1}-up"] = bands[i, :]
            bands = np.asarray(band["/BandInfo/Spin2/BandEnergies"])  # nband, nkpt
            for i in range(bands.shape[0]):
                data[f"{i + 1}-down"] = bands[i, :]

        return pl.DataFrame(data)

    def _read_tband_json(band):
        kc: list[float] = band["BandInfo"]["CoordinatesOfKPoints"]
        nkpt: int = band["BandInfo"]["NumberOfKpoints"]
        nband: int = band["BandInfo"]["NumberOfBand"]
        kcoord = np.array(kc).reshape(3, nkpt)
        kx = kcoord[0, :]
        ky = kcoord[1, :]
        kz = kcoord[2, :]
        data = {
            "kx": kx,
            "ky": ky,
            "kz": kz,
        }
        bands = np.asarray(band["BandInfo"]["Spin1"]["BandEnergies"]).reshape(
            nband, nkpt
        )
        if not band["BandInfo"]["IsProject"]:
            for i in range(bands.shape[0]):
                data[f"{i + 1}"] = bands[i, :]
        else:
            for i in range(bands.shape[0]):
                data[f"{i + 1}-up"] = bands[i, :]
            bands = np.asarray(band["BandInfo"]["Spin2"]["BandEnergies"])  # nband, nkpt
            for i in range(bands.shape[0]):
                data[f"{i + 1}-down"] = bands[i, :]

        return pl.DataFrame(data)

    def _read_pband_h5(band, mode):
        kc = band["/BandInfo/CoordinatesOfKPoints"]
        nkpt: int = band["/BandInfo/NumberOfKpoints"][0]
        nband: int = band["/BandInfo/NumberOfBand"][0]
        kcoord = np.array(kc).reshape(3, nkpt)
        kx = kcoord[0, :]
        ky = kcoord[1, :]
        kz = kcoord[2, :]
        data = {
            "kx": kx,
            "ky": ky,
            "kz": kz,
        }
        orbitals: list[str] = band["/BandInfo/Orbit"]
        atom_index = band["/BandInfo/Spin1/ProjectBand/AtomIndex"][0]
        orb_index = band["/BandInfo/Spin1/ProjectBand/OrbitIndexs"][0]

        if band["/BandInfo/SpinType"] == "collinear":
            for ai in range(atom_index):
                for oi in range(orb_index):
                    data.update(
                        {
                            f"{ai + 1}{orbitals[oi]}-up": band[
                                f"/BandInfo/Spin1/ProjectBand/{ai + 1}/{oi + 1}"
                            ]
                        }
                    )
                    data.update(
                        {
                            f"{ai + 1}{orbitals[oi]}-down": band[
                                f"/BandInfo/Spin2/ProjectBand/{ai + 1}/{oi + 1}"
                            ]
                        }
                    )
        else:
            for ai in range(atom_index):
                for oi in range(orb_index):
                    data.update(
                        {
                            f"{ai + 1}{orbitals[oi]}": band[
                                f"/BandInfo/Spin1/ProjectBand/1/{ai + 1}/{oi + 1}"
                            ]
                        }
                    )

        elements = band["/AtomInfo/Elements"]
        # elements: list[str] = [atom["Element"] for atom in band["/AtomInfo/Elements"]]
        _data = _refactor_data(data, nkpt, nband, elements, mode)

        return pl.DataFrame(_data)

    def _read_pband_json(band, mode):
        kc: list[float] = band["BandInfo"]["CoordinatesOfKPoints"]
        nkpt: int = band["BandInfo"]["NumberOfKpoints"]
        nband: int = band["BandInfo"]["NumberOfBand"]
        kcoord = np.array(kc).reshape(3, nkpt)
        kx = kcoord[0, :]
        ky = kcoord[1, :]
        kz = kcoord[2, :]
        data = {
            "kx": kx,
            "ky": ky,
            "kz": kz,
        }
        orbitals: list[str] = band["BandInfo"]["Orbit"]
        if band["BandInfo"]["SpinType"] == "collinear":
            project = band["BandInfo"]["Spin1"]["ProjectBand"]
            for p in project:
                atom_index = p["AtomIndex"]
                orb_index = p["OrbitIndex"] - 1
                contrib = p["Contribution"]
                data.update({f"{atom_index}{orbitals[orb_index]}-up": contrib})
            project = band["BandInfo"]["Spin2"]["ProjectBand"]
            for p in project:
                atom_index = p["AtomIndex"]
                orb_index = p["OrbitIndex"] - 1
                contrib = p["Contribution"]
                data.update({f"{atom_index}{orbitals[orb_index]}-down": contrib})
        else:
            project = band["BandInfo"]["Spin1"]["ProjectBand"]
            for p in project:
                atom_index = p["AtomIndex"]
                orb_index = p["OrbitIndex"] - 1
                contrib = p["Contribution"]
                data.update({f"{atom_index}{orbitals[orb_index]}": contrib})

        elements: list[str] = [atom["Element"] for atom in band["AtomInfo"]["Atoms"]]
        _data = _refactor_data(data, nkpt, nband, elements, mode)

        return pl.DataFrame(_data)

    def _refactor_data(data, nkpt, nband, elements, mode):
        _data = {}
        if mode == 1:  # ele
            for k, v in data.items():
                if k.startswith("k"):
                    _data[k] = v
                else:
                    cont = np.asarray(v).reshape(nband, nkpt)
                    ao = k.split("-")[0]
                    a, _ = _split_atomIndex_orbital(ao)
                    e = elements[a - 1]
                    for b in range(nband):
                        key = f"{b + 1}-{e}"
                        if key in _data:
                            _data[key] += np.asarray(cont[b])
                        else:
                            _data[key] = np.asarray(cont[b])
        elif mode == 2:  # ele+spdf
            for k, v in data.items():
                if k.startswith("k"):
                    _data[k] = v
                else:
                    cont = np.asarray(v).reshape(nband, nkpt)
                    ao = k.split("-")[0]
                    a, o = _split_atomIndex_orbital(ao)
                    o_1st = o[0]
                    e = elements[a - 1]
                    for b in range(nband):
                        key = f"{b + 1}-{e}-{o_1st}"
                        if key in _data:
                            _data[key] += np.asarray(cont[b])
                        else:
                            _data[key] = np.asarray(cont[b])
        elif mode == 3:  # ele+pxpy
            for k, v in data.items():
                if k.startswith("k"):
                    _data[k] = v
                else:
                    cont = np.asarray(v).reshape(nband, nkpt)
                    ao = k.split("-")[0]
                    a, o = _split_atomIndex_orbital(ao)
                    e = elements[a - 1]
                    for b in range(nband):
                        key = f"{b + 1}-{e}-{o}"
                        _data[key] = np.asarray(cont[b])
        elif mode == 4:  # atom+spdf
            for k, v in data.items():
                if k.startswith("k"):
                    _data[k] = v
                else:
                    cont = np.asarray(v).reshape(nband, nkpt)
                    ao = k.split("-")[0]
                    a, o = _split_atomIndex_orbital(ao)
                    o_1st = o[0]

                    for b in range(nband):
                        key = f"{b + 1}-{a}-{o_1st}"
                        if key in _data:
                            _data[key] += np.asarray(cont[b])
                        else:
                            _data[key] = np.asarray(cont[b])
        elif mode == 5:  # atom+spxpy...
            for k, v in data.items():
                if k.startswith("k"):
                    _data[k] = v
                else:
                    cont = np.asarray(v).reshape(nband, nkpt)
                    ao = k.split("-")[0]
                    a, o = _split_atomIndex_orbital(ao)
                    for b in range(nband):
                        _data[f"{b + 1}-{a}-{o}"] = np.asarray(cont[b])
        else:
            print(f"{mode=} not supported yet")
            exit(1)

        return _data

    if absfile.endswith(".h5"):
        band = load_h5(absfile)
        efermi = band["/BandInfo/EFermi"][0]
        print(f"{efermi=} eV")
        if not band["/BandInfo/IsProject"][0]:
            df = _read_tband_h5(band)
        else:
            df = _read_pband_h5(band, mode)

    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            band = load(fin)
        if not band["BandInfo"]["IsProject"]:
            df = _read_tband_json(band)
        else:
            df = _read_pband_json(band, mode)

    else:
        raise TypeError(f"{absfile} must be h5 or json file!")

    df = _format_float_columns_as_str_mapelements(df, fmt)

    if hide_index:
        return df
    else:
        return df.with_row_index(name="index", offset=1)


def _format_float_columns_as_str_mapelements(
    df: pl.DataFrame, fmt: str
) -> pl.DataFrame:
    if not isinstance(fmt, str):
        print(f"Warning: Format '{fmt}' is not a string. Skipping formatting.")
        return df

    try:
        return df.with_columns(
            pl.col(pl.Float64).map_elements(
                lambda x: f"{x:{fmt}}", return_dtype=pl.String
            )
        )
    except ValueError as e:
        print(
            f"Error applying format '{fmt}': {e}. This likely means the format string is invalid for a float value. Skipping formatting."
        )
        return df
    except Exception as e:
        print(f"An unexpected error occurred: {e}. Skipping formatting.")
        return df


def _split_atomIndex_orbital(s: str) -> tuple[int, str]:
    first_letter_index = -1
    for i, char in enumerate(s):
        if not char.isdigit():
            first_letter_index = i
            break

    if (
        first_letter_index == -1
    ):  # No letters found, assume the whole string is the atomIndex
        return int(s), ""
    else:
        atom_index_str = s[:first_letter_index]
        orbital_str = s[first_letter_index:]
        return int(atom_index_str), orbital_str
