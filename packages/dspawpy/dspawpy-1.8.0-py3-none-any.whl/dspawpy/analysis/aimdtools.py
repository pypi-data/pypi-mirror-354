from typing import TYPE_CHECKING, List, Optional, Sequence, Union

from loguru import logger

if TYPE_CHECKING:
    from pymatgen.core.structure import Structure


class MSD:
    # A class used for calculating mean squared displacement, adapted from the pymatgen open-source project

    def __init__(
        self,
        structures: List["Structure"],
        select: Union[str, List[str], List[int], int] = "all",
        msd_type="xyz",
    ):
        self.structures = structures
        self.msd_type = msd_type

        self.n_frames = len(structures)
        self.lattice = structures[0].lattice

        self._parse_msd_type()

        import numpy as np

        if select == "all":
            self.n_particles = len(structures[0])
            self._position_array = np.zeros(
                (self.n_frames, self.n_particles, self.dim_fac),
            )
            for i, s in enumerate(self.structures):
                self._position_array[i, :, :] = s.frac_coords[:, self._dim]
        elif isinstance(select, str):  # ':', '-3:', 'H' or even 'H1'
            if ":" in select:
                exec(
                    f"self.n_particles = self.structures[0].frac_coords[{select}][:, self._dim].shape[0]",
                )
                self._position_array = np.zeros(
                    (self.n_frames, self.n_particles, self.dim_fac),
                )
                for i, s in enumerate(self.structures):
                    exec(
                        f"self._position_array[i, :, :] = s.frac_coords[{select}][:, self._dim]",
                    )
            else:
                indices = [
                    j
                    for j, s in enumerate(self.structures[0])
                    if select == s.species_string
                ]
                assert indices != [], (
                    f"{select} did not match any element symbol, {self.structures[0].species}"
                )
                self.n_particles = (
                    self.structures[0].frac_coords[indices, :][:, self._dim].shape[0]
                )
                self._position_array = np.zeros(
                    (self.n_frames, self.n_particles, self.dim_fac),
                )
                for i, s in enumerate(self.structures):
                    self._position_array[i, :, :] = s.frac_coords[indices, :][
                        :,
                        self._dim,
                    ]
        else:
            if isinstance(select, int):  # 1
                indices = [select]
            elif isinstance(select, (list, np.ndarray)):  # [1,2,3] or ['H','O']
                # if all elements are int, then select by index
                if all(isinstance(i, int) for i in select):
                    indices = select
                # if all elements are str, then select by element
                elif all(isinstance(i, str) for i in select):
                    indices = []
                    for sel in select:
                        indices += [
                            j
                            for j, s in enumerate(self.structures[0])
                            if sel == s.species_string
                        ]
                else:
                    raise ValueError(select)
            else:
                raise ValueError(
                    f"select = {select} should be string, int, list or np.ndarray",
                )
            # get shape of returned array
            self.n_particles = (
                self.structures[0].frac_coords[indices][:, self._dim].shape[0]
            )
            self._position_array = np.zeros(
                (self.n_frames, self.n_particles, self.dim_fac),
            )
            for i, s in enumerate(self.structures):
                self._position_array[i, :, :] = s.frac_coords[indices][:, self._dim]

    def _parse_msd_type(self):
        r"""Sets up the desired dimensionality of the MSD."""
        keys = {
            "x": [0],
            "y": [1],
            "z": [2],
            "xy": [0, 1],
            "xz": [0, 2],
            "yz": [1, 2],
            "xyz": [0, 1, 2],
        }

        self.msd_type = self.msd_type.lower()

        try:
            self._dim = keys[self.msd_type]
        except KeyError:
            raise ValueError(
                f"invalid msd_type: {self.msd_type} specified, please specify one of xyz, "
                "xy, xz, yz, x, y, z",
            )

        self.dim_fac = len(self._dim)

    def run(self):
        print("Calculating MSD...")
        import numpy as np

        result = np.zeros((self.n_frames, self.n_particles))

        rd = np.zeros((self.n_frames, self.n_particles, self.dim_fac))
        for i in range(1, self.n_frames):
            disp = self._position_array[i, :, :] - self._position_array[i - 1, :, :]
            # mic by periodic boundary condition
            disp[np.abs(disp) > 0.5] = disp[np.abs(disp) > 0.5] - np.sign(
                disp[np.abs(disp) > 0.5],
            )
            disp = np.dot(disp, self.lattice.matrix)
            rd[i, :, :] = disp
        rd = np.cumsum(rd, axis=0)
        for n in range(1, self.n_frames):
            disp = rd[n:, :, :] - rd[:-n, :, :]  # [n:-n] window
            sqdist = np.square(disp).sum(axis=-1)
            result[n, :] = sqdist.mean(axis=0)

        return result.mean(axis=1)


