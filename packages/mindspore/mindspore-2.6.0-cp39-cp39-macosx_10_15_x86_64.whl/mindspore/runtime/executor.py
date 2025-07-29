# Copyright 2024 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

"""Executor manager interfaces."""
from mindspore._c_expression import RuntimeConf
from mindspore.runtime.thread_bind_core import _get_cpu_affinity_policy
from mindspore._checkparam import args_type_check
from mindspore import _checkparam as Validator
from mindspore import log as logger



def launch_blocking():
    """
    Indicates that synchronizing the execution of the startup device reduces the execution performance of the program.

    - In the initial state when this interface is not called, the operator executes asynchronously on the device.
      In this case, when an error occurs in the execution of the operator,
      it will not be possible to locate the position of the particular error script code.
    - When this interface is called, the operator is executed in a synchronized manner on the device.
      At this point, when an error occurs in the execution of the operator,
      the location of the erroneous script code can be located based on the error call stack.

    Examples:
        >>> import mindspore as ms
        >>> ms.set_device("Ascend", 1)
        >>> ms.runtime.launch_blocking()
    """
    return RuntimeConf.get_instance().set_launch_blocking()


@args_type_check(threads_num=int)
def dispatch_threads_num(threads_num):
    """
    Set the threads number of runtime used.

    The framework set the runtime number of threads are 5 by default.

    Args:
        threads_num (int): The threads number of runtime used.

    Examples:
        >>> import mindspore as ms
        >>> ms.set_device("Ascend", 1)
        >>> ms.runtime.dispatch_threads_num(6)
    """
    if RuntimeConf.get_instance().is_dispatch_threads_num_configured():
        raise RuntimeError("The 'dispatch_threads_num' can not be set repeatedly.")

    threads_num = Validator.check_positive_int(threads_num, "threads_num")

    return RuntimeConf.get_instance().set_dispatch_threads_num(threads_num)


