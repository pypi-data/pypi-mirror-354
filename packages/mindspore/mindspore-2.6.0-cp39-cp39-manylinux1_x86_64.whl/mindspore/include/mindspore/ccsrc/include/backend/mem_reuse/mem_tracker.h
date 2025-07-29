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

#ifndef MINDSPORE_CCSRC_BACKEND_OPTIMIZER_MEM_REUSE_MEM_TRACKER_H_
#define MINDSPORE_CCSRC_BACKEND_OPTIMIZER_MEM_REUSE_MEM_TRACKER_H_
#include <mutex>
#include <unordered_map>
#include <vector>
#include <string>
#include <map>
#include <utility>
#include <memory>
#include <tuple>
#include "ir/tensor_storage_info.h"
#include "mindapi/base/type_id.h"
#include "utils/ms_context.h"
#include "utils/ms_utils.h"
#include "utils/log_adapter.h"
#include "include/backend/visible.h"
#include "common/device_address.h"
#include "include/backend/mem_reuse/mem_pool_util.h"

namespace mindspore {
namespace device {
namespace tracker {
// keys
const char kStreamId[] = "stream_id";
const char kEvent[] = "event";
const char kGroup[] = "group";
const char kCommRank[] = "comm_rank";
const char kSrcRank[] = "src_rank";
const char kDstRank[] = "dst_rank";
const char kRootRank[] = "root_rank";

using DeviceMemPtr = const void *;
using KernelTensorPtr = const void *;
using MemType = memory::mem_pool::MemType;

struct TaskInfo {
  std::string node_name;
  std::string graph_name;
  std::string task_name;
  int64_t time_stamp;
  std::unordered_map<std::string, std::string> attrs;
  // The code location of task execution
  std::string file_name;
  size_t line_num;
  std::string python_stack;
  TaskInfo() : node_name(), graph_name(), task_name(), time_stamp(0), file_name(), line_num(0) {}
};

using TaskInfoPtr = std::shared_ptr<TaskInfo>;

struct MemInfo;
struct MemBlockInfo {
  // start and end use the operands of the memory pool
  int64_t start_time_stamp;
  int64_t end_time_stamp;
  DeviceMemPtr device_addr;
  std::weak_ptr<MemInfo> mem_info;
  bool is_bind;
  uint32_t stream_id;
  size_t actual_peak_memory;
  size_t size;
  std::string pool_name;
  size_t last_write_stream_id;
  size_t last_write_time_stamp;

