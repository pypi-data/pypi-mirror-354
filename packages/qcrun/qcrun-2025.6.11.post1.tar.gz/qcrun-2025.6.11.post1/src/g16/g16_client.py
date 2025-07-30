from task import Task
from pathlib import Path
from .g16_struct import Params, Structure


class G16(Task):
    params: Params
    structure: Structure

    def gen_input_content(self) -> str:
        key_word_str = self.params.to_str_lines()
        structure_str = self.structure.to_str_lines()
        return key_word_str + "\n" + structure_str + "\n"