class RDF:
    # A class for quickly calculating radial distribution functions
    # Copyright (c) Materials Virtual Lab.
    # Distributed under the terms of the BSD License.

    def __init__(
        self,
        structures: List["Structure"],
        rmin: float = 0.0,
        rmax: float = 10.0,
        ngrid: int = 101,
        sigma: float = 0.0,
    ):
        """This method calculates rdf on `np.linspace(rmin, rmax, ngrid)` points

        Parameters
        ----------
        structures (list of pymatgen Structures): structures to compute RDF
        rmin (float): minimal radius
        rmax (float): maximal radius
        ngrid (int): number of grid points, defaults to 101
        sigma (float): smooth parameter

        """
        from pymatgen.core import Structure

        if isinstance(structures, Structure):
            structures = [structures]
        self.structures = structures
        # Number of atoms in all structures should be the same
        assert len({len(i) for i in self.structures}) == 1, (
            "Different configurations have different numbers of atoms!"
        )
        elements = [[i.specie for i in j.sites] for j in self.structures]
        unique_elements_on_sites = [len(set(i)) == 1 for i in list(zip(*elements))]

        # For the same site index, all structures should have the same element there
        if not all(unique_elements_on_sites):
            raise RuntimeError("Elements are not the same at least for one site")

        self.rmin = rmin
        self.rmax = rmax
        self.ngrid = ngrid

        self.dr = (self.rmax - self.rmin) / (self.ngrid - 1)  # end points are on grid
        import numpy as np

        self.r = np.linspace(self.rmin, self.rmax, self.ngrid)  # type: ignore
        self.shell_volumes = 4.0 * np.pi * self.r**2 * self.dr
        self.shell_volumes[self.shell_volumes < 1e-8] = 1e8  # avoid divide by zero

        self.n_structures = len(self.structures)
        self.sigma = np.ceil(sigma / self.dr)

        self.density = [{}] * len(self.structures)  # type: list[dict]

        self.natoms = [
            i.composition.to_data_dict["unit_cell_composition"] for i in self.structures
        ]

        for s_index, natoms in enumerate(self.natoms):
            for i, j in natoms.items():
                self.density[s_index][i] = j / self.structures[s_index].volume

    def _dist_to_counts(self, d):
        """Convert a distance array for counts in the bin

        Parameters
        ----------
            d: (1D np.array)

        Returns
        -------
            1D array of counts in the bins centered on self.r

        """
        import numpy as np

        counts = np.zeros((self.ngrid,))
        indices = np.asarray(
            np.floor((d - self.rmin + 0.5 * self.dr) / self.dr),
            dtype=int,
        )  # Convert the found distances to grid indices (floor)
        unique, val_counts = np.unique(indices, return_counts=True)
        counts[unique] = val_counts
        return counts

    def get_rdf(
        self,
        ref_species: Union[str, List[str]],
        species: Union[str, List[str]],
        is_average=True,
    ):
        """Wrapper to get the rdf for a given species pair

        Parameters
        ----------
        ref_species (list of species or just single specie str):
            The reference species. The rdfs are calculated with these species at the center
        species (list of species or just single specie str):
            the species that we are interested in. The rdfs are calculated on these species.
        is_average (bool):
            whether to take the average over all structures

        Returns
        -------
        (x, rdf)
            x is the radial points, and rdf is the rdf value.

        """
        print("Calculating RDF...")
        if isinstance(ref_species, str):
            ref_species = [ref_species]

        if isinstance(species, str):
            species = [species]
        ref_species_index = []
        species_index = []
        for i in range(len(self.structures[0].species)):
            ele = str(self.structures[0].species[i])
            if ele in ref_species:
                ref_species_index.append(i)
            if (
                ele in species
            ):  # @syyl use if instead of elif in case of `species = ref_species`
                species_index.append(i)
        all_rdfs = [
            self.get_one_rdf(ref_species_index, species_index, i)[1]
            for i in range(self.n_structures)
        ]
        if is_average:
            import numpy as np

            all_rdfs = np.mean(all_rdfs, axis=0)
        return self.r, all_rdfs

    def get_one_rdf(
        self,
        ref_species_index: Union[str, List[str]],
        species_index: Union[str, List[str]],
        index=0,
    ):
        """Get the RDF for one structure, indicated by the index of the structure
        in all structures
        """
        lattice = self.structures[index].lattice
        distances = []
        refsp_frac_coord = self.structures[index].frac_coords[ref_species_index]
        sp_frac_coord = self.structures[index].frac_coords[species_index]
        d = lattice.get_all_distances(refsp_frac_coord, sp_frac_coord)
        indices = (
            (d >= self.rmin - self.dr / 2.0)
            & (d <= self.rmax + self.dr / 2.0)
            & (d > 1e-8)
        )
        import numpy as np

        distances = d[indices]
        counts = self._dist_to_counts(
            np.asarray(distances),
        )  # Count the number of atoms of target elements within this distance, as a list

        npairs = len(distances)
        rdf_temp = counts / npairs / self.shell_volumes / self.structures[index].volume

        if self.sigma > 1e-8:
            from scipy.ndimage import gaussian_filter1d

            rdf_temp = gaussian_filter1d(rdf_temp, self.sigma)
        return self.r, rdf_temp, npairs

    def get_coordination_number(self, ref_species, species, is_average=True):
        """Returns running coordination number

        Parameters
        ----------
        ref_species (list of species or just single specie str):
            the reference species. The rdfs are calculated with these species at the center
        species (list of species or just single specie str):
            the species that we are interested in. The rdfs are calculated on these species.
        is_average (bool): whether to take structural average

        Returns
        -------
        numpy array

        Examples
        --------
        >>> from dspawpy.io.structure import read
        >>> strs = read('dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', task="aimd")
        >>> obj = RDF(structures=strs, rmin=0, rmax=10, ngrid=101, sigma=1e-6)
        >>> rs, cn=obj.get_coordination_number(ref_species='H', species='O')
        Calculating RDF...
        >>> cn
        array([0.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
               0.00000000e+00, 7.60849690e-09, 3.89029833e-07, 7.24472699e-06,
               5.58494695e-05, 2.05738270e-04, 4.18849264e-04, 5.54848883e-04,
               5.92167829e-04, 5.96643220e-04, 5.96890366e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04, 5.96895423e-04, 5.96895423e-04, 5.96895423e-04,
               5.96895423e-04])

        """
        # Note: The average density from all input structures is used here.
        all_rdf = self.get_rdf(ref_species, species, is_average=False)[1]
        if isinstance(species, str):
            species = [species]
        density = [sum(i[j] for j in species) for i in self.density]
        import numpy as np

        cn = [
            np.cumsum(rdf * density[i] * 4.0 * np.pi * self.r**2 * self.dr)
            for i, rdf in enumerate(all_rdf)
        ]
        if is_average:
            cn = np.mean(cn, axis=0)
        return self.r, cn


