from pydantic import BaseModel, Field, model_validator
from pathlib import Path
import numpy as np
from typing import Literal
from typing_extensions import Self
import fchic
import subprocess, json, argparse, os
from ase.data import chemical_symbols, atomic_numbers
from loguru import logger
from src.task import Task, structure_file_suffix, workspace
from .g16_struct import Params, Structure as BaseStructure
from datetime import datetime
from rdkit import Chem
from rdkit.Chem import rdDepictor, rdDistGeom, AllChem


# 配置loguru输出到当前工作目录
logger.add(
    os.path.join(os.getcwd(), "g16_server.log"),  # 输出到当前工作目录
    rotation="100 MB",  # 日志文件大小达到10MB时轮转
    retention="30 days",  # 保留7天的日志
    level="INFO",  # 日志级别
    enqueue=True,  # 线程安全
    encoding="utf-8",
)


rdDepictor.SetPreferCoordGen(True)
etkdg = rdDistGeom.ETKDGv3()
etkdg.randomSeed = 0xA700F
etkdg.verbose = False
etkdg.numThreads = 0
etkdg.optimizerForceTol = 0.0135
etkdg.useRandomCoords = False


class Atom(BaseModel):
    symbol: str
    x: float
    y: float
    z: float


class Structure(BaseStructure):
    atoms: list[Atom] = Field(default_factory=list)

    @classmethod
    def parse_from_rdkit(
        cls, smiles_or_molblock: str = "", path: Path | None = None
    ) -> "Structure":
        if path:
            if not path.exists():
                logger.error(f"File not found: {path}")
                raise FileNotFoundError(f"File not found: {path}")
            smiles_or_molblock = path.read_text()

        # 1. 生成mol
        if "\n" in smiles_or_molblock.strip():
            mol = Chem.MolFromMolBlock(smiles_or_molblock)
        else:
            mol = Chem.MolFromSmiles(smiles_or_molblock)
        if mol is None:
            raise ValueError(f"Invalid smiles_or_molblock string: {smiles_or_molblock}")

        # 2. generate 3d structure
        mol = Chem.AddHs(mol)
        conf_ids = rdDistGeom.EmbedMultipleConfs(mol, numConfs=10, params=etkdg)
        if len(conf_ids) == 0:
            msg = "Failed to generate 3D coordinates for the molecule"
            logger.error(msg)
            raise ValueError(msg)

        # 3. 对每个构象用MMFF94优化，并记录能量
        energies = []
        for conf_id in conf_ids:
            # MMFF优化
            AllChem.MMFFOptimizeMolecule(mol, confId=conf_id)  # type: ignore
            # 计算能量
            mmff_props = AllChem.MMFFGetMoleculeProperties(mol)  # type: ignore
            ff = AllChem.MMFFGetMoleculeForceField(mol, mmff_props, confId=conf_id)  # type: ignore
            energy = ff.CalcEnergy()
            energies.append((conf_id, energy))

        # 4. 找到能量最低的构象
        best_conf_id, _best_energy = min(energies, key=lambda x: x[1])

        atoms = []
        conf = mol.GetConformer(best_conf_id)
        for atom in mol.GetAtoms():  # type: ignore
            symbol = atom.GetSymbol()  # type: ignore
            pos = conf.GetAtomPosition(atom.GetIdx())
            atoms.append(
                Atom(
                    symbol=symbol,
                    x=pos.x,
                    y=pos.y,
                    z=pos.z,
                )
            )

        return cls(atoms=atoms)

    @classmethod
    def parse_from_xyz_file(cls, xyz_path: Path) -> "Structure":
        if not xyz_path.exists():
            msg = f"File not found: {xyz_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        with open(xyz_path, "r") as f:
            lines = f.readlines()

        total_atoms_nums = int(lines[0].strip())
        atoms = []
        for line in lines[2:]:
            sub_strs = line.strip().split()
            if len(sub_strs) == 4:
                atoms.append(
                    Atom(
                        symbol=sub_strs[0],
                        x=float(sub_strs[1]),
                        y=float(sub_strs[2]),
                        z=float(sub_strs[3]),
                    )
                )

        if len(atoms) != total_atoms_nums:
            msg = f"parse xyz to Structure error: total_atoms_num-{total_atoms_nums} not equal parse_len-{len(atoms)}; {xyz_path.as_posix()}"
            logger.error(msg)
            raise ValueError(msg)
        return cls(atoms=atoms)

    @classmethod
    def parse_from_fchk_file(cls, fchk_path: Path) -> "Structure":
        if not fchk_path.exists():
            msg = f"File not found: {fchk_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        with open(fchk_path, "r") as f:
            coord_s0_opt = fchic.deck_load(f, "Current cartesian coordinates")
            species_s0_opt = fchic.deck_load(f, "Atomic numbers")

        symbol_s0_opt = [chemical_symbols[i] for i in species_s0_opt]  # type: ignore
        coord_s0_opt = np.array(coord_s0_opt)
        ## 注意采用fchk信息时候，单位是au
        coord_s0_opt = coord_s0_opt.reshape((-1, 3)) * 0.5291772

        atoms = []
        for index, symbol in enumerate(symbol_s0_opt):
            atoms.append(
                Atom(
                    symbol=symbol,
                    x=coord_s0_opt[index][0],
                    y=coord_s0_opt[index][1],
                    z=coord_s0_opt[index][2],
                )
            )

        return cls(atoms=atoms)

    @classmethod
    def parse_from_chk_file(cls, chk_path: Path) -> "Structure":
        # 1. 检查文件是否存在
        if not chk_path.exists():
            msg = f"File not found: {chk_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        # 2. 使用formchk将chk转换为fchk
        fchk_path = chk_path.with_suffix(".fchk")
        if not fchk_path.exists():
            # 如果fchk文件不存在，则使用formchk生成
            formchk_command = f"formchk {chk_path} {fchk_path}"
            try:
                subprocess.run(formchk_command, shell=True, check=True)
            except subprocess.CalledProcessError as e:
                msg = f"Failed to convert chk to fchk: {e}"
                logger.error(msg)
                raise RuntimeError(msg)

        # 3. 解析fchk文件
        return cls.parse_from_fchk_file(fchk_path)


