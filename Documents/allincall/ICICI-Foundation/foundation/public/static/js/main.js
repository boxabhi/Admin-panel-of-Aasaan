/*****************************/
// Global things here

var csrf = document.getElementById('csrf').value
var link_for_sourcing_file = '/media/sample/sourcing.xlsx'
var link_for_followup_file = '/media/sample/followups.xlsx'
var link_for_enollment_file = '/media/sample/enrollment.xlsx'


/*****************************/


function clearFileInput(id) {
    var oldInput = document.getElementById(id);
    var newInput = document.createElement("input");
    newInput.type = "file";
    newInput.id = oldInput.id;
    newInput.name = oldInput.name;
    newInput.className = oldInput.className;
    newInput.style.cssText = oldInput.style.cssText;
    oldInput.parentNode.replaceChild(newInput, oldInput);
}


function signOut() {
    var auth2 = gapi.auth2.getAuthInstance();
    auth2.signOut().then(function () {
        console.log('User signed out.');
    });
}

function onSignIn(googleUser) {
    var profile = googleUser.getBasicProfile();
    var email = profile.getEmail();
    var loggedIn = localStorage.getItem('loggedIn')
    console.log(loggedIn)
    if (loggedIn == null) {
        console.log("ss")
        var data = {
            'email': profile.getEmail(),
            'id': profile.getId(),
            'name': profile.getName(),
            'img': profile.getImageUrl()
        }

        localStorage.setItem('loggedIn', true)

        fetch('/login/?type=google', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },

                body: JSON.stringify(data)
            }).then(result => result.json())
            .then(response => {
                console.log(response)
                if (response.status_code == 200) {
                    tata.success('Success', response.message)
                    setTimeout(() => {
                        window.location.reload()
                    }, 500)
                } else {
                    tata.error('Error', response.message)
                }

            }).catch(error => {
                console.log(error)
            })

    }
}

function login() {
    var username = document.querySelector('#username').value
    var password = document.querySelector('#password').value
    if (!username && !password) {
        tata.error("Error", "You must enter both username & password", {
            'position': 'tm'
        })
    } else {

        var data = {
            'username': username,
            'password': password
        }
        fetch('/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },
                body: JSON.stringify(data)
            }).then(result => result.json())
            .then(response => {
                console.log(response)
                if (response.status_code == 200) {
                    tata.success('Success', response.message)
                    setTimeout(() => {
                        window.location.href = '/dashboard'
                    }, 1000)
                } else {
                    // tata.error('Error', response.message)
                    setTimeout(() => {
                        window.location.href = '/dashboard'

                    }, 1000)
                }

            })

    }

}



function show_upload() {
    var show_upload_box = document.querySelector('#show_upload_box')
    var options = document.querySelector('#options')
    var source = document.querySelector('#source')
    var form_button = document.querySelector('#form_button')
    var followups = document.querySelector('#followups')
    var enrollments = document.querySelector('#enrollments')
    var donwload_file_btn = document.querySelector('#donwload_file_btn')

    if (options.value == 1) {
        show_upload_box.style.display = "block"
        source.style.display = "block"
        followups.style.display = "none"
        enrollments.style.display = "none"

        form_button.onclick = uploadSourcingFile
        donwload_file_btn.href = link_for_sourcing_file
    } else if (options.value == 2) {
        show_upload_box.style.display = "block"
        source.style.display = "none"
        followups.style.display = "block"
        enrollments.style.display = "none"
        form_button.onclick = uploadFollowUpFile
        donwload_file_btn.href = link_for_followup_file
    } else if (options.value == 3) {
        show_upload_box.style.display = "block"

        source.style.display = "none"
        followups.style.display = "none"
        enrollments.style.display = "block"
        form_button.onclick = uploadEnrollMentFile
        donwload_file_btn.href = link_for_enollment_file

    } else {
        show_upload_box.style.display = "none"
        source.style.display = "none"
        followups.style.display = "none"
        enrollments.style.display = "none"
        donwload_file_btn.style.display = "none"

    }
}