class RMSD:
    """A class for calculating the Root Mean Square Deviation (RMSD), adapted from the pymatgen open-source project."""

    def __init__(self, structures: List["Structure"]):
        self.structures = structures

        self.n_frames = len(self.structures)
        self.n_particles = len(self.structures[0])
        self.lattice = self.structures[0].lattice

        import numpy as np

        self._position_array = np.zeros((self.n_frames, self.n_particles, 3))

        for i, s in enumerate(self.structures):
            self._position_array[i, :, :] = s.frac_coords

    def run(self, base_index=0):
        print("Calculating RMSD...")
        import numpy as np

        result = np.zeros(self.n_frames)
        rd = np.zeros((self.n_frames, self.n_particles, 3))
        for i in range(1, self.n_frames):
            disp = self._position_array[i, :, :] - self._position_array[i - 1, :, :]
            # mic by periodic boundary condition
            disp[np.abs(disp) > 0.5] = disp[np.abs(disp) > 0.5] - np.sign(
                disp[np.abs(disp) > 0.5],
            )
            disp = np.dot(disp, self.lattice.matrix)
            rd[i, :, :] = disp
        rd = np.cumsum(rd, axis=0)

        for i in range(self.n_frames):
            sqdist = np.square(rd[i] - rd[base_index]).sum(axis=-1)
            result[i] = sqdist.mean()

        return np.sqrt(result)


