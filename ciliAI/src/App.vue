<template>
  <div class="layout-container">
    <div class="layout-sidebar flex flex-col relative">
      <div style="display: flex; align-items: center; justify-content: center; height: 63px; padding: 0 16px;">
        <div style="text-align: center; font-size: 1.5rem; font-weight: bold; color: white;">CiliAI</div>
      </div>
      <div class="flex-1 flex flex-col min-h-0 overflow-y-auto">
        <el-menu
          :default-active="activeIndex"
          class="flex-1 w-full pt-8 pb-4"
          mode="vertical"
          @select="handleMenuSelect"
          background-color="transparent"
          text-color="#fff"
          active-text-color="#a3e635"
          :unique-opened="true"
        >
          <el-menu-item index="1">
            <el-icon>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-house">
                <path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"></path>
                <path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              </svg>
            </el-icon>
            <span>首页</span>
          </el-menu-item>
          <el-menu-item index="2">
            <el-icon>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
              </svg>
            </el-icon>
            <span>我的项目</span>
          </el-menu-item>
          <el-menu-item index="3">
            <el-icon>
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect width="18" height="18" x="3" y="3" rx="2" ry="2"></rect>
                <line x1="3" x2="21" y1="9" y2="9"></line>
                <line x1="9" x2="9" y1="21" y2="9"></line>
              </svg>
            </el-icon>
            <span>接单广场</span>
          </el-menu-item>
        </el-menu>
      </div>
      <div class="sidebar-footer">
        <div class="footer-item">
          <el-icon>
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            </svg>
          </el-icon>
          <span>算力</span>
          <span class="value">{{ computingPower.toLocaleString() }}</span>
        </div>
        <div class="footer-login">
          <button v-if="!isLoggedIn" class="login-btn" @click="handleLogin">
            登录
          </button>
          <div v-else class="logout-text" @click="handleLogout">
            退出登录
          </div>
        </div>
      </div>
    </div>
    <div class="layout-main">
      <div class="layout-content">
        <router-view v-slot="{ Component }">
          <transition name="fade">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </div>
  </div>

  <LoginModal v-model="showLoginModal" @login="handleLoginSubmit" />
</template>

<script setup>
import { ref, onMounted, watch, provide } from 'vue'
import { useRoute } from 'vue-router'
import router from './router'
import LoginModal from './components/LoginModal.vue'

const route = useRoute()
const activeIndex = ref('1')
const isLoggedIn = ref(false)
const showLoginModal = ref(false)
const computingPower = ref(0)
const currentInviteCode = ref('')

provide('isLoggedIn', isLoggedIn)
provide('computingPower', computingPower)
provide('currentInviteCode', currentInviteCode)

const setActiveIndexFromRoute = () => {
  const path = route.path
  switch (path) {
    case '/':
      activeIndex.value = '1'
      break
    case '/works':
      activeIndex.value = '2'
      break
    case '/order':
      activeIndex.value = '3'
      break
    default:
      if (path.startsWith('/project/')) {
        activeIndex.value = '2'
      } else {
        activeIndex.value = '1'
      }
  }
}

onMounted(() => {
  setActiveIndexFromRoute()
  const savedCode = localStorage.getItem('inviteCode')
  if (savedCode) {
    currentInviteCode.value = savedCode
    fetchUserPower(savedCode)
  }
})

const fetchUserPower = async (code) => {
  try {
    const response = await fetch(`/api/user/power?invite_code=${encodeURIComponent(code)}`)
    const result = await response.json()
    if (result.status === 'success') {
      computingPower.value = result.compute_power
      isLoggedIn.value = true
    }
  } catch (error) {
    console.error('Failed to fetch user power:', error)
  }
}

watch(
  () => route.path,
  () => {
    setActiveIndexFromRoute()
  }
)

const handleLogin = () => {
  showLoginModal.value = true
}

const handleLoginSubmit = (formData) => {
  console.log('登录表单数据:', formData)
  if (formData.computingPower !== undefined) {
    computingPower.value = formData.computingPower
    isLoggedIn.value = true
  }
  if (formData.inviteCode) {
    currentInviteCode.value = formData.inviteCode
    localStorage.setItem('inviteCode', formData.inviteCode)
  }
}

