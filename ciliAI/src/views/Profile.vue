<template>
  <div class="profile-container">
    <h1>个人中心</h1>
    <el-card class="profile-card">
      <template #header>
        <div class="card-header">
          <span>个人信息</span>
        </div>
      </template>
      <div class="profile-info">
        <div class="avatar-section">
          <el-avatar :size="120">
            {{ userInfo.username.charAt(0).toUpperCase() }}
          </el-avatar>
          <h2>{{ userInfo.username }}</h2>
          <p class="user-id">ID: {{ userInfo.id }}</p>
          <div class="computing-power">
            <h3>算力余额</h3>
            <p class="power-amount">{{ userInfo.computingPower.toLocaleString() }}</p>
          </div>
        </div>
        <div class="info-section">
          <el-form :model="userInfo" label-width="100px">
            <el-form-item label="用户名">
              <el-input v-model="userInfo.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="邮箱">
              <el-input v-model="userInfo.email" placeholder="请输入邮箱"></el-input>
            </el-form-item>
            <el-form-item label="手机号">
              <el-input v-model="userInfo.phone" placeholder="请输入手机号"></el-input>
            </el-form-item>
            <el-form-item label="简介">
              <el-input
                v-model="userInfo.bio"
                type="textarea"
                placeholder="请输入个人简介"
                :rows="3"
              ></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveProfile">保存修改</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </el-card>
    <el-card class="security-card">
      <template #header>
        <div class="card-header">
          <span>账号安全</span>
        </div>
      </template>
      <div class="security-info">
        <el-table :data="securityItems" style="width: 100%">
          <el-table-column prop="item" label="安全项" width="180"></el-table-column>
          <el-table-column prop="status" label="状态" width="120">
            <template #default="scope">
              <el-tag :type="scope.row.status === '已设置' ? 'success' : 'warning'">
                {{ scope.row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120">
            <template #default="scope">
              <el-button size="small" type="primary" @click="handleSecurity(scope.row.item)">
                {{ scope.row.status === '已设置' ? '修改' : '设置' }}
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const userInfo = ref({
  id: 'USER10001',
  username: '创作者001',
  email: 'creator@example.com',
  phone: '138****8888',
  bio: '专业AI短剧创作者，擅长现代都市题材',
  computingPower: 0, // 默认算力为0，登录后会更新
  avatar: ''
})

const securityItems = ref([
  {
    item: '登录密码',
    status: '已设置'
  },
  {
    item: '支付密码',
    status: '已设置'
  },
  {
    item: '手机验证',
    status: '已设置'
  },
  {
    item: '邮箱验证',
    status: '未设置'
  }
])

const saveProfile = () => {
  console.log('保存个人信息', userInfo.value)
  // 保存个人信息逻辑
}

const handleSecurity = (item) => {
  console.log('处理安全项', item)
  // 处理安全项逻辑
}
</script>

<style scoped>
.profile-container {
  padding: 20px;
}

.profile-card,
.security-card {
  margin-bottom: 30px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.profile-info {
  display: flex;
  gap: 40px;
}

.avatar-section {
  flex-shrink: 0;
  text-align: center;
}

.avatar-section h2 {
  margin: 10px 0 5px 0;
  font-size: 18px;
}

.user-id {
  margin: 0;
  font-size: 14px;
  color: #999;
}

.computing-power {
  margin-top: 15px;
  padding: 15px;
  background-color: #BACACB;
  border-radius: 8px;
  text-align: center;
}

.computing-power h3 {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #425D5F;
}

.power-amount {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
  color: #425D5F;
}

.info-section {
  flex: 1;
}

.security-info {
  margin-top: 20px;
}
</style>