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

tensor_cpp_methods = ['inverse', 'log2', 'log', 'eq', 'addmm', 'gcd', 'masked_select', 'std', 'histc', 'chunk', 'atan', 'arctan', 'floor_divide', 'isfinite', 'neg', 'negative', 'view_as', 'scatter', 'prod', 'cumsum', 'sqrt', 'frac', 'masked_fill_', 'logical_not', 'reshape', 'argmax', 'round', 'greater', 'gt', 'addcdiv', 'all', 'exp_', 'any', 'cos', 'sub_', '__isub__', 'select', 'var', 'div_', '__itruediv__', 'pow', '__pow__', 'clone', 'hardshrink', 'add', '__add__', 'less_equal', 'le', 'minimum', 'ceil', 'expm1', 'max', 'remainder', 'put_', 'atanh', 'arctanh', 'logaddexp2', 't', 'asinh', 'arcsinh', 'square', 'greater_equal', 'ge', 'logaddexp', 'triu', 'diag', 'baddbmm', 'topk', 'tril', 'not_equal', 'ne', 'where', 'scatter_add', 'fill_diagonal_', 'sort', 'mean', 'count_nonzero', 'isclose', 'tanh', 'tan', 'sinh', 'bitwise_and', '__and__', 'copy_', 'sub', '__sub__', 'dot', 'div', 'divide', 'sum', 'lerp', 'expand_as', 'narrow', 'reciprocal', 'isneginf', 'less', 'lt', 'fill_', 'logical_xor', 'matmul', 'fmod', 'isinf', 'type_as', 'logsumexp', '_to', 'asin', 'arcsin', 'repeat', 'unbind', 'xlogy', 'abs', 'absolute', '__abs__', 'true_divide', 'transpose', 'sinc', 'outer', 'scatter_', 'floor', 'split', 'tile', 'nan_to_num', 'cosh', 'mm', 'erfc', 'clamp', 'clip', 'unsqueeze', 'index_select', 'kthvalue', 'mul_', '__imul__', 'unique', 'argsort', 'acosh', 'arccosh', 'exp', 'subtract', 'index_add', 'roll', 'sigmoid', 'bitwise_not', 'masked_fill', 'log10', 'bitwise_xor', '__xor__', 'new_ones', 'bitwise_or', '__or__', 'new_zeros', 'log1p', 'gather', 'min', 'add_', '__iadd__', 'addbmm', 'argmin', 'nansum', 'atan2', 'arctan2', 'trunc', 'rsqrt', 'log_', 'mul', 'erf', 'bincount', 'acos', 'arccos', 'repeat_interleave', 'allclose', 'logical_and', 'logical_or', 'sin', 'maximum', 'median', 'take', 'flatten', 'addmv', 'floor_divide_', '__ifloordiv__']