  // Record mem info for profiling
  double real_start_time{-1};
  double real_end_time{-1};
  size_t alloc_in_used_size{0};    // Record in used size when allocate mem
  size_t alloc_total_size{0};      // Record total size when allocate mem
  size_t release_in_used_size{0};  // Record in used size when release mem
  size_t release_total_size{0};    // Record total size when release mem
  MemBlockInfo()
      : start_time_stamp(INT64_MAX),
        end_time_stamp(INT64_MAX),
        device_addr(nullptr),
        is_bind(false),
        stream_id(0),
        actual_peak_memory(0),
        size(0),
        pool_name(),
        last_write_stream_id(0),
        last_write_time_stamp(0) {}
};

using MemBlockInfoPtr = std::shared_ptr<MemBlockInfo>;

struct MemInfo {
  // mem info
  MemType type;
  size_t size;
  const void *kernel_tensor;
  // producer and user
  std::vector<TaskInfoPtr> user_tasks;
  TaskInfoPtr producer_task;
  // mem block
  MemBlockInfoPtr mem_block;
  // Memory application code location
  std::string file_name;
  size_t line_num;
  MemInfo() : type(MemType::kOther), size(0), kernel_tensor(nullptr), file_name(), line_num(0) {}
};

using MemInfoPtr = std::shared_ptr<MemInfo>;

// Struct for interaction with profiling
struct ProfileMemInfo {
  std::string name;
  size_t size;                  // size of block, B
  double alloc_time;            // alloc time, us
  double release_time;          // release time, us
  size_t alloc_in_used_size;    // Record in used size when allocate mem, B
  size_t alloc_total_size;      // Record total size when allocate mem, B
  size_t release_in_used_size;  // Record in used size when release mem, B
  size_t release_total_size;    // Record total size when release mem, B
  std::string device;
  ProfileMemInfo()
      : name(),
        size(0),
        alloc_time(-1),
        release_time(-1),
        alloc_in_used_size(0),
        alloc_total_size(0),
        release_in_used_size(0),
        release_total_size(0),
        device() {}
};
using ProfileMemInfoPtr = std::shared_ptr<ProfileMemInfo>;

class BACKEND_EXPORT MemTracker {
 public:
  virtual void AddTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
                       const std::string &file_name, size_t line_num) = 0;
  virtual void AddTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
                       const bool to_graph, const std::string &file_name, size_t line_num) = 0;
  virtual void AddNestedTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
                             const std::string &file_name, size_t line_num) = 0;
  virtual void DelNestedTask() = 0;
  virtual void UpdateTask(const std::string &task_name, const std::unordered_map<std::string, std::string> &attrs) = 0;
  virtual void CacheLastTask() = 0;
  virtual void EmptyCache() = 0;
  virtual void AddMemInfo(const std::string &task_name, MemType type, size_t size, DeviceAddress *device_address,
                          const std::string &file_name, size_t line_num) = 0;
  virtual void AddCompileTimeMemInfo(const std::string &task_name, size_t size, DeviceMemPtr device_ptr,
                                     MemType mem_type, const std::string &file_name, size_t line_num) = 0;
  virtual void AllocMemBlock(DeviceMemPtr device_addr, size_t size, const std::string &pool_name,
                             size_t actual_peak_memory, size_t in_used_size, size_t total_size, uint32_t stream_id) = 0;
  virtual void FreeMemBlock(DeviceMemPtr device_addr, size_t in_used_size, size_t total_size) = 0;
  virtual void UseMemBlock(const std::string &task_name, DeviceMemPtr device_addr, const std::string &file_name,
                           size_t line_num) = 0;
  virtual void BindDevicePtr(DeviceAddress *kernel_tensor, DeviceMemPtr device_ptr, const std::string &file_name,
                             size_t line_num) = 0;
  virtual void MarkTensorAsInput(const std::string &task_name, const std::string &device_name, DeviceMemPtr device_ptr,
                                 TypeId dtype, const ShapeVector &shape, TensorStorageInfoPtr tensor_info,
                                 const std::string &file_name, size_t line_num) = 0;
  virtual void MarkTensorAsOutput(const std::string &task_name, const std::string &device_name, DeviceMemPtr device_ptr,
                                  TypeId dtype, const ShapeVector &shape, TensorStorageInfoPtr tensor_info,
                                  const std::string &file_name, size_t line_num) = 0;

  virtual void Dump(size_t rank_id) = 0;
  virtual void UpdateProfilingPos() = 0;
  virtual void DumpProfilingMemInfo(size_t rank_id, const std::string &path, const std::string &file_name) = 0;
  virtual bool IsEnabled() = 0;
  virtual ~MemTracker() = default;

  virtual void SetEnableMemoryDebugInfo(bool enable_memory_debug_info) {
    enable_memory_debug_info_ = enable_memory_debug_info;
  }
  bool enable_memory_debug_info() { return enable_memory_debug_info_; }

 protected:
  bool enable_memory_debug_info_{false};
};

class BACKEND_EXPORT MemoryTrackerEnabled : public MemTracker {
  friend class MemTrackerManager;

