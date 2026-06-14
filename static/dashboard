const taskList = document.getElementById("taskList");

const totalTasks = document.getElementById("totalTasks");
const pendingTasks = document.getElementById("pendingTasks");
const progressTasks = document.getElementById("progressTasks");
const completedTasks = document.getElementById("completedTasks");

const completionPercent =
document.getElementById("completionPercent");

const progressRing =
document.querySelector(".progress-ring");

const addTaskBtn =
document.getElementById("addTaskBtn");

const taskTitle =
document.getElementById("taskTitle");

const refreshBtn =
document.getElementById("refreshBtn");


// =======================
// LOAD TASKS
// =======================

async function loadTasks() {

    try {

        const response =
        await fetch("/api/tasks");

        const tasks =
        await response.json();

        renderTasks(tasks);
        updateStats(tasks);

    }

    catch(error) {

        console.error(
            "Error loading tasks:",
            error
        );

    }

}


// =======================
// RENDER TASKS
// =======================

function renderTasks(tasks) {

    taskList.innerHTML = "";

    if(tasks.length === 0){

        taskList.innerHTML = `
        <div class="task-item">
            No tasks available.
        </div>
        `;

        return;
    }

    tasks.forEach(task => {

        const taskElement =
        document.createElement("div");

        taskElement.classList.add("task-item");

        let statusClass = "pending";

        if(task.status === "Completed"){
            statusClass = "completed";
        }

        else if(task.status === "In Progress"){
            statusClass = "progress";
        }

        taskElement.innerHTML = `

        <div class="task-info">

            <div class="task-title">
                ${task.title}
            </div>

        </div>

        <div class="task-actions">

            <select
            onchange="changeStatus(
            ${task.id},
            this.value
            )">

                <option
                value="Pending"
                ${task.status==="Pending" ? "selected" : ""}>
                Pending
                </option>

                <option
                value="In Progress"
                ${task.status==="In Progress" ? "selected" : ""}>
                In Progress
                </option>

                <option
                value="Completed"
                ${task.status==="Completed" ? "selected" : ""}>
                Completed
                </option>

            </select>

            <span class="
            status-badge
            ${statusClass}
            ">
                ${task.status}
            </span>

            <button
            class="action-btn delete-btn"
            onclick="deleteTask(${task.id})">

                Delete

            </button>

        </div>
        `;

        taskList.appendChild(
            taskElement
        );

    });

}


// =======================
// ADD TASK
// =======================

async function addTask() {

    const title =
    taskTitle.value.trim();

    if(title === ""){

        alert(
            "Please enter a task title"
        );

        return;
    }

    await fetch("/api/tasks", {

        method: "POST",

        headers: {
            "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
            title: title
        })

    });

    taskTitle.value = "";

    loadTasks();

}


// =======================
// DELETE TASK
// =======================

async function deleteTask(id){

    const confirmDelete =
    confirm(
        "Delete this task?"
    );

    if(!confirmDelete){
        return;
    }

    await fetch(`/api/tasks/${id}`,{

        method:"DELETE"

    });

    loadTasks();

}


// =======================
// UPDATE STATUS
// =======================

async function changeStatus(
    id,
    status
){

    await fetch(`/api/tasks/${id}`,{

        method:"PUT",

        headers:{
            "Content-Type":
            "application/json"
        },

        body: JSON.stringify({
            status: status
        })

    });

    loadTasks();

}


// =======================
// INITIALIZATION
// =======================

document.addEventListener("DOMContentLoaded", function() {
    loadTasks();
    addTaskBtn.addEventListener("click", addTask);
    refreshBtn.addEventListener("click", loadTasks);
});


// =======================
// UPDATE STATS
// =======================

function updateStats(tasks){

    const total =
    tasks.length;

    const pending =
    tasks.filter(
    t => t.status === "Pending"
    ).length;

    const progress =
    tasks.filter(
    t => t.status === "In Progress"
    ).length;

    const completed =
    tasks.filter(
    t => t.status === "Completed"
    ).length;

    totalTasks.textContent =
    total;

    pendingTasks.textContent =
    pending;

    progressTasks.textContent =
    progress;

    completedTasks.textContent =
    completed;

    let percentage = 0;

    if(total > 0){

        percentage =
        Math.round(
        (completed/total)*100
        );

    }

    completionPercent.textContent =
    percentage + "%";

    const degree =
    percentage * 3.6;

    progressRing.style.background =
    `conic-gradient(
        #6c3bff ${degree}deg,
        #ececff ${degree}deg
    )`;

}


// =======================
// EVENTS
// =======================

addTaskBtn.addEventListener(
    "click",
    addTask
);

refreshBtn.addEventListener(
    "click",
    loadTasks
);

taskTitle.addEventListener(
    "keypress",
    function(e){

        if(e.key === "Enter"){
            addTask();
        }

    }
);


// =======================
// INITIAL LOAD
// =======================

loadTasks();
