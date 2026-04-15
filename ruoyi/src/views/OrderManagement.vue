<template>
  <div class="order-management">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>接单管理</span>
          <el-button type="primary" @click="showCreateDialog">
            <el-icon><Plus /></el-icon>
            添加订单
          </el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab" @tab-change="handleTabChange">
        <el-tab-pane label="全部" name="all"></el-tab-pane>
        <el-tab-pane label="待开始" name="pending"></el-tab-pane>
        <el-tab-pane label="招募中" name="recruiting"></el-tab-pane>
        <el-tab-pane label="已结束" name="ended"></el-tab-pane>
      </el-tabs>

      <el-table :data="filteredOrders" v-loading="loading" stripe style="margin-top: 20px;">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="封面" width="120">
          <template #default="{ row }">
            <el-image
              :src="row.image"
              style="width: 80px; height: 60px;"
              fit="cover"
              :preview-src-list="[row.image]"
              :initial-index="0"
            >
              <template #error>
                <div class="image-slot">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="订单标题" min-width="200" />
        <el-table-column prop="price" label="价格" width="120">
          <template #default="{ row }">
            <span style="color: #E6A23C; font-weight: 600;">{{ row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="deadline" label="截止日期" width="120" />
        <el-table-column prop="contactCount" label="联系数" width="80" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="标签" width="180">
          <template #default="{ row }">
            <el-tag
              v-for="tag in row.tags"
              :key="tag"
              size="small"
              style="margin-right: 4px;"
            >
              {{ tag }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="editOrder(row)">编辑</el-button>
            <el-button link type="warning" @click="toggleStatus(row)">
              {{ getNextStatus(row.status) }}
            </el-button>
            <el-button link type="danger" @click="confirmDeleteOrder(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="createDialogVisible" :title="editingOrder ? '编辑订单' : '添加订单'" width="700px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-form-item label="订单标题" prop="title">
          <el-input v-model="form.title" placeholder="请输入订单标题" />
        </el-form-item>

        <el-form-item label="封面图片" prop="image">
          <el-input v-model="form.image" placeholder="请输入封面图片URL" style="margin-bottom: 10px;" />
          <div class="cover-upload">
            <el-upload
              class="cover-uploader"
              action="/api/admin/upload"
              :show-file-list="false"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              :before-upload="beforeUpload"
              :headers="uploadHeaders"
              accept="image/*"
            >
              <img v-if="form.image" :src="form.image" class="cover-image" />
              <el-icon v-else class="cover-uploader-icon"><Plus /></el-icon>
            </el-upload>
            <div class="upload-tip">支持 JPG、PNG、GIF、WebP 格式</div>
          </div>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="价格" prop="price">
              <el-input v-model="form.price" placeholder="如：¥5000" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="截止日期" prop="deadline">
              <el-date-picker
                v-model="form.deadline"
                type="date"
                placeholder="选择日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%;">
                <el-option label="待开始" value="pending" />
                <el-option label="招募中" value="recruiting" />
                <el-option label="已结束" value="ended" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="联系数" prop="contactCount">
              <el-input-number v-model="form.contactCount" :min="0" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="标签" prop="tags">
          <el-select v-model="form.tags" multiple placeholder="请选择标签" style="width: 100%;">
            <el-option label="AI真人" value="AI真人" />
            <el-option label="AI动画" value="AI动画" />
            <el-option label="现代都市" value="现代都市" />
            <el-option label="古装历史" value="古装历史" />
            <el-option label="科幻题材" value="科幻题材" />
            <el-option label="都市" value="都市" />
            <el-option label="古风" value="古风" />
            <el-option label="穿越" value="穿越" />
            <el-option label="悬疑" value="悬疑" />
          </el-select>
        </el-form-item>

        <el-form-item label="二维码" prop="qrcode">
          <el-input v-model="form.qrcode" placeholder="请输入企业微信二维码URL" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Picture, Plus } from '@element-plus/icons-vue'

const loading = ref(false)
const orders = ref([])
const activeTab = ref('all')
const createDialogVisible = ref(false)
const editingOrder = ref(null)
const formRef = ref(null)

const uploadHeaders = {
  'Authorization': localStorage.getItem('admin_token') || ''
}

const baseURL = import.meta.env.VITE_API_BASE_URL || ''

const filteredOrders = computed(() => {
  if (activeTab.value === 'all') {
    return orders.value
  }
  return orders.value.filter(order => order.status === activeTab.value)
})

const getStatusText = (status) => {
  const statusMap = {
    'pending': '待开始',
    'recruiting': '招募中',
    'ended': '已结束'
  }
  return statusMap[status] || status
}

const getStatusType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'recruiting': 'success',
    'ended': 'info'
  }
  return typeMap[status] || ''
}

const getNextStatus = (status) => {
  const nextMap = {
    'pending': '设为招募中',
    'recruiting': '设为已结束',
    'ended': '设为待开始'
  }
  return nextMap[status] || '切换状态'
}

const handleTabChange = (tab) => {
  activeTab.value = tab
}

const beforeUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt15M = file.size / 1024 / 1024 < 15

  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return false
  }
  if (!isLt15M) {
    ElMessage.error('图片大小不能超过 15MB！')
    return false
  }
  return true
}

const handleUploadSuccess = (response) => {
  if (response.code === 200) {
    form.image = baseURL + response.data.url
    ElMessage.success('封面上传成功')
  } else {
    ElMessage.error(response.msg || '上传失败')
  }
}

const handleUploadError = () => {
  ElMessage.error('上传失败，请重试')
}

const form = reactive({
  title: '',
  image: '',
  price: '',
  deadline: '',
  status: 'recruiting',
  tags: [],
  qrcode: '',
  contactCount: 0
})

const rules = {
  title: [{ required: true, message: '请输入订单标题', trigger: 'blur' }],
  image: [{ required: true, message: '请输入封面图片URL', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }],
  deadline: [{ required: true, message: '请选择截止日期', trigger: 'change' }]
}

const fetchOrders = async () => {
  loading.value = true
  try {
    const baseURL = import.meta.env.VITE_API_BASE_URL || ''
    const response = await fetch(`${baseURL}/api/admin/orders`)
    const result = await response.json()
    
    if (result.code === 200) {
      orders.value = result.data.list
    } else {
      console.error('获取订单列表失败', result.msg)
      orders.value = []
    }
  } catch (error) {
    console.error('获取订单列表失败', error)
    orders.value = []
  } finally {
    loading.value = false
  }
}

const showCreateDialog = () => {
  editingOrder.value = null
  form.title = ''
  form.image = ''
  form.price = ''
  form.deadline = ''
  form.status = 'recruiting'
  form.tags = []
  form.qrcode = ''
  form.contactCount = 0
  createDialogVisible.value = true
}

const editOrder = (row) => {
  editingOrder.value = row
  form.title = row.title
  form.image = row.image
  form.price = row.price
  form.deadline = row.deadline
  form.status = row.status
  form.tags = [...row.tags]
  form.qrcode = row.qrcode || ''
  form.contactCount = row.contactCount
  createDialogVisible.value = true
}

const toggleStatus = async (row) => {
  const statusCycle = {
    'pending': 'recruiting',
    'recruiting': 'ended',
    'ended': 'pending'
  }
  const newStatus = statusCycle[row.status]

  try {
    await ElMessageBox.confirm(
      `确定要将状态从"${getStatusText(row.status)}"改为"${getStatusText(newStatus)}"吗？`,
      '提示',
      { type: 'warning' }
    )

    const baseURL = import.meta.env.VITE_API_BASE_URL || ''
    const response = await fetch(`${baseURL}/api/admin/orders/${row.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status: newStatus })
    })
    
    if (response.ok) {
      row.status = newStatus
      ElMessage.success('状态更新成功')
    } else {
      throw new Error('更新失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('状态更新失败')
    }
  }
}

const deleteOrder = async (row) => {
  try {
    const baseURL = import.meta.env.VITE_API_BASE_URL || ''
    const response = await fetch(`${baseURL}/api/admin/orders/${row.id}`, {
      method: 'DELETE'
    })
    
    if (response.ok) {
      const index = orders.value.findIndex(item => item.id === row.id)
      if (index > -1) {
        orders.value.splice(index, 1)
      }
    } else {
      throw new Error('删除失败')
    }
  } catch (error) {
    console.error('删除订单失败', error)
    throw error
  }
}

const confirmDeleteOrder = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该订单吗？', '提示', {
      type: 'warning'
    })
    await deleteOrder(row)
    ElMessage.success('删除成功')
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
    const baseURL = import.meta.env.VITE_API_BASE_URL || ''
    const orderData = {
      title: form.title,
      image: form.image,
      price: form.price,
      deadline: form.deadline,
      status: form.status,
      tags: form.tags,
      qrcode: form.qrcode,
      contactCount: form.contactCount
    }
    
    if (editingOrder.value) {
      const response = await fetch(`${baseURL}/api/admin/orders/${editingOrder.value.id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      })
      
      if (response.ok) {
        Object.assign(editingOrder.value, orderData)
        ElMessage.success('订单更新成功')
      } else {
        throw new Error('更新失败')
      }
    } else {
      const response = await fetch(`${baseURL}/api/admin/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      })
      
      if (response.ok) {
        const result = await response.json()
        const newOrder = {
          id: result.data.id,
          ...orderData
        }
        orders.value.unshift(newOrder)
        ElMessage.success('订单添加成功')
      } else {
        throw new Error('创建失败')
      }
    }

    createDialogVisible.value = false
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchOrders()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 24px;
}

.cover-upload {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.cover-uploader {
  border: 1px dashed var(--el-border-color);
  border-radius: 8px;
  overflow: hidden;
  transition: border-color 0.3s;
  width: 200px;
  height: 150px;
  cursor: pointer;
  position: relative;
}

.cover-uploader:hover {
  border-color: var(--el-color-primary);
}

.cover-uploader .el-upload {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cover-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-uploader-icon {
  font-size: 28px;
  color: #8c939d;
}

.upload-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}
</style>
