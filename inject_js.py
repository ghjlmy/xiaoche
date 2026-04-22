# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = r'd:\前端项目\小车重构'
VIEWS_DIR = os.path.join(BASE_DIR, 'my-vue-app', 'src', 'views')

with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Extract JS section
js_start = None
js_end = None
for i, line in enumerate(lines):
    if '<script>' in line and i > 6000:
        js_start = i + 1
    if '</script>' in line and js_start is not None and js_end is None:
        js_end = i
js_content = '\n'.join(lines[js_start:js_end])

# Page-specific JS mapping
# Each page gets its own JS functions
page_js = {
    'MainPage': r'''
      let carX = 280;
      let carY = 250;
      let carRotation = 0;
      let battery = 82;
      let runSeconds = 2 * 3600 + 21 * 60 + 16;
      let totalMileage = 125.9;
      const pathPoints = [
        { x: 280, y: 250, targetRotation: 180 },
        { x: 280, y: 450, targetRotation: 90 },
        { x: 380, y: 450, targetRotation: 0 },
        { x: 220, y: 250, targetRotation: 180 },
      ];
      let currentPointIndex = 0;
      const chassisStates = ['空闲', '导航', '充电', '急停', '异常'];
      let currentChassisState = 0;
      let mainInterval = null;

      function updateAgvPosition() {
        const agvCar = document.getElementById("agvCar");
        if (agvCar) {
          agvCar.setAttribute('transform', `translate(${carX}, ${carY}) rotate(${carRotation})`);
        }
      }

      function startDataUpdates() {
        if (mainInterval) return;
        mainInterval = setInterval(() => {
          const posX = document.getElementById("posX");
          const posY = document.getElementById("posY");
          const speed = document.getElementById("speed");
          const angularVelocity = document.getElementById("angular-velocity");
          const current = document.getElementById("current");
          const voltage = document.getElementById("voltage");
          const mileage = document.getElementById("mileage");
          const batteryBar = document.getElementById("batteryBar");
          const batteryText = document.getElementById("batteryText");
          const uptime = document.getElementById("uptime");
          const mapMatch = document.getElementById("map-match");
          const chassisStatus = document.getElementById("chassis-status");
          const batteryTemp = document.getElementById("battery-temp");
          const errorCode = document.getElementById("error-code");

          const target = pathPoints[currentPointIndex];
          if (target) {
            const dx = target.x - carX;
            const dy = target.y - carY;
            const dist = Math.sqrt(dx * dx + dy * dy);
            if (dist > 2) {
              const moveSpeed = 1;
              carX += (dx / dist) * moveSpeed;
              carY += (dy / dist) * moveSpeed;
              const targetAngle = Math.atan2(dy, dx) * 180 / Math.PI + 90;
              let angleDiff = targetAngle - carRotation;
              while (angleDiff > 180) angleDiff -= 360;
              while (angleDiff < -180) angleDiff += 360;
              if (Math.abs(angleDiff) > 1) {
                carRotation += Math.sign(angleDiff) * Math.min(Math.abs(angleDiff), 3);
              }
              updateAgvPosition();
              if (posX) posX.textContent = ((carX - 100) * 0.1 + 30).toFixed(2);
              if (posY) posY.textContent = ((carY - 200) * 0.1 + 10).toFixed(2);
              totalMileage += 0.001;
              if (mileage) mileage.textContent = totalMileage.toFixed(1) + " km";
            } else {
              currentPointIndex = (currentPointIndex + 1) % pathPoints.length;
              const nextTarget = pathPoints[currentPointIndex];
              carRotation = nextTarget.targetRotation;
              updateAgvPosition();
            }
          }

          battery -= 0.01;
          if (batteryBar) {
            if (battery < 20) {
              batteryBar.classList.remove("bg-success");
              batteryBar.classList.add("bg-danger");
            } else if (battery < 50) {
              batteryBar.classList.remove("bg-success");
              batteryBar.classList.add("bg-warning");
            }
            batteryBar.style.width = battery + "%";
          }
          if (batteryText) batteryText.textContent = Math.round(battery) + "%";
          if (current) current.textContent = (2.3 + Math.random() * 0.2).toFixed(1) + " A";
          if (voltage) voltage.textContent = (23.7 + Math.random() * 0.2).toFixed(1) + " V";
          if (speed) speed.textContent = (0.4 + Math.random() * 0.1).toFixed(1) + " m/s";
          if (angularVelocity) angularVelocity.textContent = (Math.random() * 2 - 1).toFixed(1) + "°/s";
          if (mapMatch) mapMatch.textContent = (90 + Math.random() * 10).toFixed(0) + "%";
          if (batteryTemp) batteryTemp.textContent = (25 + Math.random() * 10).toFixed(0) + "°C";
          if (errorCode) {
            errorCode.textContent = Math.random() > 0.9 ? Math.floor(Math.random() * 100) : 0;
            errorCode.className = errorCode.textContent === "0" ? "font-medium text-success" : "font-medium text-danger";
          }
          if (Math.random() < 0.01) {
            currentChassisState = Math.floor(Math.random() * chassisStates.length);
            const statusText = chassisStates[currentChassisState];
            if (chassisStatus) {
              chassisStatus.textContent = statusText;
              chassisStatus.className = "font-medium " + 
                (statusText === '空闲' || statusText === '导航' || statusText === '充电' ? 'text-success' : 
                 statusText === '急停' ? 'text-warning' : 'text-danger');
            }
          }
          runSeconds++;
          const hours = Math.floor(runSeconds / 3600);
          const minutes = Math.floor((runSeconds % 3600) / 60);
          const seconds = runSeconds % 60;
          if (uptime) uptime.textContent = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
        }, 1000);
      }

      function stopDataUpdates() {
        if (mainInterval) {
          clearInterval(mainInterval);
          mainInterval = null;
        }
      }

      function toggleMapManage() {
        const mapManageDropdown = document.getElementById("map-manage-dropdown");
        const mapManageIcon = document.getElementById("map-manage-icon");
        if (mapManageDropdown) mapManageDropdown.classList.toggle("show");
        if (mapManageIcon) mapManageIcon.classList.toggle("rotate-180");
      }

      function toggleTaskManage() {
        const taskManageDropdown = document.getElementById("task-manage-dropdown");
        const taskManageIcon = document.getElementById("task-manage-icon");
        if (taskManageDropdown) taskManageDropdown.classList.toggle("show");
        if (taskManageIcon) taskManageIcon.classList.toggle("rotate-180");
      }
''',
    'PathManagePage': r'''
      let pathRecordingMode = false;
      let pathRecordingPoints = [];
      let pathEditMode = false;
      let pathCurveMode = false;
      let currentPathDirection = 'single';
      let selectedPath = null;
      let isDraggingPath = false;
      let draggedPathControl = null;
      let pathDragInitialized = false;

      function togglePathRecording() {
        pathRecordingMode = !pathRecordingMode;
        const btn = document.getElementById('path-record-btn');
        const status = document.getElementById('record-status');
        if (pathRecordingMode) {
          btn.innerHTML = '<i class="fa fa-stop"></i>停止录制';
          btn.classList.remove('bg-primary');
          btn.classList.add('bg-danger');
          status.classList.remove('hidden');
          pathRecordingPoints = [];
        } else {
          btn.innerHTML = '<i class="fa fa-circle"></i>开始录制';
          btn.classList.remove('bg-danger');
          btn.classList.add('bg-primary');
          status.classList.add('hidden');
          if (pathRecordingPoints.length > 1) {
            alert('已录制 ' + pathRecordingPoints.length + ' 个点！');
          }
        }
      }

      function initPathDragging() {
        if (pathDragInitialized) return;
        pathDragInitialized = true;
        const svg = document.getElementById('path-svg');
        if (!svg) return;
        const controls = document.querySelectorAll('[id^="curve-ctrl-"]');
        controls.forEach(control => {
          control.style.cursor = 'grab';
          control.addEventListener('mousedown', function(e) {
            if (!pathCurveMode) return;
            e.preventDefault();
            e.stopPropagation();
            isDraggingPath = true;
            draggedPathControl = this;
            this.style.cursor = 'grabbing';
          });
        });
        svg.addEventListener('mousemove', function(e) {
          if (!isDraggingPath || !draggedPathControl) return;
          const pt = svg.createSVGPoint();
          pt.x = e.clientX;
          pt.y = e.clientY;
          const svgP = pt.matrixTransform(svg.getScreenCTM().inverse());
          draggedPathControl.setAttribute('cx', svgP.x);
          draggedPathControl.setAttribute('cy', svgP.y);
          updatePathByControlImproved(draggedPathControl.id, svgP.x, svgP.y);
        });
        document.addEventListener('mouseup', function() {
          if (isDraggingPath && draggedPathControl) {
            draggedPathControl.style.cursor = 'grab';
          }
          isDraggingPath = false;
          draggedPathControl = null;
        });
      }

      function updatePathByControlImproved(controlId, newX, newY) {
        const pathMap = {
          'curve-ctrl-1': { pathId: 'path-1', start: '100,200', end: '180,200' },
          'curve-ctrl-2': { pathId: 'path-2', start: '180,200', end: '180,130' },
          'curve-ctrl-3': { pathId: 'path-3', start: '180,130', end: '280,130' },
          'curve-ctrl-4': { pathId: 'path-4', start: '280,130', end: '280,260' },
          'curve-ctrl-5': { pathId: 'path-5', start: '280,260', end: '380,260' }
        };
        const config = pathMap[controlId];
        if (!config) return;
        const path = document.getElementById(config.pathId);
        if (!path) return;
        path.setAttribute('d', 'M' + config.start + ' Q' + newX + ',' + newY + ' ' + config.end);
      }

      function toggleAddMode() {
        pathEditMode = false;
        pathCurveMode = false;
        hideCurveControls();
        alert('添加模式：点击两点来创建路径');
      }

      function toggleEditMode() {
        pathEditMode = !pathEditMode;
        pathCurveMode = false;
        hideCurveControls();
        if (pathEditMode) {
          alert('编辑模式：点击路径可以选中和编辑');
        }
      }

      function toggleCurveMode() {
        pathCurveMode = !pathCurveMode;
        pathEditMode = false;
        if (pathCurveMode) {
          showCurveControls();
          initPathDragging();
          alert('曲度模式：现在可以看到并拖拽黄色控制点来调整路径曲度');
        } else {
          hideCurveControls();
        }
      }

      function showCurveControls() {
        const controls = document.querySelectorAll('[id^="curve-ctrl-"]');
        controls.forEach(c => c.style.display = 'block');
      }

      function hideCurveControls() {
        const controls = document.querySelectorAll('[id^="curve-ctrl-"]');
        controls.forEach(c => c.style.display = 'none');
      }

      function setPathDirection(dir) {
        currentPathDirection = dir;
        const singleBtn = document.getElementById('dir-single-btn');
        const biBtn = document.getElementById('dir-bidirectional-btn');
        if (dir === 'single') {
          singleBtn.classList.add('bg-primary', 'text-white');
          singleBtn.classList.remove('bg-gray-200', 'text-gray-700');
          biBtn.classList.remove('bg-primary', 'text-white');
          biBtn.classList.add('bg-gray-200', 'text-gray-700');
        } else {
          biBtn.classList.add('bg-primary', 'text-white');
          biBtn.classList.remove('bg-gray-200', 'text-gray-700');
          singleBtn.classList.remove('bg-primary', 'text-white');
          singleBtn.classList.add('bg-gray-200', 'text-gray-700');
        }
      }

      function deleteSelectedPath() {
        if (!selectedPath) {
          alert('请先选择要删除的路径');
          return;
        }
        if (confirm('确定要删除路径 ' + selectedPath + ' 吗？')) {
          const pathEl = document.getElementById(selectedPath);
          if (pathEl) pathEl.remove();
          const ctrlId = selectedPath.replace('path-', 'curve-ctrl-');
          const ctrlEl = document.getElementById(ctrlId);
          if (ctrlEl) ctrlEl.remove();
          selectedPath = null;
          pathDragInitialized = false;
          alert('路径已删除');
        }
      }
''',
    'HandDrawTrackPage': r'''
      let trackRecordingMode = false;
      let trackRecordingPoints = [];
      let trackEditMode = false;
      let trackCurveMode = false;
      let currentTrackDirection = 'single';
      let selectedTrack = null;
      let isDraggingTrack = false;
      let draggedTrackControl = null;
      let trackDragInitialized = false;

      function toggleTrackRecording() {
        trackRecordingMode = !trackRecordingMode;
        const btn = document.getElementById('track-record-btn');
        const status = document.getElementById('track-record-status');
        if (trackRecordingMode) {
          btn.innerHTML = '<i class="fa fa-stop"></i>停止录制';
          btn.classList.remove('bg-primary');
          btn.classList.add('bg-danger');
          status.classList.remove('hidden');
          trackRecordingPoints = [];
        } else {
          btn.innerHTML = '<i class="fa fa-circle"></i>开始录制';
          btn.classList.remove('bg-danger');
          btn.classList.add('bg-primary');
          status.classList.remove('hidden');
          if (trackRecordingPoints.length > 1) {
            alert('已录制轨道，' + trackRecordingPoints.length + ' 个点！');
          }
        }
      }

      function initTrackDragging() {
        if (trackDragInitialized) return;
        trackDragInitialized = true;
        const svg = document.getElementById('track-svg');
        if (!svg) return;
        const controls = document.querySelectorAll('[id^="track-curve-"]');
        controls.forEach(control => {
          control.style.cursor = 'grab';
          control.addEventListener('mousedown', function(e) {
            if (!trackCurveMode) return;
            e.preventDefault();
            e.stopPropagation();
            isDraggingTrack = true;
            draggedTrackControl = this;
            this.style.cursor = 'grabbing';
          });
        });
        svg.addEventListener('mousemove', function(e) {
          if (!isDraggingTrack || !draggedTrackControl) return;
          const pt = svg.createSVGPoint();
          pt.x = e.clientX;
          pt.y = e.clientY;
          const svgP = pt.matrixTransform(svg.getScreenCTM().inverse());
          draggedTrackControl.setAttribute('cx', svgP.x);
          draggedTrackControl.setAttribute('cy', svgP.y);
          updateTrackByControl(draggedTrackControl.id, svgP.x, svgP.y);
        });
        document.addEventListener('mouseup', function() {
          if (isDraggingTrack && draggedTrackControl) {
            draggedTrackControl.style.cursor = 'grab';
          }
          isDraggingTrack = false;
          draggedTrackControl = null;
        });
      }

      function updateTrackByControl(controlId, newX, newY) {
        if (controlId === 'track-curve-1') {
          const track = document.getElementById('track-1');
          if (track) track.setAttribute('d', 'M100,100 Q' + newX + ',' + newY + ' 200,100');
        } else if (controlId.startsWith('track-curve-2')) {
          const track = document.getElementById('track-2');
          if (!track) return;
          const num = parseInt(controlId.split('-').pop());
          const d = track.getAttribute('d');
          const segs = d.split(' Q');
          if (num <= segs.length) {
            const seg = segs[num];
            const endParts = seg.split(' ');
            segs[num] = newX + ',' + newY + ' ' + endParts.slice(1).join(' ');
            track.setAttribute('d', segs.join(' Q'));
          }
        } else if (controlId === 'track-curve-3') {
          const track = document.getElementById('track-3');
          if (track) track.setAttribute('d', 'M100,300 Q' + newX + ',' + newY + ' 300,300');
        }
      }

      function toggleTrackAddMode() {
        trackEditMode = false;
        trackCurveMode = false;
        hideTrackCurveControls();
        alert('添加模式：点击两点来创建轨道');
      }

      function toggleTrackEditMode() {
        trackEditMode = !trackEditMode;
        trackCurveMode = false;
        hideTrackCurveControls();
        if (trackEditMode) {
          alert('编辑模式：点击轨道可以选中和编辑');
        }
      }

      function toggleTrackCurveMode() {
        trackCurveMode = !trackCurveMode;
        trackEditMode = false;
        if (trackCurveMode) {
          showTrackCurveControls();
          initTrackDragging();
          alert('曲度模式：现在可以看到并拖拽黄色控制点来调整轨道曲度');
        } else {
          hideTrackCurveControls();
        }
      }

      function showTrackCurveControls() {
        const controls = document.querySelectorAll('[id^="track-curve-"]');
        controls.forEach(c => c.style.display = 'block');
      }

      function hideTrackCurveControls() {
        const controls = document.querySelectorAll('[id^="track-curve-"]');
        controls.forEach(c => c.style.display = 'none');
      }

      function setTrackDirection(dir) {
        currentTrackDirection = dir;
        const singleBtn = document.getElementById('track-dir-single-btn');
        const biBtn = document.getElementById('track-dir-bidirectional-btn');
        if (dir === 'single') {
          singleBtn.classList.add('bg-primary', 'text-white');
          singleBtn.classList.remove('bg-gray-200', 'text-gray-700');
          biBtn.classList.remove('bg-primary', 'text-white');
          biBtn.classList.add('bg-gray-200', 'text-gray-700');
        } else {
          biBtn.classList.add('bg-primary', 'text-white');
          biBtn.classList.remove('bg-gray-200', 'text-gray-700');
          singleBtn.classList.remove('bg-primary', 'text-white');
          singleBtn.classList.add('bg-gray-200', 'text-gray-700');
        }
      }

      function deleteSelectedTrack() {
        if (!selectedTrack) {
          alert('请先选择要删除的轨道');
          return;
        }
        if (confirm('确定要删除轨道 ' + selectedTrack + ' 吗？')) {
          const trackEl = document.getElementById(selectedTrack);
          if (trackEl) trackEl.remove();
          selectedTrack = null;
          trackDragInitialized = false;
          alert('轨道已删除');
        }
      }
''',
    'VirtualWallPage': r'''
      let currentShapeTool = 'rect';
      let virtualWallPoints = [];
      let isDrawingVirtualWall = false;

      function initVirtualWallCanvas() {
        const canvas = document.getElementById('virtualWallCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const container = canvas.parentElement;
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        drawVirtualWallGrid(ctx, canvas);
      }

      function resizeVirtualWallCanvas() {
        const canvas = document.getElementById('virtualWallCanvas');
        if (!canvas) return;
        const ctx = canvas.getContext('2d');
        const container = canvas.parentElement;
        canvas.width = container.clientWidth;
        canvas.height = container.clientHeight;
        drawVirtualWallGrid(ctx, canvas);
      }

      function drawVirtualWallGrid(ctx, canvas) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.strokeStyle = '#e4e7ed';
        ctx.lineWidth = 0.5;
        for (let x = 0; x < canvas.width; x += 20) {
          ctx.beginPath();
          ctx.moveTo(x, 0);
          ctx.lineTo(x, canvas.height);
          ctx.stroke();
        }
        for (let y = 0; y < canvas.height; y += 20) {
          ctx.beginPath();
          ctx.moveTo(0, y);
          ctx.lineTo(canvas.width, y);
          ctx.stroke();
        }
      }

      function setShapeTool(tool) {
        currentShapeTool = tool;
        const btns = document.querySelectorAll('[data-tool]');
        btns.forEach(btn => {
          btn.classList.remove('bg-primary', 'text-white');
          btn.classList.add('bg-gray-200', 'text-gray-700');
        });
        const activeBtn = document.querySelector('[data-tool="' + tool + '"]');
        if (activeBtn) {
          activeBtn.classList.remove('bg-gray-200', 'text-gray-700');
          activeBtn.classList.add('bg-primary', 'text-white');
        }
      }
''',
}