function showLoadingButton(id, text) {
    document.getElementById(id).innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
        <span class="sr-only">${text}...</span>`
}

function showOriginalButton(id, text) {
    document.getElementById(id).innerHTML = `${text}`
}


async function uploadSourcingFile() {
    showLoadingButton('form_button', 'Loading')

    var fileupload = document.getElementById('fileupload')

    let formData = new FormData();
    formData.append("excel_file", fileupload.files[0]);
    formData.append('csrfmiddlewaretoken', csrf);
    await fetch('/api/reports/source/?excel_file', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData

        }).then(response => response.json())
        .then(result => {
            clearFileInput('fileupload')
            console.log(result)

            if (result.status_code == 200) {
                // document.getElementById('errors').style.display = 'block'
                // document.getElementById('errors').innerHTML = result.html
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            } else {
                tata.error('Error', `${result.message}`, {
                    'position': 'tr'
                })
                if (result.errors <= 0) {
                    showOriginalButton('form_button', 'Upload')
                    return;
                }

                var errors = result.errors
                var html = `<table class="table table-striped"><thead><tr>
                <th scope="col">#</th>
                <th scope="col">Error</th>
              </tr>
            </thead>
            <tbody>`

                for (var i = 0; i < errors.length; i++) {
                    html += `  <tr>
            <th scope="row">${i+1}</th>
            <td>${errors[i]}</td>
          </tr>`
                }
                html += ` </tbody></table>`
                document.getElementById('errors').innerHTML = html
                $('#staticBackdrop').modal('show')

            }

            setTimeout(() => {
                showOriginalButton('form_button', 'Upload')
            }, 500)


        })

}


async function uploadFollowUpFile() {
    showLoadingButton('form_button', 'Loading')

    var fileupload = document.getElementById('fileupload')

    let formData = new FormData();
    formData.append("excel_file", fileupload.files[0]);
    formData.append('csrfmiddlewaretoken', csrf);
    await fetch('/api/reports/followup/?excel_file', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData
        }).then(response => response.json())
        .then(result => {
            clearFileInput('fileupload')
            console.log(result)

            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()

                }, 1500)

            } else {
                tata.error('Error', `${result.message}`, {
                    'position': 'tr'
                })
                if (result.errors <= 0) {
                    showOriginalButton('form_button', 'Upload')
                    return;
                }

                var errors = result.errors
                var html = `<table class="table table-striped"><thead><tr>
                <th scope="col">#</th>
                <th scope="col">Error</th>
              </tr>
            </thead>
            <tbody>`

                for (var i = 0; i < errors.length; i++) {
                    html += `  <tr>
            <th scope="row">${i+1}</th>
            <td>${errors[i]}</td>
          </tr>`
                }
                html += ` </tbody></table>`
                console.log(html)
                document.getElementById('errors').innerHTML = html
                $('#staticBackdrop').modal('show')

            }

            setTimeout(() => {
                showOriginalButton('form_button', 'Upload')
            }, 500)


        })

}

async function uploadEnrollMentFile() {
    showLoadingButton('form_button', 'Loading')
    var fileupload = document.getElementById('fileupload')

    let formData = new FormData();
    formData.append("excel_file", fileupload.files[0]);
    formData.append('csrfmiddlewaretoken', csrf);
    await fetch('/api/reports/enrollment/', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData
        }).then(response => response.json())
        .then(result => {
            clearFileInput('fileupload')
            console.log(result)

            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()

                }, 1500)

            } else {
                tata.error('Error', `${result.message}`, {
                    'position': 'tr'
                })
                if (result.errors <= 0) {
                    showOriginalButton('form_button', 'Upload')
                    return;
                }

                var errors = result.errors
                var html = `<table class="table table-striped"><thead><tr>
                <th scope="col">#</th>
                <th scope="col">Error</th>
              </tr>
            </thead>
            <tbody>`

                for (var i = 0; i < errors.length; i++) {
                    html += `  <tr>
            <th scope="row">${i+1}</th>
            <td>${errors[i]}</td>
          </tr>`
                }
                html += ` </tbody></table>`
                console.log(html)
                document.getElementById('errors').innerHTML = html
                $('#staticBackdrop').modal('show')

            }

            setTimeout(() => {
                showOriginalButton('form_button', 'Upload')
            }, 500)


        })


}


function trigger(id, option) {

    fetch(`/api/reports/trigger/?id=${id}&option=${option}`)
        .then(response => response.json())
        .then(result => {
            if (result.status_code == 200) {
                tata.success("Success", result.message, {
                    'position': 'tm'
                })
                setTimeout(() => {
                    window.location.reload()
                }, 1500)
            } else {
                tata.error("Error", result.message, {
                    'position': 'tm'
                })

            }
        })
}


function sendSMS(id, option) {

    fetch(`/api/reports/send_sms?id=${id}&option=${option}`)
        .then(response => response.json())
        .then(result => {
            if (result.status_code == 200) {
                tata.success("Success", result.message, {
                    'position': 'tm'
                })

            } else {
                tata.error("Error", result.message, {
                    'position': 'tm'
                })

            }
        })
}

function refresh(id, option) {
    fetch(`/api/reports/refresh?id=${id}&option=${option}`)
        .then(response => response.json())
        .then(result => {
            if (result.status_code == 200) {
                tata.success("Success", result.message, {
                    'position': 'tm'
                })
                setTimeout(() => {
                    window.location.reload()
                }, 2000)

            } else {
                tata.error("Error", result.message, {
                    'position': 'tm'
                })

            }
        })
}

function getErrors(id, option) {
    fetch(`/api/reports/get-errors/?id=${id}&option=${option}`)
        .then(response => response.json())
        .then(result => {

            if ((result.errors).length <= 0) {
                tata.warn('Message', 'No errors found', {
                    'position': 'tm'
                })
                return;
            }

            var errors = result.errors
            var html = `<table class="table table-striped"><thead><tr>
            <th scope="col">#</th>
            <th scope="col">Error</th>
          </tr>
        </thead>
        <tbody>`

            for (var i = 0; i < errors.length; i++) {
                html += `  <tr>
        <th scope="row">${i+1}</th>
        <td>${errors[i]}</td>
      </tr>`
            }
            // html += ` </tbody></table>`
            console.log(html)
            document.getElementById('messages').innerHTML = html
            $('#messagesModal').modal('show')


        })
}


function remove(id, option) {

    fetch(`/api/reports/remove?id=${id}&option=${option}`)
        .then(response => response.json())
        .then(result => {
            console.log(result)
            if (result.status_code == 200) {
                tata.success("Success", result.message, {
                    'position': 'tm'
                })
                setTimeout(() => {
                    window.location.reload()

                }, 2000)

            } else {
                tata.error("Error", result.message, {
                    'position': 'tm'
                })

            }
        })

}



function updateProfile() {
    var first_name = document.getElementById('first_name').value
    var last_name = document.getElementById('last_name').value
    var emp_id = document.getElementById('emp_id').value
    var mobile = document.getElementById('mobile').value
    var address = document.getElementById('address').value
    var dob = document.getElementById('dob').value

    var data = {
        'first_name': first_name,
        'last_name': last_name,
        'emp_id': emp_id,
        'mobile': mobile,
        'address': address,
        'csrfmiddlewaretoken': csrf,
        'X-CSRFToken': csrf,

    }

    console.log(data)

    fetch('/accounts/update/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {
            if (result.status_code == 200) {
                tata.success('Success', result.message, {
                    'position': 'tm'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)
            } else {
                tata.error('Error', result.message, {
                    'position': 'tm'
                })
                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            }
            console.log(result)
        })


}




function logout() {
    signOut();
    fetch('/logout')
        .then(res => res.json())
        .then(result => {
            console.log(result)
            localStorage.removeItem('loggedIn')
            window.location.replace('/')
        })



}




$(document).ready(function () {
    $('#table_sourcing').DataTable({
        columnDefs: [{
            orderable: false,
            className: 'select-checkbox',
            targets: 0,

        }],
        select: {
            style: 'os',
            selector: 'td:first-child'
        },
        order: [
            [1, 'asc']
        ],
        buttons: [{
            text: 'Get selected data',
            action: function () {
                var count = table.rows({
                    selected: true
                }).count();
                events.prepend('<div>' + count + ' row(s) selected</div>');
            }
        }],
    });
    $('.dataTables_length').addClass('bs-select');
});



$(document).ready(function () {
    $('#table_enrollments').DataTable({
        // columnDefs: [{
        //     orderable: false,
        //     className: 'select-checkbox',
        //     targets: 0,

        // }],
        // select: {
        //     style: 'os',
        //     selector: 'td:first-child'
        // },
        // order: [
        //     [1, 'asc']
        // ],
        // buttons: [{
        //     text: 'Get selected data',
        //     action: function () {
        //         var count = table.rows({
        //             selected: true
        //         }).count();
        //         events.prepend('<div>' + count + ' row(s) selected</div>');
        //     }
        // }],
    });
    $('.dataTables_length').addClass('bs-select');
});


$(document).ready(function () {
    $('#table_followups').DataTable({
        columnDefs: [{
            orderable: false,
            className: 'select-checkbox',
            targets: 0,

        }],
        select: {
            style: 'os',
            selector: 'td:first-child'
        },
        order: [
            [1, 'asc']
        ],
        buttons: [{
            text: 'Get selected data',
            action: function () {
                var count = table.rows({
                    selected: true
                }).count();
                events.prepend('<div>' + count + ' row(s) selected</div>');
            }
        }],
    });
    $('.dataTables_length').addClass('bs-select');
});


function check(option) {
    var pk_list = []
    var selected_option = document.getElementById('selected_option')



    if (option == 1) {
        var table = $('#table_enrollments').DataTable()
        var count = table.rows({
            selected: true
        })
        var index = count[0]
        for (var i = 0; i < index.length; i++) {
            var data = table.row(index[i]).data();
            console.log(data)
            pk_list.push(data[8])
        }
    } else if (option == 2) {
        var table = $('#table_sourcing').DataTable()
        var count = table.rows({
            selected: true
        })
        var index = count[0]
        for (var i = 0; i < index.length; i++) {
            var data = table.row(index[i]).data();
            console.log(data)
            pk_list.push(data[10])
        }
    } else if (option == 3) {
        var table = $('#table_followups').DataTable()
        var count = table.rows({
            selected: true
        })
        var index = count[0]
        console.log(count)

        for (var i = 0; i < index.length; i++) {
            var data = table.row(index[i]).data();
            console.log(data)
            pk_list.push(data[9])
        }
    }





    var data = {
        'pk_lists': pk_list,
        'selected_option': selected_option.value,
        'option': option
    }

    console.log(data)

    fetch(`/api/reports/send-sms-email-to-pk/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(result => result.json())
        .then(response => {

            if (response.status_code == 200) {
                tata.success('Success', response.message, {
                    'position': 'tm'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1000)

            } else {
                tata.error('Error', response.message, {
                    'position': 'tm'
                })
            }

        })



}


function show_application_data(id) {

    fetch(`/api/reports/application-id/?id=${id}`)
        .then(response => response.json())
        .then(result => {
            var data = result.data
            var html = `<table class="table table-striped" id="table_id"><thead><tr>
        <th scope="col">#</th>
        <th scope="col">Applicaton ID</th>
        <th scope="col">DOB</th>
        <th scope="col">EMAIL</th>
        </tr>
        </thead>
        <tbody>`

            for (var i = 0; i < data.length; i++) {
                html += `  <tr>
                        <th scope="row">${i+1}</th>
                        <td>${data[i].id}</td>
                        <td>${data[i].dob}</td>
                        <td>${data[i].email}</td>
                            </tr>`
            }
            html += ` </tbody></table>`
            document.getElementById('messages').innerHTML = html
            window.$('#table_id').DataTable();
            $('#messagesModal').modal('show')

        })

}



function getBatches() {
    var element = document.getElementById('show_batches');

    var emp_id = document.getElementById('emp_id')

    if (emp_id.value == '') {
        tata.error('Error', 'Please fill Emp id')
        return;
    }


    window.location.href = `${window.location.href}?emp_id=${emp_id.value}`



    var get_batches = document.getElementById('get_batches')

    showLoadingButton('get_batches', 'Getting batches')

    setTimeout(() => {
        showOriginalButton('get_batches', 'Get Batches')
    }, 2000)


    if (emp_id.value == '') {
        tata.error('Please enter Emp id', {
            'position': 'tm'
        })
        return
    }

    fetch(`/api/reports/get-batch-details/?emp_id=${emp_id.value}`).then(result => result.json())
        .then(response => {

            console.log(response)
            tata.success('Success', 'Fetched batches successfully!')
            var html = ''
            for (var i = 0; i < response.data.length; i++) {

                if (i == 0) {
                    document.getElementById('small_text').innerText = `Emp Id : ${response.data[i].EmpId} , Emp Name : ${response.data[i].EmpName}`
                }

                var store_html = ''
                if (response.data[i].is_stored) {
                    store_html = '<i class="far fa-check-square text-success"></i>'
                } else {
                    store_html = '<i class="fas fa-times text-danger"></i>'
                }


                html += ` <tr>
            <td>
            <input type="checkbox" id="checkboxes" data-batchStartDate="${response.data[i].BatchStartDate}" data-batch="${response.data[i].BatchId}" data-emp_id="${response.data[i].EmpId}" >
            </td>
            <td>${i+1}</td>
            <td>${response.data[i].BatchId}</td>
            <td>${response.data[i].BatchName}</td>
          
            <td>${response.data[i].ISAName}</td>
            <td>${response.data[i].Course}</td>
            <td>${response.data[i].BatchStartDate}</td>
            <td>${response.data[i].BatchEndDate}</td>
            <td>${response.data[i].students}</td>

            

        
         <td class="text-center">   ${store_html} </td>
            <td>
            <a href="/api/reports/students/${response.data[i].BatchId}" target="_blank"
             class="btn btn-primary"
            >View</button>
            </td>
            `
            }

            //  console.log(html)

            element.innerHTML = html


        })
}


function getSelectedItems() {
    var nodes = document.querySelectorAll('#checkboxes')




}


function checkBoxStatus() {
    var checkbox = document.getElementById('checkbox')
    if (checkbox.checked == true) {
        var nodes = document.querySelectorAll('#checkboxes')
        for (var i = 0; i < nodes.length; i++) {
            nodes[i].checked = true
        }
    } else {
        var nodes = document.querySelectorAll('#checkboxes')
        for (var i = 0; i < nodes.length; i++) {
            nodes[i].checked = false
        }
    }
}

function increaseProgress(value, count = 0, total_count = -1) {
    var progress = document.querySelector('.progress-bar')

    if (total_count != -1) {
        var current_count_in_text = document.querySelector('#current_count_in_text')
        current_count_in_text.innerText = `${count} out of ${total_count} imported - (${value} % - Completed)`
        //document.getElementById('progress-bar').textContent = value + '%'
        if (total_count == count) {
            setTimeout(() => {
                window.location.reload()
            }, 1500)
        }

    }






    progress.style.width = value + "%"
}




function second() {
    let s = new WebSocket(`ws://localhost:8000/ws/batches-import/`)
    s.onopen = function (e) {
        console.log('Second connection')
    }
    s.onmessage = function (e) {
        var data = JSON.parse(e.data)
        console.log(data)
    };
    s.onclose = function (e) {
        console.log('Connection closed');
    };
}

function runSocket(id) {
    let socket = new WebSocket(`ws://localhost:8000/ws/pizza/`);
    socket.onopen = function (e) {
        console.log('Connection established');
    };

    socket.onmessage = function (e) {
        var data = JSON.parse(e.data)
        var value = data.payload.count
        var current = data.payload.current
        console.log(data)

        var percentComplete = current / value

        var completed = parseInt(percentComplete * 100)

        increaseProgress(completed, current, value)
    };
    socket.onclose = function (e) {
        console.log('Connection closed');
    };
}


runSocket(1)

//$('#showProgress').modal('show');



function importBatches() {
    var nodes = document.querySelectorAll('#checkboxes')
    var pk_list = []
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].checked) {
            pk_list.push({
                'batch': nodes[i].dataset.batch,
                'emp_id': nodes[i].dataset.emp_id,
                'batch_start_date': nodes[i].dataset.batchstartdate,
                'batch_end_date': nodes[i].dataset.batchenddate

            })
        }
    }



    if (pk_list.length > 0) {

        $('#showProgress').modal('show');


        fetch(`/api/reports/store-batch-list/`, {
                method: 'POST',
                headers: {
                    'Authorization': 'Basic ' + btoa('admin:123'),
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },
                body: JSON.stringify({
                    'data': JSON.stringify(pk_list)
                })
            }).then(result => result.json())
            .then(response => {

                // $('#showProgress').modal('show');

                // if (response.status_code == 200) {
                //     tata.success('Success', response.message)
                //     setTimeout(() => {
                //         window.location.reload()
                //     }, 2000)
                // }
                console.log(response)
            })
    }




    console.log(pk_list)
}

