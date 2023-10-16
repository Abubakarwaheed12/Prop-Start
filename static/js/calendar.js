// Get the current date
let currentDate = new Date();

// Function to update the displayed date and year
function updateDisplayedDate1() {
  const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
  ];
  document.getElementById("current-date").textContent =
    months[currentDate.getMonth()] + " " + currentDate.getFullYear();
}

// Function to update the selected date
function updateSelectedDate(selectedDate) {
  const selectedDateDisplay = document.getElementById("selected-date");
  selectedDateDisplay.textContent = selectedDate.toDateString();

  const selecteddates = document.getElementById("selecteddate");
  selecteddates.value = selectedDate.toDateString();
  
}

// Function to generate the static calendar dates
function generateCalendarDates1() {
  const datesElement = document.querySelector(".dates");
  datesElement.innerHTML = "";

  // Get the first day of the month
  const firstDayOfMonth = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth(),
    1
  );

  // Get the last day of the month
  const lastDayOfMonth = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth() + 1,
    0
  );

  // Get the starting day of the week for the first day of the month (0 = Sunday, 1 = Monday, ..., 6 = Saturday)
  const startingDayOfWeek = firstDayOfMonth.getDay();

  // Populate the previous month's days (if any)
  const prevMonthLastDay = new Date(
    currentDate.getFullYear(),
    currentDate.getMonth(),
    0
  );
  const prevMonthLastDate = prevMonthLastDay.getDate();

  for (let i = startingDayOfWeek - 1; i >= 0; i--) {
    const prevMonthDate = new Date(
      currentDate.getFullYear(),
      currentDate.getMonth() - 1,
      prevMonthLastDate - i
    );

    const dateItem = document.createElement("div");
    dateItem.className = "date-item previous-month";
    dateItem.textContent = prevMonthDate.getDate();
    dateItem.addEventListener("click", () => {
      updateSelectedDate(prevMonthDate);
      dateItem.classList.add("current-date");
      const dateItems = document.querySelectorAll(".date-item");
      dateItems.forEach((item) => {
        if (item !== dateItem) {
          item.classList.remove("current-date");
        }
      });
    });

    datesElement.appendChild(dateItem);
  }

  // Create the date items for each day in the current month
  for (let i = 1; i <= lastDayOfMonth.getDate(); i++) {
    const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), i);

    const dateItem = document.createElement("div");
    dateItem.className = "date-item";
    dateItem.textContent = i;
    dateItem.addEventListener("click", () => {
      updateSelectedDate(date);
      dateItem.classList.add("current-date");
      const dateItems = document.querySelectorAll(".date-item");
      dateItems.forEach((item) => {
        if (item !== dateItem) {
          item.classList.remove("current-date");
        }
      });
    });

    // Highlight the current date
    if (date.toDateString() === new Date().toDateString()) {
      dateItem.classList.add("current-date");
    }

    datesElement.appendChild(dateItem);
  }
}

// Event listeners for previous and next buttons
document.getElementById("prev-btn").addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() - 1);
  updateDisplayedDate1();
  generateCalendarDates1();
});

document.getElementById("next-btn").addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() + 1);
  updateDisplayedDate1();
  generateCalendarDates1();
});

// Initial setup
updateDisplayedDate1();
generateCalendarDates1();
