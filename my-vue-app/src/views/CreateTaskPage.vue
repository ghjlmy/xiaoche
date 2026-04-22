<template>
  <div class="flex flex-col h-screen bg-gray-50">
    <header class="bg-white shadow-sm border-b border-gray-200 px-6 py-3 flex items-center justify-between z-20 flex-shrink-0">
      <div class="flex items-center gap-2">
        <button @click="goBack" class="flex items-center gap-2 text-primary hover:text-primary/80 transition">
          <i class="fa fa-arrow-left"></i>
          <span>返回</span>
        </button>
      </div>
      <h1 class="text-lg font-bold text-gray-800">新建任务</h1>
      <div class="flex items-center gap-2">
        <button @click="goBack" class="px-6 py-2 border border-gray-200 text-gray-700 rounded-md hover:bg-gray-50 transition">
          取消
        </button>
        <button @click="createTask" :disabled="!newTaskName.trim() || nameDuplicate" class="px-6 py-2 bg-primary text-white rounded-md hover:bg-primary/90 transition disabled:opacity-50 disabled:cursor-not-allowed">
          创建任务
        </button>
      </div>
    </header>

    <main class="flex-1 flex overflow-hidden">
      <aside class="w-64 bg-white border-r border-gray-200 flex flex-col flex-shrink-0">
        <nav class="flex-1 py-3 overflow-y-auto">
          <div class="px-3 mb-2">
            <h3 class="text-xs font-semibold text-gray-500 uppercase">资源列表</h3>
          </div>
          <div class="space-y-1">
            <div>
              <button 
                @click="activeTab = 'points'" 
                :class="activeTab === 'points' ? 'bg-primary/10 text-primary' : 'hover:bg-gray-50 text-gray-dark'"
                class="w-full text-left px-3 py-2 text-sm flex items-center gap-2"
              >
                <i class="fa fa-map-marker"></i>
                点列表
              </button>
              <div v-if="activeTab === 'points'" class="pl-6 space-y-1 max-h-40 overflow-y-auto">
                <div 
                  v-for="point in pointsList" 
                  :key="point.id"
                  @click="addPointToTask(point)"
                  class="px-2 py-1 text-xs rounded bg-gray-50 hover:bg-gray-100 text-gray-dark cursor-pointer"
                >
                  {{ point.name }}
                </div>
              </div>
            </div>
            <div>
              <button 
                @click="activeTab = 'paths'" 
                :class="activeTab === 'paths' ? 'bg-primary/10 text-primary' : 'hover:bg-gray-50 text-gray-dark'"
                class="w-full text-left px-3 py-2 text-sm flex items-center gap-2"
              >
                <i class="fa fa-road"></i>
                路径列表
              </button>
              <div v-if="activeTab === 'paths'" class="pl-6 space-y-1 max-h-40 overflow-y-auto">
                <div 
                  v-for="path in pathsList" 
                  :key="path.id"
                  @click="addPathToTask(path)"
                  class="px-2 py-1 text-xs rounded bg-gray-50 hover:bg-gray-100 text-gray-dark cursor-pointer"
                >
                  {{ path.name }}
                </div>
              </div>
            </div>
          </div>
        </nav>
      </aside>

      <section class="flex-1 bg-gray-50 flex flex-col overflow-hidden">
         <div class="bg-white border-t border-gray-200 p-6">
          <div class="grid grid-cols-3 gap-4 mb-4">
            <label class="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
              <span class="text-sm text-gray-dark">循环执行</span>
              <input type="checkbox" v-model="newTaskConfig.loop" class="w-4 h-4 accent-primary" />
            </label>
            <label class="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
              <span class="text-sm text-gray-dark">轨道模式</span>
              <input type="checkbox" v-model="newTaskConfig.trackMode" class="w-4 h-4 accent-primary" />
            </label>
            <label class="flex items-center justify-between bg-gray-50 p-3 rounded-lg">
              <span class="text-sm text-gray-dark">定时任务</span>
              <input type="checkbox" v-model="newTaskConfig.scheduled" class="w-4 h-4 accent-primary" />
            </label>
          </div>

          <div v-if="newTaskConfig.scheduled" class="mb-4">
            <label class="text-sm text-gray-600 block mb-1">定时时间</label>
            <input type="datetime-local" v-model="newTaskConfig.scheduledTime" class="w-full px-3 py-2 border border-gray-200 rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary" />
          </div>

          <div class="flex items-center gap-4">
            <div class="flex-1">
              <label class="text-sm text-gray-600 block mb-1">任务名称</label>
              <input 
                v-model="newTaskName" 
                type="text" 
                :class="nameDuplicate ? 'border-danger focus:ring-danger' : 'border-gray-200 focus:ring-primary'"
                class="w-full px-3 py-2 border rounded-md text-sm focus:outline-none focus:ring-1"
                placeholder="请输入任务名称"
              />
              <div v-if="nameDuplicate" class="text-xs text-danger mt-1">
                <i class="fa fa-exclamation-circle mr-1"></i>任务名称已存在
              </div>
            </div>
          </div>
        </div>
        <div class="flex-1 p-6 overflow-y-auto">
          <div class="bg-white rounded-lg shadow-sm border border-gray-200 h-full flex flex-col">
            <div class="p-4 border-b border-gray-200 flex items-center justify-between">
              <h3 class="font-semibold text-gray-dark">任务步骤</h3>
              <button @click="clearSteps" class="px-3 py-1 text-xs text-gray-dark hover:text-danger transition">
                <i class="fa fa-trash-o mr-1"></i>清空
              </button>
            </div>
            <div class="flex-1 p-4 overflow-y-auto">
              <div v-if="newTaskSteps.length === 0" class="h-full flex items-center justify-center text-gray-400">
                <div class="text-center">
                  <i class="fa fa-list-ul text-4xl mb-2"></i>
                  <p class="text-sm">从左侧选择点或路径添加到任务</p>
                </div>
              </div>
              <div v-else class="space-y-3">
                <div 
                  v-for="(step, index) in newTaskSteps" 
                  :key="index"
                  :draggable="true"
                  @dragstart="onDragStart($event, index)"
                  @dragover.prevent="onDragOver($event, index)"
                  @drop="onDrop($event, index)"
                  class="border border-gray-200 rounded-lg p-3 bg-gray-50 hover:bg-gray-100 transition cursor-move"
                >
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center gap-2">
                      <i class="fa fa-grip-vertical text-gray-400"></i>
                      <span class="text-sm font-medium">
                        <span class="inline-flex items-center justify-center w-6 h-6 bg-primary text-white rounded-full text-xs mr-2">{{ index + 1 }}</span>
                        {{ step.type === 'point' ? '点位导航' : '路径行驶' }}: {{ step.name }}
                      </span>
                    </div>
                    <button @click="removeStep(index)" class="text-gray-400 hover:text-danger">
                      <i class="fa fa-times"></i>
                    </button>
                  </div>
                  <div class="pl-8 space-y-2 text-xs">
                    <div class="flex items-center gap-2">
                      <span class="text-gray-600">动作:</span>
                      <select v-model="step.action" class="border border-gray-200 rounded px-2 py-1 text-xs">
                        <option value="navigate">导航</option>
                        <option value="charge">自动充电</option>
                        <option value="wait">等待</option>
                      </select>
                    </div>
                    <div v-if="step.action === 'wait'" class="flex items-center gap-2">
                      <span class="text-gray-600">等待时间:</span>
                      <input type="number" v-model.number="step.waitTime" min="0" class="w-20 border border-gray-200 rounded px-2 py-1 text-xs" placeholder="秒" />
                      <span class="text-gray-500">秒</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

       
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'CreateTaskPage',
  data() {
    return {
      activeTab: 'points',
      newTaskName: '',
      newTaskSteps: [],
      newTaskConfig: {
        loop: false,
        trackMode: false,
        scheduled: false,
        scheduledTime: ''
      },
      dragIndex: null,
      pointsList: [
        { id: 'P001', name: 'P001 - 入库口', x: 180, y: 380 },
        { id: 'P002', name: 'P002 - 分拣区', x: 220, y: 380 },
        { id: 'P003', name: 'P003 - 充电位', x: 380, y: 450 },
        { id: 'P004', name: 'P004 - 导航1', x: 220, y: 250 },
        { id: 'P005', name: 'P005 - 导航2', x: 280, y: 250 },
        { id: 'P006', name: 'P006 - 导航3', x: 280, y: 450 },
        { id: 'P007', name: 'P007 - 定位点1', x: 320, y: 320 },
        { id: 'P008', name: 'P008 - 停车点', x: 350, y: 380 },
        { id: 'P009', name: 'P009 - 末端辅助定位', x: 400, y: 450 }
      ],
      pathsList: [
        { id: 'path1', name: '路径1 - 入库到充电' },
        { id: 'path2', name: '路径2 - 分拣到导航' },
        { id: 'path3', name: '路径3 - 巡检路径' }
      ],
      taskList: []
    };
  },
  computed: {
    nameDuplicate() {
      return this.taskList.some(task => task.name === this.newTaskName.trim());
    }
  },
  mounted() {
    const savedTasks = localStorage.getItem('compositeTasks');
    if (savedTasks) {
      this.taskList = JSON.parse(savedTasks);
    }
  },
  methods: {
    goBack() {
      this.$router.push('/composite-task');
    },
    addPointToTask(point) {
      this.newTaskSteps.push({
        type: 'point',
        id: point.id,
        name: point.name,
        action: 'navigate',
        waitTime: 0
      });
    },
    addPathToTask(path) {
      this.newTaskSteps.push({
        type: 'path',
        id: path.id,
        name: path.name,
        action: 'navigate',
        waitTime: 0
      });
    },
    removeStep(index) {
      this.newTaskSteps.splice(index, 1);
    },
    clearSteps() {
      if (confirm('确定要清空所有任务步骤吗？')) {
        this.newTaskSteps = [];
      }
    },
    onDragStart(e, index) {
      this.dragIndex = index;
      e.dataTransfer.effectAllowed = 'move';
    },
    onDragOver(e, index) {
      if (this.dragIndex !== index) {
        e.dataTransfer.dropEffect = 'move';
      }
    },
    onDrop(e, index) {
      e.preventDefault();
      if (this.dragIndex !== index) {
        const item = this.newTaskSteps[this.dragIndex];
        this.newTaskSteps.splice(this.dragIndex, 1);
        this.newTaskSteps.splice(index, 0, item);
      }
      this.dragIndex = null;
    },
    createTask() {
      if (!this.newTaskName.trim()) {
        alert('请输入任务名称');
        return;
      }
      
      if (this.nameDuplicate) {
        alert('任务名称已存在，请使用其他名称');
        return;
      }

      const savedTasks = localStorage.getItem('compositeTasks');
      let tasks = savedTasks ? JSON.parse(savedTasks) : [];
      
      const newId = (tasks.length + 1).toString();
      tasks.unshift({
        id: newId,
        name: this.newTaskName.trim(),
        steps: [...this.newTaskSteps],
        loop: this.newTaskConfig.loop
      });

      localStorage.setItem('compositeTasks', JSON.stringify(tasks));

      this.goBack();
    }
  }
};
</script>
