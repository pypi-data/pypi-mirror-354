from __future__ import annotations

import copy
import json
import logging
import time
from abc import abstractmethod
from collections import deque
from typing import Any

import awkward as ak
import h5py
import numpy as np
from rich.progress import track

from f9columnar.processors import Postprocessor, Processor
from f9columnar.utils.loggers import timeit


class ArraysHdf5Writer(Postprocessor):
    def __init__(self, file_path: str, dataset_names: str | list[str] | None = None, name: str = "HDF5Writer") -> None:
        """Class for HDF5 data writer postprocessors that write awkward arrays to HDF5 file.

        Parameters
        ----------
        file_path : str
            Path to the created HDF5 file.
        dataset_names : str | list[str] | None, optional
            Names of the datasets to be created. Can be dir/subdir/.../dataset_name.
        name : str, optional
            Name of the processor.

        Other Parameters
        ----------------
        shape, chunks, maxshape, dtype, compression, compression_opts
            See [1].

        References
        ----------
        [1] - https://docs.h5py.org/en/stable/high/group.html#h5py.Group.create_dataset
        [2] - https://docs.h5py.org/en/stable/high/dataset.html
        [3] - https://pythonforthelab.com/blog/how-to-use-hdf5-files-in-python/

        """
        super().__init__(name)
        self.file_path = file_path

        if type(dataset_names) is str:
            self.dataset_names = [dataset_names]
        elif type(dataset_names) is list:
            self.dataset_names = dataset_names
        else:
            self.dataset_names = []

        self._current_idx = 0
        self._current_shape: int | None = None

    def create_datasets(
        self,
        mode: str = "w",
        dataset_names: list[str] | None = None,
        shape: tuple[int, int] | tuple[int, int, int] | None = None,
        chunks: bool = False,
        maxshape: tuple[int | None, int] | tuple[int | None, int, int] | None = None,
        dtype: str = "float32",
        compression: str = "lzf",
        compression_opts: int | None = None,
    ) -> None:
        if mode not in ["w", "a"]:
            raise ValueError("Mode must be 'w' or 'a'!")

        if maxshape is not None and shape is None:
            raise ValueError("Shape must be provided if maxshape is provided!")

        if maxshape is not None or compression:
            logging.info("Auto-chunking is enabled by default, if you use compression or maxshape.")
            chunks = True

        if dataset_names is None:
            dataset_names = self.dataset_names

            if len(dataset_names) == 0:
                raise ValueError("No dataset names provided!")

        with h5py.File(self.file_path, mode) as f:
            for dataset_name in dataset_names:
                dataset_name_split = dataset_name.split("/")

                f_obj = f
                for i, group in enumerate(dataset_name_split):
                    if i == len(dataset_name_split) - 1:
                        f_obj.create_dataset(
                            group,
                            shape=shape,
                            chunks=chunks,
                            maxshape=maxshape,
                            dtype=dtype,
                            compression=compression,
                            compression_opts=compression_opts,
                        )
                    elif i == 0:
                        if group not in f_obj:
                            g = f.create_group(group)
                            f_obj = g
                        else:
                            f_obj = f_obj[group]
                    else:
                        g = g.create_group(group)
                        f_obj = g

    def add_data(
        self,
        data: np.ndarray,
        dataset_name: str,
        idx: int | tuple[int, int],
        resize: tuple | None = None,
    ) -> None:
        if type(idx) is tuple and len(idx) > 2:
            raise ValueError("Only support 2D data!")

        with h5py.File(self.file_path, "a") as f:
            dataset = f[dataset_name]

            if resize:
                dataset.resize(resize)

            if type(idx) is int:
                dataset[idx] = data
            elif type(idx) is tuple:
                dataset[idx[0] : idx[1]] = data
            else:
                raise TypeError("idx must be a tuple or an integer!")

    def add_metadata(self, metadata_dct: dict[str, Any], group_name: str | None = None) -> None:
        with h5py.File(self.file_path, "a") as f:
            if group_name is not None:
                group = f[group_name]
            else:
                group = f

            group.create_dataset("metadata", data=json.dumps(metadata_dct))

    def get_metadata(self, group_name: str | None = None) -> dict[str, Any]:
        if group_name is None:
            group_name = "metadata"
        else:
            group_name = f"{group_name}/metadata"

        with h5py.File(self.file_path, "r") as f:
            metadata = json.loads(f[group_name][()])

        return metadata

    def get_keys(self) -> list[str]:
        with h5py.File(self.file_path, "r") as f:
            keys = list(f.keys())

        return keys

    def get_handle(self, mode: str = "r") -> h5py.File:
        return h5py.File(self.file_path, mode)

    def write_arrays(
        self,
        arrays: ak.Array,
        dataset_name: str,
        column_names: list[str],
        chunk_shape: int = 1000,
    ) -> None:
        if self._current_shape is None:
            self._current_shape = chunk_shape

        save_arrays = []

        for column_name in column_names:
            if column_name not in arrays.fields:
                raise RuntimeError(f"Column {column_name} not found in arrays!")

            column = ak.to_numpy(arrays[column_name])
            column = column[:, None]
            save_arrays.append(column)

        save_arrays = np.concatenate(save_arrays, axis=1)

        array_chunks = len(save_arrays) // chunk_shape + 1
        chunk_save_arrays = np.array_split(save_arrays, array_chunks)

        for chunk_array in chunk_save_arrays:
            n_chunk = len(chunk_array)
            start_idx, stop_idx = self._current_idx, self._current_idx + n_chunk

            self._current_idx = stop_idx

            if self._current_idx > self._current_shape:
                resize = (stop_idx, chunk_array.shape[1])
                self._current_shape = stop_idx
            else:
                resize = None

            self.add_data(chunk_array, dataset_name, idx=(start_idx, stop_idx), resize=resize)

    @abstractmethod
    def run(self, processors: dict[str, Processor], *args: Any, **kwargs: Any):
        pass


