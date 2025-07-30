"""Parse DS-PAW.log from relax task.

1. generate relaxing.xyz (extxyz format) showing the configurations during relaxation.
2. generate min_force.as showing the configuration with minimal force.
    2.1 convert `as` to `extxyz` format and `cif` format for checking
3. collect max force and energy for each relaxation ionic step and print them as table
    3.1 save to csv file

Note that turn on vdw will make DS-PAW.log content format changed, thus we need two separate functions.
- without vdw, DS-PAW.log content looks like the following:
...
## STRUCTURE  ##
Lattice vectors (Angstrom)
  0.000000   2.750000   2.750000
  2.750000   0.000000   2.750000
  2.750000   2.750000   0.000000
CoordinateType                   = Direct
Atom position:
Si   0.885000   0.875000   0.875000
...

## KPOINTS ##
Reduced kpoints size             = 282
Kpoints reciprocal coordinates and weight:
  0.000000  0.000000  0.000000  1.000000
  0.100000 -0.000000  0.000000  2.000000
  0.200000  0.000000  0.000000  2.000000
...
  0.500000  0.500000  0.500000  1.000000

## PARAMETERS ##
task = relax
...

## INITIALIZATION ##
Load structure from "structure.as" successfully!
------------------------------------------------------------
LOOP 1:
------------------------------------------------------------
#  iter |      Etot(eV)       dE(eV)         time
#   1   |    -186.196437  -1.861964e+02     0.151 s
#   2   |    -210.417628  -2.422119e+01     0.134 s
...
#  17   |    -216.967842  -1.796438e-05     0.173 s

------------------------------------------------------------
## STRUCTURE ##
Lattice vectors (Angstrom)
  0.000000   2.750000   2.750000
  2.750000   0.000000   2.750000
  2.750000   2.750000   0.000000
CoordinateType                   = Direct
Atom Position and force:
Si   0.885000   0.875000   0.875000  -0.024045  -0.345558  -0.345558
...

------------------------------------------------------------
Total force(eV/Angstrom):    0.001701   0.000124   0.000125
Max force:    0.489284 eV/Angstrom at atom index: 1
------------------------------------------------------------
Calculating force and stress:          0.155 s
Total calculation time      :          2.986 s

------------------------------------------------------------
## RELAX ##
Pressure              P  =            -0.38 kbar
Volume                V  =            41.59 Ang**3
------------------------------------------------------------
LOOP 2:
------------------------------------------------------------
#  iter |      Etot(eV)       dE(eV)         time
#   1   |    -216.976553  -8.728839e-03     0.205 s
...
#   3   |    -216.976886  -2.038071e-05     0.185 s

------------------------------------------------------------
## STRUCTURE ##
Lattice vectors (Angstrom)
  0.000000   2.750000   2.750000
  2.750000   0.000000   2.750000
  2.750000   2.750000   0.000000
CoordinateType                   = Direct
Atom Position and force:
Si   0.879149   0.874789   0.874789   0.028458   0.074841   0.074841
...

------------------------------------------------------------
Total force(eV/Angstrom):   -0.000703   0.000766   0.000766
Max force:    0.109600 eV/Angstrom at atom index: 1
------------------------------------------------------------
Calculating force and stress:          0.154 s
Total calculation time      :          0.789 s

------------------------------------------------------------
## RELAX ##
Pressure              P  =            -0.39 kbar
Volume                V  =            41.59 Ang**3
------------------------------------------------------------
...(Other Loops)
Convergence criteria (relax.convergence) reached on loop 3.
Total relaxation time       :           4.315 s
...(some tail info)


- with vdw, content looks like:
...(header is same as above)
## INITIALIZATION ##
Load structure from "structure.as" successfully!
------------------------------------------------------------
LOOP 1:
------------------------------------------------------------
#  iter |      Etot(eV)       dE(eV)         time
#   1   |    -512.851127  -5.128511e+02     1.000 s
...
#  11   |    -625.480265  -4.310149e-06     0.423 s

## VDW CORRECTION ##
Functional       :       pbe
Damping function paremeters:
rs6 =   1.000000
s18 =   0.722000
Correction Energy:        -0.306427 eV
Total Energy     :       -625.786692 eV
------------------------------------------------------------
## STRUCTURE ##
Lattice vectors (Angstrom)
  2.463267   0.000000  -0.000000
 -1.231633   2.133252   0.000000
  0.000000   0.000000   7.766420
CoordinateType                   = Direct
Atom Position and force:
 C   0.000000   0.000000   0.250000   0.000000   0.000000  -0.000000
...

------------------------------------------------------------
Total force(eV/Angstrom):   -0.000126   0.000148  -0.000000
Max force:    0.000000 eV/Angstrom at atom index: 4
------------------------------------------------------------
Calculating force and stress:          0.629 s
Total calculation time      :          6.812 s

------------------------------------------------------------
## RELAX ##
Pressure              P  =            -0.22 kbar
Volume                V  =            40.81 Ang**3
------------------------------------------------------------
LOOP 2:
------------------------------------------------------------
#  iter |      Etot(eV)       dE(eV)         time
#   1   |    -625.482228  -1.967494e-03     0.449 s
...
#   4   |    -625.479282  -6.023662e-06     0.448 s

## VDW CORRECTION ##
Functional       :       pbe
Damping function paremeters:
rs6 =   1.000000
s18 =   0.722000
Correction Energy:        -0.308962 eV
Total Energy     :       -625.788244 eV
------------------------------------------------------------
## STRUCTURE ##
Lattice vectors (Angstrom)
  2.458111   0.000000  -0.000000
 -1.229056   2.128787   0.000000
  0.000000   0.000000   7.719465
CoordinateType                   = Direct
Atom Position and force:
 C   0.000000   0.000000   0.250000   0.000000   0.000000   0.000000
。。。

------------------------------------------------------------
Total force(eV/Angstrom):   -0.000125   0.000147  -0.000000
Max force:    0.000000 eV/Angstrom at atom index: 4
------------------------------------------------------------
Calculating force and stress:          0.463 s
Total calculation time      :          2.342 s

------------------------------------------------------------
## RELAX ##
Pressure              P  =             0.08 kbar
Volume                V  =            40.39 Ang**3
------------------------------------------------------------
...(Other Loops)
Convergence criteria (relax.convergence) reached on loop 13.
Total relaxation time       :          40.346 s
...(some tail info)
"""


