<div class="chatbox">
  <div class="user-column">
    <p>
      Welcome back, {{username}}! {{err_msg}}
      <br>
      Select a friend to chat with:
    </p>

    <ul id="friend-list">
      % for i in range(0, len(friend_usernames)):
        <li>
          <a href="/chat/{{friend_ids[i]}}">{{friend_usernames[i]}}</a>
        </li>
      % end
    </ul>
  </div>

  <div class="chat-column">
    <ul id=message-list>
      % for i in range(0, len(old_chat)):
          % if old_chat[i][0] == username:
          <li class="curr-user-msg"><b>{{old_chat[i][0]}}:</b> {{old_chat[i][1]}}</li>
          % else:
          <li class="friend-user-msg"><b>{{old_chat[i][0]}}:</b> {{old_chat[i][1]}}</li>
          % end
      % end
    </ul>

    <form id="message-form">
      <input id="msg-input" autocomplete="off">
      <button type="submit">Send</button>
    </form>
  </div>
</div>

<script type="text/javascript">
  window.username = "{{!username}}";
  window.friend_pk = "{{!friend_pk}}";
  window.old_chat_len = "{{!len(old_chat)}}";
</script>

<script src="js/chat_bundle.js"></script>