class ArraysHdf5PileWriter(ArraysHdf5Writer):
    def __init__(
        self,
        file_path: str,
        n_piles: int,
        pile_assignment: str = "random",
        dataset_names: str | list[str] | None = None,
        name: str = "HDF5Writer",
    ) -> None:
        """Implementation of ArraysHDF5Writer using piles. A pile is a separate dataset in the HDF5 file. Each chunk of
        data is saved to a random pile. This allows for processing large datasets that do not fit into memory and allows
        for shuffling the data during the writing process and reading process.

        Parameters
        ----------
        file_path : str
            Path to the created HDF5 file.
        n_piles : int
            Number of piles to split the data into.
        pile_assignment : str, optional
            Method of assigning data to piles. Can be 'deque' or 'random'.
        dataset_names : str | list[str] | None, optional
            Names of the datasets to be created. Can be dir/subdir/.../dataset_name.
        name : str, optional
            Name of the processor.

        Warning
        -------
        There is a chance that some piles will be missed in case of a small dataset. This is seen as piles of zeros in
        the HDF5 file. This can be fixed by setting the number of piles to an appropriate value.

        TODO: every dataset name should have its own deque to have better pile assignment coverage.

        References
        ----------
        [1] - https://blog.janestreet.com/how-to-shuffle-a-big-dataset/

        """
        super().__init__(file_path, dataset_names, name)
        self.n_piles = n_piles

        if pile_assignment not in ["deque", "random"]:
            raise ValueError("Pile assignment must be 'deque' or 'random'!")

        self.pile_assignment = pile_assignment

        if self.pile_assignment == "deque":
            self.pile_deque = deque(range(self.n_piles))

        # list of all datasets, mapping from each dataset name to a list of corresponding pile names
        self.pile_datasets_lst, self.pile_datasets_dct = self.get_pile_dataset_names()
        # mapping from each dataset name to a dictionary of its pile names and their current index and shape
        self.piles_info_dct = self.get_piles_info(start_dct={"current_idx": 0, "current_shape": None})

        self.current_dataset_name: str
        self.current_pile_name: str

    def get_pile_dataset_names(self) -> tuple[list[str], dict[str, list[str]]]:
        pile_datasets_lst, pile_datasets_dct = [], {}

        for dataset_name in self.dataset_names:
            piles = [f"{dataset_name}/p{i}" for i in range(self.n_piles)]

            pile_datasets_lst += piles
            pile_datasets_dct[dataset_name] = piles

        return pile_datasets_lst, pile_datasets_dct

    def get_piles_info(self, start_dct) -> dict[str, dict[str, dict[str, Any]]]:
        piles_info_dct = {}

        for dataset_name, pile_names in self.pile_datasets_dct.items():
            info_dct = {}

            for pile_name in pile_names:
                info_dct[pile_name] = copy.deepcopy(start_dct)

            piles_info_dct[dataset_name] = info_dct

        return piles_info_dct

    def set_current_pile_idx(self, value: int) -> ArraysHdf5PileWriter:
        self.piles_info_dct[self.current_dataset_name][self.current_pile_name]["current_idx"] = value
        return self

    def set_current_pile_shape(self, value: int) -> ArraysHdf5PileWriter:
        self.piles_info_dct[self.current_dataset_name][self.current_pile_name]["current_shape"] = value
        return self

    @property
    def current_pile_idx(self) -> int:
        return self.piles_info_dct[self.current_dataset_name][self.current_pile_name]["current_idx"]

    @property
    def current_pile_shape(self) -> int | None:
        return self.piles_info_dct[self.current_dataset_name][self.current_pile_name]["current_shape"]

    def write_arrays(
        self,
        arrays: ak.Array,
        dataset_name: str,
        column_names: list[str],
        chunk_shape: int = 1000,
    ) -> None:
        self.current_dataset_name = dataset_name

        save_arrays = []

        for column_name in column_names:
            if column_name not in arrays.fields:
                raise RuntimeError(f"Column {column_name} not found in arrays!")

            column = ak.to_numpy(arrays[column_name])
            column = column[:, None]
            save_arrays.append(column)

        save_arrays = np.concatenate(save_arrays, axis=1)

        array_chunks = len(save_arrays) // chunk_shape + 1
        chunk_save_arrays = np.array_split(save_arrays, array_chunks)

        for chunk_array in chunk_save_arrays:
            if self.pile_assignment == "deque":
                pile_idx = self.pile_deque[0]
                self.pile_deque.rotate(-1)
            else:
                pile_idx = np.random.choice(self.n_piles)

            self.current_pile_name = self.pile_datasets_dct[dataset_name][pile_idx]

            if self.current_pile_shape is None:
                self.set_current_pile_shape(chunk_shape)

            n_chunk = len(chunk_array)

            start_idx = self.current_pile_idx
            stop_idx = start_idx + n_chunk

            self.set_current_pile_idx(stop_idx)

            if self.current_pile_idx > self.current_pile_shape:  # type: ignore
                resize = (stop_idx, chunk_array.shape[1])
                self.set_current_pile_shape(stop_idx)
            else:
                resize = None

            self.add_data(chunk_array, self.current_pile_name, idx=(start_idx, stop_idx), resize=resize)

    @abstractmethod
    def run(self, processors: dict[str, Processor], *args: Any, **kwargs: Any):
        pass


