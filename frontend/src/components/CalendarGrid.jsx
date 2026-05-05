import { FiChevronLeft, FiChevronRight } from "react-icons/fi";

function formatDate(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

const MONTH_NAMES = [
  "January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"
];

function buildCalendarDays(year, month) {
  // Use local time for building the calendar grid to avoid UTC shifts
  const first = new Date(year, month - 1, 1);
  const last = new Date(year, month, 0);
  const days = [];
  for (let day = 1; day <= last.getDate(); day += 1) {
    days.push(new Date(year, month - 1, day));
  }
  return { firstWeekday: first.getDay(), days };
}

export default function CalendarGrid({ selectedDate, onSelectDate, notesByDate, currentMonth, onMonthChange }) {
  const parts = (currentMonth || "").split("-");
  const year = parseInt(parts[0], 10) || new Date().getFullYear();
  const month = parseInt(parts[1], 10) || (new Date().getMonth() + 1);
  const { firstWeekday, days } = buildCalendarDays(year, month);

  return (
    <section className="calendar-wrapper">
      <div className="calendar-header">
        <button type="button" className="icon-btn" onClick={() => onMonthChange(-1)}>
          <FiChevronLeft size={20} />
        </button>
        <button type="button" className="icon-btn" onClick={() => onMonthChange(1)}>
          <FiChevronRight size={20} />
        </button>
      </div>
      <div className="calendar-title-centered">
        <h3>{MONTH_NAMES[month - 1]} {year}</h3>
      </div>

      <div className="calendar-grid">
        {Array.from({ length: firstWeekday }).map((_, index) => (
          <div key={`blank-${index}`} className="tile empty" />
        ))}
        {days.map((day) => {
          const key = formatDate(day);
          const isSelected = key === selectedDate;
          const note = notesByDate[key];
          return (
            <button
              key={key}
              type="button"
              className={`tile ${isSelected ? "selected" : ""} ${note ? "has-note" : ""}`}
              onClick={() => onSelectDate(key)}
            >
              <span className="date-number">{day.getDate()}</span>
              {note && <p className="note-preview">{note.content}</p>}
            </button>
          );
        })}
      </div>
    </section>
  );
}