def get_lagtime_msd(
    datafile: Union[str, List[str]],
    select: Union[str, List[int]] = "all",
    msd_type: str = "xyz",
    timestep: Optional[float] = None,
):
    r"""Calculate the mean squared displacement at different time steps

    Parameters
    ----------
    datafile:
        - Path to `aimd.h5` or `aimd.json` files, or a directory containing these files (prioritizes searching for `aimd.h5`)
        - Written as a list, the data will be read sequentially and merged together
        - For example ['aimd1.h5', 'aimd2.h5', '/data/home/my_aimd_task']
    select:
        Select atomic number or element; atomic numbers start from 0; default is 'all', which calculates all atoms
    msd_type:
        Calculate the type of MSD, options: xyz, xy, xz, yz, x, y, z, default is 'xyz', which calculates all components
    timestep:
        Time interval between adjacent structures, in units of fs, default None, will be read from datafile, if failed, set to 1.0fs;
        If not None, this value will be used to calculate the time series

    Returns
    -------
    lagtime : np.ndarray
        Time series
    result : np.ndarray
        Mean square displacement sequence

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_lagtime_msd
    >>> lagtime, msd = get_lagtime_msd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', timestep=0.1)
    Calculating MSD...
    >>> lagtime, msd = get_lagtime_msd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5')
    Calculating MSD...
    >>> lagtime
    array([0.000e+00, 1.000e+00, 2.000e+00, ..., 1.997e+03, 1.998e+03,
           1.999e+03])
    >>> msd
    array([0.00000000e+00, 3.75844096e-03, 1.45298732e-02, ...,
           7.98518472e+02, 7.99267490e+02, 7.99992702e+02])
    >>> lagtime, msd = get_lagtime_msd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', select='H')
    Calculating MSD...
    >>> lagtime, msd = get_lagtime_msd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', select=[0,1])
    Calculating MSD...
    >>> lagtime, msd = get_lagtime_msd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', select=['H','O'])
    Calculating MSD...
    >>> lagtime, msd = get_lagtime_msd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', select=0)
    Calculating MSD...

    """
    from dspawpy.io.structure import read

    strs = read(datafile, task="aimd")
    if timestep is None:
        if isinstance(datafile, str) or len(datafile) == 1:
            ts = _get_time_step(datafile)
        else:
            logger.warning(
                "For multiple datafiles, you must manually specify the timestep. It will default to 1.0fs.",
            )
            ts = 1.0
    else:
        ts = timestep

    msd = MSD(strs, select, msd_type)
    result = msd.run()

    nframes = msd.n_frames
    import numpy as np

    lagtime = np.arange(nframes) * ts  # make the lag-time axis

    return lagtime, result


def get_lagtime_rmsd(datafile: Union[str, List[str]], timestep: Optional[float] = None):
    r"""Parameters
    ----------
    datafile:
        - Path to `aimd.h5` or `aimd.json` files, or a directory containing these files (prioritizes searching for `aimd.h5`).
        - Written as a list, the data will be read sequentially and merged together
        - For example ['aimd1.h5', 'aimd2.h5', '/data/home/my_aimd_task']
    timestep:
        Time interval between adjacent structures, in fs, default None, will be read from datafile, set to 1.0fs if failed;
        If not None, it will be used to calculate the time series

    Returns
    -------
    lagtime : numpy.ndarray
        Time series
    rmsd : numpy.ndarray
        Root mean square deviation sequence

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_lagtime_rmsd
    >>> lagtime, rmsd = get_lagtime_rmsd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json')
    Calculating RMSD...
    >>> lagtime, rmsd = get_lagtime_rmsd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', timestep=0.1)
    Calculating RMSD...
    >>> lagtime
    array([0.000e+00, 1.000e-01, 2.000e-01, ..., 1.997e+02, 1.998e+02,
           1.999e+02])
    >>> rmsd
    array([ 0.        ,  0.05321816,  0.09771622, ..., 28.27847679,
           28.28130893, 28.28414224])

    """
    from dspawpy.io.structure import read

    strs = read(datafile, task="aimd")
    if timestep is None:
        if isinstance(datafile, str) or len(datafile) == 1:
            ts = _get_time_step(datafile)
        else:
            logger.warning(
                "For multiple datafiles, you must manually specify the timestep. It will default to 1.0fs.",
            )
            ts = 1.0
    else:
        ts = timestep

    rmsd = RMSD(structures=strs)
    result = rmsd.run()

    # Plot
    nframes = rmsd.n_frames
    import numpy as np

    lagtime = np.arange(nframes) * ts  # make the lag-time axis

    return lagtime, result