# Now update each Vue component with its JS logic
for comp_name, js_code in page_js.items():
    filepath = os.path.join(VIEWS_DIR, '{}.vue'.format(comp_name))
    if not os.path.exists(filepath):
        print('WARNING: {}.vue not found!'.format(comp_name))
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        vue_content = f.read()
    
    # Find the script section
    script_match = re.search(r'<script>(.*?)</script>', vue_content, re.DOTALL)
    if not script_match:
        print('WARNING: No script section in {}.vue'.format(comp_name))
        continue
    
    # Build new script section
    # Add mounted/beforeUnmount lifecycle hooks
    mounted_code = ''
    before_unmount_code = ''
    
    if comp_name == 'MainPage':
        mounted_code = '\n    this.startDataUpdates();'
        before_unmount_code = '\n    this.stopDataUpdates();'
    elif comp_name == 'VirtualWallPage':
        mounted_code = '\n    setTimeout(() => { this.initVirtualWallCanvas(); this.resizeVirtualWallCanvas(); }, 100);'
        mounted_code += '\n    window.addEventListener("resize", this.resizeVirtualWallCanvas);'
        before_unmount_code = '\n    window.removeEventListener("resize", this.resizeVirtualWallCanvas);'
    
    new_script = '<script>\n' + js_code.strip() + '\n\nexport default {\n  name: \'' + comp_name + '\',' + mounted_code + '\n  mounted() {' + mounted_code + '\n  },'
    
    if before_unmount_code:
        new_script += '\n  beforeUnmount() {' + before_unmount_code + '\n  },'
    
    new_script += '\n  methods: {\n'
    
    # Extract function names from the JS code
    func_names = re.findall(r'function\s+(\w+)\s*\(', js_code)
    for fn in func_names:
        new_script += '    ' + fn + ',\n'
    
    new_script += '  },\n};\n</script>'
    
    # Replace the script section
    new_vue_content = re.sub(r'<script>.*?</script>', new_script, vue_content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_vue_content)
    
    print('Updated {}.vue with {} functions'.format(comp_name, len(func_names)))

print('\n=== JS injection complete! ===')
