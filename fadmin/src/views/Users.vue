<template>
  <div class="users">
    <el-card shadow="never">
      <template #header>
        <span>用户管理</span>
      </template>

      <el-table :data="users" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="invite_code" label="邀请码" min-width="150" />
        <el-table-column prop="compute_power" label="剩余算力" width="120" />
        <el-table-column prop="project_count" label="项目数量" width="100" />
        <el-table-column prop="record_count" label="生成记录" width="100" />
        <el-table-column prop="created_at" label="注册时间" width="180" />
        <el-table-column prop="last_login" label="最后登录" width="180">
          <template #default="{ row }">
            {{ row.last_login || '暂无记录' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="viewDetail(row)">详情</el-button>
            <el-button link type="warning" @click="addPower(row)">充值算力</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="detailDialogVisible" title="用户详情" width="600px">
      <el-descriptions :column="2" border>
        <el-descriptions-item label="用户ID">{{ currentUser.id }}</el-descriptions-item>
        <el-descriptions-item label="邀请码">{{ currentUser.invite_code }}</el-descriptions-item>
        <el-descriptions-item label="剩余算力">{{ currentUser.compute_power }}</el-descriptions-item>
        <el-descriptions-item label="项目数量">{{ currentUser.project_count }}</el-descriptions-item>
        <el-descriptions-item label="生成记录">{{ currentUser.record_count }}</el-descriptions-item>
        <el-descriptions-item label="注册时间">{{ currentUser.created_at }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <el-dialog v-model="powerDialogVisible" title="充值算力" width="400px">
      <el-form :model="powerForm" label-width="80px">
        <el-form-item label="当前算力">
          <span>{{ currentUser.compute_power }}</span>
        </el-form-item>
        <el-form-item label="充值数量">
          <el-input-number v-model="powerForm.amount" :min="1" :max="10000" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="powerDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmAddPower">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getUsers } from '../api/admin'

const loading = ref(false)
const users = ref([])
const detailDialogVisible = ref(false)
const powerDialogVisible = ref(false)
const currentUser = ref({})
const powerForm = reactive({
  amount: 100
})

const fetchUsers = async () => {
  loading.value = true
  try {
    const res = await getUsers()
    if (res.code === 200) {
      users.value = res.data.list
    }
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const viewDetail = (row) => {
  currentUser.value = row
  detailDialogVisible.value = true
}

const addPower = (row) => {
  currentUser.value = row
  powerForm.amount = 100
  powerDialogVisible.value = true
}

const confirmAddPower = () => {
  ElMessage.success(`已为用户 ${currentUser.value.invite_code} 充值 ${powerForm.amount} 算力`)
  powerDialogVisible.value = false
  fetchUsers()
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
</style>
