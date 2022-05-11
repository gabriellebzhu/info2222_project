<div class="chatbox">
  <div class="user-column">
    <div>
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

    <div class="add-friend-list">
      <a href="/friends">Add Friend</a>
    </div>
  </div>

  <div class="chat-column">
    <ul id=message-list>
    </ul>

    <form id="message-form">
      <input id="msg-input" autocomplete="off">
      <button type="submit">Send</button>
    </form>
  </div>
</div>

<script type="text/javascript">
  window.username = "{{!username}}";
  window.friendPk = "{{!friend_pk}}";
  window.oldChat = {{!old_chat2}};
  window.keyAndIv = "{{!key_and_iv}}";
  window.friendId = "{{!friend_id}}";
</script>

<script src="js/chat_bundle.js"></script>
