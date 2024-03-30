from flask import Flask, render_template, request
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__, static_folder='static', template_folder='templates')

# สร้างกราฟ
G = nx.Graph()

# เพิ่มโหนด (สถานที่เที่ยว)
places = ['KhunDanPrakanChon', 'HaewNarokWaterfall', 'forestbambootunnel', 'SalikaWaterfall', 'LungLekGarden', 'NangRongWaterfall', 'WangTakraiWaterfall', 'ManiwongTemple', 'KhlongMadueaWaterfall']
for place in places:
    G.add_node(place)

# เพิ่มเส้นเชื่อมโยงและระยะทาง
edges = [('KhunDanPrakanChon', 'HaewNarokWaterfall', 25.7),
         ('KhunDanPrakanChon', 'forestbambootunnel', 43.1),
         ('KhunDanPrakanChon', 'SalikaWaterfall',11.9 ),
         ('KhunDanPrakanChon', 'ManiwongTemple', 22.7),
         ('KhunDanPrakanChon', 'NangRongWaterfall', 3.2),
         ('KhunDanPrakanChon', 'KhlongMadueaWaterfall', 11.9),

         ('HaewNarokWaterfall', 'KhunDanPrakanChon', 25.7),
         ('HaewNarokWaterfall', 'SalikaWaterfall', 42.3),
         ('HaewNarokWaterfall', 'LungLekGarden', 44.2),
         ('HaewNarokWaterfall', 'NangRongWaterfall', 44.8),
         ('HaewNarokWaterfall', 'WangTakraiWaterfall', 46.1),  
          
         ('forestbambootunnel', 'SalikaWaterfall', 38.8),
         ('forestbambootunnel', 'LungLekGarden', 43),
         ('forestbambootunnel', 'NangRongWaterfall', 42.3),
         ('forestbambootunnel', 'ManiwongTemple', 30),
         ('forestbambootunnel', 'KhlongMadueaWaterfall', 46.6),

         ('SalikaWaterfall', 'HaewNarokWaterfall', 39.5),
         ('SalikaWaterfall', 'forestbambootunnel', 38.4),  
         ('SalikaWaterfall', 'LungLekGarden', 11.4),
         ('SalikaWaterfall', 'NangRongWaterfall', 10.6), 
         ('SalikaWaterfall', 'WangTakraiWaterfall', 10.9), 
         ('SalikaWaterfall', 'ManiwongTemple', 22.3), 
         ('SalikaWaterfall', 'KhlongMadueaWaterfall', 15), 

         ('LungLekGarden', 'KhunDanPrakanChon', 2.5),
         ('LungLekGarden', 'SalikaWaterfall', 11.5),
         ('LungLekGarden', 'NangRongWaterfall', 2.7),
         ('LungLekGarden', 'WangTakraiWaterfall', 4.5),
         ('LungLekGarden', 'KhlongMadueaWaterfall', 11),

         ('NangRongWaterfall', 'KhunDanPrakanChon', 3.2),
         ('NangRongWaterfall', 'LungLekGarden', 2.7),
         ('NangRongWaterfall', 'ManiwongTemple', 26.5),
         ('NangRongWaterfall', 'KhlongMadueaWaterfall', 10.3),
         ('NangRongWaterfall', 'WangTakraiWaterfall', 3.8),

         ('WangTakraiWaterfall', 'KhunDanPrakanChon', 4.9),
         ('WangTakraiWaterfall', 'HaewNarokWaterfall', 45.9), 
         ('WangTakraiWaterfall', 'forestbambootunnel', 42.1), 
         ('WangTakraiWaterfall', 'LungLekGarden', 4.4),  
         ('WangTakraiWaterfall', 'KhlongMadueaWaterfall', 10.5), 

         ('ManiwongTemple', 'KhunDanPrakanChon', 26.8),
         ('ManiwongTemple', 'HaewNarokWaterfall', 44.4),
         ('ManiwongTemple', 'forestbambootunnel', 29.2),
         ('ManiwongTemple', 'SalikaWaterfall', 22.8),
         ('ManiwongTemple', 'LungLekGarden', 27.1),
         ('ManiwongTemple', 'NangRongWaterfall', 25.8),
         ('ManiwongTemple', 'WangTakraiWaterfall', 26.3),
         ('ManiwongTemple', 'KhlongMadueaWaterfall', 30.1),

         ('KhlongMadueaWaterfall', 'KhunDanPrakanChon', 11.5),
         ('KhlongMadueaWaterfall', 'HaewNarokWaterfall', 50.1),
         ('KhlongMadueaWaterfall', 'forestbambootunnel', 46.7),
         ('KhlongMadueaWaterfall', 'SalikaWaterfall', 15),
         ('KhlongMadueaWaterfall', 'LungLekGarden', 11.1),
         ('KhlongMadueaWaterfall', 'NangRongWaterfall', 10.3),
         ('KhlongMadueaWaterfall', 'WangTakraiWaterfall', 10.6),
         ('KhlongMadueaWaterfall', 'ManiwongTemple', 30.9)]
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# ฟังก์ชันสำหรับการสร้างภาพกราฟและแปลงเป็น base64 string
def generate_graph_image(graph):
    # วาดกราฟ
    pos = nx.circular_layout(graph)  # เปลี่ยน layout ของโหนดเป็นแบบวงกลม
    edge_labels = {(u, v): f"{d['weight']} km" for u, v, d in graph.edges(data=True)}

    
    # สร้างกราฟ
    plt.figure(figsize=(11, 7))  # ปรับขนาดกราฟให้มีขนาดใหญ่ขึ้น
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=2000)  # วาดโหนด
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)  # แสดงระยะทางบนเส้นเชื่อมโยง
    nx.draw_networkx_edges(graph, pos, edge_color='gray')  # วาดเส้นเชื่อมโยงโดยใช้สีเทา

    # บันทึกภาพของกราฟเป็นภาพ png ใน buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # อ่านข้อมูลจาก buffer และแปลงเป็น base64 string
    graph_image = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # ปิดกราฟเพื่อล้างหน่วยความจำ
    plt.close()

    return graph_image