//$('#showProgress').modal('show');

function importTrainees() {

    var nodes = document.querySelectorAll('#checkboxes')
    var pk_list = []
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].checked) {
            pk_list.push({
                'trainee_id': nodes[i].dataset.trainee_id,
                'trainee_id': nodes[i].dataset.trainee_id,
                'trainee_name': nodes[i].dataset.trainee_name,
                'batch_id': nodes[i].dataset.batch_id,
                'applicant_id': nodes[i].dataset.application_id,

            })

        }
    }

    if (pk_list.length > 0) {

        fetch(`/api/reports/store-trainee-list/`, {
                method: 'POST',
                headers: {
                    'Authorization': 'Basic ' + btoa('admin:123'),
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },
                body: JSON.stringify({
                    'data': JSON.stringify(pk_list)
                })
            }).then(result => result.json())
            .then(response => {
                if (response.status_code == 200) {
                    tata.success('Success', response.message)
                    setTimeout(() => {
                        window.location.reload()
                    }, 2000)
                }

            })
    }


}



function issueCertificates() {
    var nodes = document.querySelectorAll('#checkboxes')
    var pk_list = []
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].checked) {
            pk_list.push({
                'trainee_id': nodes[i].dataset.trainee_id,
                'trainee_id': nodes[i].dataset.trainee_id,
                'trainee_name': nodes[i].dataset.trainee_name,
                'batch_id': nodes[i].dataset.trainee_name,
                'applicant_id': nodes[i].dataset.application_id,

            })

        }
    }

    var template_id = document.getElementById('template_id').value
    var custom_course = document.getElementById('custom_course').value
    var isa_id = document.getElementById('isa_id').value
    var start_date = document.getElementById('start_date').value
    var end_date = document.getElementById('end_date').value


    var data = {
        'pk_lists': pk_list,
        'template_id': template_id,
        'custom_course': custom_course,
        'isa_id': isa_id,
        'start_date': start_date,
        'end_date': end_date
    }

    if (pk_list.length > 0) {

        fetch(`/api/reports/issue-trainee-ceritficate/`, {
                method: 'POST',
                headers: {
                    'Authorization': 'Basic ' + btoa('admin:123'),
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrf,
                },
                body: JSON.stringify({
                    'data': JSON.stringify(data)
                })
            }).then(result => result.json())
            .then(response => {
                if (response.status_code == 200) {
                    tata.success('Success', response.message)
                    setTimeout(() => {
                        window.location.reload()
                    }, 2000)
                } else {
                    tata.success('Success', response.message)

                }

            })
    }

}