 public:
  void AddTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
               const std::string &file_name, size_t line_num) override;
  void AddTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
               const bool to_graph, const std::string &file_name, size_t line_num) override;
  void AddNestedTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
                     const std::string &file_name, size_t line_num) override;
  void DelNestedTask() override;
  void UpdateTask(const std::string &task_name, const std::unordered_map<std::string, std::string> &attrs) override;
  void CacheLastTask() override;
  void EmptyCache() override;
  void AddMemInfo(const std::string &task_name, MemType type, size_t size, DeviceAddress *device_address,
                  const std::string &file_name, size_t line_num) override;
  void AddCompileTimeMemInfo(const std::string &task_name, size_t size, DeviceMemPtr device_ptr, MemType mem_type,
                             const std::string &file_name, size_t line_num) override;
  void AllocMemBlock(DeviceMemPtr device_addr, size_t size, const std::string &pool_name, size_t actual_peak_memory,
                     size_t in_used_size, size_t total_size, uint32_t stream_id) override;
  void FreeMemBlock(DeviceMemPtr device_addr, size_t in_used_size, size_t total_size) override;
  void UseMemBlock(const std::string &task_name, DeviceMemPtr device_addr, const std::string &file_name,
                   size_t line_num) override;
  void BindDevicePtr(DeviceAddress *device_address, DeviceMemPtr device_ptr, const std::string &file_name,
                     size_t line_num) override;
  void Dump(size_t rank_id) override;
  void UpdateProfilingPos() override;
  void DumpProfilingMemInfo(size_t rank_id, const std::string &path, const std::string &file_name) override;
  void MarkTensorAsInput(const std::string &task_name, const std::string &device_name, DeviceMemPtr device_ptr,
                         TypeId dtype, const ShapeVector &shape, TensorStorageInfoPtr tensor_info,
                         const std::string &file_name, size_t line_num) override;
  void MarkTensorAsOutput(const std::string &task_name, const std::string &device_name, DeviceMemPtr device_ptr,
                          TypeId dtype, const ShapeVector &shape, TensorStorageInfoPtr tensor_info,
                          const std::string &file_name, size_t line_num) override;

  bool IsEnabled() override { return true; }

  std::tuple<std::string, std::string, std::string> GetPath(size_t rank_id);
  MemoryTrackerEnabled(const MemoryTrackerEnabled &) = delete;
  MemoryTrackerEnabled &operator=(const MemoryTrackerEnabled &) = delete;

 private:
  MemoryTrackerEnabled() = default;
  ~MemoryTrackerEnabled() override = default;

  MemInfoPtr NewMemInfo(const std::string &task_name, MemType type, size_t size, const void *kernel_tensor,
                        const std::string &file_name, size_t line_num);
  std::map<DeviceMemPtr, MemBlockInfoPtr>::iterator FindMemBlock(DeviceMemPtr device_ptr, const std::string &file_name,
                                                                 size_t line_num);
  void AddMemInfoForKernelTensor(const std::string &task_name, MemType type, size_t size, const void *kernel_tensor,
                                 const std::string &file_name, size_t line_num);
  std::mutex mutex_;
  int64_t time_stamp_ = 0;
  int64_t nested_num_ = 0;
  size_t last_profiling_pos_{0};  // Prevent the same data from being dumped.
  // for dump
  bool has_dump = false;
  bool is_init_enable_hccl_ = false;
  bool enable_hccl_ = false;
  TaskInfoPtr cache = nullptr;
  std::vector<TaskInfoPtr> task_list_;
  std::vector<MemInfoPtr> mem_info_list_;
  std::vector<MemBlockInfoPtr> mem_block_list_;
  // actor name -> task info
  std::map<std::string, TaskInfoPtr> task_map_;
  // kernel tensor -> mem info
  std::map<const void *, MemInfoPtr> kernel_tensor_mem_map;
  // device address -> mem info
  std::map<DeviceAddress *, MemInfoPtr> device_address_mem_map;
  // device addr -> mem block info
  std::map<DeviceMemPtr, MemBlockInfoPtr> device_mem_block_map;

  static MemoryTrackerEnabled &getInstance() {
    static MemoryTrackerEnabled instance;
    return instance;
  }
};

using Lock = memory::mem_pool::Lock;
using LockGuard = memory::mem_pool::LockGuard;
class BACKEND_EXPORT MemoryTrackerDisabled : public MemTracker {
  friend class MemTrackerManager;

 public:
  // mock
  void AddTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
               const std::string &file_name, size_t line_num) override;
  void AddTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
               const bool to_graph, const std::string &file_name, size_t line_num) override;
  void AddNestedTask(const std::string &task_name, const std::string &node_name, const std::string &graph_name,
                     const std::string &file_name, size_t line_num) override;
  void DelNestedTask() override {}
  void UpdateTask(const std::string &task_name, const std::unordered_map<std::string, std::string> &attrs) override {}
  void CacheLastTask() override {}
  void EmptyCache() override {}
  void AddMemInfo(const std::string &task_name, MemType type, size_t size, DeviceAddress *device_address,
                  const std::string &file_name, const size_t line_num) override;
  void AddCompileTimeMemInfo(const std::string &task_name, size_t size, DeviceMemPtr device_ptr, MemType mem_type,
                             const std::string &file_name, size_t line_num) override {}
  void AllocMemBlock(DeviceMemPtr device_addr, size_t size, const std::string &pool_name, size_t actual_peak_memory,
                     size_t in_used_size, size_t total_size, uint32_t stream_id) override {}
  void FreeMemBlock(DeviceMemPtr device_addr, size_t in_used_size, size_t total_size) override {}
  void UseMemBlock(const std::string &task_name, DeviceMemPtr device_addr, const std::string &file_name,
                   size_t line_num) override {}
  void BindDevicePtr(DeviceAddress *device_address, DeviceMemPtr device_ptr, const std::string &file_name,
                     size_t line_num) override {}
  void MarkTensorAsInput(const std::string &task_name, const std::string &device_name, DeviceMemPtr device_ptr,
                         TypeId dtype, const ShapeVector &shape, TensorStorageInfoPtr tensor_info,
                         const std::string &file_name, size_t line_num) override {}
  void MarkTensorAsOutput(const std::string &task_name, const std::string &device_name, DeviceMemPtr device_ptr,
                          TypeId dtype, const ShapeVector &shape, TensorStorageInfoPtr tensor_info,
                          const std::string &file_name, size_t line_num) override {}
  void Dump(size_t rank_id) override {}
  void UpdateProfilingPos() override {}
  void DumpProfilingMemInfo(size_t rank_id, const std::string &path, const std::string &file_name) override {}
  bool IsEnabled() override { return false; }

  MemoryTrackerDisabled(const MemoryTrackerDisabled &) = delete;
  MemoryTrackerDisabled &operator=(const MemoryTrackerDisabled &) = delete;

 private:
  MemoryTrackerDisabled() = default;
  ~MemoryTrackerDisabled() override = default;
  static MemoryTrackerDisabled &getInstance() {
    static MemoryTrackerDisabled instance;
    return instance;
  }

  Lock lock_;
  std::map<std::string, std::string> task_map_;
};

