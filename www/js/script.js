var chat_content = document.getElementsByClassName("chat-content")[0]
var attach_image_input = document.getElementsByClassName("attach-image-input")[0]
var attach_image_button = document.getElementsByClassName("attach-image-button")[0]
var remove_image_button = document.getElementsByClassName("remove-image-button")[0]
var image_src = document.getElementsByClassName("image-src")[0]
var send_button = document.getElementsByClassName("send-button")[0]
var message_box = document.getElementsByClassName("message-box")[0]

var image_file = ""

const MIN_HEIGHT = 720
const MIN_WIDTH = 1280


send_button.addEventListener("click", send_message)


attach_image_button.addEventListener("click", () => {
  if (image_file == "") {
    attach_image_input.click()
    message_box.focus()
    return
  }

  image_file = ""
  image_src.classList.add("hidden")
  remove_image_button.classList.add("hidden")
})

attach_image_input.onclick = (e) => {
  e.target.value = null;
}

attach_image_input.onchange = () => {
  var reader = new FileReader()
  var file = attach_image_input.files[0]
  
  reader.addEventListener("load", () => {
    image_file = reader.result
    image_src.src = image_file
    image_src.classList.remove("hidden")
    remove_image_button.classList.remove("hidden")
  })

  if (file) {
    reader.readAsDataURL(file)
  } else {
    image_file == ""
    image_src.classList.add("hidden")
    remove_image_button.classList.add("hidden")
  }
}

remove_image_button.addEventListener("click", () => {
  image_file = ""
  image_src.classList.add("hidden")
  remove_image_button.classList.add("hidden")
})

message_box.addEventListener("keyup", event => {

  if (event.keyCode === 13) {
    send_message()
  } else if (event.keyCode === 27) {
    message_box.blur()
  }
})

function log(message) {
  eel.log(message)
}


function send_message() {
  let text = message_box.value
  let image = image_file

  if (text === "" & image === "") {
    return
  }

  let msg = {
    text: text,
    image: image
  }
  
  add_user_message(msg)

  message_box.value = ""
  message_box.focus()

  image_file = ""
  image_src.classList.add("hidden")
  remove_image_button.classList.add("hidden")

  eel.on_message(msg)
}


function add_user_message(message) {

  text = message.text
  image = message.image

  if (text) {
    textNode = document.createElement('div')
    textNode.classList.add("chat")
    textNode.classList.add("outgoing")

    detailsNode = document.createElement('div')
    detailsNode.classList.add("details")

    pNode = document.createElement('p')
    pNode.textContent = text

    detailsNode.append(pNode)
    textNode.append(detailsNode)

    chat_content.append(textNode)
  }

  if (image) {
    chat_content.innerHTML += 
    `<div class="chat outgoing">
        <div class="details">
          <image src="${image}" alt="Image">
        </div>
      </div>`
  }
  scrollToBottom()
}

function add_bot_message(message) {

  let text = message.text
  let image = message.image
  
  if (text) {
    textNode = document.createElement('div')
    textNode.classList.add("chat")
    textNode.classList.add("incoming")

    detailsNode = document.createElement('div')
    detailsNode.classList.add("details")

    pNode = document.createElement('p')
    pNode.textContent = text

    detailsNode.append(pNode)
    textNode.append(detailsNode)

    chat_content.append(textNode)
  }

  if (image) {
    chat_content.innerHTML += 
      `<div class="chat incoming">
         <div class="details">
           <image src="${image}">
           <div class="image-options">
             <button class="image-option save-image-button">
               <img class="save-image-button-bg" src="images/save-button.png">
             </button>
           </div>
         </div>
       </div>`

    var save_image_buttons = document.getElementsByClassName("save-image-button")
    var save_image_button = save_image_buttons[save_image_buttons.length - 1]

    save_image_button.addEventListener("click", () => {
      eel.save_image(image)
    })
  }
  
  scrollToBottom()
}

function download(url, filename) {
  fetch(url)
    .then(response => response.blob())
    .then(blob => {
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      link.click();
  })
  .catch(console.error);
}



window.addEventListener("load", () => {
  window.resizeTo(MIN_WIDTH, MIN_HEIGHT)
  msg1 = {
    text: "Hi",
    image: null
  }
  msg2 = {
    text: "Type \"help\" to list all commands.!",
    image: null
  }
  add_bot_message(msg1)
  add_bot_message(msg2)
})


window.addEventListener("resize", () => {

  if (window.outerWidth < MIN_WIDTH) {
    window.resizeTo(MIN_WIDTH, window.outerHeight)
  }

  if (window.outerHeight < MIN_HEIGHT) {
    window.resizeTo(window.outerWidth, MIN_HEIGHT)
  }
})

function scrollToBottom() {
  setTimeout(function() {
    _scrollToBottom()
  }, 10)
}

function _scrollToBottom() {
  chat_content.scrollTop = chat_content.scrollHeight
}

eel.expose(add_bot_message)