function deleteUser() {
    var nodes = document.querySelectorAll('#checkboxes')

    var pk_lists = []
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].checked) {
            pk_lists.push(nodes[i].dataset.profile_id)
        }

    }

    if (pk_lists.length == 0) {
        tata.error('Error', 'Please select some users');
        return;
    }

    console.log(pk_lists)


    fetch(`/accounts/delete/`, {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('admin:123'),
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify({
                'data': {
                    'pk_lists': pk_lists
                }
            })
        })
        .then(result => result.json())
        .then(response => {
            if (response.status_code == 200) {
                tata.success('Success', response.message)

                setTimeout(() => {
                    window.location.reload()
                }, 2000)

            } else {
                tata.error(response.message)
            }
        })

}


function updateUserModal(id) {

    fetch(`/accounts/user?id=${id}`)
        .then(result => result.json())
        .then(response => {


        })



    $('#exampleModal').modal('show')


}

function showPermissions() {
    var user_type = document.getElementById('user_type').value

    if (user_type == 1) {
        document.getElementById('permissions').style.display = 'none'
    } else {
        document.getElementById('permissions').style.display = ''

    }

}

function getUser(id) {

    var email_id = document.getElementById('email_id')
    var emp_id = document.getElementById('emp_id')
    var user_type = document.getElementById('user_type')
    var permission = $('#permission').val()


    fetch(`/accounts/user/?id=${id}`)
        .then(result => result.json())
        .then(response => {
            console.log(response)

            if (response.status_code == 200) {
                email_id.value = response.data.email_id
                emp_id.value = response.data.emp_id
                $('#exampleModal').modal('show')
            } else {
                tata.error(response.message)
            }


        })



}

function createUser() {
    var email_id = document.getElementById('email_id1')
    var emp_id = document.getElementById('emp_id1')
    var user_type = document.getElementById('user_type1')
    var address = document.getElementById('address1')
    var permission = $('#permission1').val()
    var first_name = document.getElementById('first_name1')
    var last_name = document.getElementById('last_name1')

    console.log(permission)

    fetch(`/accounts/create-user/`, {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('admin:123'),
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify({
                'data': JSON.stringify({
                    'email_id': email_id.value,
                    'user_type': user_type.value,
                    'permission': permission.value,
                    'emp_id': emp_id.value,
                    'first_name': first_name.value,
                    'last_name': last_name.value,
                    'address': address.value
                })
            })
        }).then(result => result.json())
        .then(response => {
            if (response.status_code == 200) {
                tata.success('Success', response.message)
                setTimeout(() => {
                    window.location.reload()
                }, 2000)
            } else {
                tata.error('Error', response.message)
            }

        })
}

function updateUser() {
    var email_id = document.getElementById('email_id')
    var emp_id = document.getElementById('emp_id')
    var user_type = document.getElementById('user_type')
    var permission = $('#permission').val()


    console.log(permission)

    fetch(`/accounts/user/`, {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('admin:123'),
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify({
                'data': JSON.stringify({
                    'email_id': email_id.value,
                    'user_type': user_type.value,
                    'permission': permission
                })
            })
        }).then(result => result.json())
        .then(response => {
            if (response.status_code == 200) {
                tata.success('Success', response.message)
                setTimeout(() => {
                    window.location.reload()
                }, 2000)
            } else {
                tata.error('Error', response.message)
            }

        })
}





async function uploadUsers() {
    showLoadingButton('form_button', 'Loading')
    var fileupload = document.getElementById('fileupload')

    let formData = new FormData();
    formData.append("excel_file", fileupload.files[0]);
    formData.append('csrfmiddlewaretoken', csrf);

    var file_size = (fileupload.files[0].size)

    $('#uploadProgress').modal('show');

    //tata.warn('Upload' , 'Your file is getting uploaded'  , {'position': 'tm'})

    const xhr = new XMLHttpRequest()
    xhr.open('POST', '')
    xhr.upload.addEventListener("progress", e => {
        var file_uploded = e.loaded
        var percentComplete = file_uploded / file_size

        var completed = parseInt(percentComplete * 100)
        if (completed > 100) {
            completed = 100
            $('#uploadProgress').modal('hide');

        }

        increaseProgress(completed)
        console.log(parseInt(percentComplete * 100))
        //console.log(e)
    })
    xhr.setRequestHeader("Content-Type", "multipart/form-data")
    xhr.send((formData))

    await fetch('/api/reports/upload-users/', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData
        }).then(response => response.json())
        .then(result => {
            clearFileInput('fileupload')
            console.log(result)

            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })


                $('#uploadProgress').modal('hide');

                // setTimeout(() => {
                //     window.location.reload()

                // }, 1500)

            } else {
                tata.error('Error', `${result.message}`, {
                    'position': 'tr'
                })
                if (result.errors <= 0) {
                    showOriginalButton('form_button', 'Upload')
                    return;
                }
                $('#uploadProgress').modal('hide');


                var errors = result.errors
                var html = `<table class="table table-striped"><thead><tr>
                <th scope="col">#</th>
                <th scope="col">Error</th>
              </tr>
            </thead>
            <tbody>`

                for (var i = 0; i < errors.length; i++) {
                    html += `  <tr>
            <th scope="row">${i+1}</th>
            <td>${errors[i]}</td>
          </tr>`
                }
                html += ` </tbody></table>`
                console.log(html)
                document.getElementById('errors').innerHTML = html
                $('#staticBackdrop').modal('show')

            }

            setTimeout(() => {
                showOriginalButton('form_button', 'Upload')
            }, 500)
        })
}