@args_type_check(enable_affinity=bool, affinity_cpu_list=dict)
def set_cpu_affinity(enable_affinity, affinity_cpu_list=None):
    """
    Enable thread-level core binding to assign specific CPU cores to MindSpore's main modules (main thread, pynative,
    runtime, minddata), to prevent unstable performance caused by MindSpore's threads seizing CPU.

    Note:
        - Provides two binding modes: 1. Automatically generates binding policies based on available CPUs, NUMA nodes,
          and device resources in the environment to bind cores at thread level. 2. Thread-level bonding based on
          customized bonding policies passed in by `affinity_cpu_list`.

        - The automated bind-core policy generation scenario invokes system commands to obtain CPU, NUMA node, and
          device resources on the environment, and some commands cannot be executed successfully due to environment
          differences; the automated bind-core policy generated will vary according to the resources available on the
          environment:

          1. `cat /sys/fs/cgroup/cpuset/cpuset.cpus`, to obtain the available CPU resources on the environment; if the
             execution of this command fails, the bind-core function will not take effect.
          2. `npu-smi info -m`, get the available NPU resources on the environment; if the execution of this command
             fails, the bind-core policy will be generated only based on the available CPU resources,
             without considering the device affinity.
          3. `npu-smi info -t board -i {NPU_ID} -c {CHIP_ID}`, get NPU details based on the logical ID of the device;
             if the execution of this command fails, the bind-core policy is generated based on the available CPU
             resources only, regardless of device affinity.
          4. `lspci -s {PCIe_No} -vvv`, get the hardware information of the device on the environment; if the execution
             of this command fails, the bind-core policy is generated only based on the available CPU resources,
             without considering the device affinity.
          5. `lscpu`, get information about CPUs and NUMA nodes on the environment; if the execution of this command
             fails, only the available CPU resources are used to generate the bind-core policy, without considering
             the device affinity.

    Args:
        enable_affinity (bool): Switches on/off thread-level core binding.
        affinity_cpu_list (dict, optional): Specifies a customized bind-core policy. The key to be passed
            into the dict needs to be in string ``"deviceX"`` format, and the value needs to be in list
            ``["cpuidX-cpuidY"]`` format. Default: ``None``, i.e., use the bind-core policy generated automatically
            based on the environment. It is allowed to pass the empty dict ``{}``, in which case the bind-core
            policy generated automatically based on the environment will be used.

    Raises:
        TypeError: The parameter `enable_affinity` is not a boolean.
        TypeError: The parameter `affinity_cpu_list` is neither a dictionary nor a ``None``.
        ValueError: The key of parameter `affinity_cpu_list` is not a string.
        ValueError: The key of parameter `affinity_cpu_list` is not in ``"deviceX"`` format.
        ValueError: The parameter `affinity_cpu_list` has a value that is not a list.
        ValueError: The element in value of parameter `affinity_cpu_list` is not a string.
        ValueError: The element in value for parameter `affinity_cpu_list` does not match ``["cpuidX-cpuidY"]``.
        RuntimeError: Automatically generated binding policy or customized binding policy scenario where the number
            of CPU cores assigned to each device is less than 7.
        RuntimeError: A custom-specified binding policy scenario where the CPU assigned to a device is not
            available in the environment.
        RuntimeError: The `mindspore.runtime.set_cpu_affinity` API is called repeatedly.

    Examples:
        >>> import mindspore as ms
        >>> ms.set_device("Ascend", 1)
        >>> ms.runtime.set_cpu_affinity(True)
        >>>
        >>> import mindspore as ms
        >>> ms.set_device("Ascend", 1)
        >>> ms.runtime.set_cpu_affinity(True, {"device0":["0-9"],"device1":["10-15","20-29"],"device2":["35-45"]})
    """
    if RuntimeConf.get_instance().is_thread_bind_core_configured():
        raise RuntimeError("The 'mindspore.runtime.set_cpu_affinity' cannot be set repeatedly.")
    if enable_affinity:
        module_bind_core_policy, bind_policy_flag = _get_cpu_affinity_policy(affinity_cpu_list)
        if not module_bind_core_policy:
            logger.warning("set_cpu_affinity is not enabled because the environment does not meet the "
                           "basic conditions for binding core.")
            RuntimeConf.get_instance().set_thread_bind_core_configured()
            return
        if bind_policy_flag:
            RuntimeConf.get_instance().thread_bind_core_with_policy(module_bind_core_policy)
        else:
            RuntimeConf.get_instance().thread_bind_core(module_bind_core_policy)
    else:
        RuntimeConf.get_instance().set_thread_bind_core_configured()
        return


@args_type_check(thread_num=int, kernel_group_num=int)
def set_kernel_launch_group(thread_num=2, kernel_group_num=8):
    """
    O0 mode supports operator batch parallel delivery interface, supports enabling
    parallel delivery, and configures parallel number.

    Args:
        thread_num (int, optional): The number of concurrent threads, generally not recommended
            to increase. The `thread_num` and the number of threads configured by the existing interface
            mindspore.runtime.dispatch_threads_num are independent of each other. Default value is ``2``.
        kernel_group_num (int, optional): Total number of operator groups,
            kernel_group_num/thread_num groups per thread. Default value is ``8``.

    Examples:
        >>> import mindspore as ms
        >>> ms.runtime.set_kernel_launch_group(thread_num=2, kernel_group_num=8)
    """
    if RuntimeConf.get_instance().is_kernel_launch_group_configured():
        raise RuntimeError("The 'kernel_launch_group' can not be set repeatedly.")

    if thread_num < 1:
        raise ValueError(f"The value of thread_num should be at least 1, but got {thread_num}")

    if kernel_group_num < 1:
        raise ValueError(f"The value of kernel_group_num should be at least 1, but got {kernel_group_num}")

    if (kernel_group_num % thread_num) != 0:
        raise ValueError(f"Invalid parameter value, kernel_group_num: {kernel_group_num} cannot "
                         f"be evenly divisible by thread_num: {thread_num}")

    return RuntimeConf.get_instance().set_kernel_launch_group(thread_num, kernel_group_num)
