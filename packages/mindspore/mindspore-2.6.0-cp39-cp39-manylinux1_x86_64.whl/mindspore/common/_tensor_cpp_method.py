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

tensor_cpp_methods = ['logical_not', 'greater_equal', 'ge', 'new_ones', 'gcd', 'tan', 'acosh', 'arccosh', 'chunk', 'trunc', 'round', 'outer', 'log_', 'kthvalue', 'greater', 'gt', 'cos', 'fmod', 'sort', '_to', 'baddbmm', 'log10', 'exp', 'scatter', 'gather', 'allclose', 'argmin', 'matmul', 'sin', 'split', 'fill_diagonal_', 'mm', 'abs', 'absolute', '__abs__', 'subtract', 'masked_fill', 'bitwise_or', '__or__', 'expand_as', 'logsumexp', 'copy_', 'logical_or', 'log1p', 'count_nonzero', 'sinh', 'floor_divide_', '__ifloordiv__', 'take', 't', 'sum', 'all', 'histc', 'xlogy', 'var', 'sqrt', 'repeat_interleave', 'add', '__add__', 'frac', 'logaddexp2', 'tile', 'median', 'view_as', 'tanh', 'new_zeros', 'eq', 'asin', 'arcsin', 'bitwise_and', '__and__', 'acos', 'arccos', 'unsqueeze', 'atan2', 'arctan2', 'square', 'isfinite', 'flatten', 'max', 'addmv', 'remainder', 'nan_to_num', 'mul', 'bitwise_xor', '__xor__', 'div_', '__itruediv__', 'isneginf', 'not_equal', 'ne', 'exp_', 'repeat', 'inverse', 'prod', 'div', 'divide', 'masked_fill_', 'true_divide', 'add_', '__iadd__', 'reciprocal', 'select', 'neg', 'negative', 'atanh', 'arctanh', 'scatter_add', 'logaddexp', 'cumsum', 'scatter_', 'asinh', 'arcsinh', 'less_equal', 'le', 'mean', 'nansum', 'lerp', 'logical_and', 'dot', 'std', 'fill_', 'log2', 'diag', 'reshape', 'narrow', 'transpose', 'tril', 'put_', 'unbind', 'erfc', 'argmax', 'argsort', 'floor', 'log', 'triu', 'unique', 'roll', 'maximum', 'masked_select', 'clamp', 'clip', 'index_select', 'bincount', 'any', 'less', 'lt', 'ceil', 'sinc', 'minimum', 'atan', 'arctan', 'addbmm', 'min', 'mul_', '__imul__', 'clone', 'erf', 'rsqrt', 'topk', 'sub_', '__isub__', 'index_add', 'type_as', 'floor_divide', 'isinf', 'addmm', 'hardshrink', 'expm1', 'where', 'bitwise_not', 'sigmoid', 'pow', '__pow__', 'addcdiv', 'cosh', 'sub', '__sub__', 'isclose', 'logical_xor']