function downloadUserData() {


    fetch('/api/reports/download-users/')
        .then(response => response.json())
        .then(result => {
            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                window.location.href = `/media/${result.link}`
            } else {
                tata.error('Error', `${result.message}`)
            }
        })


}




function importUser(id) {
    fetch(`/api/reports/import-user/?id=${id}`)
        .then(response => response.json())
        .then(result => {
            if (result.status_code == 200) {
                tata.success('Success', 'File Imported')
            } else {
                tata.error('Error', 'Something went wrong')
            }
        })

}



function getUserErrors(id) {

    fetch(`/api/reports/get-user-errors/?id=${id}`)
        .then(response => response.json())
        .then(result => {
            console.log(result)
            if ((result.errors).length <= 0) {
                tata.warn('Message', 'No errors found', {
                    'position': 'tm'
                })
                return;
            }

            var errors = result.errors
            var html = `<table class="table table-striped"><thead><tr>
        <th scope="col">#</th>
        <th scope="col">Error</th>
      </tr>
    </thead>
    <tbody>`

            for (var i = 0; i < errors.length; i++) {
                html += `  <tr>
    <th scope="row">${i+1}</th>
    <td>${errors[i]}</td>
  </tr>`
            }
            // html += ` </tbody></table>`
            console.log(html)
            document.getElementById('messages').innerHTML = html
            $('#messagesModal').modal('show')


        })
}



function getRoleExcel() {
    fetch(`get-role-excel/`)
        .then(response => response.json())
        .then(result => {
            console.log(result)
            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })
                window.location.href = `/media/${result.link}`
            } else {
                tata.error('Error', 'Something went wrong')
            }


        })
}




function toggleActive(id) {

    fetch(`/accounts/toggle-active/`, {
            method: 'POST',
            headers: {
                'Authorization': 'Basic ' + btoa('admin:123'),
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify({
                'data': JSON.stringify({
                    'id': id,
                })
            })
        }).then(result => result.json())
        .then(response => {
            if (response.status_code == 200) {
                tata.success('Success', response.message)
                setTimeout(() => {
                    window.location.reload()
                }, 2000)
            } else {
                tata.error('Error', response.message)
            }

        })
}



function filterRefrral() {
    var start_date = document.getElementById('start_date').value
    var end_date = document.getElementById('end_date').value
    var specific_filter = document.getElementById('specific_filter').value
    var days_filter = document.getElementById('days_filter').value

    var url = '?'

    var count = 0

    if (((start_date.length) == 0 && end_date.length) || (start_date.length) && end_date.length == 0) {
        tata.error('Error', 'Select both start and end date.')
        return;
    }

    if ((start_date.length) && (end_date.length)) {
        count++;
        url += `&start_date=${start_date}&end_date=${end_date}`
    }

    if ((specific_filter.length)) {
        count++
        url += `&specific_filter=${specific_filter}`
    }



    console.log(days_filter)

    if ((days_filter.length) && days_filter != 'Choose') {
        count++
        url += `&days_filter=${days_filter}`
    }


    tata.success('Info', `You have selected 3 out of ${count} filters.`)

    setTimeout(() => {
        window.location.href = '/reports/referral/' + url

    }, (1000));


}



async function assignFollowups() {

    var nodes = document.querySelectorAll('#checkboxes')
    var assign_to_user = document.getElementById('assign_to_user').value
    var follow_up_title = document.getElementById('follow_up_title').value
    var follow_up_deadline = document.getElementById('follow_up_deadline').value

    if (assign_to_user.length == 0 || follow_up_title.length == 0 || follow_up_deadline.length == 0) {
        tata.error('Error', 'Please fill out all the fields')
        return
    }


    var pk_lists = []
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].checked) {
            pk_lists.push({
                'trainee_id': nodes[i].dataset.trainee_id,
                'trainee_name': nodes[i].dataset.trainee_name,
                'batch_id': nodes[i].dataset.batch_id,
                'batch_start_date': nodes[i].dataset.batch_start_date,
                'batch_end_date': nodes[i].dataset.batch_end_date,
                'applicant_id': nodes[i].dataset.applicant_id,
            })
        }
    }


    if (pk_lists.length == 0) {
        tata.error('Error', 'Please select some trainee')
        return
    }

    var data = {
        'pk_lists': pk_lists,
        'assign_to_user': assign_to_user,
        'follow_up_title': follow_up_title,
        'follow_up_deadline': follow_up_deadline

    }
    console.log(data)

    body: JSON.stringify(data)

    await fetch('/api/reports/assign-followups/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {


            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            } else {
                tata.error('Error', result.message)
            }

        })
}

function uploadFile() {
    const uploadForm = document.getElementById('uploadForm')
    const inpFile = document.getElementById('inpFile')
    const xhr = new XMLHttpRequest()
    xhr.open('POST', '')
    xhr.upload.addEventListener("progress", e => {
        console.log(e)
    })
    xhr.setRequestHeader("Content-Type", "multipart/form-data")
    xhr.send(new FormData(uploadForm))
}

async function createReferral() {
    var referrer_name = document.getElementById('referrer_name').value
    var referrer_mobile = document.getElementById('referrer_mobile').value
    var referrer_email = document.getElementById('referrer_email').value


    var referee_name = document.getElementById('referee_name').value
    var referee_email = document.getElementById('referee_email').value
    var referee_mobile = document.getElementById('referee_mobile').value

    var source = document.getElementById('source').value


    if (referrer_name == '' || referrer_mobile == '' || referee_name == '' || referee_email == '' || source == '') {
        tata.error('Error', 'All fields are required')
        return
    }


    var data = {
        'referrer_name': referrer_name,
        'referrer_mobile': referrer_mobile,
        'referee_name': referee_name,
        'referee_email': referee_email,
        'referrer_email': referrer_email,
        'referee_mobile': referee_mobile,
        'source': source
    }

    console.log(data)

    await fetch('/api/reports/create-refferal/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {


            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            } else {
                tata.error('Error', result.message)
            }

        })


}







function get_old_date(filter_days) {
    var date = null
    var d = new Date();



    //"":"2020-12-01",

    if (filter_days == 'next_1_months') {
        d.setDate(d.getDate() - 30);
        var month = d.getMonth() + 1
        if (month <= 9) {
            month += '0' + month
        }
    } else if (filter_days == 'next_2_months') {
        d.setDate(d.getDate() - 60);
    } else if (filter_days == 'next_3_months') {
        d.setDate(d.getDate() - 90);
    } else if (filter_days == 'next_6_months') {
        d.setDate(d.getDate() - 180);
    }


    var month = d.getMonth() + 1
    if (month <= 9) {
        month = '0' + month
    }



    date = d.getFullYear() + '-' + month + '-' + d.getDate()



    return date


}


