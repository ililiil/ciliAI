<template>
  <div class="project-detail-page">
    <div class="page-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <div class="project-info">
          <h1 class="project-title">{{ project.title }}</h1>
          <span class="project-time">鍒涘缓浜?{{ project.createTime }}</span>
        </div>
      </div>
      <div class="header-right">
        <el-button type="primary" class="save-btn" @click="saveProject" :loading="isSaving">
          淇濆瓨椤圭洰
        </el-button>
      </div>
    </div>

    <div class="page-content">
      <div class="sidebar-tabs">
        <div 
          :class="['tab-item', { active: activeModule === 'chat' }]"
          @click="activeModule = 'chat'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
          </svg>
          <span>AI瀵硅瘽</span>
        </div>
        <div 
          :class="['tab-item', { active: activeModule === 'image' }]"
          @click="activeModule = 'image'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <circle cx="8.5" cy="8.5" r="1.5"></circle>
            <polyline points="21 15 16 10 5 21"></polyline>
          </svg>
          <span>AI鐢熷浘</span>
        </div>
        <div 
          :class="['tab-item', { active: activeModule === 'extend' }]"
          @click="activeModule = 'extend'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
            <line x1="8" y1="3" x2="8" y2="21"></line>
            <line x1="16" y1="3" x2="16" y2="21"></line>
            <line x1="3" y1="8" x2="21" y2="8"></line>
            <line x1="3" y1="16" x2="21" y2="16"></line>
          </svg>
          <span>AI鎵╁浘</span>
        </div>
        <div 
          :class="['tab-item', { active: activeModule === 'edit' }]"
          @click="activeModule = 'edit'"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
          </svg>
          <span>AI鏀瑰浘</span>
        </div>
      </div>

      <div class="main-content">
        <div v-if="activeModule === 'chat'" class="chat-module">
          <div class="chat-sidebar">
            <div class="sidebar-header">
              <h3>瀵硅瘽鍒楄〃</h3>
              <button class="new-chat-btn" @click="createNewChat">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
                鏂板璇?              </button>
            </div>
            <div class="chat-list">
              <div 
                v-for="chat in chatList" 
                :key="chat.id"
                :class="['chat-item', { active: currentChatId === chat.id }]"
                @click="selectChat(chat.id)"
              >
                <div class="chat-item-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
                <div class="chat-item-content">
                  <div class="chat-item-title">{{ chat.title }}</div>
                  <div class="chat-item-time">{{ chat.updateTime }}</div>
                </div>
                <div class="chat-item-actions">
                  <button class="action-btn" @click.stop="deleteChat(chat.id)">
                    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                      <polyline points="3 6 5 6 21 6"></polyline>
                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path>
                    </svg>
                  </button>
                </div>
              </div>
              <div v-if="chatList.length === 0" class="empty-chat-list">
                <p>鏆傛棤瀵硅瘽璁板綍</p>
                <p class="hint">鐐瑰嚮"鏂板璇?寮€濮?/p>
              </div>
            </div>
          </div>

          <div class="chat-main">
            <div class="chat-messages" ref="messagesContainer">
              <div v-if="currentMessages.length === 0" class="empty-messages">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>
                <p>寮€濮嬩笌AI瀵硅瘽</p>
                <p class="hint">杈撳叆鎮ㄧ殑闂锛孉I灏嗕负鎮ㄦ彁渚涘府鍔?/p>
              </div>
              <div 
                v-for="message in currentMessages" 
                :key="message.id"
                :class="['message', message.role]"
              >
                <div class="message-avatar">
                  <div v-if="message.role === 'user'" class="avatar user-avatar">U</div>
                  <div v-else class="avatar ai-avatar">AI</div>
                </div>
                <div class="message-content">
                  <div class="message-text">{{ message.content }}</div>
                  <div class="message-time">{{ message.time }}</div>
                  <div v-if="message.status === 'sending'" class="message-status">
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                    <span class="loading-dot"></span>
                  </div>
                  <div v-else-if="message.status === 'error'" class="message-status error">
                    鍙戦€佸け璐?                  </div>
                </div>
              </div>
            </div>

            <div class="chat-input-area">
              <div class="input-wrapper">
                <textarea 
                  v-model="inputMessage"
                  placeholder="杈撳叆娑堟伅..."
                  @keydown.enter.exact.prevent="sendMessage"
                  rows="1"
                  ref="inputTextarea"
                ></textarea>
                <button 
                  class="send-btn" 
                  @click="sendMessage"
                  :disabled="!inputMessage.trim() || isSending"
                >
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="22" y1="2" x2="11" y2="13"></line>
                    <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeModule === 'image'" class="image-module">
          <div class="image-sidebar">
            <div class="sidebar-header">
              <h3>鐢熷浘鍘嗗彶</h3>
            </div>
            <div class="image-history-list">
              <div 
                v-for="item in imageHistory" 
                :key="item.id"
                class="history-item"
                @click="viewHistoryItem(item)"
              >
                <div class="history-thumbnail">
                  <img :src="item.imageUrl" :alt="item.prompt" />
                </div>
                <div class="history-info">
                  <div class="history-prompt">{{ item.prompt }}</div>
                  <div class="history-time">{{ item.createTime }}</div>
                </div>
              </div>
              <div v-if="imageHistory.length === 0" class="empty-history">
                <p>鏆傛棤鐢熷浘璁板綍</p>
              </div>
            </div>
          </div>

          <div class="image-main">
            <div class="image-params-section">
              <h3 class="section-title">鐢熷浘鍙傛暟</h3>
              <div class="params-form">
                <div class="form-item">
                  <label>鎻愮ず璇?/label>
                  <el-input
                    v-model="imageParams.prompt"
                    type="textarea"
                    :rows="4"
                    placeholder="璇疯緭鍏ュ浘鐗囨弿杩帮紝濡傦細涓€涓編涓界殑鏃ヨ惤鍦烘櫙锛屾捣杈规湁妫曟鏍?.."
                  />
                </div>
                <div class="form-item">
                  <label>鍥剧墖灏哄</label>
                  <el-select v-model="imageParams.size" placeholder="閫夋嫨灏哄">
                    <el-option label="1024 x 1024 (1K)" value="1024x1024" />
                    <el-option label="2048 x 2048 (2K)" value="2048x2048" />
                    <el-option label="2304 x 1728 (4:3)" value="2304x1728" />
                    <el-option label="2560 x 1440 (16:9)" value="2560x1440" />
                    <el-option label="4096 x 4096 (4K)" value="4096x4096" />
                  </el-select>
                </div>
                <div class="form-item">
                  <label>鍙傝€冨浘锛堝彲閫夛級</label>
                  <el-upload
                    class="reference-upload"
                    action=""
                    :auto-upload="false"
                    :on-change="handleReferenceUpload"
                    :show-file-list="true"
                    :limit="1"
                    :file-list="referenceFileList"
                  >
                    <el-button size="small" type="primary">涓婁紶鍥剧墖</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        鏀寔JPEG銆丳NG鏍煎紡锛屾渶澶?5MB
                      </div>
                    </template>
                  </el-upload>
                </div>

                <el-button 
                  type="primary" 
                  class="generate-btn"
                  @click="generateImage"
                  :loading="isGenerating"
                >
                  {{ isGenerating ? '鐢熸垚涓?..' : '寮€濮嬬敓鎴? }}
                </el-button>
              </div>
            </div>

            <div class="image-result-section">
              <h3 class="section-title">鐢熸垚缁撴灉</h3>
              <div v-if="generatedImages.length === 0" class="empty-result">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <circle cx="8.5" cy="8.5" r="1.5"></circle>
                    <polyline points="21 15 16 10 5 21"></polyline>
                  </svg>
                </div>
                <p>鏆傛棤鐢熸垚缁撴灉</p>
                <p class="hint">璁剧疆鍙傛暟鍚庣偣鍑?寮€濮嬬敓鎴?</p>
              </div>
              <div v-else class="result-grid">
                <div 
                  v-for="(image, index) in generatedImages" 
                  :key="index"
                  class="result-item"
                >
                  <img :src="image.url" :alt="image.prompt" />
                  <div class="result-actions">
                    <button class="action-btn" @click="downloadImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                      </svg>
                    </button>
                    <button class="action-btn" @click="previewImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeModule === 'extend'" class="image-module">
          <div class="image-sidebar">
            <div class="sidebar-header">
              <h3>鎵╁浘鍘嗗彶</h3>
            </div>
            <div class="image-history-list">
              <div 
                v-for="item in extendHistory" 
                :key="item.id"
                class="history-item"
                @click="viewExtendHistoryItem(item)"
              >
                <div class="history-thumbnail">
                  <img :src="item.imageUrl" :alt="item.prompt" />
                </div>
                <div class="history-info">
                  <div class="history-prompt">{{ item.prompt }}</div>
                  <div class="history-time">{{ item.createTime }}</div>
                </div>
              </div>
              <div v-if="extendHistory.length === 0" class="empty-history">
                <p>鏆傛棤鎵╁浘璁板綍</p>
              </div>
            </div>
          </div>

          <div class="image-main">
            <div class="image-params-section">
              <h3 class="section-title">鎵╁浘鍙傛暟</h3>
              <div class="params-form">
                <div class="form-item">
                  <label>鐩爣鍥剧墖</label>
                  <el-upload
                    class="reference-upload"
                    action=""
                    :auto-upload="false"
                    :on-change="handleExtendImageUpload"
                    :show-file-list="true"
                    :limit="1"
                    :file-list="extendFileList"
                  >
                    <el-button size="small" type="primary">涓婁紶鍥剧墖</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        鏀寔JPEG銆丳NG鏍煎紡锛屾渶澶?5MB
                      </div>
                    </template>
                  </el-upload>
                </div>
                <div class="form-item">
                  <label>鎵╁睍鍚庡昂瀵?/label>
                  <el-select v-model="extendParams.size" placeholder="閫夋嫨灏哄">
                    <el-option label="2048 x 2048 (2K)" value="2048x2048" />
                    <el-option label="2304 x 1728 (4:3)" value="2304x1728" />
                    <el-option label="2560 x 1440 (16:9)" value="2560x1440" />
                    <el-option label="4096 x 4096 (4K)" value="4096x4096" />
                  </el-select>
                </div>
                <div class="form-item">
                  <label>鎻愮ず璇?/label>
                  <el-input
                    v-model="extendParams.prompt"
                    type="textarea"
                    :rows="2"
                    placeholder="璇锋弿杩版墿灞曞尯鍩熺殑鍐呭锛屽锛氬欢浼哥殑椋庢櫙锛屼繚鎸佷竴鑷寸殑椋庢牸..."
                  />
                </div>
                <el-button 
                  type="primary" 
                  class="generate-btn"
                  @click="extendImage"
                  :loading="isExtending"
                >
                  {{ isExtending ? '鎵╁睍涓?..' : '寮€濮嬫墿灞? }}
                </el-button>
              </div>
            </div>

            <div class="image-result-section">
              <h3 class="section-title">鎵╁睍缁撴灉</h3>
              <div v-if="extendedImages.length === 0" class="empty-result">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
                    <line x1="8" y1="3" x2="8" y2="21"></line>
                    <line x1="16" y1="3" x2="16" y2="21"></line>
                    <line x1="3" y1="8" x2="21" y2="8"></line>
                    <line x1="3" y1="16" x2="21" y2="16"></line>
                  </svg>
                </div>
                <p>鏆傛棤鎵╁睍缁撴灉</p>
                <p class="hint">涓婁紶鍥剧墖鍚庣偣鍑?寮€濮嬫墿灞?</p>
              </div>
              <div v-else class="result-grid">
                <div 
                  v-for="(image, index) in extendedImages" 
                  :key="index"
                  class="result-item"
                >
                  <img :src="image.url" :alt="image.prompt" />
                  <div class="result-actions">
                    <button class="action-btn" @click="downloadImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                      </svg>
                    </button>
                    <button class="action-btn" @click="previewImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div v-else-if="activeModule === 'edit'" class="image-module">
          <div class="image-sidebar">
            <div class="sidebar-header">
              <h3>鏀瑰浘鍘嗗彶</h3>
            </div>
            <div class="image-history-list">
              <div 
                v-for="item in editHistory" 
                :key="item.id"
                class="history-item"
                @click="viewEditHistoryItem(item)"
              >
                <div class="history-thumbnail">
                  <img :src="item.imageUrl" :alt="item.prompt" />
                </div>
                <div class="history-info">
                  <div class="history-prompt">{{ item.prompt }}</div>
                  <div class="history-time">{{ item.createTime }}</div>
                </div>
              </div>
              <div v-if="editHistory.length === 0" class="empty-history">
                <p>鏆傛棤鏀瑰浘璁板綍</p>
              </div>
            </div>
          </div>

          <div class="image-main">
            <div class="image-params-section">
              <h3 class="section-title">鏀瑰浘鍙傛暟</h3>
              <div class="params-form">
                <div class="form-item">
                  <label>鍘熷浘</label>
                  <el-upload
                    class="reference-upload"
                    action=""
                    :auto-upload="false"
                    :on-change="handleEditImageUpload"
                    :show-file-list="true"
                    :limit="1"
                    :file-list="editFileList"
                  >
                    <el-button size="small" type="primary">涓婁紶鍘熷浘</el-button>
                    <template #tip>
                      <div class="el-upload__tip">
                        鏀寔JPEG銆丳NG鏍煎紡锛屾渶澶?.7MB
                      </div>
                    </template>
                  </el-upload>
                </div>
                <div class="form-item">
                  <label>娑傛姽鍖哄煙</label>
                  <div class="image-editor" v-if="editParams.image">
                    <div class="editor-controls">
                      <el-button size="small" :class="{ active: editingTool === 'brush' }" @click="editingTool = 'brush'">鐢荤瑪</el-button>
                      <el-button size="small" :class="{ active: editingTool === 'eraser' }" @click="editingTool = 'eraser'">姗＄毊鎿?/el-button>
                      <el-button size="small" @click="clearMask">娓呯┖</el-button>
                    </div>
                    <div class="canvas-container">
                      <canvas ref="editCanvas" @mousedown="startDrawing" @mousemove="draw" @mouseup="stopDrawing" @mouseleave="stopDrawing"></canvas>
                      <img ref="editImageRef" :src="editParams.image" class="editor-image" />
                    </div>
                  </div>
                  <div class="no-image" v-else>
                    <p>璇峰厛涓婁紶鍘熷浘</p>
                  </div>
                </div>
                <div class="form-item">
                  <label>鎻愮ず璇?/label>
                  <el-input
                    v-model="editParams.prompt"
                    type="textarea"
                    :rows="3"
                    placeholder="璇锋弿杩颁慨鏀瑰唴瀹癸紝濡傦細鍒犻櫎鐗╀綋锛屾浛鎹㈡枃瀛椾负'鏂板唴瀹?..."
                  />
                </div>
                <el-button 
                  type="primary" 
                  class="generate-btn"
                  @click="generateEditImage"
                  :loading="isEditing"
                >
                  {{ isEditing ? '淇敼涓?..' : '寮€濮嬩慨鏀? }}
                </el-button>
              </div>
            </div>

            <div class="image-result-section">
              <h3 class="section-title">淇敼缁撴灉</h3>
              <div v-if="editedImages.length === 0" class="empty-result">
                <div class="empty-icon">
                  <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                    <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                  </svg>
                </div>
                <p>鏆傛棤淇敼缁撴灉</p>
                <p class="hint">涓婁紶鍥剧墖鍜孧ask鍥惧悗鐐瑰嚮"寮€濮嬩慨鏀?</p>
              </div>
              <div v-else class="result-grid">
                <div 
                  v-for="(image, index) in editedImages" 
                  :key="index"
                  class="result-item"
                >
                  <img :src="image.url" :alt="image.prompt" />
                  <div class="result-actions">
                    <button class="action-btn" @click="downloadImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                      </svg>
                    </button>
                    <button class="action-btn" @click="previewImage(image.url)">
                      <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                        <circle cx="12" cy="12" r="3"></circle>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog
      v-model="showImagePreview"
      width="80%"
      class="image-preview-dialog"
    >
      <img :src="previewImageUrl" class="preview-image" />
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch, inject } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { generateImage as volcGenerateImage, editImage as volcEditImage, extendImage as volcExtendImage, pollTaskResult } from '../utils/volcengine.js'

const route = useRoute()
const router = useRouter()

const currentInviteCode = inject('currentInviteCode', ref(''))

// Dify API 淇℃伅
const difyApiKey = 'app-l38yBomZ4wAiYktOqJ6kaXfp'
const difyApiUrl = '/dify-api/chat-messages'

// 鐏北寮曟搸璁よ瘉淇℃伅 - 浠庣幆澧冨彉閲忚鍙?// 瀹為檯瀵嗛挜瀛樺偍鍦?.env 鏂囦欢涓紝涓嶅簲鍦ㄤ唬鐮佷腑纭紪鐮?
const activeModule = ref('chat')
const isSaving = ref(false)
const isSending = ref(false)
const isGenerating = ref(false)

const project = ref({
  id: '',
  title: '鍔犺浇涓?..',
  createTime: ''
})

const chatList = ref([])
const currentChatId = ref('')
const inputMessage = ref('')
const messagesContainer = ref(null)
const inputTextarea = ref(null)

const currentMessages = computed(() => {
  const chat = chatList.value.find(c => c.id === currentChatId.value)
  return chat ? chat.messages : []
})

const imageParams = reactive({
  prompt: '',
  size: '1024x1024',
  referenceImage: ''
})

const extendParams = reactive({
  image: '',
  size: '2048x2048',
  prompt: ''
})

const editParams = reactive({
  image: '',
  mask: '',
  prompt: ''
})

const editingTool = ref('brush')
const isDrawing = ref(false)
const editCanvas = ref(null)
const editImageRef = ref(null)
const canvasContext = ref(null)

const imageHistory = ref([])
const extendHistory = ref([])
const editHistory = ref([])
const generatedImages = ref([])
const extendedImages = ref([])
const editedImages = ref([])
const showImagePreview = ref(false)
const previewImageUrl = ref('')
const referenceFileList = ref([])
const extendFileList = ref([])
const editFileList = ref([])
const maskFileList = ref([])
const isExtending = ref(false)
const isEditing = ref(false)

const loadProjectData = async () => {
  const projectId = route.params.id
  
  project.value = {
    id: projectId,
    title: '绀轰緥椤圭洰锛岄緳鏃?,
    createTime: '2025-03-31 13:24:07'
  }
  
  chatList.value = [
    {
      id: Date.now().toString(),
      title: '鏂板璇?,
      updateTime: new Date().toLocaleString('zh-CN'),
      conversationId: '',
      messages: []
    }
  ]
  
  if (chatList.value.length > 0) {
    currentChatId.value = chatList.value[0].id
  }
  
  imageHistory.value = [
    {
      id: '1',
      prompt: '涓€涓湭鏉ュ煄甯傜殑澶滄櫙锛岄湏铏圭伅闂儊',
      imageUrl: 'https://picsum.photos/400/300?random=100',
      createTime: '2025-03-31 13:00',
      params: { size: '1024x1024', steps: 30, cfgScale: 7 }
    },
    {
      id: '2',
      prompt: '鍙や唬瀹锛岄噾纰ц緣鐓?,
      imageUrl: 'https://picsum.photos/400/300?random=101',
      createTime: '2025-03-31 11:30',
      params: { size: '1024x1024', steps: 25, cfgScale: 8 }
    }
  ]
}

const goBack = () => {
  router.push('/works')
}

const saveProject = async () => {
  isSaving.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('椤圭洰淇濆瓨鎴愬姛')
  } catch (error) {
    ElMessage.error('淇濆瓨澶辫触锛岃閲嶈瘯')
  } finally {
    isSaving.value = false
  }
}

const createNewChat = () => {
  const newChat = {
    id: Date.now().toString(),
    title: '鏂板璇?,
    updateTime: new Date().toLocaleString('zh-CN'),
    messages: [],
    conversationId: ''
  }
  chatList.value.unshift(newChat)
  currentChatId.value = newChat.id
  inputMessage.value = ''
}

const selectChat = (chatId) => {
  currentChatId.value = chatId
  scrollToBottom()
}

const deleteChat = async (chatId) => {
  try {
    await ElMessageBox.confirm('纭畾瑕佸垹闄よ繖涓璇濆悧锛?, '鎻愮ず', {
      confirmButtonText: '纭畾',
      cancelButtonText: '鍙栨秷',
      type: 'warning'
    })
    const index = chatList.value.findIndex(c => c.id === chatId)
    if (index > -1) {
      chatList.value.splice(index, 1)
      if (currentChatId.value === chatId) {
        currentChatId.value = chatList.value.length > 0 ? chatList.value[0].id : ''
      }
    }
    ElMessage.success('鍒犻櫎鎴愬姛')
  } catch {
    // 鐢ㄦ埛鍙栨秷
  }
}

const sendMessage = async () => {
  if (!inputMessage.value.trim() || isSending.value) return
  
  const message = inputMessage.value.trim()
  inputMessage.value = ''
  
  const currentChat = chatList.value.find(c => c.id === currentChatId.value)
  if (!currentChat) {
    createNewChat()
  }
  
  const userMessage = {
    id: Date.now().toString(),
    role: 'user',
    content: message,
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    status: 'success'
  }
  
  const chat = chatList.value.find(c => c.id === currentChatId.value)
  if (chat) {
    chat.messages.push(userMessage)
    chat.title = message.slice(0, 20) + (message.length > 20 ? '...' : '')
    chat.updateTime = new Date().toLocaleString('zh-CN')
  }
  
  scrollToBottom()
  
  isSending.value = true
  
  const aiMessageId = (Date.now() + 1).toString()
  const aiMessage = {
    id: aiMessageId,
    role: 'assistant',
    content: '',
    time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' }),
    status: 'sending'
  }
  
  if (chat) {
    chat.messages.push(aiMessage)
  }
  
  scrollToBottom()
  
  try {
    const { answer, conversationId } = await callDifyAPI(
      message,
      chat.conversationId || '',
      (chunk) => {
        const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
        if (msgIndex > -1) {
          chat.messages[msgIndex].content += chunk
        }
        scrollToBottom()
      }
    )
    
    if (conversationId && chat) {
      chat.conversationId = conversationId
    }
    
    const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
    if (msgIndex > -1) {
      chat.messages[msgIndex].status = 'success'
    }
  } catch (error) {
    console.error('鍙戦€佹秷鎭け璐?', error)
    const msgIndex = chat.messages.findIndex(m => m.id === aiMessageId)
    if (msgIndex > -1) {
      chat.messages[msgIndex].content = '鎶辨瓑锛孉PI 璋冪敤澶辫触锛岃绋嶅悗閲嶈瘯: ' + error.message
      chat.messages[msgIndex].status = 'error'
    }
  } finally {
    isSending.value = false
    scrollToBottom()
  }
}

const callDifyAPI = async (query, conversationId, onChunk) => {
  const requestBody = {
    inputs: {},
    query: query,
    response_mode: 'streaming',
    user: 'user-' + Date.now()
  }
  
  if (conversationId) {
    requestBody.conversation_id = conversationId
  }

  const response = await fetch(difyApiUrl, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${difyApiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(requestBody)
  })

  if (!response.ok) {
    throw new Error(`API璇锋眰澶辫触: ${response.status}`)
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let result = ''
  let newConversationId = conversationId

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    const chunk = decoder.decode(value, { stream: true })
    const lines = chunk.split('\n')

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const dataStr = line.slice(6)
        if (dataStr && dataStr !== '[DONE]') {
          try {
            const data = JSON.parse(dataStr)
            
            if (data.event === 'message' || data.event === 'agent_message') {
              result += data.answer || ''
              if (onChunk) {
                onChunk(data.answer || '')
              }
            }
            
            if (data.conversation_id) {
              newConversationId = data.conversation_id
            }
            
            if (data.event === 'message_end') {
              return { answer: result, conversationId: newConversationId }
            }
            
            if (data.event === 'error') {
              throw new Error(data.message || 'API杩斿洖閿欒')
            }
          } catch (e) {
            if (e.message !== 'Unexpected end of JSON input') {
              console.error('瑙ｆ瀽鍝嶅簲鏁版嵁澶辫触:', e)
            }
          }
        }
      }
    }
  }

  return { answer: result, conversationId: newConversationId }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

const handleReferenceUpload = (file) => {
  // 杩欓噷鍙槸鍓嶇棰勮锛屽疄闄呬笂浼犻渶瑕佸悗绔鐞?  const reader = new FileReader()
  reader.onload = (e) => {
    imageParams.referenceImage = e.target.result
    referenceFileList.value = [file]
  }
  reader.readAsDataURL(file.raw)
}

const generateImage = async () => {
  if (!imageParams.prompt.trim()) {
    ElMessage.warning('璇疯緭鍏ユ彁绀鸿瘝')
    return
  }
  
  isGenerating.value = true
  generatedImages.value = []
  
  try {
    const [width, height] = imageParams.size.split('x').map(Number)
    
    // 鏋勫缓璇锋眰鍙傛暟
    const params = {
      prompt: imageParams.prompt,
      width: width,
      height: height,
      force_single: true // 寮哄埗鐢熸垚鍗曞浘锛屽噺灏戠敓鎴愭椂闂?    }
    
    // 濡傛灉鏈夊弬鑰冨浘锛屾坊鍔犲埌璇锋眰鍙傛暟涓?    if (imageParams.referenceImage) {
      params.referenceImage = imageParams.referenceImage
    }
    
    console.log('寮€濮嬭皟鐢ㄧ敓鍥続PI锛屽弬鏁?', params)
    
    if (!currentInviteCode.value) {
      ElMessage.error('璇峰厛鐧诲綍')
      isGenerating.value = false
      return
    }
    
    // 璋冪敤鍚庣API
    const submitResponse = await volcGenerateImage(params, accessKeyId, secretAccessKey, currentInviteCode.value, project.value.id)
    
    console.log('鐢熷浘浠诲姟鍝嶅簲:', submitResponse)
    
    if (!submitResponse.data?.task_id) {
      throw new Error('浠诲姟鎻愪氦澶辫触锛屾湭杩斿洖task_id')
    }
    
    const taskId = submitResponse.data.task_id
    
    // 澶勭悊浠诲姟缁撴灉
    const newImages = []
    // 浠嶢PI鍝嶅簲涓幏鍙栫敓鎴愮殑鍥剧墖URL
    console.log('API杩斿洖鐨刬mages鏁版嵁:', submitResponse.data?.images)
    
    if (submitResponse.data?.images && submitResponse.data.images.length > 0) {
      // 浣跨敤鐪熷疄鐨凙PI杩斿洖鐨勫浘鐗嘦RL
      submitResponse.data.images.forEach((image, index) => {
        console.log('澶勭悊鍥剧墖鏁版嵁:', index, image)
        
        // 纭繚image鏄竴涓璞′笖鏈塽rl灞炴€?        if (typeof image === 'object' && image.url) {
          newImages.push({
            url: image.url,
            prompt: imageParams.prompt,
            taskId: taskId
          })
        } else if (typeof image === 'string') {
          // 濡傛灉image鏄瓧绗︿覆锛岀洿鎺ヤ綔涓簎rl
          newImages.push({
            url: image,
            prompt: imageParams.prompt,
            taskId: taskId
          })
        }
      })
    } else {
      // 娌℃湁杩斿洖鍥剧墖锛屾姏鍑洪敊璇?      throw new Error('API杩斿洖缁撴灉涓病鏈夊浘鐗囨暟鎹?)
    }
    
    console.log('澶勭悊鍚庣殑newImages:', newImages)
    
    generatedImages.value = newImages
    
    const historyItem = {
      id: Date.now().toString(),
      prompt: imageParams.prompt,
      imageUrl: newImages[0].url,
      createTime: new Date().toLocaleString('zh-CN'),
      params: {
        size: imageParams.size,
        hasReference: !!imageParams.referenceImage,
        taskId: taskId
      }
    }
    imageHistory.value.unshift(historyItem)
    
    ElMessage.success('鍥剧墖鐢熸垚鎴愬姛')
  } catch (error) {
    console.error('鐢熷浘澶辫触:', error)
    ElMessage.error(`鐢熸垚澶辫触: ${error.message}`)
    
    // 鏄剧ず璇︾粏鐨勯敊璇俊鎭紝甯姪璋冭瘯
    console.error('璇︾粏閿欒淇℃伅:', error)
    
    // 妫€鏌ユ槸鍚︽槸缃戠粶閿欒
    if (error.message.includes('Failed to fetch')) {
      ElMessage.error('缃戠粶璇锋眰澶辫触锛岃妫€鏌ョ綉缁滆繛鎺ユ垨鍚庣鏈嶅姟鍣ㄦ槸鍚﹁繍琛?)
    }
  } finally {
    isGenerating.value = false
  }
}

const viewHistoryItem = (item) => {
  imageParams.prompt = item.prompt
  imageParams.size = item.params?.size || '2048x2048'
  imageParams.referenceImage = ''
  referenceFileList.value = []
  
  generatedImages.value = [{
    url: item.imageUrl,
    prompt: item.prompt
  }]
}

const handleExtendImageUpload = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    extendParams.image = e.target.result
    extendFileList.value = [file]
  }
  reader.readAsDataURL(file.raw)
}