class DatasetHdf5Writer(ArraysHdf5Writer):
    def __init__(
        self,
        file_path: str,
        dataset_name: str,
        column_names: list[str],
        save_node: str = "output",
        chunk_shape: int = 1000,
        name: str = "datasetHDF5Writer",
        **hdf5_kwargs: Any,
    ) -> None:
        super().__init__(file_path, dataset_names=dataset_name, name=name)
        self.chunk_shape = chunk_shape
        self.column_names = column_names
        self.save_node = save_node

        self.create_datasets(
            shape=(chunk_shape, len(column_names)),
            maxshape=(None, len(column_names)),
            **hdf5_kwargs,
        )
        self.add_metadata({"columns": self.column_names})

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        self.write_arrays(arrays, self.dataset_names[0], self.column_names, self.chunk_shape)

        return {"processors": processors}


class DatasetHdf5PileWriter(ArraysHdf5PileWriter):
    def __init__(
        self,
        file_path: str,
        dataset_name: str,
        n_piles: int,
        column_names: list[str],
        pile_assignment: str = "random",
        save_node: str = "output",
        chunk_shape: int = 1000,
        name: str = "datasetHDF5Writer",
        **hdf5_kwargs: Any,
    ) -> None:
        super().__init__(file_path, n_piles, pile_assignment, dataset_name, name)
        self.chunk_shape = chunk_shape
        self.column_names = column_names
        self.save_node = save_node

        self.create_datasets(
            dataset_names=self.pile_datasets_lst,
            shape=(chunk_shape, len(column_names)),
            maxshape=(None, len(column_names)),
            **hdf5_kwargs,
        )
        self.add_metadata({"columns": self.column_names, "piles": self.pile_datasets_dct})

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        self.write_arrays(arrays, self.dataset_names[0], self.column_names, self.chunk_shape)

        return {"processors": processors}