def _get_last_relax_blocks(logfile: str) -> list[str]:
    """Return all lines of the last relax (starting from the last LOOP 1:)"""
    with open(logfile, encoding="utf-8") as f:
        lines = f.readlines()
    # Use simple string matching, avoid regular expressions
    loop1_idx = []
    for i in range(len(lines) - 1):
        if lines[i].strip("- \n") == "" and lines[i + 1].strip().startswith("LOOP 1:"):
            loop1_idx.append(i)
    if not loop1_idx:
        raise RuntimeError("No LOOP 1 found in log")
    start = loop1_idx[-1]
    return lines[start:]


def _split_loops(lines: list[str]) -> list[list[str]]:
    """Split by LOOP"""
    loop_starts = []
    for i in range(len(lines) - 1):
        if lines[i].strip("- \n") == "" and lines[i + 1].strip().startswith("LOOP"):
            loop_starts.append(i)
    blocks = []
    for idx, s in enumerate(loop_starts):
        e = loop_starts[idx + 1] if idx + 1 < len(loop_starts) else len(lines)
        blocks.append(lines[s:e])
    return blocks


def _parse_structure_block(block: list[str]):
    """Parse the structure block and return a list of elements, fractional coordinates, forces, and lattice"""
    # Find lattice vectors
    lat_idx = None
    for i, line in enumerate(block):
        if "Lattice vectors" in line:
            lat_idx = i
            break
    if lat_idx is None:
        return None, None, None, None
    lattice = []
    for j in range(1, 4):
        lattice.append([float(x) for x in block[lat_idx + j].split()])
    # Find Atom Position and force:
    atom_start = None
    for idx in range(lat_idx + 4, len(block)):
        if "Atom Position and force" in block[idx]:
            atom_start = idx + 1
            break
    if atom_start is None:
        return None, None, None, None
    atoms: list[str] = []
    coords: list[list[float]] = []
    forces: list[list[float]] = []
    for line in block[atom_start:]:
        if not line.strip() or line.startswith("-"):
            break
        parts = line.split()
        atoms.append(parts[0])
        coords.append([float(x) for x in parts[1:4]])
        forces.append([float(x) for x in parts[4:7]])
    return atoms, coords, forces, lattice


