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
constexpr auto kNameInnerInplaceIndexPut = "InnerInplaceIndexPut";
constexpr auto kNameInplaceDivMod = "InplaceDivMod";
constexpr auto kNameInnerCommIrecv = "InnerCommIrecv";
constexpr auto kNameInplaceMul = "InplaceMul";
constexpr auto kNameIdentity = "Identity";
constexpr auto kNameInplaceFillDiagonal = "InplaceFillDiagonal";
constexpr auto kNameInplaceElu = "InplaceElu";
constexpr auto kNameInplaceScatterSrcReduce = "InplaceScatterSrcReduce";
constexpr auto kNameInnerNonZero = "InnerNonZero";
constexpr auto kNameInplaceDivs = "InplaceDivs";
constexpr auto kNameIHFFTN = "IHFFTN";
constexpr auto kNameIRFFT2 = "IRFFT2";
constexpr auto kNameInplaceMuls = "InplaceMuls";
constexpr auto kNameInplaceDiv = "InplaceDiv";
constexpr auto kNameIndexFillTensor = "IndexFillTensor";
constexpr auto kNameInnerCommAllToAllV = "InnerCommAllToAllV";
constexpr auto kNameInplaceScatterValue = "InplaceScatterValue";
constexpr auto kNameIsInf = "IsInf";
constexpr auto kNameInplaceScatterSrc = "InplaceScatterSrc";
constexpr auto kNameInplaceScatterAdd = "InplaceScatterAdd";
constexpr auto kNameInplaceClampTensor = "InplaceClampTensor";
constexpr auto kNameInplaceAddExt = "InplaceAddExt";
constexpr auto kNameInplaceLog = "InplaceLog";
constexpr auto kNameInplaceThreshold = "InplaceThreshold";
constexpr auto kNameInplaceFillScalar = "InplaceFillScalar";
constexpr auto kNameInplaceIndexPut = "InplaceIndexPut";
constexpr auto kNameIsFinite = "IsFinite";
constexpr auto kNameIndexSelect = "IndexSelect";
constexpr auto kNameIHFFT2 = "IHFFT2";
constexpr auto kNameInplaceCopy = "InplaceCopy";
constexpr auto kNameIsNegInf = "IsNegInf";
constexpr auto kNameIRFFT = "IRFFT";
constexpr auto kNameIFFT2 = "IFFT2";
constexpr auto kNameInplaceSubExt = "InplaceSubExt";
constexpr auto kNameInplaceAddmm = "InplaceAddmm";
constexpr auto kNameIRFFTDouble = "IRFFTDouble";
constexpr auto kNameIDCTN = "IDCTN";
constexpr auto kNameInsertGemV2InBackward = "InsertGemV2InBackward";
constexpr auto kNameIndexAddExt = "IndexAddExt";
constexpr auto kNameInplaceTanh = "InplaceTanh";
constexpr auto kNameInnerCommAllReduce = "InnerCommAllReduce";
constexpr auto kNameIncreFlashAttention = "IncreFlashAttention";
constexpr auto kNameInplaceMaskedFillScalar = "InplaceMaskedFillScalar";
constexpr auto kNameInplaceFloorDivides = "InplaceFloorDivides";
constexpr auto kNameInplaceErfinv = "InplaceErfinv";
constexpr auto kNameInplaceHardtanh = "InplaceHardtanh";
constexpr auto kNameInplaceFillTensor = "InplaceFillTensor";
constexpr auto kNameIsClose = "IsClose";
constexpr auto kNameInplaceFloorDivide = "InplaceFloorDivide";
constexpr auto kNameIm2ColExt = "Im2ColExt";
constexpr auto kNameIndexFillScalar = "IndexFillScalar";
constexpr auto kNameIFFTN = "IFFTN";
constexpr auto kNameIDCT = "IDCT";
constexpr auto kNameInplaceAddsExt = "InplaceAddsExt";
constexpr auto kNameInplaceSubScalar = "InplaceSubScalar";
constexpr auto kNameInplacePut = "InplacePut";
constexpr auto kNameIHFFT = "IHFFT";
constexpr auto kNameIFFT = "IFFT";
constexpr auto kNameIRFFTN = "IRFFTN";
constexpr auto kNameInplaceMaskedFillTensor = "InplaceMaskedFillTensor";
constexpr auto kNameInplaceStopGradient = "InplaceStopGradient";
constexpr auto kNameInplaceZero = "InplaceZero";
constexpr auto kNameInplaceGroupedMatmulAdd = "InplaceGroupedMatmulAdd";
constexpr auto kNameInplaceNormal = "InplaceNormal";
constexpr auto kNameInnerCommAllGather = "InnerCommAllGather";
constexpr auto kNameInplaceIndexAddExt = "InplaceIndexAddExt";
constexpr auto kNameInplaceExp = "InplaceExp";
constexpr auto kNameIFFTShift = "IFFTShift";
constexpr auto kNameInnerCommReduceScatter = "InnerCommReduceScatter";
constexpr auto kNameInplaceUniform = "InplaceUniform";
constexpr auto kNameInplaceReLU = "InplaceReLU";
constexpr auto kNameInnerCommIsend = "InnerCommIsend";
constexpr auto kNameInplaceScatterValueReduce = "InplaceScatterValueReduce";
constexpr auto kNameInplaceDivMods = "InplaceDivMods";
constexpr auto kNameInnerIndex = "InnerIndex";
constexpr auto kNameInplaceClampScalar = "InplaceClampScalar";
constexpr auto kNameInplaceRandom = "InplaceRandom";
constexpr auto kNameIndex = "Index";
constexpr auto kNameInplaceFloor = "InplaceFloor";
constexpr auto kNameInplaceExponential = "InplaceExponential";
}  // namespace mindspore::ops

#endif  // MINDSPORE_CORE_OP_NAME_I_H_