class NtupleHdf5Writer(ArraysHdf5Writer):
    def __init__(
        self,
        file_path: str,
        mc_column_names: list[str],
        data_column_names: list[str] | None = None,
        save_node: str = "output",
        chunk_shape: int = 1000,
        write_mc: bool = True,
        write_data: bool = True,
        name: str = "datasetHDF5Writer",
        dataset_names: list[str] | None = None,
        **hdf5_kwargs: Any,
    ) -> None:
        if dataset_names is None:
            dataset_names = ["mc", "data"]

        if len(dataset_names) != 2:
            raise ValueError("Dataset names must be a list of two strings!")

        super().__init__(file_path, dataset_names=dataset_names, name=name)
        self.save_node = save_node
        self.chunk_shape = chunk_shape

        if write_data is False and write_mc is False:
            raise ValueError("Both write_data and write_mc cannot be False!")

        self.write_data, self.write_mc = write_data, write_mc

        self.mc_column_names = mc_column_names

        if data_column_names is None:
            logging.info("Data column names not provided, using MC column names.")
            self.data_column_names = mc_column_names
        else:
            self.data_column_names = data_column_names

        metadata = {}
        mc_group, data_group = self.dataset_names[0], self.dataset_names[1]

        if write_mc:
            self.create_datasets(
                dataset_names=[mc_group],
                shape=(self.chunk_shape, len(self.mc_column_names)),
                maxshape=(None, len(self.mc_column_names)),
                **hdf5_kwargs,
            )
            metadata[f"{mc_group}_columns"] = self.mc_column_names

        if write_data:
            self.create_datasets(
                mode="a" if self.write_mc else "w",
                dataset_names=[data_group],
                shape=(self.chunk_shape, len(self.data_column_names)),
                maxshape=(None, len(self.data_column_names)),
                **hdf5_kwargs,
            )
            metadata[f"{data_group}_columns"] = self.data_column_names

        self.add_metadata(metadata)

        self._current_mc_idx, self._current_data_idx = 0, 0
        self._current_mc_shape, self._current_data_shape = None, None

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        if self.is_data and self.write_data:
            self._current_idx, self._current_shape = self._current_mc_idx, self._current_mc_shape
            self.write_arrays(arrays, self.dataset_names[1], self.data_column_names, self.chunk_shape)
            self._current_mc_idx, self._current_mc_shape = self._current_idx, self._current_shape

        if not self.is_data and self.write_mc:
            self._current_idx, self._current_shape = self._current_data_idx, self._current_data_shape
            self.write_arrays(arrays, self.dataset_names[0], self.mc_column_names, self.chunk_shape)
            self._current_data_idx, self._current_data_shape = self._current_idx, self._current_shape

        return {"processors": processors}


