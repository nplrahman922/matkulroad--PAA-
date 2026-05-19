import type { Node, Edge } from '@vue-flow/core';

export const nodes: Node[] = [
  // --- NODES (Kotak Mata Kuliah) ---
  
  // Level 1: Prasyarat Awal (Kiri)
  { id: 'n1', position: { x: 50, y: 20 }, data: { label: 'Aljabar Linier' }, class: 'bg-white border border-gray-300 rounded-lg p-3 shadow-sm text-gray-700' },
  { id: 'n2', position: { x: 50, y: 100 }, data: { label: 'Matematika Diskrit' }, class: 'bg-white border border-gray-300 rounded-lg p-3 shadow-sm text-gray-700' },
  
  // Level 2: Mata Kuliah Inti (Tengah) - Ceritanya ini yang dicari User
  { id: 'n3', position: { x: 250, y: 60 }, data: { label: 'Pengantar AI' }, class: 'bg-blue-50 border-2 border-blue-600 rounded-lg p-3 shadow-md font-bold text-blue-800' },
  
  // Level 3: Mata Kuliah Lanjutan (Kanan)
  { id: 'n4', position: { x: 450, y: 20 }, data: { label: 'Machine Learning' }, class: 'bg-white border border-gray-300 rounded-lg p-3 shadow-sm text-gray-700' },
  { id: 'n5', position: { x: 450, y: 100 }, data: { label: 'Computer Vision' }, class: 'bg-white border border-gray-300 rounded-lg p-3 shadow-sm text-gray-700' },
  
  // Level 4: Mata Kuliah Lanjutan Ekstra (Paling Kanan)
  { id: 'n6', position: { x: 650, y: 20 }, data: { label: 'Deep Learning' }, class: 'bg-white border border-gray-300 rounded-lg p-3 shadow-sm text-gray-700' },
];

export const edges: Edge[] = [
  // --- EDGES (Garis Prasyarat - Siku-siku) ---
  
  // Garis dari prasyarat ke mata kuliah inti (dengan belok siku-siku)
  { id: 'e1-3', source: 'n1', target: 'n3', animated: true, type: 'step', style: { stroke: '#9ca3af', strokeWidth: 2 } },
  { id: 'e2-3', source: 'n2', target: 'n3', animated: true, type: 'step', style: { stroke: '#9ca3af', strokeWidth: 2 } },
  
  // Garis dari mata kuliah inti ke lanjutan (dengan belok siku-siku)
  { id: 'e3-4', source: 'n3', target: 'n4', animated: true, type: 'step', style: { stroke: '#3b82f6', strokeWidth: 2 } },
  { id: 'e3-5', source: 'n3', target: 'n5', animated: true, type: 'step', style: { stroke: '#3b82f6', strokeWidth: 2 } },
  
  // Garis dari lanjutan ke lanjutan ekstra (dengan belok siku-siku)
  { id: 'e4-6', source: 'n4', target: 'n6', animated: true, type: 'step', style: { stroke: '#3b82f6', strokeWidth: 2 } },
];

export const roadmapElements = [...nodes, ...edges];
