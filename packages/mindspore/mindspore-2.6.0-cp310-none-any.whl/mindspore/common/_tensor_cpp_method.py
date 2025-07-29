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

tensor_cpp_methods = ['logsumexp', 'repeat_interleave', 'logical_xor', 'new_zeros', 'not_equal', 'ne', 'div_', '__itruediv__', 'addbmm', 'scatter_', 'expand_as', 'neg', 'negative', 'matmul', 'lerp', 'var', 'logical_not', 'cosh', 'scatter', 'tanh', 'mul', 'isneginf', 'all', 'masked_fill_', 'addcdiv', 'triu', 'dot', 'floor_divide_', '__ifloordiv__', 'minimum', 'tan', 'eq', 'isclose', 'less', 'lt', 'histc', 'maximum', 'addmv', 'log10', 'log', 'unbind', 'exp_', 'xlogy', 'sqrt', 'min', 'kthvalue', 'argsort', 'roll', 'trunc', 'sinh', 'diag', 'inverse', 'ceil', 'nan_to_num', 'bitwise_and', '__and__', 'repeat', 'bitwise_xor', '__xor__', 'argmin', 'logaddexp2', 'rsqrt', 'any', 'div', 'divide', 'isinf', 'prod', 'atan', 'arctan', 'masked_fill', 'median', 'gcd', 'sub_', '__isub__', 'expm1', 'reshape', 'remainder', 'less_equal', 'le', 'sigmoid', 'count_nonzero', 'pow', '__pow__', 'baddbmm', 'erf', 'log1p', 'greater_equal', 'ge', 'hardshrink', 'mean', 'topk', 'log2', 'allclose', 'logical_and', 'chunk', 't', 'transpose', 'select', 'greater', 'gt', 'square', 'true_divide', 'sinc', 'sum', 'round', 'isfinite', 'add_', '__iadd__', 'sin', 'add', '__add__', 'flatten', 'logaddexp', 'cumsum', 'sub', '__sub__', 'copy_', 'log_', 'floor_divide', 'atan2', 'arctan2', 'floor', 'scatter_add', 'asin', 'arcsin', 'tile', 'sort', 'acosh', 'arccosh', 'unsqueeze', 'mm', 'exp', 'outer', 'index_add', 'type_as', 'std', 'fill_', 'bitwise_not', 'take', 'put_', 'narrow', 'atanh', 'arctanh', 'abs', 'absolute', '__abs__', 'reciprocal', 'clamp', 'clip', 'masked_select', 'nansum', 'asinh', 'arcsinh', 'mul_', '__imul__', 'frac', 'gather', 'logical_or', 'erfc', 'cos', 'argmax', 'fmod', 'bitwise_or', '__or__', 'split', 'acos', 'arccos', 'where', 'clone', 'unique', '_to', 'view_as', 'bincount', 'subtract', 'new_ones', 'index_select', 'max', 'tril', 'fill_diagonal_', 'addmm']
