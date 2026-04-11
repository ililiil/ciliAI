<template>
  <div class="invite-codes">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>邀请码列表</span>
          <div class="header-actions">
            <el-button type="primary" @click="showBatchDialog">
              <el-icon><Plus /></el-icon>
              批量生成
            </el-button>
            <el-button type="success" @click="showCreateDialog">
              <el-icon><Plus /></el-icon>
              新建邀请码
            </el-button>
          </div>
        </div>
      </template>

      <el-table :data="codes" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="code" label="邀请码" min-width="150" />
        <el-table-column prop="compute_power" label="算力值" width="100" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : row.status === 'used' ? 'info' : 'danger'">
              {{ row.status === 'active' ? '未使用' : row.status === 'used' ? '已使用' : '已禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="use_count" label="使用次数" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="editCode(row)">编辑</el-button>
            <el-button link type="danger" @click="deleteCode(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="createDialogVisible" :title="editingCode ? '编辑邀请码' : '新建邀请码'" width="450px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="邀请码" prop="code">
          <el-input v-model="form.code" placeholder="请输入邀请码" :disabled="!!editingCode" />
        </el-form-item>
        <el-form-item label="算力值" prop="compute_power">
          <el-input-number v-model="form.compute_power" :min="0" :max="10000" />
        </el-form-item>
        <el-form-item label="状态" prop="status" v-if="editingCode">
          <el-select v-model="form.status">
            <el-option label="未使用" value="active" />
            <el-option label="已使用" value="used" />
            <el-option label="已禁用" value="disabled" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="batchDialogVisible" title="批量生成邀请码" width="450px">
      <el-form :model="batchForm" :rules="batchRules" ref="batchFormRef" label-width="80px">
        <el-form-item label="生成数量" prop="count">
          <el-input-number v-model="batchForm.count" :min="1" :max="100" />
        </el-form-item>
        <el-form-item label="前缀" prop="prefix">
          <el-input v-model="batchForm.prefix" placeholder="如：FT" />
        </el-form-item>
        <el-form-item label="算力值" prop="compute_power">
          <el-input-number v-model="batchForm.compute_power" :min="0" :max="10000" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="batchDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBatchForm">生成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getInviteCodes, createInviteCode, updateInviteCode, deleteInviteCode, batchCreateInviteCodes } from '../api/admin'

const loading = ref(false)
const codes = ref([])
const createDialogVisible = ref(false)
const batchDialogVisible = ref(false)
const editingCode = ref(null)
const formRef = ref(null)
const batchFormRef = ref(null)

const form = reactive({
  code: '',
  compute_power: 1000,
  status: 'active'
})

const batchForm = reactive({
  count: 10,
  prefix: 'FT',
  compute_power: 1000
})

const rules = {
  code: [{ required: true, message: '请输入邀请码', trigger: 'blur' }]
}

const batchRules = {
  count: [{ required: true, message: '请输入生成数量', trigger: 'blur' }],
  prefix: [{ required: true, message: '请输入前缀', trigger: 'blur' }]
}

const fetchCodes = async () => {
  loading.value = true
  try {
    const res = await getInviteCodes()
    if (res.code === 200) {
      codes.value = res.data.list
    }
  } catch (error) {
    ElMessage.error('获取邀请码列表失败')
  } finally {
    loading.value = false
  }
}

const showCreateDialog = () => {
  editingCode.value = null
  form.code = ''
  form.compute_power = 1000
  form.status = 'active'
  createDialogVisible.value = true
}

const showBatchDialog = () => {
  batchForm.count = 10
  batchForm.prefix = 'FT'
  batchForm.compute_power = 1000
  batchDialogVisible.value = true
}

const editCode = (row) => {
  editingCode.value = row
  form.code = row.code
  form.compute_power = row.compute_power
  form.status = row.status
  createDialogVisible.value = true
}

const deleteCode = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该邀请码吗？', '提示', {
      type: 'warning'
    })
    const res = await deleteInviteCode(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      fetchCodes()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return

  try {
    let res
    if (editingCode.value) {
      res = await updateInviteCode(editingCode.value.id, form)
    } else {
      res = await createInviteCode(form)
    }

    if (res.code === 200) {
      ElMessage.success(editingCode.value ? '更新成功' : '创建成功')
      createDialogVisible.value = false
      fetchCodes()
    } else {
      ElMessage.error(res.msg || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const submitBatchForm = async () => {
  const valid = await batchFormRef.value.validate().catch(() => false)
  if (!valid) return

  try {
    const res = await batchCreateInviteCodes(batchForm)
    if (res.code === 200) {
      ElMessage.success(res.msg)
      batchDialogVisible.value = false
      fetchCodes()
    } else {
      ElMessage.error(res.msg || '批量生成失败')
    }
  } catch (error) {
    ElMessage.error('批量生成失败')
  }
}

onMounted(() => {
  fetchCodes()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 10px;
}
</style>
