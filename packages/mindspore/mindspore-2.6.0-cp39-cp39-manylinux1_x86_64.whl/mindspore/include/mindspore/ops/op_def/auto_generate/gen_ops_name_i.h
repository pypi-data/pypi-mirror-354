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
constexpr auto kNameInplaceElu = "InplaceElu";
constexpr auto kNameInplaceFloorDivide = "InplaceFloorDivide";
constexpr auto kNameInplaceIndexPut = "InplaceIndexPut";
constexpr auto kNameInnerCommIrecv = "InnerCommIrecv";
constexpr auto kNameInnerNonZero = "InnerNonZero";
constexpr auto kNameIHFFT = "IHFFT";
constexpr auto kNameInplaceDivs = "InplaceDivs";
constexpr auto kNameInplaceZero = "InplaceZero";
constexpr auto kNameInplaceFillScalar = "InplaceFillScalar";
constexpr auto kNameIsInf = "IsInf";
constexpr auto kNameInplaceScatterValueReduce = "InplaceScatterValueReduce";
constexpr auto kNameIdentity = "Identity";
constexpr auto kNameIFFT = "IFFT";
constexpr auto kNameInplaceMuls = "InplaceMuls";
constexpr auto kNameInplaceHardtanh = "InplaceHardtanh";
constexpr auto kNameIRFFTN = "IRFFTN";
constexpr auto kNameInnerInplaceIndexPut = "InnerInplaceIndexPut";
constexpr auto kNameInplaceDivMods = "InplaceDivMods";
constexpr auto kNameInplaceTanh = "InplaceTanh";
constexpr auto kNameIHFFT2 = "IHFFT2";
constexpr auto kNameInplaceNormal = "InplaceNormal";
constexpr auto kNameIFFTN = "IFFTN";
constexpr auto kNameInplaceClampScalar = "InplaceClampScalar";
constexpr auto kNameInnerIndex = "InnerIndex";
constexpr auto kNameInplaceScatterAdd = "InplaceScatterAdd";
constexpr auto kNameInplaceIndexAddExt = "InplaceIndexAddExt";
constexpr auto kNameInplaceCopy = "InplaceCopy";
constexpr auto kNameInplaceLog = "InplaceLog";
constexpr auto kNameIndexSelect = "IndexSelect";
constexpr auto kNameInplaceAddExt = "InplaceAddExt";
constexpr auto kNameInnerCommReduceScatter = "InnerCommReduceScatter";
constexpr auto kNameInplaceRandom = "InplaceRandom";
constexpr auto kNameInplaceReLU = "InplaceReLU";
constexpr auto kNameInnerCommAllReduce = "InnerCommAllReduce";
constexpr auto kNameInplaceScatterValue = "InplaceScatterValue";
constexpr auto kNameInplaceDiv = "InplaceDiv";
constexpr auto kNameInplaceGroupedMatmulAdd = "InplaceGroupedMatmulAdd";
constexpr auto kNameInnerCommAllGather = "InnerCommAllGather";
constexpr auto kNameInplacePut = "InplacePut";
constexpr auto kNameInplaceErfinv = "InplaceErfinv";
constexpr auto kNameInplaceMaskedFillTensor = "InplaceMaskedFillTensor";
constexpr auto kNameIFFTShift = "IFFTShift";
constexpr auto kNameInplaceFillTensor = "InplaceFillTensor";
constexpr auto kNameIncreFlashAttention = "IncreFlashAttention";
constexpr auto kNameInplaceSubExt = "InplaceSubExt";
constexpr auto kNameIRFFTDouble = "IRFFTDouble";
constexpr auto kNameInplaceStopGradient = "InplaceStopGradient";
constexpr auto kNameInplaceFloor = "InplaceFloor";
constexpr auto kNameInplaceUniform = "InplaceUniform";
constexpr auto kNameInplaceThreshold = "InplaceThreshold";
constexpr auto kNameInplaceScatterSrc = "InplaceScatterSrc";
constexpr auto kNameIm2ColExt = "Im2ColExt";
constexpr auto kNameInplaceClampTensor = "InplaceClampTensor";
constexpr auto kNameIHFFTN = "IHFFTN";
constexpr auto kNameInplaceMul = "InplaceMul";
constexpr auto kNameInplaceFloorDivides = "InplaceFloorDivides";
constexpr auto kNameIsFinite = "IsFinite";
constexpr auto kNameInplaceFillDiagonal = "InplaceFillDiagonal";
constexpr auto kNameIFFT2 = "IFFT2";
constexpr auto kNameInnerCommAllToAllV = "InnerCommAllToAllV";
constexpr auto kNameIsNegInf = "IsNegInf";
constexpr auto kNameInnerCommIsend = "InnerCommIsend";
constexpr auto kNameInsertGemV2InBackward = "InsertGemV2InBackward";
constexpr auto kNameInplaceDivMod = "InplaceDivMod";
constexpr auto kNameIndexAddExt = "IndexAddExt";
constexpr auto kNameInplaceAddmm = "InplaceAddmm";
constexpr auto kNameInplaceSubScalar = "InplaceSubScalar";
constexpr auto kNameIndex = "Index";
constexpr auto kNameIndexFillTensor = "IndexFillTensor";
constexpr auto kNameIDCTN = "IDCTN";
constexpr auto kNameIDCT = "IDCT";
constexpr auto kNameIndexFillScalar = "IndexFillScalar";
constexpr auto kNameIsClose = "IsClose";
constexpr auto kNameIRFFT2 = "IRFFT2";
constexpr auto kNameInplaceScatterSrcReduce = "InplaceScatterSrcReduce";
constexpr auto kNameInplaceExp = "InplaceExp";
constexpr auto kNameInplaceMaskedFillScalar = "InplaceMaskedFillScalar";
constexpr auto kNameIRFFT = "IRFFT";
constexpr auto kNameInplaceAddsExt = "InplaceAddsExt";
constexpr auto kNameInplaceExponential = "InplaceExponential";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_I_H_