class NtupleHdf5PileWriter(ArraysHdf5PileWriter):
    def __init__(
        self,
        file_path: str,
        n_piles: int,
        mc_column_names: list[str],
        data_column_names: list[str] | None = None,
        pile_assignment: str = "random",
        save_node: str = "output",
        chunk_shape: int = 1000,
        write_mc: bool = True,
        write_data: bool = True,
        name: str = "datasetHDF5Writer",
        dataset_names_map: dict[str, str] | None = None,
        **hdf5_kwargs: Any,
    ) -> None:
        if dataset_names_map is None:
            dataset_names = ["mc", "data"]
        else:
            dataset_names = [dataset_names_map["mc"], dataset_names_map["data"]]

        if len(dataset_names) != 2:
            raise ValueError("Dataset names must be a list of two strings!")

        super().__init__(file_path, n_piles, pile_assignment, dataset_names=dataset_names, name=name)
        self.save_node = save_node
        self.chunk_shape = chunk_shape

        if write_data is False and write_mc is False:
            raise ValueError("Both write_data and write_mc cannot be False!")

        self.write_data, self.write_mc = write_data, write_mc

        self.mc_column_names = mc_column_names

        if data_column_names is None:
            logging.info("Data column names not provided, using MC column names.")
            self.data_column_names = mc_column_names
        else:
            self.data_column_names = data_column_names

        metadata: dict[str, Any] = {}
        mc_group, data_group = self.dataset_names[0], self.dataset_names[1]

        if write_mc:
            self.create_datasets(
                dataset_names=self.pile_datasets_dct[mc_group],
                shape=(self.chunk_shape, len(self.mc_column_names)),
                maxshape=(None, len(self.mc_column_names)),
                **hdf5_kwargs,
            )
            metadata[f"{mc_group}_columns"] = self.mc_column_names

        if write_data:
            self.create_datasets(
                mode="a" if self.write_mc else "w",
                dataset_names=self.pile_datasets_dct[data_group],
                shape=(self.chunk_shape, len(self.data_column_names)),
                maxshape=(None, len(self.data_column_names)),
                **hdf5_kwargs,
            )
            metadata[f"{data_group}_columns"] = self.data_column_names

        metadata["piles"] = self.pile_datasets_dct

        self.add_metadata(metadata)

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        if self.is_data and self.write_data:
            self.write_arrays(arrays, self.dataset_names[1], self.data_column_names, self.chunk_shape)

        if not self.is_data and self.write_mc:
            self.write_arrays(arrays, self.dataset_names[0], self.mc_column_names, self.chunk_shape)

        return {"processors": processors}


