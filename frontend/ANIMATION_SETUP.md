# BabyCare 前端动画库安装完成

## ✅ 已安装的包

### 动画库
- ✅ **@vueuse/motion** - Vue 3 动画库（类似 Framer Motion）
- ✅ **gsap** - 专业动画库

### CSS 框架
- ✅ **tailwindcss** - 原子化 CSS 框架
- ✅ **autoprefixer** - 自动添加浏览器前缀
- ✅ **postcss** - CSS 处理工具

### 图标库
- ✅ **@iconify/vue** - 通用图标库
- ✅ **@vicons/ionicons5** - Ionicons 图标集（已安装）

---

## 📁 配置文件

### 1. **PostCSS 配置** ✅
```javascript
// postcss.config.js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### 2. **Tailwind 配置** ✅
```javascript
// tailwind.config.js
// 已配置品牌色系、动画、阴影等
// 位置: /Users/allenyep/Documents/gitRepo/babyCare/frontend/tailwind.config.js
```

### 3. **全局样式** ✅
```css
/* src/styles/index.css */
@tailwind base;
@tailwind components;
@tailwind utilities
```

### 4. **Vue 插件** ✅
```typescript
// src/main.ts
import { MotionPlugin } from '@vueuse/motion'

app.use(MotionPlugin)
```

---

## 🎨 使用方法

### 1. VueUse Motion

在组件中使用 `v-motion` 指令：

```vue
<template>
  <div
    v-motion
    :initial="{ opacity: 0, y: 100 }"
    :enter="{ opacity: 1, y: 0, transition: { duration: 800 } }"
  >
    淡入上移动画
  </div>
</template>
```

**预设动画：**
- `initial` - 初始状态
- `enter` - 进入动画
- `leave` - 离开动画
- `visible` - 可见性动画

### 2. Tailwind CSS

直接在类名中使用：

```vue
<template>
  <div class="bg-primary-500 text-white p-6 rounded-2xl shadow-glow">
    主要颜色卡片
  </div>
</template>
```

**可用颜色：**
- `primary-500` - 蓝色 (#0ea5e9)
- `accent-500` - 橙红色 (#f05a46)
- `success-500` - 绿色 (#22c55e)
- `warning-500` - 黄色 (#f59e0b)
- `danger-500` - 红色 (#ef4444)

**可用阴影：**
- `shadow-soft` - 微妙阴影
- `shadow-medium` - 中等阴影
- `shadow-large` - 大阴影
- `shadow-glow` - 发光效果

**可用动画：**
- `animate-fade-in` - 淡入
- `animate-fade-in-up` - 上浮淡入
- `animate-scale-in` - 缩放淡入
- `animate-shimmer` - 闪烁
- `animate-float` - 浮动
- `animate-pulse-soft` - 柔和脉冲

### 3. 自定义动画

创建自己的动画：

```vue
<script setup>
import { useMotion } from '@vueuse/motion'

const { variant } = useMotion('my-element', {
  initial: { scale: 0 },
  enter: { scale: 1 }
})
</script>

<template>
  <div v-motion="variant">动画元素</div>
</template>
```

---

## 🧪 测试页面

访问动画测试页面：
```
http://localhost:5173/animation-test
```

测试页面包含：
- ✅ VueUse Motion 动画演示
- ✅ Tailwind CSS 颜色和样式
- ✅ 预设动画效果

---

## 📖 快速参考

### 常用动画属性

**VueUse Motion:**
```javascript
// 淡入上浮
{
  initial: { opacity: 0, y: 100 },
  enter: { opacity: 1, y: 0 }
}

// 缩放
{
  initial: { scale: 0.9 },
  enter: { scale: 1 }
}

// 滑入
{
  initial: { x: -100 },
  enter: { x: 0 }
}
```

**Tailwind 动画类:**
```html
<div class="transition-all duration-300 hover:scale-105">
  悬停放大
</div>

<div class="animate-fade-in">
  淡入动画
</div>
```

---

## 🎯 下一步

### 短期
1. ✅ 测试动画库是否正常工作
2. ⏳ 在现有组件中添加动画效果
3. ⏳ 创建可复用的动画组件

### 中期
1. ⏳ 优化动画性能（GPU 加速）
2. ⏳ 添加过渡效果
3. ⏳ 实现微交互动画

### 长期
1. ⏳ 创建动画库文档
2. ⏳ 建立动画设计规范
3. ⏳ 性能监控和优化

---

## 🔗 相关资源

- [VueUse Motion 文档](https://motion.vueuse.org/)
- [Tailwind CSS 文档](https://tailwindcss.com/)
- [GSAP 文档](https://greensock.com/gsap)
- [Iconify 图标库](https://iconify.design/)

---

**配置完成时间**: 2026-03-27
**状态**: ✅ 所有库已安装并配置完成
