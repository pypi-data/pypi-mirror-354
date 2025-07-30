from pydantic import BaseModel, Field
from typing import Literal
from pathlib import Path
import json
from loguru import logger
import fchic
from ase.data import chemical_symbols, atomic_numbers
import numpy as np

JobType = Literal["s0", "s1", "t1", "absorption_spec", "emission_spec"]


class Params(BaseModel):
    nproc: int = 32
    mem: str = "64GB"
    method: str = "b3lyp"
    basis: str = "def2svp"
    EmpiricalDispersion: str = "GD3BJ"
    td: int = -1  # f" td=(nstates={self.td})"
    opt: bool = False
    freq: bool = False
    charge: int = 0
    multiplicity: int = 1
    title: JobType | str = "s0"

    @classmethod
    def parse_from_json(cls, json_path: Path):
        with open(json_path, "r") as file:
            data = json.load(file)

        params = cls(**data)
        return params

    def to_str_lines(self) -> str:
        route = f"#P {self.method}/{self.basis}"
        if self.EmpiricalDispersion:
            route += f" EmpiricalDispersion={self.EmpiricalDispersion}"
        if self.opt:
            route += " opt"
        if self.freq:
            route += " freq"
        if self.td != -1:
            route += f" td=(nstates={self.td})"

        header_lines = [
            f"%nproc={self.nproc}",
            f"%mem={self.mem}",
            route,
            "",
            f"Job Type: {self.title}",
            "",
            f"{self.charge} {self.multiplicity}",
        ]

        header = "\n".join(header_lines) + "\n"
        return header


class Atom(BaseModel):
    symbol: str
    x: float
    y: float
    z: float


class Structure(BaseModel):
    atoms: list[Atom] = Field(default_factory=list)

    def to_str_lines(self) -> str:
        atom_str_list = [
            f"{atom.symbol:<2}  {atom.x:12.6f}  {atom.y:12.6f}  {atom.z:12.6f}"
            for atom in self.atoms
        ]
        structure_str = "\n".join(atom_str_list) + "\n"
        return structure_str
