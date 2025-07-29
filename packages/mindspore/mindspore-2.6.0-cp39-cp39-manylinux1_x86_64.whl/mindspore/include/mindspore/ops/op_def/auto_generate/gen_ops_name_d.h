/**
 * Copyright 2023-2025 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef MINDSPORE_CORE_OP_NAME_D_H_
#define MINDSPORE_CORE_OP_NAME_D_H_

namespace mindspore::ops {
constexpr auto kNameDistCommAllGatherIntoTensor = "DistCommAllGatherIntoTensor";
constexpr auto kNameDiagonal = "Diagonal";
constexpr auto kNameDistCommGather = "DistCommGather";
constexpr auto kNameDistCommAllGather = "DistCommAllGather";
constexpr auto kNameDistCommBatchIsendIrecv = "DistCommBatchIsendIrecv";
constexpr auto kNameDropoutExt = "DropoutExt";
constexpr auto kNameDistCommReduceScatterTensor = "DistCommReduceScatterTensor";
constexpr auto kNameDiagExt = "DiagExt";
constexpr auto kNameDense = "Dense";
constexpr auto kNameDCTN = "DCTN";
constexpr auto kNameDropout = "Dropout";
constexpr auto kNameDistCommAllReduce = "DistCommAllReduce";
constexpr auto kNameDistCommScatter = "DistCommScatter";
constexpr auto kNameDistCommScatterTensor = "DistCommScatterTensor";
constexpr auto kNameDivs = "Divs";
constexpr auto kNameDistCommIrecv = "DistCommIrecv";
constexpr auto kNameDivMod = "DivMod";
constexpr auto kNameDCT = "DCT";
constexpr auto kNameDropoutGenMaskExt = "DropoutGenMaskExt";
constexpr auto kNameDivMods = "DivMods";
constexpr auto kNameDistCommGatherIntoTensor = "DistCommGatherIntoTensor";
constexpr auto kNameDecoderKVCache = "DecoderKVCache";
constexpr auto kNameDistCommAllToAllVSingle = "DistCommAllToAllVSingle";
constexpr auto kNameDropoutGradExt = "DropoutGradExt";
constexpr auto kNameDistCommReduce = "DistCommReduce";
constexpr auto kNameDot = "Dot";
constexpr auto kNameDiag = "Diag";
constexpr auto kNameDropoutDoMaskExt = "DropoutDoMaskExt";
constexpr auto kNameDistCommBarrier = "DistCommBarrier";
constexpr auto kNameDistCommBroadcast = "DistCommBroadcast";
constexpr auto kNameDistCommAllToAllV = "DistCommAllToAllV";
constexpr auto kNameDistCommIsend = "DistCommIsend";
constexpr auto kNameDistCommReduceScatter = "DistCommReduceScatter";
constexpr auto kNameDiv = "Div";
constexpr auto kNameDynamicQuantExt = "DynamicQuantExt";
constexpr auto kNameDynamicNTK = "DynamicNTK";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_D_H_