class PhysicsObjectDatasetHdf5Writer(ArraysHdf5Writer):
    def __init__(
        self,
        file_path: str,
        flat_column_names: list[str] | None = None,
        jagged_column_names: dict[str, list[str]] | None = None,
        chunk_shape: int = 1000,
        max_lengths: dict[str, int] | int = 10,
        pad_values: dict[str, float] | float | None = 0.0,
        n_piles: int | None = None,
        pile_assignment: str = "random",
        save_node: str = "output",
        **hdf5_kwargs,
    ) -> None:
        """Generalized HDF5 writer for physics objects. It supports both flat and jagged arrays.

        Parameters
        ----------
        file_path : str
            Path to the created HDF5 file.
        flat_column_names : list[str] | None, optional
            List of flat column names to be saved in the HDF5 file. If None, jagged_column_names must be provided.
        jagged_column_names : dict[str, list[str]] | None, optional
            Dictionary of jagged column names to be saved in the HDF5 file. The keys are the names of the physics
            objects (e.g. electrons, jets, etc.), and the values are lists of column names for each physics object.
            If None, flat_column_names must be provided.
        chunk_shape : int, optional
            Number of events to be saved in each chunk. This is used to split the data into chunks for writing.
        max_lengths : dict[str, int] | int, optional
            Maximum length of the jagged arrays. If an int is provided, it will be used for all jagged arrays.
            If a dictionary is provided, the keys must match the keys in jagged_column_names and the values are the
            maximum lengths for each jagged array.
        pad_values : dict[str, float] | float | None, optional
            Values to pad the jagged arrays with. If a float is provided, it will be used for all jagged arrays.
            If a dictionary is provided, the keys must match the keys in jagged_column_names and the values are the
            pad values for each jagged array. If None, no padding will be applied and the resulting arrays will be
            numpy masked arrays.
        n_piles : int | None, optional
            Number of piles to split the data into. If None, the data will be saved in a single dataset.
        pile_assignment : str, optional
            Method of assigning data to piles. Can be 'deque' or 'random'. If 'deque', the data will be assigned to
            piles in a double-ended queue fashion. If 'random', the data will be assigned to piles randomly.
        save_node : str, optional
            Name of the node in the processor that contains the arrays to be saved. Default is "output".

        """
        super().__init__(
            file_path,
            dataset_names=None,
            name="physicsObjectDatasetHdf5Writer",
            **hdf5_kwargs,
        )
        if flat_column_names is None and jagged_column_names is None:
            raise ValueError("At least one of flat_column_names or jagged_column_names must be provided.")

        self.chunk_shape = chunk_shape

        self.n_piles = n_piles
        self.pile_assignment = pile_assignment

        self.save_node = save_node

        self.object_info_dct: dict[str, dict[str, int]] = {}
        self.object_piles_info_dct: dict[str, dict[int, dict[str, int]]] = {}

        self.object_column_names_dct: dict[str, list[str]] = {}

        self.pad_values: dict[str, float] | None = None
        self.max_lengths: dict[str, int] | None = None

        _metadata: dict[str, Any] = {}

        if flat_column_names is not None:
            self.write_flat = True
            _flat_meatdata = self._create_event_datasets(flat_column_names, **hdf5_kwargs)
            _metadata.update(_flat_meatdata)
        else:
            self.write_flat = False

        if jagged_column_names is not None:
            self.write_jagged = True

            self._set_max_lengths(jagged_column_names, max_lengths)
            self._set_pad_values(jagged_column_names, pad_values)

            _jagged_metadata = self._create_jagged_datasets(jagged_column_names, **hdf5_kwargs)
            _metadata.update(_jagged_metadata)
        else:
            self.write_jagged = False

        _piles_metadata: dict[str, list[str]] = {}
        if "events_piles" in _metadata:
            _piles_metadata["events"] = _metadata["events_piles"]
            _metadata.pop("events_piles")

        if "jagged_piles" in _metadata:
            _piles_metadata.update(_metadata["jagged_piles"])
            _metadata.pop("jagged_piles")

        if len(_piles_metadata) != 0:
            _metadata["piles"] = _piles_metadata

        self.add_metadata(_metadata)

        self.pile_deque: deque[int] | None = None

        if self.n_piles is not None and self.pile_assignment == "deque":
            self.pile_deque = deque(range(self.n_piles))

        self.current_dataset_name: str
        self._current_pile_idx = 0

    def _set_max_lengths(self, jagged_column_names: dict[str, list[str]], max_lengths: dict[str, int] | int) -> None:
        if type(max_lengths) is int:
            self.max_lengths = {column_name: max_lengths for column_name in jagged_column_names.keys()}
        elif type(max_lengths) is dict:
            self.max_lengths = max_lengths
        else:
            raise TypeError("max_lengths must be an int or a dictionary with column names as keys.")

    def _set_pad_values(
        self, jagged_column_names: dict[str, list[str]], pad_values: dict[str, float] | float | None
    ) -> None:
        if pad_values is None:
            self.pad_values = None
        elif type(pad_values) is float:
            self.pad_values = {column_name: pad_values for column_name in jagged_column_names.keys()}
        elif type(pad_values) is dict:
            self.pad_values = pad_values
        else:
            raise TypeError("pad_values must be a float, None or a dictionary with column names as keys.")

    def _create_event_datasets(self, flat_column_names: list[str], **hdf5_kwargs) -> dict[str, list[str]]:
        _metadata: dict[str, Any] = {}

        if self.n_piles is None:
            dataset_names = ["events"]
        else:
            dataset_names = [f"events/p{p}" for p in range(self.n_piles)]

        self.create_datasets(
            mode="w",
            dataset_names=dataset_names,
            shape=(self.chunk_shape, len(flat_column_names)),
            maxshape=(None, len(flat_column_names)),
            **hdf5_kwargs,
        )

        _metadata["events_columns"] = flat_column_names

        if self.n_piles is None:
            self.object_info_dct["events"] = {"current_idx": 0, "current_shape": self.chunk_shape}
        else:
            self.object_piles_info_dct["events"] = {}
            for p in range(self.n_piles):
                self.object_piles_info_dct["events"][p] = {
                    "current_idx": 0,
                    "current_shape": self.chunk_shape,
                }

        self.object_column_names_dct["events"] = flat_column_names

        if self.n_piles is not None:
            _metadata["events_piles"] = [f"p{i}" for i in range(self.n_piles)]

        return _metadata

    def _create_jagged_datasets(self, jagged_column_names: dict[str, list[str]], **hdf5_kwargs) -> dict[str, list[str]]:
        _metadata: dict[str, Any] = {}
        _piles_metadata: dict[str, list[str]] = {}

        for physics_object_name, physics_object_column_names in jagged_column_names.items():
            if self.n_piles is None:
                dataset_names = [physics_object_name]
            else:
                dataset_names = [f"{physics_object_name}/p{p}" for p in range(self.n_piles)]

            if self.max_lengths is None:
                raise ValueError(f"max_lengths must be provided for {physics_object_name} datasets!")

            max_length = self.max_lengths[physics_object_name]

            self.create_datasets(
                mode="a" if self.write_flat else "w",
                dataset_names=dataset_names,
                shape=(self.chunk_shape, max_length, len(physics_object_column_names)),
                maxshape=(None, max_length, len(physics_object_column_names)),
                **hdf5_kwargs,
            )

            _metadata[f"{physics_object_name}_columns"] = physics_object_column_names

            if self.n_piles is None:
                self.object_info_dct[physics_object_name] = {"current_idx": 0, "current_shape": self.chunk_shape}
            else:
                self.object_piles_info_dct[physics_object_name] = {}
                for p in range(self.n_piles):
                    self.object_piles_info_dct[physics_object_name][p] = {
                        "current_idx": 0,
                        "current_shape": self.chunk_shape,
                    }

                _piles_metadata[physics_object_name] = [f"p{i}" for i in range(self.n_piles)]

            self.object_column_names_dct[physics_object_name] = physics_object_column_names

        if self.n_piles is not None:
            _metadata["jagged_piles"] = _piles_metadata

        return _metadata

    def _get_flat_arrays(self, arrays: ak.Array, column_names: list[str]) -> np.ndarray:
        save_arrays = []

        for column_name in column_names:
            if column_name not in arrays.fields:
                raise RuntimeError(f"Column {column_name} not found in arrays!")

            column = ak.to_numpy(arrays[column_name])
            column = column[:, None]
            save_arrays.append(column)

        return np.concatenate(save_arrays, axis=-1)

    def _get_jagged_arrays(self, arrays: ak.Array, column_names: list[str]) -> np.ndarray:
        save_arrays = []

        for column_name in column_names:
            if column_name not in arrays.fields:
                raise RuntimeError(f"Column {column_name} not found in arrays!")

            column_matrix = arrays[column_name]

            if self.max_lengths is not None:
                column_matrix = ak.pad_none(column_matrix, self.max_lengths[self.current_dataset_name], clip=True)

            if self.pad_values is not None:
                column_matrix = ak.fill_none(column_matrix, self.pad_values[self.current_dataset_name])

            column_matrix = ak.to_numpy(column_matrix)
            column_matrix = column_matrix[:, :, None]

            save_arrays.append(column_matrix)

        return np.concatenate(save_arrays, axis=-1)

    def get_pile_idx(self) -> int:
        if self.n_piles is None:
            raise RuntimeError("n_piles is not set!")

        if self.pile_assignment == "deque":
            if self.pile_deque is None:
                raise RuntimeError("Pile deque is not initialized!")

            idx = self.pile_deque[0]
            self.pile_deque.rotate(-1)
            return idx
        else:
            return np.random.choice(self.n_piles)

    def set_current_idx(self, value: int) -> None:
        if self.n_piles is None:
            self.object_info_dct[self.current_dataset_name]["current_idx"] = value
        else:
            self.object_piles_info_dct[self.current_dataset_name][self.current_pile_idx]["current_idx"] = value

        return None

    def set_current_shape(self, value: int) -> None:
        if self.n_piles is None:
            self.object_info_dct[self.current_dataset_name]["current_shape"] = value
        else:
            self.object_piles_info_dct[self.current_dataset_name][self.current_pile_idx]["current_shape"] = value

        return None

    def set_current_pile_idx(self, value: int) -> None:
        self._current_pile_idx = value
        return None

    @property
    def current_idx(self) -> int:
        if self.n_piles is None:
            return self.object_info_dct[self.current_dataset_name]["current_idx"]
        else:
            return self.object_piles_info_dct[self.current_dataset_name][self.current_pile_idx]["current_idx"]

    @property
    def current_shape(self) -> int:
        if self.n_piles is None:
            return self.object_info_dct[self.current_dataset_name]["current_shape"]
        else:
            return self.object_piles_info_dct[self.current_dataset_name][self.current_pile_idx]["current_shape"]

    @property
    def current_pile_idx(self) -> int:
        return self._current_pile_idx

    def write_object_arrays(
        self,
        arrays: ak.Array,
        dataset_name: str,
        column_names: list[str],
        pile_idx_lst: list[int],
        is_flat: bool = True,
    ) -> None:
        self.current_dataset_name = dataset_name

        if is_flat:
            save_arrays = self._get_flat_arrays(arrays, column_names)
        else:
            save_arrays = self._get_jagged_arrays(arrays, column_names)

        array_chunks = len(save_arrays) // self.chunk_shape + 1
        chunk_save_arrays = np.array_split(save_arrays, array_chunks)

        for i, chunk_array in enumerate(chunk_save_arrays):
            n_chunk = len(chunk_array)

            start_idx = self.current_idx
            stop_idx = start_idx + n_chunk

            self.set_current_idx(stop_idx)

            if self.current_idx > self.current_shape:
                if is_flat:
                    resize = (stop_idx, chunk_array.shape[1])
                else:
                    resize = (stop_idx, self.max_lengths[self.current_dataset_name], chunk_array.shape[2])  # type: ignore

                self.set_current_shape(stop_idx)
            else:
                resize = None

            if self.n_piles is None:
                current_dataset_name = self.current_dataset_name
            else:
                current_dataset_name = f"{self.current_dataset_name}/p{self.current_pile_idx}"
                self.set_current_pile_idx(pile_idx_lst[i])

            self.add_data(chunk_array, current_dataset_name, idx=(start_idx, stop_idx), resize=resize)

    def run(self, processors: dict[str, Processor]) -> dict[str, dict[str, Processor]]:
        arrays_processor = processors[self.save_node]

        if hasattr(arrays_processor, "arrays"):
            arrays = arrays_processor.arrays
        else:
            raise AttributeError("Arrays attribute not found in the processor!")

        if self.n_piles is not None:
            n_add_iters = len(arrays) // self.chunk_shape + 1
            pile_idx_lst = [self.get_pile_idx() for _ in range(n_add_iters)]
        else:
            pile_idx_lst = []

        for physics_object_name, physics_object_column_names in self.object_column_names_dct.items():
            self.write_object_arrays(
                arrays,
                dataset_name=physics_object_name,
                column_names=physics_object_column_names,
                pile_idx_lst=pile_idx_lst,
                is_flat=(physics_object_name == "events"),
            )

        return {"processors": processors}