async function getBatchList() {


    var isa_id = document.getElementById('isa_id').value
    var course_id = document.getElementById('course_id').value
    var batch_start_from_date = document.getElementById('batch_start_from_date').value
    var batch_start_to_date = document.getElementById('batch_start_to_date').value

    var filter_days = document.getElementById('filter_days').value

    if (filter_days != 'custom_date') {
        var d = new Date();
        var month = d.getMonth() + 1
        if (month <= 9) {
            month = '0' + month
        }

        batch_start_to_date = d.getFullYear() + '-' + month + '-' + d.getDate()
        batch_start_from_date = get_old_date(filter_days)
    }



    var data = {
        'isa_id': isa_id,
        'course_id': course_id,
        'batch_start_from_date': batch_start_from_date,
        'batch_start_to_date': batch_start_to_date,
    }

    console.log(data)



    await fetch('/api/reports/get-batch-list-api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {

            console.log(result)

            if (result.status_code == 200) {
                var html = ``

                if (result.data.length == 0) {
                    document.getElementById('not_found').innerHTML = `<p class="text-center">No bathces found</p>`
                    document.getElementById('batches_table').style = 'none'

                    return;
                }

                document.getElementById('batches_table').style = ''

                for (var i = 0; i < result.data.length; i++) {

                    html += `
                    <tr>
                    <th scope="row">${i+1}</th>
                    <td>${result.data[i].BatchName}</td>
                    <td>${result.data[i].BatchId}</td>
                    <td>${result.data[i].BatchCapacity}</td>
                    <td>${result.data[i].Course}</td>
                    <td>${result.data[i].ISAName}</td>
                    <td>${result.data[i].Shift}</td>
                    <td>${result.data[i].BatchStartDate}</td>
                    <td>${result.data[i].BatchEndDate}</td>      
                  </tr>
                  `

                }

                document.getElementById('batch_list_data').innerHTML = html


            }

        })
}

function deleteNews(id) {
    fetch(`/news/delete-news/?id=${id}`)

    tata.success('Success', 'News Deleted')

    setTimeout(() => {
        window.location.reload()
    }, 1000);

}

function toggleIsTrending(id) {
    fetch(`/news/toggle-news-trending/?id=${id}`)

    tata.success('Success', 'Trending state changed')

    setTimeout(() => {
        window.location.reload()
    }, 1000);

}

function toggleIsPublished(id) {
    fetch(`/news/toggle-news-published/?id=${id}`)

    tata.success('Success', 'Published state changed')

    setTimeout(() => {
        window.location.reload()
    }, 1000);
}



async function savePlacementPartners() {
    var name_of_company = document.getElementById('name_of_company').value
    var address = document.getElementById('address').value
    var city = document.getElementById('city').value
    var state = document.getElementById('state').value
    var name_of_person = document.getElementById('name_of_person').value
    var designation = document.getElementById('designation').value
    var mobile = document.getElementById('mobile').value
    var email = document.getElementById('email').value
    var company_type = document.getElementById('company_type').value
    var others = document.getElementById('others').value

    //name_of_the_company

    if (name_of_company == '' || address == '' || city == '' || state == '' || name_of_person == '' ||
        designation == '' || mobile == '' || email == '' || company_type == '') {
        tata.error('Error', 'All fields are required')
        return;
    }


    var data = {
        'name_of_company': name_of_company,
        'address_detail': address,
        'city': city,
        'state': state,
        'name_of_person': name_of_person,
        'designation_of_person': designation,
        'mobile_number': mobile,
        'email': email,
        'type_of_company': company_type,
        'others_div': others
    }

    console.log(data)

    await fetch('/api/create-placement-partner/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {


            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            } else {
                tata.error('Error', result.message)
            }

        })
}

function showOthers() {
    var company_type = document.getElementById('company_type')
    var others_div = document.getElementById('others_div')
    if (company_type.value == 'Others') {
        others_div.style.display = ''
    } else {
        others_div.style.display = 'none'

    }

}


async function createInterview() {

    var location = document.getElementById('isa_academy').value
    // var reason = document.getElementById('reason').value

    var name_of_company = document.getElementById('name_of_company-1').value

    var course = document.getElementById('course').value
    var designation = document.getElementById('designation-1').value
    var salary = document.getElementById('salary').value
    var contact_person = document.getElementById('contact_person').value
    var job_text = document.getElementById('job_text').value
    //var job_description_file  = document.getElementById('job_description_file').value
    var no_of_opening = document.getElementById('no_of_opening').value

    // if (reason == ''){
    //     tata.error('Error' , 'Please fill all the fields')
    //     return;
    // }

    var data = {
        'name_of_company': name_of_company,
        'location': location,
        'course': course,
        'designation': designation,
        'salary': salary,
        'contact_person': contact_person,
        'job_text': job_text,
        'no_of_opening': no_of_opening,
    }


    await fetch('/api/create-schedule-interview/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {


            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            } else {
                tata.error('Error', result.message)
            }

        })
}

async function createTreePlantation() {

    console.log(stored_files)
    

    var date_of_plantation = document.getElementById('date_of_plantation').value
    var isa_location = document.getElementById('isa_location').value
    var no_of_trees = document.getElementById('no_of_trees').value
    var varieties = document.getElementById('varieties').value
    var occasion = document.getElementById('occasion').value
    var parternship = document.getElementById('parternship').value
    var staff = document.getElementById('staff').value
    var post_plantation_care_by = document.getElementById('post_plantation_care_by').value



    let formData = new FormData();

    

    for (var i = 0; i < stored_files.length; i++) {
        formData.append("images", stored_files[i]);
    }



    formData.append("date_of_plantation", date_of_plantation);
    formData.append("isa_location", isa_location);
    formData.append("no_of_trees", no_of_trees);
    formData.append("varieties", varieties);
    formData.append("occasion", occasion);
    formData.append("parternship", parternship);
    formData.append("staff", staff);
    formData.append("post_plantation_care_by", post_plantation_care_by);


    formData.append('csrfmiddlewaretoken', csrf);


    console.log(formData)


    await fetch('/api/create-tree-plantation/', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData

        }).then(response => response.json())
        .then(result => {
            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })
                setTimeout(() => {
                    window.location.reload()
                }, 1500)
            }
        })
}


//     await fetch('/api/create-tree-plantation/', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrf,
//         },
//         body: JSON.stringify(data)
//     }).then(response => response.json())
//     .then(result => {


//         if (result.status_code == 200) {
//             tata.success('Success', `${result.message}`, {
//                 'position': 'te'
//             })

//             setTimeout(() => {
//                 window.location.reload()
//             }, 1500)

//         } else {
//             tata.error('Error', result.message)
//         }

//     })
// }


