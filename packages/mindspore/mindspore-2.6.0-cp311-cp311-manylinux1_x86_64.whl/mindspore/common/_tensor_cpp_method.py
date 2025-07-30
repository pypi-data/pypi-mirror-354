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

tensor_cpp_methods = ['narrow', 'trunc', 'log10', 'scatter_', 'unique', 'roll', 'bincount', 'exp_', 'median', 'maximum', 'floor_divide', 'addcdiv', 'acos', 'arccos', 'erfc', 'sinc', 'acosh', 'arccosh', 'view_as', 'nan_to_num', 'true_divide', 'asinh', 'arcsinh', 'remainder', 'transpose', 'put_', 'erf', 'tril', 'split', 'fmod', 'subtract', 'scatter', 'add_', '__iadd__', 'logaddexp2', 'where', 'isinf', 'pow', '__pow__', 'mean', 'all', 'expm1', 'argmin', 'lerp', 'isneginf', 'max', 'log2', 'inverse', 't', 'floor_divide_', '__ifloordiv__', 'mul_', '__imul__', 'masked_select', 'asin', 'arcsin', 'index_select', 'expand_as', 'repeat_interleave', 'new_zeros', 'rsqrt', 'sort', 'cosh', 'tan', 'tanh', 'prod', 'less', 'lt', 'bitwise_and', '__and__', 'atan', 'arctan', 'new_ones', 'xlogy', 'reciprocal', 'logical_and', 'repeat', 'unbind', 'addmv', 'sub', '__sub__', 'masked_fill', 'fill_', 'matmul', 'type_as', 'greater_equal', 'ge', 'hardshrink', 'logical_not', 'frac', 'masked_fill_', 'mul', 'logical_xor', 'neg', 'negative', 'outer', 'mm', 'allclose', 'argsort', 'clone', 'triu', 'log1p', 'dot', 'addbmm', 'gather', 'addmm', 'less_equal', 'le', 'isclose', 'minimum', 'histc', 'square', 'tile', 'copy_', 'diag', 'unsqueeze', 'min', 'log_', 'scatter_add', 'sinh', '_to', 'bitwise_or', '__or__', 'abs', 'absolute', '__abs__', 'any', 'isfinite', 'add', '__add__', 'logsumexp', 'var', 'exp', 'atan2', 'arctan2', 'fill_diagonal_', 'flatten', 'sigmoid', 'cumsum', 'select', 'nansum', 'kthvalue', 'reshape', 'topk', 'take', 'gcd', 'ceil', 'logical_or', 'log', 'sqrt', 'atanh', 'arctanh', 'sub_', '__isub__', 'not_equal', 'ne', 'greater', 'gt', 'eq', 'chunk', 'std', 'baddbmm', 'sin', 'bitwise_not', 'logaddexp', 'bitwise_xor', '__xor__', 'index_add', 'count_nonzero', 'cos', 'round', 'div', 'divide', 'sum', 'div_', '__itruediv__', 'clamp', 'clip', 'floor', 'argmax']