class PileShuffler:
    def __init__(self, file_path: str, dataset_names: str | list[str] | None = None) -> None:
        self.file_path = file_path

        if type(dataset_names) is str:
            self.dataset_names = [dataset_names]
        elif type(dataset_names) is list:
            self.dataset_names = dataset_names
        else:
            self.dataset_names = []

        self.pile_datasets = self._get_pile_datasets()

    def _get_pile_datasets(self) -> dict[str, list[str]]:
        pile_datasets = {}

        with h5py.File(self.file_path, "r") as f:
            for dataset_name in self.dataset_names:
                if dataset_name not in f:
                    raise ValueError(f"Dataset {dataset_name} not found in the file!")

                pile_datasets[dataset_name] = list(f[dataset_name].keys())

        return pile_datasets

    def _shuffle_dataset_pile(self, dataset_name: str, pile: str) -> float:
        start_time = time.time()

        with h5py.File(self.file_path, "r+") as f:
            data = f[f"{dataset_name}/{pile}"][:]
            np.random.shuffle(data)
            f[f"{dataset_name}/{pile}"][:] = data

        return time.time() - start_time

    @timeit("s")
    def shuffle(self) -> list[float]:
        shuffle_args = []

        for dataset_name, piles in self.pile_datasets.items():
            for pile in piles:
                shuffle_args.append((dataset_name, pile))

        results = []
        for shuffle_arg in track(shuffle_args, description="Shuffling piles...", total=len(shuffle_args)):
            result = self._shuffle_dataset_pile(*shuffle_arg)
            results.append(result)

        logging.info(f"Shuffled {len(results)} piles!")

        return results