namespace graph {
struct TrackerTensor {
  std::string ToString();
  std::string DtypeToString();
  std::string ShapeToString();
  std::string TensorInfoToString();
  MemBlockInfoPtr mem_block;
  TensorStorageInfoPtr tensor_info;
  ShapeVector shape;
  TypeId dtype;
};
using TrackerTensorPtr = std::shared_ptr<TrackerTensor>;

struct TrackerOperator {
  std::vector<TrackerTensorPtr> inputs;
  std::vector<TrackerTensorPtr> outputs;
  std::string ToString();
  void ValidateMemoryUsage(const std::vector<std::vector<size_t>> &dep);
  std::string name();
  TaskInfoPtr task_info;
};
using TrackerOperatorPtr = std::shared_ptr<TrackerOperator>;

struct MultiStreamDependency {
  std::vector<std::vector<size_t>> dependency;
  std::map<std::string, std::vector<size_t>> event_map;
  void Init(size_t stream_num);
  void RecordEvent(size_t stream_id, const std::string &event_id, size_t time_stamp);
  void WaitEvent(size_t stream_id, const std::string &event_id);
};
class BACKEND_EXPORT GraphTracker {
 public:
  static GraphTracker &getInstance() {
    static GraphTracker instance;
    return instance;
  }
  GraphTracker(const GraphTracker &) = delete;
  GraphTracker &operator=(const GraphTracker &) = delete;
  TrackerTensorPtr AddTensor(MemBlockInfoPtr mem_block, TypeId dtype, const ShapeVector &shape,
                             TensorStorageInfoPtr tensor_info);
  void AddOperator(TaskInfoPtr task_info);
  TrackerOperatorPtr GetOperator(TaskInfoPtr task_info);
  void Dump(const std::string &graph_path);
  void CacheLastTask();
  void EmptyCache();

  bool NeedDump() { return !operators_.empty(); }

 private:
  GraphTracker() = default;
  void InitStreamSize();
  MultiStreamDependency dep_;
  std::mutex mutex_;
  std::vector<TrackerTensorPtr> tensors_;
  std::vector<TrackerOperatorPtr> operators_;
  std::unordered_map<TaskInfoPtr, TrackerOperatorPtr> task_operator_map_;
  TrackerOperatorPtr cache = nullptr;
};
}  // namespace graph

class BACKEND_EXPORT MemTrackerManager {
 public:
  static MemTracker &GetInstance() {
    static bool enable_trace_mem = common::IsEnableAllocConfig(common::kAllocMemoryTracker);
    if (enable_trace_mem) {
      return MemoryTrackerEnabled::getInstance();
    } else {
      return MemoryTrackerDisabled::getInstance();
    }
  }
};

#define CALL_MEMORY_TRACKER_WITH_FILE(func, ...) MemTrackerManager::GetInstance().func(__VA_ARGS__, FILE_NAME, __LINE__)
#define CALL_MEMORY_TRACKER(func, ...) MemTrackerManager::GetInstance().func(__VA_ARGS__)
}  // namespace tracker
}  // namespace device
}  // namespace mindspore
#endif  // MINDSPORE_CCSRC_BACKEND_OPTIMIZER_MEM_REUSE_MEM_TRACKER_H_
