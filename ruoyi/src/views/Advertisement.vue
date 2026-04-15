<template>
  <div class="advertisement-container">
    <el-card class="header-card">
      <div class="header-actions">
        <el-button type="primary" @click="handleCreate">
          <el-icon><Plus /></el-icon>
          添加广告位
        </el-button>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" @tab-change="handleTabChange">
      <el-tab-pane label="全部" name="all" />
      <el-tab-pane label="已发布" name="published" />
      <el-tab-pane label="未发布" name="unpublished" />
    </el-tabs>

    <el-row :gutter="20">
      <el-col v-for="ad in filteredAds" :key="ad.id" :xs="24" :sm="12" :md="8" :lg="6">
        <el-card class="ad-card" shadow="hover">
          <div class="ad-preview">
            <el-image 
              :src="ad.image" 
              :alt="ad.title"
              fit="cover"
              class="ad-image"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><Picture /></el-icon>
                </div>
              </template>
            </el-image>
            <el-tag 
              :type="ad.status === 'published' ? 'success' : 'info'"
              class="status-tag"
            >
              {{ ad.status === 'published' ? '已发布' : '未发布' }}
            </el-tag>
          </div>
          
          <div class="ad-info">
            <h3 class="ad-title">{{ ad.title }}</h3>
            <p class="ad-link" v-if="ad.link_url">
              <el-icon><Link /></el-icon>
              {{ ad.link_url }}
            </p>
            <p class="ad-link" v-else>
              <el-icon><Link /></el-icon>
              <span class="text-muted">未设置链接</span>
            </p>
            <p class="ad-time">
              <el-icon><Clock /></el-icon>
              {{ formatTime(ad.created_at) }}
            </p>
          </div>

          <div class="ad-actions">
            <el-button size="small" @click="handlePreview(ad)">
              预览
            </el-button>
            <el-button size="small" type="primary" @click="handleEdit(ad)">
              编辑
            </el-button>
            <el-button 
              size="small" 
              :type="ad.status === 'published' ? 'warning' : 'success'"
              @click="handleToggleStatus(ad)"
            >
              {{ ad.status === 'published' ? '下架' : '发布' }}
            </el-button>
            <el-button size="small" type="danger" @click="handleDelete(ad)">
              删除
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="filteredAds.length === 0" description="暂无广告位" />

    <el-dialog
      v-model="dialogVisible"
      :title="isEditing ? '编辑广告位' : '添加广告位'"
      width="600px"
    >
      <el-form :model="form" label-width="100px">
        <el-form-item label="广告标题" required>
          <el-input v-model="form.title" placeholder="请输入广告标题" />
        </el-form-item>

        <el-form-item label="广告图片" required>
          <el-upload
            class="avatar-uploader"
            :show-file-list="false"
            :before-upload="beforeImageUpload"
            :http-request="handleImageUpload"
          >
            <img v-if="form.image" :src="form.image" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <div class="form-tip">支持 JPG、PNG 格式，大小不超过 5MB</div>
        </el-form-item>

        <el-form-item label="跳转链接">
          <el-input v-model="form.link_url" placeholder="请输入点击跳转的URL地址">
            <template #prefix>
              <el-icon><Link /></el-icon>
            </template>
          </el-input>
        </el-form-item>

        <el-form-item label="排序权重">
          <el-input-number v-model="form.sort_order" :min="0" :max="999" />
          <div class="form-tip">数字越小排序越靠前</div>
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave" :loading="loading">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="previewVisible" title="广告预览" width="600px">
      <div class="preview-content" v-if="currentAd">
        <el-image :src="currentAd.image" fit="cover" class="preview-image" />
        <div class="preview-info">
          <h3>{{ currentAd.title }}</h3>
          <p v-if="currentAd.link_url">
            链接: <a :href="currentAd.link_url" target="_blank">{{ currentAd.link_url }}</a>
          </p>
          <p>状态: {{ currentAd.status === 'published' ? '已发布' : '未发布' }}</p>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Picture, Link, Clock } from '@element-plus/icons-vue'

const API_BASE_URL = ''

const advertisements = ref([])
const activeTab = ref('all')
const dialogVisible = ref(false)
const previewVisible = ref(false)
const isEditing = ref(false)
const loading = ref(false)
const currentAd = ref(null)
const currentAdId = ref(null)

const form = ref({
  title: '',
  image: '',
  link_url: '',
  sort_order: 0
})

const filteredAds = computed(() => {
  if (activeTab.value === 'all') return advertisements.value
  if (activeTab.value === 'published') {
    return advertisements.value.filter(ad => ad.status === 'published')
  }
  return advertisements.value.filter(ad => ad.status !== 'published')
})

