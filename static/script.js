const form = document.querySelector("#todo");

const logout=document.getElementById('logout');

const remove=document.querySelectorAll('.remove');


function data(event) {


    event.preventDefault();

    let task_name = document.getElementById("task_name").value;
    let userTime = new Date().toISOString();



    fetch('/dashboard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            time: userTime,
            task: task_name

        })
    })
    .then(()=>{window.location.reload()})

    
}

function logout_info(event){

    fetch('/logout',
        {
        method:'POST',
        headers:{'content-type':'application/json'},
        body: JSON.stringify({logout:"True"})
        }
    )
    .then(()=>{window.location.reload()})
}

function remove_element(event){

    let row=event.target.closest('tr')
    let taskId = row.dataset.id;

    
    fetch('/dashboard',{
        method:'POST',
        headers:{'content-type':'application/json'},
        body:JSON.stringify({
            task: taskId,
            delete:"True"})
    }) 
    .then(()=>window.location.reload())
}

form.addEventListener("submit", data);
logout.addEventListener("click",logout_info);

remove.forEach((trash)=>{trash.addEventListener("click",remove_element)});