def get_rs_rdfs(
    datafile: Union[str, List[str]],
    ele1: str,
    ele2: str,
    rmin: float = 0,
    rmax: float = 10,
    ngrid: int = 101,
    sigma: float = 0,
):
    r"""Compute the radial distribution function (RDF).

    Parameters
    ----------
    datafile:
        - Path to `aimd.h5` or `aimd.json` files, or a directory containing these files (prioritizes searching for `aimd.h5`)
        - Written as a list, the data will be read sequentially and merged together
        - For example ['aimd1.h5', 'aimd2.h5', '/data/home/my_aimd_task']
    ele1:
        Central element
    ele2:
        Adjacent elements
    rmin:
        Radial distribution minimum value, default is 0
    rmax:
        Radial distribution maximum value, default is 10
    ngrid:
        Number of grid points in the radial distribution, default is 101
    sigma:
        Smoothing parameter

    Returns
    -------
    r : numpy.ndarray
        Grid points for the radial distribution
    rdf : numpy.ndarray
        Radial distribution function

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_rs_rdfs
    >>> rs, rdfs = get_rs_rdfs(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5',ele1='H',ele2='O', sigma=1e-6)
    Calculating RDF...
    >>> rs, rdfs = get_rs_rdfs(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5',ele1='H',ele2='O')
    Calculating RDF...
    >>> rdfs
    array([0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.00646866,
           0.01098199, 0.0004777 , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        ])

    """
    from dspawpy.io.structure import read

    strs = read(datafile, task="aimd")

    # Calculate RDF and plot the main curves
    obj = RDF(structures=strs, rmin=rmin, rmax=rmax, ngrid=ngrid, sigma=sigma)

    rs, rdfs = obj.get_rdf(ele1, ele2)
    return rs, rdfs


def plot_msd(
    lagtime,
    result,
    xlim: Optional[Sequence] = None,
    ylim: Optional[Sequence] = None,
    figname: Optional[str] = None,
    show: bool = True,
    ax=None,
    **kwargs,
):
    r"""Compute mean squared displacement (MSD) after the AIMD task is completed

    Parameters
    ----------
    lagtime : np.ndarray
        Time series
    result : np.ndarray
        Mean squared displacement sequence
    xlim:
        x-axis range, default None, set automatically
    ylim:
        y-axis range, default to None, automatically set
    figname:
        Image name, default to None, do not save the image
    show:
        Whether to display the image, default is True
    ax:
        Used to draw the image on a subplot in matplotlib
    **kwargs : dict
        Other parameters, such as line width, color, etc., are passed to plt.plot function

    Returns
    -------
    Image after MSD analysis

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_lagtime_msd, plot_msd

    Specify the location of the h5 file, use the get_lagtime_msd function to obtain data, and the select parameter selects the nth atom (not by element)

    >>> lagtime, msd = get_lagtime_msd('dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', select=[0]) # doctest: +ELLIPSIS
    Calculating MSD...

    Plot the data and save the figure

    >>> plot_msd(lagtime, msd, xlim=[0,800], ylim=[0,1000], figname='dspawpy_proj/dspawpy_tests/outputs/doctest/MSD.png', show=False) # doctest: +ELLIPSIS
    ==> ...MSD.png
    ...

    """
    import matplotlib.pyplot as plt

    if ax:
        ishow = False
        ax.plot(lagtime, result, c="black", ls="-", **kwargs)
    else:
        ishow = True
        fig, ax = plt.subplots()
        ax.plot(lagtime, result, c="black", ls="-", **kwargs)
        ax.set_xlabel("Time (fs)")
        ax.set_ylabel(r"MSD ($Å^2$)")

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    plt.tight_layout()
    if figname:
        import os

        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        print(f"==> {absfig}")
    if (
        show and ishow
    ):  # If showing subplots, should not display each subplot individually
        plt.show()  # show will automatically clear the image

    return ax