async function createWaterShed() {
    var date = document.getElementById('date').value
    var name_of_school = document.getElementById('name_of_school').value
    var name_of_village = document.getElementById('name_of_village').value
    var block = document.getElementById('block').value
    var district = document.getElementById('district').value
    var terrace = document.getElementById('terrace').value
    var reservoir_type = document.getElementById('reservoir_type').value

    var data = {
        'date': date,
        'name_of_school': name_of_school,
        'name_of_village': name_of_village,
        'block': block,
        'district': district,
        'terrace': terrace,
        'reservoir_type': reservoir_type,
    }

    let formData = new FormData();

    
    for (var i = 0; i < stored_files.length; i++) {
        formData.append("images", stored_files[i]);
    }


    formData.append("date", date);
    formData.append("name_of_school", name_of_school);
    formData.append("name_of_village", name_of_village);
    formData.append("block", block);
    formData.append("district", district);
    formData.append("terrace", terrace);
    formData.append("reservoir_type", reservoir_type);
    formData.append('csrfmiddlewaretoken', csrf);


    await fetch('/api/create-water-plantation/', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData

        }).then(response => response.json())
        .then(result => {
            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })
                setTimeout(() => {
                    window.location.reload()
                }, 1500)
            }
        })


    // await fetch('/api/create-water-plantation/', {
    //     method: 'POST',
    //     headers: {
    //         'Content-Type': 'application/json',
    //         'X-CSRFToken': csrf,
    //     },
    //     body: JSON.stringify(data)
    // }).then(response => response.json())
    // .then(result => {


    //     if (result.status_code == 200) {
    //         tata.success('Success', `${result.message}`, {
    //             'position': 'te'
    //         })

    //         setTimeout(() => {
    //             window.location.reload()
    //         }, 1500)

    //     } else {
    //         tata.error('Error', result.message)
    //     }

    // })



}



$(document).ready(function () {
    var max_fields = 10; //maximum input boxes allowed
    var wrapper = $(".input_fields_wrap"); //Fields wrapper
    var add_button = $(".add_field_button"); //Add button ID

    var x = 1; //initlal text box count
    $(add_button).click(function (e) { //on add input button click
        e.preventDefault();
        if (x < max_fields) { //max input box allowed
            x++; //text box increment
            $(wrapper).append(`
            <section class="remove-${x} mt-2">
           
        
                <div class="row ">
                    <div class="col-md-6">
                    <input type="file" onchange="loadFile(event , ${x})" class="form-control images" name="images[]"/>
                    </div>
                    <div class="col-md-3">
                <button type="button" onclick="removeElement(${x})" class="btn btn-danger  remove_field">Remove</a>
                </div>
                <div class="col-md-3">
                    <img id="output-${x}" style="height:200px" class="img-fluid img-responsive"/>
                </div>
                </section>`); //add input box
        }
    });


});

function removeElement(x) {
    console.log(x)
    $(`.remove-${x}`).remove();
}

function loadFile(event, x) {
    var output = document.getElementById(`output-${x}`);
    output.src = URL.createObjectURL(event.target.files[0]);
    output.onload = function () {
        URL.revokeObjectURL(output.src) // free memory
    }
}


// var datepickers = document.getElementById('.datepicker')

// datepickers.map(datepicker =>{
//     $( ".datepicker" ).datepicker({
//         format: 'yyyy-mm-dd'
//      });
// })



async function uploadPayments() {
    var fileupload = document.getElementById('fileupload')
    console.log('ccc')
    let formData = new FormData();
    formData.append("excel_file", fileupload.files[0]);
    formData.append('csrfmiddlewaretoken', csrf);
    await fetch('/api/reports/create-payment/', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData

        }).then(response => response.json())
        .then(result => {
            clearFileInput('fileupload')
            console.log(result)

            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

            }
        })
}


function importPayment(id) {
    fetch(`/api/reports/create-payment/?id=${id}`)
        .then(res => res.json())
        .then(result => {
            console.log(result)
        })
}



async function savePlacementRemarks(id) {

    var address_remarks = document.getElementById('address_remarks').value

    if (address_remarks == '') {
        tata.error('Error', 'Please fill all the fields')
        return;
    }

    var data = {
        'address_remarks': address_remarks,
        'id': id,
    }

    await fetch('/api/add-remarks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {


            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            } else {
                tata.error('Error', result.message)
            }

        })

}



$(document).ready(function () {
    $('#scroll_table').DataTable({
        "scrollX": true
    });
});


function validEmail(email) {
    const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function vaildPincode(pincode) {
    const re = /^[0-9]{1,6}$/;
    return re.test(pincode);

}

function sendOtp() {
    document.getElementById('show_otp').style.display = ''
    tata.success('Sucess', 'An OTP is send on your number')
    document.getElementById('otp_input').style.display = ''
}


function showOptionValidOption() {
    var program = document.getElementById('program').value

    if (program == 'ISA') {
        document.getElementById('show_isa').style.display = ''
        document.getElementById('show_rl').style.display = 'none'
        document.getElementById('show_organization').style.display = 'none'
    } else if (program == 'RL') {
        document.getElementById('show_isa').style.display = 'none'
        document.getElementById('show_rl').style.display = ''
        document.getElementById('show_organization').style.display = 'none'
    } else if (program == 'FEC') {
        document.getElementById('show_isa').style.display = 'none'
        document.getElementById('show_rl').style.display = 'none'
        document.getElementById('show_organization').style.display = ''
    } else {
        document.getElementById('show_isa').style.display = 'none'
        document.getElementById('show_rl').style.display = 'none'
        document.getElementById('show_organization').style.display = 'none'
    }
}

async function createOrganization() {
    var name = document.getElementById('name').value
    var organization_type = document.getElementById('organization_type').value
    var address = document.getElementById('address').value
    var state = document.getElementById('state').value
    var district = document.getElementById('district').value
    var city = document.getElementById('city').value
    var pincode = document.getElementById('pincode').value
    var contact_person = document.getElementById('contact_person').value
    var designation = document.getElementById('designation').value
    var mobile = document.getElementById('mobile').value
    var email = document.getElementById('email').value


    var data = {
        'name': name,
        'organization_type': organization_type,
        'address': address,
        'state': state,
        'district': district,
        'city': city,
        'pincode': pincode,
        'contact_person': contact_person,
        'designation': designation,
        'mobile': mobile,
        'email': email,
    }

    await fetch('/api/reports/create-organization/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {

            console.log(result)

            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            } else {
                tata.error('Error', result.message)
            }

        })

}

function toggleFinancialOrganization(id) {
    fetch(`/api/reports/create-organization/?id=${id}`)
        .then(result => result.json())
        .then(response => {
            if (response.status_code == 200) {
                tata.success('Success', 'Toggle Financial Organization')
                setTimeout(() => {
                    window.location.reload()
                }, 2000)
            } else {
                tata.error('Error', 'Something went wrong')

            }
        })
}


