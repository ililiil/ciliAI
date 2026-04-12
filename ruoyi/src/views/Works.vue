<template>
  <div class="works">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>社区分享内容管理</span>
          <el-button type="primary" @click="showCreateDialog">
            <el-icon><Plus /></el-icon>
            上传作品
          </el-button>
        </div>
      </template>

      <el-table :data="works" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="封面" width="120">
          <template #default="{ row }">
            <el-image 
              :src="getFullImageUrl(row.image)" 
              style="width: 80px; height: 60px;" 
              fit="cover"
              :preview-src-list="[getFullImageUrl(row.image)]"
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
        <el-table-column prop="title" label="作品名称" min-width="150" />
        <el-table-column prop="student_name" label="学员名称" width="120" />
        <el-table-column prop="cost" label="算力成本" width="120" />
        <el-table-column prop="duration" label="制作时长" width="100" />
        <el-table-column prop="status" label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
              {{ row.status === 'active' ? '已发布' : '已下架' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="category" label="分类" width="100">
          <template #default="{ row }">
            <el-tag :type="row.category === 'IP版权库' ? 'primary' : 'success'" size="small">
              {{ row.category === 'IP版权库' ? 'IP版权库' : '社区分享' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="editWork(row)">编辑</el-button>
            <el-button link type="warning" @click="toggleStatus(row)">
              {{ row.status === 'active' ? '下架' : '发布' }}
            </el-button>
            <el-button link type="danger" @click="confirmDeleteWork(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="createDialogVisible" :title="editingWork ? '编辑作品' : '上传作品'" width="650px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="作品名称" prop="title">
              <el-input v-model="form.title" placeholder="请输入作品名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学员名称" prop="student_name">
              <el-input v-model="form.student_name" placeholder="请输入学员姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="封面图片" prop="image">
          <el-input v-model="form.image" placeholder="请输入图片URL" style="margin-bottom: 10px;" />
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
              <img v-if="form.image" :src="getFullImageUrl(form.image)" class="cover-image" />
              <el-icon v-else class="cover-uploader-icon"><Plus /></el-icon>
            </el-upload>
            <div class="upload-tip">支持 JPG、PNG、GIF、WebP 格式</div>
          </div>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="算力成本" prop="cost">
              <el-input v-model="form.cost" placeholder="如：1000算力/分钟" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="制作时长" prop="duration">
              <el-input v-model="form.duration" placeholder="如：420分钟" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="市场价格" prop="price">
              <el-input v-model="form.price" placeholder="如：150-300元/分钟" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="版权信息" prop="copyright">
              <el-input v-model="form.copyright" placeholder="如：归CiliAI所有" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="标签" prop="tags">
          <el-select v-model="form.tags" multiple placeholder="请选择标签" style="width: 100%;">
            <el-option label="AI动画" value="AI动画" />
            <el-option label="AI真人" value="AI真人" />
            <el-option label="古风" value="古风" />
            <el-option label="穿越" value="穿越" />
            <el-option label="现代科幻" value="现代科幻" />
            <el-option label="悬疑" value="悬疑" />
            <el-option label="都市" value="都市" />
          </el-select>
        </el-form-item>

        <el-form-item label="作品简介" prop="introduction">
          <el-input v-model="form.introduction" type="textarea" :rows="4" placeholder="请输入作品简介" />
        </el-form-item>

        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" placeholder="请选择分类" style="width: 100%;">
            <el-option label="IP版权库" value="IP版权库" />
            <el-option label="社区分享" value="社区分享" />
          </el-select>
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Picture, Plus } from '@element-plus/icons-vue'
import { getWorks, createWork, updateWork, deleteWork as deleteWorkApi } from '../api/admin'

const loading = ref(false)
const works = ref([])
const createDialogVisible = ref(false)
const editingWork = ref(null)
const formRef = ref(null)

const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5002'
const uploadHeaders = {
  'Authorization': localStorage.getItem('admin_token') || ''
}

const getFullImageUrl = (url) => {
  if (!url) return ''
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }
  return baseURL + url
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
    form.image = response.data.url
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
  student_name: '',
  image: '',
  cost: '',
  duration: '',
  price: '',
  copyright: '归CiliAI所有',
  tags: [],
  introduction: '',
  category: 'IP版权库'
})

const rules = {
  title: [{ required: true, message: '请输入作品名称', trigger: 'blur' }],
  student_name: [{ required: true, message: '请输入学员姓名', trigger: 'blur' }],
  image: [{ required: true, message: '请输入封面图片URL', trigger: 'blur' }]
}

const fetchWorks = async () => {
  loading.value = true
  try {
    const res = await getWorks()
    if (res.code === 200) {
      works.value = res.data.list.map(item => ({
        ...item,
        tags: item.tags ? JSON.parse(item.tags) : []
      }))
    }
  } catch (error) {
    ElMessage.error('获取作品列表失败')
  } finally {
    loading.value = false
  }
}

const showCreateDialog = () => {
  editingWork.value = null
  form.title = ''
  form.student_name = ''
  form.image = ''
  form.cost = ''
  form.duration = ''
  form.price = ''
  form.copyright = '归CiliAI所有'
  form.tags = []
  form.introduction = ''
  form.category = 'IP版权库'
  createDialogVisible.value = true
}

const editWork = (row) => {
  editingWork.value = row
  form.title = row.title
  form.student_name = row.student_name
  form.image = row.image
  form.cost = row.cost
  form.duration = row.duration
  form.price = row.price
  form.copyright = row.copyright
  form.tags = row.tags || []
  form.introduction = row.introduction
  form.category = row.category || 'IP版权库'
  createDialogVisible.value = true
}

const toggleStatus = async (row) => {
  const newStatus = row.status === 'active' ? 'inactive' : 'active'
  try {
    const res = await updateWork(row.id, { status: newStatus })
    if (res.code === 200) {
      ElMessage.success(newStatus === 'active' ? '发布成功' : '下架成功')
      fetchWorks()
    } else {
      ElMessage.error(res.msg || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteWorkItem = async (row) => {
  try {
    const res = await deleteWorkApi(row.id)
    if (res.code === 200) {
      ElMessage.success('删除成功')
      fetchWorks()
    } else {
      ElMessage.error(res.msg || '删除失败')
    }
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

const confirmDeleteWork = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该作品吗？', '提示', {
      type: 'warning'
    })
    await deleteWorkItem(row)
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
    if (editingWork.value) {
      res = await updateWork(editingWork.value.id, form)
    } else {
      res = await createWork(form)
    }

    if (res.code === 200) {
      ElMessage.success(editingWork.value ? '更新成功' : '创建成功')
      createDialogVisible.value = false
      fetchWorks()
    } else {
      ElMessage.error(res.msg || '操作失败')
    }
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchWorks()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.image-preview {
  margin-top: 10px;
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
