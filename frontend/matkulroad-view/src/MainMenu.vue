<script setup lang="ts">
import { ref, onMounted, nextTick, watch } from 'vue';
import { VueFlow, useVueFlow, Position, Handle } from '@vue-flow/core';
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
const hasSearched = ref(false); // Flag untuk melacak apakah pencarian sudah dilakukan

const { onPaneReady, fitView } = useVueFlow();

// 1. Fungsi Jembatan: Menghitung layout dengan Dagre
const applyLayout = (apiNodes: any[], apiEdges: any[]) => {
  const dagreGraph = new dagre.graphlib.Graph();
  dagreGraph.setDefaultEdgeLabel(() => ({}));
  dagreGraph.setGraph({ rankdir: 'LR', nodesep: 80, ranksep: 120 });

  // Daftarkan node ke dagre
  apiNodes.forEach((node) => {
    dagreGraph.setNode(node.id, { width: 180, height: 80 });
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
      type: 'course', // Menggunakan tipe kustom 'course' untuk rendering yang cantik
      position: { x: nodeWithPosition.x, y: nodeWithPosition.y },
      targetPosition: Position.Left,
      sourcePosition: Position.Right,
    };
  });

  // Percantik edge/garis penghubung
  edges.value = apiEdges.map((edge) => ({
    ...edge,
    type: 'smoothstep',
    animated: true,
    style: { stroke: '#3b82f6', strokeWidth: 2 },
  }));
};

// 2. Fungsi Jembatan: Fetch data dari Backend Python
const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    // Jika kolom pencarian kosong, sembunyikan grafik dan kosongkan data
    nodes.value = [];
    edges.value = [];
    hasSearched.value = false;
    return;
  }

  try {
    // Pastikan port 5000 sesuai dengan backend Flask-mu
    const response = await fetch(`http://localhost:5000/api/roadmap?target=${searchQuery.value}`);
    if (!response.ok) throw new Error("Gagal memanggil API");
    
    const data = await response.json();
    applyLayout(data.nodes, data.edges);
    hasSearched.value = true; // Tandai bahwa pencarian telah berhasil
    
    // Fit view agar grafik pas di layar setelah di-render
    await nextTick();
    setTimeout(() => {
      fitView({ padding: 0.15 });
    }, 50);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

// Reset otomatis saat input pencarian kosong
watch(searchQuery, (newVal) => {
  if (newVal === '') {
    handleSearch();
  }
});

onPaneReady(() => {
  console.log('Pane is ready!');
  fitView({ padding: 0.15 });
});

// Awalnya tidak menampilkan apa-apa, graf hanya muncul setelah dicari
// Jadi onMounted(handleSearch) sengaja dihapus.
</script>

<template>
<div :class="[hasSearched ? 'h-[12vh]' : 'h-[25vh]', 'w-full flex justify-center items-center transition-all duration-500 ease-in-out mt-4']">
    <img :src="Logo" :class="[hasSearched ? 'h-36' : 'h-80', 'transition-all duration-500 ease-in-out object-contain']" /> 
</div>
<div :class="[hasSearched ? 'h-[12vh]' : 'h-[30vh]', 'w-full flex items-center justify-center transition-all duration-500 ease-in-out']">
    <form @submit.prevent="handleSearch" class="relative w-full max-w-lg px-4">
        <div class="absolute inset-y-0 left-0 flex items-center pl-8 pointer-events-none">
            <img :src="Search" class="w-5 h-5" alt="search icon" />
        </div>
        <div>
            <input 
                v-model="searchQuery"
                type="search" 
                class="block w-full p-4 pl-12 pr-20 text-sm text-gray-900 border border-gray-300 rounded-full bg-white focus:ring-blue-500 focus:border-blue-500 shadow-sm outline-none transition-all" 
                placeholder="Cari nama atau kode matkul kamu..." 
            />
      
            <button 
                type="submit" 
                class="text-white absolute right-6 bottom-2 bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-full text-sm px-4 py-2 transition-colors cursor-pointer">
                Cari
            </button>
        </div>
    </form>
</div>

<!-- Tampilan Awal sebelum pencarian dilakukan -->
<div v-if="!hasSearched" class="max-w-full my-5 border mx-20 border-gray-200 rounded-xl bg-white p-12 text-center shadow-sm flex flex-col items-center justify-center min-h-[40vh] transition-all duration-500">
    <div class="bg-blue-50 text-blue-600 p-4 rounded-full mb-4 animate-bounce">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
        </svg>
    </div>
    <h3 class="text-lg font-bold text-gray-800 mb-1">Cari Roadmap Mata Kuliah</h3>
    <p class="text-sm text-gray-500 max-w-md">Masukkan nama atau kode mata kuliah (misalnya: "Struktur Data" atau "MK4") pada kolom pencarian di atas untuk melihat jalur prasyarat kuliah dari awal.</p>
</div>

<!-- Tampilan jika data pencarian tidak ditemukan -->
<div v-else-if="nodes.length === 0" class="max-w-full my-5 border mx-20 border-gray-200 rounded-xl bg-white p-12 text-center shadow-sm flex flex-col items-center justify-center min-h-[40vh] transition-all duration-500">
    <div class="bg-red-50 text-red-500 p-4 rounded-full mb-4">
        <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
    </div>
    <h3 class="text-lg font-bold text-gray-800 mb-1">Mata Kuliah Tidak Ditemukan</h3>
    <p class="text-sm text-gray-500 max-w-md">Tidak ada mata kuliah yang cocok dengan kata kunci "{{ searchQuery }}". Silakan coba dengan kode atau nama mata kuliah lain.</p>
</div>

<!-- Tampilan grafik Vue Flow jika data ditemukan -->
<div v-else class="max-w-full h-[70vh] my-5 border mx-20 border-gray-200 rounded-xl overflow-hidden bg-slate-50 relative shadow-inner transition-all duration-500">
      <VueFlow class="h-full w-full" :nodes="nodes" :edges="edges">
        <!-- Render kustom untuk node mata kuliah (type="course") -->
        <template #node-course="{ data, id }">
          <div 
            :class="[
              'relative px-4 py-3 rounded-xl border-2 transition-all duration-300 min-w-[180px] text-left shadow-sm',
              searchQuery && (data.label.toLowerCase().includes(searchQuery.toLowerCase()) || id.toLowerCase().includes(searchQuery.toLowerCase()))
                ? 'border-blue-500 bg-blue-50/95 shadow-md shadow-blue-200/50 scale-105 z-50 ring-4 ring-blue-100'
                : 'border-gray-200 bg-white hover:border-gray-300 hover:shadow-md'
            ]"
          >
            <!-- Slot untuk garis masuk (target) -->
            <Handle type="target" :position="Position.Left" class="!bg-blue-500 !w-2 !h-2" />
            
            <div class="text-[10px] text-blue-600 font-bold uppercase tracking-wider mb-1">{{ id }}</div>
            <div class="text-sm font-bold text-gray-800 leading-snug min-h-[36px] flex items-center">{{ data.label }}</div>
            
            <div class="flex items-center justify-between mt-2 pt-2 border-t border-gray-100 text-[10px] text-gray-500 font-semibold">
              <span>📚 {{ data.sks }} SKS</span>
              <span>🎓 Sem {{ data.semester }}</span>
            </div>
            
            <!-- Slot untuk garis keluar (source) -->
            <Handle type="source" :position="Position.Right" class="!bg-blue-500 !w-2 !h-2" />
          </div>
        </template>
      </VueFlow>
</div>
<div class="max-w-full h-auto mt-20"></div>
</template>
