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
"""Add tensor cpp methods for stub tensor"""

tensor_cpp_methods = ['fill_diagonal_', 'atan2', 'arctan2', 'sinh', 'scatter', 'ceil', 'addbmm', 'greater_equal', 'ge', 'atan', 'arctan', 'nan_to_num', 'lerp', 'prod', 'median', 'less', 'lt', 'allclose', 'diag', 'xlogy', 'matmul', 'transpose', 'erfc', 'where', 'std', 'logsumexp', 'min', 'select', 'index_select', 'cos', 'scatter_add', 'clone', 'triu', 'isneginf', 'log10', 'sigmoid', 'kthvalue', 'gather', 'new_zeros', 'sum', 'sub', '__sub__', 'pow', '__pow__', 'logical_not', 'take', 'logical_or', 'reshape', 'index_add', 'argsort', 'div', 'divide', 'bincount', 'log_', 'add_', '__iadd__', 'eq', 'tile', 'add', '__add__', 'fmod', 'masked_fill_', 'fill_', 'logical_and', 'neg', 'negative', 'addcdiv', 'expm1', 'split', 'not_equal', 'ne', 't', 'view_as', 'frac', 'masked_fill', 'cumsum', 'chunk', 'isfinite', 'isclose', 'addmm', 'reciprocal', 'tan', 'floor', 'argmax', 'tanh', 'roll', 'gcd', 'maximum', 'baddbmm', 'topk', 'exp_', 'sqrt', 'scatter_', 'acos', 'arccos', 'log2', 'mean', 'copy_', 'sin', 'tril', 'max', 'floor_divide', 'nansum', 'all', 'dot', 'flatten', 'unbind', 'round', 'argmin', 'new_ones', 'minimum', 'square', 'log', 'sort', 'unique', 'sub_', '__isub__', 'logaddexp2', 'exp', 'logical_xor', 'isinf', 'div_', '__itruediv__', 'floor_divide_', '__ifloordiv__', 'remainder', 'asin', 'arcsin', 'put_', 'true_divide', 'mul_', '__imul__', 'bitwise_xor', '__xor__', 'type_as', 'bitwise_and', '__and__', 'trunc', 'greater', 'gt', '_to', 'repeat_interleave', 'masked_select', 'unsqueeze', 'histc', 'outer', 'addmv', 'mul', 'inverse', 'bitwise_not', 'subtract', 'log1p', 'asinh', 'arcsinh', 'any', 'var', 'repeat', 'logaddexp', 'clamp', 'clip', 'erf', 'expand_as', 'less_equal', 'le', 'atanh', 'arctanh', 'narrow', 'rsqrt', 'sinc', 'abs', 'absolute', '__abs__', 'hardshrink', 'mm', 'cosh', 'acosh', 'arccosh', 'count_nonzero', 'bitwise_or', '__or__']
