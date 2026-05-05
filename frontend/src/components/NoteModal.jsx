import { FiEdit2, FiPlus, FiTrash2, FiX } from "react-icons/fi";

export default function NoteModal({
  selectedDate,
  formContent,
  setFormContent,
  existingNote,
  onSave,
  onDelete,
  onClose,
  loading,
}) {
  return (
    <div className="modal-overlay">
      <div className="modal-card">
        <div className="modal-header">
          <h3>Note for {selectedDate}</h3>
          <button type="button" className="icon-button" onClick={onClose}>
            <FiX />
          </button>
        </div>
        <label className="field">
          <span>Note</span>
          <textarea
            rows={5}
            value={formContent}
            onChange={(event) => setFormContent(event.target.value)}
            placeholder="Write your note"
          />
        </label>
        <div className="note-meta">
          <small>Created: {existingNote?.created_at || "---"}</small>
          <small>Last edited: {existingNote?.last_edited_display || "---"}</small>
        </div>
        <div className="modal-actions">
          <button type="button" className="btn primary" onClick={onSave} disabled={loading}>
            {existingNote ? <FiEdit2 /> : <FiPlus />} {existingNote ? "Update" : "Save"}
          </button>
          {existingNote && (
            <button type="button" className="btn danger" onClick={onDelete} disabled={loading}>
              <FiTrash2 /> Delete
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
