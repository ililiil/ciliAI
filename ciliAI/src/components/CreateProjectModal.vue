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

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'create'])

const visible = ref(props.modelValue)

const form = reactive({
  projectName: '',
  episodes: 0
})

watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
  if (!val) {
    Object.assign(form, {
      projectName: '',
      episodes: 0
    })
  }
})

const handleCancel = () => {
  visible.value = false
}

const handleCreate = () => {
  if (!form.projectName.trim()) {
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
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 12px;
}

.form-input {
  width: 100%;
  background-color: #2a2a2a;
  border: none;
  border-radius: 8px;
  padding: 12px 16px;
  color: #fff;
  font-size: 14px;
  outline: none;
  transition: all 0.3s ease;
}

.form-input:focus {
  box-shadow: 0 0 0 2px rgba(163, 230, 53, 0.3);
}

.form-input::placeholder {
  color: #888;
}

.form-hint {
  color: #666;
  font-size: 12px;
  margin-top: 6px;
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
  background-color: #4a4a4a;
  border: none;
  border-radius: 6px;
  color: #fff;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.cancel-btn:hover {
  background-color: #5a5a5a;
}

.create-btn {
  padding: 10px 24px;
  background: linear-gradient(135deg, #a3e635 0%, #84cc16 100%);
  border: none;
  border-radius: 6px;
  color: #1d1d1d;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.create-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(163, 230, 53, 0.3);
}
</style>

<style>
.create-project-dialog {
  --el-dialog-bg-color: #1d1d1d !important;
  --el-dialog-border-radius: 12px !important;
  --el-dialog-title-color: #fff !important;
}

.create-project-dialog .el-dialog__header {
  border-bottom: 1px solid #2a2a2a;
  padding: 20px 24px;
}

.create-project-dialog .el-dialog__body {
  padding: 0 24px;
}

.create-project-dialog .el-dialog__footer {
  display: none;
}
</style>
