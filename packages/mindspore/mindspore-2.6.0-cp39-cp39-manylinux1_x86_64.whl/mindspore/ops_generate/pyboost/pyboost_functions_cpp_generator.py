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
"""
This module defines the PyboostFunctionsGenerator class for generating C++ functions for PyBoost operations.

The generator processes operator prototypes and constructs the necessary function definitions, including
conversions for optional parameters and tensor arguments. It generates the registration code and includes
the necessary header files for the generated functions.
"""

import os

import common.template as template
import common.gen_constants as K
from common.template import Template
from common.gen_utils import save_file
from common.op_proto import OpProto
from common.base_generator import BaseGenerator
from pyboost import pyboost_utils
from pyboost.pyboost_utils import get_convert_type_str, is_optional_param, is_op_multi_output, get_input_args_type_str, is_tensor_list

from .op_template_parser import OpTemplateParser


class PyboostFunctionsGenerator(BaseGenerator):
    """
    Generates PyBoost functions based on operator prototypes.

    This class processes operator prototypes (`op_protos`) to create the necessary C++ function definitions for
    PyBoost operations. It constructs function bodies, handles optional value conversions, and generates
    registration code and header inclusions.
    """

    def __init__(self):
        """Initializes the PyboostFunctionsGenerator with the necessary templates."""
        self.pyboost_func_include_header_template = Template(
            f'#include "{K.MS_PYBOOST_BASE_PATH}/auto_generate/${{operator_name}}.h"\n'
        )
        self.convert_optional_to_value_template = Template(
            "auto ${output} = PyNativeAlgo::PyBoost::OptionalToValue(${input});\n"
        )
        self.convert_to_tensor_template = Template(
            'auto ${output} = PyNativeAlgo::Common::ConvertStubNodeToTensor(${input}, ${need_contiguous}, '
            'op_run_info->requires_grad);\n'
        )
        self.convert_to_tensor_list_template = Template(
            'auto ${output} = PyNativeAlgo::Common::ConvertStubNodeToValueTuple(${input}, ${need_contiguous}, '
            'op_run_info->requires_grad);\n'
        )
        self.convert_template = Template("auto $arg_name = converter.${convert_func}(args, $arg_index);\n")
        self.input_args_template = Template(" const ${arg_type}& ${arg_name},")
        self.PYBOOST_FUNCTION_TEMPLATE = template.PYBOOST_FUNCTION_TEMPLATE
        self.PYBOOST_COMM_FUNCTION_TEMPLATE = template.PYBOOST_COMM_FUNCTION_TEMPLATE
        self.PYBOOST_FUNCTION_DYNAMIC_OUTPUT_TEMPLATE = template.PYBOOST_FUNCTION_DYNAMIC_OUTPUT_TEMPLATE
        self.REGISTER_DEFINE_TEMPLATE = template.REGISTER_DEFINE_TEMPLATE
        self.REGISTER_TEMPLATE = template.REGISTER_TEMPLATE
        self.PYBOOST_HEADER_TEMPLATE = template.PYBOOST_FUNCTIONS_CC_TEMPLATE
        self.TENSOR_FUNC_CLASS_REG = template.TENSOR_FUNC_CLASS_REG
        self.OP_DEF_INC_HEAD_TEMPLATE = template.OP_DEF_INC_HEAD_TEMPLATE

    def generate(self, work_path, op_protos):
        """
        Generates the C++ PyBoost functions and writes them to the specified files.

        This method processes a list of operator prototypes (`op_protos`), extracting necessary information
        such as operator names, arguments, and conversion types. It constructs the function definitions, includes,
        and registration code. The generated content is saved to the specified path as a C++ source file.

        Args:
            work_path (str): The file path where the generated files will be saved.
            op_protos (list): A list of operator prototypes containing information about the operators to be processed.

        Returns:
            None
        """
        pyboost_func_str = ''
        pyboost_func_pybind_def = ''
        pyboost_func_include_headers_str = ''
        ops_inc_head_set = set()
        for op_proto in op_protos:
            if op_proto.op_dispatch is None or not op_proto.op_dispatch.enable:
                continue
            op_parser = OpTemplateParser(op_proto)
            op_pyboost_func_name = op_parser.get_pyboost_func_name()
            op_def_name_str = op_parser.get_op_def_name_str()
            type_num, same_type = op_parser.gen_signature_same_type_table()
            parser_body_str = self._generate_parser_func(op_proto)
            op_args_str = [op_arg.arg_name for op_arg in op_proto.op_args]
            convert_stub_str = self._get_convert_stub_str(op_proto)
            optional_to_value_str = self._get_optional_to_value_str(op_proto)
            call_args_str = self._get_call_args_str(op_proto)
            grad_args_str = self._get_grad_args_str(op_proto)
            cast_args_str = self._get_cast_to_value_str(op_proto)
            view_arg_str = self._get_first_str(op_proto.op_view, grad_args_str)
            op_input_args_str = self._get_input_args_str(op_proto)
            view_arg_str = ", " + view_arg_str if view_arg_str else ''
            multi_ouptut_str = 'Multi' if is_op_multi_output(op_proto.op_returns) else ''
            output_num_str = len(op_proto.op_returns)
            function_tpl = self._get_function_tpl(op_proto)
            pyboost_func_str += function_tpl.replace(func_name=op_pyboost_func_name,
                                                     op_def_name=op_def_name_str,
                                                     type_num=type_num,
                                                     same_type=same_type,
                                                     input_args=op_input_args_str,
                                                     parser_body=parser_body_str,
                                                     op_name=op_proto.op_class.name,
                                                     class_name=op_proto.op_class.name,
                                                     op_args=op_args_str,
                                                     convert_stub=convert_stub_str,
                                                     optional_to_value=optional_to_value_str,
                                                     call_args=call_args_str,
                                                     grad_args=grad_args_str,
                                                     cast_args=cast_args_str,
                                                     view_arg=view_arg_str,
                                                     is_multi=multi_ouptut_str,
                                                     output_num=output_num_str,
                                                     operator_name=op_proto.op_name)
            pyboost_func_str = pyboost_func_str + template.NEW_LINE + template.NEW_LINE
            pyboost_op_name = op_parser.get_pyboost_name()
            pyboost_func_name = op_parser.get_pyboost_func_name()
            pyboost_func_pybind_def += self.REGISTER_DEFINE_TEMPLATE.replace(
                pyboost_op_name=pyboost_op_name,
                pyboost_cfunc_name=pyboost_func_name,
                class_name=op_proto.op_class.name)
            pyboost_func_include_headers_str += self.pyboost_func_include_header_template.replace(
                operator_name=op_proto.op_name)
            ops_inc_head_set.add(self.OP_DEF_INC_HEAD_TEMPLATE.replace(prefix_char=op_proto.op_class.name[0].lower()))
        register_func_str = self.REGISTER_TEMPLATE.replace(register_func=pyboost_func_pybind_def)
        function_class_register = self._get_function_class_register(op_protos)
        pyboost_func_file = self.PYBOOST_HEADER_TEMPLATE.replace(ops_inc=list(sorted(ops_inc_head_set)),
                                                                 include_op_header=pyboost_func_include_headers_str,
                                                                 function_body=pyboost_func_str,
                                                                 register_function_body=register_func_str,
                                                                 function_class_register=function_class_register)
        save_path = os.path.join(work_path, K.PIPELINE_PYBOOST_FUNC_GEN_PATH)
        file_name = "pyboost_functions.cc"
        save_file(save_path, file_name, pyboost_func_file)

    def _get_cast_args_with_type_str(self, op_proto, cast_args_str):
        args_with_type = []
        for op_arg, cast_args_name in zip(op_proto.op_args, cast_args_str):
            input_dtype = get_input_dtype(op_arg.arg_dtype, is_optional_param(op_arg))
            args_with_type.append("const " + input_dtype + " &" + cast_args_name)
        return list(args_with_type)

    def _get_function_class_register(self, op_protos) -> str:
        """
        Generates a function class registration string for tensor functions.

        Args:
            op_protos (list): A list of tensor op prototypes.

        Returns:
            str: A concatenated string representing the registration information for tensor
                 function classes.
        """
        function_class_register = ''
        for op_proto in op_protos:
            if op_proto.op_dispatch is None or not op_proto.op_dispatch.enable:
                continue
            class_name, op_name = op_proto.op_class.name, op_proto.op_name
            function_class_register += self.TENSOR_FUNC_CLASS_REG.replace(class_name=class_name,
                                                                          op_name=op_name)
        return function_class_register

    def _generate_parser_func(self, op_proto: OpProto) -> str:
        """
        Generates the parsing function for the operator's arguments.

        This method constructs the code for converting each argument in the operator prototype to its appropriate
        type, handling optional parameters as necessary.

        Args:
            op_proto (OpProto): The operator prototype containing the argument information.

        Returns:
            str: The generated parsing function code as a string.
        """
        parser_func_str = ''
        for index, op_arg in enumerate(op_proto.op_args):
            is_optional = is_optional_param(op_arg)
            if op_arg.is_type_id:
                convert_type_str = get_convert_type_str('type', is_optional)
            else:
                convert_type_str = get_convert_type_str(op_arg.arg_dtype, is_optional)

            parser_func_str += self.convert_template.replace(arg_name=op_arg.arg_name, convert_func=convert_type_str,
                                                             arg_index=pyboost_utils.get_index(index))
        return parser_func_str


    def _get_input_args_str(self, op_proto: OpProto) -> str:
        """
        Generates the input arguments list for the pyboost operator.

        Args:
            op_proto (OpProto): The operator prototype containing the argument information.

        Returns:
            str: The generated input arguments list as a string.
        """
        parser_func_str = ''
        for _, op_arg in enumerate(op_proto.op_args):
            is_optional = is_optional_param(op_arg)
            if op_arg.is_type_id:
                arg_type_str = get_input_args_type_str('type', is_optional)
            else:
                arg_type_str = get_input_args_type_str(op_arg.arg_dtype, is_optional)
            parser_func_str += self.input_args_template.replace(arg_name=op_arg.arg_name, arg_type=arg_type_str)
        return parser_func_str[:-1]


    def _get_convert_stub_str(self, op_proto: OpProto):
        """
        Generates the conversion stub code for the operator's arguments.

        This method creates code for converting operator arguments to tensor format, depending on whether they
        are view operations or standard tensor operations.

        Args:
            op_proto (OpProto): The operator prototype containing the argument information.

        Returns:
            str: The generated conversion stub code as a string.
        """
        convert_stub_str = ''
        need_contiguous = 'true'
        if op_proto.op_view:
            # View/ACLNN op does not need to convert to contiguous tensor.
            need_contiguous = 'false'
        for op_arg in op_proto.op_args:
            if pyboost_utils.is_tensor(op_arg):
                convert_stub_output_name = op_arg.arg_name + '_optional' if is_optional_param(op_arg) \
                    else op_arg.arg_name + "_tensor"
                convert_stub_str += self.convert_to_tensor_template.replace(input=op_arg.arg_name,
                                                                            output=convert_stub_output_name,
                                                                            need_contiguous=need_contiguous)
            elif pyboost_utils.is_tensor_list(op_arg):
                # To adapt the cases where TensorList is optional.
                convert_stub_output_name = op_arg.arg_name + '_optional' if is_optional_param(op_arg) \
                    else op_arg.arg_name + "_tensor_list"
                convert_stub_str += self.convert_to_tensor_list_template.replace(input=op_arg.arg_name,
                                                                                 output=convert_stub_output_name,
                                                                                 need_contiguous=need_contiguous)
        return convert_stub_str

    def _get_optional_to_value_str(self, op_proto: OpProto):
        """
        Generates the code for converting optional arguments to their corresponding values.

        This method constructs code to handle optional arguments and converts them to their actual values,
        ensuring proper handling for tensors and lists.

        Args:
            op_proto (OpProto): The operator prototype containing the argument information.

        Returns:
            str: The generated code for converting optional arguments to values as a string.
        """
        optional_to_value_str = ''
        for op_arg in op_proto.op_args:
            if is_optional_param(op_arg):
                if pyboost_utils.is_tensor(op_arg) or pyboost_utils.is_tensor_list(op_arg):
                    convert_stub_output_name = op_arg.arg_name + '_optional'
                    cast_output = 'cast_' + convert_stub_output_name
                    convert_optional_to_value_name = op_arg.arg_name + '_value'
                    optional_to_value_str += \
                        self.convert_optional_to_value_template.replace(input=cast_output,
                                                                        output=convert_optional_to_value_name)
                else:
                    call_arg = op_arg.arg_name
                    convert_optional_to_value_name = op_arg.arg_name + '_value'
                    optional_to_value_str += \
                        self.convert_optional_to_value_template.replace(input=call_arg,
                                                                        output=convert_optional_to_value_name)
        return optional_to_value_str

    def _get_call_args_str(self, op_proto: OpProto):
        """
        Generates the list of call arguments for the operator.

        This method constructs a list of argument names for the function call, adapting the names for
        optional tensors and tensor lists as needed.

        Args:
            op_proto (OpProto): The operator prototype containing the argument information.

        Returns:
            list: A list of formatted argument names for the function call.
        """
        call_args_str = []
        for op_arg in op_proto.op_args:
            if pyboost_utils.is_tensor(op_arg):
                convert_stub_output_name = op_arg.arg_name + '_optional' if is_optional_param(op_arg) \
                    else op_arg.arg_name + "_tensor"
                call_arg = convert_stub_output_name
            elif pyboost_utils.is_tensor_list(op_arg):
                convert_stub_output_name = op_arg.arg_name + '_optional' if is_optional_param(op_arg) \
                    else op_arg.arg_name + "_tensor_list"
                call_arg = convert_stub_output_name
            else:
                call_arg = op_arg.arg_name
            call_args_str.append(call_arg)
        return call_args_str

    def _get_grad_args_str(self, op_proto: OpProto):
        """
        Generates the list of gradient arguments for the operator.

        This method constructs a list of argument names used for computing gradients, adapting for
        optional tensors and tensor lists as necessary.

        Args:
            op_proto (OpProto): The operator prototype containing the argument information.

        Returns:
            list: A list of formatted gradient argument names.
        """
        grad_args_str = []
        for op_arg in op_proto.op_args:
            if pyboost_utils.is_tensor(op_arg):
                grad_arg = op_arg.arg_name + "_value" if is_optional_param(op_arg) else \
                    f"cast_" + op_arg.arg_name + "_tensor"
            elif pyboost_utils.is_tensor_list(op_arg):
                if is_optional_param(op_arg):
                    # To adapt the cases where TensorList is optional.
                    convert_optional_to_value_name = op_arg.arg_name + "_value"
                    grad_arg = convert_optional_to_value_name
                else:
                    convert_stub_output_name = op_arg.arg_name + "_tensor_list"
                    grad_arg = "cast_" + convert_stub_output_name
            else:
                grad_arg = "cast_" + op_arg.arg_name
                if is_optional_param(op_arg):
                    convert_optional_to_value_name = op_arg.arg_name + "_value"
                    grad_arg = convert_optional_to_value_name
            grad_args_str.append(grad_arg)
        return grad_args_str

    def _get_cast_to_value_str(self, op_proto: OpProto):
        """
        Generates the list of cast arguments for the operator.

        This method constructs a list of argument names that need to be cast to their corresponding types.

        Args:
            op_proto (OpProto): The operator prototype containing the argument information.

        Returns:
            list: A list of formatted cast argument names.
        """
        cast_args_str = []
        for op_arg in op_proto.op_args:
            cast_str = 'cast_'
            if pyboost_utils.is_tensor(op_arg):
                convert_stub_output_name = op_arg.arg_name + '_optional' if is_optional_param(op_arg) \
                    else op_arg.arg_name + "_tensor"
                cast_arg = cast_str + convert_stub_output_name
            elif pyboost_utils.is_tensor_list(op_arg):
                # To adapt the cases where TensorList is optional.
                convert_stub_output_name = op_arg.arg_name + '_optional' if is_optional_param(op_arg) \
                    else op_arg.arg_name + "_tensor_list"
                cast_arg = cast_str + convert_stub_output_name
            else:
                cast_arg = cast_str + op_arg.arg_name
            cast_args_str.append(cast_arg)
        return cast_args_str

    def _get_first_str(self, is_view_or_inplace: bool, grad_args: list):
        """
        Generates the view base str of arguments for the operator.

        This method constructs a list of argument names that need to be cast to their corresponding types.

        Args:
            is_view_or_inplace (bool): Whether the op is view op or inplace op.
            grad_args (list): grad args

        Returns:
            str: Formatted view or inplace first argument names.
        """
        arg_str = ''
        for i, grad_arg in enumerate(grad_args):
            if is_view_or_inplace and i == 0:
                arg_str = grad_arg
                break
        return arg_str


    def _get_function_tpl(self, op_proto: OpProto):
        if len(op_proto.op_returns) == 1 and is_tensor_list(op_proto.op_returns[0]):
            # op output size is unknown
            return self.PYBOOST_FUNCTION_DYNAMIC_OUTPUT_TEMPLATE
        return self.PYBOOST_COMM_FUNCTION_TEMPLATE \
            if op_proto.op_dispatch.is_comm_op else self.PYBOOST_FUNCTION_TEMPLATE
