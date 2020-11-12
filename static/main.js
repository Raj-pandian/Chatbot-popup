const popup = document.querySelector('.chat-popup');
const chatBtn = document.querySelector('.chat-btn');

const submitBtn = document.querySelector('.submit');
const chatArea = document.querySelector('.chat-area');
const inputElm = document.querySelector('input');
// chat button toggler

chatBtn.addEventListener('click', ()=>{
    popup.classList.toggle('show');
})

        function getBotResponse() {
          var rawText = $("#textInput").val();
          let temp = '<div class="out-msg" id="dyn"><span class="my-msg">' + rawText + '</span><img src="static/img/user.svg" class="avatar" /></div>';
          console.log(rawText)
          $("#textInput").val("");
          chatArea.insertAdjacentHTML("beforeend", temp);

          $.get("/get", { msg: rawText }).done(function(data) {
          console.log(data)
          let temp1 = '<div class="bot-msg" id="dyn"><img src="{{ url_for("static", filename="bot.svg")}}" class="avatar" /><span class="msg">' + data + '</span></div>';
          chatArea.insertAdjacentHTML("beforeend", temp1);
          });
        }
        $("#textInput").keypress(function(e) {
          if (e.which == 13) {
            getBotResponse();
          }
        }
        );
function deleteAllInputs() {
    $('.out-msg').remove();
    $('.bot-msg').remove();
}