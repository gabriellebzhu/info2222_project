</p>

<div class="chatbox">
  <div class="user-column">
    <p>
      Welcome back, {{username}}! {{err_msg}}
      <br>
      Select a friend to chat with:
    </p>

    <ul>
      % for i in range(0, len(friend_usernames)):
        <li>
          <a href="/chat/{{friend_ids[i]}}">{{friend_usernames[i]}}</a>
        </li>
      % end
    </ul>
  </div>

  <div class="chat-column">
    <ul id="messages"></ul>

    <form id="message-form" action="">
      <input id="msg-input" autocomplete="off">
      <button>Send</button>
    </form>
  </div>
</div>