<script setup lang="ts">
import Logo from '@/assets/Logo.webp';
import Search from '@/assets/Search.svg';

// Import Vue Flow secara benar
import { VueFlow, useVueFlow, Position } from '@vue-flow/core';
import '@vue-flow/core/dist/style.css';
import '@vue-flow/core/dist/theme-default.css';

import dagre from 'dagre';

// Alias 'nodes' dan 'edges' agar sesuai dengan variabel di bawah
import { nodes as initialNodes, edges as initialEdges } from '@/Roadmapdummy.ts';

// onPaneReady dan fitView dipanggil dari useVueFlow(), BUKAN di-import langsung
const { onPaneReady, fitView } = useVueFlow();

onPaneReady(() => {
  console.log('Pane is ready!');
  fitView({ padding: 0.1 }); 
});

// 1. Inisialisasi Graph
const dagreGraph = new dagre.graphlib.Graph();
dagreGraph.setDefaultEdgeLabel(() => ({}));
dagreGraph.setGraph({ rankdir: 'LR', nodesep: 50, ranksep: 50 });

// 2. DAFTARKAN NODE KE DAGRE 
initialNodes.forEach((node) => {
  dagreGraph.setNode(node.id, { width: 150, height: 50 }); 
});

// 3. DAFTARKAN EDGE KE DAGRE
initialEdges.forEach((edge) => {
  dagreGraph.setEdge(edge.source, edge.target);
});

// 4. SURUH DAGRE MENGHITUNG POSISI
dagre.layout(dagreGraph);

// 5. BARU KITA AMBIL HASILNYA (Map Node)
const nodes = initialNodes.map(node => {
  const nodeWithPosition = dagreGraph.node(node.id); 
  
  return {
    ...node,
    position: {
      x: nodeWithPosition.x,
      y: nodeWithPosition.y
    },
    targetPosition: Position.Left,
    sourcePosition: Position.Right
  };
});

// 6. Gunakan initialEdges langsung (sudah didefinisikan di Roadmapdummy.ts)
const edges = initialEdges;
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
