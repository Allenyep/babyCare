<template>
  <div class="test-animation-page">
    <h1>🎬 动画测试页面</h1>

    <!-- 测试 VueUse Motion -->
    <div class="animation-demo">
      <h2>VueUse Motion 测试</h2>

      <div
        v-motion
        :initial="{ opacity: 0, y: 100 }"
        :enter="{ opacity: 1, y: 0, transition: { duration: 800 } }"
        class="animated-box"
      >
        淡入上移动画 ✨
      </div>

      <div
        v-motion
        :initial="{ scale: 0 }"
        :enter="{ scale: 1, transition: { duration: 500 } }"
        class="animated-box box-secondary"
      >
        缩放动画 🎯
      </div>
    </div>

    <!-- 测试 Tailwind CSS -->
    <div class="tailwind-demo">
      <h2>Tailwind CSS 测试</h2>

      <div class="grid-test">
        <div class="grid-item bg-primary-500">Primary Blue</div>
        <div class="grid-item bg-accent-500">Accent Orange</div>
        <div class="grid-item bg-success-500">Success Green</div>
      </div>

      <button class="btn-primary">
        主要按钮
      </button>

      <button class="btn-secondary">
        次要按钮
      </button>
    </div>

    <!-- 测试动画预设 -->
    <div class="preset-demo">
      <h2>动画预设测试</h2>

      <div class="animate-fade-in">淡入动画</div>
      <div class="animate-fade-in-up">上浮动画</div>
      <div class="animate-scale-in">缩放动画</div>
      <div class="animate-shimmer">闪烁动画</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
</script>

<style scoped>
.test-animation-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 30px;
}

h2 {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
}

.animation-demo,
.tailwind-demo,
.preset-demo {
  margin-bottom: 40px;
  padding: 20px;
  background: #f9f9f9;
  border-radius: 12px;
}

.animated-box {
  width: 200px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 12px;
  margin-bottom: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.2s;
}

.animated-box:hover {
  transform: scale(1.05);
}

.box-secondary {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.grid-test {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.grid-item {
  padding: 20px;
  color: white;
  border-radius: 8px;
  text-align: center;
  font-weight: 600;
}

.tailwind-demo button {
  margin-right: 12px;
}

.preset-demo > div {
  padding: 16px;
  background: white;
  border-radius: 8px;
  margin-bottom: 12px;
  text-align: center;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
</style>
