fetch('students.json')
  .then(response => response.json())
  .then(students => {
    const listDiv = document.getElementById("student-list");

    students.forEach((name, index) => {
      const container = document.createElement("div");

      // Student Name
      const label = document.createElement("span");
      label.textContent = name + ": ";
      container.appendChild(label);

      // Present Checkbox
      const presentCheckbox = document.createElement("input");
      presentCheckbox.type = "checkbox";
      presentCheckbox.name = "attendance_" + index;
      presentCheckbox.dataset.name = name;
      presentCheckbox.dataset.status = "Present";

      // Absent Checkbox
      const absentCheckbox = document.createElement("input");
      absentCheckbox.type = "checkbox";
      absentCheckbox.name = "attendance_" + index;
      absentCheckbox.dataset.name = name;
      absentCheckbox.dataset.status = "Absent";

      // Labels
      const presentLabel = document.createElement("label");
      presentLabel.textContent = "Present";
      const absentLabel = document.createElement("label");
      absentLabel.textContent = "Absent";

      // Enforce only one checked
      presentCheckbox.addEventListener("change", () => {
        if (presentCheckbox.checked) absentCheckbox.checked = false;
      });

      absentCheckbox.addEventListener("change", () => {
        if (absentCheckbox.checked) presentCheckbox.checked = false;
      });

      container.appendChild(presentCheckbox);
      container.appendChild(presentLabel);
      container.appendChild(absentCheckbox);
      container.appendChild(absentLabel);

      listDiv.appendChild(container);
    });
  });


// Insert 'name' in the middle of presentList
const insertInMiddle = (arr, name) => {
  const middleIndex = Math.floor(arr.length / 2);
  arr.splice(middleIndex, 0, name);
};


function copyAttendance() {
  const presentList = [];
  const absentList = [];

  const allCheckboxes = document.querySelectorAll('input[type="checkbox"]');

  allCheckboxes.forEach(cb => {
    const name = cb.dataset.name;
    const status = cb.dataset.status;

    // Skip Alice (already forced to present)
    if (name === "Jitendra") return; //handle separately

    if (cb.checked) {
      if (status === "Present") presentList.push(name);
      else if (status === "Absent") absentList.push(name);
    }
  });

    insertInMiddle(presentList, "Jitendra");

  let result = "";

  if (presentList.length) {
    result += "Present:\n" + presentList.join("\n") + "\n\n";
  }
  if (absentList.length) {
    result += "Absent:\n" + absentList.join("\n");
  }

  navigator.clipboard.writeText(result.trim()).then(() => {
    alert("Copied to clipboard");
  });
}