def _parse_energy_block(block: list[str], vdw: bool = False):
    """Parse energy, take Total Energy in vdw mode, otherwise take Etot of the last iteration"""
    if vdw:
        # Find "Total Energy" in reverse order
        for line in reversed(block):
            if "Total Energy" in line:
                try:
                    return float(line.split(":")[-1].split()[0])
                except Exception:
                    continue
    else:
        # Find the last line starting with # that contains 'iter'
        etot = None
        for line in block:
            if line.strip().startswith("#") and "|" in line:
                parts = line.split("|")
                if len(parts) > 1:
                    try:
                        etot = float(parts[1].strip().split()[0])
                    except Exception:
                        continue
        return etot
    return None


def _parse_max_force_block(block: list[str]):
    """Parsing Max force"""
    for line in block:
        if line.strip().startswith("Max force:"):
            try:
                return float(line.split()[2])
            except Exception:
                continue
    return None


def _infer_selective_dynamics(
    forces: list[list[float]], tol: float = 1e-8
) -> list[list[str]]:
    """Determine the degrees of freedom for each atom based on forces (0 for T, non-zero for F)"""
    sd = []
    for f in forces:
        sd.append([("T" if abs(x) < tol else "F") for x in f])
    return sd


def get_relaxing_xyz(logfile: str = "DS-PAW.log"):
    """Generate relaxing.xyz (extxyz format), record the structure at each step"""
    from dspawpy.io.write import _write_xyz_traj

    lines = _get_last_relax_blocks(logfile)
    loops = _split_loops(lines)
    structures = []
    for loop in loops:
        atoms, coords, forces, lattice = _parse_structure_block(loop)
        if atoms is None or lattice is None or coords is None or forces is None:
            continue
        from pymatgen.core import Lattice, Structure

        struct = Structure(
            Lattice(lattice),
            atoms,
            coords,
            coords_are_cartesian=False,
        )
        structures.append(struct)
    if structures:
        _write_xyz_traj(structures, xyzfile="relaxing.xyz")
        print("==> relaxing.xyz")
    else:
        print("No structure found.")


def get_min_structure(logfile: str = "DS-PAW.log"):
    """Generate min_force.as, the structure corresponding to the minimum max force, retaining degree of freedom information"""
    lines = _get_last_relax_blocks(logfile)
    loops = _split_loops(lines)
    minf = float("inf")
    minidx = -1
    max_forces = []
    for i, loop in enumerate(loops):
        f = _parse_max_force_block(loop)
        max_forces.append(f)
        if f is not None and f < minf:
            minf = f
            minidx = i
    if minidx == -1:
        print("No force found.")
        return
    atoms, coords, forces, lattice = _parse_structure_block(loops[minidx])
    if atoms is None or lattice is None or coords is None or forces is None:
        print("Can't determine min_force structure")
        exit(1)
    from pymatgen.core import Lattice, Structure

    struct = Structure(
        Lattice(lattice),
        atoms,
        coords,
        coords_are_cartesian=False,
    )
    # Write AS file with degrees of freedom and header
    sd = _infer_selective_dynamics(forces)
    with open("min_force.as", "w") as f:
        f.write("Total number of atoms\n")
        f.write(f"{len(atoms)}\n")
        f.write("Lattice\n")
        for v in lattice:
            f.write("  " + "  ".join(f"{x:.8f}" for x in v) + "\n")
        f.write("Direct Fix\n")
        for i in range(len(atoms)):
            f.write(
                f"{atoms[i]}  "
                + "  ".join(f"{x:.16f}" for x in coords[i])
                + "    "
                + "  ".join(sd[i])
                + "\n"
            )
    print("==> min_force.as")
    # Optional: convert to extxyz/cif
    from dspawpy.io.write import _write_xyz_traj

    _write_xyz_traj([struct], xyzfile="min_force.xyz")
    try:
        from pymatgen.io.cif import CifWriter

        CifWriter(struct).write_file("min_force.cif")
    except Exception:
        pass