def find_shortest_path(graph, start, end):
    try:
        shortest_path = nx.shortest_path(graph, start, end, weight='weight')
        shortest_path_length = nx.shortest_path_length(graph, start, end, weight='weight')
    except nx.NodeNotFound:
        return None, None
    
    # วาดกราฟที่มีเส้นทางที่สั้นที่สุดเฉพาะ
    pos = nx.spring_layout(graph)
    edge_labels = {(u, v): d['weight'] for u, v, d in graph.edges(data=True)}
    plt.figure()
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', node_size=1000)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    
    # วาดเส้นทางที่สั้นที่สุดให้เป็นสีแดง
    nx.draw_networkx_nodes(graph, pos, nodelist=shortest_path, node_color='red', node_size=1000)
    nx.draw_networkx_edges(graph, pos, edgelist=[(shortest_path[i], shortest_path[i+1]) for i in range(len(shortest_path)-1)], edge_color='red', width=2)
    
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges(), edge_color='gray')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    graph_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    return shortest_path, graph_image

@app.route('/find_shortest_path', methods=['POST'])
def find_path():
    start = request.form['start']
    end = request.form['end']
    shortest_path, graph_image = find_shortest_path(G, start, end)
    return render_template('find_shortest.html', shortest_path=shortest_path, graph_image=graph_image)

# ฟังก์ชันสำหรับการเพิ่มโหนดใหม่
def insert_node(node_name):
    G.add_node(node_name)

# ฟังก์ชันสำหรับการเพิ่มเส้นเชื่อมใหม่
def insert_edge(start_node, end_node, weight):
    G.add_edge(start_node, end_node, weight=weight)

@app.route('/')
def index():
    graph_image = generate_graph_image(G)
    return render_template('index.html', graph_image=graph_image)



@app.route('/insert_node', methods=['POST'])
def insert_node_route():
    node_name = request.form['node_name']
    insert_node(node_name)
    graph_image = generate_graph_image(G)
    return render_template('index.html', graph_image=graph_image)

@app.route('/insert_edge', methods=['POST'])
def insert_edge_route():
    try:
        start_node = request.form['from_node']
        end_node = request.form['to_node']
        weight = int(request.form['weight'])
        insert_edge(start_node, end_node, weight)
        graph_image = generate_graph_image(G)
        return render_template('index.html', graph_image=graph_image)
    except KeyError:
        return "Missing required fields", 400


# ฟังก์ชันสำหรับเปลี่ยนชื่อโหนด
def change_node_name(graph, old_name, new_name):
    graph = nx.relabel_nodes(graph, {old_name: new_name})
    return graph


# ฟังก์ชันสำหรับเปลี่ยนระยะทางของเส้นเชื่อม
def change_edge_distance(G, node1, node2, new_distance):
    if G.has_edge(node1, node2):
        G[node1][node2]['weight'] = new_distance


@app.route('/edit', methods=['POST'])
def edit():
    global G
    action = request.form['action']
    if action == 'change_node_name':
        old_name = request.form['old_name']
        new_name = request.form['new_name']
        G = change_node_name(G, old_name, new_name)
    elif action == 'change_edge_distance':
        node1 = request.form['node1']
        node2 = request.form['node2']
        new_distance = int(request.form['new_distance'])
        change_edge_distance(G, node1, node2, new_distance)
    graph_image = generate_graph_image(G)
    return render_template('index.html', graph_image=graph_image)

# ฟังก์ชันสำหรับลบโหนด
def delete_node(graph, node):
    graph.remove_node(node)
    return graph

@app.route('/delete_node', methods=['POST'])
def delete_node_route():
    node_to_delete = request.form['node_to_delete']
    global G
    G = delete_node(G, node_to_delete)
    graph_image = generate_graph_image(G)
    return render_template('index.html', graph_image=graph_image)

# ฟังก์ชันสำหรับลบเส้นเชื่อม
def delete_edge(start_node, end_node):
    if G.has_edge(start_node, end_node):
        G.remove_edge(start_node, end_node)


@app.route('/delete_edge', methods=['POST'])
def delete_edge_route():
    try:
        start_node = request.form['from_node']
        end_node = request.form['to_node']
        delete_edge(start_node, end_node)
        graph_image = generate_graph_image(G)
        return render_template('index.html', graph_image=graph_image)
    except KeyError:
        return "Missing required fields", 400

if __name__ == '__main__':
    app.run(debug=True)
