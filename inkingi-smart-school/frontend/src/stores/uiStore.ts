import { create } from 'zustand';

interface UIState {
  // Modals
  isClassModalOpen: boolean;
  isEnrollmentModalOpen: boolean;
  isConfirmModalOpen: boolean;
  
  // Modal data
  confirmModalData: {
    title: string;
    message: string;
    onConfirm: () => void;
    onCancel?: () => void;
    confirmText?: string;
    cancelText?: string;
    type?: 'danger' | 'warning' | 'info';
  } | null;

  // Sidebar
  isSidebarOpen: boolean;

  // Actions
  openClassModal: () => void;
  closeClassModal: () => void;
  openEnrollmentModal: () => void;
  closeEnrollmentModal: () => void;
  
  openConfirmModal: (data: UIState['confirmModalData']) => void;
  closeConfirmModal: () => void;
  
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
}

export const useUIStore = create<UIState>((set) => ({
  // Initial state
  isClassModalOpen: false,
  isEnrollmentModalOpen: false,
  isConfirmModalOpen: false,
  confirmModalData: null,
  isSidebarOpen: false,

  // Actions
  openClassModal: () => set({ isClassModalOpen: true }),
  closeClassModal: () => set({ isClassModalOpen: false }),
  
  openEnrollmentModal: () => set({ isEnrollmentModalOpen: true }),
  closeEnrollmentModal: () => set({ isEnrollmentModalOpen: false }),
  
  openConfirmModal: (data) => set({ 
    isConfirmModalOpen: true, 
    confirmModalData: data 
  }),
  closeConfirmModal: () => set({ 
    isConfirmModalOpen: false, 
    confirmModalData: null 
  }),
  
  toggleSidebar: () => set((state) => ({ isSidebarOpen: !state.isSidebarOpen })),
  setSidebarOpen: (open) => set({ isSidebarOpen: open }),
}));