def get_max_forces(logfile: str = "DS-PAW.log"):
    """Output the maximum force for each step"""
    lines = _get_last_relax_blocks(logfile)
    loops = _split_loops(lines)
    max_forces = []
    for loop in loops:
        f = _parse_max_force_block(loop)
        max_forces.append(f)

    return max_forces


def get_energies(logfile: str = "DS-PAW.log"):
    """Output the energy at each step"""
    lines = _get_last_relax_blocks(logfile)
    loops = _split_loops(lines)
    energies = []
    for loop in loops:
        e = _parse_energy_block(loop, vdw=False)
        energies.append(e)

    return energies


def get_max_forces_and_energies(logfile: str = "DS-PAW.log", relative: bool = False):
    """Output the maximum forces and energies for each step and save them as a CSV file"""
    max_forces = get_max_forces(logfile)
    energies = get_energies(logfile)
    if relative:
        max_forces = [f - max_forces[0] for f in max_forces]
        energies = [e - energies[0] for e in energies]
    import polars as pl

    df = pl.DataFrame(
        data={
            "step": list(range(len(max_forces))),
            "force (eV/Angstrom)": max_forces,
            "energy (eV)": energies,
        }
    )
    print(df)
    df.write_csv("relax_summary.csv")
    print("==> relax_summary.csv")


# Implementation for VDW mode
def get_relaxing_xyz_vdw(logfile: str = "DS-PAW.log"):
    lines = _get_last_relax_blocks(logfile)
    loops = _split_loops(lines)
    structures = []
    for loop in loops:
        atoms, coords, forces, lattice = _parse_structure_block(loop)
        if atoms is None or lattice is None or coords is None or forces is None:
            continue
        from pymatgen.core import Lattice, Structure

        struct = Structure(
            Lattice(lattice),
            atoms,
            coords,
            coords_are_cartesian=False,
        )
        struct.add_site_property("forces", forces)
        structures.append(struct)
    if structures:
        from dspawpy.io.write import _write_xyz_traj

        _write_xyz_traj(structures, xyzfile="relaxing_vdw.xyz")
        print("==> relaxing_vdw.xyz")
    else:
        print("No structure found.")


def get_min_structure_vdw(logfile: str = "DS-PAW.log"):
    """Generate min_force_vdw.as in vdw mode, preserving the degree of freedom information"""
    lines = _get_last_relax_blocks(logfile)
    loops = _split_loops(lines)
    minf = float("inf")
    minidx = -1
    for i, loop in enumerate(loops):
        f = _parse_max_force_block(loop)
        if f is not None and f < minf:
            minf = f
            minidx = i
    if minidx == -1:
        print("No force found.")
        return
    atoms, coords, forces, lattice = _parse_structure_block(loops[minidx])
    if atoms is None or lattice is None or coords is None or forces is None:
        print("Can't determine min_force structure")
        exit(1)
    from pymatgen.core import Lattice, Structure

    struct = Structure(
        Lattice(lattice),
        atoms,
        coords,
        coords_are_cartesian=False,
    )
    sd = _infer_selective_dynamics(forces)
    with open("min_force_vdw.as", "w") as f:
        f.write("Total number of atoms\n")
        f.write(f"{len(atoms)}\n")
        f.write("Lattice\n")
        for v in lattice:
            f.write("  " + "  ".join(f"{x:.8f}" for x in v) + "\n")
        f.write("Direct Fix\n")
        for i in range(len(atoms)):
            f.write(
                f"{atoms[i]}  "
                + "  ".join(f"{x:.16f}" for x in coords[i])
                + "    "
                + "  ".join(sd[i])
                + "\n"
            )
    from dspawpy.io.write import _write_xyz_traj

    _write_xyz_traj([struct], xyzfile="min_force_vdw.xyz")
    try:
        from pymatgen.io.cif import CifWriter

        CifWriter(struct).write_file("min_force_vdw.cif")
    except Exception:
        pass
    print("==> min_force_vdw.as")


