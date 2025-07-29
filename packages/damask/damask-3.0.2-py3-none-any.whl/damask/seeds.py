# Copyright 2024-2025 Max-Planck-Institut für Nachhaltige Materialien GmbH
# Copyright 2011-2024 Max-Planck-Institut für Eisenforschung GmbH
# 
# DAMASK is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""Functionality for generation of seed points for Voronoi or Laguerre tessellation."""

from typing import Optional as _Optional, Tuple as _Tuple

from scipy import spatial as _spatial
import numpy as _np

from ._typehints import FloatSequence as _FloatSequence, IntSequence as _IntSequence, \
                        NumpyRngSeed as _NumpyRngSeed
from . import util as _util
from . import grid_filters as _grid_filters


def from_random(size: _FloatSequence,
                N_seeds: int,
                cells: _Optional[_IntSequence] = None,
                rng_seed: _Optional[_NumpyRngSeed] = None) -> _np.ndarray:
    """
    Place seeds randomly in space.

    Parameters
    ----------
    size : sequence of float, len (3)
        Edge lengths of the seeding domain.
    N_seeds : int
        Number of seeds.
    cells : sequence of int, len (3), optional.
        If given, ensures that each seed results in a grain when a standard Voronoi
        tessellation is performed using the given grid resolution (i.e. size/cells).
    rng_seed : {None, int, array_like[ints], SeedSequence, BitGenerator, Generator}, optional
        A seed to initialize the BitGenerator. Defaults to None.
        If None, then fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    coords : numpy.ndarray, shape (N_seeds,3)
        Seed coordinates in 3D space.

    """
    size_ = _np.array(size,float)
    rng = _np.random.default_rng(rng_seed)
    if cells is None:
        coords = rng.random((N_seeds,3)) * size_
    else:
        grid_coords = _grid_filters.coordinates0_point(cells,size).reshape(-1,3,order='F')
        coords = grid_coords[rng.choice(_np.prod(cells),N_seeds, replace=False)] \
               + _np.broadcast_to(size_/_np.array(cells,_np.int64),(N_seeds,3))*(rng.random((N_seeds,3))*.5-.25) # wobble w/o leaving grid

    return coords


def from_Poisson_disc(size: _FloatSequence,
                      N_seeds: int,
                      N_candidates: int,
                      distance: float,
                      periodic: bool = True,
                      rng_seed: _Optional[_NumpyRngSeed] = None) -> _np.ndarray:
    """
    Place seeds following a Poisson disc distribution.

    Parameters
    ----------
    size : sequence of float, len (3)
        Edge lengths of the seeding domain.
    N_seeds : int
        Number of seeds.
    N_candidates : int
        Number of candidates to consider for finding best candidate.
    distance : float
        Minimum acceptable distance to other seeds.
    periodic : bool, optional
        Calculate minimum distance for periodically repeated grid.
        Defaults to True.
    rng_seed : {None, int, array_like[ints], SeedSequence, BitGenerator, Generator}, optional
        A seed to initialize the BitGenerator. Defaults to None.
        If None, then fresh, unpredictable entropy will be pulled from the OS.

    Returns
    -------
    coords : numpy.ndarray, shape (N_seeds,3)
        Seed coordinates in 3D space.

    """
    rng = _np.random.default_rng(rng_seed)
    coords = _np.empty((N_seeds,3))
    coords[0] = rng.random(3) * _np.array(size,float)

    s = 1
    i = 0
    progress = _util.ProgressBar(N_seeds+1,'',50)
    while s < N_seeds:
        i += 1
        candidates = rng.random((N_candidates,3))*_np.broadcast_to(size,(N_candidates,3))
        tree = _spatial.cKDTree(coords[:s],boxsize=size) if periodic else \
               _spatial.cKDTree(coords[:s])
        distances = tree.query(candidates)[0]
        if distances.max() > distance:                                                              # require minimum separation
            i = 0
            coords[s] = candidates[distances.argmax()]                                              # maximum separation to existing point cloud
            s += 1
            progress.update(s)

        if i >= 100:
            raise ValueError('seeding not possible')

    return coords


def from_grid(grid,
              selection: _Optional[_IntSequence] = None,
              invert_selection: bool = False,
              average: bool = False,
              periodic: bool = True) -> _Tuple[_np.ndarray, _np.ndarray]:
    """
    Create seeds from grid description.

    Parameters
    ----------
    grid : damask.GeomGrid
        Grid from which the material IDs are used as seeds.
    selection : (sequence of) int, optional
        Material IDs to consider.
    invert_selection : bool, optional
        Consider all material IDs except those in selection. Defaults to False.
    average : bool, optional
        Seed corresponds to center of gravity of material ID cloud.
        Defaults to False.
    periodic : bool, optional
        Center of gravity accounts for periodic boundaries.
        Defaults to True.

    Returns
    -------
    coords, materials : numpy.ndarray, shape (:,3); numpy.ndarray, shape (:)
        Seed coordinates in 3D space, material IDs.

    Notes
    -----
    The origin is not considered in order to obtain coordinates
    in a coordinate system located at the origin. This is expected
    by damask.GeomGrid.from_Voronoi_tessellation.

    Examples
    --------
    Recreate seeds from Voronoi tessellation.

    >>> import numpy as np
    >>> import scipy.spatial
    >>> import damask
    >>> seeds = damask.seeds.from_random(np.ones(3),29,[128]*3,rng_seed=20191102)
    >>> (g := damask.GeomGrid.from_Voronoi_tessellation([128]*3,np.ones(3),seeds))
    cells:  128 × 128 × 128
    size:   1.0 × 1.0 × 1.0 m³
    origin: 0.0   0.0   0.0 m
    # materials: 29
    >>> COG,matID = damask.seeds.from_grid(g,average=True)
    >>> distance,ID = scipy.spatial.KDTree(COG,boxsize=g.size).query(seeds)
    >>> np.max(distance) / np.linalg.norm(g.size/g.cells)
    10.1
    >>> (ID == matID).all()
    True

    """
    material = grid.material.reshape((-1,1),order='F')
    mask = _np.full(grid.cells.prod(),True,dtype=bool) if selection is None else \
           _np.isin(material,selection,invert=invert_selection).flatten()
    coords = _grid_filters.coordinates0_point(grid.cells,grid.size).reshape(-1,3,order='F')

    if not average:
        return (coords[mask],material[mask])
    else:
        materials = _np.unique(material[mask])
        coords_ = _np.zeros((materials.size,3),dtype=float)
        for i,mat in enumerate(materials):
            pc = 2*_np.pi*coords[material[:,0]==mat,:]/grid.size
            coords_[i] = grid.size / 2 / _np.pi * (_np.pi +
                         _np.arctan2(-_np.average(_np.sin(pc),axis=0),
                                     -_np.average(_np.cos(pc),axis=0))) \
                         if periodic else \
                         _np.average(coords[material[:,0]==mat,:],axis=0)
        return (coords_,materials)
