from collections import deque

def build_roadmap(courses_data):
    """
    courses_data: list berisi dict mata kuliah.
    Contoh: {'id': 'IF101', 'label': 'Algoritma', 'sks': 3, 'prerequisites': []}
    """
    
    # Membangun struktur Graph (Adjacency List)
    adj_list = {course['id']: [] for course in courses_data}
    in_degree = {course['id']: 0 for course in courses_data}
    course_map = {course['id']: course for course in courses_data}

    # Menghitung derajat masuk (berapa prasyarat yang harus ditempuh)
    for course in courses_data:
        for pre_req in course['prerequisites']:
            if pre_req in adj_list:
                adj_list[pre_req].append(course['id'])
                in_degree[course['id']] += 1

    # Menggunakan Kahn's Algorithm untuk Topological Sort
    queue = deque([c_id for c_id in in_degree if in_degree[c_id] == 0])
    semester_levels = {}
    current_semester = 1

    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            curr = queue.popleft()
            semester_levels[curr] = current_semester
            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        current_semester += 1

    # Mengonversi hasil ke format JSON untuk Vue Flow
    nodes = []
    edges = []
    for c_id, sem in semester_levels.items():
        course = course_map[c_id]
        nodes.append({
            "id": c_id,
            "data": {"label": course['label'], "sks": course['sks'], "semester": sem}
        })
        for pre in course['prerequisites']:
            edges.append({"id": f"e{pre}-{c_id}", "source": pre, "target": c_id})
            
    return {"nodes": nodes, "edges": edges}