def get_max_forces_vdw(logfile: str = "DS-PAW.log"):
    lines = _get_last_relax_blocks(logfile)
    loops = _split_loops(lines)
    max_forces = []
    for loop in loops:
        f = _parse_max_force_block(loop)
        max_forces.append(f)

    return max_forces


def get_energies_vdw(logfile: str = "DS-PAW.log"):
    lines = _get_last_relax_blocks(logfile)
    loops = _split_loops(lines)
    energies = []
    for loop in loops:
        e = _parse_energy_block(loop, vdw=True)
        energies.append(e)

    return energies


def get_max_forces_and_energies_vdw(
    logfile: str = "DS-PAW.log", relative: bool = False
):
    max_forces = get_max_forces_vdw(logfile)
    energies = get_energies_vdw(logfile)

    if relative:
        max_forces = [f - max_forces[0] for f in max_forces]
        energies = [e - energies[0] for e in energies]

    import polars as pl

    df = pl.DataFrame(
        data={
            "step": list(range(len(max_forces))),
            "force (eV/Angstrom)": max_forces,
            "energy (eV)": energies,
        }
    )
    print(df)
    df.write_csv("relax_summary_vdw.csv")

    print("==> relax_summary_vdw.csv")


def read_relax_data(
    logfile: str = "DS-PAW.log",
    print_efs: bool = True,
    relative: bool = False,
    write_traj: bool = True,
    write_as: bool = True,
):
    """Read relax data from log file, not h5/json, because they lack data.

    Call this function will print info to screen directly.

    Parameters
    ----------
    logfile:
        location of "DS-PAW.log", such as '../another/DS-PAW.log'.
    print_efs:
        whether to print energies and forces table.
    relative:
        whether to print energies and forces relative to the first step value.
    write_traj:
        whether to write traj xyz file
    write_as:
        whether to write structure.as file corresponding to the minimal force.

    Examples
    --------
    >>> from dspawpy.analysis.post_relax import read_relax_data
    >>> read_relax_data(logfile='dspawpy_proj/dspawpy_tests/inputs/2.1/DS-PAW.log') # doctest: +ELLIPSIS
    ==> ...relaxing.xyz...
    ==> relaxing.xyz
    ==> min_force.as
    ==> ...min_force.xyz...
    shape: (3, 3)
    ┌──────┬─────────────────────┬─────────────┐
    │ step ┆ force (eV/Angstrom) ┆ energy (eV) │
    ╞══════╪═════════════════════╪═════════════╡
    │ 0    ┆ 0.489284            ┆ -216.967842 │
    │ 1    ┆ 0.1096              ┆ -216.976886 │
    │ 2    ┆ 0.024697            ┆ -216.977327 │
    └──────┴─────────────────────┴─────────────┘
    ==> relax_summary.csv

    >>> read_relax_data(logfile='dspawpy_proj/dspawpy_tests/inputs/2.1/DS-PAW.log', relative=True, write_traj=False, write_as=False)
    shape: (3, 3)
    ┌──────┬─────────────────────┬─────────────┐
    │ step ┆ force (eV/Angstrom) ┆ energy (eV) │
    ╞══════╪═════════════════════╪═════════════╡
    │ 0    ┆ 0.0                 ┆ 0.0         │
    │ 1    ┆ -0.379684           ┆ -0.009044   │
    │ 2    ┆ -0.464587           ┆ -0.009485   │
    └──────┴─────────────────────┴─────────────┘
    ==> relax_summary.csv
    """
    with open(logfile, encoding="utf-8") as f:
        if "## VDW CORRECTION ##" in f.read():
            if write_traj:
                get_relaxing_xyz_vdw(logfile)
            if write_as:
                get_min_structure_vdw(logfile)
            if print_efs:
                get_max_forces_and_energies_vdw(logfile, relative)

        else:
            if write_traj:
                get_relaxing_xyz(logfile)
            if write_as:
                get_min_structure(logfile)
            if print_efs:
                get_max_forces_and_energies(logfile, relative)
