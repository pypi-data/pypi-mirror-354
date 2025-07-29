/**
 * Copyright 2020 Huawei Technologies Co., Ltd
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

#ifndef MINDSPORE_CCSRC_FRONTEND_OPTIMIZER_IRPASS_BRANCH_CULLING_H_
#define MINDSPORE_CCSRC_FRONTEND_OPTIMIZER_IRPASS_BRANCH_CULLING_H_

#include <vector>
#include <algorithm>

#include "ir/func_graph.h"
#include "mindspore/ops/op_def/sequence_ops.h"
#include "mindspore/ops/op_def/comparison_ops.h"
#include "mindspore/ops/op_def/framework_ops.h"
#include "ir/func_graph_cloner.h"
#include "frontend/optimizer/optimizer_caller.h"
#include "frontend/optimizer/pattern_matcher.h"
#include "frontend/operator/ops.h"
#include "frontend/optimizer/irpass.h"
#include "pipeline/jit/ps/parse/resolve.h"

namespace mindspore {
namespace opt {
namespace irpass {
// {prim::kPrimSwitch, true, X, Y}
// {prim::kPrimSwitch, false, X, Y}
class SwitchSimplify : public OptimizerCaller {
 public:
  AnfNodePtr operator()(const OptimizerPtr &, const AnfNodePtr &node) override {
    PatternNode<AnfNodePtr> cond;
    PatternNode<AnfNodePtr> true_br;
    PatternNode<AnfNodePtr> false_br;
    auto SwitchSimplLambda = [&node, &cond, &true_br, &false_br]() -> AnfNodePtr {
      auto value_ptr = GetValueNode(cond.GetNode(node));
      bool cond_value;
      if (value_ptr->isa<BoolImm>()) {
        cond_value = GetValue<bool>(value_ptr);
      } else {
        MS_LOG_WITH_NODE(EXCEPTION, node)
          << "The condition of branch must be a bool tensor value or a bool scalar value,"
          << " not support this condition value: " << value_ptr->ToString();
      }

      MS_LOG(DEBUG) << "condition value: " << value_ptr->ToString() << ", cond: " << cond_value
                    << ", node: " << node->DebugString();
      AnfNodePtr branch_node;
      if (cond_value) {
        branch_node = true_br.GetNode(node);
      } else {
        branch_node = false_br.GetNode(node);
      }
      auto fg = GetValuePtr<FuncGraph>(branch_node);
      if (fg != nullptr) {
        MS_LOG(DEBUG) << "No recursive, " << fg->ToString();
        fg->set_flag(FUNC_GRAPH_FLAG_NO_RECURSIVE, true);
      }
      return branch_node;
    };

    auto IsDeterminateCondition = [](const AnfNodePtr &node) -> bool { return IsValueNode<BoolImm>(node); };
    MATCH_REPLACE_LAMBDA_IF(node, PPrimitive(prim::kPrimSwitch, cond, true_br, false_br), SwitchSimplLambda,
                            cond.CheckFunc(IsDeterminateCondition, node));

    return nullptr;
  }
};

// {prim::kPrimLess, Value1, Value2}
// {prim::kPrimSwitch, Less, X, Y}
// {prim::kPrimGreater, Value1, Value2}
// {prim::kPrimSwitch, Greater, X, Y}
class CompareSwitchSimplify : public OptimizerCaller {
 public:
  AnfNodePtr operator()(const OptimizerPtr &, const AnfNodePtr &node) override;
};

// {prim::kPrimTupleGetItem, {prim::kPrimSwitch, X0, X1, X2}, C} =>
// {prim::kPrimSwitch, X0, {prim::kPrimTupleGetItem, X1, C}, {prim::kPrimTupleGetItem, X2, C}}
class FloatTupleGetItemSwitch : public OptimizerCaller {
 public:
  AnfNodePtr operator()(const OptimizerPtr &, const AnfNodePtr &node) override {
    PatternNode<AnfNodePtr> cond;
    PatternNode<AnfNodePtr> true_br;
    PatternNode<AnfNodePtr> false_br;
    PatternNode<AnfNodePtr> x;
    MATCH_REPLACE_IF(node,
                     PPrimitive(prim::kPrimTupleGetItem, PPrimitive(prim::kPrimSwitch, cond, true_br, false_br), x),
                     PPrimitive(prim::kPrimSwitch, cond, PPrimitive(prim::kPrimTupleGetItem, true_br, x),
                                PPrimitive(prim::kPrimTupleGetItem, false_br, x)),
                     x.CheckFunc(IsVNode, node));
    return nullptr;
  }
};

// {prim::kPrimEnvironGet, {prim::kPrimSwitch, X1, X2, X3}, X4, X5} =>
// {prim::kPrimSwitch, X1, {prim::kPrimEnvironGet, X2, X4, X5}, {prim::kPrimEnvironGet, X3, X4, X5}}
class FloatEnvironGetSwitch : public OptimizerCaller {
 public:
  AnfNodePtr operator()(const OptimizerPtr &, const AnfNodePtr &node) override {
    PatternNode<AnfNodePtr> cond;
    PatternNode<AnfNodePtr> true_br;
    PatternNode<AnfNodePtr> false_br;
    PatternNode<AnfNodePtr> x;
    PatternNode<AnfNodePtr> x2;
    MATCH_REPLACE(node,
                  PPrimitive(prim::kPrimEnvironGet, PPrimitive(prim::kPrimSwitch, cond, true_br, false_br), x, x2),
                  PPrimitive(prim::kPrimSwitch, cond, PPrimitive(prim::kPrimEnvironGet, true_br, x, x2),
                             PPrimitive(prim::kPrimEnvironGet, false_br, x, x2)));

    return nullptr;
  }
};

namespace internal {
FuncGraphPtr TransformGraphCondTrueBranchNodes(const FuncGraphPtr &graph, const AnfNodePtr &cond);
FuncGraphPtr TransformGraphCondFalseBranchNodes(const FuncGraphPtr &graph, const AnfNodePtr &cond);
// block_nodes[0]: condition node
// block_nodes[1]: true branch node
// block_nodes[2]: false branch node
// branch_output_abs[0]: true branch abstract
// branch_output_abs[1]: false branch abstract
AnfNodePtr TransformMergeBranches(const std::vector<AnfNodePtr> &block_nodes,
                                  const std::vector<AbstractBasePtr> &branch_output_abs,
                                  const FuncGraphPtr &func_graph);
}  // namespace internal

// {{prim::kPrimSwitch, X, G1, G2}, Xs}
class ConvertSwitchReplacement {
 public:
  ConvertSwitchReplacement() = default;
  virtual ~ConvertSwitchReplacement() = default;

  bool operator()(const FuncGraphPtr &root, const OptimizerPtr &) const {
    auto manager = root->manager();
    MS_EXCEPTION_IF_NULL(manager);
    auto all_nodes = manager->all_nodes();

    bool change = false;
    for (auto &node : all_nodes) {
      if (CheckSwitchWrapNode(node)) {
        TransformSwitchBranchReplace(node);
        change = true;
      }
    }
    return change;
  }

 private:
  // Determine whether there are graphs inside the branch graph.
  bool CheckSwitchBranch(const AnfNodePtr &node) const;
  // Determine whether node matches {{prim::kPrimSwitch, X, G1, G2}, Xs}.
  bool CheckSwitchWrapNode(const AnfNodePtr &node) const;
  // Replace switch branch.
  void TransformSwitchBranchReplace(const AnfNodePtr &node) const;
};

// {prim::kPrimSwitch, {prim::kPrimDepend, ValueNode, X}, G1, G2} ->
// {prim::kPrimDepend, {prim::kPrimSwitch, ValueNode, G1, G2}, X}
class ExchangeSwitchDependValue : public OptimizerCaller {
 public:
  AnfNodePtr operator()(const OptimizerPtr &, const AnfNodePtr &node) override {
    if (!node->isa<CNode>() || node->func_graph() == nullptr) {
      return nullptr;
    }
    ScopePtr scope = node->cast<CNodePtr>()->scope();
    ScopeGuard scope_guard(scope);

    PatternNode<AnfNodePtr> cond;
    PatternNode<AnfNodePtr> true_br;
    PatternNode<AnfNodePtr> false_br;
    PatternNode<AnfNodePtr> v;
    PatternNode<AnfNodePtr> x;
    MATCH_REPLACE_IF(node, PPrimitive(prim::kPrimSwitch, PPrimitive(prim::kPrimDepend, v, x), true_br, false_br),
                     PPrimitive(prim::kPrimDepend, PPrimitive(prim::kPrimSwitch, v, true_br, false_br), x),
                     IsVNode(v.GetNode(node)));
    return nullptr;
  }
};
}  // namespace irpass
}  // namespace opt
}  // namespace mindspore
#endif  // #ifndef MINDSPORE_CCSRC_FRONTEND_OPTIMIZER_IRPASS_BRANCH_CULLING_H_