class G16(Task):
    params: Params
    structure: Structure

    def pre_check(self) -> bool:
        # 检查任务是否有效,文件依赖是否存在等
        result = subprocess.run(
            "which g16", shell=True, check=True, capture_output=True, text=True
        )
        g16_path = result.stdout.strip()
        logger.info(f"Found g16 at: {g16_path}")
        print(f"Found g16 at: {g16_path}")
        return True

    def update_state_log(self, new_msg: str):
        log_dir = Path(f"{workspace}/tasks/{self.id}")
        log_dir.mkdir(parents=True, exist_ok=True)
        with open(Path(log_dir, "task.state"), "a") as f:
            f.write(f"{datetime.now().strftime('%Y%m%d-%H%M%S')}: {new_msg}\n")

    def gen_input_content(self) -> str:
        key_word_str = self.params.to_str_lines()
        structure_str = self.structure.to_str_lines()
        content = key_word_str + "\n" + structure_str + "\n"
        return content

    def gen_input_file(self):
        self.update_state_log("Generating g16 input file...")
        content = self.gen_input_content()

        input_dir = Path(f"{workspace}/tasks/{self.id}")
        input_dir.mkdir(parents=True, exist_ok=True)  # 确保目录存在
        with open(Path(input_dir, "g16.input"), "w") as f:
            f.write(content)
        return True

    def run_g16(self):
        work_dir = f"{workspace}/tasks/{self.id}"
        command = f"g16 < {work_dir}/g16.input > {work_dir}/g16.log"
        try:
            self.update_state_log("Running g16 calculation...")
            subprocess.run(command, shell=True, check=True)
            self.update_state_log("g16 calculation finished.")
            logger.info("g16 calculation finished.")
        except subprocess.CalledProcessError as e:
            msg = f"Failed to run g16: {e}"
            logger.error(msg)
            self.update_state_log(msg)
            raise RuntimeError(msg)
        return True

    def init_structure(self):
        if self.structure:
            return

        # 按"smi", "sdf", "mol", "xyz", "chk", "fchk"的文件后缀顺序, 获取input_file中的结构文件路径
        suffix_list = list(structure_file_suffix.__args__)
        struct_files = [i for i in self.input_file if i.split(".")[-1] in suffix_list]
        if len(struct_files) == 0:
            msg = f"Failed to get structure file from input_file: {self.input_file}"
            logger.error(msg)
            raise ValueError(msg)

        struct_file_path = Path(struct_files[0])
        suffix = struct_file_path.suffix[1:]
        if not struct_file_path.exists():
            msg = f"Structure file not found: {struct_file_path}"
            logger.error(msg)
            raise FileNotFoundError(msg)

        if suffix in ["smi", "sdf", "mol"]:
            self.structure = Structure.parse_from_rdkit(path=struct_file_path)
        elif suffix == "xyz":
            self.structure = Structure.parse_from_xyz_file(struct_file_path)
        elif suffix == "chk":
            self.structure = Structure.parse_from_chk_file(struct_file_path)
        elif suffix == "fchk":
            self.structure = Structure.parse_from_fchk_file(struct_file_path)

    # @model_validator(mode="after")
    # def model_post_init(self) -> Self:
    #     self.init_structure()
    #     return self


def main():
    parser = argparse.ArgumentParser(description="Gaussian 16 calculation runner")
    parser.add_argument("config", help="Input file path, default is config.json")
    args = parser.parse_args()

    task_config = Path(args.config if args.config else "config.json")
    if not task_config.exists():
        raise FileNotFoundError(f"Gaussian 16 config file not found: {task_config}")

    with open(task_config, "r") as f:
        task = json.load(f)

    g16_task = G16(**task)
    g16_task.pre_check()
    g16_task.init_structure()
    g16_task.gen_input_file()
    g16_task.run_g16()