const extendImage = async () => {
  if (!extendParams.image) {
    ElMessage.warning('璇蜂笂浼犵洰鏍囧浘鐗?)
    return
  }
  
  isExtending.value = true
  extendedImages.value = []
  
  try {
    const [width, height] = extendParams.size.split('x').map(Number)
    
    // 璋冪敤鐪熷疄鐨勬墿鍥続PI
    const params = {
      image: extendParams.image,
      prompt: extendParams.prompt || '鎵╁睍鍥惧儚锛屼繚鎸佸師鏈夐鏍?,
      width: width,
      height: height
    }
    
    if (!currentInviteCode.value) {
      ElMessage.error('璇峰厛鐧诲綍')
      isExtending.value = false
      return
    }
    
    const response = await volcExtendImage(params, accessKeyId, secretAccessKey, currentInviteCode.value, project.value.id)
    
    console.log('鎵╁浘浠诲姟鍝嶅簲:', response)
    
    if (!response.data?.task_id) {
      throw new Error('浠诲姟鎻愪氦澶辫触锛屾湭杩斿洖task_id')
    }
    
    const taskId = response.data.task_id
    
    const newImages = []
    if (response.data?.images && response.data.images.length > 0) {
      response.data.images.forEach((image) => {
        if (typeof image === 'object' && image.url) {
          newImages.push({
            url: image.url,
            prompt: extendParams.prompt,
            taskId: taskId
          })
        } else if (typeof image === 'string') {
          newImages.push({
            url: image,
            prompt: extendParams.prompt,
            taskId: taskId
          })
        }
      })
    } else {
      throw new Error('API杩斿洖缁撴灉涓病鏈夊浘鐗囨暟鎹?)
    }
    
    extendedImages.value = newImages
    
    const historyItem = {
      id: Date.now().toString(),
      prompt: extendParams.prompt,
      imageUrl: newImages[0].url,
      createTime: new Date().toLocaleString('zh-CN'),
      params: {
        size: extendParams.size,
        taskId: taskId
      }
    }
    extendHistory.value.unshift(historyItem)
    
    ElMessage.success('鍥剧墖鎵╁睍鎴愬姛')
  } catch (error) {
    console.error('鎵╁浘澶辫触:', error)
    ElMessage.error(`鎵╁睍澶辫触: ${error.message}`)
  } finally {
    isExtending.value = false
  }
}

const viewExtendHistoryItem = (item) => {
  extendParams.prompt = item.prompt
  extendParams.size = item.params?.size || '2048x2048'
  extendParams.image = ''
  extendFileList.value = []
  
  extendedImages.value = [{
    url: item.imageUrl,
    prompt: item.prompt
  }]
}

const handleEditImageUpload = (file) => {
  const reader = new FileReader()
  reader.onload = (e) => {
    editParams.image = e.target.result
    editFileList.value = [file]
    
    // 寤惰繜鍒濆鍖栫敾甯冿紝纭繚鍥剧墖鍔犺浇瀹屾垚
    setTimeout(() => {
      initCanvas()
    }, 100)
  }
  reader.readAsDataURL(file.raw)
}

const initCanvas = () => {
  if (!editCanvas.value || !editImageRef.value) return
  
  const canvas = editCanvas.value
  const image = editImageRef.value
  
  // 璁剧疆鐢诲竷灏哄涓庡浘鐗囦竴鑷?  canvas.width = image.width
  canvas.height = image.height
  
  // 鑾峰彇鐢诲竷涓婁笅鏂?  canvasContext.value = canvas.getContext('2d')
  
  // 娓呯┖鐢诲竷
  clearMask()
}

const startDrawing = (e) => {
  isDrawing.value = true
  draw(e)
}

const draw = (e) => {
  if (!isDrawing.value || !canvasContext.value || !editCanvas.value) return
  
  const canvas = editCanvas.value
  const rect = canvas.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  
  const ctx = canvasContext.value
  ctx.lineWidth = 20
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  
  if (editingTool.value === 'brush') {
    ctx.globalCompositeOperation = 'source-over'
    ctx.fillStyle = 'white'
  } else {
    ctx.globalCompositeOperation = 'destination-out'
    ctx.fillStyle = 'black'
  }
  
  ctx.beginPath()
  ctx.arc(x, y, 10, 0, Math.PI * 2)
  ctx.fill()
  
  // 鏇存柊mask鏁版嵁
  updateMask()
}

const stopDrawing = () => {
  isDrawing.value = false
}

const clearMask = () => {
  if (!canvasContext.value || !editCanvas.value) return
  
  const canvas = editCanvas.value
  const ctx = canvasContext.value
  
  // 娓呯┖鐢诲竷
  ctx.clearRect(0, 0, canvas.width, canvas.height)
  
  // 閲嶇疆mask鏁版嵁
  editParams.mask = ''
}

const updateMask = () => {
  if (!editCanvas.value) return
  
  // 灏嗙敾甯冨唴瀹硅浆鎹负base64缂栫爜
  editParams.mask = editCanvas.value.toDataURL('image/png')
}

const generateEditImage = async () => {
  if (!editParams.image) {
    ElMessage.warning('璇蜂笂浼犲師鍥?)
    return
  }
  if (!editParams.mask) {
    ElMessage.warning('璇峰湪鍘熷浘涓婄粯鍒朵慨鏀瑰尯鍩?)
    return
  }
  
  isEditing.value = true
  editedImages.value = []
  
  try {
    // 鏋勫缓璇锋眰鍙傛暟
    const params = {
      image: editParams.image,
      mask: editParams.mask,
      prompt: editParams.prompt
    }
    
    if (!currentInviteCode.value) {
      ElMessage.error('璇峰厛鐧诲綍')
      isEditing.value = false
      return
    }
    
    // 璋冪敤鐏北寮曟搸API鎻愪氦浠诲姟
    const submitResponse = await volcEditImage(params, accessKeyId, secretAccessKey, currentInviteCode.value, project.value.id)
    
    console.log('鏀瑰浘浠诲姟鎻愪氦鍝嶅簲:', submitResponse)
    
    if (!submitResponse.data?.task_id) {
      throw new Error('浠诲姟鎻愪氦澶辫触锛屾湭杩斿洖task_id')
    }
    
    const taskId = submitResponse.data.task_id
    ElMessage.success(`鍥剧墖淇敼浠诲姟宸叉彁浜わ紝浠诲姟ID: ${taskId}`)
    
    // 杞浠诲姟缁撴灉
    console.log('寮€濮嬭疆璇换鍔＄粨鏋?..')
    const resultResponse = await pollTaskResult(taskId, accessKeyId, secretAccessKey)
    
    console.log('鏀瑰浘浠诲姟缁撴灉:', resultResponse)
    
    // 澶勭悊浠诲姟缁撴灉
    const newImages = []
    // 瀹為檯搴旂敤涓紝闇€瑕佷粠resultResponse.data涓幏鍙栫敓鎴愮殑鍥剧墖URL
    // 杩欓噷浣跨敤妯℃嫙鏁版嵁
    newImages.push({
      url: `https://picsum.photos/512/512?random=${Date.now()}`,
      prompt: editParams.prompt,
      taskId: taskId
    })
    
    editedImages.value = newImages
    
    const historyItem = {
      id: Date.now().toString(),
      prompt: editParams.prompt,
      imageUrl: newImages[0].url,
      createTime: new Date().toLocaleString('zh-CN'),
      params: {
        hasMask: true,
        taskId: taskId
      }
    }
    editHistory.value.unshift(historyItem)
    
    ElMessage.success('鍥剧墖淇敼鎴愬姛')
  } catch (error) {
    console.error('鏀瑰浘澶辫触:', error)
    ElMessage.error(`淇敼澶辫触: ${error.message}`)
  } finally {
    isEditing.value = false
  }
}

const viewEditHistoryItem = (item) => {
  editParams.prompt = item.prompt
  editParams.image = ''
  editParams.mask = ''
  editFileList.value = []
  maskFileList.value = []
  
  editedImages.value = [{
    url: item.imageUrl,
    prompt: item.prompt
  }]
}

const downloadImage = (url) => {
  const link = document.createElement('a')
  link.href = url
  link.download = `ai-image-${Date.now()}.png`
  link.click()
  ElMessage.success('寮€濮嬩笅杞?)
}

const previewImage = (url) => {
  previewImageUrl.value = url
  showImagePreview.value = true
}

onMounted(() => {
  loadProjectData()
})
</script>

<style scoped>
.project-detail-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #1d1d1d;
  color: #ffffff;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  border-bottom: 1px solid #2a2a2a;
  background-color: #1d1d1d;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.back-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: #2a2a2a;
  border: none;
  color: #fff;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.back-btn:hover {
  background-color: #3a3a3a;
}

.project-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.project-title {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
  color: #fff;
}

.project-time {
  font-size: 12px;
  color: #666;
}

.save-btn {
  background-color: #a3e635;
  border-color: #a3e635;
  color: #1d1d1d;
  font-weight: 500;
}

.save-btn:hover {
  background-color: #8bc34a;
  border-color: #8bc34a;
}

.page-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.sidebar-tabs {
  width: 120px;
  background-color: #1a1a1a;
  border-right: 1px solid #2a2a2a;
  display: flex;
  flex-direction: column;
  padding: 16px 8px;
  gap: 8px;
}

.tab-item {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 12px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #666;
  gap: 8px;
}

.tab-item:hover {
  background-color: #2a2a2a;
  color: #999;
}

.tab-item.active {
  background-color: rgba(163, 230, 53, 0.2);
  color: #a3e635;
}

.tab-item span {
  font-size: 10px;
}

.main-content {
  flex: 1;
  overflow: hidden;
}

.chat-module {
  display: flex;
  height: 100%;
}

.chat-sidebar {
  width: 260px;
  background-color: #1a1a1a;
  border-right: 1px solid #2a2a2a;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #2a2a2a;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 500;
  color: #fff;
}

.new-chat-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 6px 12px;
  background-color: #a3e635;
  border: none;
  border-radius: 6px;
  color: #1d1d1d;
  font-size: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.new-chat-btn:hover {
  background-color: #8bc34a;
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.chat-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  gap: 12px;
}

.chat-item:hover {
  background-color: #2a2a2a;
}

.chat-item.active {
  background-color: rgba(163, 230, 53, 0.1);
}

.chat-item-icon {
  color: #666;
}

.chat-item.active .chat-item-icon {
  color: #a3e635;
}

.chat-item-content {
  flex: 1;
  min-width: 0;
}

.chat-item-title {
  font-size: 13px;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-item-time {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}

.chat-item-actions {
  opacity: 0;
  transition: opacity 0.3s ease;
}

.chat-item:hover .chat-item-actions {
  opacity: 1;
}

.action-btn {
  width: 28px;
  height: 28px;
  border-radius: 4px;
  background-color: transparent;
  border: none;
  color: #666;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.action-btn:hover {
  background-color: #3a3a3a;
  color: #fff;
}

.empty-chat-list {
  text-align: center;
  padding: 40px 16px;
  color: #666;
}

.empty-chat-list .hint {
  font-size: 12px;
  margin-top: 8px;
  color: #444;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #1d1d1d;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 24px;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #666;
}

.empty-icon {
  margin-bottom: 16px;
  color: #444;
}

.empty-messages .hint {
  font-size: 13px;
  margin-top: 8px;
  color: #444;
}

.message {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  flex-shrink: 0;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 600;
}

.user-avatar {
  background-color: #a3e635;
  color: #1d1d1d;
}

.ai-avatar {
  background-color: #3a3a3a;
  color: #a3e635;
}

.message-content {
  max-width: 70%;
}

.message.user .message-content {
  align-items: flex-end;
}

.message-text {
  padding: 12px 16px;
  border-radius: 12px;
  font-size: 14px;
  line-height: 1.6;
  white-space: pre-wrap;
}

.message.user .message-text {
  background-color: #a3e635;
  color: #1d1d1d;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-text {
  background-color: #2a2a2a;
  color: #fff;
  border-bottom-left-radius: 4px;
}

.message-time {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}

.message.user .message-time {
  text-align: right;
}

.message-status {
  margin-top: 4px;
  font-size: 12px;
}

.message-status.error {
  color: #f56c6c;
}

.loading-dot {
  display: inline-block;
  width: 6px;
  height: 6px;
  background-color: #a3e635;
  border-radius: 50%;
  margin-right: 4px;
  animation: loading 1s infinite;
}

.loading-dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes loading {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.chat-input-area {
  padding: 16px 24px;
  border-top: 1px solid #2a2a2a;
  background-color: #1a1a1a;
}

.input-wrapper {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 12px 16px;
}

.input-wrapper textarea {
  flex: 1;
  background: transparent;
  border: none;
  color: #fff;
  font-size: 14px;
  resize: none;
  outline: none;
  max-height: 120px;
  line-height: 1.5;
}

.input-wrapper textarea::placeholder {
  color: #666;
}

.send-btn {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background-color: #a3e635;
  border: none;
  color: #1d1d1d;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  background-color: #8bc34a;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.image-module {
  display: flex;
  height: 100%;
}

.image-sidebar {
  width: 260px;
  background-color: #1a1a1a;
  border-right: 1px solid #2a2a2a;
  display: flex;
  flex-direction: column;
}

.image-history-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.history-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.history-item:hover {
  background-color: #2a2a2a;
}

.history-thumbnail {
  width: 60px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
  flex-shrink: 0;
}

.history-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.history-info {
  flex: 1;
  min-width: 0;
}

.history-prompt {
  font-size: 12px;
  color: #fff;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 11px;
  color: #666;
  margin-top: 4px;
}

.empty-history {
  text-align: center;
  padding: 40px 16px;
  color: #666;
}

.image-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 24px;
  gap: 24px;
}

.image-params-section,
.image-result-section {
  background-color: #2a2a2a;
  border-radius: 12px;
  padding: 20px;
}

.section-title {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 500;
  color: #a3e635;
}

.params-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form-item label {
  font-size: 13px;
  color: #999;
}

.form-row {
  display: flex;
  gap: 16px;
}

.form-row .form-item {
  flex: 1;
}

.params-form :deep(.el-input__wrapper),
.params-form :deep(.el-textarea__inner),
.params-form :deep(.el-select .el-input__wrapper) {
  background-color: #1d1d1d;
  border: 1px solid #3a3a3a;
  box-shadow: none;
}

.params-form :deep(.el-input__inner),
.params-form :deep(.el-textarea__inner) {
  color: #fff;
}

.params-form :deep(.el-input__inner::placeholder),
.params-form :deep(.el-textarea__inner::placeholder) {
  color: #666;
}

.params-form :deep(.el-upload-list__item) {
  background-color: #1d1d1d;
  border: 1px solid #3a3a3a;
}

.params-form :deep(.el-upload-list__item-name) {
  color: #999;
}

.params-form :deep(.el-upload__tip) {
  color: #666;
  font-size: 12px;
  margin-top: 4px;
}

.image-editor {
  margin-top: 8px;
}

.editor-controls {
  display: flex;
  gap: 8px;
  margin-bottom: 8px;
}

.editor-controls .el-button.active {
  background-color: #a3e635;
  border-color: #a3e635;
  color: #1d1d1d;
}

.canvas-container {
  position: relative;
  max-width: 100%;
  border: 1px solid #3a3a3a;
  border-radius: 8px;
  overflow: hidden;
}

.canvas-container canvas {
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;
  cursor: crosshair;
}

.editor-image {
  display: block;
  max-width: 100%;
  height: auto;
  z-index: 0;
}

.no-image {
  border: 1px dashed #3a3a3a;
  border-radius: 8px;
  padding: 40px 20px;
  text-align: center;
  color: #666;
  margin-top: 8px;
}

.generate-btn {
  background-color: #a3e635;
  border-color: #a3e635;
  color: #1d1d1d;
  font-weight: 500;
  margin-top: 8px;
}

.generate-btn:hover {
  background-color: #8bc34a;
  border-color: #8bc34a;
}

.empty-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #666;
}

.empty-result .empty-icon {
  margin-bottom: 16px;
  color: #444;
}

.empty-result .hint {
  font-size: 13px;
  margin-top: 8px;
  color: #444;
}

.result-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.result-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  aspect-ratio: 1;
}

.result-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.result-actions {
  position: absolute;
  bottom: 8px;
  right: 8px;
  display: flex;
  gap: 8px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.result-item:hover .result-actions {
  opacity: 1;
}

.result-actions .action-btn {
  background-color: rgba(0, 0, 0, 0.6);
  color: #fff;
}

.result-actions .action-btn:hover {
  background-color: rgba(0, 0, 0, 0.8);
}





.image-preview-dialog :deep(.el-dialog) {
  background-color: #1d1d1d;
}

.preview-image {
  width: 100%;
  max-height: 80vh;
  object-fit: contain;
}

@media (max-width: 1024px) {
  .chat-sidebar,
  .image-sidebar {
    width: 220px;
  }
}

@media (max-width: 768px) {
  .page-header {
    padding: 12px 16px;
  }

  .sidebar-tabs {
    width: 100px;
  }
  
  .tab-item {
    gap: 6px;
  }
  
  .tab-item span {
    font-size: 9px;
  }

  .chat-sidebar,
  .image-sidebar {
    display: none;
  }

  .chat-messages {
    padding: 16px;
  }

  .chat-input-area {
    padding: 12px 16px;
  }

  .message-content {
    max-width: 85%;
  }

  .image-main {
    padding: 16px;
  }

  .form-row {
    flex-direction: column;
  }
}
</style>
