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
  kTanh = 0,
  kConvolutionStrGrad = 1,
  kExp2 = 2,
  kFlashAttentionScore = 3,
  kInplaceSubScalar = 4,
  kFloorDivScalar = 5,
  kUnique2 = 6,
  kGLU = 7,
  kCeil = 8,
  kAvgPool2DGrad = 9,
  kHSigmoidGrad = 10,
  kAsinhExt = 11,
  kL1LossBackwardExt = 12,
  kSplitTensorView = 13,
  kTExt = 14,
  kErfinv = 15,
  kUpsampleBilinear2DGrad = 16,
  kMatmulReduceScatter = 17,
  kInplaceElu = 18,
  kReplicationPad3D = 19,
  kChunkView = 20,
  kNLLLossGrad = 21,
  kRmsNormGrad = 22,
  kGatherD = 23,
  kInplaceClampTensor = 24,
  kInnerInplaceIndexPut = 25,
  kInplaceTanh = 26,
  kXLogYScalarSelf = 27,
  kConv3DPadding = 28,
  kLogicalXor = 29,
  kBitwiseNot = 30,
  kInplaceIndexAddExt = 31,
  kExpandAs = 32,
  kIsFinite = 33,
  kInplaceThreshold = 34,
  kConv1DPadding = 35,
  kInplaceCopy = 36,
  kInnerIndex = 37,
  kTranspose = 38,
  kUpsampleLinear1DGrad = 39,
  kArgMaxExt = 40,
  kMultiScaleDeformableAttn = 41,
  kSortExt = 42,
  kSqrt = 43,
  kExpandDims = 44,
  kDiv = 45,
  kUpsampleNearest1DGrad = 46,
  kSubScalar = 47,
  kSilentCheckV3 = 48,
  kLinalgVectorNorm = 49,
  kRotaryPositionEmbeddingGrad = 50,
  kLess = 51,
  kLeakyReLUGradExt = 52,
  kLog1p = 53,
  kIsNegInf = 54,
  kCol2ImGrad = 55,
  kBinaryCrossEntropyGrad = 56,
  kMishExt = 57,
  kAvgPool1D = 58,
  kLogicalOr = 59,
  kInplaceMaskedFillScalar = 60,
  kGridSampler2D = 61,
  kSiLUGrad = 62,
  kSplitTensor = 63,
  kTraceExt = 64,
  kTriangularSolve = 65,
  kFloorDiv = 66,
  kLogSoftmaxGrad = 67,
  kOuter = 68,
  kConcat = 69,
  kRound = 70,
  kReflectionPad2D = 71,
  kEluExt = 72,
  kClampScalar = 73,
  kLogSumExp = 74,
  kSplit = 75,
  kSeLUExt = 76,
  kLog2 = 77,
  kMishGradExt = 78,
  kPowTensorScalar = 79,
  kClampTensor = 80,
  kAddExt = 81,
  kStackExt = 82,
  kInplaceGroupedMatmulAdd = 83,
  kGeLUGrad = 84,
  kTile = 85,
  kBatchMatMulExt = 86,
  kOneHotExt = 87,
  kMultiScaleDeformableAttnGrad = 88,
  kBatchNormElemtGrad = 89,
  kTypeAs = 90,
  kNorm = 91,
  kEqualExt = 92,
  kElu = 93,
  kNLLLoss2d = 94,
  kBitwiseXorScalar = 95,
  kUpsampleLinear1D = 96,
  kBatchNormStats = 97,
  kPow = 98,
  kNotEqual = 99,
  kRandLikeExt = 100,
  kAdaptiveMaxPool1D = 101,
  kDropoutDoMaskExt = 102,
  kMaxDim = 103,
  kVarMean = 104,
  kSinc = 105,
  kNewZeros = 106,
  kAsStrided = 107,
  kInplaceIndexPut = 108,
  kBCEWithLogitsLoss = 109,
  kReflectionPad2DGrad = 110,
  kGreater = 111,
  kStdMean = 112,
  kMSELossExt = 113,
  kSwigluGrad = 114,
  kLayerNormExt = 115,
  kArgMinExt = 116,
  kDropoutGradExt = 117,
  kMeshgrid = 118,
  kSquare = 119,
  kZeros = 120,
  kInplaceScatterValue = 121,
  kInplaceDivs = 122,
  kTrilExt = 123,
  kDivMod = 124,
  kIndexFillScalar = 125,
  kProdExt = 126,
  kAdd = 127,
  kMinimum = 128,
  kLogAddExp = 129,
  kInplaceSubExt = 130,
  kSoftShrink = 131,
  kL1LossExt = 132,
  kHSwish = 133,
  kAdamW = 134,
  kInplacePut = 135,
  kScatterValue = 136,
  kScatter = 137,
  kHardtanhGrad = 138,
  kReflectionPad3D = 139,
  kMaxPoolGradWithMask = 140,
  kAllFinite = 141,
  kEmbedding = 142,
  kAvgPool3DExt = 143,
  kCol2ImExt = 144,
  kReverseV2 = 145,
  kFlattenExt = 146,
  kRepeatInterleaveGrad = 147,
  kUpsampleNearest2D = 148,
  kGreaterEqual = 149,
  kReplicationPad3DGrad = 150,
  kInplaceRandom = 151,
  kKLDiv = 152,
  kReLU = 153,
  kBitwiseOrScalar = 154,
  kAdaptiveAvgPool3DGradExt = 155,
  kIndexSelect = 156,
  kMaskedFill = 157,
  kBitwiseOrTensor = 158,
  kHSwishGrad = 159,
  kCountNonZero = 160,
  kSigmoidGrad = 161,
  kInplaceLog = 162,
  kNormalTensorFloat = 163,
  kHSigmoid = 164,
  kPowScalarTensor = 165,
  kSplitWithSizeView = 166,
  kAdaptiveMaxPool2D = 167,
  kGatherDGradV2 = 168,
  kInplaceAddsExt = 169,
  kLeakyReLUExt = 170,
  kReciprocal = 171,
  kInplaceNormal = 172,
  kAddScalar = 173,
  kEye = 174,
  kBatchMatMul = 175,
  kSinh = 176,
  kSoftMarginLossGrad = 177,
  kInplaceScatterSrc = 178,
  kUpsampleNearest3DGrad = 179,
  kCumsumExt = 180,
  kReshape = 181,
  kMm = 182,
  kGroupNormGrad = 183,
  kFFNExt = 184,
  kSpeedFusionAttention = 185,
  kEmbeddingDenseBackward = 186,
  kInplaceClampScalar = 187,
  kRepeatInterleaveInt = 188,
  kSearchSorted = 189,
  kAddRmsNorm = 190,
  kHardtanh = 191,
  kInplaceMul = 192,
  kView = 193,
  kInplaceScatterSrcReduce = 194,
  kOnesLikeExt = 195,
  kXlogy = 196,
  kCos = 197,
  kLessEqual = 198,
  kHistcExt = 199,
  kMaskedSelectGrad = 200,
  kSin = 201,
  kMaxPoolGradWithIndices = 202,
  kInplaceUniform = 203,
  kUpsampleBicubic2D = 204,
  kHShrinkGrad = 205,
  kMoeTokenUnpermuteGrad = 206,
  kFillTensor = 207,
  kNonZeroExt = 208,
  kInplaceFillScalar = 209,
  kNewOnes = 210,
  kAddbmm = 211,
  kNonZero = 212,
  kUniqueConsecutive = 213,
  kMuls = 214,
  kRandpermExt = 215,
  kInplaceErfinv = 216,
  kKthvalue = 217,
  kRandIntLike = 218,
  kGridSampler2DGrad = 219,
  kFloor = 220,
  kSlice = 221,
  kRandn = 222,
  kInplaceHardtanh = 223,
  kMSELossGradExt = 224,
  kInplaceMuls = 225,
  kInplaceFillDiagonal = 226,
  kBincountExt = 227,
  kMaskedSelect = 228,
  kCumminExt = 229,
  kBernoulliExt = 230,
  kInplaceScatterValueReduce = 231,
  kConv2DExt = 232,
  kAddmm = 233,
  kNarrowView = 234,
  kSumExt = 235,
  kReplicationPad1D = 236,
  kFlashAttentionScoreGrad = 237,
  kBatchNormElemt = 238,
  kBitwiseAndScalar = 239,
  kTransposeView = 240,
  kUpsampleBilinear2D = 241,
  kEluGradExt = 242,
  kUpsampleNearest2DGrad = 243,
  kContiguous = 244,
  kPReLU = 245,
  kIncreFlashAttention = 246,
  kConvolutionGrad = 247,
  kMultinomialExt = 248,
  kReplicationPad2DGrad = 249,
  kSelect = 250,
  kCross = 251,
  kBatchNormGradExt = 252,
  kTan = 253,
  kCopy = 254,
  kErfc = 255,
  kLinalgQr = 256,
  kAtan2Ext = 257,
  kLogSoftmax = 258,
  kExp = 259,
  kRandnLike = 260,
  kMeanExt = 261,
  kDropoutExt = 262,
  kFmodScalar = 263,
  kAddmv = 264,
  kAbs = 265,
  kThreshold = 266,
  kThresholdGrad = 267,
  kRemainderScalarTensor = 268,
  kArgMaxWithValue = 269,
  kSoftplusGradExt = 270,
  kTriu = 271,
  kInplaceFloorDivide = 272,
  kUniformExt = 273,
  kReplicationPad2D = 274,
  kInplaceMaskedFillTensor = 275,
  kEqual = 276,
  kTanhGrad = 277,
  kUpsampleNearest1D = 278,
  kRandInt = 279,
  kSpeedFusionAttentionGrad = 280,
  kAdaptiveAvgPool2DExt = 281,
  kMul = 282,
  kSmoothL1LossGrad = 283,
  kGenerator = 284,
  kSeluGrad = 285,
  kGroupNorm = 286,
  kDivMods = 287,
  kPromptFlashAttention = 288,
  kMoeTokenPermute = 289,
  kBinaryCrossEntropy = 290,
  kDivs = 291,
  kDense = 292,
  kTransposeExtView = 293,
  kConvolution = 294,
  kNormalFloatTensor = 295,
  kReduceAll = 296,
  kXLogYScalarOther = 297,
  kMv = 298,
  kTopkExt = 299,
  kSliceExtView = 300,
  kRepeat = 301,
  kAtanExt = 302,
  kIsInf = 303,
  kMatrixInverseExt = 304,
  kAdaptiveAvgPool1D = 305,
  kSplitWithSize = 306,
  kRotaryPositionEmbedding = 307,
  kRandExt = 308,
  kAsinExt = 309,
  kConvTranspose2D = 310,
  kInplaceFillTensor = 311,
  kReflectionPad1D = 312,
  kGeLU = 313,
  kBitwiseXorTensor = 314,
  kNeg = 315,
  kMoeTokenUnpermute = 316,
  kInplaceZero = 317,
  kIndexAddExt = 318,
  kConv1DExt = 319,
  kIsClose = 320,
  kAddLayerNormV2 = 321,
  kNormalTensorTensor = 322,
  kAdaptiveAvgPool2DGradExt = 323,
  kSqueeze = 324,
  kExpandDimsView = 325,
  kGeluExt = 326,
  kAvgPool3DGradExt = 327,
  kInplaceExp = 328,
  kUpsampleNearest3D = 329,
  kReduceMin = 330,
  kAcoshExt = 331,
  kSmoothL1Loss = 332,
  kInplaceAddExt = 333,
  kSliceExt = 334,
  kBroadcastToView = 335,
  kKLDivGrad = 336,
  kDiagExt = 337,
  kConv2DPadding = 338,
  kMedianDim = 339,
  kFrac = 340,
  kScatterAddExt = 341,
  kLerp = 342,
  kRsqrt = 343,
  kNLLLoss2dGrad = 344,
  kClone = 345,
  kZerosLikeExt = 346,
  kLog = 347,
  kMaxPoolWithMask = 348,
  kGluGrad = 349,
  kViewAs = 350,
  kRmsNorm = 351,
  kSoftmaxBackward = 352,
  kArange = 353,
  kInnerNonZero = 354,
  kGeluGradExt = 355,
  kInplaceDiv = 356,
  kConv3DExt = 357,
  kTrunc = 358,
  kCustomExt = 359,
  kPReLUGrad = 360,
  kNLLLoss = 361,
  kBatchNormExt = 362,
  kInplaceReLU = 363,
  kIndexFillTensor = 364,
  kRemainderTensorTensor = 365,
  kSwiglu = 366,
  kDropoutGenMaskExt = 367,
  kLinSpaceExt = 368,
  kInplaceAddmm = 369,
  kIm2ColExt = 370,
  kBaddbmm = 371,
  kGreaterEqualScalar = 372,
  kSoftplusExt = 373,
  kAddcdivExt = 374,
  kHShrink = 375,
  kAllGatherMatmul = 376,
  kSelectExtView = 377,
  kIdentity = 378,
  kReduceAny = 379,
  kMin = 380,
  kCast = 381,
  kUnstackExtView = 382,
  kSubExt = 383,
  kChunk = 384,
  kMax = 385,
  kLog10 = 386,
  kMaximum = 387,
  kLogSoftmaxExt = 388,
  kSoftmax = 389,
  kNormalFloatFloat = 390,
  kLayerNormGradExt = 391,
  kBinaryCrossEntropyWithLogitsBackward = 392,
  kMaxPoolWithIndices = 393,
  kRoll = 394,
  kSoftMarginLoss = 395,
  kVar = 396,
  kAtanh = 397,
  kMedianExt = 398,
  kFullLike = 399,
  kFmodTensor = 400,
  kRemainderTensorScalar = 401,
  kLogSigmoidGrad = 402,
  kInplaceFloorDivides = 403,
  kInplaceFloor = 404,
  kAcosExt = 405,
  kSiLU = 406,
  kUpsampleTrilinear3DGrad = 407,
  kAvgPool2D = 408,
  kInplaceScatterAdd = 409,
  kSigmoid = 410,
  kSub = 411,
  kOnes = 412,
  kReduceMax = 413,
  kIndex = 414,
  kCosh = 415,
  kMatMul = 416,
  kInplaceDivMod = 417,
  kSelectV2 = 418,
  kMaxUnpool2DExt = 419,
  kBroadcastTo = 420,
  kUniqueDim = 421,
  kMoeTokenPermuteGrad = 422,
  kSoftShrinkGrad = 423,
  kBatchNormGatherStatsWithCounts = 424,
  kLerpScalar = 425,
  kArgSort = 426,
  kStd = 427,
  kReplicationPad1DGrad = 428,
  kNarrow = 429,
  kPolar = 430,
  kCummax = 431,
  kReflectionPad1DGrad = 432,
  kInplaceDivMods = 433,
  kBatchNormReduceGrad = 434,
  kTensorScatterElements = 435,
  kConvolutionStr = 436,
  kLogicalNot = 437,
  kNanToNum = 438,
  kInplaceStopGradient = 439,
  kExpm1 = 440,
  kAddcmulExt = 441,
  kTake = 442,
  kArgMinWithValue = 443,
  kConstantPadND = 444,
  kGcd = 445,
  kBitwiseAndTensor = 446,
  kLogAddExp2 = 447,
  kDot = 448,
  kGridSampler3DGrad = 449,
  kAdaptiveAvgPool3DExt = 450,
  kSilentCheckV2 = 451,
  kLogicalAnd = 452,
  kGridSampler3D = 453,
  kFillScalar = 454,
  kNansum = 455,
  kRepeatInterleaveTensor = 456,
  kUpsampleTrilinear3D = 457,
  kReluGrad = 458,
  kSign = 459,
  kMinDim = 460,
  kNeScalar = 461,
  kReflectionPad3DGrad = 462,
  kMatMulExt = 463,
  kErf = 464,
  kLogSigmoid = 465,
  kAddLayerNormGrad = 466,
  kUpsampleBicubic2DGrad = 467,
  kKVCacheScatterUpdate = 468,
  kGroupedMatmulV2 = 469,
  kMatmulAllReduceAddRmsNorm = 470,
  kMoeInitRouting = 471,
  kMoeFinalizeRouting = 472,
  kQuantBatchMatmul = 473,
  kQuantV2 = 474,
  kMoeInitRoutingV2 = 475,
  kAddRmsNormQuantV2 = 476,
  kWeightQuantBatchMatmul = 477,
  kGroupedMatmulV4 = 478,
  kGroupedMatmul = 479,
  kMoeGatingTopKSoftmax = 480,
  kDynamicQuantExt = 481,
  kFusedInferAttentionScore = 482,
  kMoeComputeExpertTokens = 483,
  kInplaceExponential = 484,
  kGmm = 485,
  kPixelShuffle = 486,
  kGmmBackward = 487,
  kGmmV2Backward = 488,
  kGmmV2BackwardFusion = 489,
  kGmmV2 = 490,
  kGmmBackwardFusion = 491,
};

using TanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ConvolutionStrGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &)>;
using Exp2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FlashAttentionScoreGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceSubScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using FloorDivScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using Unique2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using GLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using CeilGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AvgPool2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using HSigmoidGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AsinhExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using L1LossBackwardExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using SplitTensorViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using TExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ErfinvGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleBilinear2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using MatmulReduceScatterGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::StringImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using InplaceEluGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using ReplicationPad3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using ChunkViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using NLLLossGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using RmsNormGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GatherDGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceClampTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using InnerInplaceIndexPutGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &)>;
using InplaceTanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using XLogYScalarSelfGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Conv3DPaddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using LogicalXorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BitwiseNotGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceIndexAddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ExpandAsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IsFiniteGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceThresholdGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &)>;
using Conv1DPaddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using InplaceCopyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InnerIndexGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using TransposeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using UpsampleLinear1DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using ArgMaxExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &)>;
using MultiScaleDeformableAttnGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SortExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using SqrtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ExpandDimsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using DivGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleNearest1DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using SubScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using SilentCheckV3GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &)>;
using LinalgVectorNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using RotaryPositionEmbeddingGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using LessGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LeakyReLUGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::BoolImmPtr &)>;
using Log1pGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IsNegInfGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Col2ImGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &)>;
using BinaryCrossEntropyGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using MishExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AvgPool1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using LogicalOrGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceMaskedFillScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using GridSampler2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using SiLUGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SplitTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using TraceExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TriangularSolveGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using FloorDivGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSoftmaxGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using OuterGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ConcatGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using RoundGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using ReflectionPad2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using EluExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using ClampScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ScalarPtr> &, const std::optional<mindspore::ScalarPtr> &)>;
using LogSumExpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &)>;
using SplitGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using SeLUExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Log2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MishGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using PowTensorScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ClampTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using AddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using StackExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using InplaceGroupedMatmulAddGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GeLUGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TileGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using BatchMatMulExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using OneHotExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using MultiScaleDeformableAttnGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BatchNormElemtGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TypeAsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using EqualExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using EluGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using NLLLoss2dGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using BitwiseXorScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using UpsampleLinear1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using BatchNormStatsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using PowGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NotEqualGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RandLikeExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using AdaptiveMaxPool1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using DropoutDoMaskExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using MaxDimGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using VarMeanGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using SincGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NewZerosGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using AsStridedGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using InplaceIndexPutGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &)>;
using BCEWithLogitsLossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using ReflectionPad2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using GreaterGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using StdMeanGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using MSELossExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using SwigluGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using LayerNormExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &)>;
using ArgMinExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &)>;
using DropoutGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using MeshgridGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using SquareGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ZerosGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using InplaceScatterValueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using InplaceDivsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using TrilExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using DivModGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using IndexFillScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ProdExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using AddGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MinimumGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogAddExpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceSubExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using SoftShrinkGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using L1LossExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using HSwishGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AdamWGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using InplacePutGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &)>;
using ScatterValueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::Int64ImmPtr &)>;
using ScatterGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using HardtanhGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using ReflectionPad3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using MaxPoolGradWithMaskGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using AllFiniteGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &)>;
using EmbeddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const std::optional<mindspore::FP32ImmPtr> &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &)>;
using AvgPool3DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using Col2ImExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &)>;
using ReverseV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using FlattenExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using RepeatInterleaveGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using UpsampleNearest2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using GreaterEqualGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReplicationPad3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceRandomGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using KLDivGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using ReLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BitwiseOrScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using AdaptiveAvgPool3DGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IndexSelectGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaskedFillGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BitwiseOrTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using HSwishGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CountNonZeroGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using SigmoidGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceLogGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NormalTensorFloatGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using HSigmoidGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using PowScalarTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SplitWithSizeViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using AdaptiveMaxPool2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using GatherDGradV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceAddsExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using LeakyReLUExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ReciprocalGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceNormalGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AddScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using EyeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using BatchMatMulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using SinhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SoftMarginLossGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceScatterSrcGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleNearest3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using CumsumExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ReshapeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using MmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GroupNormGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using FFNExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using SpeedFusionAttentionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using EmbeddingDenseBackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &)>;
using InplaceClampScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ScalarPtr> &, const std::optional<mindspore::ScalarPtr> &)>;
using RepeatInterleaveIntGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &, const std::optional<mindspore::Int64ImmPtr> &)>;
using SearchSortedGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using AddRmsNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using HardtanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using InplaceMulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceScatterSrcReduceGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using OnesLikeExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using XlogyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CosGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LessEqualGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using HistcExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using MaskedSelectGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SinGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaxPoolGradWithIndicesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceUniformGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleBicubic2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using HShrinkGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using MoeTokenUnpermuteGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using FillTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using NonZeroExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceFillScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using NewOnesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using AddbmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using NonZeroGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UniqueConsecutiveGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using MulsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using RandpermExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceErfinvGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using KthvalueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using RandIntLikeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using GridSampler2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &)>;
using FloorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SliceGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &)>;
using RandnGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using InplaceHardtanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using MSELossGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceMulsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using InplaceFillDiagonalGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::BoolImmPtr &)>;
using BincountExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using MaskedSelectGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CumminExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using BernoulliExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceScatterValueReduceGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::Int64ImmPtr &)>;
using Conv2DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using AddmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using NarrowViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using SumExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ReplicationPad1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using FlashAttentionScoreGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using BatchNormElemtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &)>;
using BitwiseAndScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using TransposeViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using UpsampleBilinear2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using EluGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &)>;
using UpsampleNearest2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using ContiguousGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using PReLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IncreFlashAttentionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using ConvolutionGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &)>;
using MultinomialExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReplicationPad2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using SelectGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CrossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using BatchNormGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::ValueTuplePtr &)>;
using TanGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CopyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ErfcGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LinalgQrGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using Atan2ExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSoftmaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using ExpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RandnLikeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using MeanExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using DropoutExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FmodScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using AddmvGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using AbsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ThresholdGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &)>;
using ThresholdGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using RemainderScalarTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ArgMaxWithValueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using SoftplusGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using TriuGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceFloorDivideGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UniformExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReplicationPad2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceMaskedFillTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using EqualGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TanhGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleNearest1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using RandIntGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using SpeedFusionAttentionGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using AdaptiveAvgPool2DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using MulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SmoothL1LossGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GeneratorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &)>;
using SeluGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GroupNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &)>;
using DivModsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using PromptFlashAttentionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using MoeTokenPermuteGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const mindspore::BoolImmPtr &)>;
using BinaryCrossEntropyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using DivsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using DenseGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using TransposeExtViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using ConvolutionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using NormalFloatTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::FP32ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReduceAllGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using XLogYScalarOtherGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using MvGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using TopkExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using SliceExtViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using RepeatGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using AtanExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IsInfGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MatrixInverseExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AdaptiveAvgPool1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using SplitWithSizeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using RotaryPositionEmbeddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using RandExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using AsinExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ConvTranspose2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceFillTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReflectionPad1DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using GeLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BitwiseXorTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NegGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MoeTokenUnpermuteGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using InplaceZeroGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IndexAddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using Conv1DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using IsCloseGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &)>;
using AddLayerNormV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::BoolImmPtr &)>;
using NormalTensorTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AdaptiveAvgPool2DGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SqueezeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using ExpandDimsViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using GeluExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using AvgPool3DGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using InplaceExpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleNearest3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &)>;
using ReduceMinGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &)>;
using AcoshExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SmoothL1LossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceAddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using SliceExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using BroadcastToViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using KLDivGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using DiagExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using Conv2DPaddingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using MedianDimGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using FracGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ScatterAddExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LerpGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RsqrtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NLLLoss2dGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CloneGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ZerosLikeExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using LogGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaxPoolWithMaskGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using GluGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using ViewAsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RmsNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using SoftmaxBackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using ArangeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using InnerNonZeroGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GeluGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceDivGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Conv3DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using TruncGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CustomExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &)>;
using PReLUGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NLLLossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using BatchNormExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &)>;
using InplaceReLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using IndexFillTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RemainderTensorTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SwigluGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using DropoutGenMaskExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::FP32ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using LinSpaceExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using InplaceAddmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using Im2ColExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &)>;
using BaddbmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using GreaterEqualScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using SoftplusExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &)>;
using AddcdivExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using HShrinkGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using AllGatherMatmulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::StringImmPtr &, const mindspore::Int64ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using SelectExtViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using IdentityGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ReduceAnyGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &)>;
using MinGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CastGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using UnstackExtViewGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using SubExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ChunkGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using MaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Log10GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaximumGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSoftmaxExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const std::optional<mindspore::Int64ImmPtr> &)>;
using SoftmaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using NormalFloatFloatGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ScalarPtr &, const mindspore::ScalarPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LayerNormGradExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using BinaryCrossEntropyWithLogitsBackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using MaxPoolWithIndicesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using RollGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using SoftMarginLossGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using VarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using AtanhGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MedianExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using FullLikeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using FmodTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using RemainderTensorScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using LogSigmoidGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using InplaceFloorDividesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using InplaceFloorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AcosExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SiLUGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleTrilinear3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using AvgPool2DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using InplaceScatterAddGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SigmoidGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SubGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using OnesGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using ReduceMaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &)>;
using IndexGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using CoshGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MatMulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using InplaceDivModGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using SelectV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MaxUnpool2DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &)>;
using BroadcastToGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using UniqueDimGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using MoeTokenPermuteGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using SoftShrinkGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using BatchNormGatherStatsWithCountsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using LerpScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using ArgSortGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using StdGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using ReplicationPad1DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using NarrowGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using PolarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using CummaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using ReflectionPad1DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using InplaceDivModsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using BatchNormReduceGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using TensorScatterElementsGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using ConvolutionStrGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &, const mindspore::Int64ImmPtr &)>;
using LogicalNotGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using NanToNumGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::FP32ImmPtr> &, const std::optional<mindspore::FP32ImmPtr> &, const std::optional<mindspore::FP32ImmPtr> &)>;
using InplaceStopGradientGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using Expm1GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AddcmulExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using TakeGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ArgMinWithValueGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using ConstantPadNDGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ScalarPtr &)>;
using GcdGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using BitwiseAndTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogAddExp2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using DotGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GridSampler3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::ValueTuplePtr &)>;
using AdaptiveAvgPool3DExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using SilentCheckV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &)>;
using LogicalAndGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GridSampler3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using FillScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ScalarPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using NansumGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &, const std::optional<mindspore::Int64ImmPtr> &)>;
using RepeatInterleaveTensorGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::Int64ImmPtr> &, const std::optional<mindspore::Int64ImmPtr> &)>;
using UpsampleTrilinear3DGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using ReluGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using SignGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using MinDimGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using NeScalarGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &)>;
using ReflectionPad3DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &)>;
using MatMulExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using ErfGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using LogSigmoidGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using AddLayerNormGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using UpsampleBicubic2DGradGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::BoolImmPtr &)>;
using KVCacheScatterUpdateGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GroupedMatmulV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using MatmulAllReduceAddRmsNormGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &, const mindspore::StringImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using MoeInitRoutingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using MoeFinalizeRoutingGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using QuantBatchMatmulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using QuantV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using MoeInitRoutingV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &)>;
using AddRmsNormQuantV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::FP32ImmPtr &)>;
using WeightQuantBatchMatmulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &)>;
using GroupedMatmulV4GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GroupedMatmulGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::BoolImmPtr &)>;
using MoeGatingTopKSoftmaxGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using DynamicQuantExtGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &)>;
using FusedInferAttentionScoreGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::FP32ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::BoolImmPtr &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using MoeComputeExpertTokensGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using InplaceExponentialGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::ScalarPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::tensor::BaseTensorPtr &)>;
using GmmGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using PixelShuffleGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::tensor::BaseTensorPtr &, const mindspore::Int64ImmPtr &)>;
using GmmBackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &)>;
using GmmV2BackwardGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using GmmV2BackwardFusionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &)>;
using GmmV2GradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const std::optional<mindspore::tensor::BaseTensorPtr> &, const mindspore::Int64ImmPtr &, const mindspore::Int64ImmPtr &)>;
using GmmBackwardFusionGradFunc = std::function<void(const kernel::pyboost::OpPtr &, const mindspore::ValueTuplePtr &, const mindspore::ValueTuplePtr &, const std::optional<mindspore::ValueTuplePtr> &, const mindspore::Int64ImmPtr &)>;

