<template>
  <div class="min-h-screen bg-gray-50">
    <div class="max-w-4xl mx-auto h-screen flex flex-col">
      <!-- Header -->
      <header class="bg-white shadow-sm border-b border-gray-200 px-6 py-4">
        <div class="flex items-center justify-between">
          <h1 class="text-2xl font-bold text-gray-800">🔍 Screenshot Search</h1>
          <div class="text-sm text-gray-500">
            {{ totalScreenshots }} screenshots indexed
          </div>
        </div>
      </header>

      <!-- Chat Messages -->
      <div ref="messagesContainer" class="flex-1 overflow-y-auto px-6 py-4 space-y-4">
        <div v-if="messages.length === 0" class="text-center text-gray-500 mt-12">
          <p class="text-lg mb-2">Ask me about your screenshots!</p>
          <p class="text-sm">Try: "show me code screenshots" or "find graphs"</p>
        </div>

        <!-- Messages -->
        <div v-for="(message, index) in messages" :key="index">
          <!-- User Message -->
          <div v-if="message.type === 'user'" class="flex justify-end">
            <div class="bg-blue-600 text-white px-4 py-2 rounded-lg max-w-md">
              {{ message.content }}
            </div>
          </div>

          <!-- AI Message -->
          <div v-else class="flex justify-start">
            <div class="bg-white border border-gray-200 rounded-lg p-4 max-w-3xl w-full">
              <p class="text-gray-800 mb-3">{{ message.content }}</p>
              
              <!-- Results Grid -->
              <div v-if="message.results && message.results.length > 0" class="grid grid-cols-2 gap-3 mt-3">
                <div
                  v-for="result in message.results"
                  :key="result.id"
                  @click="openImageModal(result.filename)"
                  class="border border-gray-200 rounded-lg p-2 hover:shadow-lg transition-shadow cursor-pointer"
                >
                  <img
                    :src="`http://localhost:8000/api/images/${result.filename}`"
                    :alt="result.filename"
                    class="w-full h-32 object-cover rounded mb-2"
                  />
                  <div class="text-xs text-gray-600 truncate mb-1">{{ result.filename }}</div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-500">Confidence</span>
                    <span class="text-xs font-semibold text-blue-600">
                      {{ Math.round(result.confidence * 100) }}%
                    </span>
                  </div>
                  <div v-if="result.reason" class="text-xs text-gray-500 mt-1 line-clamp-2">
                    {{ result.reason }}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Input Area -->
      <div class="bg-white border-t border-gray-200 px-6 py-4">
        <div class="flex gap-2">
          <input
            v-model="userInput"
            @keyup.enter="sendMessage"
            type="text"
            placeholder="Ask about your screenshots..."
            class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            :disabled="isLoading"
          />
          <button
            @click="sendMessage"
            :disabled="isLoading || !userInput.trim()"
            class="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {{ isLoading ? 'Searching...' : 'Send' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div
      v-if="selectedImage"
      @click="closeImageModal"
      class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50 p-4"
    >
      <div class="relative max-w-5xl max-h-full">
        <button
          @click="closeImageModal"
          class="absolute top-4 right-4 bg-white text-gray-800 rounded-full w-10 h-10 flex items-center justify-center hover:bg-gray-100 transition-colors"
        >
          ✕
        </button>
        <img
          :src="`http://localhost:8000/api/images/${selectedImage}`"
          :alt="selectedImage"
          class="max-w-full max-h-screen object-contain rounded-lg"
          @click.stop
        />
        <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-white px-4 py-2 rounded-lg shadow-lg">
          <span class="text-sm text-gray-700">{{ selectedImage }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const messages = ref([])
const userInput = ref('')
const isLoading = ref(false)
const selectedImage = ref(null)
const messagesContainer = ref(null)
const totalScreenshots = ref(0)

onMounted(async () => {
  // Get initial stats
  try {
    const response = await axios.get(`${API_BASE_URL}/api/stats`)
    totalScreenshots.value = response.data.total_screenshots
  } catch (error) {
    console.error('Failed to fetch stats:', error)
  }
})

const sendMessage = async () => {
  if (!userInput.value.trim() || isLoading.value) return

  const query = userInput.value.trim()
  userInput.value = ''

  // Add user message
  messages.value.push({
    type: 'user',
    content: query
  })

  isLoading.value = true

  try {
    const response = await axios.post(`${API_BASE_URL}/api/chat`, {
      query: query
    })

    // Add AI response
    messages.value.push({
      type: 'ai',
      content: response.data.results.length > 0
        ? `Found ${response.data.results.length} matching screenshot${response.data.results.length > 1 ? 's' : ''}`
        : 'No matching screenshots found',
      results: response.data.results
    })

  } catch (error) {
    console.error('Search error:', error)
    messages.value.push({
      type: 'ai',
      content: 'Sorry, there was an error searching your screenshots.',
      results: []
    })
  } finally {
    isLoading.value = false
    await nextTick()
    scrollToBottom()
  }
}

const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

const openImageModal = (filename) => {
  selectedImage.value = filename
}

const closeImageModal = () => {
  selectedImage.value = null
}
</script>