def plot_rdf(
    rs,
    rdfs,
    ele1: str,
    ele2: str,
    xlim: Optional[Sequence] = None,
    ylim: Optional[Sequence] = None,
    figname: Optional[str] = None,
    show: bool = True,
    ax=None,
    **kwargs,
):
    r"""Post-AIMD analysis of rdf and plotting.

    Parameters
    ----------
    rs : numpy.ndarray
        Radial distribution grid points
    rdfs : numpy.ndarray
        Radial distribution function
    ele1:
        Center element
    ele2:
        Adjacent elements
    xlim:
        x-axis range, default to None, i.e., set automatically
    ylim:
        y-axis range, default to None, i.e., automatically set
    figname:
        Image name, default to None, meaning no image is saved
    show:
        Whether to display the image, default to True
    ax: matplotlib.axes.Axes
        Axis for plotting, default is None, which means creating a new axis
    **kwargs : dict
        Other parameters, such as line width, color, etc., are passed to plt.plot function

    Returns
    -------
    Image after RDF analysis

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_rs_rdfs, plot_rdf

    First obtain the rs and rdfs data as the x and y axis data

    >>> rs, rdfs = get_rs_rdfs('dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', 'H', 'O', rmax=6)
    Calculating RDF...

    Passing x and y data to the plot_rdf function to plot

    >>> plot_rdf(rs, rdfs, 'H','O', xlim=[0, 6], ylim=[0, 0.015],figname='dspawpy_proj/dspawpy_tests/outputs/doctest/RDF.png', show=False) # doctest: +ELLIPSIS
    ==> ...RDF.png

    """
    import matplotlib.pyplot as plt

    if ax:
        ishow = False
        ax.plot(
            rs,
            rdfs,
            label=r"$g_{\alpha\beta}(r)$" + f"[{ele1},{ele2}]",
            **kwargs,
        )

    else:
        ishow = True
        fig, ax = plt.subplots()
        ax.plot(
            rs,
            rdfs,
            label=r"$g_{\alpha\beta}(r)$" + f"[{ele1},{ele2}]",
            **kwargs,
        )

        ax.set_xlabel(r"$r$" + "(Å)")
        ax.set_ylabel(r"$g(r)$")

    ax.legend()

    # Drawing details
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    plt.tight_layout()
    if figname:
        import os

        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        print(f"==> {absfig}")
    if (
        show and ishow
    ):  # When plotting subplots, each subplot should not be shown individually
        plt.show()  # show will automatically clear the figure


def plot_rmsd(
    lagtime,
    result,
    xlim: Optional[Sequence] = None,
    ylim: Optional[Sequence] = None,
    figname: Optional[str] = None,
    show: bool = True,
    ax=None,
    **kwargs,
):
    r"""Post-AIMD analysis of RMSD and plotting

    Parameters
    ----------
    lagtime:
        Time series
    result:
        Root mean square deviation sequence
    xlim:
        x-axis range
    ylim:
        y-axis range
    figname:
        Image save path
    show:
        Whether to display the image
    ax : matplotlib.axes._subplots.AxesSubplot
        If plotting subplots, pass the subplot object
    **kwargs : dict
        Parameters passed to plt.plot

    Returns
    -------
    Image of RMSD analysis of structures

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_lagtime_rmsd, plot_rmsd

    `timestep` represents the time step length

    >>> lagtime, rmsd = get_lagtime_rmsd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', timestep=0.1)
    Calculating RMSD...
    >>> lagtime, rmsd = get_lagtime_rmsd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', timestep=0.1)
    Calculating RMSD...

    Saving directly as RMSD.png image

    >>> plot_rmsd(lagtime, rmsd, xlim=[0,200], ylim=[0, 30],figname='dspawpy_proj/dspawpy_tests/outputs/doctest/RMSD.png', show=False) # doctest: +ELLIPSIS
    ==> ...RMSD.png
    ...

    """
    import matplotlib.pyplot as plt

    # Parameter initialization
    if ax:
        ishow = False
        ax.plot(lagtime, result, **kwargs)
    else:
        ishow = True
        fig, ax = plt.subplots()
        ax.plot(lagtime, result, **kwargs)
        ax.set_xlabel("Time (fs)")
        ax.set_ylabel("RMSD (Å)")

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    plt.tight_layout()
    if figname:
        import os

        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        print(f"==> {absfig}")
    if (
        show and ishow
    ):  # If subplots are drawn, each subplot should not be shown individually
        plt.show()  # show will automatically clear the figure

    return ax


def _get_time_step(datafile):
    import os

    absfile = os.path.abspath(datafile)
    if absfile.endswith(".h5"):
        hpath = os.path.abspath(absfile)
        import h5py
        import numpy as np

        hf = h5py.File(hpath)
        try:
            t = np.asarray(hf["/Structures/TimeStep"])[0]
            timestep = float(t)
        except Exception:
            print(str(Exception))
            timestep = 1.0
    elif absfile.endswith(".json"):
        jpath = os.path.abspath(absfile)
        with open(jpath) as f:
            import json

            jdata = json.load(f)
        try:
            t = jdata["Structures"][0]["TimeStep"]
            timestep = float(t)
        except Exception:
            print(str(Exception))
            timestep = 1.0
    else:
        raise ValueError(f"{absfile} must be .h5 or .json")

    return timestep
