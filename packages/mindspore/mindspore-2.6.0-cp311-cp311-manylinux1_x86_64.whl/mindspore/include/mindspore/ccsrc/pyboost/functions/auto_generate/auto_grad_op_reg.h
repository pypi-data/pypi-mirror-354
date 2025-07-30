/**
 * Copyright 2024 Huawei Technologies Co., Ltd
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

#ifndef MINDSPORE_MINDSPORE_OPS_KERNEL_FUNCTIONS_AUTO_GENERATE_AUTO_GRAD_OP_REG_H_
#define MINDSPORE_MINDSPORE_OPS_KERNEL_FUNCTIONS_AUTO_GENERATE_AUTO_GRAD_OP_REG_H_

#include <functional>
#include <any>
#include <unordered_map>
#include "mindspore/ccsrc/pyboost/op_runner.h"

namespace mindspore {
namespace kernel {
namespace pyboost {
enum class OpType {
  kEmbedding = 0,
  kRmsNorm = 1,
  kRsqrt = 2,
  kTanhGrad = 3,
  kAsinExt = 4,
  kOuter = 5,
  kMoeTokenUnpermuteGrad = 6,
  kAdaptiveMaxPool2D = 7,
  kAvgPool1D = 8,
  kGeluGradExt = 9,
  kInnerInplaceIndexPut = 10,
  kSigmoidGrad = 11,
  kMaxDim = 12,
  kCosh = 13,
  kInplaceDivMod = 14,
  kSplitWithSize = 15,
  kReduceMax = 16,
  kReluGrad = 17,
  kRandExt = 18,
  kDiagExt = 19,
  kMv = 20,
  kNLLLoss2d = 21,
  kLogAddExp = 22,
  kSmoothL1Loss = 23,
  kMultinomialExt = 24,
  kReflectionPad2DGrad = 25,
  kCustomExt = 26,
  kTan = 27,
  kTrunc = 28,
  kConv3DPadding = 29,
  kAcoshExt = 30,
  kBaddbmm = 31,
  kTransposeExtView = 32,
  kSwigluGrad = 33,
  kNormalFloatFloat = 34,
  kNeScalar = 35,
  kMoeTokenUnpermute = 36,
  kInplaceMul = 37,
  kFmodScalar = 38,
  kLayerNormGradExt = 39,
  kAddLayerNormV2 = 40,
  kSqrt = 41,
  kMedianExt = 42,
  kChunk = 43,
  kBinaryCrossEntropyWithLogitsBackward = 44,
  kSlice = 45,
  kIdentity = 46,
  kSeluGrad = 47,
  kLinalgVectorNorm = 48,
  kSoftShrink = 49,
  kSiLUGrad = 50,
  kProdExt = 51,
  kTranspose = 52,
  kArgMinWithValue = 53,
  kOnes = 54,
  kRound = 55,
  kLerp = 56,
  kRandLikeExt = 57,
  kMaskedSelect = 58,
  kLog2 = 59,
  kUpsampleNearest2DGrad = 60,
  kMishGradExt = 61,
  kInplaceFillDiagonal = 62,
  kPReLUGrad = 63,
  kInplaceElu = 64,
  kMishExt = 65,
  kKthvalue = 66,
  kAdd = 67,
  kUniqueDim = 68,
  kHSigmoid = 69,
  kInplaceScatterSrcReduce = 70,
  kRepeat = 71,
  kInnerNonZero = 72,
  kLogSigmoidGrad = 73,
  kNorm = 74,
  kArange = 75,
  kMatrixInverseExt = 76,
  kReciprocal = 77,
  kInplaceDivs = 78,
  kDropoutExt = 79,
  kUnique2 = 80,
  kAbs = 81,
  kXlogy = 82,
  kSilentCheckV2 = 83,
  kReverseV2 = 84,
  kNonZero = 85,
  kCol2ImGrad = 86,
  kSubScalar = 87,
  kAllFinite = 88,
  kTriu = 89,
  kConvolutionStr = 90,
  kHShrinkGrad = 91,
  kMSELossExt = 92,
  kDiv = 93,
  kArgMaxExt = 94,
  kBroadcastTo = 95,
  kReplicationPad1D = 96,
  kBinaryCrossEntropy = 97,
  kMaxUnpool2DExt = 98,
  kLess = 99,
  kLogicalOr = 100,
  kFloor = 101,
  kConcat = 102,
  kMaxPoolGradWithIndices = 103,
  kLogicalNot = 104,
  kInplaceMuls = 105,
  kRepeatInterleaveTensor = 106,
  kBatchMatMulExt = 107,
  kEmbeddingDenseBackward = 108,
  kBroadcastToView = 109,
  kFrac = 110,
  kSelectV2 = 111,
  kInplaceDiv = 112,
  kSin = 113,
  kIndexFillTensor = 114,
  kNLLLoss2dGrad = 115,
  kUpsampleLinear1D = 116,
  kLogSigmoid = 117,
  kFlashAttentionScore = 118,
  kNewOnes = 119,
  kConvolution = 120,
  kGreaterEqual = 121,
  kElu = 122,
  kHShrink = 123,
  kAdaptiveMaxPool1D = 124,
  kLogicalAnd = 125,
  kCos = 126,
  kBatchNormGatherStatsWithCounts = 127,
  kErf = 128,
  kSoftplusGradExt = 129,
  kInplaceScatterValue = 130,
  kIsInf = 131,
  kConstantPadND = 132,
  kReduceMin = 133,
  kConv2DExt = 134,
  kGreater = 135,
  kStdMean = 136,
  kBinaryCrossEntropyGrad = 137,
  kSpeedFusionAttention = 138,
  kDivMod = 139,
  kInplaceScatterSrc = 140,
  kTrilExt = 141,
  kHardtanh = 142,
  kExp2 = 143,
  kInplaceScatterAdd = 144,
  kInplaceClampTensor = 145,
  kInplaceAddExt = 146,
  kFillTensor = 147,
  kReduceAll = 148,
  kUpsampleNearest1DGrad = 149,
  kInplaceLog = 150,
  kInplaceThreshold = 151,
  kClampScalar = 152,
  kReplicationPad3DGrad = 153,
  kInplaceFillScalar = 154,
  kHistcExt = 155,
  kUpsampleBilinear2DGrad = 156,
  kSoftmax = 157,
  kInplaceIndexPut = 158,
  kCol2ImExt = 159,
  kMatMulExt = 160,
  kReflectionPad2D = 161,
  kSilentCheckV3 = 162,
  kGeLUGrad = 163,
  kFFNExt = 164,
  kGridSampler2D = 165,
  kAdaptiveAvgPool2DGradExt = 166,
  kAvgPool3DGradExt = 167,
  kEqual = 168,
  kBincountExt = 169,
  kUpsampleTrilinear3D = 170,
  kLessEqual = 171,
  kExp = 172,
  kRandInt = 173,
  kCumminExt = 174,
  kIsFinite = 175,
  kBatchMatMul = 176,
  kLinSpaceExt = 177,
  kExpm1 = 178,
  kBatchNormStats = 179,
  kMul = 180,
  kMinDim = 181,
  kDot = 182,
  kRandnLike = 183,
  kArgSort = 184,
  kReflectionPad1DGrad = 185,
  kErfinv = 186,
  kLeakyReLUExt = 187,
  kIndexSelect = 188,
  kZerosLikeExt = 189,
  kConv1DPadding = 190,
  kBitwiseXorTensor = 191,
  kMultiScaleDeformableAttnGrad = 192,
  kRepeatInterleaveGrad = 193,
  kUpsampleNearest2D = 194,
  kInplaceCopy = 195,
  kGenerator = 196,
  kConvTranspose2D = 197,
  kSelect = 198,
  kFlashAttentionScoreGrad = 199,
  kIsNegInf = 200,
  kAtanExt = 201,
  kNLLLoss = 202,
  kNeg = 203,
  kTake = 204,
  kAvgPool2D = 205,
  kGcd = 206,
  kLog = 207,
  kAtan2Ext = 208,
  kLogSoftmaxExt = 209,
  kDivs = 210,
  kAddLayerNormGrad = 211,
  kUpsampleBilinear2D = 212,
  kStd = 213,
  kZeros = 214,
  kViewAs = 215,
  kRandpermExt = 216,
  kBernoulliExt = 217,
  kConvolutionStrGrad = 218,
  kInplaceSubExt = 219,
  kEye = 220,
  kRmsNormGrad = 221,
  kDropoutDoMaskExt = 222,
  kSqueeze = 223,
  kPromptFlashAttention = 224,
  kSquare = 225,
  kSoftMarginLossGrad = 226,
  kRoll = 227,
  kCountNonZero = 228,
  kNLLLossGrad = 229,
  kUniqueConsecutive = 230,
  kRandIntLike = 231,
  kSliceExtView = 232,
  kEluGradExt = 233,
  kSelectExtView = 234,
  kContiguous = 235,
  kBitwiseNot = 236,
  kInplaceAddmm = 237,
  kLayerNormExt = 238,
  kPowTensorScalar = 239,
  kScatterAddExt = 240,
  kFmodTensor = 241,
  kConv3DExt = 242,
  kCross = 243,
  kThreshold = 244,
  kFlattenExt = 245,
  kAddcmulExt = 246,
  kAddmm = 247,
  kAdamW = 248,
  kAddmv = 249,
  kUpsampleNearest1D = 250,
  kNanToNum = 251,
  kAllGatherMatmul = 252,
  kRemainderTensorScalar = 253,
  kReLU = 254,
  kSoftShrinkGrad = 255,
  kBitwiseAndScalar = 256,
  kKLDiv = 257,
  kMoeTokenPermute = 258,
  kSplit = 259,
  kVarMean = 260,
  kIndexAddExt = 261,
  kMatmulReduceScatter = 262,
  kConv1DExt = 263,
  kBatchNormElemt = 264,
  kNarrow = 265,
  kBatchNormElemtGrad = 266,
  kUpsampleNearest3D = 267,
  kRemainderScalarTensor = 268,
  kInplaceTanh = 269,
  kErfc = 270,
  kXLogYScalarOther = 271,
  kExpandDimsView = 272,
  kCummax = 273,
  kMoeTokenPermuteGrad = 274,
  kTransposeView = 275,
  kClampTensor = 276,
  kMaximum = 277,
  kPolar = 278,
  kIncreFlashAttention = 279,
  kRotaryPositionEmbeddingGrad = 280,
  kSubExt = 281,
  kBatchNormExt = 282,
  kMuls = 283,
  kOnesLikeExt = 284,
  kMatMul = 285,
  kUpsampleLinear1DGrad = 286,
  kUpsampleTrilinear3DGrad = 287,
  kBitwiseAndTensor = 288,
  kNormalTensorFloat = 289,
  kArgMaxWithValue = 290,
  kTriangularSolve = 291,
  kTile = 292,
  kMedianDim = 293,
  kOneHotExt = 294,
  kTypeAs = 295,
  kGridSampler3DGrad = 296,
  kSoftmaxBackward = 297,
  kNansum = 298,
  kInplaceMaskedFillScalar = 299,
  kInplaceFloorDivides = 300,
  kGridSampler3D = 301,
  kSoftplusExt = 302,
  kInplaceErfinv = 303,
  kInplaceHardtanh = 304,
  kTensorScatterElements = 305,
  kInplaceFillTensor = 306,
  kLinalgQr = 307,
  kL1LossExt = 308,
  kSoftMarginLoss = 309,
  kTopkExt = 310,
  kReplicationPad1DGrad = 311,
  kBitwiseOrTensor = 312,
  kIsClose = 313,
  kAddcdivExt = 314,
  kLeakyReLUGradExt = 315,
  kPowScalarTensor = 316,
  kEluExt = 317,
  kSortExt = 318,
  kInplaceFloorDivide = 319,
  kReplicationPad2D = 320,
  kMaxPoolWithIndices = 321,
  kCast = 322,
  kHSwish = 323,
  kCumsumExt = 324,
  kGroupNormGrad = 325,
  kReflectionPad3D = 326,
  kIm2ColExt = 327,
  kBitwiseXorScalar = 328,
  kDense = 329,
  kIndexFillScalar = 330,
  kExpandAs = 331,
  kSplitWithSizeView = 332,
  kReshape = 333,
  kSplitTensorView = 334,
  kGridSampler2DGrad = 335,
  kSmoothL1LossGrad = 336,
  kGatherD = 337,
  kMaskedFill = 338,
  kFloorDivScalar = 339,
  kCopy = 340,
  kMSELossGradExt = 341,
  kRepeatInterleaveInt = 342,
  kReplicationPad3D = 343,
  kMultiScaleDeformableAttn = 344,
  kReflectionPad1D = 345,
  kGeluExt = 346,
  kVar = 347,
  kDivMods = 348,
  kUniformExt = 349,
  kInplaceAddsExt = 350,
  kMeanExt = 351,
  kReplicationPad2DGrad = 352,
  kSiLU = 353,
  kMinimum = 354,
  kAsStrided = 355,
  kAddScalar = 356,
  kChunkView = 357,
  kHSigmoidGrad = 358,
  kLogSoftmax = 359,
  kFloorDiv = 360,
  kSign = 361,
  kLogSoftmaxGrad = 362,
  kNarrowView = 363,
  kInplaceSubScalar = 364,
  kInplacePut = 365,
  kSpeedFusionAttentionGrad = 366,
  kAvgPool2DGrad = 367,
  kLogAddExp2 = 368,
  kAdaptiveAvgPool2DExt = 369,
  kInplaceMaskedFillTensor = 370,
  kGLU = 371,
  kAddRmsNorm = 372,
  kDropoutGenMaskExt = 373,
  kInplaceStopGradient = 374,
  kXLogYScalarSelf = 375,
  kView = 376,
  kConvolutionGrad = 377,
  kRandn = 378,
  kClone = 379,
  kScatterValue = 380,
  kExpandDims = 381,
  kGatherDGradV2 = 382,
  kSearchSorted = 383,
  kBatchNormReduceGrad = 384,
  kAdaptiveAvgPool1D = 385,
  kAddbmm = 386,
  kInplaceZero = 387,
  kTraceExt = 388,
  kRemainderTensorTensor = 389,
  kThresholdGrad = 390,
  kSigmoid = 391,
  kReflectionPad3DGrad = 392,
  kEqualExt = 393,
  kLog1p = 394,
  kInplaceGroupedMatmulAdd = 395,
  kMm = 396,
  kLogSumExp = 397,
  kNormalTensorTensor = 398,
  kBatchNormGradExt = 399,
  kSliceExt = 400,
  kInplaceNormal = 401,
  kSplitTensor = 402,
  kBitwiseOrScalar = 403,
  kNonZeroExt = 404,
  kTanh = 405,
  kAvgPool3DExt = 406,
  kKLDivGrad = 407,
  kAdaptiveAvgPool3DExt = 408,
  kSub = 409,
  kHSwishGrad = 410,
  kCeil = 411,
  kDropoutGradExt = 412,
  kMeshgrid = 413,
  kMin = 414,
  kScatter = 415,
  kAcosExt = 416,
  kPReLU = 417,
  kInplaceIndexAddExt = 418,
  kInplaceExp = 419,
  kNotEqual = 420,
  kFullLike = 421,
  kUnstackExtView = 422,
  kSinc = 423,
  kGeLU = 424,
  kTExt = 425,
  kArgMinExt = 426,
  kAtanh = 427,
  kInplaceUniform = 428,
  kGroupNorm = 429,
  kAsinhExt = 430,
  kSinh = 431,
  kUpsampleBicubic2D = 432,
  kBCEWithLogitsLoss = 433,
  kMaxPoolGradWithMask = 434,
  kUpsampleBicubic2DGrad = 435,
  kInplaceReLU = 436,
  kNewZeros = 437,
  kMaskedSelectGrad = 438,
  kMax = 439,
  kReduceAny = 440,
  kAddExt = 441,
  kLerpScalar = 442,
  kAdaptiveAvgPool3DGradExt = 443,
  kPow = 444,
  kFillScalar = 445,
  kConv2DPadding = 446,
  kUpsampleNearest3DGrad = 447,
  kInplaceScatterValueReduce = 448,
  kInplaceDivMods = 449,
  kL1LossBackwardExt = 450,
  kSumExt = 451,
  kRotaryPositionEmbedding = 452,
  kLog10 = 453,
  kMaxPoolWithMask = 454,
  kInnerIndex = 455,
  kGreaterEqualScalar = 456,
  kInplaceClampScalar = 457,
  kHardtanhGrad = 458,
  kInplaceRandom = 459,
  kIndex = 460,
  kInplaceFloor = 461,
  kGluGrad = 462,
  kLogicalXor = 463,
  kSwiglu = 464,
  kSeLUExt = 465,
  kStackExt = 466,
  kNormalFloatTensor = 467,
  kWeightQuantBatchMatmul = 468,
  kGroupedMatmulV4 = 469,
  kGroupedMatmul = 470,
  kMoeFinalizeRouting = 471,
  kMoeGatingTopKSoftmax = 472,
  kGroupedMatmulV2 = 473,
  kQuantV2 = 474,
  kKVCacheScatterUpdate = 475,
  kQuantBatchMatmul = 476,
  kDynamicQuantExt = 477,
  kMoeInitRouting = 478,
  kAddRmsNormQuantV2 = 479,
  kMoeInitRoutingV2 = 480,
  kMatmulAllReduceAddRmsNorm = 481,
  kFusedInferAttentionScore = 482,
  kMoeComputeExpertTokens = 483,
  kGmmBackwardFusion = 484,
  kGmmV2BackwardFusion = 485,
  kGmmV2 = 486,
  kGmmV2Backward = 487,
  kPixelShuffle = 488,
  kGmmBackward = 489,
  kGmm = 490,
  kInplaceExponential = 491,
};

using EmbeddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const std::optional<mindspore::FP32ImmPtr> &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &)>;
using RmsNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using RsqrtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TanhGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AsinExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using OuterGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MoeTokenUnpermuteGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using AdaptiveMaxPool2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using AvgPool1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using GeluGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using InnerInplaceIndexPutGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &)>;
using SigmoidGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaxDimGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using CoshGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceDivModGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using SplitWithSizeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using ReduceMaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &)>;
using ReluGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RandExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using DiagExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using MvGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NLLLoss2dGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using LogAddExpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SmoothL1LossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &)>;
using MultinomialExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReflectionPad2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using CustomExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &)>;
using TanGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TruncGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Conv3DPaddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using AcoshExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BaddbmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using TransposeExtViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using SwigluGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using NormalFloatFloatGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NeScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using MoeTokenUnpermuteGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using InplaceMulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FmodScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using LayerNormGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using AddLayerNormV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &)>;
using SqrtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MedianExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ChunkGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using BinaryCrossEntropyWithLogitsBackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using SliceGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &)>;
using IdentityGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SeluGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LinalgVectorNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using SoftShrinkGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using SiLUGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ProdExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using TransposeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using ArgMinWithValueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using OnesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using RoundGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using LerpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RandLikeExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using MaskedSelectGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Log2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleNearest2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using MishGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceFillDiagonalGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::BoolImmPtr &)>;
using PReLUGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceEluGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using MishExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using KthvalueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using AddGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UniqueDimGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using HSigmoidGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceScatterSrcReduceGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using RepeatGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InnerNonZeroGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSigmoidGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ArangeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using MatrixInverseExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReciprocalGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceDivsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using DropoutExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Unique2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using AbsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using XlogyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SilentCheckV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &)>;
using ReverseV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using NonZeroGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Col2ImGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &)>;
using SubScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using AllFiniteGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &)>;
using TriuGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using ConvolutionStrGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using HShrinkGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using MSELossExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using DivGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ArgMaxExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &)>;
using BroadcastToGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using ReplicationPad1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using BinaryCrossEntropyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using MaxUnpool2DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using LessGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogicalOrGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FloorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ConcatGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using MaxPoolGradWithIndicesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using LogicalNotGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceMulsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using RepeatInterleaveTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const std::optional<mindspore::Int64ImmPtr> &)>;
using BatchMatMulExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using EmbeddingDenseBackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &)>;
using BroadcastToViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using FracGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SelectV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceDivGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SinGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IndexFillTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NLLLoss2dGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleLinear1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using LogSigmoidGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FlashAttentionScoreGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using NewOnesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ConvolutionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using GreaterEqualGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using EluGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using HShrinkGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using AdaptiveMaxPool1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using LogicalAndGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CosGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BatchNormGatherStatsWithCountsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using ErfGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SoftplusGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using InplaceScatterValueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using IsInfGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ConstantPadNDGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ScalarPtr &)>;
using ReduceMinGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &)>;
using Conv2DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using GreaterGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using StdMeanGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using BinaryCrossEntropyGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using SpeedFusionAttentionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using DivModGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using InplaceScatterSrcGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TrilExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using HardtanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using Exp2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceScatterAddGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceClampTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using InplaceAddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using FillTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ReduceAllGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using UpsampleNearest1DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using InplaceLogGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceThresholdGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &)>;
using ClampScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ScalarPtr> &, const std::optional<mindspore::ScalarPtr> &)>;
using ReplicationPad3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceFillScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using HistcExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using UpsampleBilinear2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using SoftmaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceIndexPutGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &)>;
using Col2ImExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &)>;
using MatMulExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReflectionPad2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using SilentCheckV3GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GeLUGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FFNExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GridSampler2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using AdaptiveAvgPool2DGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AvgPool3DGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using EqualGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BincountExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using UpsampleTrilinear3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using LessEqualGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ExpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RandIntGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using CumminExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using IsFiniteGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BatchMatMulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using LinSpaceExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using Expm1GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BatchNormStatsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using MulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MinDimGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using DotGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RandnLikeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ArgSortGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using ReflectionPad1DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using ErfinvGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LeakyReLUExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using IndexSelectGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ZerosLikeExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using Conv1DPaddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using BitwiseXorTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MultiScaleDeformableAttnGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RepeatInterleaveGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using UpsampleNearest2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using InplaceCopyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GeneratorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &)>;
using ConvTranspose2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &)>;
using SelectGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FlashAttentionScoreGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using IsNegInfGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AtanExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NLLLossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using NegGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TakeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AvgPool2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using GcdGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Atan2ExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSoftmaxExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const std::optional<mindspore::Int64ImmPtr> &)>;
using DivsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using AddLayerNormGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleBilinear2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using StdGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using ZerosGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ViewAsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RandpermExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using BernoulliExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ConvolutionStrGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceSubExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using EyeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using RmsNormGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using DropoutDoMaskExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using SqueezeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using PromptFlashAttentionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using SquareGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SoftMarginLossGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using RollGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using CountNonZeroGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using NLLLossGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using UniqueConsecutiveGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using RandIntLikeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using SliceExtViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using EluGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &)>;
using SelectExtViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using ContiguousGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BitwiseNotGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceAddmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using LayerNormExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &)>;
using PowTensorScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ScatterAddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FmodTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Conv3DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using CrossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using ThresholdGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &)>;
using FlattenExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using AddcmulExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using AddmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using AdamWGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using AddmvGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using UpsampleNearest1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using NanToNumGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::FP32ImmPtr> &, const std::optional<mindspore::FP32ImmPtr> &, const std::optional<mindspore::FP32ImmPtr> &)>;
using AllGatherMatmulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::StringImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using RemainderTensorScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ReLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SoftShrinkGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using BitwiseAndScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using KLDivGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using MoeTokenPermuteGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &)>;
using SplitGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using VarMeanGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using IndexAddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using MatmulReduceScatterGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::StringImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using Conv1DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using BatchNormElemtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &)>;
using NarrowGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using BatchNormElemtGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleNearest3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using RemainderScalarTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceTanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ErfcGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using XLogYScalarOtherGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ExpandDimsViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using CummaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using MoeTokenPermuteGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using TransposeViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using ClampTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using MaximumGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using PolarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IncreFlashAttentionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using RotaryPositionEmbeddingGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using SubExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using BatchNormExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &)>;
using MulsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using OnesLikeExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using MatMulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using UpsampleLinear1DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using UpsampleTrilinear3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using BitwiseAndTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NormalTensorFloatGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ArgMaxWithValueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using TriangularSolveGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using TileGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using MedianDimGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using OneHotExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using TypeAsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GridSampler3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &)>;
using SoftmaxBackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using NansumGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using InplaceMaskedFillScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using InplaceFloorDividesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using GridSampler3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using SoftplusExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using InplaceErfinvGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceHardtanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using TensorScatterElementsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceFillTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LinalgQrGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using L1LossExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using SoftMarginLossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using TopkExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using ReplicationPad1DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using BitwiseOrTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IsCloseGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &)>;
using AddcdivExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using LeakyReLUGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::BoolImmPtr &)>;
using PowScalarTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using EluExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using SortExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using InplaceFloorDivideGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReplicationPad2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using MaxPoolWithIndicesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using CastGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using HSwishGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CumsumExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using GroupNormGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using ReflectionPad3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using Im2ColExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &)>;
using BitwiseXorScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using DenseGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using IndexFillScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ExpandAsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SplitWithSizeViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using ReshapeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using SplitTensorViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GridSampler2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &)>;
using SmoothL1LossGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GatherDGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaskedFillGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FloorDivScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using CopyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MSELossGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using RepeatInterleaveIntGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ReplicationPad3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using MultiScaleDeformableAttnGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReflectionPad1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using GeluExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using VarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using DivModsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using UniformExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceAddsExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using MeanExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ReplicationPad2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using SiLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MinimumGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AsStridedGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using AddScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using ChunkViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using HSigmoidGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSoftmaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using FloorDivGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SignGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSoftmaxGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using NarrowViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceSubScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using InplacePutGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &)>;
using SpeedFusionAttentionGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using AvgPool2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using LogAddExp2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AdaptiveAvgPool2DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceMaskedFillTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using AddRmsNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using DropoutGenMaskExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::FP32ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceStopGradientGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using XLogYScalarSelfGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using ConvolutionGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &)>;
using RandnGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using CloneGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ScatterValueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::Int64ImmPtr &)>;
using ExpandDimsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using GatherDGradV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SearchSortedGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using BatchNormReduceGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using AdaptiveAvgPool1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using AddbmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using InplaceZeroGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TraceExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RemainderTensorTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ThresholdGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using SigmoidGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReflectionPad3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using EqualExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Log1pGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceGroupedMatmulAddGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSumExpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &)>;
using NormalTensorTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BatchNormGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::ValueTuplePtr &)>;
using SliceExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceNormalGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SplitTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using BitwiseOrScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using NonZeroExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AvgPool3DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using KLDivGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using AdaptiveAvgPool3DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using SubGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using HSwishGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CeilGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using DropoutGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using MeshgridGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using MinGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ScatterGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using AcosExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using PReLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceIndexAddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using InplaceExpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NotEqualGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FullLikeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using UnstackExtViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using SincGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GeLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ArgMinExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &)>;
using AtanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceUniformGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GroupNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &)>;
using AsinhExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SinhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleBicubic2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using BCEWithLogitsLossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using MaxPoolGradWithMaskGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using UpsampleBicubic2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using InplaceReLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NewZerosGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using MaskedSelectGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReduceAnyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &)>;
using AddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using LerpScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using AdaptiveAvgPool3DGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using PowGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FillScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using Conv2DPaddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using UpsampleNearest3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using InplaceScatterValueReduceGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceDivModsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using L1LossBackwardExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using SumExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using RotaryPositionEmbeddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using Log10GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaxPoolWithMaskGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using InnerIndexGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using GreaterEqualScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using InplaceClampScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ScalarPtr> &, const std::optional<mindspore::ScalarPtr> &)>;
using HardtanhGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using InplaceRandomGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IndexGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceFloorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GluGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using LogicalXorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SwigluGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using SeLUExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using StackExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using NormalFloatTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::FP32ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using WeightQuantBatchMatmulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using GroupedMatmulV4GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GroupedMatmulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using MoeFinalizeRoutingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using MoeGatingTopKSoftmaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using GroupedMatmulV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using QuantV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using KVCacheScatterUpdateGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using QuantBatchMatmulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using DynamicQuantExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using MoeInitRoutingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using AddRmsNormQuantV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using MoeInitRoutingV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using MatmulAllReduceAddRmsNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::StringImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using FusedInferAttentionScoreGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using MoeComputeExpertTokensGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using GmmBackwardFusionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &)>;
using GmmV2BackwardFusionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using GmmV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GmmV2BackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using PixelShuffleGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using GmmBackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &)>;
using GmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceExponentialGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;

struct OpsAutoGradRegisters {
  EmbeddingGradFunc EmbeddingGradFuncObj;
  RmsNormGradFunc RmsNormGradFuncObj;
  RsqrtGradFunc RsqrtGradFuncObj;
  TanhGradGradFunc TanhGradGradFuncObj;
  AsinExtGradFunc AsinExtGradFuncObj;
  OuterGradFunc OuterGradFuncObj;
  MoeTokenUnpermuteGradGradFunc MoeTokenUnpermuteGradGradFuncObj;
  AdaptiveMaxPool2DGradFunc AdaptiveMaxPool2DGradFuncObj;
  AvgPool1DGradFunc AvgPool1DGradFuncObj;
  GeluGradExtGradFunc GeluGradExtGradFuncObj;
  InnerInplaceIndexPutGradFunc InnerInplaceIndexPutGradFuncObj;
  SigmoidGradGradFunc SigmoidGradGradFuncObj;
  MaxDimGradFunc MaxDimGradFuncObj;
  CoshGradFunc CoshGradFuncObj;
  InplaceDivModGradFunc InplaceDivModGradFuncObj;
  SplitWithSizeGradFunc SplitWithSizeGradFuncObj;
  ReduceMaxGradFunc ReduceMaxGradFuncObj;
  ReluGradGradFunc ReluGradGradFuncObj;
  RandExtGradFunc RandExtGradFuncObj;
  DiagExtGradFunc DiagExtGradFuncObj;
  MvGradFunc MvGradFuncObj;
  NLLLoss2dGradFunc NLLLoss2dGradFuncObj;
  LogAddExpGradFunc LogAddExpGradFuncObj;
  SmoothL1LossGradFunc SmoothL1LossGradFuncObj;
  MultinomialExtGradFunc MultinomialExtGradFuncObj;
  ReflectionPad2DGradGradFunc ReflectionPad2DGradGradFuncObj;
  CustomExtGradFunc CustomExtGradFuncObj;
  TanGradFunc TanGradFuncObj;
  TruncGradFunc TruncGradFuncObj;
  Conv3DPaddingGradFunc Conv3DPaddingGradFuncObj;
  AcoshExtGradFunc AcoshExtGradFuncObj;
  BaddbmmGradFunc BaddbmmGradFuncObj;
  TransposeExtViewGradFunc TransposeExtViewGradFuncObj;
  SwigluGradGradFunc SwigluGradGradFuncObj;
  NormalFloatFloatGradFunc NormalFloatFloatGradFuncObj;
  NeScalarGradFunc NeScalarGradFuncObj;
  MoeTokenUnpermuteGradFunc MoeTokenUnpermuteGradFuncObj;
  InplaceMulGradFunc InplaceMulGradFuncObj;
  FmodScalarGradFunc FmodScalarGradFuncObj;
  LayerNormGradExtGradFunc LayerNormGradExtGradFuncObj;
  AddLayerNormV2GradFunc AddLayerNormV2GradFuncObj;
  SqrtGradFunc SqrtGradFuncObj;
  MedianExtGradFunc MedianExtGradFuncObj;
  ChunkGradFunc ChunkGradFuncObj;
  BinaryCrossEntropyWithLogitsBackwardGradFunc BinaryCrossEntropyWithLogitsBackwardGradFuncObj;
  SliceGradFunc SliceGradFuncObj;
  IdentityGradFunc IdentityGradFuncObj;
  SeluGradGradFunc SeluGradGradFuncObj;
  LinalgVectorNormGradFunc LinalgVectorNormGradFuncObj;
  SoftShrinkGradFunc SoftShrinkGradFuncObj;
  SiLUGradGradFunc SiLUGradGradFuncObj;
  ProdExtGradFunc ProdExtGradFuncObj;
  TransposeGradFunc TransposeGradFuncObj;
  ArgMinWithValueGradFunc ArgMinWithValueGradFuncObj;
  OnesGradFunc OnesGradFuncObj;
  RoundGradFunc RoundGradFuncObj;
  LerpGradFunc LerpGradFuncObj;
  RandLikeExtGradFunc RandLikeExtGradFuncObj;
  MaskedSelectGradFunc MaskedSelectGradFuncObj;
  Log2GradFunc Log2GradFuncObj;
  UpsampleNearest2DGradGradFunc UpsampleNearest2DGradGradFuncObj;
  MishGradExtGradFunc MishGradExtGradFuncObj;
  InplaceFillDiagonalGradFunc InplaceFillDiagonalGradFuncObj;
  PReLUGradGradFunc PReLUGradGradFuncObj;
  InplaceEluGradFunc InplaceEluGradFuncObj;
  MishExtGradFunc MishExtGradFuncObj;
  KthvalueGradFunc KthvalueGradFuncObj;
  AddGradFunc AddGradFuncObj;
  UniqueDimGradFunc UniqueDimGradFuncObj;
  HSigmoidGradFunc HSigmoidGradFuncObj;
  InplaceScatterSrcReduceGradFunc InplaceScatterSrcReduceGradFuncObj;
  RepeatGradFunc RepeatGradFuncObj;
  InnerNonZeroGradFunc InnerNonZeroGradFuncObj;
  LogSigmoidGradGradFunc LogSigmoidGradGradFuncObj;
  NormGradFunc NormGradFuncObj;
  ArangeGradFunc ArangeGradFuncObj;
  MatrixInverseExtGradFunc MatrixInverseExtGradFuncObj;
  ReciprocalGradFunc ReciprocalGradFuncObj;
  InplaceDivsGradFunc InplaceDivsGradFuncObj;
  DropoutExtGradFunc DropoutExtGradFuncObj;
  Unique2GradFunc Unique2GradFuncObj;
  AbsGradFunc AbsGradFuncObj;
  XlogyGradFunc XlogyGradFuncObj;
  SilentCheckV2GradFunc SilentCheckV2GradFuncObj;
  ReverseV2GradFunc ReverseV2GradFuncObj;
  NonZeroGradFunc NonZeroGradFuncObj;
  Col2ImGradGradFunc Col2ImGradGradFuncObj;
  SubScalarGradFunc SubScalarGradFuncObj;
  AllFiniteGradFunc AllFiniteGradFuncObj;
  TriuGradFunc TriuGradFuncObj;
  ConvolutionStrGradFunc ConvolutionStrGradFuncObj;
  HShrinkGradGradFunc HShrinkGradGradFuncObj;
  MSELossExtGradFunc MSELossExtGradFuncObj;
  DivGradFunc DivGradFuncObj;
  ArgMaxExtGradFunc ArgMaxExtGradFuncObj;
  BroadcastToGradFunc BroadcastToGradFuncObj;
  ReplicationPad1DGradFunc ReplicationPad1DGradFuncObj;
  BinaryCrossEntropyGradFunc BinaryCrossEntropyGradFuncObj;
  MaxUnpool2DExtGradFunc MaxUnpool2DExtGradFuncObj;
  LessGradFunc LessGradFuncObj;
  LogicalOrGradFunc LogicalOrGradFuncObj;
  FloorGradFunc FloorGradFuncObj;
  ConcatGradFunc ConcatGradFuncObj;
  MaxPoolGradWithIndicesGradFunc MaxPoolGradWithIndicesGradFuncObj;
  LogicalNotGradFunc LogicalNotGradFuncObj;
  InplaceMulsGradFunc InplaceMulsGradFuncObj;
  RepeatInterleaveTensorGradFunc RepeatInterleaveTensorGradFuncObj;
  BatchMatMulExtGradFunc BatchMatMulExtGradFuncObj;
  EmbeddingDenseBackwardGradFunc EmbeddingDenseBackwardGradFuncObj;
  BroadcastToViewGradFunc BroadcastToViewGradFuncObj;
  FracGradFunc FracGradFuncObj;
  SelectV2GradFunc SelectV2GradFuncObj;
  InplaceDivGradFunc InplaceDivGradFuncObj;
  SinGradFunc SinGradFuncObj;
  IndexFillTensorGradFunc IndexFillTensorGradFuncObj;
  NLLLoss2dGradGradFunc NLLLoss2dGradGradFuncObj;
  UpsampleLinear1DGradFunc UpsampleLinear1DGradFuncObj;
  LogSigmoidGradFunc LogSigmoidGradFuncObj;
  FlashAttentionScoreGradFunc FlashAttentionScoreGradFuncObj;
  NewOnesGradFunc NewOnesGradFuncObj;
  ConvolutionGradFunc ConvolutionGradFuncObj;
  GreaterEqualGradFunc GreaterEqualGradFuncObj;
  EluGradFunc EluGradFuncObj;
  HShrinkGradFunc HShrinkGradFuncObj;
  AdaptiveMaxPool1DGradFunc AdaptiveMaxPool1DGradFuncObj;
  LogicalAndGradFunc LogicalAndGradFuncObj;
  CosGradFunc CosGradFuncObj;
  BatchNormGatherStatsWithCountsGradFunc BatchNormGatherStatsWithCountsGradFuncObj;
  ErfGradFunc ErfGradFuncObj;
  SoftplusGradExtGradFunc SoftplusGradExtGradFuncObj;
  InplaceScatterValueGradFunc InplaceScatterValueGradFuncObj;
  IsInfGradFunc IsInfGradFuncObj;
  ConstantPadNDGradFunc ConstantPadNDGradFuncObj;
  ReduceMinGradFunc ReduceMinGradFuncObj;
  Conv2DExtGradFunc Conv2DExtGradFuncObj;
  GreaterGradFunc GreaterGradFuncObj;
  StdMeanGradFunc StdMeanGradFuncObj;
  BinaryCrossEntropyGradGradFunc BinaryCrossEntropyGradGradFuncObj;
  SpeedFusionAttentionGradFunc SpeedFusionAttentionGradFuncObj;
  DivModGradFunc DivModGradFuncObj;
  InplaceScatterSrcGradFunc InplaceScatterSrcGradFuncObj;
  TrilExtGradFunc TrilExtGradFuncObj;
  HardtanhGradFunc HardtanhGradFuncObj;
  Exp2GradFunc Exp2GradFuncObj;
  InplaceScatterAddGradFunc InplaceScatterAddGradFuncObj;
  InplaceClampTensorGradFunc InplaceClampTensorGradFuncObj;
  InplaceAddExtGradFunc InplaceAddExtGradFuncObj;
  FillTensorGradFunc FillTensorGradFuncObj;
  ReduceAllGradFunc ReduceAllGradFuncObj;
  UpsampleNearest1DGradGradFunc UpsampleNearest1DGradGradFuncObj;
  InplaceLogGradFunc InplaceLogGradFuncObj;
  InplaceThresholdGradFunc InplaceThresholdGradFuncObj;
  ClampScalarGradFunc ClampScalarGradFuncObj;
  ReplicationPad3DGradGradFunc ReplicationPad3DGradGradFuncObj;
  InplaceFillScalarGradFunc InplaceFillScalarGradFuncObj;
  HistcExtGradFunc HistcExtGradFuncObj;
  UpsampleBilinear2DGradGradFunc UpsampleBilinear2DGradGradFuncObj;
  SoftmaxGradFunc SoftmaxGradFuncObj;
  InplaceIndexPutGradFunc InplaceIndexPutGradFuncObj;
  Col2ImExtGradFunc Col2ImExtGradFuncObj;
  MatMulExtGradFunc MatMulExtGradFuncObj;
  ReflectionPad2DGradFunc ReflectionPad2DGradFuncObj;
  SilentCheckV3GradFunc SilentCheckV3GradFuncObj;
  GeLUGradGradFunc GeLUGradGradFuncObj;
  FFNExtGradFunc FFNExtGradFuncObj;
  GridSampler2DGradFunc GridSampler2DGradFuncObj;
  AdaptiveAvgPool2DGradExtGradFunc AdaptiveAvgPool2DGradExtGradFuncObj;
  AvgPool3DGradExtGradFunc AvgPool3DGradExtGradFuncObj;
  EqualGradFunc EqualGradFuncObj;
  BincountExtGradFunc BincountExtGradFuncObj;
  UpsampleTrilinear3DGradFunc UpsampleTrilinear3DGradFuncObj;
  LessEqualGradFunc LessEqualGradFuncObj;
  ExpGradFunc ExpGradFuncObj;
  RandIntGradFunc RandIntGradFuncObj;
  CumminExtGradFunc CumminExtGradFuncObj;
  IsFiniteGradFunc IsFiniteGradFuncObj;
  BatchMatMulGradFunc BatchMatMulGradFuncObj;
  LinSpaceExtGradFunc LinSpaceExtGradFuncObj;
  Expm1GradFunc Expm1GradFuncObj;
  BatchNormStatsGradFunc BatchNormStatsGradFuncObj;
  MulGradFunc MulGradFuncObj;
  MinDimGradFunc MinDimGradFuncObj;
  DotGradFunc DotGradFuncObj;
  RandnLikeGradFunc RandnLikeGradFuncObj;
  ArgSortGradFunc ArgSortGradFuncObj;
  ReflectionPad1DGradGradFunc ReflectionPad1DGradGradFuncObj;
  ErfinvGradFunc ErfinvGradFuncObj;
  LeakyReLUExtGradFunc LeakyReLUExtGradFuncObj;
  IndexSelectGradFunc IndexSelectGradFuncObj;
  ZerosLikeExtGradFunc ZerosLikeExtGradFuncObj;
  Conv1DPaddingGradFunc Conv1DPaddingGradFuncObj;
  BitwiseXorTensorGradFunc BitwiseXorTensorGradFuncObj;
  MultiScaleDeformableAttnGradGradFunc MultiScaleDeformableAttnGradGradFuncObj;
  RepeatInterleaveGradGradFunc RepeatInterleaveGradGradFuncObj;
  UpsampleNearest2DGradFunc UpsampleNearest2DGradFuncObj;
  InplaceCopyGradFunc InplaceCopyGradFuncObj;
  GeneratorGradFunc GeneratorGradFuncObj;
  ConvTranspose2DGradFunc ConvTranspose2DGradFuncObj;
  SelectGradFunc SelectGradFuncObj;
  FlashAttentionScoreGradGradFunc FlashAttentionScoreGradGradFuncObj;
  IsNegInfGradFunc IsNegInfGradFuncObj;
  AtanExtGradFunc AtanExtGradFuncObj;
  NLLLossGradFunc NLLLossGradFuncObj;
  NegGradFunc NegGradFuncObj;
  TakeGradFunc TakeGradFuncObj;
  AvgPool2DGradFunc AvgPool2DGradFuncObj;
  GcdGradFunc GcdGradFuncObj;
  LogGradFunc LogGradFuncObj;
  Atan2ExtGradFunc Atan2ExtGradFuncObj;
  LogSoftmaxExtGradFunc LogSoftmaxExtGradFuncObj;
  DivsGradFunc DivsGradFuncObj;
  AddLayerNormGradGradFunc AddLayerNormGradGradFuncObj;
  UpsampleBilinear2DGradFunc UpsampleBilinear2DGradFuncObj;
  StdGradFunc StdGradFuncObj;
  ZerosGradFunc ZerosGradFuncObj;
  ViewAsGradFunc ViewAsGradFuncObj;
  RandpermExtGradFunc RandpermExtGradFuncObj;
  BernoulliExtGradFunc BernoulliExtGradFuncObj;
  ConvolutionStrGradGradFunc ConvolutionStrGradGradFuncObj;
  InplaceSubExtGradFunc InplaceSubExtGradFuncObj;
  EyeGradFunc EyeGradFuncObj;
  RmsNormGradGradFunc RmsNormGradGradFuncObj;
  DropoutDoMaskExtGradFunc DropoutDoMaskExtGradFuncObj;
  SqueezeGradFunc SqueezeGradFuncObj;
  PromptFlashAttentionGradFunc PromptFlashAttentionGradFuncObj;
  SquareGradFunc SquareGradFuncObj;
  SoftMarginLossGradGradFunc SoftMarginLossGradGradFuncObj;
  RollGradFunc RollGradFuncObj;
  CountNonZeroGradFunc CountNonZeroGradFuncObj;
  NLLLossGradGradFunc NLLLossGradGradFuncObj;
  UniqueConsecutiveGradFunc UniqueConsecutiveGradFuncObj;
  RandIntLikeGradFunc RandIntLikeGradFuncObj;
  SliceExtViewGradFunc SliceExtViewGradFuncObj;
  EluGradExtGradFunc EluGradExtGradFuncObj;
  SelectExtViewGradFunc SelectExtViewGradFuncObj;
  ContiguousGradFunc ContiguousGradFuncObj;
  BitwiseNotGradFunc BitwiseNotGradFuncObj;
  InplaceAddmmGradFunc InplaceAddmmGradFuncObj;
  LayerNormExtGradFunc LayerNormExtGradFuncObj;
  PowTensorScalarGradFunc PowTensorScalarGradFuncObj;
  ScatterAddExtGradFunc ScatterAddExtGradFuncObj;
  FmodTensorGradFunc FmodTensorGradFuncObj;
  Conv3DExtGradFunc Conv3DExtGradFuncObj;
  CrossGradFunc CrossGradFuncObj;
  ThresholdGradFunc ThresholdGradFuncObj;
  FlattenExtGradFunc FlattenExtGradFuncObj;
  AddcmulExtGradFunc AddcmulExtGradFuncObj;
  AddmmGradFunc AddmmGradFuncObj;
  AdamWGradFunc AdamWGradFuncObj;
  AddmvGradFunc AddmvGradFuncObj;
  UpsampleNearest1DGradFunc UpsampleNearest1DGradFuncObj;
  NanToNumGradFunc NanToNumGradFuncObj;
  AllGatherMatmulGradFunc AllGatherMatmulGradFuncObj;
  RemainderTensorScalarGradFunc RemainderTensorScalarGradFuncObj;
  ReLUGradFunc ReLUGradFuncObj;
  SoftShrinkGradGradFunc SoftShrinkGradGradFuncObj;
  BitwiseAndScalarGradFunc BitwiseAndScalarGradFuncObj;
  KLDivGradFunc KLDivGradFuncObj;
  MoeTokenPermuteGradFunc MoeTokenPermuteGradFuncObj;
  SplitGradFunc SplitGradFuncObj;
  VarMeanGradFunc VarMeanGradFuncObj;
  IndexAddExtGradFunc IndexAddExtGradFuncObj;
  MatmulReduceScatterGradFunc MatmulReduceScatterGradFuncObj;
  Conv1DExtGradFunc Conv1DExtGradFuncObj;
  BatchNormElemtGradFunc BatchNormElemtGradFuncObj;
  NarrowGradFunc NarrowGradFuncObj;
  BatchNormElemtGradGradFunc BatchNormElemtGradGradFuncObj;
  UpsampleNearest3DGradFunc UpsampleNearest3DGradFuncObj;
  RemainderScalarTensorGradFunc RemainderScalarTensorGradFuncObj;
  InplaceTanhGradFunc InplaceTanhGradFuncObj;
  ErfcGradFunc ErfcGradFuncObj;
  XLogYScalarOtherGradFunc XLogYScalarOtherGradFuncObj;
  ExpandDimsViewGradFunc ExpandDimsViewGradFuncObj;
  CummaxGradFunc CummaxGradFuncObj;
  MoeTokenPermuteGradGradFunc MoeTokenPermuteGradGradFuncObj;
  TransposeViewGradFunc TransposeViewGradFuncObj;
  ClampTensorGradFunc ClampTensorGradFuncObj;
  MaximumGradFunc MaximumGradFuncObj;
  PolarGradFunc PolarGradFuncObj;
  IncreFlashAttentionGradFunc IncreFlashAttentionGradFuncObj;
  RotaryPositionEmbeddingGradGradFunc RotaryPositionEmbeddingGradGradFuncObj;
  SubExtGradFunc SubExtGradFuncObj;
  BatchNormExtGradFunc BatchNormExtGradFuncObj;
  MulsGradFunc MulsGradFuncObj;
  OnesLikeExtGradFunc OnesLikeExtGradFuncObj;
  MatMulGradFunc MatMulGradFuncObj;
  UpsampleLinear1DGradGradFunc UpsampleLinear1DGradGradFuncObj;
  UpsampleTrilinear3DGradGradFunc UpsampleTrilinear3DGradGradFuncObj;
  BitwiseAndTensorGradFunc BitwiseAndTensorGradFuncObj;
  NormalTensorFloatGradFunc NormalTensorFloatGradFuncObj;
  ArgMaxWithValueGradFunc ArgMaxWithValueGradFuncObj;
  TriangularSolveGradFunc TriangularSolveGradFuncObj;
  TileGradFunc TileGradFuncObj;
  MedianDimGradFunc MedianDimGradFuncObj;
  OneHotExtGradFunc OneHotExtGradFuncObj;
  TypeAsGradFunc TypeAsGradFuncObj;
  GridSampler3DGradGradFunc GridSampler3DGradGradFuncObj;
  SoftmaxBackwardGradFunc SoftmaxBackwardGradFuncObj;
  NansumGradFunc NansumGradFuncObj;
  InplaceMaskedFillScalarGradFunc InplaceMaskedFillScalarGradFuncObj;
  InplaceFloorDividesGradFunc InplaceFloorDividesGradFuncObj;
  GridSampler3DGradFunc GridSampler3DGradFuncObj;
  SoftplusExtGradFunc SoftplusExtGradFuncObj;
  InplaceErfinvGradFunc InplaceErfinvGradFuncObj;
  InplaceHardtanhGradFunc InplaceHardtanhGradFuncObj;
  TensorScatterElementsGradFunc TensorScatterElementsGradFuncObj;
  InplaceFillTensorGradFunc InplaceFillTensorGradFuncObj;
  LinalgQrGradFunc LinalgQrGradFuncObj;
  L1LossExtGradFunc L1LossExtGradFuncObj;
  SoftMarginLossGradFunc SoftMarginLossGradFuncObj;
  TopkExtGradFunc TopkExtGradFuncObj;
  ReplicationPad1DGradGradFunc ReplicationPad1DGradGradFuncObj;
  BitwiseOrTensorGradFunc BitwiseOrTensorGradFuncObj;
  IsCloseGradFunc IsCloseGradFuncObj;
  AddcdivExtGradFunc AddcdivExtGradFuncObj;
  LeakyReLUGradExtGradFunc LeakyReLUGradExtGradFuncObj;
  PowScalarTensorGradFunc PowScalarTensorGradFuncObj;
  EluExtGradFunc EluExtGradFuncObj;
  SortExtGradFunc SortExtGradFuncObj;
  InplaceFloorDivideGradFunc InplaceFloorDivideGradFuncObj;
  ReplicationPad2DGradFunc ReplicationPad2DGradFuncObj;
  MaxPoolWithIndicesGradFunc MaxPoolWithIndicesGradFuncObj;
  CastGradFunc CastGradFuncObj;
  HSwishGradFunc HSwishGradFuncObj;
  CumsumExtGradFunc CumsumExtGradFuncObj;
  GroupNormGradGradFunc GroupNormGradGradFuncObj;
  ReflectionPad3DGradFunc ReflectionPad3DGradFuncObj;
  Im2ColExtGradFunc Im2ColExtGradFuncObj;
  BitwiseXorScalarGradFunc BitwiseXorScalarGradFuncObj;
  DenseGradFunc DenseGradFuncObj;
  IndexFillScalarGradFunc IndexFillScalarGradFuncObj;
  ExpandAsGradFunc ExpandAsGradFuncObj;
  SplitWithSizeViewGradFunc SplitWithSizeViewGradFuncObj;
  ReshapeGradFunc ReshapeGradFuncObj;
  SplitTensorViewGradFunc SplitTensorViewGradFuncObj;
  GridSampler2DGradGradFunc GridSampler2DGradGradFuncObj;
  SmoothL1LossGradGradFunc SmoothL1LossGradGradFuncObj;
  GatherDGradFunc GatherDGradFuncObj;
  MaskedFillGradFunc MaskedFillGradFuncObj;
  FloorDivScalarGradFunc FloorDivScalarGradFuncObj;
  CopyGradFunc CopyGradFuncObj;
  MSELossGradExtGradFunc MSELossGradExtGradFuncObj;
  RepeatInterleaveIntGradFunc RepeatInterleaveIntGradFuncObj;
  ReplicationPad3DGradFunc ReplicationPad3DGradFuncObj;
  MultiScaleDeformableAttnGradFunc MultiScaleDeformableAttnGradFuncObj;
  ReflectionPad1DGradFunc ReflectionPad1DGradFuncObj;
  GeluExtGradFunc GeluExtGradFuncObj;
  VarGradFunc VarGradFuncObj;
  DivModsGradFunc DivModsGradFuncObj;
  UniformExtGradFunc UniformExtGradFuncObj;
  InplaceAddsExtGradFunc InplaceAddsExtGradFuncObj;
  MeanExtGradFunc MeanExtGradFuncObj;
  ReplicationPad2DGradGradFunc ReplicationPad2DGradGradFuncObj;
  SiLUGradFunc SiLUGradFuncObj;
  MinimumGradFunc MinimumGradFuncObj;
  AsStridedGradFunc AsStridedGradFuncObj;
  AddScalarGradFunc AddScalarGradFuncObj;
  ChunkViewGradFunc ChunkViewGradFuncObj;
  HSigmoidGradGradFunc HSigmoidGradGradFuncObj;
  LogSoftmaxGradFunc LogSoftmaxGradFuncObj;
  FloorDivGradFunc FloorDivGradFuncObj;
  SignGradFunc SignGradFuncObj;
  LogSoftmaxGradGradFunc LogSoftmaxGradGradFuncObj;
  NarrowViewGradFunc NarrowViewGradFuncObj;
  InplaceSubScalarGradFunc InplaceSubScalarGradFuncObj;
  InplacePutGradFunc InplacePutGradFuncObj;
  SpeedFusionAttentionGradGradFunc SpeedFusionAttentionGradGradFuncObj;
  AvgPool2DGradGradFunc AvgPool2DGradGradFuncObj;
  LogAddExp2GradFunc LogAddExp2GradFuncObj;
  AdaptiveAvgPool2DExtGradFunc AdaptiveAvgPool2DExtGradFuncObj;
  InplaceMaskedFillTensorGradFunc InplaceMaskedFillTensorGradFuncObj;
  GLUGradFunc GLUGradFuncObj;
  AddRmsNormGradFunc AddRmsNormGradFuncObj;
  DropoutGenMaskExtGradFunc DropoutGenMaskExtGradFuncObj;
  InplaceStopGradientGradFunc InplaceStopGradientGradFuncObj;
  XLogYScalarSelfGradFunc XLogYScalarSelfGradFuncObj;
  ViewGradFunc ViewGradFuncObj;
  ConvolutionGradGradFunc ConvolutionGradGradFuncObj;
  RandnGradFunc RandnGradFuncObj;
  CloneGradFunc CloneGradFuncObj;
  ScatterValueGradFunc ScatterValueGradFuncObj;
  ExpandDimsGradFunc ExpandDimsGradFuncObj;
  GatherDGradV2GradFunc GatherDGradV2GradFuncObj;
  SearchSortedGradFunc SearchSortedGradFuncObj;
  BatchNormReduceGradGradFunc BatchNormReduceGradGradFuncObj;
  AdaptiveAvgPool1DGradFunc AdaptiveAvgPool1DGradFuncObj;
  AddbmmGradFunc AddbmmGradFuncObj;
  InplaceZeroGradFunc InplaceZeroGradFuncObj;
  TraceExtGradFunc TraceExtGradFuncObj;
  RemainderTensorTensorGradFunc RemainderTensorTensorGradFuncObj;
  ThresholdGradGradFunc ThresholdGradGradFuncObj;
  SigmoidGradFunc SigmoidGradFuncObj;
  ReflectionPad3DGradGradFunc ReflectionPad3DGradGradFuncObj;
  EqualExtGradFunc EqualExtGradFuncObj;
  Log1pGradFunc Log1pGradFuncObj;
  InplaceGroupedMatmulAddGradFunc InplaceGroupedMatmulAddGradFuncObj;
  MmGradFunc MmGradFuncObj;
  LogSumExpGradFunc LogSumExpGradFuncObj;
  NormalTensorTensorGradFunc NormalTensorTensorGradFuncObj;
  BatchNormGradExtGradFunc BatchNormGradExtGradFuncObj;
  SliceExtGradFunc SliceExtGradFuncObj;
  InplaceNormalGradFunc InplaceNormalGradFuncObj;
  SplitTensorGradFunc SplitTensorGradFuncObj;
  BitwiseOrScalarGradFunc BitwiseOrScalarGradFuncObj;
  NonZeroExtGradFunc NonZeroExtGradFuncObj;
  TanhGradFunc TanhGradFuncObj;
  AvgPool3DExtGradFunc AvgPool3DExtGradFuncObj;
  KLDivGradGradFunc KLDivGradGradFuncObj;
  AdaptiveAvgPool3DExtGradFunc AdaptiveAvgPool3DExtGradFuncObj;
  SubGradFunc SubGradFuncObj;
  HSwishGradGradFunc HSwishGradGradFuncObj;
  CeilGradFunc CeilGradFuncObj;
  DropoutGradExtGradFunc DropoutGradExtGradFuncObj;
  MeshgridGradFunc MeshgridGradFuncObj;
  MinGradFunc MinGradFuncObj;
  ScatterGradFunc ScatterGradFuncObj;
  AcosExtGradFunc AcosExtGradFuncObj;
  PReLUGradFunc PReLUGradFuncObj;
  InplaceIndexAddExtGradFunc InplaceIndexAddExtGradFuncObj;
  InplaceExpGradFunc InplaceExpGradFuncObj;
  NotEqualGradFunc NotEqualGradFuncObj;
  FullLikeGradFunc FullLikeGradFuncObj;
  UnstackExtViewGradFunc UnstackExtViewGradFuncObj;
  SincGradFunc SincGradFuncObj;
  GeLUGradFunc GeLUGradFuncObj;
  TExtGradFunc TExtGradFuncObj;
  ArgMinExtGradFunc ArgMinExtGradFuncObj;
  AtanhGradFunc AtanhGradFuncObj;
  InplaceUniformGradFunc InplaceUniformGradFuncObj;
  GroupNormGradFunc GroupNormGradFuncObj;
  AsinhExtGradFunc AsinhExtGradFuncObj;
  SinhGradFunc SinhGradFuncObj;
  UpsampleBicubic2DGradFunc UpsampleBicubic2DGradFuncObj;
  BCEWithLogitsLossGradFunc BCEWithLogitsLossGradFuncObj;
  MaxPoolGradWithMaskGradFunc MaxPoolGradWithMaskGradFuncObj;
  UpsampleBicubic2DGradGradFunc UpsampleBicubic2DGradGradFuncObj;
  InplaceReLUGradFunc InplaceReLUGradFuncObj;
  NewZerosGradFunc NewZerosGradFuncObj;
  MaskedSelectGradGradFunc MaskedSelectGradGradFuncObj;
  MaxGradFunc MaxGradFuncObj;
  ReduceAnyGradFunc ReduceAnyGradFuncObj;
  AddExtGradFunc AddExtGradFuncObj;
  LerpScalarGradFunc LerpScalarGradFuncObj;
  AdaptiveAvgPool3DGradExtGradFunc AdaptiveAvgPool3DGradExtGradFuncObj;
  PowGradFunc PowGradFuncObj;
  FillScalarGradFunc FillScalarGradFuncObj;
  Conv2DPaddingGradFunc Conv2DPaddingGradFuncObj;
  UpsampleNearest3DGradGradFunc UpsampleNearest3DGradGradFuncObj;
  InplaceScatterValueReduceGradFunc InplaceScatterValueReduceGradFuncObj;
  InplaceDivModsGradFunc InplaceDivModsGradFuncObj;
  L1LossBackwardExtGradFunc L1LossBackwardExtGradFuncObj;
  SumExtGradFunc SumExtGradFuncObj;
  RotaryPositionEmbeddingGradFunc RotaryPositionEmbeddingGradFuncObj;
  Log10GradFunc Log10GradFuncObj;
  MaxPoolWithMaskGradFunc MaxPoolWithMaskGradFuncObj;
  InnerIndexGradFunc InnerIndexGradFuncObj;
  GreaterEqualScalarGradFunc GreaterEqualScalarGradFuncObj;
  InplaceClampScalarGradFunc InplaceClampScalarGradFuncObj;
  HardtanhGradGradFunc HardtanhGradGradFuncObj;
  InplaceRandomGradFunc InplaceRandomGradFuncObj;
  IndexGradFunc IndexGradFuncObj;
  InplaceFloorGradFunc InplaceFloorGradFuncObj;
  GluGradGradFunc GluGradGradFuncObj;
  LogicalXorGradFunc LogicalXorGradFuncObj;
  SwigluGradFunc SwigluGradFuncObj;
  SeLUExtGradFunc SeLUExtGradFuncObj;
  StackExtGradFunc StackExtGradFuncObj;
  NormalFloatTensorGradFunc NormalFloatTensorGradFuncObj;
  WeightQuantBatchMatmulGradFunc WeightQuantBatchMatmulGradFuncObj;
  GroupedMatmulV4GradFunc GroupedMatmulV4GradFuncObj;
  GroupedMatmulGradFunc GroupedMatmulGradFuncObj;
  MoeFinalizeRoutingGradFunc MoeFinalizeRoutingGradFuncObj;
  MoeGatingTopKSoftmaxGradFunc MoeGatingTopKSoftmaxGradFuncObj;
  GroupedMatmulV2GradFunc GroupedMatmulV2GradFuncObj;
  QuantV2GradFunc QuantV2GradFuncObj;
  KVCacheScatterUpdateGradFunc KVCacheScatterUpdateGradFuncObj;
  QuantBatchMatmulGradFunc QuantBatchMatmulGradFuncObj;
  DynamicQuantExtGradFunc DynamicQuantExtGradFuncObj;
  MoeInitRoutingGradFunc MoeInitRoutingGradFuncObj;
  AddRmsNormQuantV2GradFunc AddRmsNormQuantV2GradFuncObj;
  MoeInitRoutingV2GradFunc MoeInitRoutingV2GradFuncObj;
  MatmulAllReduceAddRmsNormGradFunc MatmulAllReduceAddRmsNormGradFuncObj;
  FusedInferAttentionScoreGradFunc FusedInferAttentionScoreGradFuncObj;
  MoeComputeExpertTokensGradFunc MoeComputeExpertTokensGradFuncObj;
  GmmBackwardFusionGradFunc GmmBackwardFusionGradFuncObj;
  GmmV2BackwardFusionGradFunc GmmV2BackwardFusionGradFuncObj;
  GmmV2GradFunc GmmV2GradFuncObj;
  GmmV2BackwardGradFunc GmmV2BackwardGradFuncObj;
  PixelShuffleGradFunc PixelShuffleGradFuncObj;
  GmmBackwardGradFunc GmmBackwardGradFuncObj;
  GmmGradFunc GmmGradFuncObj;
  InplaceExponentialGradFunc InplaceExponentialGradFuncObj;
};
}  // namespace pyboost
}  // namespace kernel
}  // namespace mindspore

#endif  // MINDSPORE_MINDSPORE_OPS_KERNEL_FUNCTIONS_AUTO_GENERATE_AUTO_GRAD_OP_REG_H_