async function addFinancialOrganization() {
    var program = document.getElementById('program').value
    var isa = document.getElementById('isa').value
    var state = document.getElementById('state').value
    var district = document.getElementById('district').value
    var village = document.getElementById('village').value
    var organization = document.getElementById('organization').value
    var mode = document.getElementById('mode').value
    var location = document.getElementById('gps').value
    var topics_covered = document.getElementById('topic_covered').value
    var nature_of_participants = document.getElementById('nature_of_participants').value
    var start_time = document.getElementById('start_time').value
    var end_time = document.getElementById('end_time').value
    var no_of_events = document.getElementById('no_of_events').value
    var total_males = document.getElementById('total_males').value
    var total_females = document.getElementById('total_females').value
    var total_partipants = document.getElementById('total_participants').value
    var fileupload = document.getElementById('fileupload')



    let formData = new FormData();

    formData.append('program', program)
    formData.append('isa', isa)
    formData.append('state', state)
    formData.append('district', district)
    formData.append('village', village)
    formData.append('organization', organization)
    formData.append('mode', mode)
    formData.append('location', location)
    formData.append('topics_covered', topics_covered)
    formData.append('nature_of_participants', nature_of_participants)
    formData.append('start_time', start_time)
    formData.append('end_time', end_time)
    formData.append('no_of_events', no_of_events)
    formData.append('total_males', total_males)
    formData.append('total_females', total_females)
    formData.append('total_partipants', total_partipants)

    formData.append("excel_file", fileupload.files[0]);
    formData.append('csrfmiddlewaretoken', csrf);


    var nodes = document.querySelectorAll('.images')

    for (var i = 0; i < nodes.length; i++) {
        formData.append("images", nodes[i].files[0]);
    }


    await fetch('/api/reports/create-financial-organization/', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData

        }).then(response => response.json())
        .then(result => {
            clearFileInput('fileupload')

            if (result.status_code == 200) {
                tata.success('Success', result.message)
                setTimeout(() => {
                    window.location.reload()
                }, 1500)
            } else {
                tata.error('Error', result.message)
            }
        })
}



async function createTemplate() {

    var template_name = document.getElementById('template_name').value
    var template_html = document.getElementById('template_html').value

    var data = {
        'template_name': template_name,
        'template_html': template_html,
    }



    await fetch('/api/reports/create-certificate/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
            },
            body: JSON.stringify(data)
        }).then(response => response.json())
        .then(result => {

            console.log(result)

            if (result.status_code == 200) {
                tata.success('Success', `${result.message}`, {
                    'position': 'te'
                })

                setTimeout(() => {
                    window.location.reload()
                }, 1500)

            } else {
                tata.error('Error', result.message)
            }

        })

}


async function importImpactExcel(id){
    await fetch(`/api/reports/upload-impact-excel/?id=${id}`)
    .then(result => result.json())
    .then(response => {
        console.log(response)
        if(response.status_code == 200){
            tata.success('Success', `${response.message}`, {
                'position': 'te'
            })

            setTimeout(() => {
                window.location.reload()
            }, 1500)
        }
        else {
            tata.error('Error', `${response.message}`, {
                'position': 'tr'
            })


            setTimeout(() => {
                window.location.reload()
            }, 1500)

        }
    })
}


async function uploadImpactExcel() {
    var fileupload = document.getElementById('fileupload')
    let formData = new FormData();

    formData.append("excel_file", fileupload.files[0]);
    formData.append('csrfmiddlewaretoken', csrf);
    await fetch('/api/reports/upload-impact-excel/', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData

        }).then(response => response.json())
        .then(result => {
                clearFileInput('fileupload')
                console.log(result)

                if (result.status_code == 200) {
            
                    tata.success('Success', `${result.message}`, {
                        'position': 'te'
                    })

                    setTimeout(() => {
                        window.location.reload()
                    }, 1500)

                } else {
                    tata.error('Error', `${result.message}`, {
                        'position': 'tr'
                    })


                    setTimeout(() => {
                        showOriginalButton('form_button', 'Upload')
                    }, 500)

                }

        })
}


async function uploadJobPostingExcel(){
    var fileupload = document.getElementById('fileupload')
    let formData = new FormData();

    formData.append("excel_file", fileupload.files[0]);
    formData.append('csrfmiddlewaretoken', csrf);
    await fetch('/api/reports/upload-job-posting-excel/', {
            method: "POST",
            'X-CSRFToken': csrf,
            body: formData

        }).then(response => response.json())
        .then(result => {
                clearFileInput('fileupload')
                console.log(result)

                if (result.status_code == 200) {
            
                    tata.success('Success', `${result.message}`, {
                        'position': 'te'
                    })

                    setTimeout(() => {
                        window.location.reload()
                    }, 1500)

                } else {
                    tata.error('Error', `${result.message}`, {
                        'position': 'tr'
                    })

                    setTimeout(() => {
                        showOriginalButton('form_button', 'Upload')
                    }, 500)
                }
        })
}

function toggleJobPosting(id){
 fetch(`/api/reports/upload-job-posting-excel/?id=${id}`)
 .then(response => response.json())
 .then(result => {
     if(result.status_code == 200){
         tata.success('Success' , 'Status Changed')
     }else{
        tata.success('Error' , 'Something went wrong')

     }

     setTimeout(()=>{
         window.location.reload()
     } , 1500)
    
 })
}   


async function createJobPosting(){

  var   job_position = document.getElementById('job_position').value
  var   job_location = document.getElementById('job_location').value
  var   job_description = document.getElementById('job_description').value


    if(job_position == ''){
        tata.error('Error' , 'Job position is required')
        return;
    }

    if(job_location == ''){
        tata.error('Error' , 'Job location is required')
        return;
    }

    if(job_description == ''){
        tata.error('Error' , 'Job description is required')
        return;
    }

    var data = {
        'job_position': job_position,
        'job_location': job_location,
        'job_description': job_description,

    }
    
    await fetch('/api/reports/create-job-posting/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
    .then(result => {

        console.log(result)

        if (result.status_code == 200) {
            tata.success('Success', `${result.message}`, {
                'position': 'te'
            })

            setTimeout(() => {
                window.location.reload()
            }, 1500)

        } else {
            tata.error('Error', result.message)
        }

    })
}


async function updateJobPosting(id){

    
  var   job_position = document.getElementById('job_position').value
  var   job_location = document.getElementById('job_location').value
  var   job_description = document.getElementById('job_description').value


    if(job_position == ''){
        tata.error('Error' , 'Job position is required')
        return;
    }

    if(job_location == ''){
        tata.error('Error' , 'Job location is required')
        return;
    }

    if(job_description == ''){
        tata.error('Error' , 'Job description is required')
        return;
    }

    var data = {
        'id' : id,
        'job_position': job_position,
        'job_location': job_location,
        'job_description': job_description,

    }
    
    await fetch('/api/reports/update-job-posting/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf,
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
    .then(result => {

        console.log(result)

        if (result.status_code == 200) {
            tata.success('Success', `${result.message}`, {
                'position': 'te'
            })

            setTimeout(() => {
                window.location.reload()
            }, 1500)

        } else {
            tata.error('Error', result.message)
        }

    })

}



function refreshBirthdays(){
    document.getElementById('refresh').classList.add('fa-spin')

    setTimeout(() => {
        tata.success('Success' , 'Birthdays refreshed' )
    }, 1000);

    setTimeout(() => {
            window.location.reload()
    }, 1500);

}