struct OpsAutoGradRegisters {
  TanhGradFunc TanhGradFuncObj;
  ConvolutionStrGradGradFunc ConvolutionStrGradGradFuncObj;
  Exp2GradFunc Exp2GradFuncObj;
  FlashAttentionScoreGradFunc FlashAttentionScoreGradFuncObj;
  InplaceSubScalarGradFunc InplaceSubScalarGradFuncObj;
  FloorDivScalarGradFunc FloorDivScalarGradFuncObj;
  Unique2GradFunc Unique2GradFuncObj;
  GLUGradFunc GLUGradFuncObj;
  CeilGradFunc CeilGradFuncObj;
  AvgPool2DGradGradFunc AvgPool2DGradGradFuncObj;
  HSigmoidGradGradFunc HSigmoidGradGradFuncObj;
  AsinhExtGradFunc AsinhExtGradFuncObj;
  L1LossBackwardExtGradFunc L1LossBackwardExtGradFuncObj;
  SplitTensorViewGradFunc SplitTensorViewGradFuncObj;
  TExtGradFunc TExtGradFuncObj;
  ErfinvGradFunc ErfinvGradFuncObj;
  UpsampleBilinear2DGradGradFunc UpsampleBilinear2DGradGradFuncObj;
  MatmulReduceScatterGradFunc MatmulReduceScatterGradFuncObj;
  InplaceEluGradFunc InplaceEluGradFuncObj;
  ReplicationPad3DGradFunc ReplicationPad3DGradFuncObj;
  ChunkViewGradFunc ChunkViewGradFuncObj;
  NLLLossGradGradFunc NLLLossGradGradFuncObj;
  RmsNormGradGradFunc RmsNormGradGradFuncObj;
  GatherDGradFunc GatherDGradFuncObj;
  InplaceClampTensorGradFunc InplaceClampTensorGradFuncObj;
  InnerInplaceIndexPutGradFunc InnerInplaceIndexPutGradFuncObj;
  InplaceTanhGradFunc InplaceTanhGradFuncObj;
  XLogYScalarSelfGradFunc XLogYScalarSelfGradFuncObj;
  Conv3DPaddingGradFunc Conv3DPaddingGradFuncObj;
  LogicalXorGradFunc LogicalXorGradFuncObj;
  BitwiseNotGradFunc BitwiseNotGradFuncObj;
  InplaceIndexAddExtGradFunc InplaceIndexAddExtGradFuncObj;
  ExpandAsGradFunc ExpandAsGradFuncObj;
  IsFiniteGradFunc IsFiniteGradFuncObj;
  InplaceThresholdGradFunc InplaceThresholdGradFuncObj;
  Conv1DPaddingGradFunc Conv1DPaddingGradFuncObj;
  InplaceCopyGradFunc InplaceCopyGradFuncObj;
  InnerIndexGradFunc InnerIndexGradFuncObj;
  TransposeGradFunc TransposeGradFuncObj;
  UpsampleLinear1DGradGradFunc UpsampleLinear1DGradGradFuncObj;
  ArgMaxExtGradFunc ArgMaxExtGradFuncObj;
  MultiScaleDeformableAttnGradFunc MultiScaleDeformableAttnGradFuncObj;
  SortExtGradFunc SortExtGradFuncObj;
  SqrtGradFunc SqrtGradFuncObj;
  ExpandDimsGradFunc ExpandDimsGradFuncObj;
  DivGradFunc DivGradFuncObj;
  UpsampleNearest1DGradGradFunc UpsampleNearest1DGradGradFuncObj;
  SubScalarGradFunc SubScalarGradFuncObj;
  SilentCheckV3GradFunc SilentCheckV3GradFuncObj;
  LinalgVectorNormGradFunc LinalgVectorNormGradFuncObj;
  RotaryPositionEmbeddingGradGradFunc RotaryPositionEmbeddingGradGradFuncObj;
  LessGradFunc LessGradFuncObj;
  LeakyReLUGradExtGradFunc LeakyReLUGradExtGradFuncObj;
  Log1pGradFunc Log1pGradFuncObj;
  IsNegInfGradFunc IsNegInfGradFuncObj;
  Col2ImGradGradFunc Col2ImGradGradFuncObj;
  BinaryCrossEntropyGradGradFunc BinaryCrossEntropyGradGradFuncObj;
  MishExtGradFunc MishExtGradFuncObj;
  AvgPool1DGradFunc AvgPool1DGradFuncObj;
  LogicalOrGradFunc LogicalOrGradFuncObj;
  InplaceMaskedFillScalarGradFunc InplaceMaskedFillScalarGradFuncObj;
  GridSampler2DGradFunc GridSampler2DGradFuncObj;
  SiLUGradGradFunc SiLUGradGradFuncObj;
  SplitTensorGradFunc SplitTensorGradFuncObj;
  TraceExtGradFunc TraceExtGradFuncObj;
  TriangularSolveGradFunc TriangularSolveGradFuncObj;
  FloorDivGradFunc FloorDivGradFuncObj;
  LogSoftmaxGradGradFunc LogSoftmaxGradGradFuncObj;
  OuterGradFunc OuterGradFuncObj;
  ConcatGradFunc ConcatGradFuncObj;
  RoundGradFunc RoundGradFuncObj;
  ReflectionPad2DGradFunc ReflectionPad2DGradFuncObj;
  EluExtGradFunc EluExtGradFuncObj;
  ClampScalarGradFunc ClampScalarGradFuncObj;
  LogSumExpGradFunc LogSumExpGradFuncObj;
  SplitGradFunc SplitGradFuncObj;
  SeLUExtGradFunc SeLUExtGradFuncObj;
  Log2GradFunc Log2GradFuncObj;
  MishGradExtGradFunc MishGradExtGradFuncObj;
  PowTensorScalarGradFunc PowTensorScalarGradFuncObj;
  ClampTensorGradFunc ClampTensorGradFuncObj;
  AddExtGradFunc AddExtGradFuncObj;
  StackExtGradFunc StackExtGradFuncObj;
  InplaceGroupedMatmulAddGradFunc InplaceGroupedMatmulAddGradFuncObj;
  GeLUGradGradFunc GeLUGradGradFuncObj;
  TileGradFunc TileGradFuncObj;
  BatchMatMulExtGradFunc BatchMatMulExtGradFuncObj;
  OneHotExtGradFunc OneHotExtGradFuncObj;
  MultiScaleDeformableAttnGradGradFunc MultiScaleDeformableAttnGradGradFuncObj;
  BatchNormElemtGradGradFunc BatchNormElemtGradGradFuncObj;
  TypeAsGradFunc TypeAsGradFuncObj;
  NormGradFunc NormGradFuncObj;
  EqualExtGradFunc EqualExtGradFuncObj;
  EluGradFunc EluGradFuncObj;
  NLLLoss2dGradFunc NLLLoss2dGradFuncObj;
  BitwiseXorScalarGradFunc BitwiseXorScalarGradFuncObj;
  UpsampleLinear1DGradFunc UpsampleLinear1DGradFuncObj;
  BatchNormStatsGradFunc BatchNormStatsGradFuncObj;
  PowGradFunc PowGradFuncObj;
  NotEqualGradFunc NotEqualGradFuncObj;
  RandLikeExtGradFunc RandLikeExtGradFuncObj;
  AdaptiveMaxPool1DGradFunc AdaptiveMaxPool1DGradFuncObj;
  DropoutDoMaskExtGradFunc DropoutDoMaskExtGradFuncObj;
  MaxDimGradFunc MaxDimGradFuncObj;
  VarMeanGradFunc VarMeanGradFuncObj;
  SincGradFunc SincGradFuncObj;
  NewZerosGradFunc NewZerosGradFuncObj;
  AsStridedGradFunc AsStridedGradFuncObj;
  InplaceIndexPutGradFunc InplaceIndexPutGradFuncObj;
  BCEWithLogitsLossGradFunc BCEWithLogitsLossGradFuncObj;
  ReflectionPad2DGradGradFunc ReflectionPad2DGradGradFuncObj;
  GreaterGradFunc GreaterGradFuncObj;
  StdMeanGradFunc StdMeanGradFuncObj;
  MSELossExtGradFunc MSELossExtGradFuncObj;
  SwigluGradGradFunc SwigluGradGradFuncObj;
  LayerNormExtGradFunc LayerNormExtGradFuncObj;
  ArgMinExtGradFunc ArgMinExtGradFuncObj;
  DropoutGradExtGradFunc DropoutGradExtGradFuncObj;
  MeshgridGradFunc MeshgridGradFuncObj;
  SquareGradFunc SquareGradFuncObj;
  ZerosGradFunc ZerosGradFuncObj;
  InplaceScatterValueGradFunc InplaceScatterValueGradFuncObj;
  InplaceDivsGradFunc InplaceDivsGradFuncObj;
  TrilExtGradFunc TrilExtGradFuncObj;
  DivModGradFunc DivModGradFuncObj;
  IndexFillScalarGradFunc IndexFillScalarGradFuncObj;
  ProdExtGradFunc ProdExtGradFuncObj;
  AddGradFunc AddGradFuncObj;
  MinimumGradFunc MinimumGradFuncObj;
  LogAddExpGradFunc LogAddExpGradFuncObj;
  InplaceSubExtGradFunc InplaceSubExtGradFuncObj;
  SoftShrinkGradFunc SoftShrinkGradFuncObj;
  L1LossExtGradFunc L1LossExtGradFuncObj;
  HSwishGradFunc HSwishGradFuncObj;
  AdamWGradFunc AdamWGradFuncObj;
  InplacePutGradFunc InplacePutGradFuncObj;
  ScatterValueGradFunc ScatterValueGradFuncObj;
  ScatterGradFunc ScatterGradFuncObj;
  HardtanhGradGradFunc HardtanhGradGradFuncObj;
  ReflectionPad3DGradFunc ReflectionPad3DGradFuncObj;
  MaxPoolGradWithMaskGradFunc MaxPoolGradWithMaskGradFuncObj;
  AllFiniteGradFunc AllFiniteGradFuncObj;
  EmbeddingGradFunc EmbeddingGradFuncObj;
  AvgPool3DExtGradFunc AvgPool3DExtGradFuncObj;
  Col2ImExtGradFunc Col2ImExtGradFuncObj;
  ReverseV2GradFunc ReverseV2GradFuncObj;
  FlattenExtGradFunc FlattenExtGradFuncObj;
  RepeatInterleaveGradGradFunc RepeatInterleaveGradGradFuncObj;
  UpsampleNearest2DGradFunc UpsampleNearest2DGradFuncObj;
  GreaterEqualGradFunc GreaterEqualGradFuncObj;
  ReplicationPad3DGradGradFunc ReplicationPad3DGradGradFuncObj;
  InplaceRandomGradFunc InplaceRandomGradFuncObj;
  KLDivGradFunc KLDivGradFuncObj;
  ReLUGradFunc ReLUGradFuncObj;
  BitwiseOrScalarGradFunc BitwiseOrScalarGradFuncObj;
  AdaptiveAvgPool3DGradExtGradFunc AdaptiveAvgPool3DGradExtGradFuncObj;
  IndexSelectGradFunc IndexSelectGradFuncObj;
  MaskedFillGradFunc MaskedFillGradFuncObj;
  BitwiseOrTensorGradFunc BitwiseOrTensorGradFuncObj;
  HSwishGradGradFunc HSwishGradGradFuncObj;
  CountNonZeroGradFunc CountNonZeroGradFuncObj;
  SigmoidGradGradFunc SigmoidGradGradFuncObj;
  InplaceLogGradFunc InplaceLogGradFuncObj;
  NormalTensorFloatGradFunc NormalTensorFloatGradFuncObj;
  HSigmoidGradFunc HSigmoidGradFuncObj;
  PowScalarTensorGradFunc PowScalarTensorGradFuncObj;
  SplitWithSizeViewGradFunc SplitWithSizeViewGradFuncObj;
  AdaptiveMaxPool2DGradFunc AdaptiveMaxPool2DGradFuncObj;
  GatherDGradV2GradFunc GatherDGradV2GradFuncObj;
  InplaceAddsExtGradFunc InplaceAddsExtGradFuncObj;
  LeakyReLUExtGradFunc LeakyReLUExtGradFuncObj;
  ReciprocalGradFunc ReciprocalGradFuncObj;
  InplaceNormalGradFunc InplaceNormalGradFuncObj;
  AddScalarGradFunc AddScalarGradFuncObj;
  EyeGradFunc EyeGradFuncObj;
  BatchMatMulGradFunc BatchMatMulGradFuncObj;
  SinhGradFunc SinhGradFuncObj;
  SoftMarginLossGradGradFunc SoftMarginLossGradGradFuncObj;
  InplaceScatterSrcGradFunc InplaceScatterSrcGradFuncObj;
  UpsampleNearest3DGradGradFunc UpsampleNearest3DGradGradFuncObj;
  CumsumExtGradFunc CumsumExtGradFuncObj;
  ReshapeGradFunc ReshapeGradFuncObj;
  MmGradFunc MmGradFuncObj;
  GroupNormGradGradFunc GroupNormGradGradFuncObj;
  FFNExtGradFunc FFNExtGradFuncObj;
  SpeedFusionAttentionGradFunc SpeedFusionAttentionGradFuncObj;
  EmbeddingDenseBackwardGradFunc EmbeddingDenseBackwardGradFuncObj;
  InplaceClampScalarGradFunc InplaceClampScalarGradFuncObj;
  RepeatInterleaveIntGradFunc RepeatInterleaveIntGradFuncObj;
  SearchSortedGradFunc SearchSortedGradFuncObj;
  AddRmsNormGradFunc AddRmsNormGradFuncObj;
  HardtanhGradFunc HardtanhGradFuncObj;
  InplaceMulGradFunc InplaceMulGradFuncObj;
  ViewGradFunc ViewGradFuncObj;
  InplaceScatterSrcReduceGradFunc InplaceScatterSrcReduceGradFuncObj;
  OnesLikeExtGradFunc OnesLikeExtGradFuncObj;
  XlogyGradFunc XlogyGradFuncObj;
  CosGradFunc CosGradFuncObj;
  LessEqualGradFunc LessEqualGradFuncObj;
  HistcExtGradFunc HistcExtGradFuncObj;
  MaskedSelectGradGradFunc MaskedSelectGradGradFuncObj;
  SinGradFunc SinGradFuncObj;
  MaxPoolGradWithIndicesGradFunc MaxPoolGradWithIndicesGradFuncObj;
  InplaceUniformGradFunc InplaceUniformGradFuncObj;
  UpsampleBicubic2DGradFunc UpsampleBicubic2DGradFuncObj;
  HShrinkGradGradFunc HShrinkGradGradFuncObj;
  MoeTokenUnpermuteGradGradFunc MoeTokenUnpermuteGradGradFuncObj;
  FillTensorGradFunc FillTensorGradFuncObj;
  NonZeroExtGradFunc NonZeroExtGradFuncObj;
  InplaceFillScalarGradFunc InplaceFillScalarGradFuncObj;
  NewOnesGradFunc NewOnesGradFuncObj;
  AddbmmGradFunc AddbmmGradFuncObj;
  NonZeroGradFunc NonZeroGradFuncObj;
  UniqueConsecutiveGradFunc UniqueConsecutiveGradFuncObj;
  MulsGradFunc MulsGradFuncObj;
  RandpermExtGradFunc RandpermExtGradFuncObj;
  InplaceErfinvGradFunc InplaceErfinvGradFuncObj;
  KthvalueGradFunc KthvalueGradFuncObj;
  RandIntLikeGradFunc RandIntLikeGradFuncObj;
  GridSampler2DGradGradFunc GridSampler2DGradGradFuncObj;
  FloorGradFunc FloorGradFuncObj;
  SliceGradFunc SliceGradFuncObj;
  RandnGradFunc RandnGradFuncObj;
  InplaceHardtanhGradFunc InplaceHardtanhGradFuncObj;
  MSELossGradExtGradFunc MSELossGradExtGradFuncObj;
  InplaceMulsGradFunc InplaceMulsGradFuncObj;
  InplaceFillDiagonalGradFunc InplaceFillDiagonalGradFuncObj;
  BincountExtGradFunc BincountExtGradFuncObj;
  MaskedSelectGradFunc MaskedSelectGradFuncObj;
  CumminExtGradFunc CumminExtGradFuncObj;
  BernoulliExtGradFunc BernoulliExtGradFuncObj;
  InplaceScatterValueReduceGradFunc InplaceScatterValueReduceGradFuncObj;
  Conv2DExtGradFunc Conv2DExtGradFuncObj;
  AddmmGradFunc AddmmGradFuncObj;
  NarrowViewGradFunc NarrowViewGradFuncObj;
  SumExtGradFunc SumExtGradFuncObj;
  ReplicationPad1DGradFunc ReplicationPad1DGradFuncObj;
  FlashAttentionScoreGradGradFunc FlashAttentionScoreGradGradFuncObj;
  BatchNormElemtGradFunc BatchNormElemtGradFuncObj;
  BitwiseAndScalarGradFunc BitwiseAndScalarGradFuncObj;
  TransposeViewGradFunc TransposeViewGradFuncObj;
  UpsampleBilinear2DGradFunc UpsampleBilinear2DGradFuncObj;
  EluGradExtGradFunc EluGradExtGradFuncObj;
  UpsampleNearest2DGradGradFunc UpsampleNearest2DGradGradFuncObj;
  ContiguousGradFunc ContiguousGradFuncObj;
  PReLUGradFunc PReLUGradFuncObj;
  IncreFlashAttentionGradFunc IncreFlashAttentionGradFuncObj;
  ConvolutionGradGradFunc ConvolutionGradGradFuncObj;
  MultinomialExtGradFunc MultinomialExtGradFuncObj;
  ReplicationPad2DGradGradFunc ReplicationPad2DGradGradFuncObj;
  SelectGradFunc SelectGradFuncObj;
  CrossGradFunc CrossGradFuncObj;
  BatchNormGradExtGradFunc BatchNormGradExtGradFuncObj;
  TanGradFunc TanGradFuncObj;
  CopyGradFunc CopyGradFuncObj;
  ErfcGradFunc ErfcGradFuncObj;
  LinalgQrGradFunc LinalgQrGradFuncObj;
  Atan2ExtGradFunc Atan2ExtGradFuncObj;
  LogSoftmaxGradFunc LogSoftmaxGradFuncObj;
  ExpGradFunc ExpGradFuncObj;
  RandnLikeGradFunc RandnLikeGradFuncObj;
  MeanExtGradFunc MeanExtGradFuncObj;
  DropoutExtGradFunc DropoutExtGradFuncObj;
  FmodScalarGradFunc FmodScalarGradFuncObj;
  AddmvGradFunc AddmvGradFuncObj;
  AbsGradFunc AbsGradFuncObj;
  ThresholdGradFunc ThresholdGradFuncObj;
  ThresholdGradGradFunc ThresholdGradGradFuncObj;
  RemainderScalarTensorGradFunc RemainderScalarTensorGradFuncObj;
  ArgMaxWithValueGradFunc ArgMaxWithValueGradFuncObj;
  SoftplusGradExtGradFunc SoftplusGradExtGradFuncObj;
  TriuGradFunc TriuGradFuncObj;
  InplaceFloorDivideGradFunc InplaceFloorDivideGradFuncObj;
  UniformExtGradFunc UniformExtGradFuncObj;
  ReplicationPad2DGradFunc ReplicationPad2DGradFuncObj;
  InplaceMaskedFillTensorGradFunc InplaceMaskedFillTensorGradFuncObj;
  EqualGradFunc EqualGradFuncObj;
  TanhGradGradFunc TanhGradGradFuncObj;
  UpsampleNearest1DGradFunc UpsampleNearest1DGradFuncObj;
  RandIntGradFunc RandIntGradFuncObj;
  SpeedFusionAttentionGradGradFunc SpeedFusionAttentionGradGradFuncObj;
  AdaptiveAvgPool2DExtGradFunc AdaptiveAvgPool2DExtGradFuncObj;
  MulGradFunc MulGradFuncObj;
  SmoothL1LossGradGradFunc SmoothL1LossGradGradFuncObj;
  GeneratorGradFunc GeneratorGradFuncObj;
  SeluGradGradFunc SeluGradGradFuncObj;
  GroupNormGradFunc GroupNormGradFuncObj;
  DivModsGradFunc DivModsGradFuncObj;
  PromptFlashAttentionGradFunc PromptFlashAttentionGradFuncObj;
  MoeTokenPermuteGradFunc MoeTokenPermuteGradFuncObj;
  BinaryCrossEntropyGradFunc BinaryCrossEntropyGradFuncObj;
  DivsGradFunc DivsGradFuncObj;
  DenseGradFunc DenseGradFuncObj;
  TransposeExtViewGradFunc TransposeExtViewGradFuncObj;
  ConvolutionGradFunc ConvolutionGradFuncObj;
  NormalFloatTensorGradFunc NormalFloatTensorGradFuncObj;
  ReduceAllGradFunc ReduceAllGradFuncObj;
  XLogYScalarOtherGradFunc XLogYScalarOtherGradFuncObj;
  MvGradFunc MvGradFuncObj;
  TopkExtGradFunc TopkExtGradFuncObj;
  SliceExtViewGradFunc SliceExtViewGradFuncObj;
  RepeatGradFunc RepeatGradFuncObj;
  AtanExtGradFunc AtanExtGradFuncObj;
  IsInfGradFunc IsInfGradFuncObj;
  MatrixInverseExtGradFunc MatrixInverseExtGradFuncObj;
  AdaptiveAvgPool1DGradFunc AdaptiveAvgPool1DGradFuncObj;
  SplitWithSizeGradFunc SplitWithSizeGradFuncObj;
  RotaryPositionEmbeddingGradFunc RotaryPositionEmbeddingGradFuncObj;
  RandExtGradFunc RandExtGradFuncObj;
  AsinExtGradFunc AsinExtGradFuncObj;
  ConvTranspose2DGradFunc ConvTranspose2DGradFuncObj;
  InplaceFillTensorGradFunc InplaceFillTensorGradFuncObj;
  ReflectionPad1DGradFunc ReflectionPad1DGradFuncObj;
  GeLUGradFunc GeLUGradFuncObj;
  BitwiseXorTensorGradFunc BitwiseXorTensorGradFuncObj;
  NegGradFunc NegGradFuncObj;
  MoeTokenUnpermuteGradFunc MoeTokenUnpermuteGradFuncObj;
  InplaceZeroGradFunc InplaceZeroGradFuncObj;
  IndexAddExtGradFunc IndexAddExtGradFuncObj;
  Conv1DExtGradFunc Conv1DExtGradFuncObj;
  IsCloseGradFunc IsCloseGradFuncObj;
  AddLayerNormV2GradFunc AddLayerNormV2GradFuncObj;
  NormalTensorTensorGradFunc NormalTensorTensorGradFuncObj;
  AdaptiveAvgPool2DGradExtGradFunc AdaptiveAvgPool2DGradExtGradFuncObj;
  SqueezeGradFunc SqueezeGradFuncObj;
  ExpandDimsViewGradFunc ExpandDimsViewGradFuncObj;
  GeluExtGradFunc GeluExtGradFuncObj;
  AvgPool3DGradExtGradFunc AvgPool3DGradExtGradFuncObj;
  InplaceExpGradFunc InplaceExpGradFuncObj;
  UpsampleNearest3DGradFunc UpsampleNearest3DGradFuncObj;
  ReduceMinGradFunc ReduceMinGradFuncObj;
  AcoshExtGradFunc AcoshExtGradFuncObj;
  SmoothL1LossGradFunc SmoothL1LossGradFuncObj;
  InplaceAddExtGradFunc InplaceAddExtGradFuncObj;
  SliceExtGradFunc SliceExtGradFuncObj;
  BroadcastToViewGradFunc BroadcastToViewGradFuncObj;
  KLDivGradGradFunc KLDivGradGradFuncObj;
  DiagExtGradFunc DiagExtGradFuncObj;
  Conv2DPaddingGradFunc Conv2DPaddingGradFuncObj;
  MedianDimGradFunc MedianDimGradFuncObj;
  FracGradFunc FracGradFuncObj;
  ScatterAddExtGradFunc ScatterAddExtGradFuncObj;
  LerpGradFunc LerpGradFuncObj;
  RsqrtGradFunc RsqrtGradFuncObj;
  NLLLoss2dGradGradFunc NLLLoss2dGradGradFuncObj;
  CloneGradFunc CloneGradFuncObj;
  ZerosLikeExtGradFunc ZerosLikeExtGradFuncObj;
  LogGradFunc LogGradFuncObj;
  MaxPoolWithMaskGradFunc MaxPoolWithMaskGradFuncObj;
  GluGradGradFunc GluGradGradFuncObj;
  ViewAsGradFunc ViewAsGradFuncObj;
  RmsNormGradFunc RmsNormGradFuncObj;
  SoftmaxBackwardGradFunc SoftmaxBackwardGradFuncObj;
  ArangeGradFunc ArangeGradFuncObj;
  InnerNonZeroGradFunc InnerNonZeroGradFuncObj;
  GeluGradExtGradFunc GeluGradExtGradFuncObj;
  InplaceDivGradFunc InplaceDivGradFuncObj;
  Conv3DExtGradFunc Conv3DExtGradFuncObj;
  TruncGradFunc TruncGradFuncObj;
  CustomExtGradFunc CustomExtGradFuncObj;
  PReLUGradGradFunc PReLUGradGradFuncObj;
  NLLLossGradFunc NLLLossGradFuncObj;
  BatchNormExtGradFunc BatchNormExtGradFuncObj;
  InplaceReLUGradFunc InplaceReLUGradFuncObj;
  IndexFillTensorGradFunc IndexFillTensorGradFuncObj;
  RemainderTensorTensorGradFunc RemainderTensorTensorGradFuncObj;
  SwigluGradFunc SwigluGradFuncObj;
  DropoutGenMaskExtGradFunc DropoutGenMaskExtGradFuncObj;
  LinSpaceExtGradFunc LinSpaceExtGradFuncObj;
  InplaceAddmmGradFunc InplaceAddmmGradFuncObj;
  Im2ColExtGradFunc Im2ColExtGradFuncObj;
  BaddbmmGradFunc BaddbmmGradFuncObj;
  GreaterEqualScalarGradFunc GreaterEqualScalarGradFuncObj;
  SoftplusExtGradFunc SoftplusExtGradFuncObj;
  AddcdivExtGradFunc AddcdivExtGradFuncObj;
  HShrinkGradFunc HShrinkGradFuncObj;
  AllGatherMatmulGradFunc AllGatherMatmulGradFuncObj;
  SelectExtViewGradFunc SelectExtViewGradFuncObj;
  IdentityGradFunc IdentityGradFuncObj;
  ReduceAnyGradFunc ReduceAnyGradFuncObj;
  MinGradFunc MinGradFuncObj;
  CastGradFunc CastGradFuncObj;
  UnstackExtViewGradFunc UnstackExtViewGradFuncObj;
  SubExtGradFunc SubExtGradFuncObj;
  ChunkGradFunc ChunkGradFuncObj;
  MaxGradFunc MaxGradFuncObj;
  Log10GradFunc Log10GradFuncObj;
  MaximumGradFunc MaximumGradFuncObj;
  LogSoftmaxExtGradFunc LogSoftmaxExtGradFuncObj;
  SoftmaxGradFunc SoftmaxGradFuncObj;
  NormalFloatFloatGradFunc NormalFloatFloatGradFuncObj;
  LayerNormGradExtGradFunc LayerNormGradExtGradFuncObj;
  BinaryCrossEntropyWithLogitsBackwardGradFunc BinaryCrossEntropyWithLogitsBackwardGradFuncObj;
  MaxPoolWithIndicesGradFunc MaxPoolWithIndicesGradFuncObj;
  RollGradFunc RollGradFuncObj;
  SoftMarginLossGradFunc SoftMarginLossGradFuncObj;
  VarGradFunc VarGradFuncObj;
  AtanhGradFunc AtanhGradFuncObj;
  MedianExtGradFunc MedianExtGradFuncObj;
  FullLikeGradFunc FullLikeGradFuncObj;
  FmodTensorGradFunc FmodTensorGradFuncObj;
  RemainderTensorScalarGradFunc RemainderTensorScalarGradFuncObj;
  LogSigmoidGradGradFunc LogSigmoidGradGradFuncObj;
  InplaceFloorDividesGradFunc InplaceFloorDividesGradFuncObj;
  InplaceFloorGradFunc InplaceFloorGradFuncObj;
  AcosExtGradFunc AcosExtGradFuncObj;
  SiLUGradFunc SiLUGradFuncObj;
  UpsampleTrilinear3DGradGradFunc UpsampleTrilinear3DGradGradFuncObj;
  AvgPool2DGradFunc AvgPool2DGradFuncObj;
  InplaceScatterAddGradFunc InplaceScatterAddGradFuncObj;
  SigmoidGradFunc SigmoidGradFuncObj;
  SubGradFunc SubGradFuncObj;
  OnesGradFunc OnesGradFuncObj;
  ReduceMaxGradFunc ReduceMaxGradFuncObj;
  IndexGradFunc IndexGradFuncObj;
  CoshGradFunc CoshGradFuncObj;
  MatMulGradFunc MatMulGradFuncObj;
  InplaceDivModGradFunc InplaceDivModGradFuncObj;
  SelectV2GradFunc SelectV2GradFuncObj;
  MaxUnpool2DExtGradFunc MaxUnpool2DExtGradFuncObj;
  BroadcastToGradFunc BroadcastToGradFuncObj;
  UniqueDimGradFunc UniqueDimGradFuncObj;
  MoeTokenPermuteGradGradFunc MoeTokenPermuteGradGradFuncObj;
  SoftShrinkGradGradFunc SoftShrinkGradGradFuncObj;
  BatchNormGatherStatsWithCountsGradFunc BatchNormGatherStatsWithCountsGradFuncObj;
  LerpScalarGradFunc LerpScalarGradFuncObj;
  ArgSortGradFunc ArgSortGradFuncObj;
  StdGradFunc StdGradFuncObj;
  ReplicationPad1DGradGradFunc ReplicationPad1DGradGradFuncObj;
  NarrowGradFunc NarrowGradFuncObj;
  PolarGradFunc PolarGradFuncObj;
  CummaxGradFunc CummaxGradFuncObj;
  ReflectionPad1DGradGradFunc ReflectionPad1DGradGradFuncObj;
  InplaceDivModsGradFunc InplaceDivModsGradFuncObj;
  BatchNormReduceGradGradFunc BatchNormReduceGradGradFuncObj;
  TensorScatterElementsGradFunc TensorScatterElementsGradFuncObj;
  ConvolutionStrGradFunc ConvolutionStrGradFuncObj;
  LogicalNotGradFunc LogicalNotGradFuncObj;
  NanToNumGradFunc NanToNumGradFuncObj;
  InplaceStopGradientGradFunc InplaceStopGradientGradFuncObj;
  Expm1GradFunc Expm1GradFuncObj;
  AddcmulExtGradFunc AddcmulExtGradFuncObj;
  TakeGradFunc TakeGradFuncObj;
  ArgMinWithValueGradFunc ArgMinWithValueGradFuncObj;
  ConstantPadNDGradFunc ConstantPadNDGradFuncObj;
  GcdGradFunc GcdGradFuncObj;
  BitwiseAndTensorGradFunc BitwiseAndTensorGradFuncObj;
  LogAddExp2GradFunc LogAddExp2GradFuncObj;
  DotGradFunc DotGradFuncObj;
  GridSampler3DGradGradFunc GridSampler3DGradGradFuncObj;
  AdaptiveAvgPool3DExtGradFunc AdaptiveAvgPool3DExtGradFuncObj;
  SilentCheckV2GradFunc SilentCheckV2GradFuncObj;
  LogicalAndGradFunc LogicalAndGradFuncObj;
  GridSampler3DGradFunc GridSampler3DGradFuncObj;
  FillScalarGradFunc FillScalarGradFuncObj;
  NansumGradFunc NansumGradFuncObj;
  RepeatInterleaveTensorGradFunc RepeatInterleaveTensorGradFuncObj;
  UpsampleTrilinear3DGradFunc UpsampleTrilinear3DGradFuncObj;
  ReluGradGradFunc ReluGradGradFuncObj;
  SignGradFunc SignGradFuncObj;
  MinDimGradFunc MinDimGradFuncObj;
  NeScalarGradFunc NeScalarGradFuncObj;
  ReflectionPad3DGradGradFunc ReflectionPad3DGradGradFuncObj;
  MatMulExtGradFunc MatMulExtGradFuncObj;
  ErfGradFunc ErfGradFuncObj;
  LogSigmoidGradFunc LogSigmoidGradFuncObj;
  AddLayerNormGradGradFunc AddLayerNormGradGradFuncObj;
  UpsampleBicubic2DGradGradFunc UpsampleBicubic2DGradGradFuncObj;
  KVCacheScatterUpdateGradFunc KVCacheScatterUpdateGradFuncObj;
  GroupedMatmulV2GradFunc GroupedMatmulV2GradFuncObj;
  MatmulAllReduceAddRmsNormGradFunc MatmulAllReduceAddRmsNormGradFuncObj;
  MoeInitRoutingGradFunc MoeInitRoutingGradFuncObj;
  MoeFinalizeRoutingGradFunc MoeFinalizeRoutingGradFuncObj;
  QuantBatchMatmulGradFunc QuantBatchMatmulGradFuncObj;
  QuantV2GradFunc QuantV2GradFuncObj;
  MoeInitRoutingV2GradFunc MoeInitRoutingV2GradFuncObj;
  AddRmsNormQuantV2GradFunc AddRmsNormQuantV2GradFuncObj;
  WeightQuantBatchMatmulGradFunc WeightQuantBatchMatmulGradFuncObj;
  GroupedMatmulV4GradFunc GroupedMatmulV4GradFuncObj;
  GroupedMatmulGradFunc GroupedMatmulGradFuncObj;
  MoeGatingTopKSoftmaxGradFunc MoeGatingTopKSoftmaxGradFuncObj;
  DynamicQuantExtGradFunc DynamicQuantExtGradFuncObj;
  FusedInferAttentionScoreGradFunc FusedInferAttentionScoreGradFuncObj;
  MoeComputeExpertTokensGradFunc MoeComputeExpertTokensGradFuncObj;
  InplaceExponentialGradFunc InplaceExponentialGradFuncObj;
  GmmGradFunc GmmGradFuncObj;
  PixelShuffleGradFunc PixelShuffleGradFuncObj;
  GmmBackwardGradFunc GmmBackwardGradFuncObj;
  GmmV2BackwardGradFunc GmmV2BackwardGradFuncObj;
  GmmV2BackwardFusionGradFunc GmmV2BackwardFusionGradFuncObj;
  GmmV2GradFunc GmmV2GradFuncObj;
  GmmBackwardFusionGradFunc GmmBackwardFusionGradFuncObj;
};
}  // namespace pyboost
}  // namespace kernel
}  // namespace mindspore

#endif  // MINDSPORE_MINDSPORE_OPS_KERNEL_FUNCTIONS_AUTO_GENERATE_AUTO_GRAD_OP_REG_H_
