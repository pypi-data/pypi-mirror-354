# qcrun - 量子化学计算任务自动化工具

![PyPI Version](https://img.shields.io/pypi/v/qcrun.svg)
[在 PyPI 查看](https://pypi.python.org/pypi/qcrun)

一个用于自动化运行 Gaussian 16 和其他量子化学计算的任务调度工具。

## 功能特性

* 支持多种输入格式 (smi/sdf/mol/xyz/chk/fchk)
* 自动结构优化和构象搜索
* 任务状态跟踪和日志记录
* 支持多种计算类型 (基态、激发态、频率计算等)

## 安装

```bash
pip install qcrun
```

## 快速开始

1. **准备配置文件 `config.json`:**

   ```json
   {
       "id": "task_001",
       "params": {
           "method": "b3lyp",
           "basis": "def2svp",
           "nproc": 32,
           "mem": "64GB",
           "td": 3
       },
       "input_file": ["molecule.xyz"]
   }
   ```

2. **运行计算:**

   ```bash
   run_g16 config.json
   ```

## 输入文件支持

| 格式         | 描述             |
| ---------- | -------------- |
| .smi       | SMILES 字符串     |
| .sdf/.mol  | MDL 分子文件       |
| .xyz       | XYZ 坐标文件       |
| .chk/.fchk | Gaussian 检查点文件 |

## 计算参数

通过 `Params` 类配置:

```python
from qcrun.g16_struct import Params

params = Params(
    method="b3lyp",
    basis="def2svp",
    nproc=32,
    mem="64GB",
    td=3  # 激发态计算
)
```


## 许可证

GNU General Public License v3.0

