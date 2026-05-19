<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { VueFlow, useVueFlow, Position } from '@vue-flow/core';
import dagre from 'dagre';
import '@vue-flow/core/dist/style.css';
import '@vue-flow/core/dist/theme-default.css';

// Import aset
import Logo from '@/assets/Logo.webp';
import Search from '@/assets/Search.svg';

// State reaktif untuk data
const searchQuery = ref('');
const nodes = ref<any[]>([]);
const edges = ref<any[]>([]);

const { onPaneReady, fitView } = useVueFlow();

// 1. Fungsi Jembatan: Menghitung layout dengan Dagre
const applyLayout = (apiNodes: any[], apiEdges: any[]) => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({ rankdir: 'LR', nodesep: 50, ranksep: 50 });

  // Daftarkan node ke dagre
  apiNodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: 150, height: 50 });
  });

  // Daftarkan edge ke dagre
  apiEdges.forEach((edge) => {
    dagreGraph.setEdge(edge.source, edge.target);
  });

  // Hitung posisi
  dagre.layout(dagreGraph);

  // Update data nodes dengan posisi baru
  nodes.value = apiNodes.map((node) => {
    const nodeWithPosition = dagreGraph.node(node.id);
    return {
      ...node,
      position: { x: nodeWithPosition.x, y: nodeWithPosition.y },
      targetPosition: Position.Left,
      sourcePosition: Position.Right,
    };
  });

  edges.value = apiEdges;
};

// 2. Fungsi Jembatan: Fetch data dari Backend Python
const handleSearch = async () => {
  try {
    // Pastikan port 5000 sesuai dengan backend Flask-mu
    const response = await fetch(`http://localhost:5000/api/roadmap?target=${searchQuery.value}`);
    if (!response.ok) throw new Error("Gagal memanggil API");
    
    const data = await response.json();
    applyLayout(data.nodes, data.edges);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

onPaneReady(() => {
  console.log('Pane is ready!');
  fitView({ padding: 0.1 });
});

// Load data awal saat komponen terpasang
onMounted(handleSearch);
</script>

<template>
<div class="h-[25vh] w-full flex justify-center">
    <img :src="Logo" class="h-80" /> 
</div>
<div class="h-[50vh] w-full flex items-center justify-center">
    <div class="relative w-full max-w-lg px-4">
            <div class="absolute inset-y-0 left-0 flex items-center pl-8 pointer-events-none">
            <img :src="Search" class="w-5 h-5" alt="search icon" />
        </div>
        <div>
            <input 
                type="search" 
                class="block w-full p-4 pl-12 text-sm text-gray-900 border border-gray-300 rounded-full bg-white focus:ring-blue-500 focus:border-blue-500 shadow-sm outline-none transition-all" 
                placeholder="Cari roadmap matkul kamu..." 
                required 
            />
      
            <button 
                type="submit" 
                class="text-white absolute right-6 bottom-2 bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm px-4 py-2 transition-colors">
                Cari
            </button>
        </div>
    </div>
</div>
<div class="max-w-full h-[75vh] my-5 border mx-20 border-gray-200 rounded-xl overflow-hidden bg-slate-50 relative shadow-inner">
      <VueFlow class="h-full w-full" :nodes="nodes" :edges="edges" />
</div>
<div class="max-w-full h-auto mt-20"></div>
</template>
