import React from 'react';
import { AlertTriangle, Info, AlertCircle } from 'lucide-react';
import { Modal } from './Modal';
import { Button } from '../ui/Button';
import { useUIStore } from '../../stores/uiStore';

const ConfirmModal: React.FC = () => {
  const { isConfirmModalOpen, confirmModalData, closeConfirmModal } = useUIStore();

  if (!confirmModalData) return null;

  const {
    title,
    message,
    onConfirm,
    onCancel,
    confirmText = 'Confirm',
    cancelText = 'Cancel',
    type = 'info',
  } = confirmModalData;

  const handleConfirm = () => {
    onConfirm();
    closeConfirmModal();
  };

  const handleCancel = () => {
    if (onCancel) onCancel();
    closeConfirmModal();
  };

  const getIcon = () => {
    switch (type) {
      case 'danger':
        return <AlertTriangle className="h-6 w-6 text-red-600" />;
      case 'warning':
        return <AlertCircle className="h-6 w-6 text-yellow-600" />;
      default:
        return <Info className="h-6 w-6 text-blue-600" />;
    }
  };

  const getConfirmButtonVariant = () => {
    switch (type) {
      case 'danger':
        return 'danger' as const;
      case 'warning':
        return 'primary' as const;
      default:
        return 'primary' as const;
    }
  };

  return (
    <Modal
      isOpen={isConfirmModalOpen}
      onClose={closeConfirmModal}
      title={title}
      size="sm"
    >
      <div className="space-y-4">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0">
            {getIcon()}
          </div>
          <div className="flex-1">
            <p className="text-sm text-gray-700">{message}</p>
          </div>
        </div>
        
        <div className="flex space-x-3 justify-end">
          <Button
            variant="ghost"
            onClick={handleCancel}
          >
            {cancelText}
          </Button>
          <Button
            variant={getConfirmButtonVariant()}
            onClick={handleConfirm}
          >
            {confirmText}
          </Button>
        </div>
      </div>
    </Modal>
  );
};

export { ConfirmModal };