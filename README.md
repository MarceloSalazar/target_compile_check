### Compile check

Simple script to automate the compile of apps
Optionally detects and compiles for all targets and toolchain

### Usage

#### Compiles all targets and toolchain

```
git clone https://github.com/MarceloSalazar/target_compile_check

mbed import https://github.com/ARMmbed/mbed-os-example-blinky-baremetal
cd mbed-os-example-blinky-baremetal

python ..\target_compile_check\check.py
```

#### Options

```
python ..\target_compile_check\check.py --help
usage: check.py [-h] [-m TARGET] [-t TOOLCHAIN]

Automation script to compile apps for targets/toolchain

optional arguments:
  -h, --help            show this help message and exit
  -m TARGET, --target TARGET
                        Target name
  -t TOOLCHAIN, --toolchain TOOLCHAIN
                        Toolchain name (ARM, GCC_ARM)
```