const fetchAdvertisements = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/api/admin/advertisements?status=all`)
    const result = await response.json()
    if (result.code === 200) {
      advertisements.value = result.data.list
    }
  } catch (error) {
    console.error('获取广告列表失败:', error)
    ElMessage.error('获取广告列表失败')
  }
}

const beforeImageUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

const handleImageUpload = (options) => {
  const { file, onSuccess, onError } = options
  const reader = new FileReader()
  reader.onload = (e) => {
    form.value.image = e.target.result
    onSuccess()
  }
  reader.onerror = () => {
    onError()
    ElMessage.error('图片上传失败')
  }
  reader.readAsDataURL(file)
}

const formatTime = (time) => {
  if (!time) return ''
  const date = new Date(time)
  return date.toLocaleString('zh-CN')
}

const handleCreate = () => {
  isEditing.value = false
  currentAdId.value = null
  form.value = {
    title: '',
    image: '',
    link_url: '',
    sort_order: 0
  }
  dialogVisible.value = true
}

const handleEdit = (ad) => {
  isEditing.value = true
  currentAdId.value = ad.id
  form.value = {
    title: ad.title,
    image: ad.image,
    link_url: ad.link_url || '',
    sort_order: ad.sort_order || 0
  }
  dialogVisible.value = true
}

const handlePreview = (ad) => {
  currentAd.value = ad
  previewVisible.value = true
}

const handleSave = async () => {
  if (!form.value.title) {
    ElMessage.warning('请输入广告标题')
    return
  }

  loading.value = true
  try {
    let response
    if (isEditing.value) {
      response = await fetch(`${API_BASE_URL}/api/admin/advertisements/${currentAdId.value}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value)
      })
    } else {
      form.value.status = 'draft'
      response = await fetch(`${API_BASE_URL}/api/admin/advertisements`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form.value)
      })
    }

    const result = await response.json()
    if (result.code === 200) {
      ElMessage.success(isEditing.value ? '广告位更新成功' : '广告位创建成功')
      dialogVisible.value = false
      await fetchAdvertisements()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    loading.value = false
  }
}

const handleToggleStatus = async (ad) => {
  const action = ad.status === 'published' ? '下架' : '发布'
  const endpoint = ad.status === 'published' ? 'unpublish' : 'publish'

  try {
    await ElMessageBox.confirm(`确定要${action}这个广告位吗?`, '确认操作', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const response = await fetch(`${API_BASE_URL}/api/admin/advertisements/${ad.id}/${endpoint}`, {
      method: 'POST'
    })
    const result = await response.json()

    if (result.code === 200) {
      ElMessage.success(`广告位${action}成功`)
      await fetchAdvertisements()
    } else {
      ElMessage.error(result.msg || '操作失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('状态切换失败:', error)
      ElMessage.error('操作失败')
    }
  }
}

const handleDelete = async (ad) => {
  try {
    await ElMessageBox.confirm('确定要删除这个广告位吗? 此操作不可撤销', '确认删除', {
      confirmButtonText: '删除',
      cancelButtonText: '取消',
      type: 'warning'
    })

    const response = await fetch(`${API_BASE_URL}/api/admin/advertisements/${ad.id}`, {
      method: 'DELETE'
    })
    const result = await response.json()

    if (result.code === 200) {
      ElMessage.success('广告位删除成功')
      await fetchAdvertisements()
    } else {
      ElMessage.error(result.msg || '删除失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

const handleTabChange = () => {
  console.log('Tab changed:', activeTab.value)
}

onMounted(() => {
  fetchAdvertisements()
})
</script>

<style scoped>
.advertisement-container {
  padding: 20px;
}

.header-card {
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.ad-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.ad-card:hover {
  transform: translateY(-4px);
}

.ad-preview {
  position: relative;
  height: 200px;
  background: #f5f5f5;
  border-radius: 4px;
  overflow: hidden;
}

.ad-image {
  width: 100%;
  height: 100%;
}

.image-error {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f5f5;
  color: #999;
  font-size: 48px;
}

.status-tag {
  position: absolute;
  top: 10px;
  right: 10px;
}

.ad-info {
  padding: 15px 0;
}

.ad-title {
  margin: 0 0 10px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.ad-link {
  margin: 5px 0;
  font-size: 14px;
  color: #606266;
  display: flex;
  align-items: center;
  gap: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.text-muted {
  color: #909399;
}

.ad-time {
  margin: 10px 0 0 0;
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 5px;
}

.ad-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 10px;
  border-top: 1px solid #eee;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  width: 200px;
  height: 150px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c9398;
}

.form-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 5px;
}

.preview-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.preview-image {
  width: 100%;
  border-radius: 8px;
}

.preview-info h3 {
  margin: 0 0 10px 0;
  font-size: 20px;
  color: #303133;
}

.preview-info p {
  margin: 8px 0;
  font-size: 14px;
  color: #606266;
}

.preview-info a {
  color: #409eff;
  text-decoration: none;
}

.preview-info a:hover {
  text-decoration: underline;
}
</style>
