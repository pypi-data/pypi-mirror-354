/*
* Copyright (c) Huawei Technologies Co., Ltd. 2025. All rights reserved.
* This file is a part of the CANN Open Software.
* Licensed under CANN Open Software License Agreement Version 1.0 (the "License").
* Please refer to the License for details. You may not use this file except in compliance with the License.
* THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND, EITHER EXPRESS OR IMPLIED,
* INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT, MERCHANTABILITY, OR FITNESS FOR A PARTICULAR PURPOSE.
* See LICENSE in the root of the software repository for the full text of the License.
*/
#ifndef ATBOPS_PARAMS_MLA_H
#define ATBOPS_PARAMS_MLA_H

#include <cstdint>
#include <string>
#include <sstream>
#include <vector>
#include "mki/types.h"
#include "mki/utils/compare/compare.h"
namespace AtbOps {
namespace OpParam {
struct MLA {
    enum Type {
        SPLIT_CACHE = 0,
    };
    Type type;
    int32_t headSize = 0;
    float tor = 0;
    int32_t kvHead = 0;

    std::vector<int32_t> qSeqLen;
    std::vector<int32_t> kvSeqLen;

    bool operator==(const MLA &other) const
    {
        return this->headSize == other.headSize &&
               this->qSeqLen == other.qSeqLen && this->kvSeqLen == other.kvSeqLen && this->type == other.type &&
               Mki::Utils::Compare<float>::IsEqual(this->tor, other.tor) && this->kvHead == other.kvHead;
    }
};
} // namespace OpParam
} // namespace AtbOps
#endif // ATBOPS_PARAMS_MLA_H