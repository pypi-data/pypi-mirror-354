import abc
import sys
from pathlib import Path
import typing
import zipfile
import os
import uuid
from collections import defaultdict
from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket
from google.protobuf.json_format import Parse
from .phenopacket_info import EagerPhenopacketInfo, ZipPhenopacketInfo
from .cohort_info import CohortInfo

class PhenopacketStore(metaclass=abc.ABCMeta):
    """
    `PhenopacketStore` provides the data and metadata for Phenopacket Store cohorts.

    Use :func:`from_release_zip` or :func:`from_notebook_dir` to open a store instance.
    """

    @staticmethod
    def from_release_zip(
            zip_file: zipfile.ZipFile,
            strategy: typing.Literal["eager", "lazy"] = "eager",
    ) -> "PhenopacketStore":
        """
        Read `PhenopacketStore` from a release ZIP archive.

        The archive structure must match the structure of the ZIP archives
        created by :class:`ppktstore.archive.PhenopacketStoreArchiver`.
        Only JSON phenopacket format is supported at the moment.

        Strategy
        ^^^^^^^^

        The phenopackets can be loaded in an *eager* or *lazy* fashion.

        The `'eager'` strategy loads *all* phenopackets during the execution
        of this function. This may do more work than necessary,
        especially if only several cohorts are needed.

        The `'lazy'` strategy only scans the ZIP for phenopackets
        and the actual parsing is done on demand, when accessing
        the :attr:`PhenopacketInfo.phenopacket` property.
        In result, the lazy loading will only succeed if the ZIP handle is kept open.

        .. note::

          We recommend using Python's context manager to ensure `zip_handle` is closed:

          >>> import zipfile
          >>> with zipfile.ZipFile("all_phenopackets.zip") as zf:  # doctest: +SKIP
          ...   ps = PhenopacketStore.from_release_zip(zf)
          ...   # Do things here...

        :param zip_file: a ZIP archive handle.
        :param strategy: a `str` with strategy for loading phenopackets, one of `{'eager', 'lazy'}`.
        :returns: :class:`PhenopacketStore` with data read from the archive.
        """
        assert strategy in (
            "eager",
            "lazy",
        ), f"Strategy must be either `eager` or `lazy`: {strategy}"

        root = zipfile.Path(zip_file)

        # Prepare paths to cohort folders
        # and collate paths to cohort phenopackets.
        cohort2path = {}
        cohort2pp_paths = defaultdict(list)
        for entry in zip_file.infolist():
            entry_path = zipfile.Path(zip_file, at=entry.filename)
            if entry_path.is_dir():
                entry_parent = relative_to(root, entry_path.parent)
                if entry_parent in ('', '.'):
                    name = entry_path.name
                else:
                    cohort_name = entry_path.name
                    cohort2path[cohort_name] = entry_path
            elif entry_path.is_file() and entry_path.name.endswith('.json'):
                # This SHOULD be a phenopacket!
                cohort = entry_path.parent.name  # type: ignore
                cohort2pp_paths[cohort].append(entry_path)

        # Put cohorts together
        cohorts = []
        for cohort, cohort_path in cohort2path.items():
            if cohort in cohort2pp_paths:
                at = relative_to(root, cohort_path)
                rel_cohort_path = zipfile.Path(
                    zip_file, at=at,
                )
                pp_infos = []
                for pp_path in cohort2pp_paths[cohort]:
                    # cohort_path_str = str(cohort_path)
                    # pp_path_str = str(pp_path)
                    # path = pp_path_str.replace(cohort_path_str, '')
                    path = relative_to(cohort_path, pp_path)
                    # path = pp_path.relative_to(cohort_path)
                    if strategy == "eager":
                        pi = EagerPhenopacketInfo.from_path(path, pp_path)
                    elif strategy == "lazy":
                        pi = ZipPhenopacketInfo(
                            path=path,
                            pp_path=pp_path,
                        )
                    pp_infos.append(pi)

                ci = CohortInfo(
                    name=cohort,
                    path=str(rel_cohort_path),
                    phenopackets=tuple(pp_infos),
                )
                cohorts.append(ci)

        path = Path(str(root))

        return PhenopacketStore.from_cohorts(
            name=name,
            path=path,
            cohorts=cohorts,
        )

    @staticmethod
    def from_notebook_dir(
            nb_dir: str,
            pp_dir: str = "phenopackets",
    ) -> "PhenopacketStore":
        """
        Create `PhenopacketStore` from Phenopacket store notebook dir `nb_dir`.

        We expect the `nb_dir` to include a folder per cohort,
        and the phenopackets should be stored in `pp_dir` sub-folder (``pp_dir=phenopackets`` by default).

        The phenopackets are loaded *eagerly* into memory.

        The function is intended for private use only and we encourage
        using the Phenopacket Store registry API presented in :ref:`load-phenopacket-store` section.
        """
        cohorts = []
        nb_path = Path(nb_dir)
        for cohort_name in os.listdir(nb_path):
            cohort_dir = nb_path.joinpath(cohort_name)
            if cohort_dir.is_dir():
                cohort_path = cohort_dir.joinpath(pp_dir)
                if cohort_path.is_dir():
                    pp_infos = []
                    rel_cohort_path = cohort_path.relative_to(nb_path)
                    for filename in os.listdir(cohort_path):
                        if filename.endswith(".json"):
                            filepath = cohort_path.joinpath(filename)
                            pp = Parse(filepath.read_text(), Phenopacket())
                            pi = EagerPhenopacketInfo(
                                path=filename,
                                phenopacket=pp,
                            )
                            pp_infos.append(pi)

                    cohorts.append(
                        CohortInfo(
                            name=cohort_name,
                            path=str(rel_cohort_path),
                            phenopackets=tuple(pp_infos),
                        )
                    )

        return PhenopacketStore.from_cohorts(
            name=nb_path.name,
            path=nb_path,
            cohorts=cohorts,
        )

    @staticmethod
    def from_cohorts(
            name: str,
            path: Path,
            cohorts: typing.Iterable[CohortInfo],
    ) -> "PhenopacketStore":
        """
        Create `PhenopacketStore` from cohorts.

        :param name: a `str` with the store name (e.g. `v0.1.23` or any other `str` will do).
        :param path: a path to the store root to resolve phenopacket locations.
        :param cohorts: an iterable with cohorts.
        """
        return DefaultPhenopacketStore(
            name=name,
            path=path,
            cohorts=cohorts,
        )

    @staticmethod
    def from_folder(path: str) -> "PhenopacketStore":
        """
        Create `PhenopacketStore` from folder we group all phenopackets to a single cohort.

        :param name: a `str` with the store name (e.g. `v0.1.23` or any other `str` will do).
        :param path: a path to the store root to resolve phenopacket locations.
        """
        cohorts = []
        cohort_name = f"{str(uuid.uuid4())}-run"
        pp_infos = []
        path = Path(path)
        for filename in os.listdir(Path(path)):
            if filename.endswith(".json"):
                filepath = path.joinpath(filename)
                pp = Parse(filepath.read_text(), Phenopacket())
                pi = EagerPhenopacketInfo(
                    path=filename,
                    phenopacket=pp,
                )
                pp_infos.append(pi)
        cohorts.append(
            CohortInfo(
                name=cohort_name,
                path=str(path),
                phenopackets=tuple(pp_infos),
            )
        )
        return DefaultPhenopacketStore(
            name=cohort_name,
            path=path,
            cohorts=cohorts,
        )

    @staticmethod
    def from_file(path: str) -> "PhenopacketStore":
        """
        Create `PhenopacketStore` from a single phenopacket JSON file.
        The result is a store with one cohort and one phenopacket.

        :param name: a `str` with the store name.
        :param path: a path to the phenopacket JSON file.
        """
        import uuid
        from phenopackets.schema.v2.phenopackets_pb2 import Phenopacket
        from google.protobuf.json_format import Parse

        cohort_name = f"{uuid.uuid4()}-single"
        path = Path(path)
        pp = Parse(path.read_text(), Phenopacket())
        pi = EagerPhenopacketInfo(
            path=path.name,
            phenopacket=pp,
        )
        cohort = CohortInfo(
            name=cohort_name,
            path=str(path),
            phenopackets=(pi,),
        )
        return DefaultPhenopacketStore(
            name=cohort_name,
            path=path,
            cohorts=[cohort],
        )

    @property
    @abc.abstractmethod
    def name(self) -> str:
        """
        Get a `str` with the Phenopacket Store name. Most of the time,
        the name corresponds to the release tag (e.g. `0.1.18`).
        """
        pass

    @property
    @abc.abstractmethod
    def path(self) -> Path:
        """
        Get path to the phenopacket store resource.
        """
        pass

    @abc.abstractmethod
    def cohorts(self) -> typing.Collection[CohortInfo]:
        """
        Get a collection of all Phenopacket Store cohorts.
        """
        pass

    @abc.abstractmethod
    def cohort_for_name(
            self,
            name: str,
    ) -> CohortInfo:
        """
        Retrieve a Phenopacket Store cohort by its name.

        :param name: a `str` with the cohort name (e.g. ``SUOX``).
        :raises KeyError: if no cohort with such name exists.
        """
        pass

    def iter_cohort_phenopackets(
            self,
            name: str,
    ) -> typing.Iterator[Phenopacket]:
        """
        Get an iterator with all phenopackets of a cohort.

        :param name: a `str` with the cohort name.
        """
        return self.cohort_for_name(name).iter_phenopackets()

    def cohort_names(self) -> typing.Iterator[str]:
        """
        Get an iterator with names of all Phenopacket Store cohorts.
        """
        return map(lambda ci: ci.name, self.cohorts())

    def cohort_count(self) -> int:
        """
        Compute the count of Phenopacket Store cohorts.
        """
        return len(self.cohorts())

    def phenopacket_count(self) -> int:
        """
        Compute the total number of phenopackets available in Phenopacket Store.
        """
        return sum(len(cohort) for cohort in self.cohorts())


class DefaultPhenopacketStore(PhenopacketStore):
    def __init__(self, name: str, path: Path, cohorts: typing.Iterable[CohortInfo]):
        self._name = name
        self._path = path
        self._cohorts = {cohort.name: cohort for cohort in cohorts}

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> Path:
        return self._path

    def cohorts(self) -> typing.Collection[CohortInfo]:
        return self._cohorts.values()

    def cohort_for_name(self, name: str) -> CohortInfo:
        return self._cohorts[name]


def relative_to(a, b) -> str:
    if sys.version_info >= (3, 12):
        # The functionality seems to have been introduced in 3.12.
        return str(a.relative_to(b))
    else:
        a_str = str(a)
        b_str = str(b)
        return b_str.replace(a_str, '')
