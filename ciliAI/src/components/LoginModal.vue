<template>
  <el-dialog
    v-model="visible"
    width="500px"
    :show-close="false"
    :close-on-click-modal="true"
    class="login-dialog"
    destroy-on-close
  >
    <div class="login-modal-content">
      <!-- 邀请码输入 -->
      <div class="input-row">
        <div class="invite-icon">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="8" width="18" height="4" rx="1"></rect>
            <path d="M12 8v13"></path>
            <path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"></path>
            <path d="M7.5 8a2.5 2.5 0 0 1 0-5 2.5 2.5 0 0 1 2.5 2.5v5"></path>
            <path d="M16.5 8v-2.5a2.5 2.5 0 0 1 5 0 2.5 2.5 0 0 1-2.5 2.5h-5"></path>
          </svg>
        </div>
        <input
          v-model="form.inviteCode"
          type="text"
          placeholder="请输入8位登录凭据"
          class="invite-input"
          maxlength="8"
          @keyup.enter="handleLogin"
        />
      </div>

      <!-- 登录/注册按钮 -->
      <button class="login-submit-btn" @click="handleLogin" :disabled="loading">
        <span v-if="loading">登录中...</span>
        <span v-else>登录</span>
      </button>

      <!-- 下次自动登录 -->
      <div class="auto-login-row">
        <div
          class="checkbox"
          :class="{ checked: form.autoLogin }"
          @click="toggleAutoLogin"
        >
          <svg v-if="form.autoLogin" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"></polyline>
          </svg>
        </div>
        <span class="auto-login-text">下次自动登录</span>
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

const emit = defineEmits(['update:modelValue', 'login'])

const visible = ref(props.modelValue)
const loading = ref(false)

const form = reactive({
  inviteCode: '',
  autoLogin: true
})

watch(() => props.modelValue, (val) => {
  visible.value = val
})

watch(visible, (val) => {
  emit('update:modelValue', val)
})

const toggleAutoLogin = () => {
  form.autoLogin = !form.autoLogin
}

const handleLogin = async () => {
  if (!form.inviteCode.trim()) {
    ElMessage.error('请输入登录凭据')
    return
  }
  
  if (form.inviteCode.trim().length !== 8) {
    ElMessage.error('登录凭据必须为8位字符')
    return
  }

  loading.value = true

  try {
    const response = await fetch('/api/verify-invite-code', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        invite_code: form.inviteCode.toUpperCase()
      })
    })

    const result = await response.json()

    if (response.ok && result.status === 'success') {
      ElMessage.success(result.message || '登录成功')
      
      emit('login', { 
        inviteCode: form.inviteCode,
        computingPower: result['算力'] || 1000,
        isNewUser: result.is_new_user
      })
      
      visible.value = false
    } else {
      ElMessage.error(result.message || result.error || '登录失败')
    }
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error('登录失败，请稍后重试')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-modal-content {
  padding: 40px 20px;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-modal-content::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 100px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.3));
  border-radius: 0 0 12px 12px;
  pointer-events: none;
}

.input-row {
  display: flex;
  align-items: center;
  background-color: #BACACB;
  border-radius: 8px;
  margin-bottom: 16px;
  height: 52px;
  overflow: hidden;
  width: 100%;
  max-width: 300px;
}

.country-code {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 0 16px;
  color: #425D5F;
  font-size: 16px;
  font-weight: 500;
  border-right: 1px solid #425D5F;
  height: 100%;
  cursor: pointer;
}

.phone-input,
.code-input,
.invite-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  color: #425D5F;
  font-size: 14px;
  padding: 0 16px;
  height: 100%;
}

.phone-input::placeholder,
.code-input::placeholder,
.invite-input::placeholder {
  color: #888;
}

.verify-row {
  background: transparent;
  gap: 12px;
  padding: 0;
}

.code-input {
  background-color: #BACACB;
  border-radius: 8px;
}

.verify-btn {
  width: 120px;
  height: 52px;
  background-color: #BACACB;
  border: none;
  border-radius: 8px;
  color: #425D5F;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.verify-btn:hover:not(:disabled) {
  background-color: #5a5a5a;
}

.verify-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.invite-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  color: #425D5F;
  border-right: 1px solid #425D5F;
  height: 100%;
}

.login-submit-btn {
  width: 100%;
  max-width: 300px;
  height: 52px;
  background: linear-gradient(135deg, #FAA943 0%, #FDE7A2 100%);
  border: none;
  border-radius: 8px;
  color: #425D5F;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 8px;
  transition: all 0.3s ease;
}

.login-submit-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(250, 169, 67, 0.3);
}

.login-submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.auto-login-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 16px;
  width: 100%;
  max-width: 300px;
}

.checkbox {
  width: 18px;
  height: 18px;
  border-radius: 4px;
  border: 2px solid #425D5F;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #425D5F;
}

.checkbox.checked {
  background-color: #425D5F;
}

.auto-login-text {
  color: #888;
  font-size: 14px;
}
</style>

<style>
.login-dialog {
  --el-dialog-bg-color: #F8F7F2 !important;
  --el-dialog-border-radius: 12px !important;
  --el-dialog-padding-primary: 0 !important;
}

.login-dialog .el-dialog__header {
  display: none;
}

.login-dialog .el-dialog__body {
  padding: 0;
}
</style>
