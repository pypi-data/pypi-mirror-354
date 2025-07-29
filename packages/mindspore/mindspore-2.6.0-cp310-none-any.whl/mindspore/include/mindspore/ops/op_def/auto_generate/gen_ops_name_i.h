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
#ifndef MINDSPORE_CORE_OP_NAME_I_H_
#define MINDSPORE_CORE_OP_NAME_I_H_

namespace mindspore::ops {
constexpr auto kNameIndexSelect = "IndexSelect";
constexpr auto kNameInplaceGroupedMatmulAdd = "InplaceGroupedMatmulAdd";
constexpr auto kNameInplaceRandom = "InplaceRandom";
constexpr auto kNameInnerCommAllGather = "InnerCommAllGather";
constexpr auto kNameInplaceAddmm = "InplaceAddmm";
constexpr auto kNameInplaceSubExt = "InplaceSubExt";
constexpr auto kNameInplaceFillDiagonal = "InplaceFillDiagonal";
constexpr auto kNameInplaceDiv = "InplaceDiv";
constexpr auto kNameIsNegInf = "IsNegInf";
constexpr auto kNameInnerInplaceIndexPut = "InnerInplaceIndexPut";
constexpr auto kNameInplaceStopGradient = "InplaceStopGradient";
constexpr auto kNameInplaceExp = "InplaceExp";
constexpr auto kNameInplaceScatterSrc = "InplaceScatterSrc";
constexpr auto kNameIDCTN = "IDCTN";
constexpr auto kNameInplaceMul = "InplaceMul";
constexpr auto kNameInplaceScatterValue = "InplaceScatterValue";
constexpr auto kNameIFFTShift = "IFFTShift";
constexpr auto kNameInplaceAddsExt = "InplaceAddsExt";
constexpr auto kNameInplaceIndexAddExt = "InplaceIndexAddExt";
constexpr auto kNameInplaceScatterSrcReduce = "InplaceScatterSrcReduce";
constexpr auto kNameIHFFT = "IHFFT";
constexpr auto kNameInnerIndex = "InnerIndex";
constexpr auto kNameIndexFillTensor = "IndexFillTensor";
constexpr auto kNameIsInf = "IsInf";
constexpr auto kNameInplaceAddExt = "InplaceAddExt";
constexpr auto kNameInnerCommReduceScatter = "InnerCommReduceScatter";
constexpr auto kNameIm2ColExt = "Im2ColExt";
constexpr auto kNameInplaceZero = "InplaceZero";
constexpr auto kNameInplaceHardtanh = "InplaceHardtanh";
constexpr auto kNameInplaceSubScalar = "InplaceSubScalar";
constexpr auto kNameInplaceMaskedFillScalar = "InplaceMaskedFillScalar";
constexpr auto kNameInplaceFloorDivides = "InplaceFloorDivides";
constexpr auto kNameIRFFT = "IRFFT";
constexpr auto kNameInplaceFillTensor = "InplaceFillTensor";
constexpr auto kNameIndexFillScalar = "IndexFillScalar";
constexpr auto kNameIFFT2 = "IFFT2";
constexpr auto kNameInplaceMaskedFillTensor = "InplaceMaskedFillTensor";
constexpr auto kNameIdentity = "Identity";
constexpr auto kNameInsertGemV2InBackward = "InsertGemV2InBackward";
constexpr auto kNameIndex = "Index";
constexpr auto kNameInplaceTanh = "InplaceTanh";
constexpr auto kNameIDCT = "IDCT";
constexpr auto kNameInplacePut = "InplacePut";
constexpr auto kNameInplaceThreshold = "InplaceThreshold";
constexpr auto kNameInplaceMuls = "InplaceMuls";
constexpr auto kNameIHFFTN = "IHFFTN";
constexpr auto kNameIRFFTDouble = "IRFFTDouble";
constexpr auto kNameInplaceFillScalar = "InplaceFillScalar";
constexpr auto kNameInplaceNormal = "InplaceNormal";
constexpr auto kNameInplaceDivs = "InplaceDivs";
constexpr auto kNameInplaceScatterValueReduce = "InplaceScatterValueReduce";
constexpr auto kNameInplaceDivMod = "InplaceDivMod";
constexpr auto kNameInplaceFloorDivide = "InplaceFloorDivide";
constexpr auto kNameIsClose = "IsClose";
constexpr auto kNameInplaceClampScalar = "InplaceClampScalar";
constexpr auto kNameInplaceDivMods = "InplaceDivMods";
constexpr auto kNameIncreFlashAttention = "IncreFlashAttention";
constexpr auto kNameIFFT = "IFFT";
constexpr auto kNameInnerCommIsend = "InnerCommIsend";
constexpr auto kNameInnerCommIrecv = "InnerCommIrecv";
constexpr auto kNameIFFTN = "IFFTN";
constexpr auto kNameInplaceElu = "InplaceElu";
constexpr auto kNameInnerNonZero = "InnerNonZero";
constexpr auto kNameInplaceErfinv = "InplaceErfinv";
constexpr auto kNameIndexAddExt = "IndexAddExt";
constexpr auto kNameInplaceIndexPut = "InplaceIndexPut";
constexpr auto kNameInplaceScatterAdd = "InplaceScatterAdd";
constexpr auto kNameInplaceCopy = "InplaceCopy";
constexpr auto kNameIRFFTN = "IRFFTN";
constexpr auto kNameInplaceReLU = "InplaceReLU";
constexpr auto kNameIHFFT2 = "IHFFT2";
constexpr auto kNameInplaceLog = "InplaceLog";
constexpr auto kNameInnerCommAllReduce = "InnerCommAllReduce";
constexpr auto kNameInnerCommAllToAllV = "InnerCommAllToAllV";
constexpr auto kNameInplaceFloor = "InplaceFloor";
constexpr auto kNameIRFFT2 = "IRFFT2";
constexpr auto kNameIsFinite = "IsFinite";
constexpr auto kNameInplaceClampTensor = "InplaceClampTensor";
constexpr auto kNameInplaceUniform = "InplaceUniform";
constexpr auto kNameInplaceExponential = "InplaceExponential";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_I_H_