const handleLogout = () => {
  isLoggedIn.value = false
  computingPower.value = 0
  currentInviteCode.value = ''
  localStorage.removeItem('inviteCode')
  console.log('已退出登录')
}

const handleMenuSelect = (index) => {
  activeIndex.value = index
  switch (index) {
    case '1':
      router.push('/')
      break
    case '2':
      router.push('/works')
      break
    case '3':
      router.push('/order')
      break
    default:
      router.push('/')
  }
}
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  background-color: #1d1d1d;
  color: #ffffff;
  overflow: hidden;
}

.layout-sidebar {
  width: 200px;
  border-right: 1px solid #2a2a2a;
  background-color: #1d1d1d;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  height: 100%;
}

.sidebar-footer {
  padding: 16px;
  border-top: 1px solid #2a2a2a;
  margin-top: auto;
}

.footer-item {
  display: flex;
  align-items: center;
  padding: 8px 0;
  cursor: pointer;
  transition: all 0.3s ease;
}

.footer-item:hover {
  color: #a3e635;
}

.footer-item .el-icon {
  margin-right: 8px;
  font-size: 16px;
}

.footer-item .value {
  margin-left: auto;
  color: #a3e635;
  font-weight: bold;
}

.footer-login {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #2a2a2a;
}

.footer-login .login-btn {
  width: 100%;
  padding: 10px 16px;
  font-size: 14px;
  color: #1d1d1d;
  background-color: #a3e635;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.footer-login .login-btn:hover {
  background-color: #8bc34a;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(163, 230, 53, 0.3);
}

.footer-login .logout-text {
  width: 100%;
  text-align: center;
  padding: 10px 16px;
  font-size: 14px;
  color: #999;
  cursor: pointer;
  transition: all 0.3s ease;
}

.footer-login .logout-text:hover {
  color: #a3e635;
}

.layout-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.layout-main .layout-header {
  height: 60px;
  border-bottom: 1px solid #2a2a2a;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  background-color: #1d1d1d;
}

.header-nav {
  display: flex;
  gap: 24px;
}

.nav-item {
  color: #999;
  text-decoration: none;
  font-size: 14px;
  padding: 8px 0;
  position: relative;
  transition: all 0.3s ease;
}

.nav-item:hover {
  color: #a3e635;
}

.nav-item.active {
  color: #a3e635;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #a3e635;
}

.header-user {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-id {
  font-size: 14px;
  color: #999;
}

.layout-main .layout-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: #1d1d1d;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 自定义滚动条样式 */
.layout-content,
.layout-sidebar .flex-1 {
  /* 平滑滚动 */
  scroll-behavior: smooth;
  /* 隐藏滚动条但保留滚动功能 */
  /* Firefox */
  scrollbar-width: thin;
  scrollbar-color: #404040 #1d1d1d;
}

/* WebKit 浏览器 (Chrome, Safari) */
.layout-content::-webkit-scrollbar,
.layout-sidebar .flex-1::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

.layout-content::-webkit-scrollbar-track,
.layout-sidebar .flex-1::-webkit-scrollbar-track {
  background: #1d1d1d;
  border-radius: 4px;
}

.layout-content::-webkit-scrollbar-thumb,
.layout-sidebar .flex-1::-webkit-scrollbar-thumb {
  background: #404040;
  border-radius: 4px;
  transition: background 0.3s ease;
}

.layout-content::-webkit-scrollbar-thumb:hover,
.layout-sidebar .flex-1::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.layout-content::-webkit-scrollbar-thumb:active,
.layout-sidebar .flex-1::-webkit-scrollbar-thumb:active {
  background: #666;
}

/* 自定义Element Plus菜单样式 */
:deep(.el-menu) {
  background-color: transparent !important;
  border-right: none !important;
}

:deep(.el-menu-item) {
  height: 48px !important;
  line-height: 48px !important;
  margin: 0 16px !important;
  border-radius: 4px !important;
  transition: all 0.3s ease !important;
}

:deep(.el-menu-item:hover) {
  background-color: rgba(163, 230, 53, 0.1) !important;
  color: #a3e635 !important;
}

:deep(.el-menu-item.is-active) {
  background-color: rgba(163, 230, 53, 0.2) !important;
  color: #a3e635 !important;
}

:deep(.el-menu-item .el-icon) {
  margin-right: 12px !important;
}
</style>