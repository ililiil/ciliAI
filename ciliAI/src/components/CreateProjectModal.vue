<template>
  <el-dialog
    v-model="visible"
    width="600px"
    :title="'创建项目'"
    :show-close="true"
    :close-on-click-modal="true"
    class="create-project-dialog"
    destroy-on-close
  >
    <div class="create-project-content">
      <!-- 项目名称 -->
      <div class="form-row">
        <label class="form-label">项目名称</label>
        <input
          v-model="form.projectName"
          type="text"
          placeholder="请输入短剧项目名称"
          class="form-input"
        />
      </div>

      <!-- 封面图片 -->
      <div class="form-row">
        <label class="form-label">封面图片（可选）</label>
        <div class="cover-upload-wrapper">
          <input
            type="file"
            accept="image/*"
            @change="handleCoverUpload"
            ref="coverInput"
            style="display: none;"
          />
          <div v-if="!form.cover" class="cover-upload-trigger" @click="triggerCoverUpload">
            <div class="upload-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <polyline points="21 15 16 10 5 21"/>
              </svg>
            </div>
            <div class="upload-text">点击上传封面图片</div>
            <div class="upload-hint">支持 JPG、PNG 格式，建议尺寸 800x450，最大 5MB</div>
          </div>
          <div v-else class="cover-preview">
            <img :src="form.cover" alt="封面预览" class="cover-preview-image" />
            <div class="cover-preview-overlay">
              <button class="remove-cover-btn" @click="removeCover">移除</button>
              <button class="change-cover-btn" @click="triggerCoverUpload">更换</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 剧集数 -->
      <div class="form-row">
        <label class="form-label">剧集数</label>
        <input
          v-model.number="form.episodes"
          type="number"
          placeholder="请输入剧集数"
          class="form-input"
          min="0"
        />
        <div class="form-hint">0即默认不分集</div>
      </div>

      <!-- 按钮 -->
      <div class="form-actions">
        <button class="cancel-btn" @click="handleCancel">取消</button>
        <button class="create-btn" @click="handleCreate">立即创建</button>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'create'])

const visible = ref(props.modelValue)
const coverInput = ref(null)

const form = reactive({
  projectName: '',
  episodes: 0,
  cover: ''
})

watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
  if (!val) {
    Object.assign(form, {
      projectName: '',
      episodes: 0,
      cover: ''
    })
  }
})

const handleCancel = () => {
  visible.value = false
}

const triggerCoverUpload = () => {
  coverInput.value.click()
}

const handleCoverUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    ElMessage.error('只能上传图片文件！')
    return
  }
  
  const isLt5M = file.size / 1024 / 1024 < 5
  if (!isLt5M) {
    ElMessage.error('封面图片大小不能超过 5MB！')
    return
  }
  
  const reader = new FileReader()
  reader.onload = (e) => {
    form.cover = e.target.result
  }
  reader.readAsDataURL(file)
}

const removeCover = () => {
  form.cover = ''
  if (coverInput.value) {
    coverInput.value.value = ''
  }
}

const handleCreate = () => {
  if (!form.projectName.trim()) {
    ElMessage.warning('请输入项目名称')
    return
  }
  
  emit('create', { ...form })
  visible.value = false
}
</script>

<style scoped>
.create-project-content {
  padding: 20px 0;
}

.form-row {
  margin-bottom: 24px;
}

.form-label {
  display: block;
  color: #425D5F;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 12px;
}

.form-input {
  width: 100%;
  background-color: #BACACB;
  border: none;
  border-radius: 8px;
  padding: 12px 16px;
  color: #425D5F;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
}

.form-input:focus {
  box-shadow: 0 0 0 2px rgba(250, 169, 67, 0.3);
}

.form-input::placeholder {
  color: #888;
}

.form-hint {
  color: #666;
  font-size: 12px;
  margin-top: 6px;
}

/* 封面上传 */
.cover-upload-wrapper {
  width: 100%;
}

.cover-upload-trigger {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 20px;
  cursor: pointer;
  border: 2px dashed #dcdfe6;
  border-radius: 8px;
  transition: all 0.3s;
  background-color: #fff;
}

.cover-upload-trigger:hover {
  border-color: #425D5F;
  background-color: rgba(66, 93, 95, 0.05);
}

.cover-upload-trigger .upload-icon {
  color: #BACACB;
}

.cover-upload-trigger .upload-text {
  font-size: 14px;
  color: #425D5F;
  font-weight: 500;
}

.cover-upload-trigger .upload-hint {
  font-size: 12px;
  color: #999;
  text-align: center;
}

.cover-preview {
  position: relative;
  width: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.cover-preview-image {
  width: 100%;
  aspect-ratio: 16/9;
  object-fit: cover;
  border-radius: 8px;
  border: 1px solid #BACACB;
}

.cover-preview-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  opacity: 0;
  transition: opacity 0.3s;
  border-radius: 8px;
}

.cover-preview:hover .cover-preview-overlay {
  opacity: 1;
}

.remove-cover-btn,
.change-cover-btn {
  padding: 8px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
  border: none;
}

.remove-cover-btn {
  background-color: #f56c6c;
  color: white;
}

.remove-cover-btn:hover {
  background-color: #e64141;
}

.change-cover-btn {
  background-color: #409eff;
  color: white;
}

.change-cover-btn:hover {
  background-color: #66b1ff;
}

/* 按钮 */
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 32px;
}

.cancel-btn {
  padding: 10px 24px;
  background-color: #BACACB;
  border: none;
  border-radius: 6px;
  color: #425D5F;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background-color: #425D5F;
}

.create-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #FAA943 0%, #FDE7A2 100%);
  border: none;
  border-radius: 6px;
  color: #425D5F;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(250, 169, 67, 0.3);
}
</style>

<style>
.create-project-dialog {
  --el-dialog-bg-color: #F8F7F2 !important;
  --el-dialog-border-radius: 12px !important;
  --el-dialog-title-color: #425D5F !important;
}

.create-project-dialog .el-dialog__header {
  border-bottom: 1px solid #BACACB;
  padding: 20px 24px;
}

.create-project-dialog .el-dialog__body {
  padding: 0 24px;
}

.create-project-dialog .el-dialog__footer {
  display: none;
}
</style>
