<template>
  <div class="task-container">
    <h1>任务管理</h1>
    <el-card class="task-card">
      <template #header>
        <div class="card-header">
          <span>我的任务</span>
        </div>
      </template>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="全部" name="all">
          <el-table :data="tasks" style="width: 100%">
            <el-table-column prop="id" label="任务ID" width="180"></el-table-column>
            <el-table-column prop="title" label="任务标题"></el-table-column>
            <el-table-column prop="orderId" label="订单ID" width="180"></el-table-column>
            <el-table-column prop="status" label="状态" width="120">
              <template #default="scope">
                <el-tag :type="getStatusType(scope.row.status)">{{ scope.row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="deadline" label="截止日期" width="180"></el-table-column>
            <el-table-column prop="createTime" label="创建时间" width="180"></el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" @click="viewTask(scope.row.id)">查看</el-button>
                <el-button size="small" @click="submitTask(scope.row.id)" v-if="scope.row.status === '进行中'">提交</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="进行中" name="ongoing">
          <el-table :data="ongoingTasks" style="width: 100%">
            <el-table-column prop="id" label="任务ID" width="180"></el-table-column>
            <el-table-column prop="title" label="任务标题"></el-table-column>
            <el-table-column prop="orderId" label="订单ID" width="180"></el-table-column>
            <el-table-column prop="deadline" label="截止日期" width="180"></el-table-column>
            <el-table-column label="操作" width="150">
              <template #default="scope">
                <el-button size="small" type="primary" @click="viewTask(scope.row.id)">查看</el-button>
                <el-button size="small" @click="submitTask(scope.row.id)">提交</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="已完成" name="completed">
          <el-table :data="completedTasks" style="width: 100%">
            <el-table-column prop="id" label="任务ID" width="180"></el-table-column>
            <el-table-column prop="title" label="任务标题"></el-table-column>
            <el-table-column prop="orderId" label="订单ID" width="180"></el-table-column>
            <el-table-column prop="completeTime" label="完成时间" width="180"></el-table-column>
            <el-table-column label="操作" width="100">
              <template #default="scope">
                <el-button size="small" type="primary" @click="viewTask(scope.row.id)">查看</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
    <div class="pagination">
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pageSize"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const activeTab = ref('all')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(30)

const tasks = ref([
  {
    id: 'TASK20240001',
    title: '现代都市情感短剧制作',
    orderId: 'ORD20240001',
    status: '进行中',
    deadline: '2024-12-31',
    createTime: '2024-12-01'
  },
  {
    id: 'TASK20240002',
    title: '科幻题材短剧制作',
    orderId: 'ORD20240002',
    status: '进行中',
    deadline: '2025-01-15',
    createTime: '2024-12-02'
  },
  {
    id: 'TASK20240003',
    title: '历史古装短剧制作',
    orderId: 'ORD20240003',
    status: '已完成',
    deadline: '2025-01-10',
    createTime: '2024-12-03',
    completeTime: '2024-12-20'
  }
])

const ongoingTasks = computed(() => {
  return tasks.value.filter(task => task.status === '进行中')
})

const completedTasks = computed(() => {
  return tasks.value.filter(task => task.status === '已完成')
})

const getStatusType = (status) => {
  switch (status) {
    case '已完成':
      return 'success'
    case '进行中':
      return 'warning'
    case '待处理':
      return 'info'
    default:
      return ''
  }
}

const viewTask = (taskId) => {
  console.log('查看任务', taskId)
  // 查看任务逻辑
}

const submitTask = (taskId) => {
  console.log('提交任务', taskId)
  // 提交任务逻辑
}

const handleSizeChange = (size) => {
  pageSize.value = size
  console.log(`每页 ${size} 条`)
}

const handleCurrentChange = (current) => {
  currentPage.value = current
  console.log(`当前页: ${current}`)
}
</script>

<style scoped>
.task-container {
  padding: 20px;
}

.task-card {
  margin-bottom: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>