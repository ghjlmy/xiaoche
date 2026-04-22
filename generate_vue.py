# -*- coding: utf-8 -*-
import os
import re

BASE_DIR = r'd:\前端项目\小车重构'
VIEWS_DIR = os.path.join(BASE_DIR, 'my-vue-app', 'src', 'views')
os.makedirs(VIEWS_DIR, exist_ok=True)

with open(os.path.join(BASE_DIR, 'index.html'), 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
total_lines = len(lines)

page_ids = [
    'login-page', 'main-page', 'create-map-page', 'mapping-page',
    'map-list-page', 'initial-location-page', 'point-manage-page',
    'path-manage-page', 'hand-draw-track-page', 'nav-config-page',
    'temp-task-page', 'record-pack-page', 'scheduled-task-page',
    'task-report-page', 'system-config-page', 'virtual-wall-page',
]

page_names = {
    'login-page': 'LoginPage', 'main-page': 'MainPage',
    'create-map-page': 'CreateMapPage', 'mapping-page': 'MappingPage',
    'map-list-page': 'MapListPage', 'initial-location-page': 'InitialLocationPage',
    'point-manage-page': 'PointManagePage', 'path-manage-page': 'PathManagePage',
    'hand-draw-track-page': 'HandDrawTrackPage', 'nav-config-page': 'NavConfigPage',
    'temp-task-page': 'TempTaskPage', 'record-pack-page': 'RecordPackPage',
    'scheduled-task-page': 'ScheduledTaskPage', 'task-report-page': 'TaskReportPage',
    'system-config-page': 'SystemConfigPage', 'virtual-wall-page': 'VirtualWallPage',
}

# Find page boundaries using character positions
page_ranges = {}
for pid in page_ids:
    pattern = 'id="{}"'.format(pid)
    pos = content.find(pattern)
    if pos == -1:
        print('WARNING: {} not found!'.format(pid))
        continue
    
    div_start = content.rfind('<div', 0, pos)
    depth = 0
    i = div_start
    end_pos = div_start
    while i < len(content):
        if content[i:i+4] == '<div':
            if i + 4 < len(content) and content[i+4] in ' \t\n\r>':
                depth += 1
        elif content[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                end_pos = i + 6
                break
        i += 1
    
    start_line = content[:div_start].count('\n')
    end_line = content[:end_pos].count('\n') + 1
    page_ranges[pid] = (start_line, end_line)
    print('{}: lines {}-{} ({} lines)'.format(pid, start_line, end_line, end_line - start_line))

# Extract JS section
js_start = None
js_end = None
for i, line in enumerate(lines):
    if '<script>' in line and i > 6000:
        js_start = i + 1
    if '</script>' in line and js_start is not None and js_end is None:
        js_end = i
js_content = '\n'.join(lines[js_start:js_end]) if js_start and js_end else ''
print('\nJS: lines {}-{}'.format(js_start, js_end))

# Generate Vue components
for pid, (start, end) in page_ranges.items():
    comp_name = page_names[pid]
    page_html = '\n'.join(lines[start:end])
    
    # Clean up the page HTML for Vue template
    # Remove the outer div's id and adjust class
    # Replace onclick="switchPage('xxx-page')" with @click="$router.push('/xxx')"
    
    # Map page IDs to route names
    route_map = {
        'login-page': '/',
        'main-page': '/main',
        'create-map-page': '/create-map',
        'mapping-page': '/mapping',
        'map-list-page': '/map-list',
        'initial-location-page': '/initial-location',
        'point-manage-page': '/point-manage',
        'path-manage-page': '/path-manage',
        'hand-draw-track-page': '/hand-draw-track',
        'nav-config-page': '/nav-config',
        'temp-task-page': '/temp-task',
        'record-pack-page': '/record-pack',
        'scheduled-task-page': '/scheduled-task',
        'task-report-page': '/task-report',
        'system-config-page': '/system-config',
        'virtual-wall-page': '/virtual-wall',
    }
    
    # Replace switchPage calls with router.push
    for page_id, route in route_map.items():
        page_html = page_html.replace(
            "switchPage('{}')".format(page_id),
            "\$router.push('{}')".format(route)
        )
        page_html = page_html.replace(
            "switchPage(\"{}\")".format(page_id),
            "\$router.push('{}')".format(route)
        )
    
    # Replace onclick with @click for Vue
    page_html = re.sub(r'onclick="([^"]+)"', r'@click="\1"', page_html)
    
    # Replace getElementById patterns with ref patterns (we'll keep using refs)
    # For now, keep the template as-is and use onMounted + document.getElementById
    
    # Build the Vue SFC
    vue_sfc = '<template>\n{}\n</template>\n\n<script>\nexport default {{\n  name: \'{}\',\n  mounted() {{\n    this.initPage();\n  }},\n  methods: {{\n    initPage() {{\n      // Page-specific initialization\n    }},\n  }},\n}};\n</script>\n'.format(page_html, comp_name)
    
    filepath = os.path.join(VIEWS_DIR, '{}.vue'.format(comp_name))
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(vue_sfc)
    
    print('Written {}.vue'.format(comp_name))

print('\n=== Vue component generation complete! ===')
