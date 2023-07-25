document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('.btn-primary').onclick = function() {
    fetch('/mailbox/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: document.querySelector('#compose-recipients').value,
          subject: document.querySelector('#compose-subject').value,
          body: document.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
      if (!result.error) {
        console.log('success')
        load_mailbox('sent')
      }
      else {
        console.log('failed')
        compose_email()
        document.querySelector('#heading').innerHTML = `New Email - <span class="text-danger">${result.error}</span>`;
      }
    })

    return false
  }

}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  const div = document.createElement('div')
  div.classList.add('list-group')
  document.querySelector('#emails-view').appendChild(div)

  fetch(`/mailbox/emails/${mailbox}`)
  .then(response => response.json())
  .then(data => {
    data.forEach(element => {
      let button = document.createElement('button')
      button.classList.add('list-group-item', 'list-group-item-action', 'justify-content-between')
      button.setAttribute('type', 'button')
      const innerHTML = `
      <div class="ms-2 me-auto">
        <div class="d-flex justify-content-between">
          <div class="fw-bold">${element.sender}</div>
          ${!element.read ? '<span class="badge bg-primary rounded-pill">New</span>' : ''}
        </div>
        <div class="d-flex justify-content-between">
          <inline>${element.subject}</inline>
          <inline>${element.timestamp}</inline>
        </div>
      </div>
      `
      if (element.read) {
        // button.style.backgroundColor = 'lightgray'
        button.classList.add('bg-secondary')
      }
      button.innerHTML = innerHTML

      button.onclick = function() {
        load_mail(element.id, mailbox==='sent')
      }

      document.querySelector('.list-group').appendChild(button)
    })
  })
  .catch(error => {
    console.log(error)
  })
}

function load_mail(mail_id, sent=false) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'block'
  document.querySelector('#compose-view').style.display = 'none'

  document.querySelector('h3').remove()
  document.querySelector('div.list-group').remove()

  fetch(`/mailbox/emails/${mail_id}`)
  .then(response => response.json())
  .then(data => {
    const ul = document.createElement('ul')
    ul.classList.add('list-group', 'list-group-flush')

    const innerHTML = `
    <li class="list-group-item">
    <p><b>From: </b>${data.sender}</p>
    <p><b>To: </b>${data.recipients.join(", ")}</p>
    <p><b>Subject: </b>${data.subject}</p>
    <p><b>Timestamp: </b>${data.timestamp}</p>
    <inline>
      <button id="reply" class="btn btn-sm btn-outline-primary">Reply</button>
      ${sent ? '' :
      `<button id="archive" class="btn btn-sm btn-outline-primary">
      ${data.archived ? 'Unarchive' : 'Archive'}
      </button>`
      }
    </inline>
    </li>
    <li class="list-group-item">${data.body}</li>
    `
    ul.innerHTML = innerHTML
    document.querySelector('#emails-view').appendChild(ul)

    if (!sent) {
      document.querySelector('#archive').addEventListener('click', () => archive(data.id, data.archived))
    }
    document.querySelector('#reply').addEventListener('click', () => reply(data))

    if (!data.read) {
      return fetch(`/mailbox/emails/${mail_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            read: true
        })
      })
    }
  })
  .then(response => {
    if (response && !response.ok) {
      load_mailbox('inbox')
    }
  })
}

function archive(mail_id, archive) {
  fetch(`/mailbox/emails/${mail_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        archived: !archive
    })
  })
  .then(response => {
    load_mailbox('inbox')
  })
}

function reply(data) {
  compose_email()

  document.querySelector('#compose-recipients').value = data.sender
  document.querySelector('#compose-subject').value = data.subject.startsWith('Re: ') ? data.subject : "Re: " + data.subject
  document.querySelector('#compose-body').value = `\n\nOn ${data.timestamp} ${data.sender} wrote:\n` + data.body
}